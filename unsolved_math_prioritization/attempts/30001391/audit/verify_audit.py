#!/usr/bin/env python3
"""Portable byte-integrity check, not a mathematical proof checker."""
from pathlib import Path
import hashlib, json, sys
p=Path(__file__).resolve().parent
j=json.loads((p/'AUDIT_MANIFEST.json').read_text())
errors=[]
files=j['files']
actual={str(x.relative_to(p)) for x in p.rglob('*') if x.is_file() and x.name!='AUDIT_MANIFEST.json' and '__pycache__' not in x.parts}
if actual!=set(files): errors.append({'audit_missing':sorted(set(files)-actual),'audit_extra':sorted(actual-set(files))})
for n,r in files.items():
    if not (p/n).exists(): continue
    b=(p/n).read_bytes()
    if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']: errors.append({'audit_mismatch':n})
submission=Path(sys.argv[1]) if len(sys.argv)>1 else p.parent/'submission'
m=submission/'SHA256SUMS.json'
if not m.is_file(): errors.append({'author_manifest_unavailable':str(m)})
else:
    b=m.read_bytes()
    if hashlib.sha256(b).hexdigest()!=j['audited_author_manifest']['sha256']: errors.append('author_manifest_sha256_mismatch')
    author=json.loads(b)
    expected=set(author['files'])
    actual={str(x.relative_to(submission)) for x in submission.rglob('*') if x.is_file() and x.name!='SHA256SUMS.json' and '__pycache__' not in x.parts}
    if expected!=actual: errors.append({'author_missing':sorted(expected-actual),'author_extra':sorted(actual-expected)})
    for n,r in author['files'].items():
        if not (submission/n).is_file(): continue
        b=(submission/n).read_bytes()
        if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']: errors.append({'author_mismatch':n})
print(json.dumps({'result':'PASS' if not errors else 'FAIL','audit_file_count':len(files),'author_manifest_sha256':j['audited_author_manifest']['sha256'],'errors':errors,'limits':'Byte integrity only; no mathematical correctness, scope, or novelty certification.'},indent=2))
sys.exit(bool(errors))
