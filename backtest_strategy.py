"""
Week 4: walk-forward backtest of the Max-Sharpe strategy.

Naively "backtesting" Week 3's optimizer would mean computing portfolio
weights using the FULL history, then checking performance over that same
history. That's look-ahead bias: the optimizer would have known the future.

This script avoids that by re-optimizing periodically using only data
available up to that point ("walk-forward" backtesting), then measuring
realized performance only on data the optimizer never saw when it chose
those weights. It compares the result against buy-and-hold equal-weighted
and the S&P 500 over the exact same out-of-sample period.

Run (after fetch_data.py has been run at least once):
    python backtest_strategy.py
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

from analyze_risk import annualized_return, annualized_volatility, max_drawdown
from optimize_portfolio import BENCHMARK, estimate_inputs, optimize_max_sharpe

DATA_DIR = "data"
PLOTS_DIR = "plots"

LOOKBACK_DAYS = 504     # ~2 trading years of history used to set each rebalance's weights
REBALANCE_EVERY = 63    # ~1 trading quarter between rebalances

# Keep in sync with the same assumption in analyze_risk.py / optimize_portfolio.py
RISK_FREE_RATE = 0.04


# --- Data ---------------------------------------------------------------

def load_data():
    prices_path = os.path.join(DATA_DIR, "raw_prices.csv")
    returns_path = os.path.join(DATA_DIR, "daily_returns.csv")
    if not (os.path.exists(prices_path) and os.path.exists(returns_path)):
        raise FileNotFoundError(
            "data/raw_prices.csv and data/daily_returns.csv not found. "
            "Run fetch_data.py first (Week 1)."
        )
    prices = pd.read_csv(prices_path, index_col=0, parse_dates=True)
    daily_returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    stock_cols = [c for c in prices.columns if c != BENCHMARK]
    return prices[stock_cols], daily_returns[stock_cols], daily_returns[BENCHMARK]


# --- Walk-forward backtest ------------------------------------------------

def get_rebalance_positions(n_periods, lookback_days=LOOKBACK_DAYS, rebalance_every=REBALANCE_EVERY):
    """Trading-day positions at which we re-optimize. The first one is the
    earliest point that has a full lookback window of history behind it."""
    return list(range(lookback_days, n_periods, rebalance_every))


def run_walk_forward(stock_prices, stock_returns):
    n = len(stock_prices)
    rebalance_positions = get_rebalance_positions(n)

    segment_returns = []
    weight_history = {}

    for i, pos in enumerate(rebalance_positions):
        segment_end = rebalance_positions[i + 1] if i + 1 < len(rebalance_positions) else n

        # Estimate weights using ONLY data strictly before `pos`. Everything
        # from `pos` to `segment_end` is data the optimizer never saw.
        lookback_window = stock_prices.iloc[pos - LOOKBACK_DAYS: pos]
        mu, cov = estimate_inputs(lookback_window)
        weights_dict, _ = optimize_max_sharpe(mu, cov)
        weights = pd.Series(weights_dict)

        weight_history[stock_prices.index[pos]] = weights

        holding_period_returns = stock_returns.iloc[pos:segment_end][weights.index]
        portfolio_returns = holding_period_returns @ weights
        segment_returns.append(portfolio_returns)

    walk_forward_returns = pd.concat(segment_returns)
    weight_history_df = pd.DataFrame(weight_history).T.fillna(0)
    return walk_forward_returns, weight_history_df


def equal_weighted_returns(stock_returns):
    return stock_returns.mean(axis=1)


# --- Performance summary ------------------------------------------------

def summarize(returns, risk_free_rate=RISK_FREE_RATE):
    ann_ret = annualized_return(returns)
    ann_vol = annualized_volatility(returns)
    sharpe = (ann_ret - risk_free_rate) / ann_vol
    mdd = max_drawdown(returns)
    total_return = (1 + returns).prod() - 1
    return {
        "total_return": total_return,
        "annualized_return": ann_ret,
        "annualized_volatility": ann_vol,
        "sharpe_ratio": sharpe,
        "max_drawdown": mdd,
    }


# --- Chart ---------------------------------------------------------------

def plot_comparison(series_dict):
    os.makedirs(PLOTS_DIR, exist_ok=True)
    plt.figure(figsize=(10, 6))
    for label, returns in series_dict.items():
        cumulative = (1 + returns).cumprod() - 1
        plt.plot(cumulative.index, cumulative, label=label)
    plt.title("Out-of-Sample Backtest: Walk-Forward Max Sharpe vs. Benchmarks")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "backtest_comparison.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


# --- Main ---------------------------------------------------------------

def main():
    stock_prices, stock_returns, benchmark_returns = load_data()

    walk_forward_returns, weight_history_df = run_walk_forward(stock_prices, stock_returns)

    # Compare everyone over the EXACT same out-of-sample window for fairness.
    eval_equal_returns = equal_weighted_returns(stock_returns).loc[walk_forward_returns.index]
    eval_benchmark_returns = benchmark_returns.loc[walk_forward_returns.index]

    results = {
        "Walk-Forward Max Sharpe": summarize(walk_forward_returns),
        "Equal Weighted": summarize(eval_equal_returns),
        "S&P 500": summarize(eval_benchmark_returns),
    }
    comparison = pd.DataFrame(results).T
    comparison.to_csv(os.path.join(DATA_DIR, "backtest_comparison.csv"))
    weight_history_df.to_csv(os.path.join(DATA_DIR, "backtest_weight_history.csv"))

    chart_path = plot_comparison({
        "Walk-Forward Max Sharpe": walk_forward_returns,
        "Equal Weighted": eval_equal_returns,
        "S&P 500": eval_benchmark_returns,
    })

    n_rebalances = len(get_rebalance_positions(len(stock_prices)))
    print(f"Out-of-sample window: {walk_forward_returns.index[0].date()} to {walk_forward_returns.index[-1].date()}")
    print(f"({n_rebalances} rebalances, ~every {REBALANCE_EVERY} trading days, "
          f"{LOOKBACK_DAYS}-day lookback for each)\n")
    print(comparison.round(3))
    print(f"\nSaved comparison to {DATA_DIR}/backtest_comparison.csv")
    print(f"Saved weight history to {DATA_DIR}/backtest_weight_history.csv")
    print(f"Saved chart to {chart_path}")


if __name__ == "__main__":
    main()
