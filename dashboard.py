import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="SME Financial Health AI",
    layout="wide"
)

st.markdown("""
<style>
.big-font {font-size:24px;font-weight:bold;}
.card {
    padding:20px;
    border-radius:15px;
    background-color:#0f172a;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 SME Financial Health AI Dashboard")

uploaded_file = st.file_uploader(
    "📁 Upload Financial Excel File",
    type=["xlsx"]
)

if uploaded_file:

    with st.spinner("🔍 AI analyzing your financial data..."):
        response = requests.post(
            API_URL,
            files={"file": uploaded_file}
        )

    if response.status_code != 200:
        st.error("❌ Backend not responding. Start FastAPI first.")
        st.stop()

    data = response.json()

    if "error" in data:
        st.error(data["error"])
        st.stop()

    # ===================== KPIs ======================

    st.subheader("📌 Key Performance Indicators")

    k1,k2,k3,k4 = st.columns(4)

    k1.metric("💰 Revenue", f"₹ {data['totals']['revenue']:,.0f}")
    k2.metric("💸 Expenses", f"₹ {data['totals']['expenses']:,.0f}")
    k3.metric("📈 Cashflow", f"₹ {data['totals']['cashflow']:,.0f}")
    k4.metric("🏦 Credit Score", data["kpis"]["credit_score"])

    # ===================== MONTHLY GRAPH ======================

    st.subheader("📅 Monthly Financial Trend")

    monthly_df = pd.DataFrame(data["monthly"])

    monthly_df["Month"] = pd.Categorical(
        monthly_df["Month"],
        categories=["Jan","Feb","Mar","Apr","May","Jun",
                    "Jul","Aug","Sep","Oct","Nov","Dec"],
        ordered=True
    )

    monthly_df = monthly_df.sort_values(["Year","Month"])

    selected_year = st.selectbox(
        "Select Year",
        sorted(monthly_df["Year"].unique())
    )

    year_data = monthly_df[monthly_df["Year"] == selected_year]

    fig_month = px.line(
        year_data,
        x="Month",
        y=["Revenue","Expenses","Cashflow"],
        markers=True,
        title=f"Monthly Performance - {selected_year}"
    )

    st.plotly_chart(fig_month, use_container_width=True)

    # ===================== YEARLY GRAPH ======================

    st.subheader("📊 Yearly Overview")

    yearly_df = pd.DataFrame(data["yearly"])

    fig_year = px.bar(
        yearly_df,
        x="Year",
        y=["Revenue","Expenses","Cashflow"],
        barmode="group",
        title="Yearly Financial Comparison"
    )

    st.plotly_chart(fig_year, use_container_width=True)

    # ===================== AI INSIGHTS ======================

    st.subheader("🤖 AI Financial Insights")

    profit_margin = data["kpis"]["profit_margin"]
    growth = data["kpis"]["growth_percent"]
    risk = data["kpis"]["risk_level"]

    if profit_margin > 20:
        st.success("✔ Strong profitability. Business operations are healthy.")
    elif profit_margin > 10:
        st.warning("⚠ Moderate profit margin. Cost optimization can improve returns.")
    else:
        st.error("❗ Low profit margin detected. Immediate financial review needed.")

    if growth > 0:
        st.success(f"📈 Revenue is growing by {growth:.2f}% annually.")
    else:
        st.warning("📉 Revenue growth is weak or negative.")

    st.info(f"⚖ Risk Level: {risk}")

    # ===================== AI RECOMMENDATIONS ======================

    st.subheader("💡 AI Recommendations")

    recommendations = []

    if profit_margin < 15:
        recommendations.append("Reduce operational costs and negotiate supplier contracts.")

    if growth < 5:
        recommendations.append("Invest in marketing and customer acquisition.")

    if data["totals"]["expenses"] > data["totals"]["revenue"] * 0.75:
        recommendations.append("High expense ratio detected. Review overhead spending.")

    if risk != "Low Risk":
        recommendations.append("Build cash reserves to improve financial stability.")

    if not recommendations:
        recommendations.append("Financial performance is excellent. Continue current strategy.")

    for rec in recommendations:
        st.write("👉", rec)

    # ===================== SUMMARY ======================

    st.subheader("📄 AI Summary")

    st.markdown(f"""
    - Total Revenue: ₹ {data['totals']['revenue']:,.0f}  
    - Total Expenses: ₹ {data['totals']['expenses']:,.0f}  
    - Cashflow: ₹ {data['totals']['cashflow']:,.0f}  
    - Profit Margin: {profit_margin:.2f}%  
    - Credit Score: {data['kpis']['credit_score']}  
    - Risk Level: {risk}
    """)

    st.success("✅ AI analysis completed successfully!")
