"""
Main dashboard page for the AI Financial Advisor.

This module is responsible for:
- Collecting core financial inputs
- Computing the primary FinancialProfile and derived metrics
- Persisting key values into `st.session_state` for use by other pages
"""

from __future__ import annotations

import streamlit as st

from config.settings import settings
from models.financial_profile import FinancialProfile
from services.advice_generator import generate_advice
from services.financial_calculations import (
    populate_derived_metrics,
    recommend_emergency_fund,
)
from services.health_score import compute_health_score
from services.risk_profile import compute_risk_profile
from utils.validators import to_positive_float
from visualization.charts import budget_allocation_chart, dti_chart


def _store_shared_state(
    profile: FinancialProfile,
    expected_return: float,
    emergency_months: int,
    risk_profile,
    advice_markdown: str,
) -> None:
    """Persist shared objects into session_state for other pages."""
    st.session_state["profile"] = profile
    st.session_state["expected_return"] = expected_return
    st.session_state["emergency_months"] = emergency_months
    st.session_state["risk_profile"] = risk_profile
    st.session_state["advice_markdown"] = advice_markdown


def render() -> None:
    """Render the main dashboard page."""
    # Custom CSS for better styling with blue, red, green, and golden theme
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #1e40af 0%, #dc2626 33%, #16a34a 66%, #fbbf24 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .metric-card {
            background: linear-gradient(135deg, #fef3c7 0%, #ffffff 100%);
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(251, 191, 36, 0.2);
            border-left: 4px solid #fbbf24;
        }
        .form-section {
            background: linear-gradient(135deg, #dbeafe 0%, #ffffff 100%);
            border: 2px solid #1e40af;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .stSlider > div > div > div {
            background: linear-gradient(90deg, #dc2626 0%, #16a34a 100%);
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(90deg, #1e40af 0%, #dc2626 100%);
            border: none;
            color: white;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"><h1>💰 AI Financial Advisor</h1><p>Interactive, AI-assisted financial planning dashboard</p><p><small>For educational purposes only – not professional advice</small></p></div>', unsafe_allow_html=True)

    # Sidebar: planning assumptions (also stored in session_state)
    with st.sidebar:
        st.subheader("Planning assumptions")
        expected_return = st.slider(
            "Expected annual return (for projections)",
            min_value=0.0,
            max_value=0.15,
            value=float(
                st.session_state.get(
                    "expected_return",
                    settings.default_expected_return_annual,
                )
            ),
            step=0.005,
            format="%.2f",
        )
        emergency_months = st.slider(
            "Target emergency fund (months of expenses)",
            min_value=1,
            max_value=12,
            value=int(st.session_state.get("emergency_months", 6)),
            step=1,
        )

    # Input form keeps UI clean and avoids partial reruns while typing
    with st.form("financial_inputs"):
        st.markdown('<div class="form-section"><h3>📊 Financial inputs</h3></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            income = to_positive_float(
                st.number_input(
                    "Monthly income",
                    min_value=0.0,
                    value=5000.0,
                    step=100.0,
                    help="Gross monthly income before tax.",
                )
            )
            expenses = to_positive_float(
                st.number_input(
                    "Monthly expenses",
                    min_value=0.0,
                    value=3000.0,
                    step=100.0,
                    help="Total fixed + variable expenses.",
                )
            )
            savings = to_positive_float(
                st.number_input(
                    "Current monthly savings / investing",
                    min_value=0.0,
                    value=500.0,
                    step=50.0,
                    help="Amount you are currently saving or investing each month.",
                )
            )

        with col2:
            debt_payments = to_positive_float(
                st.number_input(
                    "Monthly debt payments",
                    min_value=0.0,
                    value=400.0,
                    step=50.0,
                    help="Total monthly payments on loans, credit cards, etc.",
                )
            )

            st.markdown("#### Goal planning (summary)")
            goal_name = st.text_input("Primary goal name", value="Retirement")
            goal_target_amount = to_positive_float(
                st.number_input(
                    "Goal target amount (total)",
                    min_value=0.0,
                    value=500_000.0,
                    step=10_000.0,
                )
            )
            goal_years = to_positive_float(
                st.number_input(
                    "Time horizon (years)",
                    min_value=0.0,
                    value=25.0,
                    step=1.0,
                )
            )
            risk_tolerance_choice = st.selectbox(
                "Self-reported risk tolerance",
                options=["Low", "Medium", "High"],
                index=1,
            )

        with st.expander("Risk profiling questionnaire", expanded=False):
            q1 = st.slider(
                "How comfortable are you with short-term losses?",
                1,
                5,
                3,
            )
            q2 = st.slider("Investment experience level", 1, 5, 3)
            q3 = st.slider("How long until you need this money?", 1, 5, 3)
            q4 = st.slider("How would you react to a 20% drop?", 1, 5, 3)
            risk_answers = {"q1": q1, "q2": q2, "q3": q3, "q4": q4}

        submitted = st.form_submit_button("🚀 Analyze my finances", type="primary")

    if not submitted:
        # If we already have a profile in session, show a brief summary instead
        profile: FinancialProfile | None = st.session_state.get("profile")
        if profile is None:
            st.info(
                "Enter your numbers above and click **Analyze my finances** "
                "to see your financial health, goals, and AI-generated insights."
            )
        else:
            st.success("Using your most recent analysis. Navigate using the sidebar.")
        return

    if income <= 0:
        st.error("Monthly income must be greater than 0 to run an analysis.")
        return

    # Build profile and compute derived metrics
    profile = FinancialProfile(
        monthly_income=income,
        monthly_expenses=expenses,
        monthly_savings=savings,
        monthly_debt_payments=debt_payments,
        goal_name=goal_name if goal_name else None,
        goal_target_amount=goal_target_amount or None,
        goal_time_horizon_years=goal_years or None,
        risk_tolerance= risk_tolerance_choice,
    )
    profile = populate_derived_metrics(profile)

    # Risk profile from questionnaire
    risk_profile = compute_risk_profile(risk_answers)

    # Derived recommendations
    emergency_target = recommend_emergency_fund(
        monthly_expenses=profile.monthly_expenses,
        target_months=float(emergency_months),
    )

    # Pre-compute AI advice for reuse on other pages
    with st.spinner("Contacting AI financial advisor..."):
        advice_markdown = generate_advice(profile)

    # Persist key objects into session_state
    _store_shared_state(
        profile=profile,
        expected_return=expected_return,
        emergency_months=emergency_months,
        risk_profile=risk_profile,
        advice_markdown=advice_markdown,
    )

    # Quick summary cards and charts on the dashboard itself
    st.markdown('<div class="form-section"><h3>📈 Snapshot of your financial health</h3></div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("💳 Savings rate", f"{profile.savings_rate * 100:.1f}%")
    with m2:
        st.metric("📊 Expense ratio", f"{profile.expense_ratio * 100:.1f}%")
    with m3:
        st.metric(
            "⚖️ Debt-to-income (DTI)",
            f"{profile.debt_to_income_ratio * 100:.1f}%",
        )
    with m4:
        st.metric("💵 Free cash flow", f"${profile.free_cash_flow:,.2f}")

    health = compute_health_score(
        profile,
        target_emergency_months=float(emergency_months),
    )
    
    # Health score with color coding
    health_color = "🟢" if health.score >= 80 else "🟡" if health.score >= 60 else "🔴"
    grade_color = "green" if health.grade in ["A", "B"] else "orange" if health.grade == "C" else "red"
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"{health_color} Financial health score", f"{health.score}/100")
    with col2:
        st.markdown(f"<h3 style='color: {grade_color}; text-align: center; margin: 0;'>Health Grade: {health.grade}</h3>", unsafe_allow_html=True)

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

    with st.expander("🆘 Emergency fund & risk profile", expanded=True):
        st.markdown(f"""
        <div class="metric-card">
            <h4>🛡️ Emergency Fund Target</h4>
            <p>For <strong>{emergency_months} months</strong> of expenses, your recommended emergency fund is approximately:</p>
            <h3 style="color: #667eea;">${emergency_target:,.2f}</h3>
        </div>
        
        <div class="metric-card" style="margin-top: 1rem;">
            <h4>🎯 Risk Profile</h4>
            <p><strong>Risk score:</strong> {risk_profile.score}/100 ({risk_profile.level.value})</p>
            <p><em>{risk_profile.reasoning}</em></p>
        </div>
        """, unsafe_allow_html=True)


__all__ = ["render"]

