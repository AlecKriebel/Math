import hashlib,json,os,shutil,subprocess,zipfile
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parent;A=R.parents[1];D=A/'publication';T=R/'private/cold';T.mkdir(parents=True,exist_ok=False);B=T/'extracted';B.mkdir()
PYTHON='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
manifest='9154385c51af3948347f029ada48a7cff51ae9736aed84bdd3eba198a5de034c';verifier='7f661daf498cd151ddd5fd44eb0d7d763b8bdfdbf7c12262dc5255a0133a4bc6'
def need(v,s):
 if not v:raise RuntimeError(s)
def exact(a,b):
 need(type(a) is type(b),'scalar/container type')
 if isinstance(a,dict):
  need(a.keys()==b.keys(),'keys')
  for k in a:exact(a[k],b[k])
 elif isinstance(a,list):
  need(len(a)==len(b),'length')
  for x,y in zip(a,b):exact(x,y)
 else:need(a==b,'value')
with zipfile.ZipFile(D/'deep-derived-pure-braids-source-verification-v1.0.zip') as z:
 for i in z.infolist():
  p=B/i.filename;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(i));p.chmod((i.external_attr>>16)&0o777)
need(hashlib.sha256((B/'verify_package.py').read_bytes()).hexdigest()==verifier,'external verifier pin')
need(hashlib.sha256((B/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest()==manifest,'external manifest pin')
rows=[];boot='import sys,json,runpy; print(json.dumps({"observed_outer_optimization":sys.flags.optimize}),file=sys.stderr); sys.argv=sys.argv[1:];runpy.run_path(sys.argv[0],run_name="__main__")'
for mode,flags,opt,want in [('normal',[],None,0),('O',['-O'],None,1),('OO',['-OO'],None,2),('env2',[],'2',2)]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
 if opt is not None:env['PYTHONOPTIMIZE']=opt
 p=subprocess.run([PYTHON,*flags,'-B','-c',boot,str(B/'verify_package.py'),'--expected-manifest',manifest,'--pdf',str(D/'output/pdf/note.pdf'),'--workdir',str(T/'work')],env=env,cwd=T,capture_output=True,text=True,timeout=1800)
 (T/(mode+'.stdout')).write_text(p.stdout);(T/(mode+'.stderr')).write_text(p.stderr);need(p.returncode==0,mode+': '+p.stderr)
 observed=json.loads(p.stderr.splitlines()[0])['observed_outer_optimization'];need(type(observed) is int and observed==want,'outer mode')
 receipt=json.loads(p.stdout);exact(receipt,json.loads((D/('PACKAGE_REPLAY_'+mode+'.json')).read_bytes()))
 rows.append({'mode':mode,'observed_outer_optimization':observed,'returncode':p.returncode,'receipt':receipt});print(mode+' PASS actual optimize='+str(observed),flush=True)
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','package_manifest_sha256':manifest,'externally_pinned_verifier_sha256':verifier,'cold_extraction':True,'modes':rows}
(R/'COLD_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
# Actual authenticated guard helpers copied outside the closed archive; output confined here.
for name in ['package_guard_challenges.py','copy_guard_challenge.py']:shutil.copyfile(D/name,T/name)
for name,args in [('package_guard_challenges.py',['--bundle',str(B),'--python',PYTHON,'--output',str(R/'GUARD_REPLAY.json')]),('copy_guard_challenge.py',['--bundle',str(B),'--expected-manifest',manifest,'--python',PYTHON,'--output',str(R/'COPY_REPLAY.json'),'--workdir',str(T/'copywork')])]:
 p=subprocess.run([PYTHON,'-B',str(T/name),*args],capture_output=True,text=True,cwd=T,timeout=300);(T/(name+'.stdout')).write_text(p.stdout);(T/(name+'.stderr')).write_text(p.stderr);need(p.returncode==0,name+': '+p.stderr);print(name+' PASS',flush=True)
