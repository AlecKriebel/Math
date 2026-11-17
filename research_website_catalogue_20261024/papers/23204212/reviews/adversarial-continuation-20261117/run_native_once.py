"""One ordinary unmodified finite-check route, in a fresh isolated directory."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import time

LANE = Path(__file__).resolve().parent
SUPPORT = LANE.parent.parent / 'sources/archives/01-thompson-cstar-verification.zip.extracted'
WORK = LANE / 'native-once'
assert not WORK.exists()
WORK.mkdir()
for name in ('upstream_finite_checks.py', 'LICENSE_CODE.txt'):
    shutil.copy2(SUPPORT / name, WORK / name)

def inputs():
    result = []
    for path in sorted(WORK.iterdir()):
        assert path.is_file() and not path.is_symlink()
        data = path.read_bytes()
        result.append({'name': path.name, 'bytes': len(data),
                       'mode_octal': oct(stat.S_IMODE(path.stat().st_mode)),
                       'sha256': hashlib.sha256(data).hexdigest()})
    return result

before = inputs()
for entry in before:
    assert hashlib.sha256((SUPPORT / entry['name']).read_bytes()).hexdigest() == entry['sha256']
command = ['python3', 'upstream_finite_checks.py']
started = datetime.now(timezone.utc).isoformat()
clock_start = time.monotonic()
outcome = subprocess.run(command, cwd=WORK, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         timeout=60, check=False)
elapsed = time.monotonic() - clock_start
ended = datetime.now(timezone.utc).isoformat()
after = inputs()
(LANE / 'NATIVE.stdout.txt').write_bytes(outcome.stdout)
(LANE / 'NATIVE.stderr.txt').write_bytes(outcome.stderr)
receipt = {'command': command, 'cwd': str(WORK), 'UTC_start': started, 'UTC_end': ended,
           'elapsed_seconds': elapsed, 'exit_code': outcome.returncode,
           'input_before': before, 'input_after': after, 'inputs_exact': before == after,
           'native_attempt_number': 1, 'unmodified': True,
           'scope': 'Finite exact-rational corroboration only; no theorem or Lean kernel certificate'}
(LANE / 'NATIVE_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
print(outcome.stdout.decode())
print(outcome.stderr.decode())
assert outcome.returncode == 0 and before == after, 'Stop: native failure retained; no repair or retry'
