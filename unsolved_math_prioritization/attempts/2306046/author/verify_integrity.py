#!/usr/bin/env python3
"""Validate the exact frozen author inventory and bytes, not mathematical truth."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent
MANIFEST='AUTHOR_MANIFEST.json'

def verify():
    m=json.loads((ROOT/MANIFEST).read_text())
    records=m['files']
    expected={x['path'] for x in records}|{MANIFEST}
    if len(expected)!=len(records)+1: raise AssertionError('duplicate manifest path')
    actual={str(x.relative_to(ROOT)) for x in ROOT.rglob('*') if x.is_file() or x.is_symlink()}
    if actual!=expected: raise AssertionError({'missing':sorted(expected-actual),'extra':sorted(actual-expected)})
    for x in records:
        name=x['path']
        if '/' in name or '\\' in name or name.startswith('.'): raise AssertionError('invalid publication path')
        p=ROOT/name
        if p.is_symlink(): raise AssertionError('symlinks excluded')
        b=p.read_bytes()
        if len(b)!=x['bytes'] or hashlib.sha256(b).hexdigest()!=x['sha256']:
            raise AssertionError('changed file: '+name)
    return {'all_passed':True,'author_files_including_manifest':len(expected),'bytes_verified_excluding_manifest':sum(x['bytes'] for x in records),'scope':'inventory and hashes only; no theorem validation'}

if __name__=='__main__': print(json.dumps(verify(),indent=2,sort_keys=True))
