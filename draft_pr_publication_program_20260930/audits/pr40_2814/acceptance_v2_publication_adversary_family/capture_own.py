#!/usr/bin/env python3
"""Capture only independently authored local review programs, exactly once."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
assert len(sys.argv)==2 and sys.argv[1] in {'inspect_inputs.py','predicate_controls.py','inspect_wrapper.py','inspect_wrapper_v2.py','write_metadata.py'}
name=sys.argv[1]
program=HERE/name
target=HERE/(program.stem+'_actual_capture')
target.mkdir()
raw=program.read_bytes()
(target/'prelaunch_source.py').write_bytes(raw)
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
argv=[sys.executable,'-B',str(program)]
with (target/'stdout.bin').open('xb') as out,(target/'stderr.bin').open('xb') as err:
    child=subprocess.Popen(argv,cwd=HERE,stdout=out,stderr=err)
    rc=child.wait()
finished=datetime.datetime.now(datetime.timezone.utc).isoformat()
def binding(path):
    payload=path.read_bytes()
    return {'path':path.name,'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()}
receipt={'actual_execution':True,'completed':True,'status':'PASS' if rc==0 else 'FAIL','pid':child.pid,'capture_pid':os.getpid(),'argv':argv,'cwd':str(HERE),'started_utc':started,'finished_utc':finished,'exit_code':rc,'source_sha256':hashlib.sha256(raw).hexdigest(),'stdout':binding(target/'stdout.bin'),'stderr':binding(target/'stderr.bin'),'reviewed_helper_execution':False}
(target/'CAPTURE.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
print(json.dumps({'capture':str(target),'pid':child.pid,'exit_code':rc,'status':receipt['status']}))
sys.exit(rc)
