#!/usr/bin/env python3
"""Read-only closed-member, pinned-blob and finite-control verifier."""
from pathlib import Path
import hashlib,json,subprocess,sys
base=Path(__file__).resolve().parent;m=json.loads((base/'MANIFEST.json').read_text());actual=set()
for p in base.rglob('*'):
 if p.is_symlink():raise RuntimeError('Symlink: '+str(p))
 if p.is_file() and p.name!='MANIFEST.json':actual.add(p.relative_to(base).as_posix())
if actual!={x['path'] for x in m['members']}:raise RuntimeError('Member closure differs')
for x in m['members']:
 data=(base/x['path']).read_bytes()
 if len(data)!=x['bytes'] or hashlib.sha256(data).hexdigest()!=x['sha256']:raise RuntimeError('Member hash differs: '+x['path'])
repo=next(p for p in base.parents if (p/'.git').exists())
if subprocess.check_output(['git','branch','--show-current'],cwd=repo,text=True).strip()!='main':raise RuntimeError('Branch differs')
b=json.loads((base/'PINNED_MEMBER_HASHES.json').read_text())
for x in b['members']:
 g=subprocess.check_output(['git','rev-parse',b['head']+':'+x['path']],cwd=repo,text=True).strip()
 data=subprocess.check_output(['git','show',b['head']+':'+x['path']],cwd=repo)
 if g!=x['git_blob'] or hashlib.sha256(data).hexdigest()!=x['sha256']:raise RuntimeError('Pinned blob differs: '+x['path'])
new=json.loads(subprocess.check_output([sys.executable,str(base/'independent_generation_controls.py')],text=True))
if new!=json.loads((base/'FINITE_CONTROLS_RESULT.json').read_text()):raise RuntimeError('Controls differ')
total=sum(p.stat().st_size for p in base.rglob('*') if p.is_file())
if total>8*1024*1024:raise RuntimeError('Storage cap exceeded')
print(json.dumps({'passed':True,'closed_members':len(actual),'pinned_blobs':len(b['members']),'main_branch':True,'storage_bytes_including_manifest':total,'cap_bytes':8*1024*1024,'finite_controls_reproduced':True},indent=2))
