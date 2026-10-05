#!/usr/bin/env python3
"""Check every manifest-listed audit payload file without changing it."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
for record in manifest['files']:
    payload=(root/record['name']).read_bytes()
    assert len(payload)==record['bytes'], record['name']+' byte mismatch'
    assert hashlib.sha256(payload).hexdigest()==record['sha256'], record['name']+' hash mismatch'
actual={p.name for p in root.iterdir() if p.is_file()}-{'AUDIT_MANIFEST.json'}
assert actual=={r['name'] for r in manifest['files']}, 'unexpected or missing payload'
print(json.dumps({'status':'PASS','verified_payload_files':len(actual)}))
