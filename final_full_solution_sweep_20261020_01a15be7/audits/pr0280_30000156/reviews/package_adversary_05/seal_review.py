#!/usr/bin/env python3
"""Verify reviewed inputs/private custody and seal every public authored file."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,sys,os,stat
O=Path(__file__).resolve().parent;A=O.parents[1];R=A.parents[1];W=R/'private/pr0280_package05'
sha=lambda b:hashlib.sha256(b).hexdigest()
def ck(v,m):
 if not v:raise RuntimeError(m)
def e(p,base):
 ck(p.is_file() and not p.is_symlink(),'regular '+str(p));b=p.read_bytes();return {'path':p.relative_to(base).as_posix(),'bytes':len(b),'sha256':sha(b)}
def verify(base,entries):
 ck(len({x['path'] for x in entries})==len(entries),'unique entries')
 for x in entries:ck(e(base/x['path'],base)=={k:x[k] for k in ['path','bytes','sha256']},'changed '+x['path'])
m=A/'ops_record_url_repair_20261021/MANIFEST.json';ck(sha(m.read_bytes())=='b12e7262026d780029a7eeee1fb8d0c8a514c4a2ab382faadebad40a84dba55d','390 seal');v=json.loads(m.read_text());verify(A,v['files']);ck(len(v['files'])==390,'390 count')
state=[e(p,R.parent) for p in sorted((R.parent/'.zenodo-state').rglob('*')) if p.is_file()];ck(len(state)==314 and sha(json.dumps(state,sort_keys=True,separators=(',',':')).encode())=='1d241f0c6e2450ec0df942bf36bfe438f937d5ad530414028b3b47fcf827010b','state aggregate')
priv=json.loads((O/'PRIVATE_EVIDENCE_MANIFEST.json').read_text());verify(W,priv['files']);ck({e(p,W)['path'] for p in W.rglob('*') if p.is_file() and not p.is_symlink()}=={x['path'] for x in priv['files']},'private inventory')
controls=[]
for p in sorted(W.rglob('*')):
 if p.is_symlink():
  b=os.readlink(p).encode();controls.append({'path':p.relative_to(W).as_posix(),'kind':'symlink','target':os.readlink(p),'bytes':len(b),'sha256':sha(b)})
 elif not p.is_file() and not p.is_dir():
  ck(stat.S_ISFIFO(p.lstat().st_mode),'expected special control');controls.append({'path':p.relative_to(W).as_posix(),'kind':'fifo','bytes':0,'sha256':sha(b'')})
ck(controls==priv['filesystem_controls'],'special hostile control inventory')
excluded={'AUTHORED_FILE_MANIFEST.json','AUTHORED_FILE_MANIFEST.sha256'}
paths=sorted(p for p in O.rglob('*') if p.is_file() and p.name not in excluded)
for p in paths:
 ck(not p.is_symlink(),'public symlink')
 if p.suffix=='.py':ast.parse(p.read_text())
 if p.suffix=='.json':json.loads(p.read_text())
manifest=O/'AUTHORED_FILE_MANIFEST.json';checksum=O/'AUTHORED_FILE_MANIFEST.sha256'
if '--verify' in sys.argv:
 v=json.loads(manifest.read_text());ck(checksum.read_text().split()[0]==sha(manifest.read_bytes()),'self seal');verify(O,v['files']);ck({p.relative_to(O).as_posix() for p in paths}=={x['path'] for x in v['files']},'public inventory')
else:
 ck(not manifest.exists() and not checksum.exists(),'immutable own seal exists')
 v={'schema':1,'sealed_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'package_adversary_05','assigned_review_completion_percent':100,'verdict':'REPAIR_REQUIRED','unresolved_material_findings':['P280-OPS-05'],'publication_authorization':False,'scope':'All final authored public files in assigned review directory, excluding only this manifest and checksum. Each entry uses path/bytes/SHA256. Private evidence separately hash-inventoried; current390 and314-state inputs verified at sealing.','files':[e(p,O) for p in paths]};manifest.write_text(json.dumps(v,indent=2)+'\n');checksum.write_text(sha(manifest.read_bytes())+'  AUTHORED_FILE_MANIFEST.json\n')
print(json.dumps({'verified_public_files':len(v['files']),'private_files':len(priv['files']),'reviewed390_unchanged':True,'state314_unchanged':True,'manifest_sha256':sha(manifest.read_bytes()),'verdict':'REPAIR_REQUIRED','publication_authorization':False}))
