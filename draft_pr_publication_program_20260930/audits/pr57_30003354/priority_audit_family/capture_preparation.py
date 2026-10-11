"""Actual private read-only readiness capture, not a ROOT or mathematical verdict."""
from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess,sys
F=Path(__file__).absolute().parent
q=F/'verify_preparation.py';source=q.read_bytes()
with (F/'verify_preparation_prelaunch.py').open('xb') as f:f.write(source)
cmd=[sys.executable,str(q)];start=dt.datetime.now(dt.timezone.utc).isoformat()
child=subprocess.Popen(cmd,cwd=F,stdout=subprocess.PIPE,stderr=subprocess.PIPE);a,b=child.communicate()
end=dt.datetime.now(dt.timezone.utc).isoformat()
with (F/'readiness.stdout.bin').open('xb') as f:f.write(a)
with (F/'readiness.stderr.bin').open('xb') as f:f.write(b)
out=dict(schema='pr57-priority-actual-private-readiness-capture/v1',caller_pid=os.getpid(),child_pid=child.pid,argv=cmd,cwd=str(F),started_utc=start,finished_utc=end,exit_code=child.returncode,source_sha256=hashlib.sha256(source).hexdigest(),operator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),complete_stdout=dict(path='readiness.stdout.bin',bytes=len(a),sha256=hashlib.sha256(a).hexdigest()),complete_stderr=dict(path='readiness.stderr.bin',bytes=len(b),sha256=hashlib.sha256(b).hexdigest()),ROOT_execution_or_approval=False)
with (F/'READINESS_CAPTURE.json').open('x') as f:json.dump(out,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps(out));sys.exit(child.returncode)
