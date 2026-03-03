"""
Centralized Gemini 2.0 Flash client.

This module owns the concrete GeminiClient implementation so that all
call sites across the application share the same configuration and
error-handling behavior.
"""

from typing import Any

import google.generativeai as genai

from config.settings import settings


# Configure the Gemini SDK once at import time.
genai.configure(api_key=settings.gemini_api_key)


class GeminiClient:
    """Thin wrapper around the Gemini model for financial advice and chat."""

    def __init__(self, model_name: str | None = None) -> None:
        self._model_name = model_name or settings.gemini_model
        self._model = genai.GenerativeModel(self._model_name)

    def generate_text(self, prompt: str) -> str:
        """
        Generate a text completion for the given prompt.

        This is the generic entrypoint. Domain-specific helpers can wrap
        this to provide more structured behavior.
        """
        try:
            response: Any = self._model.generate_content(prompt)
        except Exception as exc:  # Network / quota / config issues
            return (
                "Unable to contact AI advisor right now. "
                f"Technical details: {exc}"
            )

        # Preferred path for recent SDK versions.
        if hasattr(response, "text") and response.text:
            return response.text

        # Defensive fallback if SDK returns candidates/parts instead of .text.
        try:
            candidates = getattr(response, "candidates", [])
            if not candidates:
                return "AI did not return any advice. Please try again."
            parts = candidates[0].content.parts
            text_chunks = [
                getattr(part, "text", "") for part in parts if hasattr(part, "text")
            ]
            joined = "".join(text_chunks).strip()
            return joined or "AI returned an empty response. Please try again."
        except Exception:
            return "Unexpected AI response format. Please try again later."

    # Backwards-compatible method name used elsewhere in the app.
    def generate_financial_advice(self, prompt: str) -> str:
        """Alias kept for backwards compatibility with existing call sites."""
        return self.generate_text(prompt)


__all__ = ["GeminiClient"]

