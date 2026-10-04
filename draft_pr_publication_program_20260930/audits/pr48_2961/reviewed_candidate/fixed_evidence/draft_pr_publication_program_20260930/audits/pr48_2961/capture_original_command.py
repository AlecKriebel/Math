"""Retain actual PR48 read-only commands, prelaunch source, and complete streams."""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, os, subprocess, sys, traceback
A=Path(__file__).resolve().parent
R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def main():
    p=argparse.ArgumentParser();p.add_argument('capture_name');p.add_argument('argv',nargs=argparse.REMAINDER);a=p.parse_args()
    assert a.capture_name and '/' not in a.capture_name and a.capture_name not in ('.','..')
    argv=a.argv[1:] if a.argv and a.argv[0]=='--' else a.argv;assert argv
    d=A/a.capture_name;d.mkdir(mode=0o700)
    source=Path(__file__).read_bytes();write(d/'prelaunch_operator.py',source)
    rec=dict(schema='pr48-original-actual-command/v1',argv=argv,cwd=str(R),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_execution=False,pid=None,exit_code=None,completed=False,stdin_supplied=False,operator_sha256=sha(source))
    target=None
    if len(argv)>1 and argv[0] in ('python','python3'):
        q=(R/argv[1]).resolve();assert q.is_relative_to(A) and q.is_file();target=q.read_bytes();write(d/'prelaunch_target.py',target);rec['target_source']=dict(path=str(q),bytes=len(target),sha256=sha(target))
    write(d/'PRELAUNCH.json',(json.dumps(rec,indent=2,sort_keys=True)+'\n').encode())
    out,err=b'',b''
    try:
        child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);rec.update(actual_execution=True,pid=child.pid);out,err=child.communicate();rec.update(completed=True,exit_code=child.returncode)
    except BaseException:rec['operator_error']=traceback.format_exc()
    rec['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
    for key,b in [('stdout',out),('stderr',err)]:write(d/(key+'.bin'),b);rec[key]=dict(path=key+'.bin',bytes=len(b),sha256=sha(b))
    rec['operator_unchanged']=Path(__file__).read_bytes()==source
    if target is not None:rec['target_unchanged']=q.read_bytes()==target
    ok=rec['actual_execution'] is True and rec['completed'] is True and rec['exit_code']==0 and rec['operator_unchanged'] and rec.get('target_unchanged',True) and 'operator_error' not in rec
    rec['status']='CAPTURE_COMPLETED' if ok else 'CAPTURE_FAILED';write(d/'CAPTURE.json',(json.dumps(rec,indent=2,sort_keys=True)+'\n').encode())
    for q in d.iterdir():assert q.is_file() and not q.is_symlink();os.chmod(q,0o444);assert q.stat().st_mode&0o7777==0o444
    print(json.dumps(rec,sort_keys=True));return 0 if ok else 1
if __name__=='__main__':sys.exit(main())
