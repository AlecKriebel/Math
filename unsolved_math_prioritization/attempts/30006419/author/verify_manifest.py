#!/usr/bin/env python3
"""Verify a strictly inventoried author freeze against an external digest."""
import argparse
import hashlib
import json
from pathlib import Path

def fail(s): raise SystemExit(s)
p=argparse.ArgumentParser();p.add_argument('--expected-manifest-sha256',required=True);a=p.parse_args()
root=Path(__file__).resolve().parent
mp=root/'MANIFEST.json'
if mp.is_symlink() or not mp.is_file(): fail('Invalid manifest path')
data=mp.read_bytes()
if hashlib.sha256(data).hexdigest()!=a.expected_manifest_sha256: fail('External manifest digest mismatch')
m=json.loads(data)
expected=set(m['files'])|{'MANIFEST.json'}
actual={q.name for q in root.iterdir()}
if actual != expected: fail('Inventory mismatch')
for name,record in m['files'].items():
    if name!=Path(name).name or name in ('','.', '..'): fail('Unsafe filename')
    q=root/name
    if q.is_symlink() or not q.is_file(): fail('Nonregular file: '+name)
    b=q.read_bytes()
    if len(b)!=record['bytes'] or hashlib.sha256(b).hexdigest()!=record['sha256']: fail('Content mismatch: '+name)
print(json.dumps({'status':'PASS','files_verified':len(m['files']),'manifest_sha256':a.expected_manifest_sha256},sort_keys=True))
