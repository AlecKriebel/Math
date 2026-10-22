#!/usr/bin/env python3
"""Verify all audit payloads; manifest hash is externally bound by the receipt."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
listed=set()
for item in manifest['files']:
    path=root/item['path']
    data=path.read_bytes()
    if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
        raise SystemExit('FAIL: '+item['path'])
    listed.add(item['path'])
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
        and p.name!='AUDIT_MANIFEST.json' and '__pycache__' not in p.parts}
if actual!=listed:raise SystemExit('FAIL: file inventory')
print(json.dumps({'result':'PASS','files':len(listed),'target_id':manifest['target_id']}))
