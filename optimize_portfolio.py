"""
Week 3: portfolio optimization (Modern Portfolio Theory).

Uses PyPortfolioOpt to find the max-Sharpe and minimum-volatility portfolios
from the Week 1 price history, plots the efficient frontier, and compares
the optimized portfolios against a naive equal-weighted portfolio and the
S&P 500 benchmark.

Run (after fetch_data.py has been run at least once):
    python optimize_portfolio.py
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pypfopt import EfficientFrontier, expected_returns, plotting, risk_models

from analyze_risk import annualized_return, annualized_volatility

DATA_DIR = "data"
PLOTS_DIR = "plots"

BENCHMARK = "^GSPC"

# Keep this in sync with the same assumption in analyze_risk.py.
RISK_FREE_RATE = 0.04


# --- Data ---------------------------------------------------------------

def load_prices():
    path = os.path.join(DATA_DIR, "raw_prices.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{path} not found. Run fetch_data.py first (Week 1) to generate it."
        )
    prices = pd.read_csv(path, index_col=0, parse_dates=True)
    # The optimizer chooses among the stocks we could actually hold — drop
    # the benchmark from that universe, but keep its prices for comparison.
    stock_prices = prices.drop(columns=[BENCHMARK])
    benchmark_prices = prices[BENCHMARK]
    return stock_prices, benchmark_prices


def estimate_inputs(stock_prices):
    """Modern Portfolio Theory needs exactly two inputs per asset universe:
    an expected return for each asset, and a covariance matrix describing
    how every pair of assets moves together."""
    mu = expected_returns.mean_historical_return(stock_prices)
    cov = risk_models.sample_cov(stock_prices)
    return mu, cov


# --- Portfolios ---------------------------------------------------------

def optimize_max_sharpe(mu, cov):
    ef = EfficientFrontier(mu, cov)
    ef.max_sharpe(risk_free_rate=RISK_FREE_RATE)
    weights = ef.clean_weights()
    performance = ef.portfolio_performance(risk_free_rate=RISK_FREE_RATE)
    return weights, performance


def optimize_min_volatility(mu, cov):
    ef = EfficientFrontier(mu, cov)
    ef.min_volatility()
    weights = ef.clean_weights()
    performance = ef.portfolio_performance(risk_free_rate=RISK_FREE_RATE)
    return weights, performance


def equal_weighted_performance(mu, cov):
    """A naive 1/N portfolio — the baseline every optimizer should beat
    on a risk-adjusted basis, otherwise the optimization isn't earning
    its complexity."""
    n = len(mu)
    weights = pd.Series(1 / n, index=mu.index)
    ret = float(weights @ mu)
    vol = float(np.sqrt(weights @ cov @ weights))
    sharpe = (ret - RISK_FREE_RATE) / vol
    return weights.to_dict(), (ret, vol, sharpe)


def benchmark_performance(benchmark_prices):
    benchmark_returns = benchmark_prices.pct_change().dropna()
    ann_return = annualized_return(benchmark_returns)
    ann_vol = annualized_volatility(benchmark_returns)
    sharpe = (ann_return - RISK_FREE_RATE) / ann_vol
    return ann_return, ann_vol, sharpe


# --- Chart ---------------------------------------------------------------

def plot_frontier(mu, cov, marked_portfolios):
    """marked_portfolios: dict of label -> (return, volatility) to star on the chart."""
    os.makedirs(PLOTS_DIR, exist_ok=True)

    # Use a fresh EfficientFrontier instance purely for drawing the curve —
    # plot_efficient_frontier sweeps across many target returns internally.
    ef = EfficientFrontier(mu, cov)
    fig, ax = plt.subplots(figsize=(9, 6))
    plotting.plot_efficient_frontier(ef, ax=ax, show_assets=True)

    for label, (ret, vol) in marked_portfolios.items():
        ax.scatter(vol, ret, marker="*", s=250, label=label, zorder=5)

    ax.set_title("Efficient Frontier")
    ax.legend()
    fig.tight_layout()
    path = os.path.join(PLOTS_DIR, "efficient_frontier.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


# --- Main ---------------------------------------------------------------

def main():
    stock_prices, benchmark_prices = load_prices()
    mu, cov = estimate_inputs(stock_prices)

    max_sharpe_weights, max_sharpe_perf = optimize_max_sharpe(mu, cov)
    min_vol_weights, min_vol_perf = optimize_min_volatility(mu, cov)
    equal_weights, equal_perf = equal_weighted_performance(mu, cov)
    bench_perf = benchmark_performance(benchmark_prices)

    weights_table = pd.DataFrame({
        "max_sharpe": max_sharpe_weights,
        "min_volatility": min_vol_weights,
        "equal_weighted": equal_weights,
    }).fillna(0)
    weights_table.to_csv(os.path.join(DATA_DIR, "portfolio_weights.csv"))

    comparison = pd.DataFrame(
        [max_sharpe_perf, min_vol_perf, equal_perf, bench_perf],
        index=["Max Sharpe", "Min Volatility", "Equal Weighted", "S&P 500"],
        columns=["expected_return", "volatility", "sharpe_ratio"],
    )
    comparison.to_csv(os.path.join(DATA_DIR, "portfolio_comparison.csv"))

    frontier_path = plot_frontier(mu, cov, {
        "Max Sharpe": (max_sharpe_perf[0], max_sharpe_perf[1]),
        "Min Volatility": (min_vol_perf[0], min_vol_perf[1]),
        "Equal Weighted": (equal_perf[0], equal_perf[1]),
    })

    print("Portfolio comparison (expected return is forward-looking from historical data,")
    print("not a guarantee — see the Week 3 walkthrough for caveats):\n")
    print(comparison.round(3))

    print("\nMax-Sharpe portfolio weights (non-zero only):")
    print(pd.Series(max_sharpe_weights).round(3).replace(0, np.nan).dropna())

    print(f"\nSaved weights to {DATA_DIR}/portfolio_weights.csv")
    print(f"Saved comparison to {DATA_DIR}/portfolio_comparison.csv")
    print(f"Saved chart to {frontier_path}")


if __name__ == "__main__":
    main()
