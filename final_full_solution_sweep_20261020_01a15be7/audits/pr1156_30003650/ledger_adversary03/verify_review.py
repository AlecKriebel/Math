#!/usr/bin/env python3
"""Verify this closed public review artifact set and optional retained input snapshot."""
import hashlib,json
from pathlib import Path
O=Path(__file__).resolve().parent
manifest_path=O/'MANIFEST.json'
manifest=manifest_path.read_bytes()
expected=(O/'MANIFEST.sha256').read_text().split()[0]
if hashlib.sha256(manifest).hexdigest()!=expected:raise RuntimeError('Manifest SHA mismatch')
v=json.loads(manifest)
excluded={'MANIFEST.json','MANIFEST.sha256'}
actual={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file() and p.relative_to(O).parts[0]!='private' and p.relative_to(O).as_posix() not in excluded}
if actual!={e['path'] for e in v['entries']}:raise RuntimeError('Public artifact closure mismatch')
for e in v['entries']:
 p=O/e['path'];b=p.read_bytes()
 if p.is_symlink() or len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise RuntimeError('Artifact binding mismatch: '+e['path'])
snapshot=O/'private/snapshot'
if snapshot.exists():
 pv=json.loads((O/'PRIVATE_SNAPSHOT_MANIFEST.json').read_text())
 found={p.relative_to(snapshot).as_posix() for p in snapshot.rglob('*') if p.is_file()}
 if found!={e['path'] for e in pv['entries']}:raise RuntimeError('Private snapshot closure mismatch')
 for e in pv['entries']:
  b=(snapshot/e['path']).read_bytes()
  if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise RuntimeError('Private snapshot SHA mismatch')
print(json.dumps({'public_manifest_verified':True,'public_payloads':len(v['entries']),'private_snapshot_verified':snapshot.exists(),'execution_readiness':False}))
