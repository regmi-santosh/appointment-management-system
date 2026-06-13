Migration notes — legacy → new layout
=====================================

This project was refactored to a cleaner, domain-driven layout. The following
notes map previous locations to the new consolidated modules and include a
recommended migration checklist.

Mapping
-------

- Old: `app/db.py` → New: `app/core/db.py` (re-export removed)
- Old: `app/auth.py` → New: `app/core/auth.py` (re-export removed)
- Old: `app/users/domain/repository.py` → New: `app/users/repository.py`
- Old: `app/users/services/user_service.py` → New: `app/users/service.py`
- Old: `app/users/schemas/user.py` → New: `app/users/schemas.py`
- Old: `app/users/api/__init__.py` → New: `app/api/v1/users.py`

Checklist for final cleanup
--------------------------
1. Run the full test-suite: `pytest -q` and fix failing imports.
2. Replace any external imports that referenced old locations (search for
   `app.users.domain` or `app.auth`) and point them at the new modules.
3. Remove compatibility wrappers only after all consumers update.
4. Update CI workflows to run tests and lint the new layout.
5. Prepare a PR with a clear commit history: (a) file moves, (b) import updates,
   (c) behavior fixes/tests.

Rollback
--------
If you need to roll back, the easiest approach is to revert the commit/branch
that performed the migration. If that is not possible, you can reconstruct
compatibility modules as small wrappers that re-export symbols from the new
locations while you update clients.
