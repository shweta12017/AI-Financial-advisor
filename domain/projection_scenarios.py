from __future__ import annotations

from typing import Dict, List

import pandas as pd

from domain.financial_engine import build_projection_series


def build_savings_scenarios(
    current_savings: float,
    base_monthly_savings: float,
    years: float,
    annual_return: float,
) -> pd.DataFrame:
    """
    Build multiple savings projection paths for comparison.

    Scenarios:
      - Baseline
      - Increase savings by 10%
      - Increase savings by 20%
    """
    scenarios: Dict[str, float] = {
        "Baseline": base_monthly_savings,
        "+10% savings": base_monthly_savings * 1.10,
        "+20% savings": base_monthly_savings * 1.20,
    }

    rows: List[Dict] = []
    for name, monthly in scenarios.items():
        points = build_projection_series(
            current_savings=current_savings,
            monthly_contribution=monthly,
            years=years,
            annual_return=annual_return,
        )
        for year, balance in points:
            rows.append({"Year": year, "Balance": balance, "Scenario": name})

    return pd.DataFrame(rows)


__all__ = ["build_savings_scenarios"]

