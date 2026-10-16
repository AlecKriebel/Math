#!/usr/bin/env python3
"""Replay frozen release from a fresh extraction, never modifying candidate."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,datetime,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
A=HERE.parent.parent
P=A/'publication/reviewed_candidates/candidate01'
PYTHON=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python')
PIN='e2b2f091451dddc4e69032d05ba94b46fddaf49bd9e610f61a43692cb2ffc487'
def need(c,m):
 if not c: raise RuntimeError(m)
def strict(b):
 def pairs(xs):
  d={}
  for k,v in xs:
   need(k not in d,'duplicate key'); d[k]=v
  return d
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def same(x,y):
 need(type(x) is type(y),'JSON type mismatch')
 if isinstance(x,dict):
  need(x.keys()==y.keys(),'JSON keys mismatch')
  for k in x:same(x[k],y[k])
 elif isinstance(x,list):
  need(len(x)==len(y),'JSON length mismatch')
  for a,b in zip(x,y):same(a,b)
 else: need(x==y,'JSON value mismatch')
def main():
 global P
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate',type=Path,default=P);ap.add_argument('--output-dir',type=Path,default=HERE);args=ap.parse_args();P=args.candidate.absolute();output=args.output_dir.absolute();output.mkdir(parents=True,exist_ok=True)
 (HERE/'tmp').mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory(dir=HERE/'tmp',prefix='independent_replay_') as td:
  t=Path(td); bundle=t/'package'
  with zipfile.ZipFile(P/'rotational-veech-source-verification-v1.0.zip') as z:z.extractall(bundle)
  results={}
  for label,flags,opt in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('env2',[],'2')]:
   env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
   if opt:env['PYTHONOPTIMIZE']=opt
   cmd=[str(PYTHON),*flags,str(bundle/'verify_package.py'),'--expected-manifest',PIN,'--pdf',str(P/'output/pdf/note.pdf'),'--workdir',str(t/'scratch')]
   p=subprocess.run(cmd,env=env,cwd=t,text=True,capture_output=True,timeout=1800)
   (output/('REPLAY_'+label+'.stdout')).write_text(p.stdout);(output/('REPLAY_'+label+'.stderr')).write_text(p.stderr)
   need(p.returncode==0,label+' failure '+p.stderr);results[label]=strict(p.stdout)
   if label!='normal':same(results['normal'],results[label])
   print(label+' PASS',flush=True)
  guards={}
  for name,args in [('package_guard_challenges.py',['--bundle',str(bundle),'--python',str(PYTHON),'--output',str(output/'CURRENT_GUARDS.json')]),('copy_guard_challenge.py',['--bundle',str(bundle),'--python',str(PYTHON),'--expected-manifest',PIN,'--output',str(output/'COPY_GUARDS.json'),'--workdir',str(t/'copy_work')])]:
   guard=t/name;shutil.copy2(P/name,guard)
   p=subprocess.run([str(PYTHON),str(guard),*args],text=True,capture_output=True,timeout=300)
   need(p.returncode==0,name+' failure '+p.stderr);guards[name]={'status':'PASS','executed_sha256':hashlib.sha256(guard.read_bytes()).hexdigest()}; print(name+' PASS',flush=True)
  receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','outer_modes':list(results),'strict_full_json_identical':True,'replay_output_sha256':hashlib.sha256((output/'REPLAY_normal.stdout').read_bytes()).hexdigest(),'guards':guards,'fresh_extraction':True,'candidate_never_executed_or_mutated':True}
  (output/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
if __name__=='__main__':main()
