#!/usr/bin/env python3
"""Strict byte/hash verification of the frozen authored payload."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / "AUTHOR_MANIFEST.json").read_text())
expected = {item["path"] for item in manifest["files"]}
actual = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()
          and p.name != "AUTHOR_MANIFEST.json" and "__pycache__" not in p.parts}
if actual != expected:
    raise RuntimeError({"missing": sorted(expected-actual), "extra": sorted(actual-expected)})
for item in manifest["files"]:
    p = root / item["path"]
    if p.is_symlink() or not p.resolve().is_relative_to(root):
        raise RuntimeError("Unsafe manifest path: " + item["path"])
    data = p.read_bytes()
    if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
        raise RuntimeError("Byte/hash mismatch: " + item["path"])
print(json.dumps({"status": "PASS", "verified_files": len(expected),
                  "manifest_sha256": hashlib.sha256((root/"AUTHOR_MANIFEST.json").read_bytes()).hexdigest()},
                 sort_keys=True))
