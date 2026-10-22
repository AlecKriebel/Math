#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,json,hashlib,datetime,concurrent.futures
R=Path(__file__).resolve().parent;CODE=R/'independent_polytope_control.py'
def one(opt,bad):
 args=[sys.executable,'-B']+(['-O'] if opt else [])+[str(CODE)]+(['--force-failure'] if bad else [])
 t=datetime.datetime.now(datetime.UTC).isoformat();p=subprocess.run(args,capture_output=True)
 label=('optimized' if opt else 'normal');where=R/('tmp/forced_'+label if bad else 'RESULTS.'+label+'.json')
 if bad:
  where.with_suffix('.stdout').write_bytes(p.stdout);where.with_suffix('.stderr').write_bytes(p.stderr)
  if p.returncode==0 or b'three-point exact value' not in p.stderr:raise RuntimeError('inactive mathematical forced failure')
 else:
  where.write_bytes(p.stdout)
  if p.returncode:raise RuntimeError(p.stderr.decode())
  if json.loads(p.stdout)['status']!='PASS':raise RuntimeError('failed status')
 return {'optimized':opt,'forced_corrupt_iid_substitution':bad,'exit_code':p.returncode,'started_utc':t,'stdout_bytes':len(p.stdout),'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_bytes':len(p.stderr),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest(),'expected_failure_message':('three-point exact value (forced corrupt iid substitution if requested)' if bad else None)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:runs=list(ex.map(lambda a:one(*a),[(False,False),(True,False),(False,True),(True,True)]))
a=(R/'RESULTS.normal.json').read_bytes();b=(R/'RESULTS.optimized.json').read_bytes()
if a!=b:raise RuntimeError('optimization result drift')
obj={'utc':datetime.datetime.now(datetime.UTC).isoformat(),'status':'PASS','python':sys.version,'code':{'bytes':CODE.stat().st_size,'sha256':hashlib.sha256(CODE.read_bytes()).hexdigest()},'normal_optimized_byte_equal':True,'runs':runs}
(R/'INDEPENDENT_REPLAY.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n');print(json.dumps(obj,indent=2))
