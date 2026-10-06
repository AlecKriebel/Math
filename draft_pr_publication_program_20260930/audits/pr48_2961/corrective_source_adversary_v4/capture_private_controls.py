"""Own actual private child capture only; candidate runtimes remain unexecuted."""
from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess,sys
F=Path(__file__).absolute().parent
R=Path('/Users/alec/Documents/Math')
def pin(p):
    b=p.read_bytes();return dict(path=p.relative_to(F).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
    os.umask(0o022);d=F/'private_actual_capture';d.mkdir();source=F/'private_controls.py';op=Path(__file__);sb=source.read_bytes();ob=op.read_bytes();(d/'PRELAUNCH_SOURCE.py').write_bytes(sb);(d/'PRELAUNCH_OPERATOR.py').write_bytes(ob)
    argv=[sys.executable,'-B',str(source)];rec=dict(schema='pr48-v4-independent-private-actual-capture/v1',argv=argv,cwd=str(R),operator_pid=os.getpid(),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),stdin_supplied=False,prelaunch_source=pin(d/'PRELAUNCH_SOURCE.py'),prelaunch_operator=pin(d/'PRELAUNCH_OPERATOR.py'),actual_execution=False,completed=False,pid=None,exit_code=None)
    child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);rec.update(actual_execution=True,pid=child.pid);out,err=child.communicate();rec.update(completed=True,exit_code=child.returncode,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),source_unchanged=source.read_bytes()==sb,operator_unchanged=op.read_bytes()==ob)
    for n,b in [('stdout.json',out),('stderr.bin',err)]:
        with (d/n).open('xb') as f:f.write(b)
    rec['stdout']=pin(d/'stdout.json');rec['stderr']=pin(d/'stderr.bin');rec['status']='PASS' if child.returncode==0 and err==b'' and rec['source_unchanged'] and rec['operator_unchanged'] else 'FAIL'
    with (d/'CAPTURE.json').open('xb') as f:f.write((json.dumps(rec,indent=2)+'\n').encode())
    print(json.dumps(rec,indent=2));assert rec['status']=='PASS'
if __name__=='__main__':main()
