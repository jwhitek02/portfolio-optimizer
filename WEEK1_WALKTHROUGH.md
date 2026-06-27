# Week 1 Walkthrough: What We Built and Why

This explains every file in `portfolio-optimizer/` so far, and walks through `fetch_data.py` piece by piece. No prior coding background assumed.

## The big picture

A "data pipeline" just means: get raw data in → clean it up → transform it into the shape you actually need. Week 1's pipeline does exactly three things, in order:

1. Download raw stock prices
2. Clean them (real data always has gaps/errors)
3. Convert prices into *returns* (the thing we actually analyze)

Everything below supports that.

## Mini glossary

A few words that will come up constantly:

- **Library/package** — pre-written code someone else published so you don't have to write it yourself. `pandas` is a library for working with tabular data; `yfinance` is a library for pulling stock data from Yahoo Finance.
- **pip** — the tool that downloads and installs libraries. `pip install pandas` fetches the `pandas` library onto your machine.
- **Virtual environment (venv)** — an isolated folder of installed libraries just for this project, so installing things here doesn't affect other Python projects on your computer. Creating one (`python3 -m venv .venv`) is like giving this project its own private toolbox.
- **DataFrame** — pandas' main data structure: think of it as a spreadsheet inside Python (rows, columns, labels).
- **Function** — a named, reusable block of code. You give it inputs, it gives you back an output, and you don't need to know its internals to use it.
- **CSV** — a plain-text spreadsheet format (comma-separated values). Easy to open in Excel or load back into pandas.

## File by file

### `requirements.txt`

A plain list of every library the project needs. Anyone (including future-you) can run `pip install -r requirements.txt` and get the exact same setup in one command, instead of guessing what to install.

What each line is for:

- `pandas`, `numpy` — data wrangling and math (used every week)
- `yfinance` — pulls historical stock prices (Week 1)
- `PyPortfolioOpt` — does the Modern Portfolio Theory math (Week 3)
- `matplotlib`, `plotly` — charts (Weeks 2–4)
- `streamlit` — the dashboard (Week 5)

You're installing everything now so you don't have to stop and install mid-project later.

### `.gitignore`

Git (the version control tool) tracks every file in a folder by default. `.gitignore` tells it which files to *ignore* — things that are either machine-specific (`.venv/`, `__pycache__/`) or regeneratable (`data/*.csv`, since `fetch_data.py` recreates them on demand). Keeping generated data out of the repo is standard practice: it keeps the repo small and proves the pipeline works for anyone who clones it, rather than relying on a stale CSV someone uploaded once.

### `README.md`

The front page of the repo. When a recruiter or interviewer opens your GitHub project, this is what they see first — so it explains what the project is, how to set it up, and how to run it, without them needing to ask you.

### `fetch_data.py` — the main script

This is the actual pipeline. Here's what happens, top to bottom.

**1. The docstring at the top**

```python
"""
Week 1: data pipeline.
...
"""
```

A triple-quoted string at the top of a file is a *docstring* — a comment that explains what the file does. It's not executed; it's documentation for humans.

**2. Imports**

```python
import os
import pandas as pd
import yfinance as yf
```

This loads the libraries we need. `os` is built into Python (for things like creating folders); `pandas` and `yfinance` are the libraries from `requirements.txt`. The `as pd` / `as yf` part just gives them short nicknames so we don't have to type `pandas.` every time.

**3. The config section**

```python
TICKERS = {...}
BENCHMARK = "^GSPC"
PERIOD = "5y"
INTERVAL = "1d"
DATA_DIR = "data"
```

These are constants — values that control the script's behavior, all grouped at the top instead of buried inside the logic. The reason: if you want to change the stock list, the time window, or the output folder later, you edit one line near the top instead of hunting through the whole file. This is a habit worth keeping in every script you write.

**4. `fetch_prices()` — get the raw data**

```python
def fetch_prices(tickers, benchmark, period=PERIOD, interval=INTERVAL):
    all_tickers = list(tickers) + [benchmark]
    raw = yf.download(all_tickers, period=period, interval=interval, auto_adjust=True, progress=False)
    ...
    prices = raw["Close"]
    return prices
```

`yf.download(...)` is one function call that hits Yahoo Finance's servers and hands back years of daily prices for every ticker you list. A few details worth understanding:

