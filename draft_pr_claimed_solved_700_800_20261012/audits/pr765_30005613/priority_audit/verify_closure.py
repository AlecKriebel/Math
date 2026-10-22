#!/usr/bin/env python3
"""Read-only verification of the closed recursive authored-file manifest."""
from pathlib import Path
import hashlib
import json
import sys

root = Path(__file__).resolve().parent
manifest_path = root / "MANIFEST.json"
data = json.loads(manifest_path.read_text())
expected = data["files"]
if len({row["path"] for row in expected}) != len(expected):
    raise SystemExit("FAIL: duplicate manifest entry")
actual = {}
for path in root.rglob("*"):
    if path.is_symlink():
        raise SystemExit("FAIL: unexpected symlink: " + str(path))
    if path.is_file() and path != manifest_path:
        actual[path.relative_to(root).as_posix()] = path
if set(actual) != {row["path"] for row in expected}:
    raise SystemExit("FAIL: recursive file set differs, including hidden files")
for row in expected:
    path = actual[row["path"]]
    body = path.read_bytes()
    if len(body) != row["bytes"] or hashlib.sha256(body).hexdigest() != row["sha256"]:
        raise SystemExit("FAIL: bytes/hash mismatch: " + row["path"])
verdict = json.loads((root / "VERDICT.json").read_text())
if not verdict["closed"] or not verdict["audit_complete"]:
    raise SystemExit("FAIL: audit is not closed")
print(json.dumps({
    "result": "PASS",
    "authored_regular_files_excluding_manifest": len(expected),
    "hidden_files_included": True,
    "unexpected_files": [],
    "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
    "verdict_sha256": hashlib.sha256((root / "VERDICT.json").read_bytes()).hexdigest(),
    "report_sha256": hashlib.sha256((root / "REPORT.md").read_bytes()).hexdigest()
}, indent=2))
