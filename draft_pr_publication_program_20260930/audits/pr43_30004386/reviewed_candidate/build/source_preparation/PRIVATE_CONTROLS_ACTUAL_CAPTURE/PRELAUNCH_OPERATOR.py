#!/usr/bin/env python3
"""Actual captures of this preparer's two narrow own authoring/private operations.

An exact allowlist excludes builder/operator/candidate/family mathematical
sources. No source is imported or compiled for inspection. Failures are kept.
"""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

P = Path(__file__).absolute().parent
allowed = {'AUTHORING_ACTUAL_CAPTURE': 'author_source_documents.py',
           'PRIVATE_CONTROLS_ACTUAL_CAPTURE': 'private_contract_controls.py'}
if len(sys.argv) != 2 or sys.argv[1] not in allowed:
    raise ValueError('Exactly one allowed own operation required')
require_source = P / allowed[sys.argv[1]]
capture = P / sys.argv[1]
capture.mkdir(exist_ok=False)
source, operator = require_source.read_bytes(), Path(__file__).read_bytes()
(capture / 'PRELAUNCH_SOURCE.py').write_bytes(source)
(capture / 'PRELAUNCH_OPERATOR.py').write_bytes(operator)
record = dict(schema='PR43_PREPARER_OWN_ACTUAL_OPERATION_CAPTURE_v1',
    operator_pid=os.getpid(), argv=['/usr/bin/python3', '-B', str(require_source)], cwd=str(P),
    started_utc=dt.datetime.now(dt.timezone.utc).isoformat(), actual_execution=False,
    completed=False, pid=None, exit_code=None, stdin_supplied=False,
    source_sha256=hashlib.sha256(source).hexdigest(), operator_sha256=hashlib.sha256(operator).hexdigest(),
    builder_future_ROOT_operator_or_scientific_helpers_imported_compiled_executed=False)
try:
    with (capture / 'stdout.bin').open('xb') as out, (capture / 'stderr.bin').open('xb') as err:
        child = subprocess.Popen(record['argv'], cwd=P, stdin=subprocess.DEVNULL, stdout=out, stderr=err)
        record.update(actual_execution=True, pid=child.pid)
        try:
            record['exit_code'] = child.wait(timeout=60)
            record['completed'] = True
        except BaseException:
            child.kill(); record['exit_code'] = child.wait()
            raise
except BaseException:
    record['failure'] = traceback.format_exc()
finally:
    record['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    for channel in ['stdout', 'stderr']:
        path = capture / (channel + '.bin')
        if path.exists():
            raw = path.read_bytes()
            record[channel] = dict(path=path.name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    record['source_unchanged'] = require_source.read_bytes() == source
    record['operator_unchanged'] = Path(__file__).read_bytes() == operator
    with (capture / 'CAPTURE.json').open('x') as out:
        json.dump(record, out, indent=2); out.write('\n')
print(json.dumps(record, indent=2))
sys.exit(0 if record['actual_execution'] is True and record['completed'] is True and
         type(record['exit_code']) is int and record['exit_code'] == 0 and 'failure' not in record else 1)
