#!/usr/bin/env python3
"""Verify a frozen packet against an independently supplied manifest SHA-256."""
import argparse
import hashlib
import json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--expected-manifest',required=True)
a=p.parse_args()
root=Path(__file__).resolve().parent
raw=(root/'MANIFEST.json').read_bytes()
digest=hashlib.sha256(raw).hexdigest()
if digest != a.expected_manifest:
    raise SystemExit('FAIL: manifest does not match the independently supplied hash')
m=json.loads(raw)
expected=set(m['files'])
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
if actual != expected | {'MANIFEST.json'}:
    raise SystemExit('FAIL: inventory mismatch')
for name,record in m['files'].items():
    data=(root/name).read_bytes()
    if len(data)!=record['bytes'] or hashlib.sha256(data).hexdigest()!=record['sha256']:
        raise SystemExit('FAIL: '+name)
print(json.dumps({'status':'PASS','files':len(expected),'manifest_sha256':digest},indent=2))
