# Week 4 Walkthrough: Walk-Forward Backtesting

Week 3 produced a Max-Sharpe portfolio and reported it would have returned X% with volatility Y% — but that number was computed using the *entire* 5-year history at once. This week explains why that's misleading, and fixes it.

## The problem: look-ahead bias

If you optimize using all 5 years of data, then report performance over that same 5 years, the optimizer effectively got to "see the future" when it chose its weights — it picked the exact combination that worked best *in hindsight*, for the period you're now claiming to predict. That's not a backtest, it's curve-fitting. Any result from doing this is close to meaningless, no matter how good the Sharpe ratio looks.

This is one of the most common mistakes in amateur quant projects, and explicitly avoiding it is one of the strongest signals of rigor you can show in this project.

## The fix: walk-forward backtesting

Instead of one optimization using all the data, we do many small optimizations, each one only allowed to see data *before* the period it's being judged on:

1. At each rebalance point, look back at the trailing ~2 years of prices (`LOOKBACK_DAYS = 504` trading days)
2. Run the exact same Max-Sharpe optimization from Week 3 on that trailing window only
3. Hold those weights for the next ~quarter (`REBALANCE_EVERY = 63` trading days) — this is the "out-of-sample" period, since the optimizer never saw it
4. Record how the portfolio actually performed during that quarter
5. Move forward to the next rebalance point and repeat, using a new trailing window that now includes the quarter just finished

String all those quarters together and you get a continuous, honest performance history — one where, at every single point in time, the weights being used were chosen using only information that would have actually been available then. This is the standard technique professional quant research uses, called walk-forward analysis (or walk-forward optimization).

## Why we also need a warm-up period

The very first rebalance can't happen on day 1 — there's no trailing 2 years of history yet to estimate from. `LOOKBACK_DAYS` worth of data at the start of your 5-year window is "spent" purely as a warm-up; backtest evaluation only starts once a full lookback window is available (~2 years in, leaving roughly 3 years of genuine out-of-sample evaluation in our 5-year dataset). This trade-off — longer lookback gives more stable estimates per rebalance, but eats into the evaluation period you can actually test — is worth understanding, not just accepting.

## Why the comparisons matter again

Same logic as Week 3: the walk-forward strategy is only meaningful relative to baselines. Equal-weighted and S&P 500 returns are computed over the *exact same* out-of-sample dates as the walk-forward strategy (not the full 5 years) — comparing different time windows would make the comparison invalid.

## What to actually expect

Be prepared for the walk-forward Max-Sharpe strategy to *not* clearly beat equal-weighted or the S&P 500. This is a realistic and common outcome, not a sign something's broken — Week 3's walkthrough already flagged that mean-variance optimization is highly sensitive to estimation noise, and walk-forward backtesting is precisely what exposes that sensitivity instead of hiding it. If your optimized weights keep changing dramatically between quarters (check `data/backtest_weight_history.csv`) and performance is mediocre, that's a genuine, interesting, and honest finding for your write-up: naive Markowitz optimization can be unstable in practice, and that instability has a real cost.

## Walking through `backtest_strategy.py`

**`load_data()`** — loads Week 1's prices and returns, separates the benchmark from the tradeable stock universe (same pattern as Week 3).

**`get_rebalance_positions()`** — returns a list of trading-day positions (not dates — simpler to reason about as "every 63 rows," roughly every quarter) at which we'll re-optimize. Starts at `LOOKBACK_DAYS` so the first rebalance always has a full lookback window behind it.

**`run_walk_forward()`** — the heart of the script. For each rebalance position `pos`:
- `lookback_window = stock_prices.iloc[pos - LOOKBACK_DAYS : pos]` — strictly the data *before* `pos`. This single line is what prevents look-ahead bias; if this accidentally included data at or after `pos`, the whole exercise would be invalid.
- `estimate_inputs()` and `optimize_max_sharpe()` are imported directly from `optimize_portfolio.py` — Week 3's exact functions, reused rather than rewritten.
- `holding_period_returns = stock_returns.iloc[pos:segment_end][weights.index]` — the *next* quarter's actual returns, which the optimizer above never saw.
- `portfolio_returns = holding_period_returns @ weights` — for each day in that quarter, multiplies each stock's return by its weight and sums, giving the portfolio's realized daily return.
- All quarters' results get concatenated into one continuous `walk_forward_returns` series, and every quarter's weights get saved into `weight_history` so you can inspect how the allocation drifted over time.

**`summarize()`** — reuses `annualized_return`, `annualized_volatility`, and `max_drawdown` from Week 2's `analyze_risk.py` (same reuse principle as Week 3) to produce one row of metrics per strategy.

**`plot_comparison()`** — plots cumulative return curves for all three strategies over the identical out-of-sample window, so you can see at a glance who actually came out ahead and how bumpy the ride was.

## Output files

`data/backtest_comparison.csv` — total return, annualized return, volatility, Sharpe, and max drawdown for the walk-forward strategy vs. equal-weighted vs. S&P 500, all over the same out-of-sample period.

`data/backtest_weight_history.csv` — one row per rebalance date, one column per stock, showing exactly what weights were chosen each quarter. Worth opening directly — large swings between adjacent rows are a visible signature of estimation noise.

`plots/backtest_comparison.png` — the three cumulative return lines, side by side.

## Next

Week 5 wraps the whole pipeline (Weeks 1–4) into an interactive Streamlit dashboard, and Week 6 is the write-up — where this week's honest, possibly underwhelming result becomes one of the most interesting things to discuss.
