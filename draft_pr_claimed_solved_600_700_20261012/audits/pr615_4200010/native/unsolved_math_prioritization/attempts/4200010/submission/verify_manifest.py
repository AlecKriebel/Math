#!/usr/bin/env python3
"""Verify the exact allowlisted release inventory and SHA-256 metadata."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={x['path']:x for x in manifest['files']}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual==set(expected)|{'MANIFEST.json'},(actual,set(expected))
for name,row in expected.items():
    p=root/name
    assert not p.is_symlink(),name
    data=p.read_bytes()
    assert len(data)==row['bytes'],name
    assert hashlib.sha256(data).hexdigest()==row['sha256'],name
print(json.dumps({'result':'PASS','verified_files':len(expected),'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()},sort_keys=True))
