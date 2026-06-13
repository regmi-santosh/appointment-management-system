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
- toolkit/: development helpers, skills and agent templates

Final architecture (summary)
----------------------------
The project follows a small, domain-driven layout:

- `app/main.py` — FastAPI application and router mounting
- `app/core/` — core utilities used across domains (DB, auth, config)
- `app/api/v1/` — versioned API routers (e.g., `users.py`)
- `app/users/` — domain package for users: `repository.py`, `service.py`, `schemas.py`, `errors.py`
- `tests/` — unit and integration tests

When adding new domains (e.g., `appointments`) follow the same pattern under `app/`:

```
app/
	api/
		v1/
			users.py
			appointments.py  # new router
	core/
		db.py
		auth.py
		config.py
	users/
		repository.py
		service.py
		schemas.py
		errors.py
	appointments/      # new domain
		repository.py
		service.py
		schemas.py
		errors.py
```

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

Authentication / Login
----------------------

This project includes a simple login flow using hashed passwords and JWT access tokens.

- Create a user with an optional password:

```bash
curl -X POST "http://127.0.0.1:8000/users/" \
	-H "Content-Type: application/json" \
	-d '{"email":"carol@example.com","full_name":"Carol","password":"s3cr3t"}'
```

- Obtain an access token (login):

```bash
curl -X POST "http://127.0.0.1:8000/users/login" \
	-H "Content-Type: application/json" \
	-d '{"email":"carol@example.com","password":"s3cr3t"}'
```

The response contains an `access_token` and `token_type` (bearer). The token is signed with the `APP_SECRET` environment variable; in development the code falls back to a default secret. For production, set `APP_SECRET` to a strong, random value (>=32 bytes recommended).

Notes & recommendations
-----------------------
- Passwords are hashed using `passlib` (`pbkdf2_sha256` by default in this repo).
- Tokens use `PyJWT` (HS256). Consider rotating secrets and using RS256 for larger deployments.
- If you are upgrading an existing database, the application will add a `password` column automatically on startup when needed.

Developer notes
---------------
- Tests: run `pytest -q` to execute the test-suite used by CI.
- Env: set `DB_PATH` to change the SQLite file and `APP_SECRET` to a production secret.
- Adding modules: add domain modules under `app/` and register routers under `app/api/v1`.


Notes
-----

- The canonical versioned API is mounted at `/api/v1/users`.
- This repository focuses on the backend; BDD tests are maintained in a separate project.
