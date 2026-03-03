import os
from dataclasses import dataclass

from dotenv import load_dotenv


# Environment variable names (centralized to avoid typos).
GEMINI_API_KEY_ENV = "GEMINI_API_KEY"
GEMINI_MODEL_ENV = "GEMINI_MODEL"


# Load .env if present (local development convenience). In production
# you normally rely on the hosting platform's environment variables.
load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Application configuration loaded from environment variables."""

    gemini_api_key: str
    gemini_model: str = "gemini-2.0-flash"
    default_expected_return_annual: float = 0.06  # 6% annual return assumption
    default_inflation_annual: float = 0.02  # 2% inflation assumption
    max_years_projection: int = 40

    @staticmethod
    def from_env() -> "Settings":
        """
        Construct settings from environment variables and basic validation.

        Secrets are never logged or printed; only the presence of required
        variables is validated.
        """
        raw_api_key = os.getenv(GEMINI_API_KEY_ENV, "")
        api_key = raw_api_key.strip()
        if not api_key:
            # Do not include the actual key value in this message.
            raise RuntimeError(
                "Gemini API key is not configured. "
                f"Set the '{GEMINI_API_KEY_ENV}' environment variable "
                "via your deployment platform or in a local .env file. "
                "Never hard-code API keys in source code."
            )

        raw_model = os.getenv(GEMINI_MODEL_ENV, "").strip()
        model = raw_model or "gemini-2.0-flash"

        return Settings(
            gemini_api_key=api_key,
            gemini_model=model,
        )


settings = Settings.from_env()

