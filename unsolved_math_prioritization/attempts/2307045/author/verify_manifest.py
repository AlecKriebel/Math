#!/usr/bin/env python3
"""Check the frozen authored packet without consulting external sources."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text())
expected={x['path'] for x in m['files']}
actual={p.name for p in root.iterdir() if p.is_file() and p.name!='MANIFEST.json'}
assert expected==actual, (expected-actual,actual-expected)
for x in m['files']:
    b=(root/x['path']).read_bytes()
    assert len(b)==x['bytes'],x['path']
    assert hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
print('PASS: all',len(expected),'authored packet files match the manifest')
