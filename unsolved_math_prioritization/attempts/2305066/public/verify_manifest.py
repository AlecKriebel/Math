#!/usr/bin/env python3
"""Check the complete public allowlist and hashes; manifest excludes itself."""
import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
m=json.loads((p/'SHA256SUMS.json').read_text())
expected=set(m['files'])
actual={str(x.relative_to(p)) for x in p.rglob('*') if x.is_file() and x.name!='SHA256SUMS.json' and '__pycache__' not in x.parts}
assert actual==expected,{'extra':sorted(actual-expected),'missing':sorted(expected-actual)}
for name,entry in m['files'].items():
    b=(p/name).read_bytes()
    assert len(b)==entry['bytes'],name
    assert hashlib.sha256(b).hexdigest()==entry['sha256'],name
    assert not name.lower().endswith(('.pdf','.png','.zip')),name
print(json.dumps({'result':'pass','files_checked':len(expected),'manifest_sha256':hashlib.sha256((p/'SHA256SUMS.json').read_bytes()).hexdigest()},sort_keys=True))
