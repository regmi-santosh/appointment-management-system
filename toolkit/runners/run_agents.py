#!/usr/bin/env python3
"""Coordinator to run coding and security agent checks and produce a combined report into toolkit/reports.

This script runs the key tooling and writes `toolkit/reports/agents-report.md`. It exits with non-zero if any check fails.
"""
import shutil
import subprocess
from pathlib import Path
import sys

TOOLKIT_ROOT = Path(__file__).resolve().parent.parent
REPORTS = TOOLKIT_ROOT / 'reports'
REPORTS.mkdir(exist_ok=True)


def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = proc.stdout.decode()
    return proc.returncode, out


def ensure_tool(tool):
    return shutil.which(tool) is not None


def main():
    report_lines = []
    failed = False

    checks = [
        ("pre-commit", ["pre-commit", "run", "--all-files"]),
        ("flake8", ["flake8", "."]),
        ("mypy", ["mypy", "."]),
        ("bandit", ["bandit", "-r", "app/"]),
        ("pip-audit", ["pip-audit", "--progress", "off"]),
        ("safety", ["safety", "check", "--full-report"]),
    ]

    for name, cmd in checks:
        report_lines.append(f"## {name}\n")
        if not ensure_tool(cmd[0]):
            report_lines.append(f"{name} not installed: {cmd[0]}\n")
            failed = True
            continue

        rc, out = run_cmd(cmd)
        report_lines.append(out or "(no output)\n")
        if rc != 0:
            failed = True

    out_path = REPORTS / 'agents-report.md'
    out_path.write_text('\n'.join(report_lines))
    print(f"Wrote report to {out_path}")

    if failed:
        print("One or more checks failed.")
        sys.exit(1)
    print("All checks passed.")


if __name__ == '__main__':
    main()
