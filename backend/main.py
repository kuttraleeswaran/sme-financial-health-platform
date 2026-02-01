from fastapi import FastAPI, UploadFile, File
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

from finance_engine import (
    analyze_financials,
    forecast_revenue,
    compare_with_industry
)

from ai_engine import generate_ai_insights

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from fastapi.responses import FileResponse

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {"message": "SME Financial AI Backend Running"}


# =============================
# Upload & Analyze
# =============================

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    df = pd.read_csv(file.file)

    summary = analyze_financials(df)

    forecast = forecast_revenue(df)

    benchmark = compare_with_industry(summary, industry="retail")

    # Change language="hi" for Hindi
    ai_insights = generate_ai_insights(summary, language="en")

    return {
        "summary": summary,
        "forecast": forecast,
        "benchmark": benchmark,
        "ai_insights": ai_insights
    }


# =============================
# PDF Report Download
# =============================
@app.get("/download-report")
def download_report():

    file_name = "financial_report.pdf"

    # Sample data for now (in real app you can pass last analyzed data)
    health_score = 100
    profit_margin = 28
    forecast = [473333, 466666, 460000]

    benchmark = {
        "industry": "retail",
        "industry_profit_margin": 20,
        "industry_health_score": 75
    }

    risks = ["No major risks detected"]

    insights = [
        "Reduce unnecessary expenses",
        "Improve customer collections",
        "Maintain emergency cash buffer",
        "Monitor loan repayments carefully"
    ]

    c = canvas.Canvas(file_name, pagesize=A4)

    y = 800

    def draw(text):
        nonlocal y
        c.drawString(50, y, text)
        y -= 25

    # --------------------
    # Title
    # --------------------
    draw("SME FINANCIAL HEALTH REPORT")
    y -= 20

    # --------------------
    # Summary
    # --------------------
    draw(f"Health Score: {health_score}")
    draw(f"Profit Margin: {profit_margin}%")

    y -= 15

    # --------------------
    # Forecast
    # --------------------
    draw("Revenue Forecast (Next 3 Months):")

    for i, val in enumerate(forecast, 1):
        draw(f"  Month {i}: ₹{val}")

    y -= 15

    # --------------------
    # Industry Benchmark
    # --------------------
    draw("Industry Benchmark Comparison:")
    draw(f"  Industry: {benchmark['industry']}")
    draw(f"  Industry Avg Margin: {benchmark['industry_profit_margin']}%")
    draw(f"  Industry Health Score: {benchmark['industry_health_score']}")

    y -= 15

    # --------------------
    # Risks
    # --------------------
    draw("Identified Risks:")

    for r in risks:
        draw(f"  - {r}")

    y -= 15

    # --------------------
    # AI Insights
    # --------------------
    draw("AI Recommendations:")

    for tip in insights:
        draw(f"  - {tip}")

    c.save()

    return FileResponse(file_name, filename=file_name)

