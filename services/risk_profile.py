"""
Service-layer facade for risk profiling.

Re-exports the domain implementation so existing imports continue to work
while keeping the core logic in the domain layer.
"""

from domain.risk_profile import RiskLevel, RiskProfile, compute_risk_profile

__all__ = ["RiskLevel", "RiskProfile", "compute_risk_profile"]

