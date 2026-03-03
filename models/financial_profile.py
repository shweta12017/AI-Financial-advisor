from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class FinancialProfile:
    """Represents a user's high-level financial situation and goals."""

    # Raw user inputs (monthly)
    monthly_income: float
    monthly_expenses: float
    monthly_savings: float
    monthly_debt_payments: float

    # Goal info (optional)
    goal_name: Optional[str] = None
    goal_target_amount: Optional[float] = None
    goal_time_horizon_years: Optional[float] = None
    risk_tolerance: Optional[str] = None  # e.g. "Low", "Medium", "High"

    # Derived metrics (populated after calculations)
    savings_rate: Optional[float] = None
    expense_ratio: Optional[float] = None
    debt_to_income_ratio: Optional[float] = None
    free_cash_flow: Optional[float] = None

    budget_breakdown: Optional[Dict[str, float]] = None

    def as_dict_for_llm(self) -> Dict:
        """Return a JSON-safe dict representation for passing into Gemini prompts."""
        return {
            "monthly_income": self.monthly_income,
            "monthly_expenses": self.monthly_expenses,
            "monthly_savings": self.monthly_savings,
            "monthly_debt_payments": self.monthly_debt_payments,
            "goal_name": self.goal_name,
            "goal_target_amount": self.goal_target_amount,
            "goal_time_horizon_years": self.goal_time_horizon_years,
            "risk_tolerance": self.risk_tolerance,
            "savings_rate": self.savings_rate,
            "expense_ratio": self.expense_ratio,
            "debt_to_income_ratio": self.debt_to_income_ratio,
            "free_cash_flow": self.free_cash_flow,
            "budget_breakdown": self.budget_breakdown,
        }

