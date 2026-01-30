import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="SME Financial Health AI Platform",
    layout="wide"
)

st.title("📊 SME Financial Health Assessment Platform")

st.markdown("AI-powered financial analysis for SMEs")

# ---------------- LANGUAGE ----------------

language = st.selectbox(
    "🌍 Select Language",
    {
        "English": "en",
        "Hindi": "hi",
        "Tamil": "ta"
    }.keys()
)

lang_code = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta"
}[language]

# ---------------- FILE UPLOAD ----------------

file = st.file_uploader("📁 Upload Financial Excel File", type=["xlsx"])

if file:

    with st.spinner("Analyzing financial data..."):
        response = requests.post(
            API_URL + f"?language={lang_code}",
            files={"file": file}
        )

    if response.status_code != 200:
        st.error("FastAPI backend is not running!")
        st.stop()

    data = response.json()

    # ================= SUMMARY KPIs =================

    s = data["summary"]

    st.subheader("📌 Key Financial Metrics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Revenue", f"₹{s['total_revenue']:,.0f}")
    c2.metric("Total Expenses", f"₹{s['total_expenses']:,.0f}")
    c3.metric("Total Cashflow", f"₹{s['total_cashflow']:,.0f}")
    c4.metric("Profit Margin", f"{s['profit_margin']}%")

    st.divider()

    # ================= BENCHMARK =================

    st.subheader("🏭 Industry Benchmark")

    b = data["benchmark"]

    if "Above" in b["status"]:
        st.success(
            f"Above Industry Average 🚀 "
            f"(Your Margin: {b['your_margin']}% | Industry Avg: {b['industry_avg_margin']}%)"
        )
    else:
        st.warning(
            f"Below Industry Average ⚠️ "
            f"(Your Margin: {b['your_margin']}% | Industry Avg: {b['industry_avg_margin']}%)"
        )

    # ================= MONTHLY TREND =================

    st.subheader("📅 Monthly Financial Trends")

    years = list(data["monthly_by_year"].keys())

    selected_year = st.selectbox("Select Year", years)

    df_month = pd.DataFrame(data["monthly_by_year"][selected_year])

    fig_month = px.line(
        df_month,
        x="Month",
        y=["Revenue", "Expenses", "Cashflow"],
        markers=True,
        title=f"Monthly Performance - {selected_year}"
    )

    st.plotly_chart(fig_month, use_container_width=True)

    # ================= YEARLY TREND =================

    st.subheader("📊 Yearly Financial Summary")

    df_year = pd.DataFrame(data["yearly_summary"])

    fig_year = px.bar(
        df_year,
        x="Year",
        y=["Revenue", "Expenses", "Cashflow"],
        barmode="group",
        title="Yearly Growth Overview"
    )

    st.plotly_chart(fig_year, use_container_width=True)

    # ================= ML FORECAST =================

    st.subheader("🔮 AI Forecast (ML Based)")

    forecast = data["ml_forecast"]

    st.info(
        f"Predicted Revenue for {forecast['next_year']} : "
        f"₹{forecast['predicted_revenue']:,.0f}"
    )

    # ================= GST COMPLIANCE =================

    st.subheader("🧾 GST Compliance Check")

    gst = data["gst_compliance"]

    if gst["status"] == "Compliant":
        st.success(
            f"GST Compliant ✅ (Expected: ₹{gst['expected_gst']:,.0f} | "
            f"Estimated Paid: ₹{gst['estimated_paid']:,.0f})"
        )
    else:
        st.error(
            f"GST Non-Compliant ❌ (Expected: ₹{gst['expected_gst']:,.0f} | "
            f"Estimated Paid: ₹{gst['estimated_paid']:,.0f})"
        )

    # ================= AI INSIGHTS =================

    st.subheader("🧠 AI Insights")

    for i in data["ai_insights"]:
        st.success(i)

    # ================= AI RECOMMENDATIONS =================

    st.subheader("💡 AI Recommendations")

    for r in data["recommendations"]:
        st.write("👉", r)

    # ================= PDF DOWNLOAD =================

    st.subheader("📄 Investor-ready Financial Report")

    if os.path.exists("financial_report.pdf"):
        with open("financial_report.pdf", "rb") as pdf_file:
            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf_file,
                file_name="financial_report.pdf",
                mime="application/pdf"
            )
