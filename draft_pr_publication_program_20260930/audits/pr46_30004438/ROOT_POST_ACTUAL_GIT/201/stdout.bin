"""Genuine capture for only this preparer's own inspection/authoring/control code."""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, os, stat, subprocess, sys, traceback
F=Path(__file__).absolute().parent; R=F.parent.parents[2]
def sha(raw): return hashlib.sha256(raw).hexdigest()
def regular(path):
    if path.is_symlink() or any(p.is_symlink() for p in path.parents) or not stat.S_ISREG(path.stat().st_mode): raise ValueError('Regular nonsymlink source required')
    return path.read_bytes()
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('name'); parser.add_argument('source'); args=parser.parse_args()
    if args.source not in {'author_source_documents.py','inspect_source_inputs.py','private_contract_controls.py'} or not args.name or '/' in args.name or args.name in {'.','..'}: raise ValueError('Own source operation only')
    source=F/args.source; raw=regular(source); operator=regular(Path(__file__).absolute()); destination=F/args.name; destination.mkdir(exist_ok=False)
    (destination/'PRELAUNCH_SOURCE.py').write_bytes(raw); (destination/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
    argv=['/usr/bin/python3','-B',str(source)]
    pre={'schema':'PR46_SOURCE_PREPARATION_PRELAUNCH_v1','argv':argv,'cwd':str(R),
      'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'operator_pid':os.getpid(),
      'source_sha256':sha(raw),'operator_sha256':sha(operator),'production_builder_or_ROOT_operator_executed':False}
    (destination/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
    record=dict(pre,schema='PR46_SOURCE_PREPARATION_ACTUAL_CAPTURE_v1',actual_execution=False,completed=False,
      pid=None,exit_code=None,stdin_supplied=False)
    child=None
    try:
        with (destination/'stdout.bin').open('xb') as out, (destination/'stderr.bin').open('xb') as err:
            child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
            record.update(actual_execution=True,pid=child.pid)
            try: record['exit_code']=child.wait(timeout=120); record['completed']=True
            except BaseException: child.kill(); record['exit_code']=child.wait(); raise
    except BaseException: record['operator_failure']=traceback.format_exc()
    finally:
        record['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        for channel in ['stdout','stderr']:
            path=destination/(channel+'.bin')
            if path.exists():
                data=regular(path); record[channel]={'path':path.name,'bytes':len(data),'sha256':sha(data)}
        record['source_unchanged']=regular(source)==raw; record['operator_unchanged']=regular(Path(__file__).absolute())==operator
        ok=record['actual_execution'] is True and record['completed'] is True and type(record['exit_code']) is int and record['exit_code']==0 and record['source_unchanged'] is True and record['operator_unchanged'] is True and 'operator_failure' not in record
        record['status']='PASS_SOURCE_ONLY_OPERATION' if ok else 'FAIL_SOURCE_ONLY_OPERATION_PRESERVED'
        (destination/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
