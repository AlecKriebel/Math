#!/usr/bin/env python3
"""Verify durable family files without mutating any source or result."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "family_manifest.json"
manifest = json.loads(MANIFEST.read_text())
expected = {row["path"]: row for row in manifest["files"]}
failures = []
for rel, row in expected.items():
    path = ROOT / rel
    if not path.is_file():
        failures.append({"path": rel, "reason": "missing"})
        continue
    content = path.read_bytes()
    if len(content) != row["bytes"] or hashlib.sha256(content).hexdigest() != row["sha256"]:
        failures.append({"path": rel, "reason": "size/hash mismatch"})
actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
          if p.is_file() and not any(x in {"tmp", "__pycache__"} for x in p.relative_to(ROOT).parts)
          and p != MANIFEST}
for rel in sorted(actual - expected.keys()):
    failures.append({"path": rel, "reason": "unlisted durable file"})
print(json.dumps({"all_manifest_files_match": not failures,
                  "listed_files": len(expected), "failures": failures}, indent=2))
if failures:
    raise SystemExit(1)
