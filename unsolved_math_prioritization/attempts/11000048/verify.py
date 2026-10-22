#!/usr/bin/env python3
"""Verify exact frozen author and independent audit artifacts without network access."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / "PUBLICATION_MANIFEST.json").read_text())
for name, expected in manifest["sha256"].items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
assert hashlib.sha256((root / "package/MANIFEST.json").read_bytes()).hexdigest() == manifest["frozen_author_manifest_sha256"]
audit = json.loads((root / "audit-independent/AUDIT_MANIFEST.json").read_text())
assert audit["input_manifest_sha256"] == manifest["frozen_author_manifest_sha256"]
for name, expected in audit["files"].items():
    assert hashlib.sha256((root / "audit-independent" / name).read_bytes()).hexdigest() == expected, name
result = json.loads((root / "audit-independent/AUDIT_RESULTS.json").read_text())
assert result["verdict"] == "PASS" and result["substantive_author_turns"] == 0
subprocess.run([sys.executable, str(root / "package/verify.py")], check=True)
print(json.dumps({"publication_integrity": "pass", "bound_files": len(manifest["sha256"]),
                  "outcome": "already_solved", "turns": "0/5",
                  "audit": "PASS, with limitations in the audit report"}, indent=2))
