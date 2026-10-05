#!/usr/bin/env python3
"""Verify the safe file manifest and replay elementary controls offline."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

base = Path(__file__).resolve().parent
manifest = json.loads((base / "AUTHOR_MANIFEST.json").read_text())
expected = set(manifest["files"])
actual = {p.name for p in base.iterdir() if p.is_file()}
assert actual == expected | {"AUTHOR_MANIFEST.json"}, (actual, expected)
for name, metadata in manifest["files"].items():
    data = (base / name).read_bytes()
    assert len(data) == metadata["bytes"], name
    assert hashlib.sha256(data).hexdigest() == metadata["sha256"], name
run = subprocess.run([sys.executable, str(base / "controls.py")],
                     check=True, capture_output=True, text=True)
assert run.stdout == (base / "CHECK_RESULTS.json").read_text()
print(json.dumps({"manifest": "PASS", "files_verified": len(expected),
                  "exact_replay": "PASS", "independent_audit": False},
                 sort_keys=True))
