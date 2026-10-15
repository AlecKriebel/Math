#!/usr/bin/python3
"""Actual capture for own nonproduction authoring/inspection/private controls only."""
import argparse,datetime,hashlib,json,os,pathlib,stat,subprocess,sys,traceback
F=pathlib.Path(__file__).absolute().parent;R=F.parent.parents[2]
ALLOWED={'inspect_source_inputs.py','author_source_documents.py','private_contract_controls.py','final_source_read.py'}
def sha(b):return hashlib.sha256(b).hexdigest()
def regular(p):
    if p.is_symlink() or any(q.is_symlink() for q in p.parents) or not stat.S_ISREG(p.stat().st_mode):raise ValueError('Regular nonsymlink file required')
    return p.read_bytes()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
    p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('source');a=p.parse_args()
    if a.source not in ALLOWED or not a.name or '/' in a.name or a.name in {'.','..'}:raise ValueError('Only own nonproduction operations')
    source=F/a.source;raw=regular(source);op=regular(pathlib.Path(__file__).absolute());out=F/a.name;out.mkdir(exist_ok=False)
    (out/'PRELAUNCH_SOURCE.py').write_bytes(raw);(out/'PRELAUNCH_OPERATOR.py').write_bytes(op)
    argv=['/usr/bin/python3','-B',str(source)]
    pre={'schema':'pr49-source-preparation-prelaunch/v1','argv':argv,'cwd':str(R),'started_utc':utc(),'operator_pid':os.getpid(),'source_sha256':sha(raw),'operator_sha256':sha(op),'production_builder_or_ROOT_operator_executed':False}
    (out/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n');c=dict(pre,schema='pr49-source-preparation-actual-capture/v1',actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False)
    try:
        with (out/'stdout.bin').open('xb') as stdout,(out/'stderr.bin').open('xb') as stderr:
            child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr);c.update(actual_execution=True,pid=child.pid)
            try:c['exit_code']=child.wait(timeout=120);c['completed']=True
            except BaseException:child.kill();c['exit_code']=child.wait();raise
    except BaseException:c['operator_failure']=traceback.format_exc()
    finally:
        c['finished_utc']=utc()
        for k in ['stdout','stderr']:
            q=out/(k+'.bin')
            if q.exists():b=regular(q);c[k]={'path':q.name,'bytes':len(b),'sha256':sha(b)}
        c['source_unchanged']=regular(source)==raw;c['operator_unchanged']=regular(pathlib.Path(__file__).absolute())==op
        ok=c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==0 and c['source_unchanged'] is True and c['operator_unchanged'] is True and 'operator_failure' not in c
        c['status']='PASS_SOURCE_ONLY_OPERATION' if ok else 'FAIL_SOURCE_ONLY_OPERATION_PRESERVED';(out/'CAPTURE.json').write_text(json.dumps(c,indent=2)+'\n')
    print(json.dumps({'capture':str(out),'pid':c['pid'],'exit_code':c['exit_code'],'status':c['status']}));return 0 if ok else 1
if __name__=='__main__':sys.exit(main())
