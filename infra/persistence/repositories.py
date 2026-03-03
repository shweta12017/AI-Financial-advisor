"""
Repository abstractions for multi-user support.

These classes define how user profiles and financial data should be loaded
and saved, without tying the rest of the app to a specific database.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from models.financial_profile import FinancialProfile


@dataclass
class User:
    """Minimal user representation for future multi-user dashboards."""

    id: str
    display_name: str
    email: str | None = None


class UserRepository(Protocol):
    """Contract for loading and saving user records."""

    def list_users(self) -> Sequence[User]:  # pragma: no cover - interface
        ...

    def get_user(self, user_id: str) -> User | None:  # pragma: no cover - interface
        ...


class FinancialProfileRepository(Protocol):
    """Contract for persisting financial profiles per user."""

    def get_latest_profile(self, user_id: str) -> FinancialProfile | None:  # pragma: no cover - interface
        ...

    def save_profile(self, user_id: str, profile: FinancialProfile) -> None:  # pragma: no cover - interface
        ...


# Example in-memory implementations for quick experiments or tests.

class InMemoryUserRepository:
    """Simple in-memory user repository (not for production use)."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def list_users(self) -> Sequence[User]:
        return list(self._users.values())

    def get_user(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def upsert_user(self, user: User) -> None:
        self._users[user.id] = user


class InMemoryFinancialProfileRepository:
    """In-memory financial profile storage keyed by user id."""

    def __init__(self) -> None:
        self._profiles: dict[str, FinancialProfile] = {}

    def get_latest_profile(self, user_id: str) -> FinancialProfile | None:
        return self._profiles.get(user_id)

    def save_profile(self, user_id: str, profile: FinancialProfile) -> None:
        self._profiles[user_id] = profile


__all__ = [
    "User",
    "UserRepository",
    "FinancialProfileRepository",
    "InMemoryUserRepository",
    "InMemoryFinancialProfileRepository",
]

