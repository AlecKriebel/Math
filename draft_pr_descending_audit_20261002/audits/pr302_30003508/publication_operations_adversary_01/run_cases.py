"""Actual local process capture; no service invocation."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,stat,subprocess,sys
W=Path(__file__).resolve().parent
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),resolved_path=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
def write(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def utc():return datetime.now(timezone.utc).isoformat()
C=W/'actual_isolated_cases_01';C.mkdir(exist_ok=False)
sources=[]
for n in ['run_cases.py','isolated_cases.py']:
 p=W/n;q=C/(n+'.gz');q.write_bytes(gzip.compress(p.read_bytes(),mtime=0));q.chmod(0o444)
 if gzip.decompress(q.read_bytes())!=p.read_bytes():raise RuntimeError('Source archive differs')
 sources.append(dict(input=pin(p),stored_full_source=pin(q)))
argv=['/opt/homebrew/bin/python3','-E','-B',str(W/'isolated_cases.py')]
request=dict(actual_launcher_PID=os.getpid(),argv=argv,cwd=str(W),requested_UTC=utc(),prelaunch_full_sources=sources,resolved_interpreter=pin(Path(argv[0]).resolve()),no_service_calls=True)
write(C/'request.json',request);start=utc();p=subprocess.Popen(argv,cwd=W,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
write(C/'started.json',dict(actual_PID=p.pid,start_UTC=start,state='STARTED_OUTCOME_PENDING'))
timeout=False
try:out,err=p.communicate(timeout=55)
except subprocess.TimeoutExpired:timeout=True;p.kill();out,err=p.communicate()
result=dict(request,actual_PID=p.pid,start_UTC=start,end_UTC=utc(),exit_code=p.returncode,timed_out=timeout)
for n,b in [('stdout',out),('stderr',err)]:
 q=C/(n+'.bin.gz');q.write_bytes(gzip.compress(b,mtime=0));q.chmod(0o444)
 if gzip.decompress(q.read_bytes())!=b:raise RuntimeError('Full stream differs')
 result[n]=dict(logical_bytes=len(b),logical_sha256=hashlib.sha256(b).hexdigest(),stored=pin(q))
write(C/'execution.json',result)
print(json.dumps(dict(actual_launcher_PID=os.getpid(),actual_test_PID=p.pid,exit_code=p.returncode,timed_out=timeout,stdout=out.decode(errors='replace'),stderr=err.decode(errors='replace')),indent=2))
if p.returncode or timeout:raise SystemExit(1)
