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

**Contribution**

- **Docs**: See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute and open PRs.
- **Style**: Follow the guidelines in [CODE_STYLE.md](CODE_STYLE.md).

**Coding Standards**

- **Formatters & linters**: This project uses Black, isort, flake8 and mypy. Pre-commit hooks are configured in [.pre-commit-config.yaml](.pre-commit-config.yaml).
- **Dev deps**: Install development tooling from [requirements-dev.txt](requirements-dev.txt).

**Toolkit & Governance**

- The repository includes a lightweight governance toolkit under [toolkit/](toolkit/). Key artifacts:
	- Agent descriptions: [toolkit/agents/](toolkit/agents/)
	- Skills, policies, rules: [toolkit/skills/](toolkit/skills/), [toolkit/policies/](toolkit/policies/), [toolkit/rules/](toolkit/rules/)
	- Runners: [toolkit/runners/](toolkit/runners/)
	- Orchestrator: [toolkit/runtime.py](toolkit/runtime.py)
	- Reports: [toolkit/reports/](toolkit/reports/)

**Run governance checks (local)**

1. Activate the project virtualenv:

```bash
. .venv/bin/activate
```

2. Install dev tools:

```bash
pip install -r requirements-dev.txt
```

3. Run the coordinator to execute all checks and produce reports:

```bash
python toolkit/runners/run_agents.py
# or run a single agent via the runtime:
python toolkit/runtime.py toolkit/agents/senior_fastapi.agent.md
```

Reports are written to the [toolkit/reports/](toolkit/reports/) directory. CI also uploads the governance report on PRs via [.github/workflows/governance.yml](.github/workflows/governance.yml).



Notes
-----

- The canonical versioned API is mounted at `/api/v1/users`.
- This repository focuses on the backend; BDD tests are maintained in a separate project.
