import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Portfolio Optimizer", layout="wide")
st.title("Portfolio Optimizer Dashboard")
st.caption("A walk-forward backtested portfolio optimization across 10 stocks (2021–2024)")

tab1, tab2, tab3, tab4 = st.tabs(["Stock Prices", "Risk Analysis", "Optimization", "Backtest"])

# --- Tab 1: Stock Prices ---
with tab1:
    st.header("Stock Prices & Cumulative Returns")
    st.write("This tab shows how each stock performed over the full period — both raw daily returns and how $1 invested would have grown.")

    cumulative = pd.read_csv("data/cumulative_returns.csv", index_col="Date", parse_dates=True)

    stocks = [c for c in cumulative.columns if c != "^GSPC"]
    selected = st.multiselect("Select stocks to display", stocks, default=stocks)

    if selected:
        fig = px.line(
            cumulative[selected],
            labels={"value": "Cumulative Return (starting at 1.0)", "Date": "Date", "variable": "Stock"},
            title="Cumulative Returns Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.write("**How to read this:** A value of 1.5 means a 50% return since the start. The higher the line ends, the better that stock performed.")

# --- Tab 2: Risk Analysis ---
with tab2:
    st.header("Risk Metrics & Correlations")
    st.write("This tab shows how risky each stock is individually, and how they move relative to each other.")

    risk = pd.read_csv("data/risk_metrics.csv", index_col=0)
    risk.columns = ["Annualized Return", "Annualized Volatility", "Sharpe Ratio", "Max Drawdown"]
    risk = risk.round(3)

    st.subheader("Risk Metrics by Stock")
    st.dataframe(risk, use_container_width=True)
    st.write("""
    - **Annualized Return** — average yearly gain
    - **Annualized Volatility** — how much the price swings (higher = riskier)
    - **Sharpe Ratio** — return per unit of risk (higher = better)
    - **Max Drawdown** — worst peak-to-trough loss during the period
    """)

    st.subheader("Correlation Matrix")
    corr = pd.read_csv("data/correlation_matrix.csv", index_col=0)
    fig2 = px.imshow(
        corr,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        title="Stock Return Correlations",
        text_auto=".2f"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.write("**How to read this:** Values close to 1 (dark red) mean two stocks move together. Values close to -1 (dark blue) mean they move oppositely. Stocks that move independently of each other are valuable for diversification.")

# --- Tab 3: Portfolio Optimization ---
with tab3:
    st.header("Portfolio Optimization Results")
    st.write("This tab shows the output of Week 3's Mean-Variance Optimization — the mathematically ideal way to split money across stocks.")

    weights = pd.read_csv("data/portfolio_weights.csv", index_col=0)
    weights.columns = ["Max Sharpe", "Min Volatility", "Equal Weighted"]
    weights = (weights * 100).round(1)

    comparison = pd.read_csv("data/portfolio_comparison.csv", index_col=0)
    comparison.columns = ["Expected Return", "Volatility", "Sharpe Ratio"]
    comparison = comparison.round(3)

    st.subheader("Portfolio Performance Comparison")
    st.dataframe(comparison, use_container_width=True)

    st.subheader("Portfolio Weights (%)")
    fig3 = px.bar(
        weights,
        barmode="group",
        labels={"value": "Weight (%)", "index": "Stock", "variable": "Strategy"},
        title="How Each Strategy Allocates Money Across Stocks"
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.write("**How to read this:** Each bar shows what percentage of your money goes into that stock. Notice how Max Sharpe puts 0% in many stocks — that's the concentration problem we discovered in Week 4.")

# --- Tab 4: Backtest ---
with tab4:
    st.header("Walk-Forward Backtest Results")
    st.write("This tab shows how each strategy would have actually performed if used in real time, only using data available at each point — no peeking into the future.")

    backtest = pd.read_csv("data/backtest_comparison.csv", index_col=0)
    backtest.columns = ["Total Return", "Annualized Return", "Annualized Volatility", "Sharpe Ratio", "Max Drawdown"]
    backtest = backtest.round(3)

    st.subheader("Strategy Comparison")
    st.dataframe(backtest, use_container_width=True)

    weight_history = pd.read_csv("data/backtest_weight_history.csv", index_col=0)
    stock_cols = [c for c in weight_history.columns if c not in ["rebalance_date", "period_start", "period_end"]]

    st.subheader("Cumulative Returns by Strategy")
    cumulative = pd.read_csv("data/cumulative_returns.csv", index_col="Date", parse_dates=True)
    if "^GSPC" in cumulative.columns:
        sp500 = cumulative[["^GSPC"]].rename(columns={"^GSPC": "S&P 500"})
        fig4 = px.line(sp500, labels={"value": "Cumulative Return", "Date": "Date", "variable": "Strategy"}, title="S&P 500 Cumulative Return (Backtest Period Reference)")
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Optimizer Weight History")
    fig5 = px.bar(
        weight_history[stock_cols],
        labels={"value": "Weight", "index": "Rebalance Period", "variable": "Stock"},
        title="How the Optimizer Allocated Weights at Each Rebalance"
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.write("**How to read this:** Each bar group is one rebalance period. Notice how the optimizer concentrates everything into just 1–2 stocks each time, and picks completely different stocks each period — this instability is why it underperformed.")

    st.subheader("Key Takeaway")
    st.info("The equal-weight strategy outperformed the optimizer on both total return and risk-adjusted return (Sharpe Ratio). This is a well-documented result in finance — simple diversification often beats complex optimization because the optimizer overfits to historical patterns that don't repeat.")
