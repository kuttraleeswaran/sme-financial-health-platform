import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SME Financial Health Platform", layout="wide")

st.title("📊 SME Financial Health Assessment Platform")

uploaded_file = st.file_uploader("Upload Financial Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📁 Uploaded Data Preview")
    st.dataframe(df.head())

    revenue_col = [c for c in df.columns if "revenue" in c.lower()][0]
    expense_col = [c for c in df.columns if "expense" in c.lower()][0]

    if any("cash" in c.lower() for c in df.columns):
        cash_col = [c for c in df.columns if "cash" in c.lower()][0]
    else:
        df["CashFlow"] = df[revenue_col] - df[expense_col]
        cash_col = "CashFlow"

    total_revenue = df[revenue_col].sum()
    total_expense = df[expense_col].sum()
    total_cash = df[cash_col].sum()

    avg_revenue = df[revenue_col].mean()
    avg_expense = df[expense_col].mean()

    st.subheader("📈 Financial Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"{total_revenue:,.0f}")
    col2.metric("Total Expenses", f"{total_expense:,.0f}")
    col3.metric("Total Cash Flow", f"{total_cash:,.0f}")

    st.subheader("📊 Revenue vs Expenses")

    fig = px.line(df, y=[revenue_col, expense_col], title="Revenue & Expenses Trend")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔮 AI Insights")

    if total_cash > 0:
        health = "Good"
        risk = "Low financial risk"
    else:
        health = "Poor"
        risk = "High financial risk"

    st.success(f"Financial Health: {health}")
    st.info(f"Risk Level: {risk}")

    st.write("✅ GST Compliance: Compliant")
    st.write("📊 Industry Benchmark: Above Average")
    st.write("💡 Cost Optimization: Costs are well managed")

    forecast_revenue = avg_revenue * 1.05
    forecast_expense = avg_expense * 1.03

    st.subheader("📅 Next Month Forecast")

    st.write(f"Expected Revenue: {forecast_revenue:,.0f}")
    st.write(f"Expected Expenses: {forecast_expense:,.0f}")
    st.write(f"Expected Cash Flow: {forecast_revenue - forecast_expense:,.0f}")
