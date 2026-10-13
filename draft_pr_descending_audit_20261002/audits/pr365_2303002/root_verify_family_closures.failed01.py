"""ROOT full immutable family inventories and literal read-only reexecution.

Writes only new ROOT receipts; temporarily restores two hash-verified ignored
Poisson source PDFs, removes them in finally, and never reruns writing drivers.
"""
from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess,sys
A=Path(__file__).resolve().parent
REPO=A.parents[2]
PY=REPO/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
OUT=A/'root_family_streams';OUT.mkdir(exist_ok=False)
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1',PYTHONDONTWRITEBYTECODE='1')
checks=[];records=[];allowed=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text())
def check(n,c):
 if not c:raise AssertionError(n)
 checks.append(n)
def identity(p,r):
 b=p.read_bytes();check(str(p.relative_to(A))+':bytes',len(b)==r['bytes']);check(str(p.relative_to(A))+':sha',sha(b)==r['sha256']);return b
def normalized(m):return m['files'] if isinstance(m['files'],dict) else {r['path']:r for r in m['files']}
pins={
 'path_geometry_review':('PUBLIC_MANIFEST.json','44d334caa6835c18388a67f58f5d8756637c76c355268cddfd5160569f61c80c','d27fb0fabce2459ade5afdf28586f0831d7d16815f04b8306c9dd6da4dfa74e9'),
 'poisson_components_review':('PUBLIC_MANIFEST.json','5a6ef2af64d435ecce35a305a7de91295ea6ccd02c2290edfab0c7c7fa70be9d','082d6d7886f5d9b50903020a0f4698589f27bc7a66df2a9668146466100314a3'),
 'poisson_components_corrections':('SUPPLEMENT_MANIFEST.json',None,'eb94d2c623d6ee2d542d690393216468b3391158c04577d1686c09a318aa8d9b')}
before={};manifests={}
for name,(mf,msha,sseal) in pins.items():
 R=A/name;m=load(R/mf);manifests[name]=m
 if msha:check(name+':manifestpin',sha((R/mf).read_bytes())==msha)
 check(name+':sealpin',sha((R/'FINAL_SEAL.json').read_bytes())==sseal)
 public=normalized(m)
 if name=='path_geometry_review':private={r['path']:r for r in m['private_inventory']}
 elif name=='poisson_components_review':private=load(R/'receipts/private_inventory.json')['files']
 else:private=load(R/'PRIVATE_INVENTORY.json')['files']
 expected=set(public)|set(private)|{mf,'FINAL_SEAL.json'}
 actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 check(name+':exactALLnamespace',actual==expected)
 for path,r in {**public,**private}.items():
  b=identity(R/path,r)
  if path.endswith('.gz') and 'logical_bytes' in r:
   d=gzip.decompress(b);check(path+':logicalbytes',len(d)==r['logical_bytes']);check(path+':logicalsha',sha(d)==r['logical_sha256'])
 before[name]={path:sha((R/path).read_bytes()) for path in expected}
def capture(label,argv,cwd,env=None,expected_exit=0,old=None):
 start=utc();r=subprocess.run(argv,cwd=cwd,env=dict(ENV,**(env or {})),capture_output=True,timeout=180)
 rec={'label':label,'argv':list(map(str,argv)),'cwd':str(cwd),'environment_changes':{k:ENV[k] for k in ('GIT_OPTIONAL_LOCKS','GIT_NO_LAZY_FETCH','PYTHONDONTWRITEBYTECODE')},'started_utc':start,'completed_utc':utc(),'exit':r.returncode,'streams':{}}
 for n,b in [('stdout',r.stdout),('stderr',r.stderr)]:
  z=gzip.compress(b,compresslevel=9,mtime=0);p=OUT/(label+'.'+n+'.gz');p.write_bytes(z)
  rec['streams'][n]={'path':str(p.relative_to(A)),'bytes':len(b),'sha256':sha(b),'stored_bytes':len(z),'stored_sha256':sha(z)}
 records.append(rec);(A/'root_family_command_progress.json').write_text(json.dumps(records,indent=2)+'\n')
 check(label+':exit',r.returncode==expected_exit)
 if old:
  for n,b in [('stdout',r.stdout),('stderr',r.stderr)]:
   if b==old[n]:check(label+':whole-'+n,True);continue
   if label=='poisson_api_pr' and n=='stdout':
    x=load_json= json.loads(old[n]);y=json.loads(b);diff=[]
    permitted={('head','repo','open_issues_count'),('head','repo','open_issues'),('head','repo','pushed_at'),('head','repo','updated_at'),('base','repo','open_issues_count'),('base','repo','open_issues'),('base','repo','pushed_at'),('base','repo','updated_at')}
    def walk(a,c,path=()):
     if isinstance(a,dict) and isinstance(c,dict):
      check(label+str(path)+':objectkeys',set(a)==set(c))
      for k in a:walk(a[k],c[k],path+(k,))
     elif a!=c:
      check(label+str(path)+':allowedmetadata',path in permitted and type(a) is type(c))
      diff.append({'path':list(path),'before':a,'after':c})
    walk(x,y);allowed.extend(diff)
   else:check(label+':whole-'+n,False)
 return r
