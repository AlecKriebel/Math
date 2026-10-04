#!/usr/bin/env python3
"""Verify exact allowlist and hashes. No file or network mutation."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / "SHA256SUMS.json").read_text())
expected = set(manifest["files"]) | {"SHA256SUMS.json"}
actual = {p.name for p in root.iterdir() if p.is_file()}
assert actual == expected, {"missing": sorted(expected-actual),
                            "unexpected": sorted(actual-expected)}
assert not any(p.is_dir() or p.is_symlink() for p in root.iterdir())
for name, digest in manifest["files"].items():
    assert "/" not in name and "\\" not in name
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
print(json.dumps({"manifest_passed": True, "files": len(manifest["files"]),
                  "target_solved": False}, sort_keys=True))
