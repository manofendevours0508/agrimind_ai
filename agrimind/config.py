import os
from pathlib import Path


def load_env_file():
    """Load simple KEY=VALUE entries from the project's .env file."""
    env_path = Path(__file__).resolve().parent.parent / ".env"

    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key:
            os.environ.setdefault(key, value)


load_env_file()


class BaseConfig:
    """Shared configuration for all environments."""

    SECRET_KEY = os.environ.get("AGRIMIND_SECRET_KEY")


class DevelopmentConfig(BaseConfig):
    """Local development settings."""

    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    """Automated testing settings."""

    DEBUG = False
    TESTING = True
    SECRET_KEY = "test-only-secret-key"


class ProductionConfig(BaseConfig):
    """Production settings."""

    DEBUG = False
    TESTING = False

    @classmethod
    def validate(cls):
        if not cls.SECRET_KEY:
            raise RuntimeError(
                "AGRIMIND_SECRET_KEY must be configured in production."
            )

        if cls.SECRET_KEY == "test-only-secret-key":
            raise RuntimeError(
                "Production cannot use the testing secret key."
            )

        if len(cls.SECRET_KEY) < 32:
            raise RuntimeError(
                "Production secret key must contain at least 32 characters."
            )
