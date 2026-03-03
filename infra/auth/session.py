"""
Session utilities for Streamlit-based multi-user dashboards.

These helpers provide a small abstraction over `st.session_state` so the rest
of the codebase does not rely directly on Streamlit globals.
"""

from __future__ import annotations

from typing import Any, Optional

import streamlit as st


def get_current_user_id() -> Optional[str]:
    """
    Return the current user id from session state, if set.

    In a real deployment this could be mapped from an authenticated identity
    (e.g. OAuth subject) or a secure cookie.
    """
    return st.session_state.get("user_id")


def set_current_user_id(user_id: str) -> None:
    """Store the current user id in session state."""
    st.session_state["user_id"] = user_id


def get_session_value(key: str, default: Any | None = None) -> Any:
    """Generic helper to read from Streamlit session state."""
    return st.session_state.get(key, default)


def set_session_value(key: str, value: Any) -> None:
    """Generic helper to write to Streamlit session state."""
    st.session_state[key] = value


__all__ = [
    "get_current_user_id",
    "set_current_user_id",
    "get_session_value",
    "set_session_value",
]

