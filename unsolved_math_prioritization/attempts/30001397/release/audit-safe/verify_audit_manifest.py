#!/usr/bin/env python3
"""Verify the exact portable audit payload inventory and SHA-256 fingerprints."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / "MANIFEST.json").read_text())
expected = {entry["path"] for entry in manifest["files"]}
actual = {path.name for path in root.iterdir()
          if path.is_file() and path.name != "MANIFEST.json"}
if expected != actual:
    raise AssertionError({"missing": sorted(expected-actual), "extra": sorted(actual-expected)})
for entry in manifest["files"]:
    path = Path(entry["path"])
    if path.name != str(path):
        raise ValueError("Only flat payload paths are permitted")
    data = (root / path).read_bytes()
    if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
        raise AssertionError(str(path))
print(json.dumps({"passed": True, "files_checked": len(expected)}, sort_keys=True))
