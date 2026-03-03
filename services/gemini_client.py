"""
Service-layer facade for the Gemini client.

This module simply re-exports the centralized GeminiClient from the `ai`
package so existing imports continue to work without duplicating logic.
"""

from ai.gemini_client import GeminiClient

__all__ = ["GeminiClient"]
