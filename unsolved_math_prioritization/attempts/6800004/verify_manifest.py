#!/usr/bin/env python3
"""Verify this portable publication packet, using only the standard library."""
import hashlib, json
from pathlib import Path
root = Path(__file__).resolve().parent
manifest = json.loads((root / "MANIFEST.json").read_text())
expected = {"MANIFEST.json"} | {item["path"] for item in manifest["files"]}
actual = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
assert expected == actual, (expected - actual, actual - expected)
for item in manifest["files"]:
    data = (root / item["path"]).read_bytes()
    assert len(data) == item["bytes"], item["path"]
    assert hashlib.sha256(data).hexdigest() == item["sha256"], item["path"]
assert (root / "turns.jsonl").read_bytes() == b""
assert manifest["original_turns_used"] == 0
assert manifest["independent_review_status"] == "PASS"
print("PASS: exact file set, all SHA-256 hashes, empty 0/5 ledger, audit PASS")
