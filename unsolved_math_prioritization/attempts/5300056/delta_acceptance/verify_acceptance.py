#!/usr/bin/env python3
"""Verify only the included acceptance packet; omitted archives are not replayed."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={e['path']:e for e in manifest['files']}
actual={p.name:p for p in root.iterdir() if p.is_file() and p.name!='MANIFEST.json'}
if len(expected)!=len(manifest['files']) or set(actual)!=set(expected):raise AssertionError('Closed file-set mismatch')
for p in root.iterdir():
    if p.is_symlink() or not p.is_file():raise AssertionError('Unexpected directory or symlink')
for name,p in actual.items():
    if p.suffix not in {'.md','.json','.py','.patch'}:raise AssertionError('Forbidden extension')
    b=p.read_bytes();e=expected[name]
    if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise AssertionError('Hash mismatch: '+name)
print(json.dumps({'status':'PASS','checked_files':len(actual),'scope':'Acceptance packet integrity only; use verify_delta.py with all three input archives for full delta and relocated arithmetic replay.'},sort_keys=True))
