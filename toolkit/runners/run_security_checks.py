#!/usr/bin/env python3
"""Run security scans and custom rules; produce a summary report into toolkit/reports."""
import os
import subprocess
import sys
import shutil
from pathlib import Path

TOOLKIT_ROOT = Path(__file__).resolve().parent.parent
REPORTS = TOOLKIT_ROOT / 'reports'
REPORTS.mkdir(exist_ok=True)


def run(cmd):
    print(f"Running: {' '.join(cmd)}")
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return out.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()


def main():
    report = []
    # bandit
    if shutil.which('bandit'):
        report.append('=== bandit ===')
        report.append(run(['bandit', '-r', 'app/']))
    else:
        report.append('bandit not installed')

    # pip-audit
    if shutil.which('pip-audit'):
        report.append('=== pip-audit ===')
        report.append(run(['pip-audit', '--progress', 'off']))
    else:
        report.append('pip-audit not installed')

    # safety
    if shutil.which('safety'):
        report.append('=== safety ===')
        report.append(run(['safety', 'check', '--full-report']))
    else:
        report.append('safety not installed')

    # custom rules runner if available
    rules_file = TOOLKIT_ROOT / 'rules' / 'security.rules.yaml'
    if rules_file.exists():
        report.append('=== custom rules ===')
        report.append(f'Rules file: {rules_file}')

    out_path = REPORTS / 'security-report.md'
    out_path.write_text('\n\n'.join(report))
    print(f'Report written to {out_path}')


if __name__ == '__main__':
    main()
