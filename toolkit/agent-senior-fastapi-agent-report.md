# Agent run: senior-fastapi-agent

## Metadata
capabilities:
- code-edit
- design
- review
- testing
- ci-config
- api-design
- openapi
config:
  allow_direct_commits: false
  max_steps: 12
description: Senior Python developer (15 years) specializing in FastAPI, architecture,
  testing, and production readiness.
entrypoint: toolkit.runtime:run_agent
id: senior-fastapi-agent
name: Senior FastAPI Developer
policies:
- senior-fastapi-no-secrets
- senior-fastapi-require-tests


### Skill: coding-standards (exit 0)

```
Report written to /Users/sansha/Documents/Projects/Tej Dai/appointment-management-system/toolkit/reports/coding-report.md

```

### Skill: security-standards (exit 0)

```
Report written to /Users/sansha/Documents/Projects/Tej Dai/appointment-management-system/toolkit/reports/security-report.md

```
