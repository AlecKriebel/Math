"""Actual administrative source-derivation capture; no compressor invocation."""
import datetime,hashlib,json,os,subprocess,sys
from pathlib import Path
N=Path(__file__).absolute().parent
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def ref(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),full_mode=p.stat().st_mode&0o7777)
def main():
    d=N/'preparation_actual_capture';d.mkdir(exist_ok=False);op=N/'prepare_source.py'
    put(d/'prelaunch_operator.py',op.read_bytes());put(d/'prelaunch_controller.py',Path(__file__).read_bytes())
    argv=[sys.executable,'-B',str(op)];start=utc();c=subprocess.Popen(argv,cwd=N,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=c.communicate();end=utc();put(d/'stdout.json',out);put(d/'stderr.bin',err)
    cap=dict(role='SOURCE_PREPARER',actual_execution=True,pid=c.pid,argv=argv,cwd=str(N),started_utc=start,finished_utc=end,completed=True,exit_code=c.returncode,
      prelaunch_operator=ref(d/'prelaunch_operator.py'),prelaunch_controller=ref(d/'prelaunch_controller.py'),stdout=ref(d/'stdout.json'),stderr=ref(d/'stderr.bin'),
      operator_unchanged=op.read_bytes()==(d/'prelaunch_operator.py').read_bytes(),ROOT_approval=False,compression_executed=False)
    put(d/'CAPTURE.json',(json.dumps(cap,indent=2,sort_keys=True)+'\n').encode());print(json.dumps(cap));assert c.returncode==0
if __name__=='__main__':main()
