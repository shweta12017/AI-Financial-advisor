"""
Legacy facade for financial advice generation.

The core prompt engineering now lives in :mod:`ai.prompt_engine`. This
module simply re-exports the high-level function so existing imports
continue to work.
"""

from models.financial_profile import FinancialProfile
from ai.prompt_engine import generate_financial_advice


def generate_advice(profile: FinancialProfile) -> str:
    """Backward-compatible wrapper around `ai.prompt_engine.generate_financial_advice`."""
    return generate_financial_advice(profile)


__all__ = ["generate_advice"]

