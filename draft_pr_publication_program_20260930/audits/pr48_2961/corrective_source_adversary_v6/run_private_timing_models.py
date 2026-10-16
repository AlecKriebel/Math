"""Actual own private-child capture; no proposed or ROOT helper loading."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess
import sys

F = Path(__file__).absolute().parent
R = F.parents[3]
D = F / 'PRIVATE_TIMING_ACTUAL_CAPTURE'

def sha(body):
    return hashlib.sha256(body).hexdigest()

def put(name, body):
    with (D / name).open('xb') as stream:
        stream.write(body)

def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()

os.umask(0o022)
D.mkdir()
source = (F / 'private_timing_models.py').read_bytes()
operator = Path(__file__).read_bytes()
put('PRELAUNCH_SOURCE.py', source)
put('PRELAUNCH_OPERATOR.py', operator)
argv = [sys.executable, '-B', str(F / 'private_timing_models.py')]
pre = dict(schema='pr48-v6-own-private-prelaunch/v1', argv=argv, cwd=str(R), actual_operator_pid=os.getpid(), prepared_utc=dt.datetime.now(dt.timezone.utc).isoformat(), source_sha256=sha(source), operator_sha256=sha(operator), stdin_supplied=False, proposed_or_production_code_loaded=False)
put('PRELAUNCH.json', encode(pre))
started = dt.datetime.now(dt.timezone.utc).isoformat()
child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
out, err = child.communicate()
finished = dt.datetime.now(dt.timezone.utc).isoformat()
put('stdout.bin', out)
put('stderr.bin', err)
capture = dict(pre, schema='pr48-v6-own-private-actual-capture/v1', actual_execution=True, completed=True, pid=child.pid, exit_code=child.returncode, started_utc=started, finished_utc=finished, source_unchanged=(F / 'private_timing_models.py').read_bytes() == source, operator_unchanged=Path(__file__).read_bytes() == operator, stdout=dict(path='stdout.bin', bytes=len(out), sha256=sha(out)), stderr=dict(path='stderr.bin', bytes=len(err), sha256=sha(err)), status='PASS' if child.returncode == 0 and not err else 'FAIL')
put('CAPTURE.json', encode(capture))
assert all(stat.S_IMODE(q.stat().st_mode) == 0o644 for q in D.iterdir()) and stat.S_IMODE(D.stat().st_mode) == 0o755
print(json.dumps(dict(status=capture['status'], actual_private_pid=child.pid, capture=str(D / 'CAPTURE.json'), full_stdout_retained=True, full_stderr_retained=True, production_loaded=False)))
assert capture['status'] == 'PASS'
