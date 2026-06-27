# Portfolio Optimizer & Strategy Backtester

Week 1 of the project plan (see `../project_plan.md`): a data pipeline that pulls historical prices for a diversified stock universe, cleans them, and computes daily/cumulative returns. Later weeks add risk analytics, Modern Portfolio Theory optimization, backtesting, and a Streamlit dashboard.

## Stock universe

| Ticker | Sector |
|---|---|
| AAPL | Technology |
| MSFT | Technology |
| JNJ | Healthcare |
| JPM | Financials |
| XOM | Energy |
| PG | Consumer Staples |
| AMZN | Consumer Discretionary |
| CAT | Industrials |
| NEE | Utilities |
| DIS | Communication Services |
| ^GSPC | S&P 500 (benchmark) |

Feel free to swap tickers — just keep a mix of sectors so the diversification analysis in Week 2 is meaningful.

## Setup

```bash
# from inside portfolio-optimizer/
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the pipeline

```bash
python fetch_data.py
```

This downloads 5 years of daily prices via `yfinance`, cleans them, and writes three files to `data/`:

- `raw_prices.csv` — adjusted close prices, one column per ticker
- `daily_returns.csv` — daily simple returns
- `cumulative_returns.csv` — cumulative returns from the start of the window

It also prints a quick summary so you can sanity-check the output without opening the CSVs.

## Git setup (if not done already)

```bash
git init
git add .
git commit -m "Week 1: data pipeline"
```

Then create an empty repo on GitHub and push:

```bash
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

## Next step

Week 2: compute annualized return, volatility, Sharpe ratio, max drawdown, and the correlation matrix from `daily_returns.csv` — see the main project plan for details.
