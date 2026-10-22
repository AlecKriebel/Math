#!/usr/bin/env python3
"""Verify the frozen author packet, using only the Python standard library."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={e['path'] for e in manifest['files']}|{'MANIFEST.json'}
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual==expected, {'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
for e in manifest['files']:
    p=root/e['path'];data=p.read_bytes()
    assert len(data)==e['bytes'],e['path']
    assert hashlib.sha256(data).hexdigest()==e['sha256'],e['path']
print(json.dumps({'status':'PASS_MANIFEST','files':len(manifest['files'])}))
