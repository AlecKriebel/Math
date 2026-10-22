#!/usr/bin/env python3
"""Read-only byte-custody check. This does not verify mathematics or completeness."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
receipt = json.loads((root / 'RECEIPT.json').read_text())
count = 0
for category in ('inputs', 'artifacts', 'private_evidence'):
    for row in receipt[category]:
        path = (root / row['path']).resolve()
        data = path.read_bytes()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise SystemExit(f'Byte-custody mismatch: {row["path"]}')
        count += 1
print(json.dumps({'status': 'PASS', 'pinned_files': count,
                  'meaning': 'byte custody only; scopes in SOURCE_READS.md'}))
