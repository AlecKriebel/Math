#!/usr/bin/env python3
"""Portable allowlist and hash verification, without external inputs."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={entry['path'] for entry in manifest['files']}|{'MANIFEST.json'}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual==expected, {'extra':sorted(actual-expected),'missing':sorted(expected-actual)}
for entry in manifest['files']:
    data=(root/entry['path']).read_bytes()
    assert len(data)==entry['bytes'],entry['path']
    assert hashlib.sha256(data).hexdigest()==entry['sha256'],entry['path']
print(json.dumps({'status':'PASS','file_hashes_checked':len(manifest['files']),'exact_allowlist':True},sort_keys=True))
