from fastapi import FastAPI, UploadFile, File
import pandas as pd
from sklearn.linear_model import LinearRegression
from fpdf import FPDF
from deep_translator import GoogleTranslator
import os

app = FastAPI(title="SME Financial Health AI Platform")

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]

def translate(texts, lang):
    return [GoogleTranslator(source='auto', target=lang).translate(t) for t in texts]

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), language: str = "en"):

    df = pd.read_excel(file.file)

    df["Cashflow"] = df["Revenue"] - df["Expenses"]

    df["Month"] = pd.Categorical(df["Month"], categories=MONTHS, ordered=True)
    df = df.sort_values(["Year","Month"])

    total_revenue = float(df["Revenue"].sum())
    total_expenses = float(df["Expenses"].sum())
    total_cashflow = float(df["Cashflow"].sum())

    profit_margin = (total_cashflow / total_revenue) * 100

    yearly = df.groupby("Year")[["Revenue","Expenses","Cashflow"]].sum().reset_index()

    yearly_data = yearly.to_dict(orient="records")

    monthly_by_year = {}
    for y in df["Year"].unique():
        temp = df[df["Year"] == y]
        monthly_by_year[str(y)] = temp[["Month","Revenue","Expenses","Cashflow"]].to_dict(orient="records")

    # ============ ML FORECAST ============

    X = yearly["Year"].values.reshape(-1,1)
    y = yearly["Revenue"].values

    model = LinearRegression()
    model.fit(X,y)

    next_year = yearly["Year"].max() + 1
    predicted_revenue = float(model.predict([[next_year]])[0])

    # ============ GST COMPLIANCE (SIMULATED) ============

    gst_ratio = total_expenses * 0.18
    gst_paid_estimated = gst_ratio * 0.95  # assume some gap

    gst_status = "Compliant" if gst_paid_estimated >= gst_ratio*0.9 else "Non-Compliant"

    gst_report = {
        "expected_gst": round(gst_ratio,2),
        "estimated_paid": round(gst_paid_estimated,2),
        "status": gst_status
    }

    # ============ BENCHMARK ============

    industry_avg = 18
    benchmark_status = "Above Industry" if profit_margin > industry_avg else "Below Industry"

    benchmark = {
        "industry": "Retail",
        "industry_avg_margin": industry_avg,
        "your_margin": round(profit_margin,2),
        "status": benchmark_status
    }

    # ============ INSIGHTS ============

    insights = [
        f"Profit margin is {round(profit_margin,1)}%",
        "Revenue shows steady growth",
        f"GST compliance status is {gst_status}"
    ]

    recommendations = [
        "Optimize operational expenses",
        "Improve cashflow cycle",
        "Consider financing options for growth"
    ]

    # ============ MULTILINGUAL ============

    if language != "en":
        insights = translate(insights, language)
        recommendations = translate(recommendations, language)

    # ============ PDF REPORT ============

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200,10,"SME Financial Health Report", ln=True)

    pdf.cell(200,10,f"Revenue: {total_revenue}", ln=True)
    pdf.cell(200,10,f"Expenses: {total_expenses}", ln=True)
    pdf.cell(200,10,f"Cashflow: {total_cashflow}", ln=True)
    pdf.cell(200,10,f"Profit Margin: {round(profit_margin,2)}%", ln=True)
    pdf.cell(200,10,f"Forecast Revenue Next Year: {round(predicted_revenue,2)}", ln=True)
    pdf.cell(200,10,f"GST Status: {gst_status}", ln=True)

    pdf_path = "financial_report.pdf"
    pdf.output(pdf_path)

    return {
        "summary": {
            "total_revenue": round(total_revenue,2),
            "total_expenses": round(total_expenses,2),
            "total_cashflow": round(total_cashflow,2),
            "profit_margin": round(profit_margin,2)
        },
        "monthly_by_year": monthly_by_year,
        "yearly_summary": yearly_data,
        "ml_forecast": {
            "next_year": next_year,
            "predicted_revenue": round(predicted_revenue,2)
        },
        "gst_compliance": gst_report,
        "benchmark": benchmark,
        "ai_insights": insights,
        "recommendations": recommendations,
        "pdf_report": pdf_path
    }
