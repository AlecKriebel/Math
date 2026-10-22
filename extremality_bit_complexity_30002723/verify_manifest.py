#!/usr/bin/env python3
"""Verify every payload listed in MANIFEST.json, and reject extra payload files."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
assert manifest['schema']=='sha256-payload-manifest-v1'
expected={x['path']:x for x in manifest['files']}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix()!='MANIFEST.json' and '__pycache__' not in p.parts and p.suffix!='.pyc'}
assert actual==set(expected),{'missing':sorted(set(expected)-actual),'extra':sorted(actual-set(expected))}
for name,entry in expected.items():
 p=root/name;b=p.read_bytes()
 assert len(b)==entry['bytes'],name
 assert hashlib.sha256(b).hexdigest()==entry['sha256'],name
print(json.dumps({'status':'PASS','payload_files':len(expected),'payload_bytes':sum(x['bytes'] for x in expected.values()),'manifest_self_hash':'The manifest excludes itself; authenticate its SHA-256 separately.'}))
