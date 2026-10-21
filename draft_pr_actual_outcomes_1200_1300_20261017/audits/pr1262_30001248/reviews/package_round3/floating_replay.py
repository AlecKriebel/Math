from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys
R=Path(__file__).resolve().parent;A=R.parents[1];rows=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
for raw in ['reviews/source_question_family/finite_checks.py','reviews/reconstruction_adversary/independent_checks.py','reviews/fourier_adversary/verify_fourier.py']:
 source=A/raw;scratch=R/'_local/floating'/source.parent.name;scratch.mkdir(parents=True,exist_ok=True);target=scratch/source.name;shutil.copyfile(source,target)
 sh=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 if sh(source)!=sh(target):raise RuntimeError('copy differs')
 p=subprocess.run([sys.executable,'-B',str(target)],capture_output=True,text=True,env=env,timeout=180)
 if p.returncode:raise RuntimeError(p.stderr)
 obj=json.loads(p.stdout);rows.append({'program':raw,'sha256':sh(source),'normal_only':True,'PYTHONOPTIMIZE_unset':True,'result':obj})
out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','runs':rows,'limits':'Only copied audit-authored checkers. Their own assertions/tolerances remain active; no optimized run or bitwise floating comparison. No source-author code or asymptotic proof is executed.'}
(R/'FLOATING_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','normal_only_checkers':len(rows)}))
