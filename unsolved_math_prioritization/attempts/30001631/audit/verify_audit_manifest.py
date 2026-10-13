#!/usr/bin/env python3
"""Read-only verification of this audit's exact public-file allowlist."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
manifest=json.loads((root/"MANIFEST.json").read_bytes())
expected={row["path"]:row for row in manifest["files"]}
actual={p.name for p in root.iterdir()}
if actual != set(expected)|{"MANIFEST.json"}:
    raise AssertionError("Audit allowlist differs")
for path in root.iterdir():
    if not path.is_file() or path.is_symlink():
        raise AssertionError("Unexpected directory or symlink")
for name,row in expected.items():
    data=(root/name).read_bytes()
    if len(data)!=row["bytes"] or hashlib.sha256(data).hexdigest()!=row["sha256"]:
        raise AssertionError(name)
print(json.dumps({"passed":True,"files_verified":len(expected),"manifest_self_excluded":True},sort_keys=True))
