# Decision Proposal: Toolkit & Agent Structure (Draft for Board)

Recommendation (short)
- Adopt the Hybrid model: canonical shared folders under `toolkit/` for shared assets, and optional per-agent subfolders for agent-specific resources.

Canonical layout (final proposal)

toolkit/
  agents/                # agent markdowns (`<agent>.agent.md`) referencing policies/skills
  agents/<agent-id>/     # optional per-agent subfolder for overrides (templates, README)
  skills/                # shared skill YAMLs describing checks
  policies/              # policy YAMLs mapping policy ids to rules/skills
  rules/                 # shared rule definitions (security, coding, governance)
  runners/               # executable scripts implementing skill checks
  templates/             # vetted codegen templates (versioned)
  reports/               # run outputs and archived artifacts
  audits/                # audit logs and change history
  runtime.py             # orchestrator that loads agents and runs required runners

Key enforcement points
- Local: `pre-commit` hooks for formatting and fast checks.
- Runtime: `toolkit/runtime.py` runs the required skill runners and enforces policy results before PR creation.
- CI: runs `toolkit/run_agents.py` (coordinator) and the per-agent runtime runs to validate PRs and produce artifacts.

Access & permissions
- Agents default to `allow_direct_commits: false`. Runtime must create PRs for code changes.
- Designate a small group of maintainers able to approve agent-generated PRs and to enable `allow_direct_commits` for specific safe agents.

Template and codegen governance
- Templates live in `toolkit/templates/` and are versioned. Only Board-approved templates can be used by agents.
- Agents must include tests with any generated code; `coding-standards` skill includes `pytest` to ensure tests pass.

Refactor plan (minimal, incremental)
1. Move current runner scripts into `toolkit/runners/` and update skill YAMLs to reference them.
2. Create `toolkit/reports/` and `toolkit/audits/` and update runners to write outputs there.
3. Add per-agent subfolders only when necessary and migrate agent-specific assets.
4. Update `toolkit/runtime.py` to discover runners under `toolkit/runners/` and allow per-agent overrides.
5. Update CI to execute per-agent runtime checks on PRs and upload reports.

Acceptance criteria for Board sign-off
- Clear folder layout agreed and documented.
- Owner(s) for each top-level folder assigned.
- Minimum checks list finalized (format/lint/tests/security), and CI runs them on PRs.
- Migration/refactor plan approved with staged tasks and owners.

Next step
- Schedule the Board meeting and collect availability. After sign-off I'll implement step 1 and open a PR for the refactor.
