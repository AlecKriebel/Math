from pathlib import Path
import subprocess,os,signal,time,json,datetime
p=Path(__file__).resolve().parent;start=time.monotonic();proc=None;receipt={}
try:
 proc=subprocess.Popen(['/Users/alec/Documents/Math/research_website_catalogue_20261024/tmp/shared-math-runtime/bin/python','-I','-B',str(p/'independent_algebra.py')],cwd=p/'cache',stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 out,err=proc.communicate(timeout=25);(p/'own_algebra.stdout.json').write_text(out);(p/'own_algebra.stderr.txt').write_text(err);receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-start,'returncode':proc.returncode,'timeout_seconds':25,'processgroup_cleanup':'SIGKILLfinallyincludingdescendants'}
except subprocess.TimeoutExpired:receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-start,'timed_out':True}
finally:
 if proc:
  try:os.killpg(proc.pid,signal.SIGKILL)
  except ProcessLookupError:pass
 (p/'own_algebra_run.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
