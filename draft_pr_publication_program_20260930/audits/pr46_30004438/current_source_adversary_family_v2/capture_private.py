#!/usr/bin/env python3
"""Capture only this family's own private administrative scripts, retaining failures."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess
import sys
import traceback

F=Path(__file__).absolute().parent; R=F.parent.parents[2]
N=['unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']]+['draft_pr_publication_program_20260930/inventory.json']
def sha(b): return hashlib.sha256(b).hexdigest()
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def dump(v): return (json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def read(p):
    if p.is_symlink() or any(q.is_symlink() for q in p.parents) or not stat.S_ISREG(p.stat().st_mode): raise ValueError('Regular file required')
    return p.read_bytes()
def native():
    result=[]
    for n in N:
        b=read(R/n); result.append({'path':n,'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE((R/n).stat().st_mode)})
    return result
def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ['private_source_controls.py','inspect_remaining.py']: raise ValueError('Own private source only')
    source=F/sys.argv[1]; source_raw=read(source); operator_raw=read(Path(__file__).absolute())
    directory=F/('actual_private_capture_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')); directory.mkdir(exist_ok=False)
    (directory/'PRELAUNCH_SOURCE.py').write_bytes(source_raw); (directory/'PRELAUNCH_OPERATOR.py').write_bytes(operator_raw)
    before=native()
    argv=['/usr/bin/python3','-B',str(source)]
    rec={'schema':'PR46_INDEPENDENT_V2_PRIVATE_ACTUAL_CAPTURE_v1','argv':argv,'cwd':str(R),'operator_pid':os.getpid(),'source_sha256':sha(source_raw),'operator_sha256':sha(operator_raw),'started_utc':utc(),'actual_execution':False,'completed':False,'pid':None,'exit_code':None,'stdin_supplied':False,'production_import_compile_execute':False,'native13_before':before}
    (directory/'PRELAUNCH.json').write_bytes(dump(rec))
    try:
        with (directory/'stdout.bin').open('xb') as out, (directory/'stderr.bin').open('xb') as err:
            child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
            rec.update(actual_execution=True,pid=child.pid)
            try: rec['exit_code']=child.wait(timeout=600); rec['completed']=True
            except BaseException: child.kill(); rec['exit_code']=child.wait(); raise
    except BaseException: rec['operator_failure']=traceback.format_exc()
    finally:
        rec['finished_utc']=utc()
        rec['source_unchanged']=read(source)==source_raw; rec['operator_unchanged']=read(Path(__file__).absolute())==operator_raw
        rec['native13_after']=native(); rec['native13_unchanged']=rec['native13_after']==before
        for n in ['stdout','stderr']:
            b=read(directory/(n+'.bin')); rec[n]={'path':n+'.bin','bytes':len(b),'sha256':sha(b)}
        ok=rec['actual_execution'] is True and rec['completed'] is True and type(rec['exit_code']) is int and rec['exit_code']==0 and rec['source_unchanged'] is True and rec['operator_unchanged'] is True and rec['native13_unchanged'] is True and 'operator_failure' not in rec
        rec['status']='PASS_PRIVATE_ADMINISTRATIVE_CAPTURE' if ok else 'FAILED_ACTUAL_PRIVATE_CAPTURE_PRESERVED'
        rec['ROOT_runtime_or_future_merge_certified']=False
        (directory/'CAPTURE.json').write_bytes(dump(rec))
    print(json.dumps({'directory':str(directory),'pid':rec['pid'],'exit_code':rec['exit_code'],'status':rec['status'],'capture_sha256':sha(read(directory/'CAPTURE.json'))},sort_keys=True))
    return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
