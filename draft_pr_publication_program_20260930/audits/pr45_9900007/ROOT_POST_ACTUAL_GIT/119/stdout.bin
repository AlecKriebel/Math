"""Capture only this SOURCE preparer's own authoring/control operations."""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, os, subprocess, sys, traceback
F = Path(__file__).resolve().parent
R = F.parent.parents[2]
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser(); p.add_argument('name'); p.add_argument('source'); a=p.parse_args()
    allowed={'author_source_documents.py','private_contract_controls.py','inspect_source_inputs.py','close_source_preparation.py'}
    assert a.source in allowed and a.name and '/' not in a.name and a.name not in ('.','..')
    source=F/a.source; raw=source.read_bytes(); op=Path(__file__).read_bytes(); d=F/a.name; d.mkdir()
    (d/'PRELAUNCH_SOURCE.py').write_bytes(raw); (d/'PRELAUNCH_OPERATOR.py').write_bytes(op)
    argv=['/usr/bin/python3','-B',str(source)]; start=dt.datetime.now(dt.timezone.utc).isoformat()
    c={'schema':'PR45_CURRENT_SOURCE_PREPARATION_ACTUAL_CAPTURE_v1','argv':argv,'cwd':str(R),
       'started_utc':start,'operator_pid':os.getpid(),'source_sha256':sha(raw),'operator_sha256':sha(op),
       'actual_execution':False,'completed':False,'pid':None,'exit_code':None,'stdin_supplied':False,
       'production_builder_or_ROOT_operator_executed':False}
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
    c['status']='PASS_SOURCE_ONLY_OPERATION' if ok else 'FAIL_SOURCE_ONLY_OPERATION_PRESERVED'
    (d/'CAPTURE.json').write_text(json.dumps(c,indent=2)+'\n'); print(json.dumps(c,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
