#!/usr/bin/env python3
"""Verify the exact independent audit package and optional independent replay."""
import hashlib,json
from pathlib import Path
r=Path(__file__).resolve().parent
m=json.loads((r/'AUDIT_MANIFEST.json').read_text())
expected={f['path']:f for f in m['files']}
actual={str(f.relative_to(r)) for f in r.rglob('*') if f.is_file() and f.name!='AUDIT_MANIFEST.json'}
assert actual==set(expected),(actual-set(expected),set(expected)-actual)
for n,f in expected.items():
 b=(r/n).read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],n
print(json.dumps({'status':'PASS','files_verified':len(expected),'verdict':m['verdict'],'full_original_problem_solved':False},indent=2))
