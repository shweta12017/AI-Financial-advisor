"""
Config package.

Exports the strongly-typed application settings object so other layers can
import configuration without knowing how it is loaded.
"""

from .settings import settings

__all__ = ["settings"]

