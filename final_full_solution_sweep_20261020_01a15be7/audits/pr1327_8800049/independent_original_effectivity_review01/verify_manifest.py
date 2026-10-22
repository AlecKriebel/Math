#!/usr/bin/env python3
"""Read-only verification of closed local evidence and the pinned Git inputs."""
from pathlib import Path
import hashlib,json,subprocess,sys
base=Path(__file__).resolve().parent
manifest=json.loads((base/'MANIFEST.json').read_text())
actual=set()
for p in base.rglob('*'):
 if p.is_symlink():raise RuntimeError('Symlink is not permitted: '+str(p))
 if p.is_file() and p.name!='MANIFEST.json':actual.add(p.relative_to(base).as_posix())
expected={x['path'] for x in manifest['members']}
if actual!=expected:raise RuntimeError('Member closure differs: '+str(actual^expected))
for x in manifest['members']:
 p=base/x['path'];data=p.read_bytes()
 if len(data)!=x['bytes'] or hashlib.sha256(data).hexdigest()!=x['sha256']:raise RuntimeError('Member mismatch: '+x['path'])
total=sum(p.stat().st_size for p in base.rglob('*') if p.is_file())
if total>8*1024*1024:raise RuntimeError('Storage cap exceeded')
repo=next(p for p in base.parents if (p/'.git').exists())
if subprocess.check_output(['git','branch','--show-current'],cwd=repo,text=True).strip()!='main':raise RuntimeError('Branch differs from authorized main')
binding=json.loads((base/'PINNED_MEMBER_HASHES.json').read_text())
for x in binding['members']:
 actual_blob=subprocess.check_output(['git','rev-parse',binding['head']+':'+x['path']],cwd=repo,text=True).strip()
 data=subprocess.check_output(['git','show',binding['head']+':'+x['path']],cwd=repo)
 if actual_blob!=x['expected_git_blob'] or hashlib.sha256(data).hexdigest()!=x['sha256']:raise RuntimeError('Pinned object mismatch: '+x['path'])
controls=json.loads(subprocess.check_output([sys.executable,str(base/'independent_finite_controls.py')],text=True))
if controls!=json.loads((base/'FINITE_CONTROLS_RESULT.json').read_text()):raise RuntimeError('Finite controls differ')
print(json.dumps({'closed_members':len(actual),'pinned_blobs':len(binding['members']),'storage_bytes_including_manifest':total,'cap_bytes':8*1024*1024,'finite_controls_reproduced':True,'main_branch':True,'passed':True},indent=2))
