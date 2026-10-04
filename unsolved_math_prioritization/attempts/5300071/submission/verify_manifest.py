#!/usr/bin/env python3
"""Verify all authored files and reject unexpected files in this frozen packet."""
import hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parent
manifest=json.loads((p/'SHA256SUMS.json').read_text())
files={x.name for x in p.iterdir() if x.is_file()}
assert files==set(manifest)|{'SHA256SUMS.json'},(files,set(manifest))
assert all(x.is_file() for x in p.iterdir()),'unexpected subdirectory'
for name,info in manifest.items():
 b=(p/name).read_bytes()
 assert len(b)==info['bytes'],name
 assert hashlib.sha256(b).hexdigest()==info['sha256'],name
print(json.dumps({'verified':True,'authored_files':len(manifest)},sort_keys=True))
