"""Inspected supplied programs replayed in a fresh own-folder quarantine only."""
from pathlib import Path
import subprocess,os,signal,time,json,datetime,shutil,hashlib
p=Path(__file__).resolve().parent;src=p.parents[1]/'sources/published-source/source_preparation';q=p/'cache/supplied-quarantine';q.mkdir(exist_ok=False);(q/'historical').mkdir();(q/'tmp').mkdir();copied=[]
for name in ['run_checks.py','verify_exact.py','PROOF_BINDING.json','root_dependent_spanning_trees.tex','historical/PROOF.md']:
 f=src/name;g=q/name;shutil.copyfile(f,g);assert f.read_bytes()==g.read_bytes();copied.append({'path':name,'bytes':g.stat().st_size,'sha256':hashlib.sha256(g.read_bytes()).hexdigest()})
(p/'supplied_quarantine_bindings.json').write_text(json.dumps(copied,indent=2)+'\n')
start=time.monotonic();process=None;receipt={}
try:
 env=os.environ.copy();env['TMPDIR']=str(q/'tmp');env['PYTHONDONTWRITEBYTECODE']='1'
 process=subprocess.Popen(['/Users/alec/Documents/Math/research_website_catalogue_20261024/tmp/shared-math-runtime/bin/python','-I','-B',str(q/'run_checks.py'),'--output',str(p/'supplied_replay_receipt.json')],cwd=q,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 out,err=process.communicate(timeout=25);(p/'supplied_replay.stdout.txt').write_text(out);(p/'supplied_replay.stderr.txt').write_text(err)
 receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-start,'returncode':process.returncode,'timeout_seconds':25,'all_execution_in_own_quarantine':True,'historical_programs_executed':False,'process_group_cleanup':'SIGKILLfinallyincludingdescendants'}
except subprocess.TimeoutExpired:
 receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-start,'timed_out':True}
finally:
 if process:
  try:os.killpg(process.pid,signal.SIGKILL)
  except ProcessLookupError:pass
 (p/'supplied_replay_run.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
