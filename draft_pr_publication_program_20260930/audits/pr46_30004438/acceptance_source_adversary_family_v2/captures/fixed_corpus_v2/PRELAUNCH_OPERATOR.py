#!/usr/bin/python3
"""Actual independent private controls only; no production/closure may be launched."""
import datetime,hashlib,json,os,pathlib,stat,subprocess,sys,traceback
F=pathlib.Path(__file__).absolute().parent;R=F.parent.parents[2]
ALLOWED={'fixed_corpus_controls.py','fixed_corpus_controls_v2.py','ownership_phase_controls.py','final_capture_controls.py'}
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
    if p.is_symlink() or any(q.is_symlink() for q in p.parents) or not stat.S_ISREG(p.stat().st_mode):raise ValueError('Unsafe own source')
    return p.read_bytes()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
    if len(sys.argv)!=3 or sys.argv[1] not in ALLOWED or '/' in sys.argv[2] or sys.argv[2] in {'','.','..'}:raise ValueError('Only own private source and new capture name')
    source=F/sys.argv[1];b=read(source);op=read(pathlib.Path(__file__).absolute());d=F/'captures'/sys.argv[2];d.mkdir(parents=True,exist_ok=False)
    (d/'PRELAUNCH_SOURCE.py').write_bytes(b);(d/'PRELAUNCH_OPERATOR.py').write_bytes(op)
    pre={'schema':'pr46-source-v2-independent-private-prelaunch/v1','source_sha256':sha(b),'operator_sha256':sha(op),'argv':['/usr/bin/python3','-B',str(source)],'cwd':str(R),'operator_pid':os.getpid(),'created_utc':utc(),'production_imported_compiled_executed':False}
    (d/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n');c=dict(pre,schema='pr46-source-v2-independent-private-actual-capture/v1',actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False,started_utc=utc())
    try:
        with (d/'stdout.bin').open('xb') as out,(d/'stderr.bin').open('xb') as err:
            child=subprocess.Popen(pre['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err);c.update(actual_execution=True,pid=child.pid)
            try:c['exit_code']=child.wait(timeout=180);c['completed']=True
            except BaseException:child.kill();c['exit_code']=child.wait();raise
    except BaseException:c['operator_failure']=traceback.format_exc()
    finally:
        c['finished_utc']=utc();c['source_unchanged']=read(source)==b;c['operator_unchanged']=read(pathlib.Path(__file__).absolute())==op
        for k in ['stdout','stderr']:
            q=d/(k+'.bin')
            if q.exists():v=read(q);c[k]={'path':q.name,'bytes':len(v),'sha256':sha(v)}
        ok=c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==0 and c['source_unchanged'] is True and c['operator_unchanged'] is True and 'operator_failure' not in c
        c['status']='PASS_PRIVATE_SOURCE_ONLY' if ok else 'FAILED_PRIVATE_SOURCE_CONTROL_PRESERVED';(d/'CAPTURE.json').write_text(json.dumps(c,indent=2)+'\n')
    print(json.dumps({'actual_pid':c['pid'],'exit_code':c['exit_code'],'status':c['status'],'capture':str(d)}));return 0 if ok else 1
if __name__=='__main__':sys.exit(main())
