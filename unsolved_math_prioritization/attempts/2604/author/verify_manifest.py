#!/usr/bin/env python3
"""Verify the frozen authored payload without external or private source files."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'AUTHOR_MANIFEST.json').read_text())
assert m['problem_id']==2604 and not m['original_problem_solved']
expected={r['path']:r for r in m['files']}
actual={p.name for p in ROOT.iterdir() if p.is_file() and p.name!='AUTHOR_MANIFEST.json'}
assert actual==set(expected),(actual,set(expected))
assert all(p.is_file() for p in ROOT.iterdir()),'Unexpected subdirectory'
for name,record in expected.items():
    assert '/' not in name and '\\' not in name
    b=(ROOT/name).read_bytes()
    assert len(b)==record['bytes'],name
    assert hashlib.sha256(b).hexdigest()==record['sha256'],name
print(json.dumps({'status':'PASS','verified_files':len(expected),'problem_solved':False}))
