"""Capture only our new independent static controls, no reviewed runner launch."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import subprocess
import sys

F = Path(__file__).resolve().parent
source = F / 'own_static_controls.py'
output = F / 'own_actual_execution_01'
output.mkdir()
raw = source.read_bytes()
(output / 'prelaunch_source.py').write_bytes(raw)
start = dt.datetime.now(dt.timezone.utc).isoformat()
argv = ['/usr/bin/python3', '-B', str(source)]
child = subprocess.Popen(argv, cwd=F, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = child.communicate(timeout=60)
end = dt.datetime.now(dt.timezone.utc).isoformat()
(output / 'stdout.bin').write_bytes(out)
(output / 'stderr.bin').write_bytes(err)
def pin(path):
    b = path.read_bytes()
    return {'path': path.name, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
value = {'schema': 'pr39-own-runner-static-review-control-capture/v1',
    'actual_execution': True, 'completed': True, 'pid': child.pid, 'argv': argv, 'cwd': str(F),
    'started_utc': start, 'finished_utc': end, 'exit_code': child.returncode,
    'status': 'PASS' if child.returncode == 0 else 'FAIL', 'stdin_supplied': False,
    'runner_and_helpers_imported_or_executed': False,
    'source_sha256': hashlib.sha256(raw).hexdigest(), 'prelaunch_source': pin(output / 'prelaunch_source.py'),
    'stdout': pin(output / 'stdout.bin'), 'stderr': pin(output / 'stderr.bin'),
    'own_source_after_unchanged': source.read_bytes() == raw}
(output / 'CAPTURE.json').write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
print(json.dumps(value, indent=2, sort_keys=True))
print(out.decode())
if err:
    print(err.decode(), file=sys.stderr)
sys.exit(child.returncode)
