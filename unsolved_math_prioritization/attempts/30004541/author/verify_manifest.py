#!/usr/bin/env python3
"""Verify the authored artifact allowlist against its SHA-256 manifest."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parent
m=json.loads((root/'AUTHOR_MANIFEST.json').read_text())
expected=set(m['files'])|{'AUTHOR_MANIFEST.json'}
actual={p.name for p in root.iterdir() if p.is_file()}
assert actual==expected, {'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}
assert all(p.is_file() for p in root.iterdir()), 'Unexpected directory'
for name,meta in m['files'].items():
    b=(root/name).read_bytes()
    assert len(b)==meta['bytes'],name
    assert hashlib.sha256(b).hexdigest()==meta['sha256'],name
print(json.dumps({'status':'PASS','files_checked':len(m['files']),
                  'manifest_sha256':hashlib.sha256((root/'AUTHOR_MANIFEST.json').read_bytes()).hexdigest()}))
