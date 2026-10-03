"""Actual captures of only the two explicitly allowed authoring/control scripts."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import traceback

P = Path(__file__).resolve().parent
allowed = {'AUTHORING_ACTUAL_CAPTURE': 'author_adjacent_revision.py', 'PERMISSION_ACTUAL_CAPTURE': 'permission_controls.py'}
assert len(sys.argv) == 2 and sys.argv[1] in allowed
capture = P / sys.argv[1]
capture.mkdir(exist_ok=False)
source = P / allowed[sys.argv[1]]
own, body = Path(__file__).read_bytes(), source.read_bytes()
(capture / 'PRELAUNCH_OPERATOR.py').write_bytes(own)
(capture / 'PRELAUNCH_SOURCE.py').write_bytes(body)
rec = dict(schema='PR42_V2_ACTUAL_AUTHORING_OR_FINITE_PERMISSION_CAPTURE_v1',
           argv=['/usr/bin/python3', '-B', str(source)], cwd=str(P),
           started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
           actual_execution=False, completed=False, pid=None, exit_code=None, stdin_supplied=False,
           builder_imported_executed_compiled=False, source_sha256=hashlib.sha256(body).hexdigest(),
           operator_sha256=hashlib.sha256(own).hexdigest())
try:
    with (capture / 'stdout.bin').open('xb') as out, (capture / 'stderr.bin').open('xb') as err:
        child = subprocess.Popen(rec['argv'], cwd=P, stdin=subprocess.DEVNULL, stdout=out, stderr=err)
        rec.update(actual_execution=True, pid=child.pid)
        try:
            rec['exit_code'] = child.wait(timeout=60)
            rec['completed'] = True
        except BaseException:
            child.kill()
            rec['exit_code'] = child.wait()
            raise
except BaseException:
    rec['failure'] = traceback.format_exc()
finally:
    rec['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    for channel in ['stdout', 'stderr']:
        path = capture / (channel + '.bin')
        if path.exists():
            raw = path.read_bytes()
            rec[channel] = dict(path=path.name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    rec['source_unchanged'] = source.read_bytes() == body
    rec['operator_unchanged'] = Path(__file__).read_bytes() == own
    (capture / 'CAPTURE.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps(rec, indent=2))
sys.exit(0 if rec['completed'] and rec['exit_code'] == 0 and 'failure' not in rec else 1)
