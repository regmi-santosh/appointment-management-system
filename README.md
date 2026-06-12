# Appointment Management System (scaffold)

Minimal FastAPI project scaffold with BDD test structure (pytest-bdd).

Setup (macOS / Linux):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run dev server:

```bash
uvicorn app.main:app --reload
```

Run tests (Behave BDD):

```bash
behave -q
```

Project layout:

- app/: FastAPI application
- tests/: pytest + pytest-bdd tests
- requirements.txt: dependencies

API docs
--------

When the server is running locally the OpenAPI/Swagger UI and Redoc are available at:

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

Quick example (create a user):

```bash
curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{"email":"alice@example.com","full_name":"Alice"}'
```

Notes
-----

- The canonical versioned API is mounted at `/api/v1/users`.
- This repository focuses on the backend; BDD tests are maintained in a separate project.
