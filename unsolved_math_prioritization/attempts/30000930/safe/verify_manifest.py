#!/usr/bin/env python3
"""Verify the current release and all preserved history bytes."""
import hashlib,json
from pathlib import Path
r=Path(__file__).resolve().parent
m=json.loads((r/'MANIFEST.json').read_text());expected={e['path']:e for e in m['files']}
actual={str(p.relative_to(r)) for p in r.rglob('*') if p.is_file() and p!=r/'MANIFEST.json'}
assert actual==set(expected),{'missing':sorted(set(expected)-actual),'extra':sorted(actual-set(expected))}
for name,e in expected.items():
 p=Path(name);assert not p.is_absolute() and '..' not in p.parts and '__pycache__' not in p.parts
 b=(r/p).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],name
h=json.loads((r/'HISTORY_BINDING.json').read_text())
for e in h['files']:
 b=(r/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
print(json.dumps({'status':'PASS','files':len(expected),'historical_files_bound':len(h['files'])},sort_keys=True))
