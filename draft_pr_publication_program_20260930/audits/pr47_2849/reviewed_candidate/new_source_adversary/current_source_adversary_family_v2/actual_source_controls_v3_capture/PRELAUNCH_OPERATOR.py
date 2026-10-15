#!/usr/bin/env python3
"""Own actual capture. Never launches production or historical mathematical helpers."""
import datetime as dt, hashlib, json, os, subprocess, sys
from pathlib import Path
F=Path(__file__).absolute().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
name=sys.argv[1]; script=F/sys.argv[2]
assert name and '/' not in name and script.parent==F and script.name.startswith('private_')
D=F/name; D.mkdir(exist_ok=False)
source=script.read_bytes(); operator=Path(__file__).read_bytes()
(D/'PRELAUNCH_SOURCE.py').write_bytes(source); (D/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
argv=['/usr/bin/python3','-B',str(script)]
rec={'schema':'pr47-source-v2-adversary-own-actual-capture/v1','argv':argv,'cwd':'/Users/alec/Documents/Math','operator_pid':os.getpid(),'started_utc':utc(),'stdin_supplied':False,'actual_execution':False,'completed':False,'pid':None,'exit_code':None}
with (D/'stdout.bin').open('xb') as out,(D/'stderr.bin').open('xb') as err:
 child=subprocess.Popen(argv,cwd=rec['cwd'],stdin=subprocess.DEVNULL,stdout=out,stderr=err)
 rec.update(actual_execution=True,pid=child.pid); rec['exit_code']=child.wait(timeout=120); rec['completed']=True
rec['finished_utc']=utc()
for k in ['stdout','stderr']:
 b=(D/(k+'.bin')).read_bytes(); rec[k]={'path':k+'.bin','bytes':len(b),'sha256':sha(b)}
rec['source_unchanged']=script.read_bytes()==source; rec['operator_unchanged']=Path(__file__).read_bytes()==operator
rec['production_execution']=False; rec['future_acceptance_approved']=False
(D/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2)); sys.exit(rec['exit_code'])
