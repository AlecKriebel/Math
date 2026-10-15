#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
HERE=Path(__file__).resolve().parent
run=HERE/'edge_capture'
run.mkdir(exist_ok=False)
script=HERE/'edge_mutation_checks.py'
body=script.read_bytes()
operator=Path(__file__).resolve().read_bytes()
(run/'prelaunch_edge_mutation_checks.py').write_bytes(body)
(run/'prelaunch_operator.py').write_bytes(operator)
def utc():return datetime.now(timezone.utc).isoformat()
def bind(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
argv=['/usr/bin/python3','-B',str(script)]
start=utc()
with (run/'stdout.bin').open('wb') as out,(run/'stderr.bin').open('wb') as err:
    p=subprocess.Popen(argv,cwd=str(HERE),stdout=out,stderr=err)
    pid=p.pid
    code=p.wait()
end=utc()
stdout=(run/'stdout.bin').read_bytes()
stderr=(run/'stderr.bin').read_bytes()
cap={'schema':'private-independent-edge-capture-v1','argv':argv,'cwd':str(HERE),
 'operator_pid':os.getpid(),'child_pid':pid,'utc_start':start,'utc_end':end,
 'exit_code':code,'source':bind(body),'prelaunch_operator':bind(operator),
 'source_unchanged_after':script.read_bytes()==body,
 'operator_unchanged_after':Path(__file__).resolve().read_bytes()==operator,
 'stdout':bind(stdout),'stderr':bind(stderr),'production_executed':False,
 'ROOT_authority':False}
(run/'CAPTURE.json').write_text(json.dumps(cap,indent=2,sort_keys=True)+'\n')
print(json.dumps(cap,indent=2,sort_keys=True))
if code==0:
    result=json.loads(stdout)
    (HERE/'EDGE_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS: edge controls; assertions='+str(result['total_assertions']))
sys.exit(code)
