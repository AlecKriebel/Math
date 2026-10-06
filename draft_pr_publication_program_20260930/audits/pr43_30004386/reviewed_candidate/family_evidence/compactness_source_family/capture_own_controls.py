"""Exclusive fresh-run capture for this family's own controls only."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):
    raw=p.read_bytes()
    return {'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
base=Path(__file__).resolve().parent
run=base/'own_controls_actual_capture_001'
run.mkdir()  # never replace a prior capture or failure
operator=Path(__file__).resolve()
source=base/'exact_compactness_controls.py'
start=utc()
(run/'prelaunch_control.py').write_bytes(source.read_bytes())
(run/'prelaunch_operator.py').write_bytes(operator.read_bytes())
pre=[digest(run/'prelaunch_control.py'),digest(run/'prelaunch_operator.py')]
argv=[sys.executable,str(run/'prelaunch_control.py')]
with (run/'stdout.bin').open('xb') as out, (run/'stderr.bin').open('xb') as err:
    launched=utc()
    child=subprocess.Popen(argv,cwd=run,stdout=out,stderr=err)
    child_pid=child.pid
    code=child.wait()
end=utc()
record={'schema':'compactness-source-own-execution/v1','capture_pid':os.getpid(),'parent_pid':os.getppid(),'child_pid':child_pid,'start_utc':start,'launch_utc':launched,'end_utc':end,'argv':argv,'cwd':str(run),'prelaunch_sources':pre,'exit_code':code,'actual_execution':True,'stdin_supplied':False,'candidate_imported_compiled_executed':False,'historical_runtime_attestation':False,'FILE':[digest(run/'prelaunch_control.py'),digest(run/'prelaunch_operator.py'),digest(run/'stdout.bin'),digest(run/'stderr.bin')]}
(run/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
print((run/'stdout.bin').read_text())
if code:sys.exit(code)
