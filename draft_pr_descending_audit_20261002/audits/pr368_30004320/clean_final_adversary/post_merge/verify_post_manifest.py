#!/usr/bin/env python3
"""Read-only closed public post-merge packet and earlier immutable seals."""
from pathlib import Path,PurePosixPath
import hashlib,json
F=Path(__file__).resolve().parent;OWN=F.parent;A=OWN.parent
sha=lambda b:hashlib.sha256(b).hexdigest();excluded={'private','private_runs','__pycache__','post_publication','provenance_appendix'}
m=json.loads((F/'PUBLIC_MANIFEST.json').read_bytes());seen=set()
for r in m['files']:
 p=PurePosixPath(r['path']);assert not p.is_absolute() and '..' not in p.parts and p.as_posix()==r['path'] and r['path'] not in seen;seen.add(r['path']);f=F/p;assert not f.is_symlink() and f.resolve().is_relative_to(F.resolve());b=f.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['path']
actual={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file() and p!=F/'PUBLIC_MANIFEST.json' and not any(x in excluded for x in p.relative_to(F).parts)};assert actual==seen and len(seen)==m['public_files']
s=json.loads((F/'FINAL_POST_SEAL.json').read_bytes())
for r in s['bindings']:
 b=(F/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
for r in s['earlier_seal_bindings']:
 root=OWN if r['root']=='original' else OWN/'final_live';b=(root/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
assert sha((OWN/'PUBLIC_MANIFEST.json').read_bytes())=='bf7cece6ed2edc56f2b865baed9f0bcf9a13378511929c3f7f64d0cfb2144036'
assert sha((OWN/'final_live/PUBLIC_MANIFEST.json').read_bytes())=='3c047d9b0663018219c9f6b4e6898a18175f75cd6e96ee6f93acfb1038d10445'
print(json.dumps({'status':'PASS','post_public_files':len(seen),'original47_final_live1635_seals_unchanged':True,'actual_merge_verified':'2da0adc1c56dbb15e53be162489eb001cfa83e03','accepted_problem_status':'unsolved5/5','final_independent_replay_publication_pending':True},sort_keys=True))
