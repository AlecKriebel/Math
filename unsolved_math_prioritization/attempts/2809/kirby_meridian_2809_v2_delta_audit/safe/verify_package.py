#!/usr/bin/env python3
import hashlib,json
from pathlib import Path

def need(x,s):
    if not x:raise RuntimeError(s)
root=Path(__file__).resolve().parent
paths=list(root.rglob('*'));need(not any(p.is_symlink() for p in paths),'Symlink')
actual={p.relative_to(root).as_posix():p for p in paths if p.is_file() and p.relative_to(root).as_posix()!='MANIFEST.json'}
entries=json.loads((root/'MANIFEST.json').read_text())['files']
need(len(entries)==len({e['path'] for e in entries}),'Duplicate entry')
need(set(actual)=={e['path'] for e in entries},'Membership mismatch')
for e in entries:
    b=actual[e['path']].read_bytes();need(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'Hash mismatch: '+e['path'])
print('PASS: exact C1 v2 delta-acceptance packet manifest')
