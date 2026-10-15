#!/usr/bin/env python3
"""Replay the exact offline controls without changing any frozen payload."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from integrity import safe_path, verify_nested

ROOT = Path(__file__).resolve().parent


def inventory():
    result = {}
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT)
        if ".venv" in rel.parts or "__pycache__" in rel.parts:
            continue
        if p.is_symlink():
            raise RuntimeError(f"Unexpected symlink: {rel}")
        if p.is_file():
            name = rel.as_posix()
            safe_path(name)
            result[name] = p.read_bytes()
    return result


def main():
    if not __debug__ or os.environ.get("PYTHONOPTIMIZE"):
        raise RuntimeError("Run without Python optimization")
    manifest = json.loads((ROOT / "MANIFEST.json").read_text())
    before = inventory()
    expected = set(manifest["files"]) | {"MANIFEST.json"}
    if set(before) != expected:
        raise RuntimeError(
            f"Inventory mismatch: extra={set(before)-expected}, "
            f"missing={expected-set(before)}"
        )
    for name, record in manifest["files"].items():
        safe_path(name)
        data = before[name]
        if (len(data) != record["bytes"]
                or hashlib.sha256(data).hexdigest() != record["sha256"]):
            raise RuntimeError(f"Payload mismatch: {name}")
    if manifest["nested_seals"] != json.loads(before["SEALS.json"]):
        raise RuntimeError("Nested seal registry disagrees with SEALS.json")
    nested = verify_nested(before, manifest["nested_seals"])
    jobs = json.loads((ROOT / "JOBS.json").read_text())
    with tempfile.TemporaryDirectory(prefix=".verify-", dir=ROOT) as directory:
        scratch = Path(directory)
        for folder in ("original", "reviews", "root_reproduction"):
            shutil.copytree(ROOT / folder, scratch / folder)
        for job in jobs:
            script = safe_path(job["script"]).as_posix()
            record = safe_path(job["record"]).as_posix()
            p = subprocess.run(
                [sys.executable, str(scratch / script)],
                cwd=(scratch / script).parent,
                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
                capture_output=True, text=True,
            )
            if p.returncode:
                raise RuntimeError(f"{script} failed:\n{p.stderr}")
            actual = json.loads(p.stdout)
            if "generated_record" in job:
                if script != "reviews/priority04_hib1996/checks.py":
                    raise RuntimeError("Generated-record replay assigned to wrong job")
                summary = json.loads(before[safe_path(job["stdout_record"]).as_posix()])
                if actual != summary:
                    raise RuntimeError(f"Replay summary mismatch: {script}")
                generated = safe_path(job["generated_record"]).as_posix()
                actual = json.loads((scratch / generated).read_text())
            wanted = json.loads(before[record])
            # This sole generated field is a source-check execution timestamp.
            # Mathematical values, counts, limits and all other fields must match.
            ignored = job.get("ignored_dynamic_fields", [])
            if ignored not in ([], ["checked_at_utc"]):
                raise RuntimeError("Unsupported replay normalization")
            if ignored and script != "reviews/source01/check_source_bridge.py":
                raise RuntimeError("Timestamp normalization assigned to wrong job")
            for key in ignored:
                if key not in actual or key not in wanted:
                    raise RuntimeError("Missing generated check timestamp")
                actual.pop(key)
                wanted.pop(key)
            if actual != wanted:
                raise RuntimeError(f"Replay mismatch: {script}")
            print(json.dumps({"check": script, "status": "PASS"}))
    if inventory() != before:
        raise RuntimeError("Frozen payload changed during replay")
    print(json.dumps({
        "status": "PASS", "outer_payloads_verified": len(manifest["files"]),
        "nested_entries_verified": nested, "replayed_jobs": len(jobs),
        "offline": True, "frozen_payloads_unchanged": True,
        "limits": "Finite controls supplement analytic proofs. Seals establish "
                  "consistency, not authenticity, novelty or formal certification.",
    }))


if __name__ == "__main__":
    main()
