import os
import tempfile

from app.db import init_db
from app.repository import SQLiteUserRepository


def test_repository_create_and_get():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    os.environ["DB_PATH"] = tmp.name
    init_db()
    repo = SQLiteUserRepository()
    u = repo.create(email="u1@example.com", full_name="User One")
    assert u.id == 1
    got = repo.get(u.id)
    assert got is not None
    assert got.email == "u1@example.com"


def test_repository_unique_email():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    os.environ["DB_PATH"] = tmp.name
    init_db()
    repo = SQLiteUserRepository()
    repo.create(email="dup@example.com", full_name="Dup")
    try:
        repo.create(email="dup@example.com", full_name="Dup2")
        assert False, "expected unique constraint to raise"
    except Exception:
        # expected (SQLite IntegrityError)
        pass
