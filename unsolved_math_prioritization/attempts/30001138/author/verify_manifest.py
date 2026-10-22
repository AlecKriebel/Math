#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
m=json.loads((p/'MANIFEST.json').read_text())
for f in m['files']:
 b=(p/f['path']).read_bytes()
 assert len(b)==f['bytes'],f['path']
 assert hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
actual={str(x.relative_to(p)) for x in p.rglob('*') if x.is_file() and '__pycache__' not in x.parts and x.name not in ['MANIFEST.json','replay.json']}
assert actual=={f['path'] for f in m['files']},(actual,{f['path'] for f in m['files']})
print('PASS',len(m['files']),'manifest entries')
