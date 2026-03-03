"""
Domain-level financial calculation engine.

This module contains pure calculation functions with no dependency on
Streamlit or the AI layer. Application services are expected to call
these helpers and, where needed, inject configuration defaults such as
expected returns.
"""

from __future__ import annotations

from math import isfinite
from typing import Dict, List, Tuple


def calculate_savings_rate(income: float, savings: float) -> float:
    """
    Calculate the savings rate for a given income and savings amount.

    savings_rate = savings / income

    If income is zero or negative, this function returns 0.0.
    """
    if income <= 0:
        return 0.0
    return savings / income


def calculate_expense_ratio(income: float, expenses: float) -> float:
    """
    Calculate the expense ratio for a given income and expense amount.

    expense_ratio = expenses / income

    If income is zero or negative, this function returns 0.0.
    """
    if income <= 0:
        return 0.0
    return expenses / income


def calculate_debt_to_income_ratio(income: float, debt_payments: float) -> float:
    """
    Calculate the debt-to-income (DTI) ratio.

    dti = monthly_debt_payments / gross_monthly_income

    If income is zero or negative, this function returns 0.0.
    """
    if income <= 0:
        return 0.0
    return debt_payments / income


def recommend_emergency_fund(
    monthly_expenses: float,
    target_months: float,
) -> float:
    """
    Recommend the size of an emergency fund based on monthly expenses.

    emergency_fund = monthly_expenses * target_months

    Negative inputs are treated as zero.
    """
    safe_months = max(target_months, 0.0)
    safe_expenses = max(monthly_expenses, 0.0)
    return safe_expenses * safe_months


def estimate_budget_breakdown(
    income: float,
    expenses: float,
    savings: float,
) -> Dict[str, float]:
    """
    Estimate a simple budget breakdown similar to a 50/30/20 rule.

    Ratios are normalized against the larger of income or observed
    cash outflows (expenses + savings) to keep proportions stable.
    """
    total = max(income, expenses + savings, 1e-9)
    return {
        "Needs": min(expenses / total, 1.0),
        "Wants": 0.0,
        "Savings": min(savings / total, 1.0),
    }


def monthly_contribution_for_goal(
    target_amount: float,
    years: float,
    annual_return: float,
) -> float:
    """
    Compute the required monthly contribution to reach a financial goal.

    This function assumes a constant contribution every month and a constant
    annual rate of return. It uses the future value formula for an ordinary
    annuity:

        FV = P * [((1 + r/n)^(n*t) - 1) / (r/n)]

    where:
        FV = target_amount
        P  = monthly contribution (what we solve for)
        r  = annual_return
        n  = 12 (monthly compounding)
        t  = years

    If return assumptions break down (e.g. zero or negative rates), the
    function falls back to a simple linear savings rule:

        P = target_amount / (years * 12)
    """
    if target_amount <= 0 or years <= 0:
        return 0.0

    periods_per_year = 12
    r_period = annual_return / periods_per_year
    n_periods = years * periods_per_year

    if r_period <= 0:
        return target_amount / n_periods

    growth_factor = (1 + r_period) ** n_periods
    denominator = growth_factor - 1.0
    if denominator <= 0 or not isfinite(denominator):
        return target_amount / n_periods

    return target_amount * (r_period / denominator)


def goal_monthly_savings_requirement(
    target_amount: float,
    years: float,
    annual_return: float,
) -> float:
    """Alias for :func:`monthly_contribution_for_goal` for readability."""
    return monthly_contribution_for_goal(
        target_amount=target_amount,
        years=years,
        annual_return=annual_return,
    )


def build_projection_series(
    current_savings: float,
    monthly_contribution: float,
    years: float,
    annual_return: float,
) -> List[Tuple[float, float]]:
    """
    Build yearly projection points (year, projected_balance) for visualization.

    Uses compound interest with monthly contributions.
    """
    months = int(years * 12)
    r_monthly = annual_return / 12

    balance = current_savings
    points: List[Tuple[float, float]] = [(0.0, balance)]

    for m in range(1, months + 1):
        balance = balance * (1 + r_monthly) + monthly_contribution
        if m % 12 == 0:
            points.append((m / 12, balance))

    return points


__all__ = [
    "calculate_savings_rate",
    "calculate_expense_ratio",
    "calculate_debt_to_income_ratio",
    "recommend_emergency_fund",
    "estimate_budget_breakdown",
    "monthly_contribution_for_goal",
    "goal_monthly_savings_requirement",
    "build_projection_series",
]

