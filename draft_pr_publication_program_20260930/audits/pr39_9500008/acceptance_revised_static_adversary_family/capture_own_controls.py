"""Capture only the independently authored static reader's actual execution."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import subprocess
import sys

F = Path(__file__).resolve().parent
source = F / 'independent_static_controls.py'
output = F / 'own_actual_execution_01'
output.mkdir()
raw = source.read_bytes()
(output / 'prelaunch_source.py').write_bytes(raw)
started = dt.datetime.now(dt.timezone.utc).isoformat()
argv = ['/usr/bin/python3', '-B', str(source)]
child = subprocess.Popen(argv, cwd=F, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = child.communicate(timeout=120)
finished = dt.datetime.now(dt.timezone.utc).isoformat()
(output / 'stdout.bin').write_bytes(stdout)
(output / 'stderr.bin').write_bytes(stderr)
def pin(path):
    b = path.read_bytes()
    return {'path': path.name, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
capture = {
    'schema': 'pr39-own-revised-static-adversary-actual-execution/v1',
    'actual_execution': True,
    'completed': True,
    'pid': child.pid,
    'argv': argv,
    'cwd': str(F),
    'started_utc': started,
    'finished_utc': finished,
    'exit_code': child.returncode,
    'status': 'PASS' if child.returncode == 0 else 'FAIL',
    'source_sha256': hashlib.sha256(raw).hexdigest(),
    'prelaunch_source': pin(output / 'prelaunch_source.py'),
    'stdout': pin(output / 'stdout.bin'),
    'stderr': pin(output / 'stderr.bin'),
    'stdin_supplied': False,
    'reviewed_helpers_imported_or_executed': False,
    'unchanged_own_source_after': source.read_bytes() == raw,
}
(output / 'CAPTURE.json').write_text(json.dumps(capture, indent=2, sort_keys=True) + '\n')
print(json.dumps(capture, indent=2, sort_keys=True))
if stdout:
    print(stdout.decode())
if stderr:
    print(stderr.decode(), file=sys.stderr)
sys.exit(child.returncode)
