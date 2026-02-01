import pandas as pd

# =============================
# Financial Analysis Engine
# =============================

def analyze_financials(df):

    avg_revenue = df['revenue'].mean()
    avg_expenses = df['expenses'].mean()

    profit_margin = ((avg_revenue - avg_expenses) / avg_revenue) * 100

    receivables = df['receivables'].mean()
    payables = df['payables'].mean()

    cash_gap = receivables - payables

    loan_payment = df['loan_payment'].mean()

    score = 0

    # Profitability
    if profit_margin > 20:
        score += 30
    elif profit_margin > 10:
        score += 20
    else:
        score += 10

    # Liquidity
    if cash_gap < 50000:
        score += 30
    else:
        score += 15

    # Debt
    if loan_payment < avg_revenue * 0.1:
        score += 20
    else:
        score += 10

    # Compliance placeholder
    score += 20

    risks = []

    if profit_margin < 15:
        risks.append("Low profitability")

    if receivables > 100000:
        risks.append("High outstanding receivables")

    if avg_expenses > avg_revenue * 0.8:
        risks.append("High operating costs")

    summary = {
        "avg_revenue": round(avg_revenue, 2),
        "avg_expenses": round(avg_expenses, 2),
        "profit_margin": round(profit_margin, 2),
        "health_score": score,
        "cash_gap": round(cash_gap, 2),
        "risks": risks
    }

    return summary


# =============================
# Revenue Forecast Engine
# =============================

def forecast_revenue(df, months=3):

    revenues = df['revenue'].values

    growth = (revenues[-1] - revenues[0]) / len(revenues)

    forecasts = []
    last_val = revenues[-1]

    for _ in range(months):
        next_val = last_val + growth
        forecasts.append(round(next_val, 2))
        last_val = next_val

    return forecasts


# =============================
# Industry Benchmark (Mock)
# =============================

INDUSTRY_BENCHMARKS = {
    "retail": {"profit_margin": 20, "health_score": 75},
    "manufacturing": {"profit_margin": 18, "health_score": 70},
    "services": {"profit_margin": 25, "health_score": 80}
}

def compare_with_industry(summary, industry="retail"):

    benchmark = INDUSTRY_BENCHMARKS[industry]

    return {
        "industry": industry,
        "your_profit_margin": summary["profit_margin"],
        "industry_profit_margin": benchmark["profit_margin"],
        "your_health_score": summary["health_score"],
        "industry_health_score": benchmark["health_score"]
    }
