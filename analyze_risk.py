"""
Week 2: risk & return analytics.

Loads the daily/cumulative returns produced by fetch_data.py and computes,
per ticker:
    - annualized return
    - annualized volatility
    - Sharpe ratio
    - max drawdown

Also computes the correlation matrix across tickers and saves two charts.

Run (after fetch_data.py has been run at least once):
    python analyze_risk.py
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_DIR = "data"
PLOTS_DIR = "plots"

TRADING_DAYS_PER_YEAR = 252

# Annualized risk-free rate, used for the Sharpe ratio. This is an assumption,
# not live data — roughly tracks short-term T-bill yields. Update it if you
# want a more precise comparison.
RISK_FREE_RATE = 0.04


# --- Metrics ---------------------------------------------------------------

def annualized_return(daily_returns):
    """Geometric (compounded) annualized return per column."""
    total_growth = (1 + daily_returns).prod()
    n_years = len(daily_returns) / TRADING_DAYS_PER_YEAR
    return total_growth ** (1 / n_years) - 1


def annualized_volatility(daily_returns):
    """Annualized standard deviation of returns per column."""
    return daily_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def sharpe_ratio(ann_return, ann_vol, risk_free_rate=RISK_FREE_RATE):
    """Risk-adjusted return: excess return per unit of volatility."""
    return (ann_return - risk_free_rate) / ann_vol


def max_drawdown(daily_returns):
    """Largest peak-to-trough decline per column, as a negative fraction."""
    wealth_index = (1 + daily_returns).cumprod()
    running_max = wealth_index.cummax()
    drawdown = wealth_index / running_max - 1
    return drawdown.min()


def build_metrics_table(daily_returns):
    ann_ret = annualized_return(daily_returns)
    ann_vol = annualized_volatility(daily_returns)
    sharpe = sharpe_ratio(ann_ret, ann_vol)
    mdd = max_drawdown(daily_returns)

    metrics = pd.DataFrame({
        "annualized_return": ann_ret,
        "annualized_volatility": ann_vol,
        "sharpe_ratio": sharpe,
        "max_drawdown": mdd,
    })
    return metrics.sort_values("sharpe_ratio", ascending=False)


# --- Charts ------------------------------------------------------------

def plot_cumulative_returns(cumulative_returns):
    os.makedirs(PLOTS_DIR, exist_ok=True)
    plt.figure(figsize=(10, 6))
    for col in cumulative_returns.columns:
        plt.plot(cumulative_returns.index, cumulative_returns[col], label=col)
    plt.title("Cumulative Returns")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend(loc="upper left", fontsize=8)
    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "cumulative_returns.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def plot_correlation_heatmap(corr):
    os.makedirs(PLOTS_DIR, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, label="Correlation")
    ax.set_title("Return Correlation Matrix")
    fig.tight_layout()
    path = os.path.join(PLOTS_DIR, "correlation_heatmap.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


# --- Main ---------------------------------------------------------------

def main():
    daily_returns_path = os.path.join(DATA_DIR, "daily_returns.csv")
    cumulative_returns_path = os.path.join(DATA_DIR, "cumulative_returns.csv")

    if not os.path.exists(daily_returns_path):
        raise FileNotFoundError(
            f"{daily_returns_path} not found. Run fetch_data.py first (Week 1) "
            "to generate the returns data this script depends on."
        )

    daily_returns = pd.read_csv(daily_returns_path, index_col=0, parse_dates=True)
    cumulative_returns = pd.read_csv(cumulative_returns_path, index_col=0, parse_dates=True)

    metrics = build_metrics_table(daily_returns)
    metrics.to_csv(os.path.join(DATA_DIR, "risk_metrics.csv"))

    corr = daily_returns.corr()
    corr.to_csv(os.path.join(DATA_DIR, "correlation_matrix.csv"))

    cum_path = plot_cumulative_returns(cumulative_returns)
    corr_path = plot_correlation_heatmap(corr)

    print("Risk & return metrics (sorted by Sharpe ratio, best first):\n")
    print(metrics.round(3))
    print(f"\nSaved metrics to {DATA_DIR}/risk_metrics.csv and {DATA_DIR}/correlation_matrix.csv")
    print(f"Saved charts to {cum_path} and {corr_path}")


if __name__ == "__main__":
    main()
