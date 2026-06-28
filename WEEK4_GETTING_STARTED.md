# Getting Started: Week 4

## Step 0: Confirm Weeks 1–3 are done

This script needs `data/raw_prices.csv` and `data/daily_returns.csv` (Week 1), and imports functions from `analyze_risk.py` (Week 2) and `optimize_portfolio.py` (Week 3) — so those files need to already exist in the folder (they do, from previous weeks) and Week 1's data needs to have actually been generated.

```
dir data
```

Confirm `raw_prices.csv` and `daily_returns.csv` are there.

## Step 1: Activate your environment

```
.venv\Scripts\Activate.ps1
```

No new libraries needed this week — everything was installed back in Week 1/3.

## Step 2: Run the backtest

```
python backtest_strategy.py
```

This will take a bit longer than previous weeks' scripts — it's running the full optimization process roughly a dozen times (once per rebalance) instead of once.

Expected output: a line stating the out-of-sample date range and number of rebalances, then a 3-row comparison table (Walk-Forward Max Sharpe / Equal Weighted / S&P 500).

## Step 3: Check the outputs

```
dir data
dir plots
```

New files: `data/backtest_comparison.csv`, `data/backtest_weight_history.csv`, `plots/backtest_comparison.png`.

Open `backtest_weight_history.csv` in Excel — look at how much the weights jump around between consecutive rows. Open `backtest_comparison.png` — three lines tracking cumulative return over the same out-of-sample window.

Don't be surprised or worried if the optimized strategy doesn't clearly win — see the Week 4 walkthrough for why that's a legitimate, expected outcome worth discussing rather than something to fix.

## Step 4: Commit and push

```
git add .
git commit -m "Week 4: walk-forward backtest"
git push
```

## Week 4 done-checklist

- [ ] `python backtest_strategy.py` runs with no errors
- [ ] `data/backtest_comparison.csv` and `data/backtest_weight_history.csv` exist and look reasonable
- [ ] `plots/backtest_comparison.png` shows three comparable cumulative return lines
- [ ] Pushed to GitHub

## Next

Week 5: wrap Weeks 1–4 into an interactive Streamlit dashboard. Let me know when this week's checked off.
