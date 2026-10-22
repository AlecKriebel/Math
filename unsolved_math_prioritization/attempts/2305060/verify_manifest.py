#!/usr/bin/env python3
"""Verify exact frozen public-file names, byte counts and SHA-256 hashes."""
import hashlib,json,pathlib,sys
root=pathlib.Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
actual={p.name for p in root.iterdir() if p.is_file() and p.name!='SHA256SUMS.json'}
expected=set(manifest['files'])
errors=[]
if actual!=expected:errors.append({'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)})
for name,meta in manifest['files'].items():
 p=root/name
 if not p.exists():continue
 b=p.read_bytes()
 if hashlib.sha256(b).hexdigest()!=meta['sha256'] or len(b)!=meta['bytes']:errors.append({'changed':name})
print(json.dumps({'result':'PASS' if not errors else 'FAIL','file_count':len(expected),'errors':errors},indent=2))
sys.exit(bool(errors))
