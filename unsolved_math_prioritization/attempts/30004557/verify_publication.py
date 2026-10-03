#!/usr/bin/env python3
"""Verify publication bytes and replay finite formula controls; no network."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / "AUTHOR_MANIFEST.json").read_text())
for entry in manifest["files"]:
    relative = Path(entry["path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise SystemExit("Unsafe manifest path")
    data = (root / relative).read_bytes()
    if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
        raise SystemExit("Manifest mismatch: " + entry["path"])
actual = json.loads(subprocess.check_output([sys.executable, str(root / "verify_matrix_controls.py")], text=True, cwd=root))
expected = json.loads((root / "MATRIX_CONTROLS.json").read_text())
if actual != expected:
    raise SystemExit("Finite controls differ from recorded output")
print(json.dumps({"status": "PASS", "manifest_files": len(manifest["files"]), "finite_controls": actual["total"], "scope": "File integrity and finite-set formula checks; not a proof of constructive metatheory"}, indent=2))
