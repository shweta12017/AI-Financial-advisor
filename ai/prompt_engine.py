"""
Prompt engine for financial advice.

This module owns reusable prompt templates and structured prompt
construction for the Gemini 2.0 Flash model.
"""

from __future__ import annotations

from textwrap import dedent
from typing import Optional

from models.financial_profile import FinancialProfile
from ai.gemini_client import GeminiClient


BASE_SYSTEM_PROMPT = """
You are an experienced, conservative financial planner acting as a
fiduciary. You provide realistic, implementable guidance that prioritizes
the user's long‑term financial safety over aggressive returns.

You must NOT give tax, legal, or jurisdiction‑specific advice and you
must NOT guarantee any investment outcomes.
"""


OUTPUT_FORMAT_INSTRUCTIONS = """
STRUCTURE YOUR RESPONSE IN MARKDOWN USING THESE SECTIONS
(even if some sections are short):

## Overview
- 2–3 sentence plain‑language summary of the user's overall situation.

## Key Metrics
- Bullet list or table summarizing: savings rate, expense ratio,
  debt‑to‑income (DTI), free cash flow, and any notable budget imbalance.

## Budget Optimization
- 3–5 specific recommendations to improve cash flow and savings.
- Each item should follow this mini‑format:
  - **Action** – what to change
  - **Why** – the benefit or risk reduced
  - **When** – suggested timeframe (e.g. next month, 3–6 months).

## Risk‑Aware Investment Strategy
- Describe an investment approach consistent with the user's
  risk tolerance (Low / Medium / High) and debt level.
- Discuss approximate allocations (cash / safety assets / growth assets)
  in ranges (e.g. 10–20%, 40–60%) without naming specific securities.
- Emphasize diversification, emergency fund priority, and paying down
  high‑interest debt before aggressive investing.

## Goal‑Based Plan
- If a goal is provided, explain:
  - Whether the goal looks realistic given income, savings, and horizon.
  - How monthly savings might be split between emergency fund, debt
    reduction, and goal investing.
  - A simple timeline (e.g. Years 0–2, 2–5, 5+).
- If no goal is specified, propose 1–2 sensible medium‑term goals.

## Actionable Checklist
- 5–10 numbered, concise steps the user can take.
- Each step should be clearly actionable, realistic, and ordered by
  priority (most urgent / impactful first).
"""


def _profile_context_block(profile: FinancialProfile) -> str:
    """Build the user/metrics context block for the prompt."""
    data = profile.as_dict_for_llm()
    return f"""
USER SNAPSHOT (all values monthly unless noted)
- Income: {data["monthly_income"]:.2f}
- Expenses: {data["monthly_expenses"]:.2f}
- Savings: {data["monthly_savings"]:.2f}
- Debt payments: {data["monthly_debt_payments"]:.2f}

DERIVED METRICS
- Savings rate: {data["savings_rate"]:.2%}
- Expense ratio (expenses/income): {data["expense_ratio"]:.2%}
- Debt-to-income ratio: {data["debt_to_income_ratio"]:.2%}
- Free cash flow (income - expenses - debt): {data["free_cash_flow"]:.2f}
- Budget breakdown (approx): {data["budget_breakdown"]}

GOAL INFORMATION
- Goal name: {data["goal_name"]}
- Goal target amount: {data["goal_target_amount"]}
- Goal time horizon (years): {data["goal_time_horizon_years"]}
- Risk tolerance: {data["risk_tolerance"]}
"""


def build_structured_advice_prompt(profile: FinancialProfile) -> str:
    """
    Build a structured prompt that drives Gemini to produce:
    - More structured output with clear sections
    - Actionable, prioritized recommendations
    - Risk-aware investment suggestions
    - Budget optimization guidance
    - Goal-based planning explanation
    """
    context = _profile_context_block(profile)

    prompt = f"""
{BASE_SYSTEM_PROMPT}

USER DATA
{context}

YOUR TASK
- Analyze the user's situation holistically.
- Be conservative and emphasize downside protection.
- Avoid shaming; be encouraging but realistic.

{OUTPUT_FORMAT_INSTRUCTIONS}

CONSTRAINTS
- Keep total length around 700 words or less.
- Use only information that could reasonably be inferred from the data;
  if you must assume something, state it explicitly as an assumption.
"""
    return dedent(prompt).strip()


def generate_financial_advice(
    profile: FinancialProfile,
    client: Optional[GeminiClient] = None,
) -> str:
    """
    Generate AI-powered financial advice for the given profile using the
    structured prompt templates defined in this module.

    Callers should depend on this function rather than the underlying
    Gemini client so that prompt strategies and model settings can evolve
    without affecting the rest of the codebase.
    """
    if client is None:
        client = GeminiClient()

    prompt = build_structured_advice_prompt(profile)
    return client.generate_financial_advice(prompt)


__all__ = ["build_structured_advice_prompt", "generate_financial_advice"]

