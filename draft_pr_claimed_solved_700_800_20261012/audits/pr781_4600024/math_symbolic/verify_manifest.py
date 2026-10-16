#!/usr/bin/env python3
"""Verify this closed authored package and its three immutable source inputs.
The manifest is the custody envelope: every other authored file is hashed by it.
Its own SHA256 is printed independently to avoid circular self-hashing.
"""
from pathlib import Path
import hashlib,json

root=Path(__file__).resolve().parent
manifest_path=root/'MANIFEST.json'
manifest=json.loads(manifest_path.read_text())
expected={item['path']:item for item in manifest['authored_files']}
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()
        and p!=manifest_path}
assert actual==set(expected), {'unmanifested':sorted(actual-set(expected)),
                               'missing':sorted(set(expected)-actual)}
assert not any(p.is_symlink() for p in root.rglob('*')), 'symlink in package'
for name,item in expected.items():
    body=(root/name).read_bytes()
    assert len(body)==item['bytes'], name
    assert hashlib.sha256(body).hexdigest()==item['sha256'], name
for item in manifest['immutable_inputs']:
    body=(root.parent/item['path']).read_bytes()
    assert hashlib.sha256(body).hexdigest()==item['sha256'], item['path']
print(json.dumps({'status':'PASS','custody_code':manifest['custody_code'],
                  'closed_authored_file_count_including_manifest':len(expected)+1,
                  'immutable_input_count':len(manifest['immutable_inputs']),
                  'manifest_sha256':hashlib.sha256(manifest_path.read_bytes()).hexdigest()},
                 indent=2,sort_keys=True))
