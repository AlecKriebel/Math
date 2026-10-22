#!/usr/bin/env python3
"""Check the exact frozen author-packet file set and bytes, without network."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'SHA256SUMS.json').read_text())
expected={x['path'] for x in m['files']}
actual={p.name for p in root.iterdir() if p.is_file() and p.name!='SHA256SUMS.json'}
assert expected==actual,(sorted(expected-actual),sorted(actual-expected))
for row in m['files']:
    b=(root/row['path']).read_bytes()
    assert len(b)==row['bytes'],row['path']
    assert hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
print('Verified %d frozen author files.'%len(expected))
