# Governance Instructions — How to run governance checks

1. Install dev tools:

```bash
python3 -m pip install ruff pytest bandit
```

2. Run governance skill locally:

```bash
# Lint
ruff .

# Tests
pytest -q

# Security scan
bandit -r app/

# Custom rules (simple YAML-driven checks)
python3 toolkit/run_governance_rules.py --rules toolkit/rules/governance.rules.yaml
```

3. Interpret the `governance-report.md` and file issues for any critical findings.

4. For PRs: mandate that `governance-report.md` shows no errors before merging.
