#!/usr/bin/python3
"""Actual private capture operator; preserves complete code/proof before child launch."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys

root=Path(__file__).resolve().parent
run=root/'actual_controls'
run.mkdir(mode=0o755)
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
pre={}
for name in ('controls.py','PROOF.md','INITIAL_SCOPE_AND_ARGUMENT.md','capture_controls.py'):
    body=(root/name).read_bytes()
    (run/(name+'.prelaunch')).write_bytes(body)
    pre[name]={'sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'mode_07777':oct((root/name).stat().st_mode&0o7777)}
argv=['/usr/bin/python3','-B',str(root/'controls.py')]
record={'role':'ACTUAL_INDEPENDENT_CONTROL_CAPTURE','operator_pid':os.getpid(),'operator_argv':sys.argv,
        'child_argv':argv,'cwd':str(root),'source_prelaunch':pre,'start_utc':utc()}
(run/'prelaunch.json').write_text(json.dumps(record,indent=2)+'\n')
with open(run/'stdout.json','xb') as out,open(run/'stderr.bin','xb') as err:
    child=subprocess.Popen(argv,cwd=root,stdout=out,stderr=err)
    record['child_pid']=child.pid; record['exit']=child.wait()
record['end_utc']=utc()
for name in ('stdout.json','stderr.bin'):
    body=(run/name).read_bytes();record[name]={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
(run/'capture.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
if record['exit']: raise SystemExit(record['exit'])
