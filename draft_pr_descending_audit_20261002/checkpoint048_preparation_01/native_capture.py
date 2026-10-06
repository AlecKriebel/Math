"""Actual lossless local process custody; outputs stay private in this folder.

No fabricated completion for this module or its running parent. Receipts are
written only after communicate and direct wait. Host/runtime closure is limited
to the named executable bodies, not transitive libraries or opaque descendants.
"""
from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, json, os, signal, stat, subprocess, sys, time
B = Path(__file__).resolve().parent
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    p=Path(p)
    if p.is_symlink() or not p.is_file(): raise RuntimeError('literal regular input required')
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def put(p,b):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
def save(p,obj): put(p,(json.dumps(obj,indent=2,sort_keys=True)+'\n').encode())
def call(run,label,argv,cwd,stdin=None,timeout=45,ok=(0,),env=None):
    run=Path(run).resolve()
    if not run.is_relative_to(B): raise RuntimeError('own custody namespace required')
    d=run/'private/native'/label; d.mkdir(parents=True,exist_ok=False)
    executable=Path(argv[0]).resolve()
    request=dict(UTC=utc(),actual_recorder_PID=os.getpid(),argv=argv,cwd=str(cwd),timeout_seconds=timeout,
      cleanup_seconds=5,stdin_bytes=len(stdin or b''),stdin_sha256=sha(stdin) if stdin is not None else None,
      executable=pin(executable),recorder_source=pin(__file__),python_launcher=pin(Path(sys.executable).resolve()),python_engine=pin('/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'),
      qualification='Named runtime bodies only; no credential/environment values or transitive runtime claim')
    save(d/'request.json',request)
    put(d/'program_PRELAUNCH.py',Path(__file__).read_bytes())
    if stdin is not None: put(d/'stdin.gz',gzip.compress(stdin,mtime=0))
    p=None; out=b''; err=b''; failure=None; errors=[]; complete=False; wait=False; start=time.monotonic()
    try:
        p=subprocess.Popen(argv,cwd=cwd,env=env,stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,
          stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        save(d/'started.json',dict(UTC=utc(),actual_child_PID=p.pid))
        out,err=p.communicate(stdin,timeout=timeout); complete=True
    except BaseException as e:
        failure=dict(type=type(e).__name__,message=str(e))
        if isinstance(getattr(e,'output',None),bytes): out=e.output
        if isinstance(getattr(e,'stderr',None),bytes): err=e.stderr
    finally:
        if p is not None and not complete:
            try: os.killpg(p.pid,signal.SIGKILL)
            except BaseException as e: errors.append(dict(stage='signal',type=type(e).__name__,message=str(e)))
            try: out,err=p.communicate(timeout=5); complete=True
            except BaseException as e: errors.append(dict(stage='collect',type=type(e).__name__,message=str(e)))
        if p is not None:
            try: p.wait(timeout=5); wait=True
            except BaseException as e: errors.append(dict(stage='wait',type=type(e).__name__,message=str(e)))
    streams={}
    for name,body in [('stdout',out),('stderr',err)]:
        z=gzip.compress(body,mtime=0); put(d/(name+'.gz'),z)
        streams[name]=dict(logical_bytes=len(body),logical_sha256=sha(body),stored_bytes=len(z),stored_sha256=sha(z),complete=complete)
    code=p.returncode if p else None
    save(d/'execution.json',dict(UTC=utc(),actual_recorder_PID=os.getpid(),actual_child_PID=p.pid if p else None,
      argv=argv,cwd=str(cwd),elapsed_seconds=time.monotonic()-start,returncode=code,communication_complete=complete,
      wait_completed=wait,reaped=p is not None and code is not None and (wait or complete),failure=failure,
      cleanup_errors=errors,streams=streams))
    if failure or errors or not complete or not wait or code not in ok:
        raise RuntimeError('Native failure: preserve all actual state; no automatic mutation retry')
    return out
