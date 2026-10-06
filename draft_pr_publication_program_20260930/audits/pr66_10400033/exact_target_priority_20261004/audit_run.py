#!/usr/bin/env python3
"""Capture real process custody without copying publication bodies to Git.

Usage: python3 audit_run.py LABEL -- executable arg ...
Raw stdout/stderr are private; this folder receives only receipts.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PRIVATE = Path('/Users/alec/.cache/pr66_exact_target_priority_20261004')

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def stat(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}

def main():
    label, sep, *command = sys.argv[1:]
    assert sep == '--' and command
    assert all(c.isalnum() or c in '_-' for c in label)
    PRIVATE.mkdir(parents=True, exist_ok=True)
    (PRIVATE / 'raw').mkdir(exist_ok=True)
    (ROOT / 'receipts').mkdir(exist_ok=True)
    path = ROOT / 'receipts' / (label + '.json')
    if path.exists():
        raise SystemExit('Refusing to overwrite receipt: ' + str(path))
    out = PRIVATE / 'raw' / (label + '.stdout')
    err = PRIVATE / 'raw' / (label + '.stderr')
    start = utc()
    mono = time.monotonic()
    with out.open('wb') as o, err.open('wb') as e:
        proc = subprocess.Popen(command, cwd=ROOT, stdout=o, stderr=e)
        pid = proc.pid
        code = proc.wait()
    receipt = {'label': label, 'kind': 'executed_subprocess',
               'started_at_utc': start, 'finished_at_utc': utc(),
               'elapsed_seconds': time.monotonic()-mono,
               'recorder_pid': os.getpid(), 'subprocess_pid': pid,
               'cwd': str(ROOT), 'argv': command, 'returncode': code,
               'stdout': stat(out), 'stderr': stat(err)}
    path.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))
    return code

if __name__ == '__main__':
    raise SystemExit(main())
