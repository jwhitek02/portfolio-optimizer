# Week 2 Walkthrough: Risk & Return Analytics

Week 1 turned prices into returns. Week 2 asks the next question: *is a high return actually good, or did it come with risk that makes it a bad deal?* This is the core idea behind everything in `analyze_risk.py`.

## Why return alone is misleading

Imagine two stocks both returned 20% this year. Stock A moved up steadily. Stock B crashed 40% in March, then rocketed back. Same return, very different experience — and very different odds of you panic-selling at the bottom. Finance has standard ways to quantify that difference. That's what this week's four metrics do.

## The four metrics, conceptually

**Annualized return** — your average yearly growth rate, accounting for compounding. We don't just average the daily returns and multiply by 252, because gains compound (a +5% day and a -5% day don't cancel out — you end up slightly down). Instead we compute the *total* growth over the whole window, then ask "what constant yearly rate would produce that same total growth?" That's the geometric mean, also called CAGR (compound annual growth rate).

**Annualized volatility** — how much returns bounce around their average, scaled to a yearly figure. This is the standard statistical measure of risk: standard deviation. We annualize daily volatility by multiplying by √252 (not 252) because variance — not volatility itself — scales linearly with time, and volatility is the square root of variance. This square-root scaling shows up everywhere in quantitative finance, so it's worth remembering.

**Sharpe ratio** — return per unit of risk: `(annualized return − risk-free rate) / annualized volatility`. The risk-free rate represents what you could earn doing nothing risky (parking money in T-bills), so the numerator is your *excess* return for taking on risk at all. Dividing by volatility answers "was the extra return worth the bumpiness?" A higher Sharpe ratio means more return for the risk taken — it's the standard way investors compare two assets that have different return levels. Note `RISK_FREE_RATE` in the script is a placeholder assumption (0.04), not a live number — a real version would pull the current T-bill yield, which is a reasonable upgrade to mention if asked about limitations.

**Max drawdown** — the worst peak-to-trough loss you'd have experienced if you'd bought at the worst possible time and held through the worst possible point. Two assets can have identical volatility but very different max drawdowns, and drawdown is often what actually drives investor behavior (it's the number that makes people sell at the bottom). We compute it by tracking a running "wealth index" (what $1 invested on day one would be worth each day), comparing it to its running peak, and finding the largest percentage gap between the two.

## Why the correlation matrix matters

This sets up Week 3. Modern Portfolio Theory's central insight is that combining assets that *don't* move together reduces a portfolio's overall risk, even if you don't touch the expected return. Two stocks with 0.9 correlation move almost in lockstep — holding both barely diversifies anything. Two stocks with 0.1 or negative correlation smooth each other out. The heatmap makes it visual: dark/extreme colors are pairs that move together, lighter or opposite-colored cells are pairs that don't. When we build the optimizer next week, this correlation structure (technically the covariance matrix) is one of its two key inputs.

## Walking through `analyze_risk.py`

**`annualized_return(daily_returns)`** — `(1 + daily_returns).prod()` multiplies `(1 + r)` across every day to get total growth (e.g., 1.35 means +35% total). `** (1 / n_years) - 1` converts that total growth into an equivalent constant yearly rate.

**`annualized_volatility(daily_returns)`** — `.std()` gives the daily standard deviation per column; `* np.sqrt(252)` annualizes it.

**`sharpe_ratio(...)`** — directly implements the formula above. Takes the already-computed annualized return and volatility rather than recomputing from scratch.

**`max_drawdown(daily_returns)`** — `(1 + daily_returns).cumprod()` builds the wealth index; `.cummax()` tracks the running peak at every point in time; dividing the wealth index by its running peak and subtracting 1 gives the drawdown at every point; `.min()` picks out the worst one.

**`build_metrics_table(...)`** — calls all four functions and assembles them into one DataFrame, one row per ticker, sorted by Sharpe ratio so the best risk-adjusted performers show up first.

**`plot_cumulative_returns(...)`** — loops over every ticker and plots its cumulative return line on the same chart, so you can visually compare growth trajectories (including the S&P 500 benchmark) at a glance.

**`plot_correlation_heatmap(...)`** — `imshow` renders the correlation matrix as a grid of colors; the nested loop adds the numeric value as text inside each cell so it's readable, not just colored.

**`main()`** — checks that `data/daily_returns.csv` exists first (a friendly error if you skipped Week 1), loads both CSVs, runs all the calculations, saves two new CSVs (`risk_metrics.csv`, `correlation_matrix.csv`) and two PNG charts into a new `plots/` folder, then prints the metrics table so you get instant feedback in the terminal.

## What "good" output looks like

A real run won't match any specific numbers, but you should see: a metrics table with one row per ticker plus `^GSPC`, volatilities roughly in the 15–35% range for individual stocks (lower for the index), Sharpe ratios mostly between -1 and 2, and max drawdowns as negative percentages (more negative = worse). The correlation heatmap should show most tickers positively correlated with each other and with `^GSPC` (stocks broadly move with the market), with some pairs more correlated than others depending on sector.

## Next

Week 3 takes the return and covariance structure from this week and feeds it into an optimizer to build an actual portfolio — the first point where "data science" and "this is genuinely a finance technique" fully merge.
