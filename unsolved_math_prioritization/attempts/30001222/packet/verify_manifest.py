#!/usr/bin/env python3
"""Check the frozen packet's byte-count and SHA-256 inventory."""
import hashlib
import json
from pathlib import Path

p=Path(__file__).resolve().parent
m=json.loads((p/'MANIFEST.json').read_text())
expected={r['path']:r for r in m['files']}
actual={str(f.relative_to(p)) for f in p.rglob('*') if f.is_file() and f.name!='MANIFEST.json' and '__pycache__' not in f.parts}
assert actual==set(expected), ('file set mismatch',sorted(actual^set(expected)))
for rel,record in expected.items():
    b=(p/rel).read_bytes()
    assert len(b)==record['bytes'], ('byte count',rel)
    assert hashlib.sha256(b).hexdigest()==record['sha256'], ('SHA-256',rel)
print(json.dumps({'status':'PASS','files_checked':len(expected)},sort_keys=True))
