"""Own actual private child capture; no native/Git/helper outside own family."""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, os, stat, subprocess, sys, traceback
F=Path(__file__).absolute().parent; R=Path('/Users/alec/Documents/Math')
def need(x,n):
    if not x: raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'regular');return p.read_bytes()
def row(p):
    b=raw(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def write(p,o):
    b=o if type(o)is bytes else (json.dumps(o,indent=2,allow_nan=False)+'\n').encode()
    with p.open('xb')as h:h.write(b);h.flush();os.fsync(h.fileno())
def main():
    a=argparse.ArgumentParser();a.add_argument('label');a.add_argument('target');a.add_argument('--cwd');args=a.parse_args()
    need(args.label and '/'not in args.label and args.label not in ('.','..'),'own label');target=Path(args.target).absolute();need(target.is_relative_to(F),'own target');source=raw(target);operator=raw(Path(__file__));cwd=Path(args.cwd).absolute() if args.cwd else F;need(cwd==F or cwd.is_relative_to(F),'own cwd')
    d=F/args.label;d.mkdir(exist_ok=False);write(d/'prelaunch_target.py',source);write(d/'prelaunch_operator.py',operator)
    pre=dict(schema='pr50-classical-private-child/v1',argv=['/usr/bin/python3','-B',str(target)],cwd=str(cwd),operator_pid=os.getpid(),operator_parent_pid=os.getppid(),created_utc=stamp(),source=row(target),operator_sha256=sha(operator),actual_execution=False,completed=False,pid=None,exit_code=None,source_unchanged=None,stdin_supplied=False)
    write(d/'PRELAUNCH.json',pre);c=dict(pre,started_utc=stamp())
    try:
        with (d/'stdout.bin').open('xb')as out,(d/'stderr.bin').open('xb')as err:
            p=subprocess.Popen(c['argv'],cwd=cwd,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));c.update(actual_execution=True,pid=p.pid)
            try:c['exit_code']=p.wait(timeout=60);c['completed']=True
            except BaseException:p.kill();c['exit_code']=p.wait();raise
    except BaseException:c['failure']=traceback.format_exc()
    finally:
        c['finished_utc']=stamp()
        for k in ('stdout','stderr'):
            q=d/(k+'.bin')
            if q.exists():b=raw(q);c[k]=dict(path=k+'.bin',bytes=len(b),sha256=sha(b))
        c['source_unchanged']=raw(target)==source;c['operator_unchanged']=raw(Path(__file__))==operator
        ok=c['actual_execution']is True and c['completed']is True and type(c['exit_code'])is int and c['exit_code']==0 and c['source_unchanged']is True and c['operator_unchanged']is True and 'failure'not in c
        c['status']='PASS_ACTUAL_PRIVATE_CHILD'if ok else'FAILED_ACTUAL_PRIVATE_CHILD_PRESERVED';write(d/'CAPTURE.json',c)
    print(json.dumps(dict(status=c['status'],pid=c['pid'],exit_code=c['exit_code'],started_utc=c['started_utc'],finished_utc=c['finished_utc'],capture=row(d/'CAPTURE.json')),indent=2));return 0 if ok else 1
if __name__=='__main__':sys.exit(main())
