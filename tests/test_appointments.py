import importlib
import os
import tempfile

from fastapi.testclient import TestClient


def _make_client_with_temp_db():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    os.environ["DB_PATH"] = tmp.name
    # initialize DB for the temporary path
    import app.core.db as dbmod

    dbmod.init_db()
    import app.main as appmod

    importlib.reload(appmod)
    return TestClient(appmod.app)


def test_create_and_get_appointment():
    client = _make_client_with_temp_db()

    # create a user first (owner)
    resp_user = client.post("/users/", json={"email": "owner@example.com", "full_name": "Owner", "password": "s3cr3t"})
    assert resp_user.status_code == 201
    owner_id = resp_user.json()["id"]
    # get auth token
    login = client.post("/users/login", json={"email": "owner@example.com", "password": "s3cr3t"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    payload = {
        "title": "Meeting",
        "description": "Discuss project",
        "start_time": "2026-01-01T10:00:00Z",
        "end_time": "2026-01-01T11:00:00Z",
        "owner_id": owner_id,
    }
    resp = client.post("/appointments/", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == 1
    assert data["title"] == "Meeting"

    resp2 = client.get(f"/appointments/{data['id']}")
    assert resp2.status_code == 200
    assert resp2.json()["owner_id"] == owner_id


def test_list_owner_appointments():
    client = _make_client_with_temp_db()
    resp_user = client.post("/users/", json={"email": "owner2@example.com", "full_name": "Owner2", "password": "pw2"})
    owner_id = resp_user.json()["id"]
    login = client.post("/users/login", json={"email": "owner2@example.com", "password": "pw2"})
    token = login.json()["access_token"]

    for i in range(3):
        payload = {
            "title": f"Appt {i}",
            "description": "",
            "start_time": "2026-01-02T09:00:00Z",
            "end_time": "2026-01-02T10:00:00Z",
            "owner_id": owner_id,
        }
        r = client.post("/appointments/", json=payload, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 201

    resp = client.get(f"/appointments/owner/{owner_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_update_and_delete_appointment():
    client = _make_client_with_temp_db()
    resp_user = client.post("/users/", json={"email": "owner3@example.com", "full_name": "Owner3", "password": "pw3"})
    owner_id = resp_user.json()["id"]
    login = client.post("/users/login", json={"email": "owner3@example.com", "password": "pw3"})
    token = login.json()["access_token"]

    payload = {
        "title": "Initial",
        "description": "Initial desc",
        "start_time": "2026-02-01T09:00:00Z",
        "end_time": "2026-02-01T10:00:00Z",
        "owner_id": owner_id,
    }
    r = client.post("/appointments/", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 201
    appt = r.json()

    # update title and times
    upd = {"title": "Updated", "start_time": "2026-02-01T09:30:00Z", "end_time": "2026-02-01T10:30:00Z"}
    r2 = client.put(f"/appointments/{appt['id']}", json=upd, headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    data = r2.json()
    assert data["title"] == "Updated"

    # invalid time update
    bad = {"start_time": "2026-02-01T11:00:00Z", "end_time": "2026-02-01T10:00:00Z"}
    r3 = client.put(f"/appointments/{appt['id']}", json=bad, headers={"Authorization": f"Bearer {token}"})
    assert r3.status_code == 400

    # delete
    r4 = client.delete(f"/appointments/{appt['id']}", headers={"Authorization": f"Bearer {token}"})
    assert r4.status_code == 204
    r5 = client.get(f"/appointments/{appt['id']}")
    assert r5.status_code == 404
