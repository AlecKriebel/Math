#!/usr/bin/env python3
"""Strict closed-allowlist verifier for this independent audit payload."""
import hashlib
import json
from pathlib import Path

def verify(root):
    records = json.loads((root/'MANIFEST.json').read_text())['files']
    expected = {x['path']:x for x in records}
    if len(expected) != len(records):
        raise ValueError('Duplicate manifest entries')
    entries = list(root.iterdir())
    if {p.name for p in entries} != set(expected) | {'MANIFEST.json'}:
        raise ValueError('Audit allowlist mismatch')
    for p in entries:
        if p.is_symlink() or not p.is_file():
            raise ValueError('Nonregular audit entry')
        if p.name == 'MANIFEST.json':
            continue
        r = expected[p.name]
        if Path(r['path']).name != r['path']:
            raise ValueError('Nonlocal audit entry')
        b = p.read_bytes()
        if len(b) != r['bytes'] or hashlib.sha256(b).hexdigest() != r['sha256']:
            raise ValueError('Audit byte/hash mismatch: '+p.name)
    return len(expected)

if __name__ == '__main__':
    print(json.dumps({'status':'PASS','payload_files':verify(Path(__file__).resolve().parent),
                      'manifest_self_hash':'Recorded in the external audit freeze receipt.'},sort_keys=True))
