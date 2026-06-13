# Coding Style Guide

This project follows a consistent, modern Python style to improve readability and reduce friction when contributing.

Formatting
- Use `black` (line length 88). Run: `black .`
- Use `isort` for import sorting. Run: `isort .`

Linting
- Use `flake8` for linting; configure to enforce complexity, unused imports, and line length.
- Use `mypy` for optional static typing checks.

Type Hints
- Add type hints for public functions and methods where practical.

Naming & Structure
- Prefer descriptive names; avoid single-letter names except in comprehensions and iterators.
- Keep modules small and focused. One class or closely related helper functions per module.

Files & Imports
- Group imports in three sections: standard library, third-party, local.
- Avoid wildcard imports.

Tests
- Add tests for new features and bug fixes. Strive for meaningful unit tests with fixtures.

Commit Messages
- Use conventional commits style: `feat:`, `fix:`, `chore:`, `docs:`, `test:`.

Formatting commands (quick):
```
pip install -r requirements.txt
pip install black isort flake8 mypy pre-commit
pre-commit install
black .
isort .
flake8
mypy
```
