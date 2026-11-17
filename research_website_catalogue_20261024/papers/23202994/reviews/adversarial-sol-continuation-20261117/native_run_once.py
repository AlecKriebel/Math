"""One documented, unmodified native checker; custody and literal streams only."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
NATIVE = ROOT / 'native-atomic'
EXPECTED = '5689152e970b652a8e40c3c120eda3b45320c8745968a5cb416fa9b9dbdc5385'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def snapshot(root):
    rows = []
    for path in [root] + sorted(root.rglob('*')):
        info = path.lstat()
        row = {'path': '.' if path == root else path.relative_to(root).as_posix(),
               'mode': oct(stat.S_IMODE(info.st_mode)),
               'type': 'dir' if stat.S_ISDIR(info.st_mode) else 'file'}
        assert stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode), row
        if path.is_file():
            data = path.read_bytes()
            row.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        else:
            row['empty'] = not any(path.iterdir())
        rows.append(row)
    return rows

for name in ['NATIVE_RUN.json', 'NATIVE_STDOUT.bin', 'NATIVE_STDERR.bin',
             'NATIVE_INPUT_BEFORE.json', 'NATIVE_INPUT_AFTER.json']:
    assert not (ROOT / name).exists(), name
assert hashlib.sha256((NATIVE / 'verification/check_certificate.py').read_bytes()).hexdigest() == EXPECTED
assert hashlib.sha256((ROOT / 'primary/openai/atomic/verification/check_certificate.py').read_bytes()).hexdigest() == EXPECTED
before = snapshot(NATIVE)
(ROOT / 'NATIVE_INPUT_BEFORE.json').write_text(json.dumps(before, indent=2) + '\n')
command = ['python3', '-I', 'verification/check_certificate.py']
started = utc()
clock = time.monotonic()
try:
    result = subprocess.run(command, cwd=NATIVE, capture_output=True, timeout=180)
    out, err, code, timeout = result.stdout, result.stderr, result.returncode, False
except subprocess.TimeoutExpired as failure:
    out, err, code, timeout = failure.stdout or b'', failure.stderr or b'', None, True
elapsed = time.monotonic() - clock
ended = utc()
(ROOT / 'NATIVE_STDOUT.bin').write_bytes(out)
(ROOT / 'NATIVE_STDERR.bin').write_bytes(err)
after = snapshot(NATIVE)
(ROOT / 'NATIVE_INPUT_AFTER.json').write_text(json.dumps(after, indent=2) + '\n')
receipt = {'command': command, 'cwd': str(NATIVE), 'attempts': 1,
           'started_utc': started, 'ended_utc': ended, 'elapsed_seconds': elapsed,
           'exit_code': code, 'timeout': timeout, 'input_guard_equal': before == after,
           'stdout_bytes': len(out), 'stderr_bytes': len(err),
           'stdout_sha256': hashlib.sha256(out).hexdigest(),
           'stderr_sha256': hashlib.sha256(err).hexdigest(),
           'python3_resolved': shutil.which('python3'), 'runner_python_version': sys.version,
           'runner_executable': sys.executable, 'runner_assertions_enabled': __debug__,
           'pythonoptimize_environment_present': 'PYTHONOPTIMIZE' in os.environ,
           'checker_sha256': EXPECTED, 'scope': 'finite atomic certificate only',
           'installs': 0, 'repairs': 0, 'switches': 0, 'retries': 0}
(ROOT / 'NATIVE_RUN.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
assert before == after, 'native input mutation'
