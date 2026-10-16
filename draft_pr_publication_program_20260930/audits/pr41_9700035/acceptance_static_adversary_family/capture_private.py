#!/usr/bin/env python3
"""Capture one own script with real child PID, clocks, whole source and channels."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

OWN = Path(__file__).resolve().parent


def main():
    p = argparse.ArgumentParser()
    p.add_argument('script', choices=['inspect_inputs.py', 'finite_controls.py', 'final_check.py'])
    p.add_argument('capture_name')
    a = p.parse_args()
    source = OWN / a.script
    capture = OWN / a.capture_name
    if capture.parent != OWN or capture.exists() or capture.is_symlink():
        raise ValueError('New private direct-child capture required')
    capture.mkdir()
    source_bytes = source.read_bytes()
    (capture / 'prelaunch_source.py').write_bytes(source_bytes)
    argv = [sys.executable, '-B', str(source)]
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    with (capture / 'stdout.bin').open('xb') as stdout, (capture / 'stderr.bin').open('xb') as stderr:
        child = subprocess.Popen(argv, cwd=OWN, env=env, stdin=subprocess.DEVNULL,
                                 stdout=stdout, stderr=stderr)
        pid = child.pid
        code = child.wait(timeout=60)
    finished = dt.datetime.now(dt.timezone.utc).isoformat()
    def row(name):
        raw = (capture / name).read_bytes()
        return {'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    obj = {'actual_execution': True, 'completed': True, 'pid': pid, 'argv': argv,
           'cwd': str(OWN), 'started_utc': started, 'finished_utc': finished,
           'exit_code': code, 'status': 'PASS' if code == 0 else 'FAILED_RETAINED',
           'stdin_supplied': False, 'source_sha256': hashlib.sha256(source_bytes).hexdigest(),
           'stdout': row('stdout.bin'), 'stderr': row('stderr.bin'),
           'candidate_code_imported_compiled_or_executed': False}
    with (capture / 'CAPTURE.json').open('x') as out:
        json.dump(obj, out, indent=2)
        out.write('\n')
    print(json.dumps(obj, indent=2))
    sys.exit(code)


if __name__ == '__main__':
    main()
