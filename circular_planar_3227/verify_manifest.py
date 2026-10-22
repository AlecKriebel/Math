"""Verify sealed payload hashes, byte counts, and exact file membership."""
import hashlib
import json
from pathlib import Path
base=Path(__file__).resolve().parent
manifest=json.loads((base/'MANIFEST.json').read_text())
actual={str(p.relative_to(base)) for p in base.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
expected={r['path'] for r in manifest['files']}
if actual!=expected:
    raise ValueError(f'File set differs: extra={actual-expected}, missing={expected-actual}')
for row in manifest['files']:
    data=(base/row['path']).read_bytes()
    if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
        raise ValueError(f"Mismatch: {row['path']}")
print(f"PASS: {len(expected)} payload files; {sum(r['bytes'] for r in manifest['files'])} bytes.")
