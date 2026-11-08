#!/usr/bin/env python3
"""Positive and negative controls for fail-closed, optimized-mode replay."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def run(where, optimized):
    command = [sys.executable] + (["-O"] if optimized else []) + [str(where / "verify_release.py")]
    return subprocess.run(command, text=True, capture_output=True, timeout=120)


def rebind(where, name):
    path = where / "MANIFEST.json"
    m = json.loads(path.read_text())
    b = (where/name).read_bytes()
    m["files"][name] = {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
    path.write_text(json.dumps(m, indent=2, sort_keys=True)+"\n")


def mutate_json(where, name, key, value):
    p = where/name
    d = json.loads(p.read_text())
    if isinstance(key, tuple):
        d[key[0]][key[1]] = value
    else:
        d[key] = value
    p.write_text(json.dumps(d, indent=2, sort_keys=True)+"\n")
    rebind(where, name)


def main():
    checks = []
    for optimized in [False, True]:
        r = run(ROOT, optimized)
        require(r.returncode == 0, "clean replay failed: " + r.stderr)
        value = json.loads(r.stdout)
        require(value["optimized_python"] == optimized, "optimized-mode indicator")
        checks.append({"case":"clean", "optimized":optimized, "expected_pass":True})
    cases = ["changed_bytes", "missing_file", "wrong_target", "wrong_certificate", "nan_json", "empty_manifest"]
    for case in cases:
        with tempfile.TemporaryDirectory(prefix="bahri_xu_verifier_") as directory:
            where = Path(directory)
            for p in ROOT.iterdir():
                if p.is_file():
                    shutil.copy2(p, where/p.name)
            if case == "changed_bytes":
                p = where/"RESEARCH_REPORT.md"
                p.write_text(p.read_text()+"\nUnmanifested alteration.\n")
            elif case == "missing_file":
                (where/"EXACT_CERTIFICATES.json").unlink()
            elif case == "wrong_target":
                mutate_json(where,"TARGET_REVIEW.json","problem_id",30000264)
            elif case == "wrong_certificate":
                mutate_json(where,"EXACT_CERTIFICATES.json",("min_ball","boundary_count"),4)
            elif case == "nan_json":
                p=where/"TARGET_REVIEW.json"
                p.write_text('{"problem_id": NaN}\n')
                rebind(where,p.name)
            elif case == "empty_manifest":
                (where/"MANIFEST.json").write_text('{"schema":1,"files":{}}\n')
            for optimized in [False, True]:
                r = run(where, optimized)
                require(r.returncode != 0 and "FAIL:" in r.stderr, f"negative control accepted: {case}, -O={optimized}")
                checks.append({"case":case,"optimized":optimized,"expected_pass":False})
    print(json.dumps({"status":"PASS", "controls":checks, "count":len(checks)}, sort_keys=True))


if __name__ == "__main__":
    main()
