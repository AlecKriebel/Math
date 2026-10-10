#!/usr/bin/env python3
"""Check the public-safe package's exact files, sizes, and SHA-256 values."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
manifest=json.loads((root/"MANIFEST.json").read_text())
expected={r["path"] for r in manifest["files"]}|{"MANIFEST.json"}
actual={p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
if expected != actual:
    raise SystemExit("File-set mismatch: "+str(sorted(expected^actual)))
for row in manifest["files"]:
    b=(root/row["path"]).read_bytes()
    if len(b)!=row["bytes"] or hashlib.sha256(b).hexdigest()!=row["sha256"]:
        raise SystemExit("Byte mismatch: "+row["path"])
print(json.dumps({"status":"PASS","files_checked":len(manifest["files"])}))
