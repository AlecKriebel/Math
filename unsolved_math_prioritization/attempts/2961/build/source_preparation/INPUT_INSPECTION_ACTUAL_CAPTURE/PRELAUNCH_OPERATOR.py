"""Actual capture restricted to this family's source-only authoring and controls."""
import argparse, datetime as dt, hashlib, json, os, stat, subprocess, sys, traceback
from pathlib import Path
F=Path(__file__).absolute().parent
R=F.parent.parents[2]
def digest(b): return hashlib.sha256(b).hexdigest()
def regular(p):
    if p.is_symlink() or any(q.is_symlink() for q in p.parents) or not stat.S_ISREG(p.stat().st_mode): raise ValueError('Regular nonsymlink file required')
    return p.read_bytes()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('name');parser.add_argument('source');args=parser.parse_args()
    if args.source not in {'inspect_source_inputs.py','author_source_documents.py','private_contract_controls.py'} or not args.name or '/' in args.name or args.name in {'.','..'}: raise ValueError('Only own nonproduction source operation')
    source=F/args.source;raw=regular(source);operator=regular(Path(__file__).absolute());dest=F/args.name;dest.mkdir(exist_ok=False)
    (dest/'PRELAUNCH_SOURCE.py').write_bytes(raw);(dest/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
    argv=['/usr/bin/python3','-B',str(source)];pre={'schema':'pr48-source-preparation-prelaunch/v1','argv':argv,'cwd':str(R),'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'operator_pid':os.getpid(),'source_sha256':digest(raw),'operator_sha256':digest(operator),'production_builder_or_ROOT_operator_executed':False}
    (dest/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n');record=dict(pre,schema='pr48-source-preparation-actual-capture/v1',actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False)
    try:
        with (dest/'stdout.bin').open('xb') as out,(dest/'stderr.bin').open('xb') as err:
            child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
            record.update(actual_execution=True,pid=child.pid)
            try: record['exit_code']=child.wait(timeout=120);record['completed']=True
            except BaseException:child.kill();record['exit_code']=child.wait();raise
    except BaseException:record['operator_failure']=traceback.format_exc()
    finally:
        record['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        for channel in ['stdout','stderr']:
            p=dest/(channel+'.bin')
            if p.exists():b=regular(p);record[channel]={'path':p.name,'bytes':len(b),'sha256':digest(b)}
        record['source_unchanged']=regular(source)==raw;record['operator_unchanged']=regular(Path(__file__).absolute())==operator
        ok=record['actual_execution'] is True and record['completed'] is True and type(record['exit_code']) is int and record['exit_code']==0 and record['source_unchanged'] is True and record['operator_unchanged'] is True and 'operator_failure' not in record
        record['status']='PASS_SOURCE_ONLY_OPERATION' if ok else 'FAIL_SOURCE_ONLY_OPERATION_PRESERVED';(dest/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,sort_keys=True));return 0 if ok else 1
if __name__=='__main__':sys.exit(main())
