# Getting Started: Week 3

## Step 0: Confirm Weeks 1–2 are done

This script needs `data/raw_prices.csv` (from Week 1). Check:

```
dir data
```

If `raw_prices.csv` isn't there, go back and run `python fetch_data.py` first.

## Step 1: Activate your environment

```
.venv\Scripts\Activate.ps1
```

## Step 2: Install this week's new library

`PyPortfolioOpt` was already listed in `requirements.txt` from the start, but if you set up your environment before this week, install it now to be sure:

```
pip install -r requirements.txt
```

This is safe to run anytime — it skips anything already installed.

## Step 3: Run the optimizer

```
python optimize_portfolio.py
```

Expected output: a 4-row comparison table (Max Sharpe / Min Volatility / Equal Weighted / S&P 500) with return, volatility, and Sharpe ratio columns, followed by the list of non-zero weights in the Max Sharpe portfolio.

## Step 4: Check the outputs

```
dir data
dir plots
```

New files: `data/portfolio_weights.csv`, `data/portfolio_comparison.csv`, and `plots/efficient_frontier.png`.

Open `portfolio_weights.csv` in Excel — you'll see three columns (max_sharpe, min_volatility, equal_weighted), one row per stock, showing what fraction of the portfolio each strategy puts into each stock. Open `efficient_frontier.png` — you should see a curved line (the frontier), scattered dots (your individual stocks), and three star markers for the three portfolios.

If `pip install` fails specifically on `PyPortfolioOpt` (it occasionally needs a C++ build tool on Windows), let me know the exact error — there's usually a workaround.

## Step 5: Commit and push

```
git add .
git commit -m "Week 3: portfolio optimization"
git push
```

## Week 3 done-checklist

- [ ] `python optimize_portfolio.py` runs with no errors
- [ ] `data/portfolio_weights.csv` and `data/portfolio_comparison.csv` look reasonable (weights sum to ~1 in each column)
- [ ] `plots/efficient_frontier.png` shows a frontier curve with star markers
- [ ] Pushed to GitHub

## Next

Week 4: backtest a simple strategy (e.g., periodically rebalancing to the Max Sharpe weights) over historical time and compare its realized performance to just holding the S&P 500. Let me know when this week's checked off.
