# Portfolio Optimizer & Strategy Backtester



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

.
