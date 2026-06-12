# Agents directory

Structure and conventions for repository-scoped agents used by maintainers.

Layout:

- `/.github/agents/` - top-level agent definitions (one file per agent).
- `/.github/agents/rules/` - reusable rule files referenced by agents' `policies`.
- `/.github/agents/skills/` - reusable skill definitions that map to runtime handlers.
 - `/.github/agents/agents/` - agent manifests (one file per agent).
 - `toolkit/skills/` - runtime-owned skill definitions and implementations.

Conventions:

- Agent files should be YAML or Markdown with frontmatter including `id`, `name`, `description`, `entrypoint`, `capabilities`, and `policies`.
- Rules should define `id`, `description`, `trigger`, `condition`, and `action`.
- Skills should define `id`, `name`, `description`, `commands` with `handler` and `permissions`.
- Keep `allow_direct_commits` conservative (false) for agents that modify repo code.

Placement guidance:

- Put repository governance (rules, agent manifests) under `/.github/agents/`.
- Put skill implementations that map to `toolkit.skills.*` under `toolkit/skills/` so code and YAML live together.

Validation:

- Use the `.github/workflows/validate-agents.yml` workflow to lint and parse agent YAML files on PRs and pushes.
