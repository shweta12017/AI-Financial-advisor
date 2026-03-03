"""
Service-layer facade around the domain financial engine.

This module keeps the existing public API but delegates all pure
calculations to :mod:`domain.financial_engine`, injecting configuration
defaults (like expected returns) where appropriate.
"""

from __future__ import annotations

from typing import Dict, List, Tuple, Optional

from config.settings import settings
from domain import financial_engine as _core
from models.financial_profile import FinancialProfile


# Re-export core pure functions for backwards compatibility.
calculate_savings_rate = _core.calculate_savings_rate
calculate_expense_ratio = _core.calculate_expense_ratio
calculate_debt_to_income_ratio = _core.calculate_debt_to_income_ratio
recommend_emergency_fund = _core.recommend_emergency_fund
estimate_budget_breakdown = _core.estimate_budget_breakdown


def monthly_contribution_for_goal(
    target_amount: float,
    years: float,
    annual_return: Optional[float] = None,
) -> float:
    """
    Compute the required monthly contribution to reach a financial goal.

    If ``annual_return`` is omitted, the app-wide default from settings is
    used, preserving previous behavior while keeping the core logic in the
    domain layer.
    """
    effective_return = (
        annual_return
        if annual_return is not None
        else settings.default_expected_return_annual
    )
    return _core.monthly_contribution_for_goal(
        target_amount=target_amount,
        years=years,
        annual_return=effective_return,
    )


def goal_monthly_savings_requirement(
    target_amount: float,
    years: float,
    annual_return: Optional[float] = None,
) -> float:
    """
    Convenience wrapper for computing the goal monthly savings requirement.
    """
    effective_return = (
        annual_return
        if annual_return is not None
        else settings.default_expected_return_annual
    )
    return _core.goal_monthly_savings_requirement(
        target_amount=target_amount,
        years=years,
        annual_return=effective_return,
    )


def build_projection_series(
    current_savings: float,
    monthly_contribution: float,
    years: float,
    annual_return: Optional[float] = None,
) -> List[Tuple[float, float]]:
    """
    Build yearly projection points (year, projected_balance) for visualization.

    Delegates to the domain engine while injecting a default expected return
    when one is not provided.
    """
    effective_return = (
        annual_return
        if annual_return is not None
        else settings.default_expected_return_annual
    )
    return _core.build_projection_series(
        current_savings=current_savings,
        monthly_contribution=monthly_contribution,
        years=years,
        annual_return=effective_return,
    )


def populate_derived_metrics(profile: FinancialProfile) -> FinancialProfile:
    """
    Fill derived metric fields on the profile instance in-place and return it.
    """
    income = profile.monthly_income
    profile.savings_rate = calculate_savings_rate(income, profile.monthly_savings)
    profile.expense_ratio = calculate_expense_ratio(income, profile.monthly_expenses)
    profile.debt_to_income_ratio = calculate_debt_to_income_ratio(
        income, profile.monthly_debt_payments
    )
    profile.free_cash_flow = (
        income - profile.monthly_expenses - profile.monthly_debt_payments
    )
    profile.budget_breakdown = estimate_budget_breakdown(
        income, profile.monthly_expenses, profile.monthly_savings
    )
    return profile


__all__ = [
    "calculate_savings_rate",
    "calculate_expense_ratio",
    "calculate_debt_to_income_ratio",
    "recommend_emergency_fund",
    "estimate_budget_breakdown",
    "monthly_contribution_for_goal",
    "goal_monthly_savings_requirement",
    "build_projection_series",
    "populate_derived_metrics",
]

from math import isfinite
from typing import Dict, List, Tuple, Optional

from config.settings import settings
from models.financial_profile import FinancialProfile


def calculate_savings_rate(income: float, savings: float) -> float:
    """
    Calculate the savings rate for a given income and savings amount.

    Savings rate is defined as:

        savings_rate = savings / income

    If income is zero or negative, this function returns 0.0 to avoid
    division-by-zero and negative ratios.
    """
    if income <= 0:
        return 0.0
    return savings / income


