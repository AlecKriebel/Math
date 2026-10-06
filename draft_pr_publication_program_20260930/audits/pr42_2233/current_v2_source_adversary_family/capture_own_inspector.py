"""Actual retained execution of only this family's own independent inspector."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback
F=Path(__file__).resolve().parent
label=sys.argv[1] if len(sys.argv)==2 else 'ACTUAL_INSPECTOR_CAPTURE'
assert label in {'ACTUAL_INSPECTOR_CAPTURE','ACTUAL_INSPECTOR_CAPTURE_v2','ACTUAL_INSPECTOR_CAPTURE_v3'}
D=F/label;D.mkdir(exist_ok=False)
S=F/'independent_inspector.py';source=S.read_bytes();operator=Path(__file__).read_bytes()
(D/'PRELAUNCH_SOURCE.py').write_bytes(source);(D/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
rec=dict(schema='PR42_V2_INDEPENDENT_OWN_ACTUAL_CAPTURE_v1',operator_pid=os.getpid(),argv=['/usr/bin/python3','-B',str(S)],cwd=str(F),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False,source_sha256=hashlib.sha256(source).hexdigest(),operator_sha256=hashlib.sha256(operator).hexdigest(),builder_or_mathematical_helper_import_compile_execute=False)
try:
    with (D/'stdout.bin').open('xb') as out,(D/'stderr.bin').open('xb') as err:
        child=subprocess.Popen(rec['argv'],cwd=F,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
        rec.update(actual_execution=True,pid=child.pid)
        try: rec['exit_code']=child.wait(timeout=55);rec['completed']=True
        except BaseException: child.kill();rec['exit_code']=child.wait();raise
except BaseException: rec['failure']=traceback.format_exc()
finally:
    rec['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
    for c in ['stdout','stderr']:
        p=D/(c+'.bin')
        if p.exists():
            raw=p.read_bytes();rec[c]=dict(path=p.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    rec['source_unchanged']=S.read_bytes()==source;rec['operator_unchanged']=Path(__file__).read_bytes()==operator
    (D/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
sys.exit(0 if rec['completed'] and rec['exit_code']==0 and 'failure' not in rec else 1)
