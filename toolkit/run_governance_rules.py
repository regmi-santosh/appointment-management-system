import os
import sys

import yaml


def run_rules(path: str):
    with open(path, "r") as f:
        rules = yaml.safe_load(f)
    findings = []
    for r in rules.get("rules", []):
        rid = r.get("id")
        desc = r.get("description")
        # simple env-based check
        if r.get("check") == "env:APP_SECRET":
            val = os.environ.get("APP_SECRET", "")
            if len(val) < 32:
                findings.append(
                    {"id": rid, "severity": r.get("severity"), "message": desc}
                )
        # pattern checks could be extended
    return findings


def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--rules", required=True)
    args = p.parse_args()
    f = run_rules(args.rules)
    if f:
        print("Governance findings:")
        for item in f:
            print(item)
        sys.exit(2)
    print("No governance findings")


if __name__ == "__main__":
    main()
