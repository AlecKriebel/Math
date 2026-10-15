#!/usr/bin/env python3
"""Capture only this family's own independent inspectors/models, never reviewed helpers."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
P=Path(__file__).resolve().parent
name=sys.argv[1]
assert name in {'inspect_inputs.py','finite_specification.py'}
source=P/name
capture=P/(name.removesuffix('.py')+'_actual_capture')
capture.mkdir(exist_ok=False)
raw=source.read_bytes();(capture/'prelaunch_source.py').write_bytes(raw)
sha=lambda b:hashlib.sha256(b).hexdigest()
started=dt.datetime.now(dt.timezone.utc).isoformat()
argv=[sys.executable,str(source)]
with (capture/'stdout.bin').open('xb') as out,(capture/'stderr.bin').open('xb') as err:
    child=subprocess.Popen(argv,cwd=P,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
    code=child.wait()
finished=dt.datetime.now(dt.timezone.utc).isoformat()
def row(n):
    b=(capture/n).read_bytes();return {'path':n,'bytes':len(b),'sha256':sha(b)}
record={'schema':'pr41-independent-v2-source-only-own-operation-capture/v1','actual_execution':True,'completed':True,'pid':child.pid,'source_sha256':sha(raw),'source_after_unchanged':source.read_bytes()==raw,'argv':argv,'cwd':str(P),'started_utc':started,'finished_utc':finished,'exit_code':code,'status':'PASS_OWN_OPERATION' if code==0 else 'FAILED_OWN_OPERATION_RETAINED','stdin_supplied':False,'stdout':row('stdout.bin'),'stderr':row('stderr.bin'),'candidate_execution':False}
(capture/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
sys.exit(code)
