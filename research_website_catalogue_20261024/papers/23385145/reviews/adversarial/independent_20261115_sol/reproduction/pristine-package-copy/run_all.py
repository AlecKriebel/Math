#!/usr/bin/env python3
"""Replay every registered finite control offline, preserving frozen payloads."""
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
CLOCK_FIELDS = ["started_at_utc", "completed_at_utc", "elapsed_seconds"]


def inventory():
    result = {}
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if "__pycache__" in rel.parts or ".venv" in rel.parts:
            continue
        if path.is_symlink():
            raise RuntimeError(f"Unexpected symlink: {rel}")
        if path.is_file():
            name = rel.as_posix()
            safe_path(name)
            result[name] = path.read_bytes()
    return result


def main():
    if not __debug__ or os.environ.get("PYTHONOPTIMIZE"):
        raise RuntimeError("Run with assertions enabled, without PYTHONOPTIMIZE")
    before = inventory()
    manifest = json.loads(before["MANIFEST.json"])
    if set(before) != set(manifest["files"]) | {"MANIFEST.json"}:
        raise RuntimeError("Outer payload inventory mismatch")
    for name, record in manifest["files"].items():
        safe_path(name)
        data = before[name]
        if len(data) != record["bytes"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise RuntimeError(f"Outer payload mismatch: {name}")
    registry = json.loads(before["SEALS.json"])
    if manifest["nested_seals"] != registry:
        raise RuntimeError("Seal registry mismatch")
    nested, original = verify_nested(before, registry)
    jobs = json.loads(before["JOBS.json"])
    for job in jobs:
        # Every script gets its own fresh copy. Generated control records never
        # become an input for a later job or change a sealed expected record.
        with tempfile.TemporaryDirectory(prefix="weighted-center-replay-") as directory:
            scratch = Path(directory)
            for folder in ("original", "reviews"):
                shutil.copytree(ROOT / folder, scratch / folder)
            script = safe_path(job["script"]).as_posix()
            record = safe_path(job["record"]).as_posix()
            proc = subprocess.run(
                [sys.executable, str(scratch / script)],
                cwd=(scratch / script).parent,
                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
                capture_output=True, text=True,
            )
            if proc.returncode != 0:
                raise RuntimeError(f"Replay failed: {script}\n{proc.stderr}")
            actual = json.loads(proc.stdout)
            wanted = json.loads(before[record])
            ignored = job.get("ignored_clock_fields", [])
            if ignored:
                if script != "reviews/oracle01/controls.py" or ignored != CLOCK_FIELDS:
                    raise RuntimeError("Unsupported replay normalization")
                for field in CLOCK_FIELDS:
                    if field not in actual or field not in wanted:
                        raise RuntimeError("Missing expected clock field")
                    actual.pop(field)
                    wanted.pop(field)
            if actual != wanted:
                raise RuntimeError(f"Complete mathematical JSON mismatch: {script}")
            print(json.dumps({"job": script, "status": "PASS", "ignored_clock_fields": ignored}), flush=True)
    if inventory() != before:
        raise RuntimeError("Frozen payloads changed during replay")
    print(json.dumps({"status": "PASS", "outer_payloads_verified": len(manifest["files"]),
                      "nested_entries_verified": nested, "original_inputs_verified": original,
                      "replayed_jobs": len(jobs), "offline": True,
                      "frozen_payloads_unchanged": True,
                      "limits": "Finite controls supplement proofs; no fast BDH implementation, runtime benchmark, historical-first or formal/human certification."}))


if __name__ == "__main__":
    main()
