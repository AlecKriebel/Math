#!/usr/bin/env python3
"""Verify the frozen packet's file set, SHA-256 hashes and byte counts."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / "MANIFEST.json").read_text())
expected = {x["path"] for x in manifest["files"]}
actual = {str(x.relative_to(root)) for x in root.rglob("*")
          if x.is_file() and x.name != "MANIFEST.json"}
assert actual == expected, {"missing": sorted(expected-actual), "extra": sorted(actual-expected)}
for entry in manifest["files"]:
    data = (root / entry["path"]).read_bytes()
    assert len(data) == entry["bytes"], entry["path"]
    assert hashlib.sha256(data).hexdigest() == entry["sha256"], entry["path"]
print(json.dumps({"status": "PASS", "files": len(expected),
                  "scope": "Byte integrity only; not mathematical certification."}, sort_keys=True))
