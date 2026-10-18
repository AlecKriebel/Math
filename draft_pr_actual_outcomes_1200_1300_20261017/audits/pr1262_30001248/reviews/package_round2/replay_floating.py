#!/usr/bin/env python3
"""Copy hash-identical retained checks into scratch and run normal Python only."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys
R=Path(__file__).resolve().parent;A=R.parents[1];runs=[]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
for family,program,result in [('source_question_family','finite_checks.py','finite_checks.json'),('reconstruction_adversary','independent_checks.py','independent_checks.json'),('fourier_adversary','verify_fourier.py','FINITE_CONTROLS.json')]:
 p=A/'reviews'/family/program;d=R/'_local/floating'/family;d.mkdir(parents=True,exist_ok=True);q=d/program;shutil.copyfile(p,q)
 if hashlib.sha256(q.read_bytes()).digest()!=hashlib.sha256(p.read_bytes()).digest():raise RuntimeError('copy drift')
 run=subprocess.run([sys.executable,'-B',str(q)],cwd=d,env=env,capture_output=True,text=True,timeout=180)
 if run.returncode:raise RuntimeError(run.stderr)
 fresh=json.loads((d/result).read_text());runs.append({'family':family,'program_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'normal_only':True,'own_tolerances_assertions_passed':True,'stdout':json.loads(run.stdout),'fresh_result':fresh})
(R/'FLOATING_REPLAYS.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','comparison':'Normal-only execution under original explicit assertions/tolerances; no bitwise floating-output portability requirement.','runs':runs},indent=2)+'\n');print(json.dumps({'status':'PASS','normal_only_programs':len(runs)}))
