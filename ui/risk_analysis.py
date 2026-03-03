"""
Risk and financial health analysis page.

Shows key ratios, scores, and charts based on the current FinancialProfile.
"""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go

from models.financial_profile import FinancialProfile
from services.financial_calculations import recommend_emergency_fund
from services.health_score import compute_health_score
from visualization.charts import budget_allocation_chart, dti_chart


def _get_profile() -> FinancialProfile | None:
    return st.session_state.get("profile")


def render() -> None:
    """Render the risk and financial health analysis page."""
    # Custom CSS for risk analysis styling with blue, red, green, and golden theme
    st.markdown("""
    <style>
        .risk-header {
            background: linear-gradient(90deg, #dc2626 0%, #fbbf24 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            text-align: center;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .metric-card {
            background: linear-gradient(135deg, #fef3c7 0%, #ffffff 100%);
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(251, 191, 36, 0.2);
            border-left: 4px solid #dc2626;
            margin-bottom: 1rem;
        }
        .high-risk { border-left-color: #dc2626; }
        .medium-risk { border-left-color: #fbbf24; }
        .low-risk { border-left-color: #16a34a; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="risk-header"><h2>🔴 Financial Health & Risk Analysis</h2><p>Understand your financial strengths and areas for improvement</p></div>', unsafe_allow_html=True)

    profile = _get_profile()
    if profile is None:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 No Financial Profile Found</h4>
            <p>To analyze your financial health and risk profile:</p>
            <ol>
                <li>Go to the <strong>Dashboard</strong> page</li>
                <li>Enter your financial details</li>
                <li>Run an analysis</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        return

    emergency_months = int(st.session_state.get("emergency_months", 6))
    risk_profile = st.session_state.get("risk_profile")

    # Key metrics with risk indicators
    st.markdown('<h3>📈 Key Financial Metrics</h3>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    
    # Determine risk levels for color coding
    savings_risk = "🟢" if profile.savings_rate >= 0.2 else "🟡" if profile.savings_rate >= 0.1 else "🔴"
    expense_risk = "🟢" if profile.expense_ratio <= 0.7 else "🟡" if profile.expense_ratio <= 0.85 else "🔴"
    dti_risk = "🟢" if profile.debt_to_income_ratio <= 0.36 else "🟡" if profile.debt_to_income_ratio <= 0.43 else "🔴"
    cashflow_risk = "🟢" if profile.free_cash_flow > 0 else "🔴"
    
    with m1:
        st.metric(f"{savings_risk} Savings rate", f"{profile.savings_rate * 100:.1f}%")
    with m2:
        st.metric(f"{expense_risk} Expense ratio", f"{profile.expense_ratio * 100:.1f}%")
    with m3:
        st.metric(
            f"{dti_risk} Debt-to-income (DTI)",
            f"{profile.debt_to_income_ratio * 100:.1f}%",
        )
    with m4:
        st.metric(f"{cashflow_risk} Free cash flow", f"${profile.free_cash_flow:,.2f}")

    # Health score
    health = compute_health_score(
        profile,
        target_emergency_months=float(emergency_months),
    )

    col_score, col_gauge = st.columns([1, 2])
    with col_score:
        st.metric("Financial health score", f"{health.score}/100")
        st.metric("Health grade", health.grade)

        # Color-coded stability indicator
        if health.score >= 85:
            stability = "Stable / Very strong"
            color = "green"
        elif health.score >= 70:
            stability = "Stable / Solid"
            color = "limegreen"
        elif health.score >= 55:
            stability = "Watch list / Needs attention"
            color = "orange"
        elif health.score >= 40:
            stability = "Stressed / High risk"
            color = "orangered"
        else:
            stability = "Critical / Very high risk"
            color = "red"

        st.markdown(
            f"**Stability status:** "
            f"<span style='color:{color}; font-weight:bold'>{stability}</span>",
            unsafe_allow_html=True,
        )

    with col_gauge:
        # Plotly gauge for health score
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=health.score,
                number={"suffix": "/100"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "darkblue"},
                    "steps": [
                        {"range": [0, 40], "color": "#ff4d4d"},
                        {"range": [40, 55], "color": "#ff944d"},
                        {"range": [55, 70], "color": "#ffd24d"},
                        {"range": [70, 85], "color": "#b3ff66"},
                        {"range": [85, 100], "color": "#33cc33"},
                    ],
                },
            )
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=220,
        )
        st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.altair_chart(
            budget_allocation_chart(profile),
            use_container_width=True,
        )
    with c2:
        st.altair_chart(
            dti_chart(profile),
            use_container_width=True,
        )

    emergency_target = recommend_emergency_fund(
        monthly_expenses=profile.monthly_expenses,
        target_months=float(emergency_months),
    )

    with st.expander("Emergency fund & risk profile", expanded=True):
        st.write(
            f"For **{emergency_months} months** of expenses, your "
            f"recommended emergency fund is approximately "
            f"**{emergency_target:,.2f}**."
        )
        if risk_profile is not None:
            st.write(
                f"Risk score: **{risk_profile.score}/100** "
                f"({risk_profile.level.value}). {risk_profile.reasoning}"
            )
        else:
            st.write(
                "No risk questionnaire has been completed yet. "
                "Fill it out on the Dashboard to see a risk profile here."
            )

    # Explanation of score factors
    with st.expander("How is my score calculated?"):
        st.markdown(
            "- **Savings rate (max 40 pts)**: Higher savings as a share of income "
            "improves your score up to roughly 30% of income.\n"
            "- **Debt-to-income (max 30 pts)**: Lower DTI, especially below 36%, "
            "is viewed as healthier.\n"
            "- **Emergency fund (max 30 pts)**: Having an emergency fund that covers "
            f"around {emergency_months} months of expenses increases your score."
        )
        st.write("Component scores:", health.components)

    # Suggestions based on score range
    with st.expander("Suggestions to improve your financial health"):
        if health.score >= 85:
            st.markdown(
                "- You are in a **very strong position**. Consider:\n"
                "  - Fine-tuning your investment mix to match your risk tolerance.\n"
                "  - Focusing on long-term tax efficiency and estate planning.\n"
                "  - Stress-testing your plan against different market scenarios."
            )
        elif health.score >= 70:
            st.markdown(
                "- Your situation is **solid**, with room for optimization:\n"
                "  - Gradually increase your savings rate toward your target.\n"
                "  - Pay down any higher-interest debt to reduce future risk.\n"
                "  - Ensure your emergency fund target is fully funded."
            )
        elif health.score >= 55:
            st.markdown(
                "- You are in a **moderate** position:\n"
                "  - Aim to grow your savings rate over the next 6–12 months.\n"
                "  - Prioritize paying down non-essential or high-cost debt.\n"
                "  - Build at least 3 months of essential expenses in cash.\n"
            )
        elif health.score >= 40:
            st.markdown(
                "- Your finances appear **stressed**:\n"
                "  - Create a strict budget to free up cash for debt reduction.\n"
                "  - Avoid new debt and consider consolidating expensive debt.\n"
                "  - Build a minimal emergency buffer (1–2 months) as soon as possible."
            )
        else:
            st.markdown(
                "- Your score indicates a **critical** situation:\n"
                "  - Focus first on essential expenses and avoiding new debt.\n"
                "  - Seek personalized advice from a qualified financial professional.\n"
                "  - Look for ways to increase income and reduce fixed costs.\n"
            )


__all__ = ["render"]

