#!/usr/bin/env python3
"""Check this supplement's listed files; audit-manifest authenticity is external."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest_path = root / "AUDIT_MANIFEST.json"
manifest = json.loads(manifest_path.read_bytes())
entries = manifest["files"]
names = [e["path"] for e in entries]
if len(names) != len(set(names)):
    raise ValueError("Duplicate entry")
for name in names:
    p = Path(name)
    if p.is_absolute() or ".." in p.parts or name == manifest_path.name:
        raise ValueError("Invalid entry")
actual = set()
for path in root.rglob("*"):
    if path.is_symlink():
        raise ValueError("Symlink")
    if path.is_file() and path != manifest_path:
        actual.add(path.relative_to(root).as_posix())
if actual != set(names):
    raise ValueError("File-set mismatch")
for entry in entries:
    data = (root / entry["path"]).read_bytes()
    if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
        raise ValueError("Byte mismatch: " + entry["path"])
print(json.dumps({"status": "PASS", "files": len(entries), "scope": "Supplement integrity only; compare the audit-manifest hash to the receipt separately."}, sort_keys=True))
