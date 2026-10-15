"""Own real prelaunch wrapper for the private source audit only."""
from pathlib import Path
import datetime as dt, hashlib, json, os, subprocess, sys, traceback
F=Path(__file__).absolute().parent; R=F.parent.parents[2]
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def emit(q,x): q.write_bytes((json.dumps(x,indent=2,sort_keys=True,allow_nan=False)+'\n').encode())
def main():
    source=F/'private_source_audit.py'; raw=source.read_bytes(); operator=Path(__file__).absolute().read_bytes()
    destination=F/('PRIVATE_AUDIT_ACTUAL_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')); destination.mkdir(exist_ok=False)
    (destination/'PRELAUNCH_SOURCE.py').write_bytes(raw); (destination/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
    argv=['/usr/bin/python3','-B',str(source)]
    pre={'schema':'PR46_CURRENT_SOURCE_ADVERSARY_PRELAUNCH_v1','argv':argv,'cwd':str(R),'operator_pid':os.getpid(),'started_utc':now(),'source_sha256':sha(raw),'operator_sha256':sha(operator),'production_import_compile_or_execution':False}
    emit(destination/'PRELAUNCH.json',pre)
    capture=dict(pre,schema='PR46_CURRENT_SOURCE_ADVERSARY_ACTUAL_CAPTURE_v1',actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False)
    try:
        with (destination/'stdout.bin').open('xb') as out,(destination/'stderr.bin').open('xb') as err:
            child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
            capture.update(actual_execution=True,pid=child.pid)
            try: capture['exit_code']=child.wait(timeout=120); capture['completed']=True
            except BaseException: child.kill(); capture['exit_code']=child.wait(); raise
    except BaseException: capture['failure']=traceback.format_exc()
    finally:
        capture['finished_utc']=now()
        for channel in ['stdout','stderr']:
            q=destination/(channel+'.bin')
            if q.exists():
                b=q.read_bytes(); capture[channel]={'path':q.name,'bytes':len(b),'sha256':sha(b)}
        capture['source_unchanged']=source.read_bytes()==raw; capture['operator_unchanged']=Path(__file__).absolute().read_bytes()==operator
        ok=capture['actual_execution'] is True and capture['completed'] is True and type(capture['exit_code']) is int and capture['exit_code']==0 and capture['source_unchanged'] is True and capture['operator_unchanged'] is True and 'failure' not in capture
        capture['status']='PASS_PRIVATE_ACTUAL_SOURCE_AUDIT' if ok else 'FAILED_PRIVATE_ACTUAL_SOURCE_AUDIT_PRESERVED'
        emit(destination/'CAPTURE.json',capture)
    print(json.dumps({'status':capture['status'],'capture':str(destination/'CAPTURE.json'),'pid':capture['pid'],'exit_code':capture['exit_code'],'capture_sha256':sha((destination/'CAPTURE.json').read_bytes())},sort_keys=True))
    return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
