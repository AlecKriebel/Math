#!/usr/bin/env python3
from pathlib import Path
import ast,datetime,hashlib,json,os,subprocess,sys,tempfile
R=Path(__file__).resolve().parent;A=R.parents[1];L=R/'_local'
def need(c,m):
    if not c:raise RuntimeError(m)
specs=[('reviews/source_only_math/CHECK_MOD2.py',None),('reviews/candidate_adversary/COMPUTATION.py','require'),('reviews/chow_computation/check_chow.py','require'),('reviews/finite_computation_adversary/check_independent.py','ensure')]
rows=[]
with tempfile.TemporaryDirectory(prefix='finite-negative-',dir=L) as tmp:
 root=Path(tmp)
 for index,(raw,guard) in enumerate(specs):
  data=(A/raw).read_text();need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(data))),'assert found '+raw)
  folder=root/str(index);folder.mkdir();program=folder/'checker.py'
  if guard is None:
   before='if (8, 0, 0, 4, 4) not in direct:';need(data.count(before)==1,'decisive guard selector')
   program.write_text(data.replace(before,'if True:'))
   launch=program
  else:
   program.write_text(data);launch=folder/'false_guard.py'
   launch.write_text("import runpy\nm=runpy.run_path("+repr(str(program))+")\nm["+repr(guard)+"](False,'ROUND1_FALSE_GUARD')\n")
  modes=[]
  for flags in [[],['-O'],['-OO']]:
   p=subprocess.run([sys.executable,'-B',*flags,str(launch)],cwd=folder,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
   expected='Expected decisive coefficient is not one' if guard is None else 'ROUND1_FALSE_GUARD'
   need(p.returncode!=0 and expected in p.stderr,'false mathematical guard survived silently '+raw)
   modes.append({'flags':flags,'nonzero_exit':p.returncode,'decisive_message_verified':True})
  rows.append({'program':raw,'source_sha256':hashlib.sha256(data.encode()).hexdigest(),'AST_assert_count':0,'false_guard_controls':modes})
out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'controls':rows,'scope':'Deliberately false finite-program guards on own temporary copies; no original files changed.'}
(R/'FINITE_NEGATIVE_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','programs':len(rows),'guard_failures_observed':12}))
