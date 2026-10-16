#!/usr/bin/env python3
"""ROOT's exact six-member capture, including /usr/bin/python3 -B target."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess
import sys

assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
A = Path(__file__).absolute().parent
R = A.parents[2]
D = A / 'original_preparation_closure_actual_capture'
target = A / 'close_original_preparation.py'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def save(name, body):
    with (D / name).open('xb') as handle:
        handle.write(body)
        handle.flush()
        os.fsync(handle.fileno())

assert R == Path('/Users/alec/Documents/Math') and not D.exists()
source = Path(__file__).read_bytes()
body = target.read_bytes()
assert sha(body) == 'ac383e969e766da6bd9424aa613cbe8f0d774cedfd81e3d7b1a6b8fe6869be0d'
assert not target.is_symlink() and stat.S_ISREG(target.stat().st_mode)
D.mkdir(mode=0o700)
save('prelaunch_operator.py', source)
save('prelaunch_target.py', body)
argv = ['/usr/bin/python3', '-B', str(target)]
record = dict(schema='pr48-root-original-closure-actual-command/v1', argv=argv,
    cwd=str(R), operator_pid=os.getpid(), started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
    actual_execution=False, completed=False, pid=None, exit_code=None, stdin_supplied=False,
    operator_sha256=sha(source), target_source=dict(path=str(target), bytes=len(body), sha256=sha(body)))
save('PRELAUNCH.json', (json.dumps(record, indent=2) + '\n').encode())
with (D/'stdout.bin').open('xb') as out, (D/'stderr.bin').open('xb') as err:
    child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=out, stderr=err)
    record.update(actual_execution=True, pid=child.pid)
    record.update(exit_code=child.wait(timeout=60), completed=True)
record.update(finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
    operator_unchanged=Path(__file__).read_bytes() == source, target_unchanged=target.read_bytes() == body)
for channel in ('stdout','stderr'):
    b=(D/(channel+'.bin')).read_bytes()
    record[channel]=dict(path=channel+'.bin',bytes=len(b),sha256=sha(b))
okay = record['actual_execution'] is True and record['completed'] is True and type(record['exit_code']) is int and record['exit_code']==0 and record['operator_unchanged'] is True and record['target_unchanged'] is True
record['status']='CAPTURE_COMPLETED' if okay else 'CAPTURE_FAILED'
save('CAPTURE.json',(json.dumps(record,indent=2)+'\n').encode())
assert {p.name for p in D.iterdir()} == {'prelaunch_operator.py','prelaunch_target.py','PRELAUNCH.json','stdout.bin','stderr.bin','CAPTURE.json'}
for p in D.iterdir():
    p.chmod(0o444)
    assert stat.S_IMODE(p.stat().st_mode)==0o444
print(json.dumps(record,sort_keys=True))
sys.exit(0 if okay else 1)
