"""
Application-wide logging configuration.

Configure Python's logging module once here, then import and call
`configure_logging()` from your entrypoint (e.g. `app.py`) so that all
modules share the same formatting and log level.
"""

from __future__ import annotations

import logging
from typing import Optional


def configure_logging(level: int = logging.INFO, logger_name: Optional[str] = None) -> logging.Logger:
    """
    Configure a root or named logger with a simple, production-friendly format.

    Call this early in your app startup so logs from all modules are consistent.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


__all__ = ["configure_logging"]

