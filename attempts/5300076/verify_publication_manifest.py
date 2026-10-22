#!/usr/bin/env python3
"""Reject changed, missing, or unlisted files in the complete public packet."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'PUBLICATION_MANIFEST.json').read_text())
expected={x['path'] for x in m['files']}|{'PUBLICATION_MANIFEST.json'}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual==expected,('Inventory mismatch',sorted(actual^expected))
for e in m['files']:
    p=Path(e['path'])
    assert not p.is_absolute() and '..' not in p.parts
    b=(root/p).read_bytes()
    assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],str(p)
print(f"PASS: {len(m['files'])} bound publication artifacts")
