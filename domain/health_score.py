from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from models.financial_profile import FinancialProfile
from domain.financial_engine import recommend_emergency_fund


@dataclass
class HealthScore:
    """Composite financial health score and its components."""

    score: int
    grade: str
    components: Dict[str, int]


def _grade(score: int) -> str:
    """Map a numeric score to a simple letter grade."""
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 55:
        return "C"
    if score >= 40:
        return "D"
    return "E"


def compute_health_score(
    profile: FinancialProfile,
    target_emergency_months: float = 6.0,
) -> HealthScore:
    """
    Aggregate several metrics into a single financial health score (0–100).

    Components:
      - Savings rate: higher is better (up to ~30%)    -> max 40 points
      - DTI: lower is better (below 36% preferred)     -> max 30 points
      - Emergency fund: coverage of target months      -> max 30 points
    """
    # Savings rate (0–40 points)
    sr = profile.savings_rate or 0.0
    sr_target = 0.30
    sr_score = int(min(sr / sr_target, 1.0) * 40)

    # DTI (0–30 points)
    dti = profile.debt_to_income_ratio or 0.0
    if dti <= 0.36:
        dti_score = 30
    elif dti <= 0.45:
        dti_score = 20
    elif dti <= 0.6:
        dti_score = 10
    else:
        dti_score = 0

    # Emergency fund (0–30 points)
    target_fund = recommend_emergency_fund(
        profile.monthly_expenses,
        target_emergency_months,
    )
    coverage = (
        (profile.monthly_savings * target_emergency_months) / target_fund
        if target_fund > 0
        else 0
    )
    ef_score = int(min(max(coverage, 0.0), 1.0) * 30)

    total = sr_score + dti_score + ef_score
    components = {
        "savings_rate": sr_score,
        "dti": dti_score,
        "emergency_fund": ef_score,
    }
    return HealthScore(score=total, grade=_grade(total), components=components)


__all__ = ["HealthScore", "compute_health_score"]

