from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from domain.risk_profile import RiskLevel


@dataclass(frozen=True)
class Allocation:
    """Portfolio allocation as fractions that sum to 1.0."""

    equity: float
    bonds: float
    cash: float


RISK_ALLOCATIONS: Dict[RiskLevel, Allocation] = {
    RiskLevel.LOW: Allocation(equity=0.3, bonds=0.5, cash=0.2),
    RiskLevel.MEDIUM: Allocation(equity=0.6, bonds=0.3, cash=0.1),
    RiskLevel.HIGH: Allocation(equity=0.8, bonds=0.15, cash=0.05),
}

EXPECTED_ANNUAL_RETURNS: Dict[str, float] = {
    "equity": 0.07,
    "bonds": 0.03,
    "cash": 0.01,
}


def _allocation_expected_return(allocation: Allocation) -> float:
    """Weighted annual return based on asset class expectations."""
    return (
        allocation.equity * EXPECTED_ANNUAL_RETURNS["equity"]
        + allocation.bonds * EXPECTED_ANNUAL_RETURNS["bonds"]
        + allocation.cash * EXPECTED_ANNUAL_RETURNS["cash"]
    )


def simulate_portfolio_path(
    years: float,
    initial_balance: float,
    monthly_contribution: float,
    risk_level: RiskLevel,
) -> List[Tuple[float, float]]:
    """
    Deterministic portfolio growth projection for a given risk level.

    Uses a single expected annual return derived from the chosen allocation.
    Returns yearly (year, balance) points for easy charting.
    """
    allocation = RISK_ALLOCATIONS[risk_level]
    r_annual = _allocation_expected_return(allocation)
    r_monthly = r_annual / 12
    months = int(years * 12)

    balance = initial_balance
    points: List[Tuple[float, float]] = [(0.0, balance)]

    for m in range(1, months + 1):
        balance = balance * (1 + r_monthly) + monthly_contribution
        if m % 12 == 0:
            points.append((m / 12, balance))

    return points


__all__ = ["Allocation", "RISK_ALLOCATIONS", "simulate_portfolio_path"]

