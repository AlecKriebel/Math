from pathlib import Path
from datetime import datetime,timezone
import subprocess,os,json,concurrent.futures
O=Path(__file__).resolve().parent;B=O.parent
script=B/'publication_package_v2/materials/verification/run_checks.py'
dep=B.parent/'pr200_5100007/math_algebra_family_01/runtime_packages'
if not dep.is_dir():raise RuntimeError(str(dep))
tmp=O/'runtime_tmp';tmp.mkdir(exist_ok=True)
env=os.environ.copy();env.update(PYTHONPATH=str(dep),PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(tmp))
rows=[('normal',[]),('optimized',['-O']),('guard_false',[],['--guard-false']),('guard_false_optimized',['-O'],['--guard-false']),('legacy_replay',[],['--legacy-replay'])]
def run(row):
 name,opts,*tail=row;args=tail[0] if tail else []
 cmd=['/opt/homebrew/opt/python@3.14/bin/python3.14','-B',*opts,str(script),*args]
 r=subprocess.run(cmd,cwd=O,env=env,text=True,capture_output=True)
 (O/(name+'.stdout')).write_text(r.stdout);(O/(name+'.stderr')).write_text(r.stderr)
 expected='guard_false' in name
 if expected:
  if r.returncode==0 or 'DELIBERATE FALSE CONDITION' not in r.stderr:raise RuntimeError(name+' false guard incorrectly accepted')
 elif r.returncode:raise RuntimeError(name+' failed '+r.stderr[-2000:])
 return {'name':name,'returncode':r.returncode,'expected_failure':expected,'command':cmd}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as x:results=list(x.map(run,rows))
(O/'SUPPORTED_CHECK_RESULTS.json').write_text(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','dependency_root':str(dep),'results':results},indent=2)+'\n')
print(json.dumps(results,indent=2))
