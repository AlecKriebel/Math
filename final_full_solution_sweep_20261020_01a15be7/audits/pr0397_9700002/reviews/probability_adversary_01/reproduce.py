#!/usr/bin/env python3
"""Reproduce immutable PR397 packet in a disposable private copy."""
from pathlib import Path
import datetime as dt, hashlib, json, os, platform, shutil, subprocess, sys, tempfile
BASE=Path(__file__).resolve().parents[2]
INPUT=BASE/'original'
OUT=Path(__file__).resolve().parent

def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def diff(a,b,path=''):
 if type(a)!=type(b):return [{'path':path,'before':a,'after':b,'type_changed':True}]
 if isinstance(a,dict):
  result=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:result.append({'path':path+'/'+k,'before':a.get(k),'after':b.get(k),'missing_key':True})
   else:result+=diff(a[k],b[k],path+'/'+k)
  return result
 if isinstance(a,list):
  if len(a)!=len(b):return [{'path':path,'length_before':len(a),'length_after':len(b)}]
  return [v for i,(x,y) in enumerate(zip(a,b)) for v in diff(x,y,path+'/'+str(i))]
 if a==b:return []
 item={'path':path,'before':a,'after':b}
 if isinstance(a,(int,float)) and isinstance(b,(int,float)):item['absolute_change']=abs(a-b)
 return [item]

if __name__=='__main__':
 original={str(p.relative_to(INPUT)):h(p) for p in INPUT.rglob('*') if p.is_file()}
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
 results=[]
 with tempfile.TemporaryDirectory(prefix='pr397-probability-',dir=str(OUT)) as td:
  cp=Path(td)/'packet';shutil.copytree(INPUT,cp)
  for file in ['turns/turn_01/check_model.py','turns/turn_02/check_model.py','review/portable_independent_checks.py']:
   shutil.copytree(INPUT,cp,dirs_exist_ok=True) # Restore immutable inputs for EACH standalone run.
   r=subprocess.run([sys.executable,'-B',str(cp/file)],cwd=cp,capture_output=True,text=True,env=env)
   stem=file.replace('/','_').removesuffix('.py')
   (OUT/(stem+'.stdout')).write_text(r.stdout);(OUT/(stem+'.stderr')).write_text(r.stderr)
   expected='review/INDEPENDENT_CHECKS.json' if file.startswith('review') else file.replace('check_model.py','CHECKS.json')
   generated='review/PORTABLE_INDEPENDENT_CHECKS.json' if file.startswith('review') else expected
   if r.returncode==0:
    after=json.loads((cp/generated).read_text());before=json.loads((INPUT/expected).read_text())
    (OUT/(stem+'_ACTUAL.json')).write_text(json.dumps(after,indent=2)+'\n')
    differences=diff(before,after)
    results.append({'script':file,'exit_code':r.returncode,'all_assertions_passed':after.get('all_assertions_passed'),'expected_sha256':h(INPUT/expected),'actual_sha256':h(cp/generated),'exact_bytes_match':h(INPUT/expected)==h(cp/generated),'differences':differences})
   else:results.append({'script':file,'exit_code':r.returncode,'stderr':r.stderr})
 after={str(p.relative_to(INPUT)):h(p) for p in INPUT.rglob('*') if p.is_file()}
 assert original==after
 import numpy,scipy
 receipt={'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'interpreter':sys.executable,'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,'frozen_inputs_unchanged':True,'results':results,'initial_attempts':[{'python':'default Python3.14','failure':'NumPy unavailable; no mathematical test executed.'},{'python':'bundled Python','failure':'SciPy unavailable; no mathematical test executed.'},{'python':'repository .venv Python3.9','failure':'REPLAY_ALL strict SHA comparison failed after first author script; semantic investigation follows in this receipt.'}]}
 (OUT/'REPLAY_DETAIL.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
