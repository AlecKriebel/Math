#!/usr/bin/env python3
"""Verify an externally pinned authored manifest, then rerun exact arithmetic.

Usage: python3 check.py --manifest-sha256 <trusted sha256>
The expected digest must come from outside this directory. No network or raw
paper files are needed. Python 3 and PARI/GP must be installed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--manifest-sha256", required=True)
args = parser.parse_args()
base = Path(__file__).resolve().parent
manifest = base / "artifact_manifest.json"
digest = lambda data: hashlib.sha256(data).hexdigest()
if digest(manifest.read_bytes()) != args.manifest_sha256.lower():
    sys.exit("FAIL: manifest does not match the external pin")
spec = json.loads(manifest.read_text())
for rec in spec["files"]:
    path = Path(rec["path"])
    if path.is_absolute() or ".." in path.parts or path.parts[0] == "raw":
        sys.exit("FAIL: unsafe or raw-source manifest path")
    data = (base / path).read_bytes()
    if len(data) != rec["bytes"] or digest(data) != rec["sha256"]:
        sys.exit(f"FAIL: authored file differs: {path}")
gp = shutil.which("gp")
if not gp:
    sys.exit("FAIL: PARI/GP executable gp is required")
run = subprocess.run(
    [gp, "-q", "-f", str(base / "arithmetic.gp")],
    text=True,
    capture_output=True,
    timeout=180,
)
print(run.stdout, end="")
if run.returncode or "***" in run.stderr or "AUDIT_OK" not in run.stdout:
    print(run.stderr, file=sys.stderr)
    sys.exit("FAIL: exact arithmetic did not complete")
print(f"PINNED_AUTHORED_ARTIFACTS_OK {args.manifest_sha256.lower()}")
