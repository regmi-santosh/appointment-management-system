"""Domain subpackage for users.

Expose repository implementations and domain models here.
"""

from .repository import UserRepository, SQLiteUserRepository, UserRecord, get_repo

__all__ = ["UserRepository", "SQLiteUserRepository", "UserRecord", "get_repo"]
