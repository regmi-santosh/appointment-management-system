import os
import sqlite3
from typing import Iterator


def _db_path() -> str:
    return os.environ.get("DB_PATH", os.path.join(os.getcwd(), ".data", "dev.db"))


def get_connection() -> sqlite3.Connection:
    path = _db_path()
    # ensure directory exists
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            password TEXT
        )
        """
    )
    conn.commit()

    # Ensure older databases that lack the `password` column are migrated.
    try:
        cur.execute("PRAGMA table_info(users)")
        rows = cur.fetchall()
        col_names = [r[1] if not hasattr(r, "keys") else r["name"] for r in rows]
        if "password" not in col_names:
            cur.execute("ALTER TABLE users ADD COLUMN password TEXT")
            conn.commit()
    finally:
        conn.close()


def iter_conn() -> Iterator[sqlite3.Connection]:
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
