"""Capture this adversary's private standard-library inspection or countermodels only."""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, os, subprocess, sys, traceback
F=Path(__file__).absolute().parent
R=F.parents[3]
def sha(b): return hashlib.sha256(b).hexdigest()
def put(p,b):
    with p.open('xb') as h: h.write(b); h.flush(); os.fsync(h.fileno())
def main():
    p=argparse.ArgumentParser(); p.add_argument('capture_name'); p.add_argument('script'); a=p.parse_args()
    assert '/' not in a.capture_name and a.capture_name not in ('','.','..')
    assert a.script in ['inspect_fixed_inputs.py','independent_countermodels.py','verify_private_evidence.py']
    dest=F/a.capture_name; dest.mkdir(mode=0o700)
    source=F/a.script; src=source.read_bytes(); op=Path(__file__).read_bytes()
    put(dest/'PRELAUNCH_SOURCE.py',src); put(dest/'PRELAUNCH_OPERATOR.py',op)
    argv=['/usr/bin/python3','-B',str(source)]
    rec={'schema':'pr48-acceptance-source-adversary-private-actual-capture/v1','argv':argv,'cwd':str(R),'operator_pid':os.getpid(),'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'source_sha256':sha(src),'operator_sha256':sha(op),'production_imported_compiled_executed':False,'actual_execution':False,'completed':False,'pid':None,'exit_code':None,'stdin_supplied':False}
    put(dest/'PRELAUNCH.json',(json.dumps(rec,sort_keys=True,indent=2)+'\n').encode())
    out=err=b''
    try:
        ch=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        rec.update(actual_execution=True,pid=ch.pid); out,err=ch.communicate(); rec.update(completed=True,exit_code=ch.returncode)
    except BaseException: rec['operator_error']=traceback.format_exc()
    rec.update(finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),source_unchanged=source.read_bytes()==src,operator_unchanged=Path(__file__).read_bytes()==op)
    for n,b in [('stdout',out),('stderr',err)]:
        put(dest/(n+'.bin'),b); rec[n]={'path':n+'.bin','bytes':len(b),'sha256':sha(b)}
    put(dest/'CAPTURE.json',(json.dumps(rec,sort_keys=True,indent=2)+'\n').encode())
    print(json.dumps(rec,sort_keys=True))
    return 0 if rec['completed'] is True and rec['exit_code']==0 and rec['source_unchanged'] is True and rec['operator_unchanged'] is True and not err and 'operator_error' not in rec else 1
if __name__=='__main__': sys.exit(main())
