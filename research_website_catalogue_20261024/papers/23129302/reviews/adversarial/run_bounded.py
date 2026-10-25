from pathlib import Path
import subprocess,sys,os,signal,time,json,hashlib,datetime
P=Path(__file__).resolve().parent
runtime=P.parents[3]/'tmp/shared-math-runtime/bin/python'
start=time.monotonic();proc=subprocess.Popen([str(runtime),'-B',str(P/'independent_checks.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
timed_out=False
try:
 out,err=proc.communicate(timeout=25)
except subprocess.TimeoutExpired:
 timed_out=True;os.killpg(proc.pid,signal.SIGKILL);out,err=proc.communicate()
finally:
 try:os.killpg(proc.pid,signal.SIGKILL)
 except ProcessLookupError:pass
(P/'independent_stdout.txt').write_bytes(out);(P/'independent_stderr.txt').write_bytes(err)
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'deadline_seconds':25,'timed_out':timed_out,'returncode':proc.returncode,'elapsed_seconds':time.monotonic()-start,'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'cleanup':'new process group; SIGKILL attempted in finally; absence expected after normal completion'}
(P/'bounded_run.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));print(err.decode())
