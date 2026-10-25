from pathlib import Path
import subprocess,os,signal,time,json,hashlib,datetime
P=Path(__file__).resolve().parent;runtime=P.parents[3]/'tmp/shared-math-runtime/bin/python'
p=subprocess.Popen([str(runtime),'-B',str(P/'independent_checks.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);start=time.monotonic();timed_out=False
try:out,err=p.communicate(timeout=25)
except subprocess.TimeoutExpired:timed_out=True;os.killpg(p.pid,signal.SIGKILL);out,err=p.communicate()
finally:
 try:os.killpg(p.pid,signal.SIGKILL)
 except ProcessLookupError:pass
(P/'independent_stdout.txt').write_bytes(out);(P/'independent_stderr.txt').write_bytes(err)
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'deadline_seconds':25,'timed_out':timed_out,'returncode':p.returncode,'elapsed_seconds':time.monotonic()-start,'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'cleanup':'isolated process group, SIGKILL attempted in finally; no group expected after normal completion'}
(P/'bounded_run.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));print(err.decode())
