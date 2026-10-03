"""Genuine retained capture of the independent full closed-JSON reader."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import traceback

F=Path(__file__).resolve().parent
D=F/'ACTUAL_JSON_READER_CAPTURE'
D.mkdir(exist_ok=False)
S=F/'read_closed_json.py'
source=S.read_bytes()
operator=Path(__file__).read_bytes()
(D/'PRELAUNCH_SOURCE.py').write_bytes(source)
(D/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
argv=['/usr/bin/python3','-B',str(S)]
rec=dict(schema='PR42_INDEPENDENT_ADVERSARY_ACTUAL_CAPTURE_v1',argv=argv,cwd=str(F),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False,source_sha256=hashlib.sha256(source).hexdigest(),operator_sha256=hashlib.sha256(operator).hexdigest(),builder_or_scientific_helper_import_compile_execute=False)
try:
    with (D/'stdout.bin').open('xb') as out,(D/'stderr.bin').open('xb') as err:
        child=subprocess.Popen(argv,cwd=F,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
        rec.update(actual_execution=True,pid=child.pid)
        rec['exit_code']=child.wait(timeout=60)
        rec['completed']=True
except BaseException:
    rec['failure']=traceback.format_exc()
finally:
    rec['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
    for channel in ['stdout','stderr']:
        p=D/(channel+'.bin')
        if p.exists():
            raw=p.read_bytes()
            rec[channel]=dict(path=p.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    rec['source_unchanged']=S.read_bytes()==source
    rec['operator_unchanged']=Path(__file__).read_bytes()==operator
    (D/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
sys.exit(0 if rec['completed'] and rec['exit_code']==0 and 'failure' not in rec else 1)
