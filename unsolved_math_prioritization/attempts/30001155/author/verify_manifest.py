#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text())
for f in m['files']:
 b=(root/f['path']).read_bytes()
 assert len(b)==f['bytes'], f['path']
 assert hashlib.sha256(b).hexdigest()==f['sha256'], f['path']
print(json.dumps({'status':'PASS','files':len(m['files']),'bytes':sum(f['bytes'] for f in m['files'])}))
