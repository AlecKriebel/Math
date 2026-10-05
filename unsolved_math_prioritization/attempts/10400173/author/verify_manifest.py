#!/usr/bin/env python3
"""Verify the exact closed allowlist and bytes of this authored packet."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
files=manifest['files']
expected=set(files)|{'SHA256SUMS.json'}
actual={x.name for x in root.iterdir() if x.is_file()}
if actual!=expected:
    raise SystemExit('Unexpected/missing files: '+repr(sorted(actual^expected)))
for name,meta in files.items():
    p=root/name
    if p.is_symlink() or p.name!=name or not p.is_file():raise SystemExit('Invalid file: '+name)
    b=p.read_bytes()
    if len(b)!=meta['bytes'] or hashlib.sha256(b).hexdigest()!=meta['sha256']:
        raise SystemExit('Integrity mismatch: '+name)
print(json.dumps({'verified_files':len(files),'manifest_sha256':hashlib.sha256((root/'SHA256SUMS.json').read_bytes()).hexdigest()},sort_keys=True))
