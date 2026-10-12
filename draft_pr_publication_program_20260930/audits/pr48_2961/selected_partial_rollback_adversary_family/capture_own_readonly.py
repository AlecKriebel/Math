"""Capture own read-only inspection, with no production helper invocation."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

if not __debug__ or sys.flags.optimize: raise RuntimeError('Optimized Python refused')
HERE=Path(__file__).resolve().parent
source=HERE/'inspect_source_v2.py'
out=HERE/'actual_source_v2_capture'
out.mkdir()
raw=source.read_bytes()
(out/'PRELAUNCH_SOURCE.py').write_bytes(raw)
argv=[sys.executable,'-B',str(source)]
stamp=lambda:dt.datetime.now(dt.timezone.utc).isoformat()
sha=lambda body:hashlib.sha256(body).hexdigest()
started=stamp()
pre={'controller_pid':os.getpid(),'prepared_utc':started,'argv':argv,'source_sha256':sha(raw),'source_bytes':len(raw),'read_only':True}
(out/'PRELAUNCH.json').write_text(json.dumps(pre,sort_keys=True,indent=2)+'\n')
p=subprocess.Popen(argv,cwd='/Users/alec/Documents/Math',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout,stderr=p.communicate(timeout=90)
finished=stamp()
(out/'stdout.bin').write_bytes(stdout)
(out/'stderr.bin').write_bytes(stderr)
cap={**pre,'pid':p.pid,'started_utc':started,'finished_utc':finished,'exit_code':p.returncode,'stdout':{'bytes':len(stdout),'sha256':sha(stdout)},'stderr':{'bytes':len(stderr),'sha256':sha(stderr)},'complete_streams':True,'production_or_git_mutation_executed':False,'ROOT_approval_claimed':False}
(out/'CAPTURE.json').write_text(json.dumps(cap,sort_keys=True,indent=2)+'\n')
print(json.dumps(cap,sort_keys=True,indent=2))
if p.returncode: print(stderr.decode(errors='replace')); raise SystemExit(p.returncode)
(HERE/'SOURCE_V2_CHECK.json').write_bytes(stdout)
