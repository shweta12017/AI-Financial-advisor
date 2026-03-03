"""
Domain models for the AI Financial Advisor.

This package currently re-exports the `FinancialProfile` from the existing
`models` package to provide a stable import path for domain code.
"""

from models.financial_profile import FinancialProfile

__all__ = ["FinancialProfile"]

