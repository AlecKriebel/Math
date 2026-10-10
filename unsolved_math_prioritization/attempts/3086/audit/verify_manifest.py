#!/usr/bin/env python3
"""Validate exactly the safe audit release listed in the manifest."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'manifest.json').read_text())
entries=m['files']; expected={e['path'] for e in entries}|{'manifest.json'}
if len(expected)!=len(entries)+1:raise RuntimeError('Repeated manifest name')
actual={p.name for p in root.iterdir()}
if actual!=expected:raise RuntimeError('Release allowlist differs: '+str(actual^expected))
for e in entries:
 name=e['path'];p=root/name
 if '/' in name or '\\' in name or name in ('.','..') or p.is_symlink() or not p.is_file():raise RuntimeError('Unsafe member')
 b=p.read_bytes()
 if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise RuntimeError('Digest mismatch: '+name)
print(json.dumps({'status':'PASS','safe_files':len(expected)}))
