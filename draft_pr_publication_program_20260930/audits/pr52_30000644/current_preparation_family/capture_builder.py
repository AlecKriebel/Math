#!/usr/bin/env python3
"""Single real text-builder capture; no production operation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
HERE=Path(__file__).resolve().parent
run=HERE/'builder_capture';run.mkdir(exist_ok=False)
source=HERE/'build_current.py';body=source.read_bytes()
operator=Path(__file__).resolve().read_bytes()
(run/'prelaunch_build_current.py').write_bytes(body)
(run/'prelaunch_operator.py').write_bytes(operator)
def utc():return datetime.now(timezone.utc).isoformat()
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
argv=['/usr/bin/python3','-B',str(source)]
start=utc()
with (run/'stdout.bin').open('wb') as out,(run/'stderr.bin').open('wb') as err:
    child=subprocess.Popen(argv,cwd=str(HERE),stdout=out,stderr=err)
    pid=child.pid;code=child.wait()
end=utc()
stdout=(run/'stdout.bin').read_bytes();stderr=(run/'stderr.bin').read_bytes()
value={'schema':'pr52-current-private-builder-capture/v1','argv':argv,'cwd':str(HERE),
 'child_pid':pid,'operator_pid':os.getpid(),'utc_start':start,'utc_end':end,'exit_code':code,
 'source':digest(body),'operator':digest(operator),'stdout':digest(stdout),'stderr':digest(stderr),
 'source_unchanged_after':source.read_bytes()==body,'operator_unchanged_after':Path(__file__).resolve().read_bytes()==operator,
 'ROOT_or_production_execution':False}
(run/'CAPTURE.json').write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
print(json.dumps(value,indent=2,sort_keys=True))
sys.exit(code)
