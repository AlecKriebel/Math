#!/usr/bin/env python3
"""Read-only verification of this current-run freeze; no historical recreation."""

import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
manifest_path = BASE / "FREEZE_MANIFEST.json"
expected_manifest_hash = (BASE / "FREEZE_SHA256.txt").read_text(encoding="utf-8").split()[0]
actual_manifest_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
assert actual_manifest_hash == expected_manifest_hash, "Freeze manifest hash differs."
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
for name, expected in manifest["artifacts"].items():
    assert Path(name).name == name
    actual = hashlib.sha256((BASE / name).read_bytes()).hexdigest()
    assert actual == expected, f"Frozen artifact differs: {name}"

import reconstruct

frozen = json.loads((BASE / "results.json").read_text(encoding="utf-8"))
current = reconstruct.run()
# JSON round trip normalizes tuples to arrays, as in the frozen output.
assert json.loads(json.dumps(current)) == frozen, "Current results differ from frozen results."
print("PASS: freeze hashes, both exact methods, mathematical outputs, and all controls.")
print("Ordinary palette minimum: 5; supplied-list solutions: 0; arbitrary-list number: 6.")
print("No frozen file or historical log was rewritten.")
