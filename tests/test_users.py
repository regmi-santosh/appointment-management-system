import os
import tempfile
import importlib

from fastapi.testclient import TestClient


def _make_client_with_temp_db():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    os.environ["DB_PATH"] = tmp.name
    # reload app module so startup uses the new DB_PATH
    # ensure DB is initialized for the temp path
    import app.db as dbmod

    dbmod.init_db()
    import app.main as appmod

    importlib.reload(appmod)
    return TestClient(appmod.app)


def test_create_and_get_user():
    client = _make_client_with_temp_db()
    resp = client.post("/users/", json={"email": "alice@example.com", "full_name": "Alice"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == 1
    assert data["email"] == "alice@example.com"

    resp2 = client.get(f"/users/{data['id']}")
    assert resp2.status_code == 200
    assert resp2.json()["email"] == "alice@example.com"


def test_duplicate_email_rejected():
    client = _make_client_with_temp_db()
    client.post("/users/", json={"email": "bob@example.com", "full_name": "Bob"})
    resp = client.post("/users/", json={"email": "bob@example.com", "full_name": "Bobby"})
    assert resp.status_code == 409
    assert resp.json()["detail"] == "email already exists"
