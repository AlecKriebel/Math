#!/usr/bin/env python3
"""Replay both independent implementations and compare saved JSON outputs.
Run from any working directory: python3 /path/to/package/reproduce.py
Requires Python 3.8+ standard library; do not use Python's -O option.
"""
import contextlib
import io
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import check_counts

HERE = Path(__file__).resolve().parent
if not __debug__:
    raise SystemExit('Assertions must be enabled. Do not run with -O.')

def compare(name, actual):
    expected = json.loads((HERE / name).read_text(encoding='utf-8'))
    # Normalize integer JSON object keys in freshly computed dictionaries.
    actual = json.loads(json.dumps(actual))
    if actual != expected:
        raise AssertionError('Replay differs from ' + name)
    print(name + ': PASS (exact saved-output match)', flush=True)

started = time.monotonic()
buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    check_counts.run()
compare('counts.json', json.loads(buffer.getvalue()))
compare('certificate.json', check_counts.certificate())
compare('small_crosschecks.json', check_counts.small_expansion_crosscheck())
result = subprocess.run([sys.executable, str(HERE / 'independent_audit.py')],
                        capture_output=True, text=True, check=True, cwd=HERE)
compare('independent_audit.json', json.loads(result.stdout))
print('PASS: both implementations replayed; all four outputs match.')
print('Python: ' + platform.python_version())
print('Elapsed seconds: %.3f' % (time.monotonic() - started))
