"""
Service-layer facade for computing the financial health score.

Re-exports the domain implementation so existing imports continue to work
while keeping the core logic in the domain layer.
"""

from domain.health_score import HealthScore, compute_health_score

__all__ = ["HealthScore", "compute_health_score"]

