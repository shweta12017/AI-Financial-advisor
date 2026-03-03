from __future__ import annotations

from textwrap import dedent
from typing import List, Literal, TypedDict

from models.financial_profile import FinancialProfile
from services.gemini_client import GeminiClient


Role = Literal["user", "assistant"]


class ChatMessage(TypedDict):
    """Simple chat message representation."""

    role: Role
    content: str


def build_chat_prompt(profile: FinancialProfile, messages: List[ChatMessage]) -> str:
    """Inject financial context and recent chat into a single prompt."""
    data = profile.as_dict_for_llm()
    history_str = "\n".join(f"{m['role']}: {m['content']}" for m in messages[-8:])

    prompt = f"""
    You are an AI financial assistant. Be clear, conservative, and educational.
    Do not provide tax or legal advice.

    User snapshot (monthly):
    - Income: {data["monthly_income"]:.2f}
    - Expenses: {data["monthly_expenses"]:.2f}
    - Savings: {data["monthly_savings"]:.2f}
    - Debt payments: {data["monthly_debt_payments"]:.2f}
    - Savings rate: {data["savings_rate"]:.2%}
    - Debt-to-income: {data["debt_to_income_ratio"]:.2%}
    - Risk tolerance: {data["risk_tolerance"]}

    Conversation so far:
    {history_str}

    Respond to the user's latest question only.
    Use short paragraphs and bullet points when helpful.
    """
    return dedent(prompt).strip()


def chat_reply(
    profile: FinancialProfile,
    history: List[ChatMessage],
    client: GeminiClient | None = None,
) -> str:
    """
    Generate a chatbot response given the financial profile and message history.
    """
    if client is None:
        client = GeminiClient()
    prompt = build_chat_prompt(profile, history)
    return client.generate_financial_advice(prompt)


__all__ = ["ChatMessage", "chat_reply"]

