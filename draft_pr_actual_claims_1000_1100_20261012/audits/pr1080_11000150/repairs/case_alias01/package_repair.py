#!/usr/bin/env python3
"""One bounded local packaging pass; never installed in the portable kit."""
import hashlib,json,os,zipfile,datetime
from pathlib import Path
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0';K=D/'verification_kit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_text())
def put(p,b):
 t=p.with_name(p.name+'.case_alias01-new');t.write_bytes(b);os.replace(t,p)
def dump(p,d):put(p,(json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def row(p,root,key='path'):return {key:p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
names=sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file())
allow=obj(K/'ALLOWLIST.json');allow['members']=names;dump(K/'ALLOWLIST.json',allow)
manifest=obj(K/'MANIFEST.json');manifest['files']=[row(K/n,K) for n in names if n!='MANIFEST.json'];dump(K/'MANIFEST.json',manifest)
tmp=D/'verification_kit.zip.case_alias01-new'
with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_STORED) as z:
 for n in names:
  i=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_STORED;i.flag_bits=0;z.writestr(i,(K/n).read_bytes())
os.replace(tmp,D/'verification_kit.zip')
b=obj(D/'EXTERNAL_BINDING.json');b['as_of_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();b['scope']='External noncircular bounded case-alias repair binding; ROOT repair adoption and NEW complete whole03 required. Dated stages remain historical; no publication or human refereeing certified.'
b['manifest_sha256']=sha(K/'MANIFEST.json');b['archive']=row(D/'verification_kit.zip',D,'filename')
b['external_files']=[row(D/n,D,'filename') for n in sorted([r['filename'] for r in b['external_files']]+['CURRENT_CASE_ALIAS_REPAIR01.json'])]
dump(D/'EXTERNAL_BINDING.json',b)
print(json.dumps({'members':len(names),'archive':b['archive'],'manifest_sha256':b['manifest_sha256']}))
