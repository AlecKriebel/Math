#!/usr/bin/env python3
"""Verify this immutable author freeze using only the Python standard library."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'AUTHOR_MANIFEST.json').read_text())
expected={x['path'] for x in m['files']}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='AUTHOR_MANIFEST.json'}
assert actual==expected,('unexpected or missing files',sorted(actual-expected),sorted(expected-actual))
for x in m['files']:
 b=(root/x['path']).read_bytes()
 assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
assert m['problem_id']==2623 and m['result']=='unresolved_after_five_approaches'
print(json.dumps({'ok':True,'file_count':len(expected),'problem_id':2623,'audit_state':m['independent_audit']},sort_keys=True))
