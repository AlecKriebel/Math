"""Reviewer-owned complete native process recorder; no external/Git writes."""
from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, json, os, stat, subprocess, sys
HERE=Path(__file__).resolve().parent
def now(): return datetime.now(timezone.utc).isoformat()
def digest(b): return hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p); b=p.read_bytes()
 return dict(path=str(p.absolute()),resolved_path=str(p.resolve()),bytes=len(b),sha256=digest(b),mode=stat.S_IMODE(p.stat().st_mode))
def write(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def capture(label,argv,cwd,sources=()):
 work=HERE/'process_evidence'/label; work.mkdir(parents=True,exist_ok=False)
 before=[]
 for i,p in enumerate(dict.fromkeys([Path(__file__).resolve(),*map(Path,sources)])):
  body=p.read_bytes(); archive=work/('source_%03d.bin.gz'%i); archive.write_bytes(gzip.compress(body,mtime=0))
  assert gzip.decompress(archive.read_bytes())==body
  before.append(dict(original=pin(p),stored=pin(archive),logical_bytes=len(body),logical_sha256=digest(body)))
 req=dict(label=label,actual_launcher_PID=os.getpid(),requested_UTC=now(),argv=list(argv),cwd=str(Path(cwd).resolve()),sources_before=before,interpreter=pin(sys.executable),optimization=sys.flags.optimize,recorder_source=pin(__file__),custody_limit='Actual recorder self-report and Popen PID, not independent operating-system or upstream-clock attestation.')
 write(work/'request.json',req)
 proc=subprocess.Popen(argv,cwd=cwd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 started=now();write(work/'started.json',dict(actual_child_PID=proc.pid,started_UTC=started,argv=list(argv),cwd=req['cwd']))
 out,err=proc.communicate()
 result=dict(req,actual_child_PID=proc.pid,started_UTC=started,completed_UTC=now(),exit_code=proc.returncode)
 for name,body in [('stdout',out),('stderr',err)]:
  p=work/(name+'.bin.gz');p.write_bytes(gzip.compress(body,mtime=0));assert gzip.decompress(p.read_bytes())==body
  result[name]=dict(stored=pin(p),logical_bytes=len(body),logical_sha256=digest(body))
 for row in before: assert pin(row['original']['path'])==row['original']
 write(work/'execution.json',result)
 return result,out,err
