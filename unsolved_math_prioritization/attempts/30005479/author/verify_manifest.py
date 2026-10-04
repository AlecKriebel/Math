#!/usr/bin/env python3
"""Check the frozen authored packet, without reading private research inputs."""
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
assert {p.name for p in root.iterdir() if p.is_file()}==set(manifest['files'])|{'SHA256SUMS.json'}
for name,meta in manifest['files'].items():
    raw=(root/name).read_bytes()
    assert len(raw)==meta['bytes'],name
    assert hashlib.sha256(raw).hexdigest()==meta['sha256'],name
print(json.dumps({'passed':True,'files_checked':len(manifest['files'])},sort_keys=True))
