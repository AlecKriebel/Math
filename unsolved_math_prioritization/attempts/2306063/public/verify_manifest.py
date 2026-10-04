#!/usr/bin/env python3
"""Strict manifest replay; no filesystem writes, subprocesses, or network."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
expected=set(manifest['files'])|{'SHA256SUMS.json'}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual==expected, {'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
for rel,record in manifest['files'].items():
    assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
    data=(root/rel).read_bytes()
    assert len(data)==record['bytes'],rel
    assert hashlib.sha256(data).hexdigest()==record['sha256'],rel
assert all(not p.endswith(('.pdf','.png','.jpg','.sqlite','.db')) for p in expected)
print(json.dumps({'status':'PASS','verified_files':len(manifest['files']),'strict_inventory':True},sort_keys=True))
