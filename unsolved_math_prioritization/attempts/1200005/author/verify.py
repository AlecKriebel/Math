#!/usr/bin/env python3
"""Verify the sealed safe packet and replay its exact controls offline."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

if sys.flags.optimize:
    raise SystemExit("Run without -O: exact controls use assertions.")
root = Path(__file__).resolve().parent
manifest = json.loads((root / "MANIFEST.json").read_text())
allowed = set(manifest["files"]) | {"MANIFEST.json"}
actual = {p.name for p in root.iterdir() if p.is_file()}
if actual != allowed:
    raise SystemExit(f"File allowlist mismatch: {actual ^ allowed}")
unexpected_dirs = [p.name for p in root.iterdir()
                   if p.is_dir() and p.name != "__pycache__"]
if unexpected_dirs:
    raise SystemExit(f"Unexpected directories: {unexpected_dirs}")
for name, info in manifest["files"].items():
    p = root / name
    if p.is_symlink():
        raise SystemExit(f"Symlink forbidden: {name}")
    data = p.read_bytes()
    if len(data) != info["bytes"] or hashlib.sha256(data).hexdigest() != info["sha256"]:
        raise SystemExit(f"Binding mismatch: {name}")
proc = subprocess.run([sys.executable, "-B", str(root / "controls.py")],
                      cwd=root, check=True, capture_output=True)
expected = (root / "CONTROL_RESULTS.json").read_bytes()
if proc.stdout != expected:
    raise SystemExit("Control output differs from the frozen result.")
print(json.dumps({"status": "PASS", "bound_files": len(manifest["files"]),
                  "exact_control_bytes": len(expected),
                  "control_sha256": hashlib.sha256(expected).hexdigest()}, sort_keys=True))
