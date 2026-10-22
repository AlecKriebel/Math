#!/usr/bin/env python3
"""Verify this review's authored-file seal. Standard library only."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root/"MANIFEST.json").read_text())
checks = []
for item in manifest["authored_files"]:
    path = root/item["path"]
    if path.parent != root or not path.is_file():
        raise AssertionError("nonlocal or missing authored file: " + item["path"])
    data = path.read_bytes()
    if len(data) != item["size_bytes"]:
        raise AssertionError("size mismatch: " + item["path"])
    if hashlib.sha256(data).hexdigest() != item["sha256"]:
        raise AssertionError("hash mismatch: " + item["path"])
    checks.append(item["path"])
expected = {i["path"] for i in manifest["authored_files"]} | {"MANIFEST.json"}
actual = {p.name for p in root.iterdir() if p.is_file()}
if actual != expected:
    raise AssertionError("unsealed or missing file: " + str(sorted(actual ^ expected)))
print(json.dumps({"status": "passed", "verified_authored_files": len(checks),
                  "files": checks, "manifest_self_hash_excluded": True}, indent=2))
