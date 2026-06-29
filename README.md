# Portfolio Optimizer & Strategy Backtester

A quantitative finance project built in Python that fetches real stock data, constructs an optimized portfolio using Modern Portfolio Theory, validates it with a walk-forward backtest, and presents all results in an interactive Streamlit dashboard.

---

## Project Overview

This project answers a core question in investing: **can a mathematically optimized portfolio consistently beat a simple equal-weight strategy in real-world conditions?**

The answer — and the reasoning behind it — is the central finding of this project.

### What It Does

| Week | Module | Description |
|------|--------|-------------|
| 1 | `fetch_data.py` | Pulls 3 years of daily price data for 10 stocks via yfinance, computes daily and cumulative returns |
| 2 | `analyze_risk.py` | Calculates annualized return, volatility, Sharpe Ratio, max drawdown, and correlation matrix |
| 3 | `optimize_portfolio.py` | Applies Mean-Variance Optimization to construct the efficient frontier and find the Maximum Sharpe Ratio portfolio |
| 4 | `backtest_strategy.py` | Runs a walk-forward backtest — reoptimizing every 3 months on a rolling window — to evaluate out-of-sample performance |
| 5 | `dashboard.py` | Interactive Streamlit dashboard with 4 tabs covering all results |

---

## Key Finding

The walk-forward backtest compared three strategies over the out-of-sample period:

| Strategy | Total Return | Sharpe Ratio | Volatility |
|----------|-------------|--------------|------------|
| Equal Weighted | 74.4% | 1.27 | 13.0% |
| S&P 500 | 67.3% | 0.99 | 15.0% |
| Walk-Forward Optimizer | 53.9% | 0.61 | 19.0% |

**The optimized portfolio underperformed both benchmarks.** The optimizer consistently produced concentrated portfolios — allocating 100% to just 1-2 stocks — leading to high volatility and poor compounding. This is consistent with academic literature on the *1/N puzzle*, which documents that equal weighting frequently outperforms complex optimization due to overfitting.

---

## Stock Universe

| Ticker | Company | Sector |
|--------|---------|--------|
| AAPL | Apple | Technology |
| MSFT | Microsoft | Technology |
| JNJ | Johnson & Johnson | Healthcare |
| JPM | JPMorgan Chase | Financials |
| XOM | ExxonMobil | Energy |
| PG | Procter & Gamble | Consumer Staples |
| AMZN | Amazon | Consumer Discretionary |
| CAT | Caterpillar | Industrials |
| NEE | NextEra Energy | Utilities |
| DIS | Disney | Communication Services |
| ^GSPC | S&P 500 | Benchmark |

---

## Setup & Usage

```bash
# Clone the repo
git clone https://github.com/jwhitek02/portfolio-optimizer.git
cd portfolio-optimizer

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Run Each Module

```bash
# Week 1 — fetch data
python fetch_data.py

# Week 2 — risk analysis
python analyze_risk.py

# Week 3 — portfolio optimization
python optimize_portfolio.py

# Week 4 — walk-forward backtest
python backtest_strategy.py

# Week 5 — launch dashboard
streamlit run dashboard.py
```

---

## Dashboard

The Streamlit dashboard has four interactive tabs:

- **Stock Prices** — cumulative return chart with stock selector
- **Risk Analysis** — risk metrics table and correlation heatmap
- **Optimization** — efficient frontier, portfolio weights, and performance comparison
- **Backtest** — strategy comparison table and weight history

---

## Tech Stack

- **Python** — pandas, NumPy
- **Data** — yfinance
- **Optimization** — PyPortfolioOpt
- **Visualization** — Plotly, Streamlit
- **Version Control** — Git / GitHub
