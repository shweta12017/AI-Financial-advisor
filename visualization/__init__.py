"""
Visualization package.

Provides reusable chart builders for financial metrics, backed by Altair.
"""

from .charts import (  # noqa: F401
    budget_allocation_chart,
    dti_chart,
    goal_projection_chart,
)

__all__ = [
    "budget_allocation_chart",
    "dti_chart",
    "goal_projection_chart",
]

