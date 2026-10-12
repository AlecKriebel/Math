#!/usr/bin/env python3
"""Read-only closed additive packet and immutable parent/seal verification."""
from pathlib import Path,PurePosixPath
import hashlib,json
F=Path(__file__).resolve().parent;OWN=F.parent;A=OWN.parent
excluded={'private','private_runs','__pycache__','post_merge','provenance_appendix'}
def sha(b):return hashlib.sha256(b).hexdigest()
def scope():return {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file() and not any(x in excluded for x in p.relative_to(F).parts) and p!=F/'PUBLIC_MANIFEST.json'}
m=json.loads((F/'PUBLIC_MANIFEST.json').read_bytes());seen=set()
for r in m['files']:
 p=PurePosixPath(r['path']);assert not p.is_absolute() and '..' not in p.parts and p.as_posix()==r['path'] and r['path'] not in seen;seen.add(r['path']);f=F/p;assert not f.is_symlink() and f.resolve().is_relative_to(F.resolve());b=f.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['path']
assert seen==scope() and len(seen)==m['public_files']
s=json.loads((F/'FINAL_LIVE_SEAL.json').read_bytes())
for r in s['bindings']:
 b=(F/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['path']
for row in s['original_seal_bindings']:
 root=OWN if row['root']=='own_original' else A;b=(root/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'],row['path']
assert sha((OWN/'PUBLIC_MANIFEST.json').read_bytes())=='bf7cece6ed2edc56f2b865baed9f0bcf9a13378511929c3f7f64d0cfb2144036'
print(json.dumps({'status':'PASS','additive_public_files':len(seen),'immutable_original47_manifest_source_math_final_seals':True,'original_problem':'unsolved5/5','actual_merge_pending':True},sort_keys=True))
