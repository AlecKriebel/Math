#!/usr/bin/env python3
"""Verify only an explicit curated map, anchored by an independently supplied hash."""
import argparse, hashlib, json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
manifest=Path(a.manifest).resolve();raw=manifest.read_bytes()
actual=hashlib.sha256(raw).hexdigest()
if actual!=a.manifest_sha256: raise SystemExit('Manifest hash mismatch')
d=json.loads(raw);base=manifest.parent
if d.get('schema')!='pr932-source-model-explicit-public-map-v1': raise SystemExit('Unexpected schema')
names=[]
for item in d['files']:
 name=item['path'];rel=Path(name)
 if rel.is_absolute() or '..' in rel.parts or 'private' in rel.parts: raise SystemExit('Unsafe/private map entry')
 if name in [manifest.name,d['external_anchor']]: raise SystemExit('Circular metadata entry')
 if name in names: raise SystemExit('Duplicate entry')
 names.append(name);target=base/rel
 if target.is_symlink() or not target.is_file(): raise SystemExit('Missing or symlinked curated file: '+name)
 content=target.read_bytes()
 if len(content)!=item['bytes'] or hashlib.sha256(content).hexdigest()!=item['sha256']: raise SystemExit('Content mismatch: '+name)
print(json.dumps(dict(manifest_sha256=actual,manifest_bytes=len(raw),curated_files_checked=len(names),all_match=True,private_bodies_included=False),indent=2))
