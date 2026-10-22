#!/usr/bin/env python3
"""Check the complete audit file set without network access or file changes."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root / "AUDIT_MANIFEST.json").read_text())
expected = {"AUDIT_MANIFEST.json"}
for entry in manifest["files"]:
    name = entry["path"]
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts or name in expected:
        raise ValueError("Invalid or duplicate manifest path")
    expected.add(name)
    path = root / relative
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root):
        raise ValueError("Unsafe or absent file: " + name)
    content = path.read_bytes()
    if len(content) != entry["bytes"] or hashlib.sha256(content).hexdigest() != entry["sha256"]:
        raise ValueError("Integrity mismatch: " + name)
actual = set()
for path in root.rglob("*"):
    if path.is_symlink():
        raise ValueError("Symlink in audit")
    if path.is_file():
        actual.add(path.relative_to(root).as_posix())
if actual != expected:
    raise ValueError("Audit file set differs from manifest")
print(json.dumps({"status": "PASS", "audit_files": len(actual), "hashes": "all matched"}, sort_keys=True))
