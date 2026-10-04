"""Actual administrative derivation capture; no production helper import/run."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
N = Path(__file__).absolute().parent
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(q,b):
    with q.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
def ref(q):
    b=q.read_bytes(); return dict(path=str(q.relative_to(N)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),full_mode=q.stat().st_mode & 0o7777)
def main():
    d=N/'source_derivation_actual_capture'; d.mkdir(exist_ok=False)
    op=N/'derive_helpers.py'; put(d/'prelaunch_operator.py',op.read_bytes())
    put(d/'prelaunch_controller.py',Path(__file__).read_bytes())
    argv=[sys.executable,'-B',str(op)]; start=now()
    c=subprocess.Popen(argv,cwd=N,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=c.communicate(); end=now(); put(d/'stdout.bin',out);put(d/'stderr.bin',err)
    cap=dict(schema='checkpoint1915-actual-source-derivation/v1',actual_execution=True,completed=True,
             operator_role='SOURCE_PREPARER',pid=c.pid,argv=argv,cwd=str(N),started_utc=start,finished_utc=end,
             exit_code=c.returncode,operator_unchanged=op.read_bytes()==(d/'prelaunch_operator.py').read_bytes(),
             ROOT_execution_or_approval=False,production_helpers_executed=False,
             prelaunch_operator=ref(d/'prelaunch_operator.py'),prelaunch_controller=ref(d/'prelaunch_controller.py'),
             stdout=ref(d/'stdout.bin'),stderr=ref(d/'stderr.bin'))
    put(d/'CAPTURE.json',(json.dumps(cap,indent=2,sort_keys=True)+'\n').encode());print(json.dumps(cap))
    assert c.returncode==0
if __name__=='__main__':main()
