#!/usr/bin/env python3
"""Agent runtime orchestrator.

This simple runtime reads an agent markdown file with YAML frontmatter, loads
policy files, runs the relevant skill runners (coding + security), evaluates
whether required skills passed, and writes a combined report.

Usage (CLI):
  python toolkit/runtime.py path/to/agent.md

It also exposes `run_agent(agent_path, repo_root='.')` for programmatic use.
"""
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any

try:
    import yaml
except Exception:
    print('PyYAML is required. Install with `pip install pyyaml`')
    raise

ROOT = Path(__file__).resolve().parent


def load_frontmatter(path: Path) -> Dict[str, Any]:
    text = path.read_text()
    m = re.search(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    return yaml.safe_load(m.group(1)) or {}


def run_process(cmd):
    print(f"Running: {cmd}")
    parts = cmd if isinstance(cmd, (list, tuple)) else shlex.split(cmd)
    proc = subprocess.run(parts, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.decode()


def find_skill_file_by_name(skill_name: str):
    skills_dir = ROOT / 'skills'
    if not skills_dir.exists():
        return None
    for f in skills_dir.glob('*.yaml'):
        data = yaml.safe_load(f.read_text()) or {}
        if data.get('name') == skill_name or data.get('id') == skill_name:
            return f, data
    return None


def run_skill_runner(skill_name: str, agent_id: str = None) -> Dict[str, Any]:
    """Resolve a skill's runner (skill YAML `runner` field), prefer per-agent override,
    and execute it. Returns dict with `name`, `exit_code`, and `output`.
    """
    found = find_skill_file_by_name(skill_name)
    runner_path = None
    if found:
        f, data = found
        runner_field = data.get('runner')
        if runner_field:
            # runner_field may be a relative path like 'runners/run_x.py'
            candidate = ROOT / runner_field
            # allow per-agent override
            if agent_id:
                agent_override = ROOT / 'agents' / agent_id / Path(runner_field).name
                if agent_override.exists():
                    runner_path = agent_override
            if runner_path is None and candidate.exists():
                runner_path = candidate

    # fallback: common mapping
    if runner_path is None:
        mapping = {
            'coding-standards': ROOT / 'runners' / 'run_coding_checks.py',
            'security': ROOT / 'runners' / 'run_security_checks.py',
            'security-standards': ROOT / 'runners' / 'run_security_checks.py',
        }
        runner_path = mapping.get(skill_name)

    if runner_path is None or not runner_path.exists():
        return {'name': skill_name, 'exit_code': 2, 'output': f'No runner for {skill_name} (tried {runner_path})'}

    python_exe = shutil.which('python') or shutil.which('python3')
    if not python_exe:
        return {'name': skill_name, 'exit_code': 2, 'output': 'python not found in PATH'}

    rc, out = run_process([python_exe, str(runner_path)])
    return {'name': skill_name, 'exit_code': rc, 'output': out}


def load_policy(policy_id: str) -> Dict[str, Any]:
    p = ROOT / 'policies' / f'{policy_id}.yaml'
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text()) or {}


def run_agent(agent_path: str, repo_root: str = '.') -> int:
    agent_file = Path(agent_path)
    if not agent_file.exists():
        print(f'Agent file not found: {agent_file}')
        return 2

    meta = load_frontmatter(agent_file)
    agent_id = meta.get('id') or agent_file.stem
    print(f'Running agent: {agent_id}')

    # collect policies
    policies = meta.get('policies', [])
    policy_defs = [load_policy(p) for p in policies]

    # determine required skills from policies (fallback: run all skills)
    required_skills = set()
    for p in policy_defs:
        for s in p.get('required_skills', []) or []:
            required_skills.add(s)

    if not required_skills:
        # run all skill yamls in toolkit/skills
        skills_dir = ROOT / 'skills'
        if skills_dir.exists():
            for f in skills_dir.glob('*.yaml'):
                data = yaml.safe_load(f.read_text()) or {}
                name = data.get('name')
                if name:
                    required_skills.add(name)

    print(f'Required skills to run: {sorted(required_skills)}')

    results = []
    for skill in sorted(required_skills):
        res = run_skill_runner(skill)
        results.append(res)

    report_path = ROOT / f'agent-{agent_id}-report.md'
    with report_path.open('w') as f:
        f.write(f'# Agent run: {agent_id}\n\n')
        f.write('## Metadata\n')
        f.write(yaml.safe_dump(meta))
        f.write('\n\n')
        for r in results:
            f.write(f"### Skill: {r['name']} (exit {r['exit_code']})\n\n")
            f.write('''```
''')
            f.write(r.get('output') or '(no output)')
            f.write('\n```\n\n')

    # determine overall success: all exit_code == 0
    failed = any(r['exit_code'] != 0 for r in results)

    # write audit entry
    try:
        import json
        from datetime import datetime
        import os

        audits_dir = ROOT / 'audits'
        audits_dir.mkdir(exist_ok=True)
        audit = {
            'agent_id': agent_id,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'user': os.environ.get('USER') or os.environ.get('USERNAME') or None,
            'agent_meta': meta,
            'results': [{'name': r['name'], 'exit_code': r['exit_code']} for r in results],
            'report': str(report_path),
        }
        audit_path = audits_dir / f"audit-{agent_id}-{int(datetime.utcnow().timestamp())}.json"
        audit_path.write_text(json.dumps(audit, indent=2))
        print(f'Wrote audit to {audit_path}')
    except Exception as e:
        print(f'Failed to write audit: {e}')

    if failed:
        print(f'Agent {agent_id} failed checks; see {report_path}')
        return 3

    print(f'Agent {agent_id} completed successfully; report at {report_path}')
    return 0


def main():
    if len(sys.argv) < 2:
        print('Usage: toolkit/runtime.py path/to/agent.md')
        sys.exit(2)
    rc = run_agent(sys.argv[1])
    sys.exit(rc)


if __name__ == '__main__':
    main()