def calculate_expense_ratio(income: float, expenses: float) -> float:
    """
    Calculate the expense ratio for a given income and expense amount.

    Expense ratio is defined as:

        expense_ratio = expenses / income

    If income is zero or negative, this function returns 0.0.
    """
    if income <= 0:
        return 0.0
    return expenses / income


def calculate_debt_to_income_ratio(income: float, debt_payments: float) -> float:
    """
    Calculate the debt-to-income (DTI) ratio for a given income and debt payments.

    DTI is defined as:

        dti = monthly_debt_payments / gross_monthly_income

    If income is zero or negative, this function returns 0.0.
    """
    if income <= 0:
        return 0.0
    return debt_payments / income


def recommend_emergency_fund(
    monthly_expenses: float,
    target_months: float = 3.0,
) -> float:
    """
    Recommend the size of an emergency fund based on monthly expenses.

    By default this uses a simple rule-of-thumb:

        emergency_fund = monthly_expenses * target_months

    Where ``target_months`` is the desired number of months of core expenses
    to keep in highly liquid, low-risk accounts (e.g., 3–6 months).

    Parameters
    ----------
    monthly_expenses:
        Average monthly non-discretionary expenses to be covered.
    target_months:
        Number of months of expenses to hold in the emergency fund. Values
        less than or equal to zero are treated as 0.

    Returns
    -------
    float
        Recommended emergency fund size. Never negative.
    """
    safe_months = max(target_months, 0.0)
    safe_expenses = max(monthly_expenses, 0.0)
    return safe_expenses * safe_months


def estimate_budget_breakdown(
    income: float, expenses: float, savings: float
) -> Dict[str, float]:
    """
    Estimate a simple budget breakdown similar to a 50/30/20 rule.

    The model knows only income, expenses, and savings, so "Wants" is left
    for the AI layer to interpret. Ratios are normalized against the larger
    of income or observed cash outflows to keep proportions stable.
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
    annual_return: Optional[float] = None,
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

    r_annual = annual_return if annual_return is not None else settings.default_expected_return_annual
    periods_per_year = 12
    r_period = r_annual / periods_per_year
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
    annual_return: Optional[float] = None,
) -> float:
    """
    Convenience wrapper for computing the goal monthly savings requirement.

    This is a readability-focused alias for :func:`monthly_contribution_for_goal`
    so that application code can express the intent more clearly while sharing
    the same underlying implementation.

    Parameters
    ----------
    target_amount:
        Total amount you want to accumulate by the end of the period.
    years:
        Number of years available to reach the goal.
    annual_return:
        Expected annual rate of return (e.g. 0.06 for 6%). If omitted, the
        application default from settings is used.

    Returns
    -------
    float
        Required monthly savings amount to reach ``target_amount`` under the
        given assumptions.
    """
    return monthly_contribution_for_goal(
        target_amount=target_amount,
        years=years,
        annual_return=annual_return,
    )


def build_projection_series(
    current_savings: float,
    monthly_contribution: float,
    years: float,
    annual_return: Optional[float] = None,
) -> List[Tuple[float, float]]:
    """
    Build yearly projection points (year, projected_balance) for visualization
    using compound interest and monthly contributions.
    """
    r_annual = annual_return if annual_return is not None else settings.default_expected_return_annual
    months = int(years * 12)
    r_monthly = r_annual / 12

    balance = current_savings
    points: List[Tuple[float, float]] = [(0.0, balance)]

    for m in range(1, months + 1):
        balance = balance * (1 + r_monthly) + monthly_contribution
        if m % 12 == 0:
            year = m / 12
            points.append((year, balance))

    return points


def populate_derived_metrics(profile: FinancialProfile) -> FinancialProfile:
    """Fill derived metric fields on the profile instance in-place and return it."""
    income = profile.monthly_income
    profile.savings_rate = calculate_savings_rate(income, profile.monthly_savings)
    profile.expense_ratio = calculate_expense_ratio(income, profile.monthly_expenses)
    profile.debt_to_income_ratio = calculate_debt_to_income_ratio(
        income, profile.monthly_debt_payments
    )
    profile.free_cash_flow = (
        income - profile.monthly_expenses - profile.monthly_debt_payments
    )
    profile.budget_breakdown = estimate_budget_breakdown(
        income, profile.monthly_expenses, profile.monthly_savings
    )
    return profile

