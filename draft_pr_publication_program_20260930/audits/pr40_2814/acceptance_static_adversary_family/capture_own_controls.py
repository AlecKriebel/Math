#!/usr/bin/env python3
"""Capture this family's own independent controls only; not reviewed helpers."""
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
program = sys.argv[1]
if program not in {'inspect_static_inputs.py', 'independent_static_controls.py'}:
    raise ValueError('Only this family\'s own independent control sources may run')
directory = HERE / (program.removesuffix('.py') + '_actual_capture')
directory.mkdir()
source = (HERE / program).read_bytes()
(directory / 'prelaunch_source.py').write_bytes(source)
argv = ['/usr/bin/python3', str(HERE / program)]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
record = {'schema': 'pr40-own-independent-static-control-capture/v1', 'argv': argv, 'cwd': str(HERE),
          'source_program': program, 'source_sha256': hashlib.sha256(source).hexdigest(),
          'started_utc': started, 'actual_execution': False, 'reviewed_helpers_executed': False}
(directory / 'PRELAUNCH.json').write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
try:
    process = subprocess.Popen(argv, cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    record.update(actual_execution=True, pid=process.pid)
    try:
        stdout, stderr = process.communicate(timeout=90)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        record['timeout'] = True
    record['exit_code'] = process.returncode
except OSError as failure:
    stdout, stderr = b'', str(failure).encode()
    record.update(exit_code=None, launch_failure_type=type(failure).__name__, launch_failure=str(failure))
(directory / 'stdout.bin').write_bytes(stdout)
(directory / 'stderr.bin').write_bytes(stderr)
record.update(finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), completed=True,
              status='PASS_OWN_CONTROL_EXECUTION' if record['exit_code'] == 0 else 'FAIL_OWN_CONTROL_EXECUTION',
              stdout={'path': 'stdout.bin', 'bytes': len(stdout), 'sha256': hashlib.sha256(stdout).hexdigest()},
              stderr={'path': 'stderr.bin', 'bytes': len(stderr), 'sha256': hashlib.sha256(stderr).hexdigest()})
(directory / 'CAPTURE.json').write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
print(json.dumps({'status': record['status'], 'pid': record.get('pid'), 'exit_code': record['exit_code'],
                  'capture': str(directory / 'CAPTURE.json'), 'stdout_bytes': len(stdout), 'stderr_bytes': len(stderr)}))
if record['exit_code'] != 0:
    sys.exit(1)
