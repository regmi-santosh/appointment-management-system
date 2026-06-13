import os
from typing import Any, Dict


def get_settings() -> Dict[str, Any]:
    """Return minimal runtime settings from environment variables.

    This keeps configuration centralized; expand as needed.
    """
    return {
        "APP_SECRET": os.environ.get("APP_SECRET", "dev-secret"),
        "DB_PATH": os.environ.get("DB_PATH", os.path.join(os.getcwd(), ".data", "dev.db")),
    }
