from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_create_and_get_user():
    resp = client.post("/users/", json={"email": "alice@example.com", "full_name": "Alice"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == 1
    assert data["email"] == "alice@example.com"

    resp2 = client.get(f"/users/{data['id']}")
    assert resp2.status_code == 200
    assert resp2.json()["email"] == "alice@example.com"


def test_duplicate_email_rejected():
    client.post("/users/", json={"email": "bob@example.com", "full_name": "Bob"})
    resp = client.post("/users/", json={"email": "bob@example.com", "full_name": "Bobby"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "email already exists"
