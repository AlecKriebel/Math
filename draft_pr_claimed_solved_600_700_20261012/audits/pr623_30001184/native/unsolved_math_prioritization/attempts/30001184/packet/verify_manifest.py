#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
m=json.loads((p/'SHA256SUMS.json').read_bytes())
actual={str(f.relative_to(p)):f for f in p.rglob('*') if f.is_file() and f.name!='SHA256SUMS.json'}
assert set(actual)==set(m), 'file set mismatch'
for name,entry in m.items():
    b=actual[name].read_bytes()
    assert len(b)==entry['bytes'], name+' byte count'
    assert hashlib.sha256(b).hexdigest()==entry['sha256'], name+' sha256'
print(json.dumps({'result':'PASS','files_verified':len(m)},sort_keys=True))
