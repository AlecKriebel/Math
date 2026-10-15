#!/usr/bin/env python3
"""Actual own-source preparation capture, never a production launcher."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def digest(raw): return hashlib.sha256(raw).hexdigest()
def dump(value): return (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
def main():
    here=Path(__file__).absolute().parent
    source=here/sys.argv[1]
    assert source.parent==here and source.name in {'author_source_documents.py','private_contract_controls.py'}
    capture=here/sys.argv[2]
    assert capture.parent==here and not capture.exists()
    capture.mkdir()
    body=source.read_bytes(); operator=Path(__file__).read_bytes()
    (capture/'PRELAUNCH_SOURCE.py').write_bytes(body)
    (capture/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
    argv=['/usr/bin/python3','-B',str(source)]
    rec={'schema':'PR44_OWN_PREPARATION_ACTUAL_CAPTURE_v1','operator_pid':os.getpid(),
         'argv':argv,'cwd':str(here),'started_utc':now(),'source_sha256':digest(body),
         'operator_sha256':digest(operator),'actual_execution':False,'completed':False,'pid':None,
         'exit_code':None,'stdin_supplied':False,'production_executed':False}
    try:
        with (capture/'stdout.bin').open('xb') as out,(capture/'stderr.bin').open('xb') as err:
            child=subprocess.Popen(argv,cwd=here,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
            rec.update(actual_execution=True,pid=child.pid)
            rec['exit_code']=child.wait(timeout=60);rec['completed']=True
    except BaseException:
        rec['failure']=traceback.format_exc()
        if 'child' in locals() and child.poll() is None:
            child.kill();rec['exit_code']=child.wait()
    finally:
        rec['finished_utc']=now()
        for channel in ['stdout','stderr']:
            p=capture/(channel+'.bin')
            if p.exists():
                content=p.read_bytes()
                rec[channel]={'path':p.name,'bytes':len(content),'sha256':digest(content)}
        rec['source_unchanged']=source.read_bytes()==body
        rec['operator_unchanged']=Path(__file__).read_bytes()==operator
        rec['status']='PASS_OWN_SOURCE_PREPARATION' if rec['actual_execution'] and rec['completed'] and rec['exit_code']==0 and rec['source_unchanged'] and rec['operator_unchanged'] and 'failure' not in rec else 'FAILED_OWN_SOURCE_PREPARATION_PRESERVED'
        (capture/'CAPTURE.json').write_bytes(dump(rec))
    print(json.dumps(rec,indent=2))
    return 0 if rec['status']=='PASS_OWN_SOURCE_PREPARATION' else 1
if __name__=='__main__':sys.exit(main())
