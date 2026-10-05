#!/usr/bin/env python3
"""Verify exact audit and author-snapshot inventory with SHA-256 and byte counts."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'AUDIT_MANIFEST.json').read_text()); entries=m['files']; expected={'AUDIT_MANIFEST.json'}|{v['path'] for v in entries}
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
if actual!=expected:raise SystemExit('FAIL: inventory mismatch '+repr(sorted(actual^expected)))
for v in entries:
 p=root/v['path']
 if p.is_symlink():raise SystemExit('FAIL: symlink '+v['path'])
 b=p.read_bytes()
 if len(b)!=v['bytes'] or hashlib.sha256(b).hexdigest()!=v['sha256']:raise SystemExit('FAIL: bytes/hash mismatch '+v['path'])
print('PASS: exact audit inventory and all '+str(len(entries))+' file hashes')
