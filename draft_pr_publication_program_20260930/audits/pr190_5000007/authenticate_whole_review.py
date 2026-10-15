"""Authenticate exact whole-review evidence, without promoting its opinion blindly."""
from pathlib import Path
import datetime,hashlib,json,stat,sys
A=Path(__file__).resolve().parent;d=sys.argv[1];outname=sys.argv[2];D=A/d
def require(x,msg):
 if not x:raise RuntimeError(msg)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
seal=json.loads((D/'FINAL_SEAL.json').read_text());entries=seal.get('files',seal.get('manifest',seal.get('key_files')));require(isinstance(entries,list) and entries,'Bad final seal schema')
names=set()
for x in entries:
 n=x['path'];q=Path(n);require(not q.is_absolute() and '..' not in q.parts and not (D/q).is_symlink(),'Unsafe review entry');p=D/q;actual=pin(p);require(actual['sha256']==x.get('sha256',x.get('SHA256')) and actual['bytes']==x['bytes'],'Review content identity drift '+n);require(stat.S_IMODE(p.stat().st_mode)==0o444,'Unprotected review artifact '+n);names.add(n)
safe_j=json.loads((D/'SAFE_AUTHORED_ALLOWLIST.json').read_text());safe=safe_j.get('files',safe_j.get('key_files'));require(isinstance(safe,list) and len(safe)==len(set(safe)),'Invalid safeallowlist')
for n in safe:
 require(n in names or n=='FINAL_SEAL.json','Unsealed safe artifact '+n)
 require(not any('private' in x.lower() or 'chrome' in x.lower() for x in Path(n).parts) and not n.endswith('.layout.txt'),'Private/source body path in safeallowlist')
 require(stat.S_IMODE((D/n).stat().st_mode)==0o444,'Safe artifact not protected '+n)
require('FINAL_REPORT.md' in names,'Final report absent from seal')
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'EXACT_REVIEW_FINAL_SEAL_AND_SAFE_AUTHORSHIP_SCOPE_AUTHENTICATED','reviewer':d,'sealed_files':len(names),'safe_files':len(safe),'report':pin(D/'FINAL_REPORT.md'),'final_seal':pin(D/'FINAL_SEAL.json'),'safeallowlist':pin(D/'SAFE_AUTHORED_ALLOWLIST.json'),'all_actual_modes_0444':True,'judgment_requires_root_read_and_scope_review':True}
p=A/outname;require(not p.exists(),'Authentication record already exists');p.write_text(json.dumps(out,indent=2)+'\n');p.chmod(0o444);print(json.dumps(out))
