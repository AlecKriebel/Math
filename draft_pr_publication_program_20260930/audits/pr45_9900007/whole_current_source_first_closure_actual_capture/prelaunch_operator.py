"""Actual own final closure outer, kept beside the self-only family to avoid circularity."""
from pathlib import Path
import subprocess,datetime,hashlib,os,sys,json
P=Path(__file__).resolve().parent;D=P.parent/'whole_current_source_first_closure_actual_capture';S=P/'close_family.py'
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,o):(D/n).write_text(json.dumps(o,indent=2)+'\n')
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','')not in ('','0'):raise RuntimeError('nonoptimized outer')
D.mkdir(exist_ok=False);source=S.read_bytes();operator=Path(__file__).read_bytes()
(D/'prelaunch_source.py').write_bytes(source);(D/'prelaunch_operator.py').write_bytes(operator)
argv=[sys.executable,str(S)];pre={'schema':'pr45-own-self-closure-prelaunch/v1','operator_pid':os.getpid(),'prepared_utc':stamp(),'child_argv':argv,'cwd':str(P),'source_sha256':sha(source),'operator_sha256':sha(operator),'completed_capture_does_not_exist_prelaunch':True}
write('PRELAUNCH.json',pre);start=stamp();child=subprocess.Popen(argv,cwd=P,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'PYTHONOPTIMIZE':'0'})
write('LAUNCHED.json',{'child_pid':child.pid,'operator_pid':os.getpid(),'start_utc':start,'child_argv':argv})
out,err=child.communicate();end=stamp();(D/'stdout.bin').write_bytes(out);(D/'stderr.bin').write_bytes(err)
cap={**pre,'schema':'pr45-own-complete-self-closure-capture/v1','child_pid':child.pid,'start_utc':start,'end_utc':end,'exit_code':child.returncode,'completed':True,'actual_execution':True,'stdin_supplied':False,'stdout':{'path':'stdout.bin','bytes':len(out),'sha256':sha(out)},'stderr':{'path':'stderr.bin','bytes':len(err),'sha256':sha(err)},'source_unchanged':S.read_bytes()==source,'operator_unchanged':Path(__file__).read_bytes()==operator,'future_native_acceptance_approved':False}
write('CAPTURE.json',cap)
for q in D.iterdir():q.chmod(0o444)
print(json.dumps({'capture_path':str(D),'capture_sha256':sha((D/'CAPTURE.json').read_bytes()),'child_pid':child.pid,'operator_pid':os.getpid(),'exit_code':child.returncode,'stdout_bytes':len(out),'stderr_bytes':len(err)},indent=2));sys.exit(child.returncode)
