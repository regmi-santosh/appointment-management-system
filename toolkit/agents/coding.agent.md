---
name: Coding Standards Agent
maintainer: Dev Team
description: |
  Runs project coding standards checks (formatting, linting, typing) and
  enforces repository-level rules. Produces a summary report suitable for
  inclusion in PRs or CI artifacts.
capabilities:
  - run-checks: Execute pre-commit, flake8, mypy, and custom rule checks.
  - report: Produce a markdown summary with findings and suggested fixes.
inputs:
  - repo_path: Path to code repository
outputs:
  - report_path: Path to generated report
runbook: |
  1. Ensure dev dependencies installed: `pip install -r requirements.txt` and `pip install pre-commit flake8 mypy`.
  2. Run `python toolkit/run_coding_checks.py` from repo root.
  3. Attach `toolkit/coding-report.md` to PR or CI job.
