import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="SME Financial Health Platform", layout="wide")

st.title("📊 SME Financial Health Assessment Platform")

uploaded_file = st.file_uploader("Upload Financial Excel File", type=["xlsx"])

if uploaded_file:

    files = {"file": uploaded_file.getvalue()}
    
    response = requests.post(API_URL, files={"file": uploaded_file})

    if response.status_code == 200:
        data = response.json()["results"]

        totals = data["totals"]
        averages = data["average"]
        forecast = data["forecast"]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Revenue", f"₹{totals['revenue']:,}")
        col2.metric("Total Expenses", f"₹{totals['expenses']:,}")
        col3.metric("Total Cashflow", f"₹{totals['cashflow']:,}")
        col4.metric("Credit Score", data["credit_score"])

        chart_df = pd.DataFrame({
            "Metric": ["Revenue", "Expenses", "Cashflow"],
            "Amount": [
                totals["revenue"],
                totals["expenses"],
                totals["cashflow"]
            ]
        })

        fig = px.bar(chart_df, x="Metric", y="Amount", title="Financial Overview")
        st.plotly_chart(fig, use_container_width=True)

        forecast_df = pd.DataFrame({
            "Type": ["Revenue", "Expenses", "Cashflow"],
            "Next Period": [
                forecast["next_revenue"],
                forecast["next_expenses"],
                forecast["next_cashflow"]
            ]
        })

        fig2 = px.line(forecast_df, x="Type", y="Next Period", title="Forecast Trend", markers=True)
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📌 Risk & Insights")
        st.write("Risk Level:", data["risks"][0])
        st.write("Industry Benchmark:", data["industry_benchmark"])
        st.write("GST Compliance:", data["gst_compliance"])
        st.write("Financial Health:", data["financial_health"])

        st.subheader("💡 Cost Optimization Suggestions")
        for tip in data["cost_optimization"]:
            st.write("•", tip)

    else:
        st.error("API Error")
