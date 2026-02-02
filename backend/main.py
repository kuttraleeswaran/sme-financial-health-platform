from fastapi import FastAPI, UploadFile, File
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from .finance_engine import analyze_financials


from backend.finance_engine import analyze_financials, forecast_revenue, compare_with_industry

from ai_engine import generate_ai_insights

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ------------------------
# Store last analysis
# ------------------------

last_result = {}

@app.get("/")
def home():
    return {"message": "Backend Running"}


# ========================
# Upload & Analyze
# ========================

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    df = pd.read_csv(file.file)

    summary = analyze_financials(df)
    forecast = forecast_revenue(df)
    benchmark = compare_with_industry(summary, "retail")

    ai_insights = generate_ai_insights(summary, language="en")

    global last_result

    last_result = {
        "summary": summary,
        "forecast": forecast,
        "benchmark": benchmark,
        "ai_insights": ai_insights
    }

    return last_result


# ========================
# Dynamic PDF Generator
# ========================

@app.get("/download-report")
def download_report():

    if not last_result:
        return {"error": "Please upload financial data first"}

    file_name = "financial_report.pdf"

    c = canvas.Canvas(file_name, pagesize=A4)
    y = 800

    def draw(text):
        nonlocal y
        c.drawString(50, y, text)
        y -= 22

    summary = last_result["summary"]
    forecast = last_result["forecast"]
    benchmark = last_result["benchmark"]
    insights = last_result["ai_insights"].split("\n")

    # ---------------- Title ----------------

    draw("SME FINANCIAL HEALTH REPORT")
    y -= 15

    # ---------------- Summary ----------------

    draw(f"Health Score: {summary['health_score']}")
    draw(f"Average Revenue: ₹{summary['avg_revenue']}")
    draw(f"Profit Margin: {summary['profit_margin']}%")
    draw(f"Cash Gap: ₹{summary['cash_gap']}")

    y -= 10

    # ---------------- Forecast ----------------

    draw("Revenue Forecast:")

    for i, val in enumerate(forecast, 1):
        draw(f" Month {i}: ₹{val}")

    y -= 10

    # ---------------- Benchmark ----------------

    draw("Industry Benchmark:")

    draw(f" Industry: {benchmark['industry']}")
    draw(f" Your Margin: {benchmark['your_profit_margin']}%")
    draw(f" Industry Avg Margin: {benchmark['industry_profit_margin']}%")
    draw(f" Your Health Score: {benchmark['your_health_score']}")
    draw(f" Industry Health Score: {benchmark['industry_health_score']}")

    y -= 10

    # ---------------- Risks ----------------

    draw("Identified Risks:")

    if len(summary["risks"]) == 0:
        draw(" None detected")
    else:
        for r in summary["risks"]:
            draw(f" - {r}")

    y -= 10

    # ---------------- AI Insights ----------------

    draw("AI Recommendations:")

    for line in insights:
        if line.strip():
            draw(f" {line}")

    c.save()

    return FileResponse(file_name, filename=file_name)
