#!/usr/bin/env python3
"""Validate audit A and its exact author packet; does not prove the theorem."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--author-public", type=Path, default=HERE.parents[1] / "public")
args = parser.parse_args()

def check(path, expected):
    data = path.read_bytes()
    assert len(data) == expected["bytes"], f"Byte count differs: {path.name}"
    assert hashlib.sha256(data).hexdigest() == expected["sha256"], f"Hash differs: {path.name}"

manifest = json.loads((HERE / "MANIFEST.json").read_text())
expected_files = set(manifest["files"])
actual_files = {p.name for p in HERE.iterdir() if p.is_file()} - {"MANIFEST.json"}
assert actual_files == expected_files, "Audit file inventory differs"
for name, metadata in manifest["files"].items():
    assert Path(name).name == name, "Unexpected nested audit entry"
    check(HERE / name, metadata)
acceptance = json.loads((HERE / "ACCEPTANCE.json").read_text())
assert acceptance["verdict"] == "PASS" and not acceptance["blocking_defects"]
check(args.author_public / "PROOF.md", acceptance["frozen_author_proof"])
check(args.author_public / "MANIFEST.json", acceptance["frozen_author_manifest"])
author_manifest = json.loads((args.author_public / "MANIFEST.json").read_text())
for name, metadata in author_manifest["files"].items():
    assert Path(name).name == name, "Unexpected nested author entry"
    check(args.author_public / name, metadata)
check(HERE / acceptance["full_audit"]["file"], acceptance["full_audit"])
check(HERE / acceptance["independent_controls"]["file"], acceptance["independent_controls"])
controls = json.loads((HERE / "INDEPENDENT_CONTROLS.json").read_text())
assert controls["verdict"] == "PASS"
assert controls["control_groups"] == 6 and controls["assertions"] == 63
assert controls["frozen_proof_sha256"] == acceptance["frozen_author_proof"]["sha256"]
assert controls["frozen_manifest_sha256"] == acceptance["frozen_author_manifest"]["sha256"]
assert manifest["frozen_author_proof"] == acceptance["frozen_author_proof"]
assert manifest["frozen_author_manifest"] == acceptance["frozen_author_manifest"]
print(json.dumps({"verdict": "PASS", "audit_files": len(expected_files),
                  "author_files": len(author_manifest["files"]),
                  "frozen_proof_sha256": acceptance["frozen_author_proof"]["sha256"]}, indent=2))
