#!/usr/bin/env python3
"""Strict publication allowlist and exact-byte validation. No network access."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'PUBLICATION_MANIFEST.json').read_text())
expected={e['path'] for e in manifest['files']}
assert len(expected)==len(manifest['files']),'duplicate manifest entries'
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p!=root/'PUBLICATION_MANIFEST.json'}
assert actual==expected,{'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}
for e in manifest['files']:
    b=(root/e['path']).read_bytes()
    assert len(b)==e['bytes'],e['path']+' byte count'
    assert hashlib.sha256(b).hexdigest()==e['sha256'],e['path']+' SHA-256'
# The two nested manifests remain bound to their original exact payloads.
for folder,name in [('submission','SHA256SUMS.json'),('audit','AUDIT_MANIFEST.json')]:
    nested=root/folder;m=json.loads((nested/name).read_text())
    names={e['path'] for e in m['files']}|{name}
    assert {str(p.relative_to(nested)) for p in nested.rglob('*') if p.is_file()}==names,folder+' exact inventory'
    for e in m['files']:
        b=(nested/e['path']).read_bytes()
        assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],folder+'/'+e['path']
print('PASS:',len(expected)+1,'publication files and nested manifests')
