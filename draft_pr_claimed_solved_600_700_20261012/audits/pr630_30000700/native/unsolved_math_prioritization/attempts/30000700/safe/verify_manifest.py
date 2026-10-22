#!/usr/bin/env python3
"""Validate all frozen safe-packet members, rejecting unexpected files."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text())
expected={x['path'] for x in m['files']}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
assert actual==expected,{'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}
for x in m['files']:
    b=(root/x['path']).read_bytes()
    assert len(b)==x['bytes'],x['path']
    assert hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
print(json.dumps({'status':'PASS','files':len(expected),'total_bytes':sum(x['bytes'] for x in m['files'])},sort_keys=True))
