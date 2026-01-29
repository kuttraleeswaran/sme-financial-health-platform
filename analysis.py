import pandas as pd
import numpy as np

def analyze_data(df):

    # Ensure required columns exist
    required_cols = ["Revenue", "Expenses", "Loan_Payment", "Receivables", "Inventory", "Tax"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # ---------------- BASIC CALCULATIONS ----------------

    total_revenue = df["Revenue"].sum()
    total_expenses = df["Expenses"].sum()
    total_cashflow = total_revenue - total_expenses

    avg_revenue = df["Revenue"].mean()
    avg_expenses = df["Expenses"].mean()

    # ---------------- CREDIT SCORE (simple model) ----------------

    debt_ratio = df["Loan_Payment"].sum() / total_revenue

    if debt_ratio < 0.2:
        credit_score = 800
    elif debt_ratio < 0.4:
        credit_score = 650
    else:
        credit_score = 500

    # ---------------- RISK DETECTION ----------------

    risks = []

    if total_cashflow < 0:
        risks.append("Negative cash flow")

    if debt_ratio > 0.4:
        risks.append("High debt burden")

    if df["Receivables"].mean() > avg_revenue * 0.5:
        risks.append("High unpaid receivables")

    if not risks:
        risks.append("Low financial risk")

    # ---------------- COST OPTIMIZATION ----------------

    suggestions = []

    expense_ratio = total_expenses / total_revenue

    if expense_ratio > 0.7:
        suggestions.append("Reduce operational costs")

    if df["Inventory"].mean() > avg_revenue:
        suggestions.append("Optimize inventory levels")

    if not suggestions:
        suggestions.append("Costs are well managed")

    # ---------------- AI FORECASTING ----------------

    df["Revenue_Change"] = df["Revenue"].diff()
    df["Expenses_Change"] = df["Expenses"].diff()

    avg_rev_growth = df["Revenue_Change"].mean()
    avg_exp_growth = df["Expenses_Change"].mean()

    last_revenue = df["Revenue"].iloc[-1]
    last_expenses = df["Expenses"].iloc[-1]

    forecast_revenue = last_revenue + avg_rev_growth
    forecast_expenses = last_expenses + avg_exp_growth
    forecast_cashflow = forecast_revenue - forecast_expenses

    # ---------------- INDUSTRY BENCHMARK (MOCK DATA) ----------------

    industry_avg_margin = 0.25  # 25%

    company_margin = total_cashflow / total_revenue

    if company_margin > industry_avg_margin:
        benchmark_status = "Above industry average"
    else:
        benchmark_status = "Below industry average"

    # ---------------- GST COMPLIANCE CHECK ----------------

    expected_tax = total_revenue * 0.05
    actual_tax = df["Tax"].sum()

    gst_compliance = "Compliant" if actual_tax >= expected_tax * 0.9 else "Non-compliant"

    # ---------------- FINANCIAL HEALTH SUMMARY ----------------

    if total_cashflow > 0 and credit_score > 650:
        financial_health = "Good"
    elif total_cashflow > 0:
        financial_health = "Average"
    else:
        financial_health = "Poor"

    # ---------------- FINAL RESPONSE ----------------

    return {
        "totals": {
            "revenue": round(float(total_revenue), 2),
            "expenses": round(float(total_expenses), 2),
            "cashflow": round(float(total_cashflow), 2)
        },

        "averages": {
            "revenue": round(float(avg_revenue), 2),
            "expenses": round(float(avg_expenses), 2)
        },

        "credit_score": credit_score,

        "risks": risks,

        "cost_optimization": suggestions,

        "forecast": {
            "next_revenue": round(float(forecast_revenue), 2),
            "next_expenses": round(float(forecast_expenses), 2),
            "next_cashflow": round(float(forecast_cashflow), 2)
        },

        "industry_benchmark": benchmark_status,

        "gst_compliance": gst_compliance,

        "financial_health": financial_health
    }
