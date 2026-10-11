"""Capture only own text authoring. Generated ROOT author is never imported or launched."""
from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess,sys
F=Path(__file__).absolute().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def put(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def enc(q):return (json.dumps(q,sort_keys=True,indent=2)+'\n').encode()
need=sys.argv==[sys.argv[0]]
if not need:raise ValueError('Own writer only; no arguments or production target')
script=F/'prepare_author.py';source=script.read_bytes();operator=Path(__file__).read_bytes();d=F/'SOURCE_WRITER_ACTUAL_CAPTURE';d.mkdir()
pre=dict(schema='pr49-root-author-source-writer-prelaunch/v1',created_utc=now(),argv=[sys.executable,'-B',str(script)],cwd=str(F),stdin_supplied=False,source_sha256=sha(source),operator_sha256=sha(operator))
put(d/'PRELAUNCH_SOURCE.py',source);put(d/'PRELAUNCH_OPERATOR.py',operator);put(d/'PRELAUNCH.json',enc(pre));started=now();c=subprocess.Popen(pre['argv'],cwd=F,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=c.communicate();finished=now()
q=dict(schema='pr49-root-author-source-writer-actual/v1',prelaunch=pre,pid=c.pid,operator_pid=os.getpid(),actual_execution=True,completed=True,exit_code=c.returncode,started_utc=started,finished_utc=finished,source_unchanged=script.read_bytes()==source,operator_unchanged=Path(__file__).read_bytes()==operator,generated_ROOT_author_imported_compiled_executed=False,ROOT_approval_created=False)
for n,b in [('stdout',out),('stderr',err)]:put(d/(n+'.bin'),b);q[n]=dict(path=n+'.bin',bytes=len(b),sha256=sha(b))
put(d/'CAPTURE.json',enc(q));print(json.dumps(dict(actual_SOURCE_writer_pid=c.pid,exit_code=c.returncode,stdout=out.decode(errors='replace'),stderr=err.decode(errors='replace'),generated_ROOT_author_imported_compiled_executed=False)));sys.exit(c.returncode)
