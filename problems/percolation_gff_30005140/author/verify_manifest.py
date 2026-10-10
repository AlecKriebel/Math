#!/usr/bin/env python3
"""Verify the frozen authored-file allowlist. Does not assess mathematical validity."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={row['path']:row for row in manifest['files']}
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()
        and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
assert actual==set(expected), {'missing': sorted(set(expected)-actual),
                              'unexpected': sorted(actual-set(expected))}
for name,row in expected.items():
    p=root/name
    assert not p.is_symlink(), name
    data=p.read_bytes()
    assert len(data)==row['bytes'], name
    assert hashlib.sha256(data).hexdigest()==row['sha256'], name
print(json.dumps({'status':'PASS','files_checked':len(expected),
                  'scope':'Byte identity and allowlist only; not a proof audit.'},sort_keys=True))
