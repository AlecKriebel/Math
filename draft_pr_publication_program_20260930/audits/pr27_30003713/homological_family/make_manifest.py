#!/usr/bin/env python3
"""Create or verify the self-excluding first-party audit manifest."""
import hashlib
import json
from pathlib import Path
import sys

OWN = Path(__file__).resolve().parent
MANIFEST = OWN / "FIRST_PARTY_SHA256_MANIFEST.json"
excluded_dirs = {"tmp", "__pycache__"}
paths = sorted(p for p in OWN.rglob("*") if p.is_file()
               and p != MANIFEST
               and not any(part in excluded_dirs for part in p.relative_to(OWN).parts))
rows = [{"path": str(p.relative_to(OWN)), "bytes": p.stat().st_size,
         "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
out = {"scope": "All first-party files in this audit directory, recursively; manifest excludes itself, tmp and __pycache__.",
       "self_excluding": True, "files": rows}
if "--check" in sys.argv:
    assert json.loads(MANIFEST.read_text()) == out
    print("Verified", len(rows), "first-party artifacts")
else:
    MANIFEST.write_text(json.dumps(out, indent=2) + "\n")
    print("Manifested", len(rows), "first-party artifacts")
