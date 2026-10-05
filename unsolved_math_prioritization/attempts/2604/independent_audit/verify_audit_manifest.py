#!/usr/bin/env python3
"""Verify the complete flat independent-audit payload without rewriting files."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
assert manifest['problem_id']==2604 and manifest['original_problem_solved'] is False
expected={r['path']:r for r in manifest['files']}
assert all(p.is_file() for p in root.iterdir()),'Unexpected directory'
actual={p.name for p in root.iterdir() if p.name!='AUDIT_MANIFEST.json'}
assert actual==set(expected),(actual,set(expected))
for name,r in expected.items():
    assert '/' not in name and '\\' not in name
    b=(root/name).read_bytes()
    assert len(b)==r['bytes'],name
    assert hashlib.sha256(b).hexdigest()==r['sha256'],name
print(json.dumps({'status':'PASS','verified_files':len(expected),'problem_solved':False}))