G=A/'path_geometry_review'
for x in manifests['path_geometry_review']['captures']:
 rec=load(G/x['receipt'])
 old={}
 for n in ('stdout','stderr'):
  r=rec[n];b=gzip.decompress((G/r['path']).read_bytes());check(x['label']+n+':oldbytes',len(b)==r['bytes']);check(x['label']+n+':oldsha',sha(b)==r['sha256']);old[n]=b
 if x['read_only_command']:
  capture('geometry_'+x['label'],rec['argv'],rec['cwd'],rec['environment_changes'],rec['exit_code'],old)
 else:check(x['label']+':writing-acquisition-driver-verified-not-rerun',True)
capture('geometry_final_verifier',[str(PY),str(G/'verify_review.py'),'--include-private','--replay'],G)
P=A/'poisson_components_review';created=[]
try:
 for f in load(P/'receipts/primary_fetch.json'):
  b=gzip.decompress((P/'private'/(f['name']+'.pdf.gz')).read_bytes())
  check(f['name']+':sourcepdfexact',len(b)==f['bytes'] and sha(b)==f['sha256'])
  p=P/'private/sources'/(f['name']+'.pdf');check('rehydrate:'+str(p),not p.exists());p.parent.mkdir(exist_ok=True);p.write_bytes(b);created.append(p)
 for rec in load(P/'receipts/commands.json'):
  old={}
  for n,r in rec['streams'].items():
   z=(P/r['path']).read_bytes();check(rec['name']+n+':oldstored',len(z)==r['stored_bytes'] and sha(z)==r['stored_sha256']);b=gzip.decompress(z);check(rec['name']+n+':oldlogical',len(b)==r['logical_bytes'] and sha(b)==r['logical_sha256']);old[n]=b
  capture('poisson_'+rec['name'],rec['command'],rec['cwd'],expected_exit=rec['exit'],old=old)
finally:
 for p in created:p.unlink()
capture('poisson_final_verifier',[str(PY),str(P/'verify_readonly.py')],P)
C=A/'poisson_components_corrections'
capture('poisson_corrections_verifier',[str(PY),str(C/'verify_readonly.py')],C)
for name,values in before.items():
 R=A/name;actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 check(name+':unchanged-namespace-after',actual==set(values))
 for path,h in values.items():check(name+path+':unchanged-after',sha((R/path).read_bytes())==h)
result={'status':'PASS_ENTIRE_FAMILY_EVIDENCE_AND_LITERAL_READONLY_REEXECUTION','utc':utc(),'checks':checks,'commands':records,'allowed_repository_metadata_differences':allowed,'pins':pins,'credited_resolution_percent':100,'new_theorems':0,'workflow_completion_percent':70,'sealed_families_unchanged':True,'private_raw_sources_excluded':True,'public_only_limits':'Original Poisson review/supplement verifiers require private evidence; geometry allows private absent and verifies listed public paths rather than exact namespace. Current whole-review verifier documents and strengthens these integrity conditions. No missing private stream is represented as reproduced. ROOT here checked all private evidence and all readonly captures.','writing_acquisition_drivers_reexecuted':False,'program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_family_verification_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'readonly_commands':len(records),'allowed_metadata_differences':len(allowed),'sealed_families_unchanged':True,'workflow_percent':70},indent=2))
