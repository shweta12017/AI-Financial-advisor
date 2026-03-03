"""
Goal planning and projection page.

Uses the FinancialProfile and assumptions stored in `st.session_state`
by the dashboard page to render tailored savings targets and projections.
"""

from __future__ import annotations

import streamlit as st
import altair as alt

from models.financial_profile import FinancialProfile
from services.financial_calculations import (
    build_projection_series,
    goal_monthly_savings_requirement,
)
from services.projection_scenarios import build_savings_scenarios
from utils.validators import validate_goal
from visualization.charts import goal_projection_chart


def _get_profile() -> FinancialProfile | None:
    return st.session_state.get("profile")


def render() -> None:
    """Render the goal planning and projections page."""
    # Custom CSS for goal planner styling with blue, red, green, and golden theme
    st.markdown("""
    <style>
        .goal-header {
            background: linear-gradient(90deg, #16a34a 0%, #1e40af 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            text-align: center;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .goal-card {
            background: linear-gradient(135deg, #fef3c7 0%, #ffffff 100%);
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(251, 191, 36, 0.2);
            border-left: 4px solid #16a34a;
            margin-bottom: 1rem;
        }
        .success-goal { border-left-color: #16a34a; }
        .warning-goal { border-left-color: #fbbf24; }
        .danger-goal { border-left-color: #dc2626; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="goal-header"><h2>🟢 Goal Planning & Projections</h2><p>Plan your financial future with smart projections and scenarios</p></div>', unsafe_allow_html=True)

    profile = _get_profile()
    if profile is None:
        st.markdown("""
        <div class="goal-card">
            <h4>📊 No Financial Profile Found</h4>
            <p>To plan your financial goals:</p>
            <ol>
                <li>Go to the <strong>Dashboard</strong> page</li>
                <li>Enter your financial details</li>
                <li>Set your goal information</li>
                <li>Run an analysis</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        return

    expected_return = float(
        st.session_state.get("expected_return", 0.06)
    )

    if not profile.goal_target_amount or not profile.goal_time_horizon_years:
        st.markdown("""
        <div class="goal-card warning-goal">
            <h4>🎯 No Goal Information Set</h4>
            <p>To see projections and planning scenarios:</p>
            <ol>
                <li>Go to the <strong>Dashboard</strong> page</li>
                <li>Update your goal details (target amount and time horizon)</li>
                <li>Come back here for detailed projections</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        return

    valid_goal, message = validate_goal(
        profile.goal_target_amount,
        profile.goal_time_horizon_years,
    )
    if not valid_goal:
        st.warning(message)
        return

    required_monthly = goal_monthly_savings_requirement(
        target_amount=profile.goal_target_amount,
        years=profile.goal_time_horizon_years,
        annual_return=expected_return,
    )

    st.markdown(
        f"To reach **{profile.goal_name}** in "
        f"**{profile.goal_time_horizon_years:.1f} years**, you should "
        f"aim to save about **{required_monthly:,.2f} per month**, "
        f"assuming an annual return of {expected_return * 100:.1f}%."
    )

    projection = build_projection_series(
        current_savings=0.0,
        monthly_contribution=required_monthly,
        years=profile.goal_time_horizon_years,
        annual_return=expected_return,
    )
    st.altair_chart(
        goal_projection_chart(
            projection_points=projection,
            target_amount=profile.goal_target_amount,
        ),
        use_container_width=True,
    )

    # Predictive savings projection scenarios
    st.markdown("### What if I save more?")
    scenario_df = build_savings_scenarios(
        current_savings=0.0,
        base_monthly_savings=profile.monthly_savings,
        years=profile.goal_time_horizon_years,
        annual_return=expected_return,
    )
    scenario_chart = (
        alt.Chart(scenario_df)
        .mark_line()
        .encode(
            x="Year:Q",
            y="Balance:Q",
            color="Scenario:N",
            tooltip=["Year", "Balance", "Scenario"],
        )
        .properties(title="Predictive savings projections by scenario")
    )
    st.altair_chart(scenario_chart, use_container_width=True)


__all__ = ["render"]

