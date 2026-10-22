#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text())
expected=set(m['files'])
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST.json'}
assert actual==expected,{'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
for name,meta in m['files'].items():
    raw=(root/name).read_bytes()
    assert len(raw)==meta['bytes'],name
    assert hashlib.sha256(raw).hexdigest()==meta['sha256'],name
print('PASS: '+str(len(expected))+' payload files match the manifest.')
