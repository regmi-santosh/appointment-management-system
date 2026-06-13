# Board of Experts Consultation Request: Toolkit & Agent Structure

Purpose
- Solicit guidance from the Board of Experts on the canonical layout, ownership, and enforcement workflow for toolkit agents, skills, policies, rules, and runners.

Meeting goals
- Validate a proposed directory layout for `toolkit/`.
- Agree naming conventions for agents, skills, policies, rules, and runners.
- Define enforcement points (local pre-commit, agent runtime, CI) and mapping of responsibilities.
- Decide on access controls for agents that can create commits/PRs.
- Define audit and reporting expectations (artifacts, format, retention).

Proposed agenda
1. Introductions and scope (5m)
2. Walkthrough of current toolkit state and examples (10m)
3. Review proposed structure and rationale (15m)
4. Discuss enforcement model: runtime responsibilities and CI gating (15m)
5. Access control & approval process for automated changes (10m)
6. Open Q&A and action items (5m)

Key questions for the board
- Do you prefer a single `toolkit/` with clearly-separated subfolders, or multiple top-level folders (e.g., `.github/agents` + `toolkit/`)?
- For agents that can modify code, should `allow_direct_commits` ever be true, and under what controls? (e.g., signed approvals, protected branches)
- Preferred format for policy files and rule expressions (YAML DSL, JSON, or embedded Python)?
- How should we structure templates for generated code so the runtime can validate them deterministically?
- What reviewers/roles should be auto-assigned for governance PRs?

Deliverables requested from Board
- Approved folder layout (one-page) and naming conventions.
- Short checklist of mandatory checks for any agent-run codegen (format/lint/tests/security).
- Recommended retention policy for generated reports and audit logs.

Next steps after meeting
- Consolidate feedback into `toolkit/board/PROPOSED_TOOLKIT_STRUCTURE.md` and a refactor plan.
- Implement refactor in a gated branch and open PR for Board review.
