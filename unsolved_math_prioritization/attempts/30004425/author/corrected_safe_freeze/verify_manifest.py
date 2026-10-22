#!/usr/bin/env python3
"""Verify exactly the authored frozen payload; read-only and portable."""
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
m=json.loads((p/'MANIFEST.json').read_text())
expected=set(m['files'])|{'MANIFEST.json'}
actual={x.name for x in p.iterdir() if x.is_file()}
assert expected==actual,(expected-actual,actual-expected)
for name,meta in m['files'].items():
 b=(p/name).read_bytes()
 assert len(b)==meta['bytes'],name
 assert hashlib.sha256(b).hexdigest()==meta['sha256'],name
print(json.dumps({'result':'PASS','files_checked':len(m['files']),'manifest_self_excluded':True}))
