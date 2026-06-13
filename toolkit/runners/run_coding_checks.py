#!/usr/bin/env python3
"""Run coding-standards checks and produce a summary report into toolkit/reports."""
import shutil
import subprocess
from pathlib import Path
import sys

TOOLKIT_ROOT = Path(__file__).resolve().parent.parent
REPORTS = TOOLKIT_ROOT / 'reports'
REPORTS.mkdir(exist_ok=True)


def run(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return out.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()


def main():
    report = []

    # pre-commit
    if shutil.which('pre-commit'):
        report.append('=== pre-commit ===')
        report.append(run(['pre-commit', 'run', '--all-files']))
    else:
        report.append('pre-commit not available')

    # flake8
    if shutil.which('flake8'):
        report.append('=== flake8 ===')
        report.append(run(['flake8', '.']))
    else:
        report.append('flake8 not available')

    # mypy
    if shutil.which('mypy'):
        report.append('=== mypy ===')
        report.append(run(['mypy', '.']))
    else:
        report.append('mypy not available')

    # pytest
    if shutil.which('pytest'):
        report.append('=== pytest ===')
        report.append(run(['pytest', '-q']))
    else:
        report.append('pytest not available')

    out_path = REPORTS / 'coding-report.md'
    out_path.write_text('\n\n'.join(report))
    print(f'Report written to {out_path}')


if __name__ == '__main__':
    main()
