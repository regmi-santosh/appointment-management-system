# Proposed Toolkit Structure (for Board review)

Overview
- The toolkit contains agent metadata, skills (declarative checklists), policy mappings, rule definitions, runners, templates, and reports. The goal is a clear separation of concerns and discoverability.

Suggested layout

toolkit/
  agents/                # agent markdowns (`agent.md`) with YAML frontmatter
  skills/                # skill YAMLs defining checks and tool invocations
  policies/              # policy YAMLs mapping policy IDs to required skills/rules
  rules/                 # rule definitions (security, coding, governance)
  runners/               # executable scripts that implement skills (python scripts)
  runtime.py             # orchestrator that loads agents and runs required runners
  templates/             # vetted codegen templates (must be approved by Board)
  reports/               # generated run reports and archived artifacts
  audits/                # audit logs and change history

Naming conventions
- Agent files: `snake-case.agent.md` with `id:` in frontmatter.
- Skills/policies/rules: `kebab-case.yaml` with a top-level `name` or `id`.
- Runners: `run_<skill>.py` in `runners/` and referenced by skill YAML.
- Templates: versioned subfolders, e.g., `templates/v1/fastapi-endpoint/`.

Enforcement model
- Local: `pre-commit` enforces formatting and simple checks.
- Agent runtime: deterministic validation runs (format, lint, mypy, tests, security) before generating commits/PRs.
- CI: `governance.yml` runs coordinator to validate PRs and uploads reports.

Access control
- Default: `allow_direct_commits: false` on agents. Runtime should create PRs only.
- PRs require at least one Board maintainer approval for agent-generated changes that modify application code.

Refactor checklist
1. Move current runners to `toolkit/runners/` and update `toolkit/skills/*.yaml` to reference them.
2. Move `toolkit/run_*` scripts into `toolkit/runners/` and update `toolkit/runtime.py` to call runners from `runners/`.
3. Add `toolkit/reports/` and update runners to write there.
4. Add `toolkit/templates/` and migrate any codegen templates.
5. Update `.github/workflows/governance.yml` to call `toolkit/runtime.py` against each `toolkit/agents/*.md`.

Questions for implementation
- Do we keep `toolkit/` under repo root or extract to a separate governance repo? (pros/cons)
- Should runners be sandboxed (docker) in CI for stronger isolation?
