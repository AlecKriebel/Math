"""Actual capture of this family's authoring, inspection and private controls only."""
import datetime as dt, hashlib, json, os, stat, subprocess, sys, traceback
from pathlib import Path
F=Path(__file__).absolute().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def raw(p):
    if p.is_symlink() or any(x.is_symlink() for x in p.parents) or not stat.S_ISREG(p.stat().st_mode): raise ValueError('Regular nonsymlink required')
    return p.read_bytes()
def dump(p,o):
    with p.open('xb') as h: h.write((json.dumps(o,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()); h.flush(); os.fsync(h.fileno())
def main():
    source,name=sys.argv[1:]
    if source not in ['private_capture_class_controls_v2_final_v2.py'] or '/' in name: raise ValueError('Preparation source whitelist only')
    if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'): raise ValueError('No optimized guards')
    p=F/source; body=raw(p); operator=raw(Path(__file__).absolute()); out=F/name; out.mkdir(exist_ok=False)
    (out/'PRELAUNCH_SOURCE.py').write_bytes(body); (out/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
    pre={'schema':'PR47_SOURCE_V2_PREPARATION_PRELAUNCH_v1','argv':['/usr/bin/python3','-B',str(p)],'cwd':str(F.parent.parents[2]),'operator_pid':os.getpid(),'started_utc':now(),'source_sha256':sha(body),'operator_sha256':sha(operator),'production_import_compile_or_execution':False}
    dump(out/'PRELAUNCH.json',pre)
    rec=dict(pre,schema='PR47_SOURCE_V2_PREPARATION_ACTUAL_CAPTURE_v1',actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False)
    try:
        with (out/'stdout.bin').open('xb') as stdout,(out/'stderr.bin').open('xb') as stderr:
            child=subprocess.Popen(pre['argv'],cwd=pre['cwd'],stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr)
            rec.update(actual_execution=True,pid=child.pid)
            try: rec['exit_code']=child.wait(timeout=60); rec['completed']=True
            except BaseException: child.kill(); rec['exit_code']=child.wait(); raise
    except BaseException: rec['operator_failure']=traceback.format_exc()
    finally:
        rec.update(finished_utc=now(),source_unchanged=raw(p)==body,operator_unchanged=raw(Path(__file__).absolute())==operator)
        for channel in ['stdout','stderr']:
            b=raw(out/(channel+'.bin')); rec[channel]={'path':channel+'.bin','bytes':len(b),'sha256':sha(b)}
        dump(out/'CAPTURE.json',rec)
    print(json.dumps({'capture':name,'pid':rec['pid'],'exit_code':rec['exit_code'],'production_import_compile_or_execution':False}))
    return 0 if rec['completed'] and rec['exit_code']==0 and rec['source_unchanged'] and rec['operator_unchanged'] and 'operator_failure' not in rec else 1
if __name__=='__main__': sys.exit(main())
