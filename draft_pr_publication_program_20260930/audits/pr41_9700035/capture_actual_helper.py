"""ROOT capture of a fully reviewed administrative helper; never invent execution."""
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


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('capture_name')
    p.add_argument('source')
    p.add_argument('source_sha256')
    p.add_argument('helper_args', nargs=argparse.REMAINDER)
    a = p.parse_args()
    assert a.capture_name and '/' not in a.capture_name and a.capture_name not in ('.', '..')
    script = Path(a.source)
    assert script.is_absolute() and script.is_file() and not script.is_symlink()
    assert script.parent == A / 'acceptance_preparation_family_v2'
    source = script.read_bytes()
    assert sha(source) == a.source_sha256
    assert subprocess.check_output(['git', 'branch', '--show-current'], cwd=R).strip() == b'main'
    helper_args = a.helper_args[1:] if a.helper_args[:1] == ['--'] else a.helper_args
    argv = ['/usr/bin/python3', '-B', str(script), *helper_args]
    dest = A / a.capture_name
    dest.mkdir(mode=0o700)
    with (dest / 'prelaunch_source.py').open('xb') as f:
        f.write(source); f.flush(); os.fsync(f.fileno())
    rec = {'schema': 'root-reviewed-administrative-helper-capture/v1',
           'actual_execution': False, 'completed': False, 'pid': None,
           'argv': argv, 'cwd': str(A), 'source_sha256': sha(source),
           'stdin_supplied': False,
           'started_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
    out, err = b'', b''
    try:
        child = subprocess.Popen(argv, cwd=A, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        rec.update(actual_execution=True, pid=child.pid)
        out, err = child.communicate()
        rec.update(completed=True, exit_code=child.returncode)
    except BaseException:
        rec['operator_error'] = traceback.format_exc()
    rec['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    rec['source_unchanged'] = script.read_bytes() == source
    for name, raw in [('stdout.bin', out), ('stderr.bin', err)]:
        with (dest / name).open('xb') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        rec[name[:-4]] = {'path': name, 'bytes': len(raw), 'sha256': sha(raw)}
    ok = (rec['actual_execution'] is True and rec['completed'] is True
          and type(rec.get('exit_code')) is int and rec['exit_code'] == 0
          and rec['source_unchanged'] is True and 'operator_error' not in rec)
    rec['status'] = 'PASS' if ok else 'FAIL'
    with (dest / 'CAPTURE.json').open('x') as f:
        json.dump(rec, f, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
    fd = os.open(dest, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    assert {f.name for f in dest.iterdir()} == {'CAPTURE.json', 'prelaunch_source.py', 'stdout.bin', 'stderr.bin'}
    print(json.dumps(rec, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
