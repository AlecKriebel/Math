#!/usr/bin/env python3
import hashlib,json,os,shutil,subprocess,sys,zipfile
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parents[1];P=A/'publication';PY=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python');PIN='b1881fcc385141e3f54a24dcc04cc35d4b76365a588cd18c2e832a4a4efb8364'
def require(x,s):
 if not x:raise RuntimeError(s)
def equivalent(a,b):
 require(type(a) is type(b),'type')
 if type(a) is dict:
  require(a.keys()==b.keys(),'keys')
  for k in a:equivalent(a[k],b[k])
 elif type(a) is list:
  require(len(a)==len(b),'length')
  for x,y in zip(a,b):equivalent(x,y)
 else:require(a==b,'value')
def main():
 import AUTHENTICATE,argparse
 global P
 ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path);ap.add_argument('--result-dir',type=Path);args=ap.parse_args();R=(args.result_dir or D).resolve();R.mkdir(parents=True,exist_ok=True)
 if args.candidate:P=args.candidate.resolve()
 AUTHENTICATE.run(P);tmp=R/'tmp';tmp.mkdir(exist_ok=True);bundle=tmp/'bundle'
 if bundle.exists():shutil.rmtree(bundle)
 with zipfile.ZipFile(P/'rotational-veech-source-verification-v1.0.zip') as z:z.extractall(bundle)
 require(hashlib.sha256((bundle/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest()==PIN,'manifest')
 rows=[];results=[]
 for mode,flags,opt in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('env2',[],'2')]:
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
  if opt:env['PYTHONOPTIMIZE']=opt
  p=subprocess.run([str(PY),*flags,str(bundle/'verify_package.py'),'--expected-manifest',PIN,'--pdf',str(P/'output/pdf/note.pdf'),'--workdir',str(tmp/'scratch'/mode)],capture_output=True,text=True,env=env,timeout=1800)
  (tmp/(mode+'.stdout')).write_text(p.stdout);(tmp/(mode+'.stderr')).write_text(p.stderr);require(p.returncode==0,mode+': '+p.stderr);r=json.loads(p.stdout);require(r['status']=='PASS',mode);results.append(r);rows.append({'mode':mode,'status':'PASS','stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest()})
 for r in results[1:]:equivalent(results[0],r)
 (R/'REPLAY_RECEIPT.json').write_text(json.dumps({'status':'PASS','four_modes_strict_recursive_type_key_value_identical':True,'rows':rows,'full_result':results[0]},indent=2)+'\n')
 code=R/'reviewed_code';code.mkdir(exist_ok=True)
 for name in ['package_guard_challenges.py','copy_guard_challenge.py']:
  shutil.copyfile(P/name,code/name)
  args=[str(PY),str(code/name),'--bundle',str(bundle),'--python',str(PY),'--output',str(R/('CURRENT_GUARDS.json' if name.startswith('package') else 'COPY_GUARDS.json'))]
  if name.startswith('copy'):args+=['--expected-manifest',PIN,'--workdir',str(tmp/'copy_controls')]
  p=subprocess.run(args,capture_output=True,text=True,timeout=600);require(p.returncode==0,p.stderr);print(p.stdout)
 print(json.dumps({'status':'PASS','full_modes':4}))
if __name__=='__main__':main()
