#!/usr/bin/env python3
"""Verify the frozen public files. Python 3.10+, standard library only."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
expected=set(manifest['files'])
actual={p.name for p in root.iterdir() if p.is_file() and p.name!='SHA256SUMS.json'}
assert expected==actual, {'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}
for name,entry in manifest['files'].items():
    data=(root/name).read_bytes()
    assert len(data)==entry['bytes'], name
    assert hashlib.sha256(data).hexdigest()==entry['sha256'], name
print(json.dumps({'status':'passed','files_verified':len(expected)},sort_keys=True))
