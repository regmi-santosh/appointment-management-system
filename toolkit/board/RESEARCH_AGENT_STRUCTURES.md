# Research: Agent & Toolkit Structure Options

Purpose
- Summarize common layouts for storing agents, skills, policies, rules, runners and templates; list pros/cons and recommend a pragmatic approach for this project.

Common approaches

1) Flat toolkit hierarchy (recommended default)
- Structure: `toolkit/agents/`, `toolkit/skills/`, `toolkit/policies/`, `toolkit/rules/`, `toolkit/runners/`, `toolkit/templates/`, `toolkit/reports/`
- Pros: clear separation of concerns; easy discovery and bulk operations; CI can run all skills/policies; simple mappings for runtime.
- Cons: some agent-specific assets (templates, rules) may need cross-references; possible clutter if many agents.

2) Agent-centric directories (per-agent bundle)
- Structure: `toolkit/agents/<agent-id>/` containing `agent.md`, `rules.yaml`, `skills.yaml`, `runner.py`, `README.md`, `templates/`.
- Pros: encapsulates everything an agent needs; easier to review agent-level changes; simplifies packaging and permissions per-agent.
- Cons: harder to share common skills and rules; duplication risk; CI must discover nested assets.

3) Hybrid (recommended)
- Structure: canonical shared folders for common assets and per-agent subfolders for agent-specific overrides.
- Layout:
  - `toolkit/agents/agent-a.md`
  - `toolkit/agents/agent-a/` (optional overrides)
  - `toolkit/skills/` (shared skill descriptors)
  - `toolkit/policies/` (shared policies)
  - `toolkit/rules/` (shared rules)
  - `toolkit/runners/` (scripts)
  - `toolkit/templates/` (versioned)
- Pros: reuses shared assets, keeps agent bundles when needed; balances discoverability and encapsulation.

4) Git-native placement (.github or .gitlab integration)
- Structure: place agent descriptors under `.github/agents/` or `.gitlab/agents/` for tighter integration with platform workflows.
- Pros: direct platform integration (actions, workflow contexts); may simplify CI permissions.
- Cons: mixing governance metadata with platform config; less portable; unclear for multi-platform setups.

5) Separate governance repo
- Move `toolkit/` into a dedicated governance repository.
- Pros: isolates governance tooling, tighter access control, separate CI and lifecycle.
- Cons: cross-repo changes are more complex; codegen affecting application repo requires PRs across repos or bot permissions.

Evaluation criteria
- Discoverability and simplicity for reviewers
- Reuse vs duplication of checks and templates
- Ease of CI/automation and runtime discovery
- Access control and least-privilege for agents
- Auditability and retention of reports

Recommended approach for this project
- Adopt the Hybrid model:
  - Keep canonical shared folders under `toolkit/` (`skills/`, `policies/`, `rules/`, `runners/`, `templates/`, `reports/`).
  - Allow `toolkit/agents/<agent-id>/` subfolders for agent-local assets only when necessary (templates, long agent READMEs, agent-specific tests).
  - Keep default agent descriptors as `toolkit/agents/<agent>.md` with frontmatter referencing policies/skills.
  - Place CI and runtime orchestration in `toolkit/runtime.py` (already added) and `toolkit/runners/` for executable scripts.

Immediate implementation plan
1. Move existing runner scripts to `toolkit/runners/` and update `toolkit/skills/*.yaml` to reference runners by path.
2. Create `toolkit/agents/<agent-id>/` only when agent requires multiple files (templates, extended docs).
3. Update `toolkit/runtime.py` to prefer runner lookups under `toolkit/runners/` and allow per-agent overrides under `toolkit/agents/<agent-id>/`.
4. Update CI (`.github/workflows/governance.yml`) to call `toolkit/runtime.py` per agent file.
5. Pilot with 1-2 agents (coding, security) and gather Board feedback.

Questions for Board
- Is the Hybrid model acceptable? Any preference for a stricter per-agent or flat model?
- Any organizational policies (e.g., put governance artifacts in a separate repo) we must follow?
- Are there compliance or retention rules for reports/audits we should implement now?
