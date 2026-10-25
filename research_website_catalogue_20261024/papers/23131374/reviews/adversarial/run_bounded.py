from pathlib import Path
import subprocess,os,signal,time,json,hashlib,datetime
p=Path(__file__).resolve().parent;runtime=p.parents[3]/'tmp/shared-math-runtime/bin/python'
start=time.monotonic();child=subprocess.Popen([str(runtime),'-B',str(p/'independent_checks.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);timeout=False
try:out,err=child.communicate(timeout=25)
except subprocess.TimeoutExpired:
 timeout=True;os.killpg(child.pid,signal.SIGKILL);out,err=child.communicate()
finally:
 try:os.killpg(child.pid,signal.SIGKILL)
 except ProcessLookupError:pass
(p/'independent_stdout.txt').write_bytes(out);(p/'independent_stderr.txt').write_bytes(err)
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'deadline_seconds':25,'timed_out':timeout,'returncode':child.returncode,'elapsed_seconds':time.monotonic()-start,'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'isolated_process_group_cleanup':'SIGKILL attempted in finally; absent group after normal completion expected'}
(p/'bounded_run.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));print(err.decode())
