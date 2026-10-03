#!/usr/bin/env python3
"""Own explicit private-control capture. Never imports/executes production sources."""
from pathlib import Path
import datetime as dt, hashlib, json, os, subprocess, sys, traceback
F=Path(__file__).absolute().parent
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def digest(b): return hashlib.sha256(b).hexdigest()
assert __debug__ and not sys.flags.optimize
name=sys.argv[1]; source=F/sys.argv[2]
assert source.parent==F and source.name in {'independent_source_controls.py','extended_controls.py','expected_negative.py','closure_capture_validation.py'}
D=F/name; D.mkdir(exist_ok=False)
b=source.read_bytes(); op=Path(__file__).read_bytes()
(D/'PRELAUNCH_SOURCE.py').write_bytes(b); (D/'PRELAUNCH_OPERATOR.py').write_bytes(op)
argv=['/usr/bin/python3','-B',str(source),*sys.argv[3:]]
pre={'schema':'pr47-independent-private-prelaunch/v1','operator_pid':os.getpid(),'started_utc':now(),'argv':argv,'cwd':str(F),'source_sha256':digest(b),'operator_sha256':digest(op),'production_import_compile_execute':False}
(D/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
rec=dict(pre,actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False)
try:
    with (D/'stdout.bin').open('xb') as out,(D/'stderr.bin').open('xb') as err:
        p=subprocess.Popen(argv,cwd=F,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
        rec.update(actual_execution=True,pid=p.pid)
        try: rec['exit_code']=p.wait(timeout=120); rec['completed']=True
        except BaseException: p.kill(); rec['exit_code']=p.wait(); raise
except BaseException: rec['failure']=traceback.format_exc()
finally:
    rec['finished_utc']=now()
    for k in ['stdout','stderr']:
        q=D/(k+'.bin'); raw=q.read_bytes() if q.exists() else b''
        rec[k]={'path':q.name,'bytes':len(raw),'sha256':digest(raw)}
    rec['source_unchanged']=source.read_bytes()==b
    rec['operator_unchanged']=Path(__file__).read_bytes()==op
    rec['status']='COMPLETED_ACTUAL_PRIVATE_CONTROL' if rec['completed'] else 'FAILED_ACTUAL_PRIVATE_CONTROL'
    (D/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
sys.exit(0 if rec['completed'] and rec['exit_code']==0 and rec['source_unchanged'] and rec['operator_unchanged'] else 1)