- `auto_adjust=True` adjusts historical prices for stock splits and dividends. Without this, a 2-for-1 stock split would look like the price crashed 50% overnight, which would wreck any return calculation. This is a real gotcha in finance data — always check whether a data source is adjusting for splits/dividends.
- When you ask for *multiple* tickers at once, yfinance hands back a table with two levels of columns (price type, then ticker) instead of one. The code pulls out just the `"Close"` level since that's all we need.

**5. `clean_prices()` — handle messy real-world data**

```python
def clean_prices(prices):
    min_obs = int(len(prices) * 0.9)
    prices = prices.dropna(axis=1, thresh=min_obs)
    prices = prices.ffill().dropna()
    return prices
```

Real market data is never perfectly clean — a company might have IPO'd partway through your date range, or a data feed might be missing a day. This function handles that in two steps:

- `dropna(axis=1, thresh=min_obs)`: if a ticker is missing more than 10% of its expected history, drop that whole column. A stock with huge gaps would distort everything downstream, so it's safer to exclude it than guess.
- `ffill()` ("forward fill"): for small, occasional gaps, carry the last known price forward (if Tuesday's price is missing, assume it equaled Monday's). Then `dropna()` removes any row that's still incomplete after that — typically just the first few rows where forward-fill has nothing to fill from yet.

**6. `compute_returns()` — the actual point of Week 1**

```python
def compute_returns(prices):
    daily_returns = prices.pct_change().dropna()
    cumulative_returns = (1 + daily_returns).cumprod() - 1
    return daily_returns, cumulative_returns
```

This is the most important conceptual step. We don't analyze raw prices directly, because prices aren't comparable across stocks — a $500 stock moving $5 is a 1% move, while a $50 stock moving $5 is a 10% move. *Returns* (percent changes) put every stock on the same scale, which is what makes comparison, diversification analysis, and optimization (later weeks) meaningful at all.

- `pct_change()` computes `(today's price − yesterday's price) / yesterday's price` for every day, automatically.
- Cumulative return answers "if I'd invested on day 1, what's my total return by today?" You can't just add daily returns together because gains compound — a +10% day followed by a −10% day doesn't get you back to even. `(1 + daily_returns).cumprod() - 1` correctly compounds each day's return on top of the last.

**7. `main()` — runs the steps in order**

```python
def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    prices = fetch_prices(TICKERS, BENCHMARK)
    prices = clean_prices(prices)
    daily_returns, cumulative_returns = compute_returns(prices)
    prices.to_csv(...)
    daily_returns.to_csv(...)
    cumulative_returns.to_csv(...)
    print(...)
```

This is the pipeline made literal: each function's output becomes the next function's input. `main()` just calls them in sequence and saves the results to CSV files so later scripts (Week 2 onward) can load them without re-downloading from Yahoo every time. The `print` at the end is a sanity check — a quick way to eyeball that the numbers look reasonable before moving on.

**8. The bottom two lines**

```python
if __name__ == "__main__":
    main()
```

This is a standard Python idiom that means "only run `main()` if this file was executed directly (`python fetch_data.py`), not if it was imported by another script." It lets you reuse these functions in Week 2+ scripts without accidentally re-running the whole download every time you import something.

## What actually happens when you type `python fetch_data.py`

1. Python reads the file top to bottom, defining the functions (nothing runs yet).
2. It hits the `if __name__ == "__main__":` line at the bottom and calls `main()`.
3. `main()` creates the `data/` folder if it doesn't exist.
4. It calls `fetch_prices()`, which reaches out to Yahoo Finance over the internet and downloads ~5 years of daily prices for 11 tickers.
5. It calls `clean_prices()` on that raw data to handle gaps.
6. It calls `compute_returns()` to turn prices into daily and cumulative returns.
7. It writes three CSVs to `data/`.
8. It prints a one-line summary plus a ranked list of cumulative returns, so you immediately see something like "AAPL is up 80% over this window" without opening a file.

## Why git/GitHub matter here

Git tracks every change you make to the code over time (so you can undo mistakes and see history). GitHub hosts that history online. For a resume project, the GitHub link *is* the proof of work — it's what a recruiter or interviewer actually clicks on. Committing regularly (e.g., once per week of this project) also creates a visible timeline of progress, which is its own small signal of consistency.

## Where this goes next

Week 2 loads `data/daily_returns.csv` and computes risk metrics (volatility, Sharpe ratio, max drawdown) and the correlation matrix — see `../project_plan.md`. Ask for the same kind of walkthrough when we get there, or anytime something in the code doesn't make sense.
