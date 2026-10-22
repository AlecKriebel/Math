#!/usr/bin/env python3
"""Read-only SHA256/length validation; receipt is sealed externally, never itself."""
import hashlib
import json
from pathlib import Path

base = Path(__file__).resolve().parent
allowed = base.parent.parent.resolve()
receipt = json.loads((base / 'RECEIPT.json').read_text())
count = 0
for group in ('artifacts', 'inputs', 'private_source_files'):
    for row in receipt[group]:
        path = (base / row['path']).resolve()
        if not path.is_relative_to(allowed):
            raise ValueError('receipt path escapes the assigned problem folder')
        if path == base / 'RECEIPT.json':
            raise ValueError('circular receipt pin')
        data = path.read_bytes()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise ValueError('integrity mismatch: ' + row['path'])
        count += 1
print(json.dumps({'status':'PASS','validated_pins':count,'receipt_not_self_pinned':True},sort_keys=True))
