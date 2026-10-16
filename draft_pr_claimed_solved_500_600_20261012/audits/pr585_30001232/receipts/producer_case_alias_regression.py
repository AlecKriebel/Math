#!/usr/bin/env python3
"""Real unchanged-producer case-alias controls using only preserved authored bytes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect-accepted", action="store_true")
    args = parser.parse_args()
    audit = Path(__file__).resolve().parents[1]
    original = (audit / "publication/make_package.py").read_bytes()
    expected_zip = (audit / "publication/verification_package.zip").read_bytes()
    cases = []
    for component in (".cache", "sources", "scratch", "qa", ".secrets", ".private"):
        with tempfile.TemporaryDirectory(prefix="case-alias-", dir=audit / "root_reproduction/.cache") as temp:
            copy = Path(temp) / "audit"
            shutil.copytree(audit, copy, ignore=shutil.ignore_patterns(".cache", "qa", "receipts", "package_preflight*"))
            family = copy / "reviews/geometry01"
            lower = copy / component / "sealed_family"
            lower.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(family), str(lower))
            upper = copy / component.upper() / "sealed_family"
            if not upper.exists() or not upper.samefile(lower):
                raise RuntimeError("This regression requires the observed case-insensitive filesystem")
            family.symlink_to(upper, target_is_directory=True)
            script = copy / "publication/make_package.py"
            if script.read_bytes() != original:
                raise RuntimeError("Copied producer changed")
            proc = subprocess.run(["/usr/bin/sandbox-exec", "-p", "(version 1) (allow default) (deny network*)",
                                   sys.executable, "-B", str(script)], cwd=script.parent,
                                  env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), capture_output=True, text=True)
            accepted = proc.returncode == 0
            if accepted != args.expect_accepted:
                raise RuntimeError("Unexpected case-alias result: " + component + proc.stderr)
            if not accepted and "Excluded source" not in proc.stderr:
                raise RuntimeError("Unrelated failure: " + proc.stderr)
            if accepted and (copy / "publication/verification_package.zip").read_bytes() != expected_zip:
                raise RuntimeError("Accepted selection changed payload bytes")
            cases.append({"component": component, "alias": component.upper(), "same_object": True,
                          "actual_unchanged_producer_process": True, "selectors_and_seals_unchanged": True,
                          "accepted": accepted, "returncode": proc.returncode,
                          "diagnostic": proc.stderr.strip().splitlines()[-1] if proc.stderr else "accepted exact ZIP"})
    print(json.dumps({"status": "PASS", "producer_sha256": hashlib.sha256(original).hexdigest(),
                      "OS_network_denied": True, "controls": cases,
                      "limits": "Copies selected only the same sealed authored bytes, never raw or private data."},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
