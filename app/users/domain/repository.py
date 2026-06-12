from typing import Optional
from dataclasses import dataclass
import sqlite3
from app.db import get_connection
from .errors import UserAlreadyExists, RepositoryError


@dataclass
class UserRecord:
    id: int
    email: str
    full_name: str
    password: Optional[str] = None


class UserRepository:
    def create(self, email: str, full_name: str, password: Optional[str] = None) -> UserRecord:
        raise NotImplementedError

    def get(self, user_id: int) -> Optional[UserRecord]:
        raise NotImplementedError

    def get_by_email(self, email: str) -> Optional[UserRecord]:
        raise NotImplementedError


class SQLiteUserRepository(UserRepository):
    def __init__(self):
        # ensure DB initialized elsewhere (app startup)
        pass

    def create(self, email: str, full_name: str, password: Optional[str] = None) -> UserRecord:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (email, full_name, password) VALUES (?, ?, ?)",
                (email, full_name, password),
            )
            conn.commit()
            user_id = cur.lastrowid
            return UserRecord(id=user_id, email=email, full_name=full_name, password=password)
        except sqlite3.IntegrityError as e:
            # Unique constraint on email
            raise UserAlreadyExists("email already exists")
        except Exception as e:
            raise RepositoryError(str(e))
        finally:
            conn.close()

    def get(self, user_id: int) -> Optional[UserRecord]:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, email, full_name, password FROM users WHERE id = ?", (user_id,))
            row = cur.fetchone()
            if not row:
                return None
            return UserRecord(id=row[0], email=row[1], full_name=row[2], password=row[3])
        finally:
            conn.close()

    def get_by_email(self, email: str) -> Optional[UserRecord]:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, email, full_name, password FROM users WHERE email = ?", (email,))
            row = cur.fetchone()
            if not row:
                return None
            return UserRecord(id=row[0], email=row[1], full_name=row[2], password=row[3])
        finally:
            conn.close()


def get_repo() -> SQLiteUserRepository:
    # return a fresh repository instance; callers (FastAPI) can manage lifetime
    return SQLiteUserRepository()
