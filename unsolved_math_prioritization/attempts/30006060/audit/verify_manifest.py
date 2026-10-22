#!/usr/bin/env python3
"""Check all frozen payload paths, hashes and sizes without assertions."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
listed=set()
for row in manifest['files']:
    name=row['path'];relative=Path(name)
    if relative.is_absolute() or '..' in relative.parts or name in listed or name=='MANIFEST.json':
        raise ValueError('unsafe or duplicate manifest path')
    listed.add(name);file=root/relative
    if file.is_symlink() or not file.is_file():raise ValueError('missing or unsafe payload: '+name)
    content=file.read_bytes()
    if len(content)!=row['bytes'] or hashlib.sha256(content).hexdigest()!=row['sha256']:
        raise ValueError('payload mismatch: '+name)
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
if actual!=listed:raise ValueError('manifest does not cover exact payload')
print(json.dumps({'status':'pass','payload_files':len(listed),'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()},sort_keys=True))
