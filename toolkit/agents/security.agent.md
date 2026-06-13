---
name: Security Agent
maintainer: Security Team
description: |
  An automated agent that runs security scans and produces a prioritized report
  of issues, suggested fixes, and references. Integrates bandit, pip-audit,
  safety, and repository-specific custom rules.
capabilities:
  - run-scans: Execute configured security tools and collect outputs.
  - triage: Prioritize issues by severity and suggest remediation steps.
  - report: Produce markdown summaries suitable for PR comments.
inputs:
  - repo_path: Path to code repository
  - env: Optional environment variables
outputs:
  - report_path: Path to generated report
runbook: |
  1. Ensure virtualenv with dev dependencies is available.
  2. Run `bandit -r app/` then `pip-audit` and `safety check`.
  3. Execute `toolkit/run_governance_rules.py --rules toolkit/rules/security.rules.yaml`.
  4. Aggregate and triage findings into a `security-report.md`.
# Security Agent — Project Security Assistant

Purpose
-------
Assist in enforcing security best practices across the codebase and CI: dependency checks, static analysis, secret/credential detection, configuration validation, and threat review.

Responsibilities
----------------
- Run automated security scanners (Bandit, pip-audit/pip-audit, safety) and aggregate results.
- Detect hard-coded secrets and unsafe config (e.g., weak APP_SECRET, DB_PATH in repo).
- Validate password hashing and token handling follow best practices.
- Produce a prioritized `security-report.md` with findings and remediation steps.

Usage
-----
- Local: run the provided instructions to reproduce security checks.
- CI: run on PRs and block merges for high-severity findings.
