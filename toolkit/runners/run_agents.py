#!/usr/bin/env python3
"""Coordinator to run coding and security agent checks and produce a combined report into toolkit/reports.

This script runs the key tooling and writes `toolkit/reports/agents-report.md`. It exits with non-zero if any check fails.
"""
import shutil
import subprocess
import sys
import venv
from pathlib import Path

TOOLKIT_ROOT = Path(__file__).resolve().parent.parent
REPORTS = TOOLKIT_ROOT / "reports"
REPORTS.mkdir(exist_ok=True)


def run_cmd(cmd):
    # Prefer project .venv tool if available
    venv_tool = TOOLKIT_ROOT.parent / ".venv" / "bin" / cmd[0]
    if venv_tool.exists():
        cmd = [str(venv_tool)] + cmd[1:]
    print(f"Running: {' '.join(cmd)}")
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = proc.stdout.decode()
    return proc.returncode, out


def ensure_tool(tool):
    # Check system path first
    if shutil.which(tool):
        return True
    # Check project .venv bin
    venv_bin = TOOLKIT_ROOT.parent / ".venv" / "bin" / tool
    if venv_bin.exists():
        return True
    return False


def ensure_project_venv():
    venv_path = TOOLKIT_ROOT.parent / ".venv"
    python_bin = venv_path / "bin" / "python"
    if python_bin.exists():
        return True

    print("Creating project virtualenv at .venv and installing dev requirements...")
    try:
        venv.create(str(venv_path), with_pip=True)
    except Exception as e:
        print("Failed to create virtualenv:", e)
        return False

    reqs = TOOLKIT_ROOT.parent / "requirements-dev.txt"
    if not reqs.exists():
        print("No requirements-dev.txt found; skipping install")
        return True

    pip_cmd = [str(python_bin), "-m", "pip", "install", "--upgrade", "pip"]
    subprocess.run(pip_cmd, check=False)
    install_cmd = [str(python_bin), "-m", "pip", "install", "-r", str(reqs)]
    rc = subprocess.run(install_cmd)
    return rc.returncode == 0


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

    # check for missing tools first
    missing = [name for name, cmd in checks if not ensure_tool(cmd[0])]
    if missing:
        print("Missing tools detected:", missing)
        ok = ensure_project_venv()
        if ok:
            print("Installed project dev dependencies; continuing")
            # attempt per-tool install for any still-missing tools
            venv_python = TOOLKIT_ROOT.parent / ".venv" / "bin" / "python"
            for name in missing:
                tool = name
                venv_tool = TOOLKIT_ROOT.parent / ".venv" / "bin" / tool
                if not venv_tool.exists():
                    print(f"Attempting to install {tool} into .venv")
                    install_cmd = [str(venv_python), "-m", "pip", "install", tool]
                    subprocess.run(install_cmd)
        else:
            print(
                "Failed to prepare project virtualenv; continuing to report missing tools"
            )

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

    out_path = REPORTS / "agents-report.md"
    out_path.write_text("\n".join(report_lines))
    print(f"Wrote report to {out_path}")

    if failed:
        print("One or more checks failed.")
        sys.exit(1)
    print("All checks passed.")


if __name__ == "__main__":
    main()
