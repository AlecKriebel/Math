#!/usr/bin/env python3
"""Verify this audit's closed top-level allowlist and file hashes, read-only."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
p=root/'AUDIT_SHA256SUMS.json'
if p.is_symlink() or not p.is_file():raise SystemExit('Invalid audit manifest')
m=json.loads(p.read_bytes());files=m['files'];expected=set(files)|{'AUDIT_SHA256SUMS.json'}
entries=list(root.iterdir())
if any(x.is_symlink() or not x.is_file() for x in entries):raise SystemExit('Unexpected non-regular entry')
if {x.name for x in entries}!=expected:raise SystemExit('Unexpected/missing audit entries')
for name,meta in files.items():
 if Path(name).name!=name or name in ('','.','..'):raise SystemExit('Invalid filename')
 b=(root/name).read_bytes()
 if len(b)!=meta['bytes'] or hashlib.sha256(b).hexdigest()!=meta['sha256']:raise SystemExit('Audit integrity mismatch: '+name)
print(json.dumps({'verified_files':len(files),'audit_manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'frozen_author_binding':m['frozen_author_binding']},sort_keys=True))
