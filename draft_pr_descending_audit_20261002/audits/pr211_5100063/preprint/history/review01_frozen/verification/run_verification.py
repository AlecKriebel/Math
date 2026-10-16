#!/usr/bin/env python3
"""Verify the portable payload and replay checkers in disposable copies.

No repository checkout, network connection or absolute workspace path is used.
The checkers are archived verbatim. They intentionally write results beside
their script, so only explicitly listed inputs are copied to temporary folders.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import time

BASE = Path(__file__).resolve().parent
FORBIDDEN = {"private", "private_reading", "private_transport", "__pycache__"}

JOBS = [
    {"id": "author", "group": "core", "folder": "original_submission",
     "script": "verify.py", "inputs": ["PROOF.md"], "result": "verification.json"},
    {"id": "inherited_independent", "group": "core", "folder": "original_submission/independent_review",
     "script": "independent_check.py", "inputs": [], "result": "INDEPENDENT_CHECKS.json"},
    {"id": "source_geometry", "group": "core", "folder": "audits/source_scope_adversary_01",
     "script": "source_geometry_check.py", "inputs": [], "result": "source_geometry_checks.json"},
    {"id": "geometry_algebra", "group": "core", "folder": "audits/geometry_algebra_adversary_01",
     "script": "controls.py", "inputs": ["INDEPENDENT_DERIVATION.md"], "result": "CONTROL_SUMMARY.json",
     "environment_fields": ["python"]},
    {"id": "meromorphic_divisor", "group": "core", "folder": "audits/meromorphic_divisor_adversary_01",
     "script": "independent_controls.py", "inputs": ["INDEPENDENT_DERIVATION.md"], "result": "CONTROL_RESULTS.json",
     "environment_fields": ["python"]},
    {"id": "exact_scope_separation", "group": "scope", "folder": "audits/priority_author_updates_01",
     "script": "exact_scope_separation.py", "inputs": [], "result": "EXACT_SCOPE_SEPARATION.json"},
    {"id": "classical_transfer_controls", "group": "scope", "folder": "audits/priority_classical_general_01",
     "script": "check_controls.py", "inputs": [], "result": "CONTROL_RESULTS.json"},
    {"id": "exact_triangle", "group": "scope", "folder": "scope_controls",
     "script": "root_exact_triangle_control.py", "inputs": [], "result": "ROOT_EXACT_TRIANGLE_CONTROL.json"},
    {"id": "generic_transfer_obstruction", "group": "scope", "folder": "scope_controls",
     "script": "root_generic_transfer_counterexample.py", "inputs": [], "result": "ROOT_GENERIC_TRANSFER_COUNTEREXAMPLE.json"},
    {"id": "transverse_transfer_obstruction", "group": "scope", "folder": "scope_controls",
     "script": "root_transverse_transfer_counterexample.py", "inputs": [], "result": "ROOT_TRANSVERSE_TRANSFER_COUNTEREXAMPLE.json"},
]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def checked_relative(name):
    path = PurePosixPath(name)
    if (path.is_absolute() or not path.parts or any(x in {"", ".", ".."} for x in path.parts)
            or set(path.parts) & FORBIDDEN or "\\" in name):
        raise ValueError(f"Unsafe manifest path: {name!r}")
    return path


def verify_integrity():
    raw = (BASE / "MANIFEST.json").read_bytes()
    manifest = json.loads(raw)
    if manifest.get("schema") != "portable-pr211-sha256-v1":
        raise ValueError("Unexpected portable manifest schema")
    seen = set()
    total = 0
    for row in manifest["files"]:
        rel = checked_relative(row["path"])
        if row["path"] in seen or row["path"] == "MANIFEST.json":
            raise ValueError("Duplicate entry or self-reference in manifest")
        seen.add(row["path"])
        path = BASE.joinpath(*rel.parts)
        if path.is_symlink() or not path.is_file() or BASE not in path.resolve().parents:
            raise ValueError(f"Missing or unsafe payload: {rel}")
        data = path.read_bytes()
        if len(data) != row["bytes"] or sha256(data) != row["sha256"]:
            raise ValueError(f"Integrity mismatch: {rel}")
        total += len(data)
    actual = set()
    for path in BASE.rglob("*"):
        rel = path.relative_to(BASE)
        if path.is_symlink() or set(rel.parts) & FORBIDDEN:
            raise ValueError(f"Forbidden payload or symlink: {rel}")
        if path.is_file() and rel.as_posix() != "MANIFEST.json":
            actual.add(rel.as_posix())
    if actual != seen:
        raise ValueError(f"Manifest inventory differs: missing={sorted(seen-actual)}, extra={sorted(actual-seen)}")
    return {"status": "PASS", "files": len(seen), "bytes": total,
            "manifest_sha256": sha256(raw)}


def check_environment():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError("Run without -O/-OO: archived checkers use assertions")
    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10 or newer is required; exercised version is 3.14.6")
    required = {"sympy": "1.14.0", "mpmath": "1.3.0"}
    for name, wanted in required.items():
        got = importlib.metadata.version(name)
        if got != wanted:
            raise RuntimeError(f"Require {name}=={wanted}, found {got}")
    return {"python": sys.version, **required}


def scientific_payload(value, job):
    value = deepcopy(value)
    for name in job.get("environment_fields", []):
        value.pop(name, None)
    return value


def replay(job, timeout):
    folder = BASE / job["folder"]
    expected_raw = (folder / job["result"]).read_bytes()
    expected = json.loads(expected_raw)
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="k904a-replay-") as name:
        work = Path(name)
        for relative in [job["script"], *job["inputs"]]:
            rel = checked_relative(relative)
            destination = work.joinpath(*rel.parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(folder / relative, destination)
        env = os.environ.copy()
        env.pop("PYTHONOPTIMIZE", None)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run([sys.executable, "-B", str(work / job["script"])], cwd=work,
                                   env=env, capture_output=True, text=True, timeout=timeout)
        if completed.returncode:
            raise RuntimeError(f"{job['id']} failed ({completed.returncode}):\n{completed.stderr[-6000:]}\n{completed.stdout[-2000:]}")
        actual_raw = (work / job["result"]).read_bytes()
        actual = json.loads(actual_raw)
        if scientific_payload(actual, job) != scientific_payload(expected, job):
            raise AssertionError(f"{job['id']}: replay JSON differs from frozen scientific results; investigate, do not silently relax")
        return {"id": job["id"], "status": "PASS", "isolated": True,
                "scientific_json_equal": True, "byte_identical": actual_raw == expected_raw,
                "expected_result_sha256": sha256(expected_raw),
                "actual_result_sha256": sha256(actual_raw),
                "ignored_environment_fields": job.get("environment_fields", []),
                "seconds": round(time.monotonic() - start, 3)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", choices=["core", "scope", "all"] + [j["id"] for j in JOBS],
                        help="Replay the five core programs, scope controls, all programs, or one named job")
    parser.add_argument("--list", action="store_true", help="List jobs after checking payload integrity")
    parser.add_argument("--timeout", type=int, default=1800, help="Per-job timeout in seconds")
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    before = verify_integrity()
    result = {"integrity": before, "limitations": "Finite exact controls and uncertified numerical diagnostics support the written universal proof; they are neither a formal proof nor a priority certificate."}
    if args.list:
        result["jobs"] = [{k: job[k] for k in ["id", "group", "folder", "script", "inputs", "result"]} for job in JOBS]
    if args.run:
        result["environment"] = check_environment()
        selected = [j for j in JOBS if args.run == "all" or j["group"] == args.run or j["id"] == args.run]
        result["replays"] = []
        for job in selected:
            print(f"Replaying {job['id']} in a temporary folder", file=sys.stderr, flush=True)
            result["replays"].append(replay(job, args.timeout))
        after = verify_integrity()
        if after != before:
            raise AssertionError("Frozen packet changed during replay")
        result["frozen_payload_unchanged"] = True
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
