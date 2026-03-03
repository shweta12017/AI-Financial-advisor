"""
Service-layer facade for predictive savings scenarios.

Re-exports the domain implementation so existing imports continue to work
while keeping the core logic in the domain layer.
"""

from domain.projection_scenarios import build_savings_scenarios

__all__ = ["build_savings_scenarios"]

