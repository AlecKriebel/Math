"""Retain an explicit read-only evidence command and its complete process streams."""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import traceback

A = Path(__file__).resolve().parent
R = A.parents[2]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('capture_name')
    parser.add_argument('argv', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    assert args.capture_name and '/' not in args.capture_name and args.capture_name not in ('.', '..')
    argv = args.argv[1:] if args.argv and args.argv[0] == '--' else args.argv
    assert argv and all(type(x) is str for x in argv)
    dest = A / args.capture_name
    dest.mkdir(mode=0o700)
    source = Path(__file__).read_bytes()
    (dest / 'prelaunch_operator.py').write_bytes(source)
    rec = {'schema': 'pr47-original-explicit-command-capture/v1', 'argv': argv, 'cwd': str(R),
           'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_execution': False,
           'pid': None, 'exit_code': None, 'completed': False, 'stdin_supplied': False,
           'operator_sha256': hashlib.sha256(source).hexdigest()}
    (dest / 'PRELAUNCH.json').write_text(json.dumps(rec, indent=2) + '\n')
    out, err = b'', b''
    try:
        child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        rec.update(actual_execution=True, pid=child.pid)
        out, err = child.communicate()
        rec.update(completed=True, exit_code=child.returncode)
    except BaseException:
        rec['operator_error'] = traceback.format_exc()
    rec['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    for name, body in [('stdout.bin', out), ('stderr.bin', err)]:
        with (dest / name).open('xb') as f:
            f.write(body)
            f.flush()
            os.fsync(f.fileno())
        rec[name[:-4]] = {'path': name, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}
    rec['operator_unchanged'] = Path(__file__).read_bytes() == source
    ok = rec['actual_execution'] is True and rec['completed'] is True and rec['exit_code'] == 0 and rec['operator_unchanged'] is True and 'operator_error' not in rec
    rec['status'] = 'CAPTURE_COMPLETED' if ok else 'CAPTURE_FAILED'
    (dest / 'CAPTURE.json').write_text(json.dumps(rec, indent=2) + '\n')
    for p in dest.iterdir():
        assert p.is_file() and not p.is_symlink()
        os.chmod(p, 0o444)
        assert p.stat().st_mode & 0o7777 == 0o444
    print(json.dumps(rec, sort_keys=True))
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
