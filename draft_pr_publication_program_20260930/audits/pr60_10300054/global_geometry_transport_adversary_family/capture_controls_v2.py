#!/usr/bin/python3
"""Actual bounded own child capture; exclusive directory, full streams."""
import ast,datetime,hashlib,json,os,stat,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'actual_controls_v2';OUT.mkdir(exist_ok=False)
pins={}
for name in ('controls_v2.py','GLOBAL_OBLIGATIONS_v2.md','INITIAL_SCOPE_AND_ANALYSIS.md','capture_controls_v2.py'):
    p=ROOT/name;body=p.read_bytes()
    if name.endswith('.py'): ast.parse(body.decode(),filename=str(p))
    (OUT/(name+'.prelaunch')).write_bytes(body)
    pins[name]={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'mode_07777':oct(stat.S_IMODE(p.stat().st_mode))}
(OUT/'prelaunch.json').write_text(json.dumps(pins,indent=2)+'\n')
argv=['/usr/bin/python3','-B',str(ROOT/'controls_v2.py')]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (OUT/'stdout.json').open('wb') as out,(OUT/'stderr.bin').open('wb') as err:
    child=subprocess.Popen(argv,cwd=str(ROOT),stdout=out,stderr=err);pid=child.pid;code=child.wait()
record={'role':'ACTUAL_INDEPENDENT_GLOBAL_CONTROL_CAPTURE','operator_pid':os.getpid(),'operator_argv':sys.argv,
        'child_pid':pid,'child_argv':argv,'cwd':str(ROOT),'start_utc':start,
        'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':code,'source_prelaunch':pins}
for name in ('stdout.json','stderr.bin'):
    body=(OUT/name).read_bytes();record[name]={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
(OUT/'capture.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,sort_keys=True));sys.exit(code)
