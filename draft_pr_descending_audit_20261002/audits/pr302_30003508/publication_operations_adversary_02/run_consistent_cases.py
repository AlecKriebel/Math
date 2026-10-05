from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,stat,subprocess,sys
R=Path('/Users/alec/Documents/Math');W=Path(__file__).resolve().parent;P=W/'actual_consistent_cases_01';P.mkdir();child_source=W/'consistent_cases.py'
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),resolved_path=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
def utc():return datetime.now(timezone.utc).isoformat()
def put(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
sources=[]
for i,p in enumerate((Path(__file__).resolve(),child_source)):
 q=P/(str(i)+'_'+p.name+'.gz');q.write_bytes(gzip.compress(p.read_bytes(),mtime=0));q.chmod(0o444);assert gzip.decompress(q.read_bytes())==p.read_bytes();sources.append(dict(input=pin(p),full_source_archive=pin(q)))
argv=['/opt/homebrew/bin/python3','-E','-B',str(child_source)];request=dict(actual_launcher_PID=os.getpid(),argv=argv,cwd=str(R),requested_UTC=utc(),full_prelaunch_sources=sources,resolved_executable=pin(Path(argv[0]).resolve()),resolved_caller_interpreter=pin(Path(sys.executable).resolve()),automatic_retry=False,custody_limit='Recorder/Popen observations; no independent OS/clock attestation')
put(P/'request.json',request);start=utc();child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);put(P/'started.json',dict(actual_PID=child.pid,start_UTC=start,state='STARTED_OUTCOME_PENDING'))
timeout=False
try:out,err=child.communicate(timeout=55)
except subprocess.TimeoutExpired:timeout=True;child.kill();out,err=child.communicate()
result=dict(request,actual_PID=child.pid,start_UTC=start,end_UTC=utc(),exit_code=child.returncode,timed_out=timeout)
for name,b in (('stdout',out),('stderr',err)):
 q=P/(name+'.bin.gz');q.write_bytes(gzip.compress(b,mtime=0));assert gzip.decompress(q.read_bytes())==b;result[name]=dict(logical_bytes=len(b),logical_sha256=hashlib.sha256(b).hexdigest(),stored=pin(q))
put(P/'execution.json',result);print(json.dumps(dict(actual_launcher_PID=os.getpid(),actual_PID=child.pid,exit_code=child.returncode,timed_out=timeout,stdout_bytes=len(out),stderr_bytes=len(err))))
if child.returncode:print(err.decode(errors='replace'));sys.exit(child.returncode)
