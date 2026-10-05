#!/usr/bin/env python3
"""Verify the audit's inventory and hashes. Optional external manifest anchor."""
import argparse
import hashlib
import json
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--expected-manifest-sha256')
a=ap.parse_args()
root=Path(__file__).resolve().parent
p=root/'MANIFEST.json'
if p.is_symlink():
    raise SystemExit('FAIL: symlink manifest')
b=p.read_bytes()
actual_hash=hashlib.sha256(b).hexdigest()
if a.expected_manifest_sha256 and actual_hash!=a.expected_manifest_sha256:
    raise SystemExit('FAIL: external manifest anchor')
m=json.loads(b)
if m.get('schema')!='erdos-2235-independent-audit-manifest-v1':
    raise SystemExit('FAIL: schema')
names=[e['path'] for e in m['files']]
if len(names)!=len(set(names)) or any(Path(n).name!=n for n in names):
    raise SystemExit('FAIL: unsafe or duplicate path')
if {x.name for x in root.iterdir()} != set(names)|{'MANIFEST.json'}:
    raise SystemExit('FAIL: inventory')
for e in m['files']:
    x=root/e['path']
    if x.is_symlink() or not x.is_file():
        raise SystemExit('FAIL: unsafe file')
    data=x.read_bytes()
    if len(data)!=e['bytes'] or hashlib.sha256(data).hexdigest()!=e['sha256']:
        raise SystemExit('FAIL: payload '+e['path'])
print(json.dumps({'status':'PASS','files':len(names)+1,
 'manifest_sha256':actual_hash,'external_anchor_checked':bool(a.expected_manifest_sha256)},
 indent=2,sort_keys=True))
