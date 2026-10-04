"""Actual operator for independent private specification controls only."""
from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess,sys
F=Path(__file__).absolute().parent;R=F.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def ref(p):
 b=p.read_bytes();return dict(path=p.name,bytes=len(b),sha256=sha(b))
source=F/'private_controls.py';body=source.read_bytes();operator=Path(__file__).read_bytes();(F/'PRIVATE_PRELAUNCH_SOURCE.py').write_bytes(body);(F/'PRIVATE_PRELAUNCH_OPERATOR.py').write_bytes(operator)
argv=[sys.executable,'-B',str(source)];cap=dict(schema='pr48-v3-independent-private-actual-capture/v1',argv=argv,cwd=str(R),operator_pid=os.getpid(),started_utc=now(),stdin_supplied=False,prelaunch_source=ref(F/'PRIVATE_PRELAUNCH_SOURCE.py'),prelaunch_operator=ref(F/'PRIVATE_PRELAUNCH_OPERATOR.py'),actual_execution=False,completed=False,pid=None,exit_code=None)
p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0'));cap.update(actual_execution=True,pid=p.pid);out,err=p.communicate();cap.update(completed=True,exit_code=p.returncode,finished_utc=now(),source_unchanged=source.read_bytes()==body,operator_unchanged=Path(__file__).read_bytes()==operator)
for n,b in [('PRIVATE_STDOUT.json',out),('PRIVATE_STDERR.bin',err)]:
 with (F/n).open('xb') as f:f.write(b)
cap.update(stdout=ref(F/'PRIVATE_STDOUT.json'),stderr=ref(F/'PRIVATE_STDERR.bin'),status='PASS' if p.returncode==0 and err==b'' and cap['source_unchanged'] and cap['operator_unchanged'] else 'FAIL');(F/'PRIVATE_CAPTURE.json').write_text(json.dumps(cap,indent=2)+'\n');print(json.dumps(cap));assert cap['status']=='PASS'
