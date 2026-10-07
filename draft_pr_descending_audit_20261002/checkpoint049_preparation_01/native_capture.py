"""Exact named-process custody; private only, immutable completed receipts.

No completion receipt for a still running actor. Named executable bodies are
bounded identities, not a transitive runtime or opaque descendant guarantee.
"""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,signal,stat,subprocess,sys,time
B=Path(__file__).resolve().parent
ENGINE='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'
def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,m):
    if not x:raise RuntimeError(m)
def pin(p):
    p=Path(p);need(p.is_file() and not p.is_symlink(),'literal regular input')
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def put(p,b):
    p=Path(p);need(p.resolve().is_relative_to(B),'own custody namespace');p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    p.chmod(0o444)
def save(p,d):put(p,(json.dumps(d,indent=2,sort_keys=True)+'\n').encode())
def call(run,label,argv,cwd,stdin=None,timeout=45,ok=(0,),env=None):
    run=Path(run);need(run.is_absolute() and run.resolve()==run and run.is_relative_to(B),'literal own run');need(type(argv) is list and all(type(x) is str for x in argv),'literal argv')
    need(type(timeout) in (float,int) and not isinstance(timeout,bool) and 0<timeout<=600,'bounded timeout')
    d=run/'private/native'/label;d.mkdir(parents=True,exist_ok=False)
    ex=Path(argv[0]).resolve();runtime=pin(ex);recorder=pin(__file__);py=pin(Path(sys.executable).resolve());engine=pin(ENGINE)
    program=pin(argv[3]) if len(argv)>3 and argv[1:3]==['-E','-B'] and Path(argv[3]).is_file() else None
    req=dict(schema='checkpoint049-native-request-v1',UTC=utc(),actual_recorder_PID=os.getpid(),argv=argv,cwd=str(cwd),timeout_seconds=timeout,cleanup_seconds=5,stdin_bytes=len(stdin or b''),stdin_sha256=sha(stdin) if stdin is not None else None,executable=runtime,recorder_source=recorder,python_launcher=py,python_engine=engine,program=program,environment_values_recorded=False,transitive_runtime_certified=False)
    save(d/'request.json',req);put(d/'recorder_PRELAUNCH.py',Path(__file__).read_bytes())
    if program:put(d/'program_PRELAUNCH.py',Path(program['path']).read_bytes())
    if stdin is not None:put(d/'stdin.gz',gzip.compress(stdin,mtime=0))
    p=None;out=b'';err=b'';failure=None;errors=[];complete=False;wait=False;start=time.monotonic()
    try:
        p=subprocess.Popen(argv,cwd=cwd,env=env,stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        save(d/'started.json',dict(schema='checkpoint049-native-start-v1',UTC=utc(),actual_recorder_PID=os.getpid(),actual_child_PID=p.pid))
        out,err=p.communicate(stdin,timeout=timeout);complete=True
    except BaseException as e:
        failure=dict(type=type(e).__name__,message=str(e))
        if isinstance(getattr(e,'output',None),bytes):out=e.output
        if isinstance(getattr(e,'stderr',None),bytes):err=e.stderr
    finally:
        if p is not None and not complete:
            try:os.killpg(p.pid,signal.SIGKILL)
            except BaseException as e:errors.append(dict(stage='signal',type=type(e).__name__,message=str(e)))
            try:out,err=p.communicate(timeout=5);complete=True
            except BaseException as e:errors.append(dict(stage='collect',type=type(e).__name__,message=str(e)))
        if p is not None:
            try:p.wait(timeout=5);wait=True
            except BaseException as e:errors.append(dict(stage='wait',type=type(e).__name__,message=str(e)))
    try:
        changed=pin(ex)!=runtime or pin(__file__)!=recorder or pin(Path(sys.executable).resolve())!=py or pin(ENGINE)!=engine or program is not None and pin(program['path'])!=program
        if changed:errors.append(dict(stage='postlaunch_named_body_guard',type='RuntimeError',message='named source/runtime changed'))
    except BaseException as e:errors.append(dict(stage='postlaunch_named_body_guard',type=type(e).__name__,message=str(e)))
    streams={}
    for name,b in [('stdout',out),('stderr',err)]:
        z=gzip.compress(b,mtime=0);put(d/(name+'.gz'),z);streams[name]=dict(stored=pin(d/(name+'.gz')),logical_bytes=len(b),logical_sha256=sha(b),complete=complete)
    code=p.returncode if p else None
    save(d/'execution.json',dict(schema='checkpoint049-native-completed-observation-v1',UTC=utc(),actual_recorder_PID=os.getpid(),actual_child_PID=p.pid if p else None,argv=argv,cwd=str(cwd),request=pin(d/'request.json'),elapsed_seconds=time.monotonic()-start,returncode=code,communication_complete=complete,wait_completed=wait,reaped=p is not None and type(code) is int and wait,failure=failure,cleanup_errors=errors,streams=streams))
    if failure or errors or complete is not True or wait is not True or type(code) is not int or code not in ok:raise RuntimeError('Preserved genuine native failure; no automatic retry or mutation continuation')
    return out
