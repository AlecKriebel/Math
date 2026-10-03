#!/usr/bin/env python3
"""Capture only this adversary's handwritten static inspector, once."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import traceback
F = Path(__file__).absolute().parent
source = F / 'inspect_static_source.py'
capture = F / 'OWN_STATIC_INSPECTION_ACTUAL_CAPTURE'
capture.mkdir(exist_ok=False)
def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(raw):
    return hashlib.sha256(raw).hexdigest()
raw, operator = source.read_bytes(), Path(__file__).read_bytes()
(capture / 'PRELAUNCH_SOURCE.py').write_bytes(raw)
(capture / 'PRELAUNCH_OPERATOR.py').write_bytes(operator)
record = dict(schema='PR43_NEW_SOURCE_ADVERSARY_ACTUAL_OWN_STATIC_CAPTURE_v1', operator_pid=os.getpid(),
      argv=['/usr/bin/python3', '-B', str(source)], cwd=str(F), started_utc=stamp(), stdin_supplied=False,
      actual_execution=False, completed=False, pid=None, exit_code=None, source_sha256=sha(raw), operator_sha256=sha(operator))
try:
    with (capture / 'stdout.bin').open('xb') as out, (capture / 'stderr.bin').open('xb') as err:
        child = subprocess.Popen(record['argv'], cwd=F, stdin=subprocess.DEVNULL, stdout=out, stderr=err)
        record.update(actual_execution=True, pid=child.pid)
        try:
            record['exit_code'] = child.wait(timeout=60)
            record['completed'] = True
        except BaseException:
            child.kill()
            record['exit_code'] = child.wait()
            raise
except BaseException:
    record['failure'] = traceback.format_exc()
finally:
    record['finished_utc'] = stamp()
    for channel in ['stdout', 'stderr']:
        path = capture / (channel + '.bin')
        if path.exists():
            body = path.read_bytes()
            record[channel] = dict(path=path.name, bytes=len(body), sha256=sha(body))
    record['source_unchanged'] = source.read_bytes() == raw
    record['operator_unchanged'] = Path(__file__).read_bytes() == operator
    record['candidate_source_import_compile_execution'] = False
    record['future_freeze_or_whole_current_PASS_claimed'] = False
    (capture / 'CAPTURE.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
raise SystemExit(0 if record['actual_execution'] and record['completed'] and record['exit_code'] == 0 and 'failure' not in record else 1)
