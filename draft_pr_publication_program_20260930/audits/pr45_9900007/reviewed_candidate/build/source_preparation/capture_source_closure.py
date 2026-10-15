"""Capture only own source closure outside its self-only family inventory."""
from pathlib import Path
import datetime as dt, hashlib, json, os, subprocess, sys, traceback
F=Path(__file__).resolve().parent; A=F.parent; R=A.parents[2]
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    d=A/'current_preparation_closure_actual_capture'; d.mkdir()
    source=F/'close_source_preparation.py'; raw=source.read_bytes(); op=Path(__file__).read_bytes()
    (d/'PRELAUNCH_SOURCE.py').write_bytes(raw); (d/'PRELAUNCH_OPERATOR.py').write_bytes(op)
    argv=['/usr/bin/python3','-B',str(source)]
    c={'schema':'PR45_CURRENT_SOURCE_CLOSURE_ACTUAL_CAPTURE_v1','argv':argv,'cwd':str(R),
       'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'operator_pid':os.getpid(),
       'source_sha256':sha(raw),'operator_sha256':sha(op),'actual_execution':False,'completed':False,
       'pid':None,'exit_code':None,'stdin_supplied':False,'production_builder_or_ROOT_operator_executed':False}
    out=err=b''
    try:
        child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        c.update(actual_execution=True,pid=child.pid); out,err=child.communicate(); c.update(completed=True,exit_code=child.returncode)
    except BaseException: c['operator_error']=traceback.format_exc()
    c['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
    for name,b in [('stdout',out),('stderr',err)]:
        with (d/(name+'.bin')).open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
        c[name]={'path':name+'.bin','bytes':len(b),'sha256':sha(b)}
    c['source_unchanged']=source.read_bytes()==raw; c['operator_unchanged']=Path(__file__).read_bytes()==op
    ok=c['actual_execution'] is True and c['completed'] is True and c['exit_code']==0 and c['source_unchanged'] is True and c['operator_unchanged'] is True and 'operator_error' not in c
    c['status']='PASS_CLOSED_SOURCE_ONLY_PREPARATION' if ok else 'FAIL_OWN_SOURCE_CLOSURE_PRESERVED'
    (d/'CAPTURE.json').write_text(json.dumps(c,indent=2)+'\n')
    for p in d.iterdir(): os.chmod(p,0o444)
    print(json.dumps(c,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
