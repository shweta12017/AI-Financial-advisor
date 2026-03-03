"""
Service-layer facade for investment simulation.

Re-exports the domain implementation so existing imports continue to work
while keeping the core logic in the domain layer.
"""

from domain.investment_simulator import (
    Allocation,
    RISK_ALLOCATIONS,
    simulate_portfolio_path,
)

__all__ = ["Allocation", "RISK_ALLOCATIONS", "simulate_portfolio_path"]

