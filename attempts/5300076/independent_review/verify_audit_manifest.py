#!/usr/bin/env python3
"""Check the complete public audit allowlist and each artifact's bytes."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
expected={e['path'] for e in manifest['files']}|{'AUDIT_MANIFEST.json'}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual==expected,('Audit inventory mismatch',sorted(actual^expected))
for e in manifest['files']:
    p=Path(e['path'])
    assert not p.is_absolute() and '..' not in p.parts
    data=(root/p).read_bytes()
    assert len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256'],str(p)
print(f"PASS: {len(manifest['files'])} bound audit artifacts")
