#!/usr/bin/env python3
"""Verify the exact frozen file set; excludes only MANIFEST.json itself."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'MANIFEST.json').read_text())
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
expected={r['path'] for r in d['files']}
errors=[]
if actual!=expected:
 errors.append({'unexpected':sorted(actual-expected),'missing':sorted(expected-actual)})
for r in d['files']:
 p=root/r['path']
 if not p.is_file():continue
 b=p.read_bytes()
 if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:
  errors.append({'mismatch':r['path']})
print(json.dumps({'status':'FAIL' if errors else 'PASS','file_count':len(expected),'errors':errors},indent=2))
if errors:sys.exit(1)
