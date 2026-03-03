"""
Fallback chatbot service that provides financial advice without API calls.
Used when Gemini API is unavailable due to quota or other issues.
"""

from __future__ import annotations

from typing import List
from models.financial_profile import FinancialProfile
from services.chatbot import ChatMessage


def get_finance_advice(query: str, profile: FinancialProfile) -> str:
    """Provide basic financial advice based on common questions and profile data."""
    
    query_lower = query.lower()
    
    # Salary and savings advice
    if "salary" in query_lower and "save" in query_lower:
        savings_rate = profile.savings_rate if profile.savings_rate > 0 else 0.10
        recommended_savings = profile.monthly_income * 0.20  # 20% rule
        
        return f"""
Based on your monthly salary of ${profile.monthly_income:,.2f}, here's my recommendation:

💰 **Recommended Savings: ${recommended_savings:,.2f} (20% of income)**

Your current savings rate is {savings_rate*100:.1f}%. Here's a breakdown:

📊 **Savings Guidelines:**
• **Emergency Fund**: 3-6 months of expenses
• **Retirement**: 15-20% of income  
• **Other Goals**: 5-10% of income

🎯 **Action Steps:**
1. Build emergency fund first (${profile.monthly_expenses * 6:,.2f})
2. Increase savings gradually to 20%
3. Automate savings transfers

💡 **Tip**: Start with what you can afford, then increase by 1% every few months.
"""

    # Investment advice
    elif "invest" in query_lower:
        return f"""
📈 **Investment Recommendations for Your Profile:**

Based on your risk tolerance ({profile.risk_tolerance}) and income:

🔹 **Conservative Mix** (if Low risk tolerance):
• 60% Bonds/Fixed deposits
• 30% Index funds
• 10% Gold/REITs

🔹 **Balanced Mix** (if Medium risk tolerance):
• 40% Bonds
• 50% Equity funds
• 10% Alternative investments

🔹 **Growth Mix** (if High risk tolerance):
• 20% Bonds
• 70% Equity funds
• 10% High-growth options

💰 **Monthly Investment**: Start with ${profile.monthly_savings:,.2f} and increase gradually.

⚠️ **Remember**: Past performance doesn't guarantee future results.
"""

    # Debt advice
    elif "debt" in query_lower or "loan" in query_lower:
        dti_ratio = profile.debt_to_income_ratio
        
        return f"""
⚖️ **Debt Management Strategy:**

Your current debt-to-income ratio: {dti_ratio*100:.1f}%

🎯 **Priority Order for Debt Repayment:**
1. **High-interest debt** (>18% APR) - Credit cards, personal loans
2. **Medium-interest debt** (10-18% APR) - Car loans, education loans  
3. **Low-interest debt** (<10% APR) - Home loans, student loans

💡 **Debt Reduction Tips:**
• Pay more than minimum on high-interest debt
• Consider debt consolidation if APR > 15%
• Avoid new debt while repaying existing loans

📊 **Healthy DTI Ratio**: Below 36% is ideal
"""

    # Emergency fund advice
    elif "emergency" in query_lower or "fund" in query_lower:
        emergency_target = profile.monthly_expenses * 6
        
        return f"""
🛡️ **Emergency Fund Planning:**

**Target Amount**: ${emergency_target:,.2f} (6 months of expenses)

🏦 **Where to Keep Emergency Fund:**
• High-yield savings account
• Liquid mutual funds
• Fixed deposits (easy withdrawal)

📈 **Building Your Fund:**
• Save ${emergency_target/12:,.2f} per month to reach goal in 1 year
• Or save ${emergency_target/24:,.2f} per month for 2-year plan

⚡ **When to Use Emergency Fund:**
• Medical emergencies
• Job loss
• Urgent home/car repairs
• Essential family needs

💡 **Rule**: Only use for true emergencies, replenish immediately after use.
"""

    # Retirement advice
    elif "retirement" in query_lower or "future" in query_lower:
        return f"""
🏖️ **Retirement Planning Guide:**

📊 **Retirement Savings Guidelines:**
• Start saving as early as possible
• Aim for 15-20% of income
• Increase contributions with salary hikes

🎯 **Retirement Corpus Target:**
• 25x your annual expenses (by age 60)
• For expenses of ${profile.monthly_expenses*12:,.2f}/year: target ${profile.monthly_expenses*12*25:,.2f}

💰 **Monthly Retirement Savings:**
${profile.monthly_income * 0.15:,.2f} (15% of current income)

📈 **Investment Options:**
• PPF/EPF (tax benefits)
• NPS (National Pension System)
• Mutual funds (equity-oriented)
• Real estate (long-term)

⚠️ **Key Factors:**
• Start early (power of compounding)
• Increase contributions with age
• Review and rebalance annually
"""

    # General financial health advice
    else:
        return f"""
📊 **Your Financial Health Summary:**

💳 **Income**: ${profile.monthly_income:,.2f}/month
💸 **Expenses**: ${profile.monthly_expenses:,.2f}/month ({profile.expense_ratio*100:.1f}%)
💰 **Savings**: ${profile.monthly_savings:,.2f}/month ({profile.savings_rate*100:.1f}%)
⚖️ **Debt**: ${profile.monthly_debt_payments:,.2f}/month ({profile.debt_to_income_ratio*100:.1f}% DTI)

🎯 **Key Recommendations:**
1. **Savings Rate**: Aim for 20% of income (you're at {profile.savings_rate*100:.1f}%)
2. **Emergency Fund**: Build 6 months expenses (${profile.monthly_expenses * 6:,.2f})
3. **Debt Management**: Keep DTI below 36% (you're at {profile.debt_to_income_ratio*100:.1f}%)
4. **Investments**: Start with mutual funds or index funds

💡 **Next Steps:**
• Track expenses for 1 month
• Set up automatic savings
• Review insurance coverage
• Start investment planning

📞 **For personalized advice**, consider consulting a certified financial advisor.

*This is educational advice only. Please consult professionals for personal financial planning.*
"""


def chat_reply_fallback(
    profile: FinancialProfile,
    history: List[ChatMessage],
) -> str:
    """
    Generate a chatbot response using fallback logic when API is unavailable.
    """
    if not history:
        return "Hello! I'm your financial assistant. Ask me about savings, investments, debt management, or retirement planning!"
    
    # Get the last user message
    last_message = history[-1]["content"] if history else ""
    
    # Generate advice based on the query
    return get_finance_advice(last_message, profile)


__all__ = ["chat_reply_fallback"]
