# Folder Restructure Proposal

Summary
-------
This document proposes a streamlined folder layout and migration plan for the Appointment Management System. The goal is to improve discoverability, enforce clear separation of concerns, and make the repo easier to navigate for contributors.

Current (high-level)
--------------------
```
app/
  __init__.py
  db.py
  main.py
  openapi_description.md
  api/
  schemas/
  services/
  users/
    api/
    domain/
    schemas/
    services/
features/
tests/
toolkit/
```

Proposed (streamlined)
----------------------
```
app/
  main.py                 # FastAPI app setup, docs, startup events
  core/                   # core app utilities and shared components
    config.py             # app configuration (env management)
    auth.py               # auth helpers (token creation/verify)
    db.py                 # DB connection & migrations
  api/                    # API routers (versioned)
    v1/
      users.py            # users endpoints
  users/                  # domain package for users
    __init__.py
    models.py             # dataclasses / pydantic models used by domain
    repository.py         # repository implementations
    service.py            # domain services
    schemas.py            # request/response pydantic schemas (API-facing)
tests/
  unit/
  integration/
features/
tooling/                  # CI, devtools, scripts (migrations, linters)
README.md
```

Rationale
---------
- `core/` groups cross-cutting utilities (config, auth, db) used across domains.
- Move versioned API routers under `app/api/v1` to keep top-level API routing consistent.
- Combine per-domain `schemas` and `services` into a single `users/` package with clear names (`models.py`, `repository.py`, `service.py`, `schemas.py`) to reduce nested folders and duplication.
- Separate `toolkit/` into `tooling/` for scripts and CI helpers; keep `features/` for BDD scenarios.

Migration plan
--------------
1. Draft PR that only moves files and updates imports (no behavior changes). Keep changes minimal and run tests.
2. Run full test suite and fix import regressions.
3. Incrementally refactor internal names (e.g., rename `user_service.py` → `service.py`) in separate small PRs.
4. Use redirects/compatibility imports for a short period (e.g., `app/users/api/__init__.py` re-exporting new module) if public import paths are relied upon.

Checklist for reviewers
----------------------
- Are all API paths preserved (or intentional redirects added)?
- Are tests still passing after moves?
- Are DB init/migration steps safe and idempotent?
- Is auth/security code centralized and documented?

Next steps
----------
1. Assign board reviewers from `BOARD_OF_EXPERTS.md`.
2. Maintain a branch and open a PR implementing step 1 of the migration plan.
3. Address comments and iterate.
