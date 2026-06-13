# Governance Agent — Project Governance Assistant

Purpose
-------
Lightweight agent to help enforce and review project governance: architecture alignment, security practices, coding standards, and contribution policies.

Responsibilities
----------------
- Run automated checks (lint, security scanners) and report failures.
- Validate new modules follow the project's architecture and directory layout.
- Review PRs for coding standards and security best practices.
- Produce concise remediation guidance for maintainers.

How to use
----------
- Manual: run the governance checks locally during code review.
- CI: wire this agent into PR pipelines to produce a governance report artifact.

Outputs
-------
- `governance-report.md` — summary of findings.
- GitHub labels or checklist comments indicating required actions.
