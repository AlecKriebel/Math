"""Genuine capture of this family's independent audit code, never production."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import traceback

HERE = Path(__file__).absolute().parent
REPO = HERE.parents[3]
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(x): return (json.dumps(x, indent=2, allow_nan=False) + '\n').encode()
assert __debug__ and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0')
assert len(sys.argv) == 3
name, filename = sys.argv[1:]
assert '/' not in name and name not in ('', '.', '..')
assert filename in ('independent_source_controls.py', 'supplemental_gate_controls.py', 'inspect_before_closure.py')
source = HERE / filename
body = source.read_bytes()
operator = Path(__file__).read_bytes()
dest = HERE / name
dest.mkdir(exist_ok=False)
for label, raw in [('PRELAUNCH_SOURCE.py', body), ('PRELAUNCH_OPERATOR.py', operator)]:
    with (dest / label).open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
argv = ['/usr/bin/python3', '-B', str(source)]
rec = {'schema': 'pr44-independent-source-adversary-actual-capture/v1',
       'operator_pid': os.getpid(), 'argv': argv, 'cwd': str(REPO), 'started_utc': now(),
       'source_sha256': sha(body), 'operator_sha256': sha(operator), 'actual_execution': False,
       'completed': False, 'pid': None, 'exit_code': None, 'stdin_supplied': False,
       'production_import_compile_execution': False}
child = None
try:
    with (dest / 'stdout.bin').open('xb') as out, (dest / 'stderr.bin').open('xb') as err:
        child = subprocess.Popen(argv, cwd=REPO, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                 env=dict(os.environ, PYTHONOPTIMIZE='0', GIT_OPTIONAL_LOCKS='0'))
        rec.update(actual_execution=True, pid=child.pid)
        try:
            rec['exit_code'] = child.wait(timeout=180)
            rec['completed'] = True
        except BaseException:
            child.kill(); rec['exit_code'] = child.wait(); raise
except BaseException:
    rec['failure'] = traceback.format_exc()
finally:
    rec['finished_utc'] = now()
    for channel in ('stdout', 'stderr'):
        p = dest / (channel + '.bin')
        if p.exists():
            raw = p.read_bytes(); rec[channel] = {'path': p.name, 'bytes': len(raw), 'sha256': sha(raw)}
    rec['source_unchanged'] = source.read_bytes() == body
    rec['operator_unchanged'] = Path(__file__).read_bytes() == operator
    rec['status'] = 'PASS' if rec['actual_execution'] is True and rec['completed'] is True and rec['exit_code'] == 0 and rec['source_unchanged'] and rec['operator_unchanged'] and 'failure' not in rec else 'FAIL_PRESERVED'
    (dest / 'CAPTURE.json').write_bytes(dump(rec))
print(json.dumps(rec, indent=2))
sys.exit(0 if rec['status'] == 'PASS' else 1)
