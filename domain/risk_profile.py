from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class RiskLevel(str, Enum):
    """Discrete risk buckets used across the app."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class RiskProfile:
    """Represents a user's risk profile based on questionnaire answers."""

    score: int  # 0–100 composite score
    level: RiskLevel
    reasoning: str


def _map_score_to_level(score: int) -> RiskLevel:
    """Map a numeric score into a RiskLevel."""
    if score < 35:
        return RiskLevel.LOW
    if score < 70:
        return RiskLevel.MEDIUM
    return RiskLevel.HIGH


def compute_risk_profile(answers: Dict[str, int]) -> RiskProfile:
    """
    Compute a risk profile from questionnaire answers.

    Parameters
    ----------
    answers:
        Mapping of question_id -> answer value (1–5). Values are clamped
        into [1, 5] to tolerate bad inputs.
    """
    if not answers:
        return RiskProfile(
            score=50,
            level=RiskLevel.MEDIUM,
            reasoning="No answers provided; defaulting to medium risk.",
        )

    normalized: List[int] = []
    for value in answers.values():
        try:
            v = int(value)
        except (TypeError, ValueError):
            v = 3
        normalized.append(min(max(v, 1), 5))

    avg = sum(normalized) / len(normalized)
    score = int(round((avg - 1) / 4 * 100))  # 1–5 -> 0–100
    level = _map_score_to_level(score)

    if level == RiskLevel.LOW:
        reasoning = "Prefers capital preservation and lower volatility."
    elif level == RiskLevel.HIGH:
        reasoning = "Comfortable with higher volatility for potentially higher returns."
    else:
        reasoning = "Balanced tolerance for risk and return."

    return RiskProfile(score=score, level=level, reasoning=reasoning)


__all__ = ["RiskLevel", "RiskProfile", "compute_risk_profile"]

