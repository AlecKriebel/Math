#!/usr/bin/env python3
"""Independent negative controls; writes only this family's disposable tmp."""
import os,sys,json,hashlib,subprocess,shutil,socket,importlib.util,datetime,ast
from pathlib import Path
HERE=Path(__file__).resolve().parent;T=HERE/'tmp/hostile';T.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('guard',HERE/'guarded_replay.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SOURCE=HERE.parents[1]/'original/unsolved_math_prioritization/attempts/30003634';PYTHON='/Users/alec/Documents/Math/.venv/bin/python'
results=[];g.authenticate(SOURCE)
external=T/'BOOTSTRAP.py';shutil.copyfile(SOURCE/'BOOTSTRAP.py',external)
g.need(hashlib.sha256(external.read_bytes()).hexdigest()==g.PINS['BOOTSTRAP.py'][1],'external bootstrap identity')
def fresh(case):
 p=T/case;shutil.copytree(SOURCE,p)
 for x in p.rglob('*'):x.chmod(0o755 if x.is_dir()else 0o644)
 p.chmod(0o755);g.authenticate(p);return p

def jwrite(p,v):p.write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
def rebind(p,inner=None):
 if inner:
  folder,name=inner;f=p/folder/('AUDIT_MANIFEST.json'if folder=='audit1'else'MANIFEST.json');m=json.loads(f.read_text())
  for row in m['files']:
   if row['path']==name:
    raw=(p/folder/name).read_bytes();row.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
  jwrite(f,m)
 f=p/'PUBLICATION_MANIFEST.json';m=json.loads(f.read_text())
 for row in m['files']:
  path=p/row['path']
  if path.is_file()and not path.is_symlink():
   raw=path.read_bytes();row.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
 jwrite(f,m)

def probe(label,p,expect_old_reject=True):
 # The trusted immutable external bootstrap is authenticated before each call.
 g.need(hashlib.sha256(external.read_bytes()).hexdigest()==g.PINS['BOOTSTRAP.py'][1],'external identity drift')
 pin=hashlib.sha256((p/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()
 for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO']),('env2',[])]:
  env={k:v for k,v in os.environ.items()if not k.startswith('PYTHON')};env.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(T))
  if mode=='env2':env['PYTHONOPTIMIZE']='2'
  startup=[]if mode=='env2'else['-I']
  cp=subprocess.run([PYTHON,*startup,'-B',*flags,str(external),'--packet',str(p),'--expected-manifest',pin,'--check-only'],env=env,capture_output=True,text=True,timeout=20)
  # Source guard is our already reviewed external code, not any packet code.
  cg=subprocess.run([PYTHON,*startup,'-B',*flags,str(HERE/'guarded_replay.py'),'--packet',str(p),'--check-only'],env=env,capture_output=True,text=True,timeout=20)
  g.need(cg.returncode!=0,'current immutable guard accepted '+label)
  g.need((cp.returncode!=0)==expect_old_reject,'unexpected original behavior '+label+' '+cp.stderr)
  g.need('UNAUTHENTICATED_CODE_RAN'not in cp.stdout+cp.stderr,'unauthenticated code executed')
  results.append({'case':label,'mode':mode,'original_rejected':cp.returncode!=0,'original_diagnostic':cp.stderr.strip(),'current_guard_rejected':cg.returncode!=0,'current_guard_diagnostic':cg.stderr.strip(),'top_manifest_pin_fresh':True})
 (HERE/'HOSTILE_RESULTS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
 print(label,flush=True)
for name in ['empty_directory','extra_file','fifo','socket','executable_file','writable_directory','root_symlink','ancestor_symlink','directory_symlink','false_assert_code','verifier_code','bootstrap_code','certificate_status','certificate_bool_inertia','ledger_bool','false_count','false_top_status','false_top_turns','manifest_float_count','extra_missing_witness']:
 p=fresh(name)
 if name=='empty_directory':(p/'audit2/empty').mkdir()
 elif name=='extra_file':(p/'audit2/extra.py').write_text('print("UNAUTHENTICATED_CODE_RAN")')
 elif name=='fifo':(p/'README.md').unlink();os.mkfifo(p/'README.md')
 elif name=='socket':
  (p/'README.md').unlink();s=socket.socket(socket.AF_UNIX);old=os.getcwd()
  try:os.chdir(p);s.bind('README.md')
  finally:os.chdir(old);s.close()
 elif name=='executable_file':(p/'original/verify.py').chmod(0o755)
 elif name=='writable_directory':(p/'audit1').chmod(0o777)
 elif name=='root_symlink':
  link=T/'root_alias';link.symlink_to(p,target_is_directory=True);p=link
 elif name=='ancestor_symlink':
  parent=T/'ancestor_parent';parent.mkdir();dest=parent/'packet';shutil.move(str(p),dest);alias=T/'ancestor_alias';alias.symlink_to(parent,target_is_directory=True);p=alias/'packet'
 elif name=='directory_symlink':
  target=T/'external_audit1';shutil.move(str(p/'audit1'),target);(p/'audit1').symlink_to(target,target_is_directory=True)
 elif name=='false_assert_code':
  f=p/'original/verify.py';f.write_text('assert False\nprint("UNAUTHENTICATED_CODE_RAN")\n');rebind(p,('original','verify.py'))
 elif name=='verifier_code':(p/'VERIFY_PUBLICATION.py').write_text('print("UNAUTHENTICATED_CODE_RAN")\n');rebind(p)
 elif name=='bootstrap_code':(p/'BOOTSTRAP.py').write_text('print("UNAUTHENTICATED_CODE_RAN")\n');rebind(p)
 elif name in ['certificate_status','certificate_bool_inertia']:
  f=p/'original/certificate.json';x=json.loads(f.read_text())
  if name=='certificate_status':x['signature']=0
  else:x['goeritz_inertia'][2]=False
  jwrite(f,x);rebind(p,('original','certificate.json'))
 elif name=='ledger_bool':
  f=p/'original/ATTEMPT_LEDGER.json';x=json.loads(f.read_text());x['turns_used']=True;jwrite(f,x);rebind(p,('original','ATTEMPT_LEDGER.json'))
 elif name=='extra_missing_witness':(p/'original/certificate.json').unlink()
 else:
  f=p/'PUBLICATION_MANIFEST.json';x=json.loads(f.read_text())
  if name=='false_count':x['files']=x['files'][:-1]
  if name=='false_top_status':x['status']='accepted'
  if name=='false_top_turns':x['turns']='0/5'
  if name=='manifest_float_count':x['files'][0]['bytes']=float(x['files'][0]['bytes'])
  jwrite(f,x)
 probe(name,p,expect_old_reject=name!='ancestor_symlink')
# Wrong external anchor is separately exercised on a valid unmodified snapshot.
g.authenticate(SOURCE)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(T))
cp=subprocess.run([PYTHON,'-I','-B',str(external),'--packet',str(SOURCE),'--expected-manifest','0'*64,'--check-only'],env=env,capture_output=True,text=True,timeout=20)
g.need(cp.returncode!=0,'wrong external anchor accepted')
results.append({'case':'wrong_external_anchor','original_rejected':True,'diagnostic':cp.stderr.strip()})
(HERE/'HOSTILE_RESULTS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results,'case_count':21,'original_ancestor_symlink_acceptances':4,'current_guard_ancestor_rejections':4,'malicious_marker_never_executed':True},indent=2)+'\n')
