#!/usr/bin/env python3
"""Reproduce the authenticated publication archive in four outer modes."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time
HERE=Path(__file__).resolve().parent
PIN='eff4b4b19c1d931d3f067af7261c315a33452b732ba1c647163e3995804f5b39'
def main():
 root=HERE/'tmp/bundle';work=HERE/'tmp/replay_work';work.mkdir(exist_ok=True)
 rows=[];results=[]
 for mode,flags,opt in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('env2',[],'2')]:
  env=dict(os.environ,TMPDIR=str(work),PYTHONDONTWRITEBYTECODE='1')
  env.pop('PYTHONOPTIMIZE',None)
  if opt:env['PYTHONOPTIMIZE']=opt
  before=time.monotonic()
  p=subprocess.run([sys.executable,*flags,str(root/'verify_package.py'),'--expected-manifest',PIN,'--pdf',str(HERE.parents[1]/'publication/output/pdf/note.pdf'),'--workdir',str(work)],env=env,capture_output=True,text=True,timeout=1800)
  (HERE/'tmp'/f'replay_{mode}.stderr').write_text(p.stderr)
  (HERE/'tmp'/f'replay_{mode}.stdout').write_text(p.stdout)
  if p.returncode:raise RuntimeError(mode+' failed: '+p.stderr)
  result=json.loads(p.stdout)
  if result['status']!='PASS' or result['worker_optimization']!=0:raise RuntimeError('wrong replay result')
  (HERE/f'REPLAY_{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
  results.append(result)
  rows.append({'mode':mode,'seconds':time.monotonic()-before,'status':result['status'],'worker_optimization':result['worker_optimization'],'children':len(result['child_execution_guards'])})
 if not all(r==results[0] for r in results):raise RuntimeError('outer modes disagree')
 out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'package_manifest_sha256':PIN,'outer_modes_identical':True,'rows':rows}
 (HERE/'REPLAY_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
