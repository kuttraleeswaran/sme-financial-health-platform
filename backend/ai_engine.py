def generate_ai_insights(summary, language="en"):
    
    if language == "hi":
        return f"""
वित्तीय स्वास्थ्य स्कोर: {summary['health_score']}

औसत आय: ₹{summary['avg_revenue']}
लाभ प्रतिशत: {summary['profit_margin']}%

मुख्य सलाह:
- खर्च कम करें
- ग्राहकों से भुगतान जल्दी लें
- नकद बचत बनाए रखें
- समय पर ऋण भुगतान करें
"""

    # English default
    return f"""
Financial Health Score: {summary['health_score']}

Average Revenue: ₹{summary['avg_revenue']}
Profit Margin: {summary['profit_margin']}%

Key Recommendations:
- Reduce unnecessary expenses
- Improve customer collections
- Maintain emergency cash buffer
- Monitor loan repayments carefully
"""
