"""Launch only this family's handwritten read-only control, preserving failures."""
from pathlib import Path
import datetime as dt, hashlib, json, os, subprocess, sys
H=Path(__file__).resolve().parent
source=H/'private_static_audit.py'
name=sys.argv[1]
if not name or '/' in name or name in {'.','..'}:raise ValueError('safe own capture name')
C=H/name;C.mkdir(exist_ok=False)
raw=source.read_bytes();(C/'PRELAUNCH_SOURCE.py').write_bytes(raw)
(C/'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
clock=lambda:dt.datetime.now(dt.timezone.utc).isoformat()
argv=[sys.executable,'-B',str(source)]
rec={'schema':'pr42-independent-private-readonly-control-capture/v1','argv':argv,'cwd':str(H),'started_utc':clock(),'source_sha256':sha(raw),'stdin_supplied':False}
with (C/'stdout.bin').open('xb') as out,(C/'stderr.bin').open('xb') as err:
    proc=subprocess.Popen(argv,cwd=H,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
    rec.update(pid=proc.pid,actual_execution=True);code=proc.wait()
rec.update(completed=True,exit_code=code,finished_utc=clock(),source_unchanged=source.read_bytes()==raw,status='PASS' if code==0 else 'FAIL')
for k in ['stdout','stderr']:
    b=(C/(k+'.bin')).read_bytes();rec[k]={'path':k+'.bin','bytes':len(b),'sha256':sha(b)}
rec.update(proposed_helpers_imported_compiled_executed=False,native_helper_imported_compiled_executed=False,native_Git_remote_people_mutations=False)
(C/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec));sys.exit(code)
