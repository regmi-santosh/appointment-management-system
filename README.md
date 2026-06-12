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

Run tests:

```bash
pytest -q
```

Project layout:

- app/: FastAPI application
- tests/: pytest + pytest-bdd tests
- requirements.txt: dependencies
