# Getting Started: Week 2

Picks up right where Week 1 left off. Same terminal habits as before.

## Step 0: Make sure Week 1 actually finished

Week 2 reads the files Week 1 creates, so it won't run without them. Check:

```
dir data
```

You need to see `daily_returns.csv` and `cumulative_returns.csv` in there. If you don't, go back to `GETTING_STARTED.md` and run `python fetch_data.py` first.

## Step 1: Open a terminal and activate your environment

Same as Week 1 — open PowerShell in the `portfolio-optimizer` folder, then:

```
.venv\Scripts\Activate.ps1
```

Your prompt should show `(.venv)`. If you closed your terminal since Week 1, you'll need to do this again — it doesn't stay active between sessions.

No new libraries are needed for Week 2 — `matplotlib` and `numpy` were already installed in Week 1's `pip install -r requirements.txt`.

## Step 2: Run the analytics script

```
python analyze_risk.py
```

Expected output: a printed table with one row per ticker, showing annualized return, volatility, Sharpe ratio, and max drawdown, sorted best-to-worst by Sharpe ratio. Then two lines confirming what got saved.

## Step 3: Check the outputs

```
dir data
dir plots
```

You should now additionally have `risk_metrics.csv` and `correlation_matrix.csv` in `data/`, plus a new `plots/` folder containing `cumulative_returns.png` and `correlation_heatmap.png`.

Open `risk_metrics.csv` in Excel the same way as last week. Open the two `.png` files by double-clicking them (they'll open in Photos or your default image viewer) — the cumulative returns chart should show several lines trending generally upward over the 5-year window, and the heatmap should be a colored grid of correlation values between -1 and 1.

If a number looks clearly broken (e.g., volatility of 500%, or every Sharpe ratio is identical), paste what you're seeing back to me.

## Step 4: Commit and push

```
git add .
git commit -m "Week 2: risk and return analytics"
git push
```

(No need to repeat `git remote add origin` — that's a one-time setup from Week 1.)

## Week 2 done-checklist

- [ ] `python analyze_risk.py` runs with no errors
- [ ] `data/risk_metrics.csv` and `data/correlation_matrix.csv` exist and look reasonable
- [ ] `plots/cumulative_returns.png` and `plots/correlation_heatmap.png` exist and render correctly
- [ ] Pushed to GitHub

## Next

Week 3: feed these return and correlation numbers into an optimizer (`PyPortfolioOpt`) to build an actual risk-optimized portfolio. Let me know when this week is checked off.
