#!/usr/bin/env python3
from pathlib import Path
import datetime,hashlib,json,os,zipfile
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0';K=D/'verification_kit'
def obj(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def row(p,root,key='path'):return {key:p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
sources=obj(A/'newreviews/package_04/SOURCE_READ_LEDGER.json')['sources']
dump(K/'TERMINAL_AFTER_WHOLE04_SOURCE_BODY_OMISSIONS.json',{'scope':'Eight newly selected authored source-interface references; bodies remain exact local inputs only. Extract derivatives separately omitted by the 52-row output-decision ledger. This administration performs no new semantic body read.','files':[{'source':r['source'],'original_path':r['path'],'bytes':r['bytes'],'sha256':r['sha256'],'disposition':'omitted','reason':'Third-party primary body not newly distributed; exact local path/version/hash and actual whole04 reading scope retained in selected authored ledger.'} for r in sources]})
names=sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file());allow=obj(K/'ALLOWLIST.json');allow['members']=names;dump(K/'ALLOWLIST.json',allow)
m=obj(K/'MANIFEST.json');m['files']=[row(K/n,K) for n in names if n!='MANIFEST.json'];dump(K/'MANIFEST.json',m)
temp=D/'verification_kit.zip.terminal-after04-new'
with zipfile.ZipFile(temp,'w',compression=0) as z:
 for n in names:
  i=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=0;z.writestr(i,(K/n).read_bytes())
os.replace(temp,D/'verification_kit.zip')
b=obj(D/'EXTERNAL_BINDING.json');b['as_of_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();b['scope']='Current terminal administrative successor after four complete reviews/minimum two/latest whole04 ZERO ROOT-adopted. No further complete whole review currently required; external final ROOT integrity required and UNADOPTED. Internal publication readiness/issues-resolved/published false; PR1032 service hold. Historical checkpoint objects and native metadata unchanged.';b['manifest_sha256']=sha(K/'MANIFEST.json');b['archive']=row(D/'verification_kit.zip',D,'filename');b['external_files']=[row(D/r['filename'],D,'filename') for r in b['external_files']];b['current_terminal_after_whole04']=row(D/'CURRENT_TERMINAL_AFTER_WHOLE04.json',D,'filename');dump(D/'EXTERNAL_BINDING.json',b)
dump(W/'PACKAGING_COMPLETE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'members':len(names),'manifest_payloads':len(names)-1,'archive':b['archive'],'pdf':b['pdf'],'current_status':b['current_terminal_after_whole04']});print(json.dumps(obj(W/'PACKAGING_COMPLETE.json'),indent=2))
