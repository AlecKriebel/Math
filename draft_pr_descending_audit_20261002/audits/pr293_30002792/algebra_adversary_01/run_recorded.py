import datetime, gzip, hashlib, json, os, pathlib, signal, subprocess, sys, time

W = pathlib.Path(__file__).resolve().parent
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':p.stat().st_mode&0o777}
def put(p,x): p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')

name=sys.argv[1]
if not name.replace('_','').isalnum(): raise RuntimeError('invalid owned capture name')
argv=sys.argv[2:]
C=W/'native'/name
C.mkdir(parents=True,exist_ok=False)
source=pathlib.Path(argv[3]) if argv[:3]==['/opt/homebrew/bin/python3','-E','-B'] else None
sources={}
for label,p in [('recorder',pathlib.Path(__file__).resolve()),('program',source)]:
    if p:
        b=p.read_bytes(); (C/(label+'_PRELAUNCH.gz')).write_bytes(gzip.compress(b,mtime=0)); sources[label]=pin(p)
request={'UTC':utc(),'actual_recorder_PID':os.getpid(),'argv':argv,'cwd':str(W),'stdin_hex':'','sources':sources,'timeout_seconds':180,'optimized_python':False}
put(C/'request.json',request)
child=None; stdout=b''; stderr=b''; error=None; reaped=False
try:
    child=subprocess.Popen(argv,cwd=W,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    put(C/'started.json',{'UTC':utc(),'actual_recorder_PID':os.getpid(),'actual_child_PID':child.pid})
    stdout,stderr=child.communicate(b'',timeout=180); reaped=child.poll() is not None
except BaseException as exc:
    error=repr(exc)
    if child is not None:
        if child.poll() is None:
            try: os.killpg(child.pid,signal.SIGKILL)
            except ProcessLookupError: pass
        stdout,stderr=child.communicate(timeout=10); reaped=child.poll() is not None
finally:
    for name_,body in [('stdout',stdout),('stderr',stderr)]: (C/(name_+'.gz')).write_bytes(gzip.compress(body,mtime=0))
    execution={'UTC_end':utc(),'actual_recorder_PID':os.getpid(),'actual_child_PID':child.pid if child else None,'exit_code':child.returncode if child else None,'error':error,'parent_reaped':reaped,'stdout':{'bytes':len(stdout),'sha256':hashlib.sha256(stdout).hexdigest()},'stderr':{'bytes':len(stderr),'sha256':hashlib.sha256(stderr).hexdigest()}}
    put(C/'execution.json',execution)
    print(json.dumps({'capture':str(C),**execution},sort_keys=True))
if error is not None or child.returncode: sys.exit(1)
