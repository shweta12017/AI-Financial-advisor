from typing import List, Tuple

import altair as alt
import pandas as pd

from models.financial_profile import FinancialProfile


def budget_allocation_chart(profile: FinancialProfile) -> alt.Chart:
    """Bar chart of the approximate budget breakdown."""
    breakdown = profile.budget_breakdown or {}
    data = [{"Category": k, "Ratio": float(v)} for k, v in breakdown.items()]
    df = pd.DataFrame(data)

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("Category:N", title="Category"),
            y=alt.Y("Ratio:Q", axis=alt.Axis(format="%"), title="Portion of income"),
            color="Category:N",
            tooltip=["Category", alt.Tooltip("Ratio:Q", format=".1%")],
        )
        .properties(title="Budget breakdown")
    )
    return chart


def dti_chart(profile: FinancialProfile) -> alt.Chart:
    """Bar chart comparing monthly income vs. monthly debt payments."""
    data = [
        {"Type": "Income", "Amount": profile.monthly_income},
        {"Type": "Debt payments", "Amount": profile.monthly_debt_payments},
    ]
    df = pd.DataFrame(data)

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("Type:N", title=""),
            y=alt.Y("Amount:Q", title="Monthly amount"),
            color="Type:N",
            tooltip=["Type", alt.Tooltip("Amount:Q", format=",.2f")],
        )
        .properties(title="Income vs. Debt payments")
    )
    return chart


def goal_projection_chart(
    projection_points: List[Tuple[float, float]],
    target_amount: float | None = None,
) -> alt.Chart:
    """Line chart of projected balance over time with an optional goal target line."""
    df = pd.DataFrame(
        [{"Year": year, "Balance": balance} for year, balance in projection_points]
    )

    base = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Year:Q", title="Years from now"),
            y=alt.Y("Balance:Q", title="Projected balance"),
            tooltip=[
                alt.Tooltip("Year:Q", format=".0f"),
                alt.Tooltip("Balance:Q", format=",.2f"),
            ],
        )
        .properties(title="Goal projection")
    )

    if target_amount and target_amount > 0:
        target_df = pd.DataFrame(
            [
                {"Year": df["Year"].min(), "Target": target_amount},
                {"Year": df["Year"].max(), "Target": target_amount},
            ]
        )
        target_line = (
            alt.Chart(target_df)
            .mark_rule(color="red", strokeDash=[4, 4])
            .encode(
                x="Year:Q",
                y="Target:Q",
                tooltip=[
                    alt.Tooltip("Target:Q", format=",.2f", title="Target amount")
                ],
            )
        )
        return base + target_line

    return base

