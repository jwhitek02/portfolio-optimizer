# Week 3 Walkthrough: Portfolio Optimization (Modern Portfolio Theory)

Weeks 1–2 gave you returns, volatility, and correlations for individual stocks. Week 3 is where it becomes a *portfolio* project: instead of judging stocks one at a time, we decide how much of each to hold so the combination is as good as possible.

## The core idea: diversification is a free lunch (sort of)

If you mix stocks that don't move in lockstep (low correlation — Week 2's heatmap), the portfolio's ups and downs partially cancel out, so the combined volatility can be *lower* than the average of the individual stocks' volatilities, without giving up much expected return. Harry Markowitz formalized this in 1952 (Modern Portfolio Theory, MPT) and won a Nobel Prize for it. The math answers one question: given a set of assets, their expected returns, and how they move together, what mix of weights gives the best possible return for each level of risk?

## Two inputs, two outputs

**Inputs:** for each asset, an expected return (`mu`, estimated from historical average return — `expected_returns.mean_historical_return`), and the covariance matrix (`cov`, basically Week 2's correlations, but scaled by each asset's volatility — `risk_models.sample_cov`). Covariance captures both "how risky is each asset" and "how do pairs move together" in one matrix.

**Output:** the *efficient frontier* — the curve of portfolios that have the best possible return for every level of risk. Any portfolio below this curve is wasteful (you could get more return for the same risk); nothing exists above it given these inputs. Two points on this curve get special attention:

- **Max Sharpe portfolio** — the single best risk-adjusted point on the frontier (highest return per unit of risk). This is usually what people mean by "the optimal portfolio."
- **Min Volatility portfolio** — the single least-risky point on the frontier, regardless of return. For someone who cares about minimizing pain more than maximizing growth.

## Why we also compute an equal-weighted portfolio and the S&P 500

Optimization is only impressive if it beats doing nothing clever. The equal-weighted portfolio (just split money evenly across all 10 stocks) is the standard naive baseline in this literature — research has shown it's a surprisingly tough benchmark to beat in practice, largely because optimizers can overfit to noisy historical estimates. Including the S&P 500 grounds everything in "could I have just bought an index fund instead." Reporting all four side by side is what makes this a credible analysis instead of a one-sided demo — and if your optimized portfolio doesn't clearly beat equal-weighted here, that's a legitimate and interesting finding to discuss, not a bug to hide.

## Walking through `optimize_portfolio.py`

**`load_prices()`** — reads Week 1's `raw_prices.csv`, splits it into the stocks we'd actually optimize over and the S&P 500 (kept separate since it's a comparison point, not something the optimizer is allowed to choose).

**`estimate_inputs()`** — produces `mu` (expected return per stock) and `cov` (the covariance matrix) — literally the two ingredients MPT needs. Everything else in the script is built on these two objects.

**`optimize_max_sharpe()` / `optimize_min_volatility()`** — each creates an `EfficientFrontier` object (from `PyPortfolioOpt`) and calls one of its built-in solvers. `clean_weights()` rounds tiny weights down to zero so the result is readable instead of "0.7% in eleven different stocks." `portfolio_performance()` reports back the resulting expected return, volatility, and Sharpe ratio for that specific weight combination.

**`equal_weighted_performance()`** — there's no library call for "just split evenly," so this computes it directly: portfolio return is the weighted average of individual expected returns (`weights @ mu`); portfolio variance uses the standard formula `wᵀ Σ w` (weights times covariance matrix times weights) — this is the formula that captures *why* diversification works mathematically, since cross-terms between correlated assets either amplify or dampen the total depending on their correlation sign.

**`benchmark_performance()`** — reuses `annualized_return()` and `annualized_volatility()` from Week 2's `analyze_risk.py` rather than rewriting them. This is a small but deliberate software-engineering choice: one source of truth for "what does annualized return mean in this project," reused everywhere it's needed.

**`plot_frontier()`** — `PyPortfolioOpt`'s `plotting.plot_efficient_frontier()` sweeps across a range of target returns, solving the optimization at each one, and traces the resulting curve. `show_assets=True` adds a dot for each individual stock's own risk/return, so you can see how much better the frontier is than holding any single stock alone. The star markers added afterward show exactly where the Max Sharpe, Min Volatility, and Equal Weighted portfolios sit relative to that curve.

**`main()`** — runs everything, saves `portfolio_weights.csv` (the actual allocations — e.g., "21% CAT, 13% JNJ...") and `portfolio_comparison.csv` (the four-way performance comparison), and prints both to the terminal.

## Reading your results

A few things to look for once you run this on your real data:

The Max Sharpe portfolio will likely concentrate heavily into just a handful of your 10 stocks (often 3–6 with meaningful weight, the rest near zero). That's expected — the optimizer is greedily exploiting whatever return/correlation pattern existed in *this specific* historical window, which is also this method's biggest weakness (see below).

Check where each star sits on the frontier chart relative to the S&P 500 dot. If your Max Sharpe star is up and to the left of the S&P 500 (more return, less risk), that's the headline result of this week's analysis.

## The honest limitation (important for your write-up)

This optimizer is fitting to *past* returns and assuming the future will look statistically similar — it won't. Expected returns estimated from 5 years of historical data are notoriously noisy, and Markowitz optimization is known to amplify that noise into extreme, concentrated weights (this is a well-documented critique of "naive" MPT, not a flaw in your implementation). This is exactly why the equal-weighted comparison matters, and why a real-world version would use more robust return/covariance estimates or constrain position sizes. Mentioning this limitation explicitly in your final report is a sign of rigor, not a weakness to hide.

## Next

Week 4 takes one of these ideas — most simply, periodically rebalancing to the Max Sharpe weights, or a separate technical rule like a moving-average crossover — and backtests it as a strategy over time, rather than treating the optimized weights as a single static snapshot.
