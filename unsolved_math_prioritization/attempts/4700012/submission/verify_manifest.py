#!/usr/bin/env python3
"""Check the exact frozen allowlist and every listed file's bytes."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
expected=set(manifest['files']) | {'SHA256SUMS.json'}
actual={p.name for p in root.iterdir() if p.is_file()}
if expected != actual:
    raise SystemExit('File allowlist mismatch')
for name, entry in manifest['files'].items():
    b=(root/name).read_bytes()
    if len(b)!=entry['bytes'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:
        raise SystemExit('Hash or length mismatch: '+name)
print(json.dumps({'manifest_verified':True,'files_checked':len(manifest['files'])},sort_keys=True))
