#!/usr/bin/env python3
"""Authenticate every deliberately public member; do not read private sources."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest_path=root/'MANIFEST.json'
manifest=json.loads(manifest_path.read_text())
files=manifest['files']; allowed=manifest['explicit_public_allowlist']
assert isinstance(files,dict)
assert len(allowed)==len(set(allowed))
assert sorted(files)==sorted(allowed)
assert 'MANIFEST.json' not in files
for name,expected in files.items():
 p=Path(name)
 assert not p.is_absolute() and '..' not in p.parts and p.parts[0]!='private_primary'
 body=(root/p).read_bytes()
 assert len(body)==expected['bytes'],name
 assert hashlib.sha256(body).hexdigest()==expected['sha256'],name
print(json.dumps({'authenticated_public_members':len(files),'manifest_sha256':hashlib.sha256(manifest_path.read_bytes()).hexdigest()}))
