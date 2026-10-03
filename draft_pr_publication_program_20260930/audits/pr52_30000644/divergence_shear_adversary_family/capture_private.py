#!/usr/bin/env python3
"""One real private run, preserving complete streams and prelaunch source."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys

HERE=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
source=HERE/'independent_checks.py'
run=HERE/'private_capture'
run.mkdir(exist_ok=False)
body=source.read_bytes()
(run/'prelaunch_independent_checks.py').write_bytes(body)
argv=['/usr/bin/python3','-B',str(source)]
start=utc()
with (run/'stdout.bin').open('wb') as out, (run/'stderr.bin').open('wb') as err:
    child=subprocess.Popen(argv,cwd=str(HERE),stdout=out,stderr=err,
                           env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    pid=child.pid
    code=child.wait()
end=utc()
stdout=(run/'stdout.bin').read_bytes()
stderr=(run/'stderr.bin').read_bytes()
capture={'schema':'private-independent-capture-v1','argv':argv,'cwd':str(HERE),
         'operator_pid':os.getpid(),'child_pid':pid,'utc_start':start,'utc_end':end,
         'exit_code':code,'source':{'path':str(source),'bytes':len(body),'sha256':sha(body)},
         'source_unchanged_after':source.read_bytes()==body,
         'stdout':{'bytes':len(stdout),'sha256':sha(stdout)},
         'stderr':{'bytes':len(stderr),'sha256':sha(stderr)},
         'production_executed':False,'ROOT_authority':False}
(run/'CAPTURE.json').write_text(json.dumps(capture,indent=2,sort_keys=True)+'\n')
print(json.dumps(capture,indent=2,sort_keys=True))
if code==0:
    result=json.loads(stdout)
    (HERE/'RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS: private independent checker; assertions='+str(result['total_assertions']))
sys.exit(code)
