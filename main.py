from fastapi import FastAPI, UploadFile, File
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    df = pd.read_excel(file.file)

    # Ensure columns exist
    df["Year"] = df["Year"].astype(int)
    df["Month"] = df["Month"].astype(str)

    # 👉 Auto calculate Cashflow
    df["Cashflow"] = df["Revenue"] - df["Expenses"]

    # ---------------- TOTALS ----------------

    totals = {
        "revenue": float(df["Revenue"].sum()),
        "expenses": float(df["Expenses"].sum()),
        "cashflow": float(df["Cashflow"].sum())
    }

    # ---------------- MONTHLY ----------------

    monthly = (
        df.groupby(["Year", "Month"])
        .sum(numeric_only=True)
        .reset_index()
        .to_dict(orient="records")
    )

    for row in monthly:
        row["Year"] = int(row["Year"])
        row["Revenue"] = float(row["Revenue"])
        row["Expenses"] = float(row["Expenses"])
        row["Cashflow"] = float(row["Cashflow"])

    # ---------------- YEARLY ----------------

    yearly = (
        df.groupby("Year")
        .sum(numeric_only=True)
        .reset_index()
        .to_dict(orient="records")
    )

    for row in yearly:
        row["Year"] = int(row["Year"])
        row["Revenue"] = float(row["Revenue"])
        row["Expenses"] = float(row["Expenses"])
        row["Cashflow"] = float(row["Cashflow"])

    # ---------------- KPIs ----------------

    profit = totals["revenue"] - totals["expenses"]
    profit_margin = (profit / totals["revenue"]) * 100

    growth = ((yearly[-1]["Revenue"] - yearly[0]["Revenue"]) / yearly[0]["Revenue"]) * 100

    credit_score = int(min(850, 650 + profit_margin * 4))

    if profit_margin > 20:
        risk = "Low Risk"
    elif profit_margin > 10:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    kpis = {
        "profit_margin": round(profit_margin,2),
        "growth_percent": round(growth,2),
        "credit_score": credit_score,
        "risk_level": risk
    }

    # ---------------- AI INSIGHTS ----------------

    insights = [
        f"Total Revenue: ₹{int(totals['revenue'])}",
        f"Total Expenses: ₹{int(totals['expenses'])}",
        f"Profit Margin: {round(profit_margin,1)}%",
        f"Business Risk: {risk}"
    ]

    # ---------------- AI RECOMMENDATIONS ----------------

    recommendations = []

    if profit_margin < 15:
        recommendations.append("Reduce operating expenses to improve profit.")

    if growth < 5:
        recommendations.append("Focus on increasing sales and marketing.")

    if risk != "Low Risk":
        recommendations.append("Improve cashflow management.")

    if not recommendations:
        recommendations.append("Financial performance is strong. Maintain current strategy.")

    return {
        "totals": totals,
        "monthly": monthly,
        "yearly": yearly,
        "kpis": kpis,
        "insights": insights,
        "recommendations": recommendations
    }
