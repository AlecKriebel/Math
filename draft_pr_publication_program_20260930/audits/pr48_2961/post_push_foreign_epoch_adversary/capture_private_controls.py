"""Run only the handwritten private audit controls; preserve true child evidence."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, subprocess, sys, traceback
F=Path(__file__).absolute().parent
script=F/'private_review_controls.py'
d=F/'actual_private_control_capture'
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def record(p):
    b=p.read_bytes();return dict(path=p.name,bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
os.umask(0o022)
d.mkdir(exist_ok=False)
source=script.read_bytes();operator=Path(__file__).read_bytes()
put(d/'PRELAUNCH_SOURCE.py',source);put(d/'PRELAUNCH_OPERATOR.py',operator)
argv=['/usr/bin/python3','-B',str(script)]
pre=dict(schema='pr48-independent-private-prelaunch/v1',argv=argv,cwd=str(F),prepared_utc=stamp(),operator_pid=os.getpid(),source=record(script),operator=record(Path(__file__)),stdin_supplied=False,candidate_or_production_execution=False)
put(d/'PRELAUNCH.json',(json.dumps(pre,indent=2,sort_keys=True)+'\n').encode())
c=dict(pre,schema='pr48-independent-private-actual-capture/v1',started_utc=stamp(),actual_execution=False,completed=False,pid=None,exit_code=None);child=None;out=err=b''
try:
    child=subprocess.Popen(argv,cwd=F,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0'))
    c.update(actual_execution=True,pid=child.pid);out,err=child.communicate();c.update(completed=True,exit_code=child.returncode)
except BaseException:
    c['operator_error']=traceback.format_exc()
    if child is not None:out,err=child.communicate();c.update(completed=True,exit_code=child.returncode)
for k,b in [('stdout',out),('stderr',err)]:put(d/(k+'.bin'),b);c[k]=record(d/(k+'.bin'))
c.update(finished_utc=stamp(),source_unchanged=script.read_bytes()==source==(d/'PRELAUNCH_SOURCE.py').read_bytes(),operator_unchanged=Path(__file__).read_bytes()==operator==(d/'PRELAUNCH_OPERATOR.py').read_bytes(),source_fullmode_unchanged=stat.S_IMODE(script.stat().st_mode)==pre['source']['full_mode'],operator_fullmode_unchanged=stat.S_IMODE(Path(__file__).stat().st_mode)==pre['operator']['full_mode'])
c['status']='PASS_PRIVATE_ONLY' if c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and err==b'' and all(c[k] is True for k in ['source_unchanged','operator_unchanged','source_fullmode_unchanged','operator_fullmode_unchanged']) and 'operator_error' not in c else 'FAIL_PRIVATE_ONLY'
put(d/'CAPTURE.json',(json.dumps(c,indent=2,sort_keys=True)+'\n').encode())
print(json.dumps(dict(status=c['status'],actual_pid=c['pid'],actual_exit_code=c['exit_code'],capture=str(d/'CAPTURE.json'))))
if c['status']!='PASS_PRIVATE_ONLY':sys.exit(1)
