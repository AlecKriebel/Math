#!/usr/bin/env python3
"""Capture only this family's own explicitly saved source; no reviewed imports."""
import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def pin(path, base):
    raw = path.read_bytes()
    return {'path': path.relative_to(base).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', choices=['inspect_revised_inputs.py', 'finite_guard_controls.py', 'write_review_metadata.py'])
    parser.add_argument('capture')
    a = parser.parse_args()
    source = HERE / a.source
    output = HERE / a.capture
    if output.parent != HERE or output.exists() or output.is_symlink():
        raise ValueError('New direct first-party capture directory required')
    output.mkdir()
    raw = source.read_bytes()
    (output / 'prelaunch_source.py').write_bytes(raw)
    argv = ['/usr/bin/python3', '-B', str(source)]
    start = stamp()
    child = subprocess.Popen(argv, cwd=HERE, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = child.communicate(timeout=180)
    end = stamp()
    (output / 'stdout.bin').write_bytes(stdout)
    (output / 'stderr.bin').write_bytes(stderr)
    receipt = {'schema': 'pr40-revised-static-own-capture/v1', 'started_utc': start,
               'finished_utc': end, 'actual_execution': True, 'completed': True,
               'pid': child.pid, 'argv': argv, 'cwd': str(HERE), 'exit_code': child.returncode,
               'status': 'PASS' if child.returncode == 0 else 'FAILED_RETAINED',
               'source_sha256': sha(raw), 'stdin': 'DEVNULL',
               'stdout': pin(output / 'stdout.bin', output), 'stderr': pin(output / 'stderr.bin', output),
               'reviewed_helper_import_or_execution': False, 'new_substantive_attempts': 0, 'audit_turns': 0}
    (output / 'CAPTURE.json').write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'capture': a.capture, 'pid': child.pid, 'exit_code': child.returncode,
                      'stdout_bytes': len(stdout), 'stderr_bytes': len(stderr),
                      'capture_sha256': sha((output / 'CAPTURE.json').read_bytes())}, sort_keys=True))
    sys.exit(child.returncode)


if __name__ == '__main__':
    main()
