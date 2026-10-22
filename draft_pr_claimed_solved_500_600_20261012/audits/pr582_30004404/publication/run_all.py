#!/usr/bin/env python3
"""Replay all registered exact controls in separate disposable copies."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True
from integrity import safe_path, verify_nested
from verify_original_snapshot import verify

ROOT = Path(__file__).resolve().parent


def inventory():
    result = {}
    for path in ROOT.rglob("*"):
        if path.is_symlink():
            raise RuntimeError(f"Unexpected symlink: {path.relative_to(ROOT)}")
        if path.is_file():
            name = path.relative_to(ROOT).as_posix()
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
    strict = verify(ROOT)
    registry = json.loads(before["SEALS.json"])
    if manifest["nested_seals"] != registry:
        raise RuntimeError("Seal registry mismatch")
    nested, original = verify_nested(before, registry)
    jobs = json.loads(before["JOBS.json"])
    for job in jobs:
        with tempfile.TemporaryDirectory(prefix="zero-filling-replay-") as directory:
            scratch = Path(directory)
            for name, data in before.items():
                path = scratch / safe_path(name)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            script = safe_path(job["script"]).as_posix()
            record = safe_path(job["record"]).as_posix()
            proc = subprocess.run(
                [sys.executable, "-B", str(scratch / script), *job.get("args", [])],
                cwd=(scratch / script).parent,
                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
                capture_output=True, text=True,
            )
            if proc.returncode != 0:
                raise RuntimeError(f"Replay failed: {script}\n{proc.stderr}")
            if "result_file" in job:
                actual = json.loads((scratch / safe_path(job["result_file"])).read_bytes())
            else:
                actual = json.loads(proc.stdout)
            if actual != json.loads(before[record]):
                raise RuntimeError(f"Complete JSON mismatch: {script}")
            print(json.dumps({"job": script, "status": "PASS", "normalized_fields": []}), flush=True)
    if inventory() != before:
        raise RuntimeError("Frozen payloads changed during replay")
    print(json.dumps({"status": "PASS", "outer_payloads_verified": len(manifest["files"]),
                      "nested_entries_verified": nested, "nested_seals": len(registry),
                      "original_inputs_verified": original,
                      "strict_original_gate": strict["status"],
                      "replayed_jobs": len(jobs), "network_access_required": False,
                      "frozen_payloads_unchanged": True,
                      "limits": "Finite controls supplement the universal proof and credited topology; not priority, authenticity, human peer review or formal certification."}))


if __name__ == "__main__":
    main()
