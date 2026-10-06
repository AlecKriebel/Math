"""Retain own literal private controls and actual child streams; no candidate run."""
from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess,sys
F=Path(__file__).absolute().parent;R=Path('/Users/alec/Documents/Math')
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(F).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
    os.umask(0o022);d=F/'private_actual_capture';d.mkdir();s=F/'private_controls.py';op=Path(__file__);sb=s.read_bytes();ob=op.read_bytes();(d/'PRELAUNCH_SOURCE.py').write_bytes(sb);(d/'PRELAUNCH_OPERATOR.py').write_bytes(ob);argv=[sys.executable,'-B',str(s)]
    v=dict(schema='pr48-v5-independent-private-actual-capture/v1',argv=argv,cwd=str(R),operator_pid=os.getpid(),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),stdin_supplied=False,prelaunch_source=ref(d/'PRELAUNCH_SOURCE.py'),prelaunch_operator=ref(d/'PRELAUNCH_OPERATOR.py'),actual_execution=False,completed=False,pid=None,exit_code=None)
    child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);v.update(actual_execution=True,pid=child.pid);out,err=child.communicate();v.update(completed=True,exit_code=child.returncode,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),source_unchanged=s.read_bytes()==sb,operator_unchanged=op.read_bytes()==ob)
    for n,b in [('stdout.json',out),('stderr.bin',err)]:
        with (d/n).open('xb') as f:f.write(b)
    v.update(stdout=ref(d/'stdout.json'),stderr=ref(d/'stderr.bin'));v['status']='PASS' if child.returncode==0 and not err and v['source_unchanged'] and v['operator_unchanged'] else 'FAIL'
    with (d/'CAPTURE.json').open('xb') as f:f.write((json.dumps(v,indent=2)+'\n').encode())
    print(json.dumps(v,indent=2));assert v['status']=='PASS'
if __name__=='__main__':main()
