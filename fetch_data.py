"""
Week 1: data pipeline.

Pulls historical daily prices for a diversified stock universe + the S&P 500
benchmark, cleans the data, and computes daily/cumulative returns.

Run:
    python fetch_data.py
"""

import os

import pandas as pd
import yfinance as yf

# --- Config ------------------------------------------------------------

# Ticker -> sector, just for documentation/reference (not used in the math)
TICKERS = {
    "AAPL": "Technology",
    "MSFT": "Technology",
    "JNJ": "Healthcare",
    "JPM": "Financials",
    "XOM": "Energy",
    "PG": "Consumer Staples",
    "AMZN": "Consumer Discretionary",
    "CAT": "Industrials",
    "NEE": "Utilities",
    "DIS": "Communication Services",
}

BENCHMARK = "^GSPC"  # S&P 500

PERIOD = "5y"     # how far back to pull
INTERVAL = "1d"   # daily data

DATA_DIR = "data"


# --- Pipeline ------------------------------------------------------------

def fetch_prices(tickers, benchmark, period=PERIOD, interval=INTERVAL):
    """Download adjusted close prices for a list of tickers plus a benchmark."""
    all_tickers = list(tickers) + [benchmark]
    print(f"Downloading {len(all_tickers)} tickers: {all_tickers}")

    raw = yf.download(
        all_tickers, period=period, interval=interval, auto_adjust=True, progress=False
    )

    # yf.download returns a MultiIndex column (field, ticker) when given
    # multiple tickers. With auto_adjust=True, "Close" is already the
    # adjusted close.
    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"]
    else:
        # Single-ticker edge case: columns are just field names.
        prices = raw[["Close"]].rename(columns={"Close": all_tickers[0]})

    return prices


def clean_prices(prices):
    """Drop tickers with too much missing history, then fill small gaps."""
    min_obs = int(len(prices) * 0.9)
    prices = prices.dropna(axis=1, thresh=min_obs)  # drop tickers missing >10% of history
    prices = prices.ffill().dropna()  # forward-fill small gaps, drop any remaining NaN rows
    return prices


def compute_returns(prices):
    """Compute daily simple returns and cumulative returns from a price series."""
    daily_returns = prices.pct_change().dropna()
    cumulative_returns = (1 + daily_returns).cumprod() - 1
    return daily_returns, cumulative_returns


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    prices = fetch_prices(TICKERS, BENCHMARK)
    prices = clean_prices(prices)
    daily_returns, cumulative_returns = compute_returns(prices)

    prices.to_csv(os.path.join(DATA_DIR, "raw_prices.csv"))
    daily_returns.to_csv(os.path.join(DATA_DIR, "daily_returns.csv"))
    cumulative_returns.to_csv(os.path.join(DATA_DIR, "cumulative_returns.csv"))

    print(f"\nSaved {len(prices)} rows x {len(prices.columns)} tickers to {DATA_DIR}/")
    print("\nLatest cumulative returns (highest to lowest):")
    print(cumulative_returns.iloc[-1].sort_values(ascending=False).round(3))


if __name__ == "__main__":
    main()
