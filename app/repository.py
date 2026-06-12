from typing import Optional
from dataclasses import dataclass
from .db import get_connection


@dataclass
class UserRecord:
    id: int
    email: str
    full_name: str


class UserRepository:
    def create(self, email: str, full_name: str) -> UserRecord:
        raise NotImplementedError

    def get(self, user_id: int) -> Optional[UserRecord]:
        raise NotImplementedError


class SQLiteUserRepository(UserRepository):
    def __init__(self):
        # ensure DB initialized elsewhere (app startup)
        pass

    def create(self, email: str, full_name: str) -> UserRecord:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (email, full_name) VALUES (?, ?)", (email, full_name)
            )
            conn.commit()
            user_id = cur.lastrowid
            return UserRecord(id=user_id, email=email, full_name=full_name)
        finally:
            conn.close()

    def get(self, user_id: int) -> Optional[UserRecord]:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, email, full_name FROM users WHERE id = ?", (user_id,))
            row = cur.fetchone()
            if not row:
                return None
            return UserRecord(id=row[0], email=row[1], full_name=row[2])
        finally:
            conn.close()


def get_repo() -> SQLiteUserRepository:
    # return a fresh repository instance; callers (FastAPI) can manage lifetime
    return SQLiteUserRepository()
