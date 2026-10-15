#!/usr/bin/env python3
"""Verify the retained self-excluding first-party manifest; never writes files."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / "MANIFEST.json").read_text())
assert manifest["self_excluding"] is True
assert "MANIFEST.json" not in [x["path"] for x in manifest["first_party_artifacts"]]
for item in manifest["first_party_artifacts"]:
    b = (root / item["path"]).read_bytes()
    assert len(b) == item["bytes"], item["path"]
    assert hashlib.sha256(b).hexdigest() == item["sha256"], item["path"]
assert (root / "EARLY_PRIMARY_SEAL.md").read_bytes()
seal = json.loads((root / "EARLY_PRIMARY_SEAL.json").read_text())
assert hashlib.sha256((root / seal["file"]).read_bytes()).hexdigest() == seal["sha256"]
assert seal["prior_package_or_sibling_read"] is False
print("PASS: all", len(manifest["first_party_artifacts"]), "retained first-party artifacts and early seal match.")
