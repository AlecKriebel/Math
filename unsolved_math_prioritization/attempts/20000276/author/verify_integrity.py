#!/usr/bin/env python3
"""Verify the exact authored packet without network or third-party packages."""
from pathlib import Path
import hashlib
import json
base=Path(__file__).resolve().parent
manifest=json.loads((base/'AUTHOR_MANIFEST.json').read_text())
expected={x['path'] for x in manifest['files']}
actual={str(x.relative_to(base)) for x in base.rglob('*') if x.is_file() and x.name!='AUTHOR_MANIFEST.json'}
assert actual==expected, {'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
for rec in manifest['files']:
    b=(base/rec['path']).read_bytes()
    assert len(b)==rec['bytes'],rec['path']
    assert hashlib.sha256(b).hexdigest()==rec['sha256'],rec['path']
print(json.dumps({'status':'PASS','verified_files':len(expected),'problem_id':manifest['problem_id']},sort_keys=True))
