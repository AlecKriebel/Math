#!/usr/bin/env python3
"""Read-only exact-allowlist verification for this audit bundle."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
expected=set(manifest['files'])|{'AUDIT_MANIFEST.json'}
assert set(p.name for p in root.iterdir())==expected, 'Unexpected or missing audit artifact'
for name,want in manifest['files'].items():
    path=root/name
    assert path.is_file() and not path.is_symlink(), name
    data=path.read_bytes()
    got={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    assert got==want, (name,got,want)
print(json.dumps({'status':'PASS','files_checked':len(manifest['files']),
                  'manifest_sha256':hashlib.sha256((root/'AUDIT_MANIFEST.json').read_bytes()).hexdigest()}))
