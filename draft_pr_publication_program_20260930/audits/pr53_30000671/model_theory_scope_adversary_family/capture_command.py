"""Capture an actual independent audit command without conferring ROOT authority."""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import traceback

F = Path(__file__).resolve().parent
R = F.parents[3]

def main():
    p = argparse.ArgumentParser()
    p.add_argument('capture_name')
    p.add_argument('argv', nargs=argparse.REMAINDER)
    a = p.parse_args()
    assert a.capture_name and '/' not in a.capture_name and a.capture_name not in ('.', '..')
    argv = a.argv[1:] if a.argv and a.argv[0] == '--' else a.argv
    assert argv and all(type(x) is str for x in argv)
    dest = F / a.capture_name
    dest.mkdir(mode=0o700)
    source = Path(__file__).read_bytes()
    (dest / 'prelaunch_operator.py').write_bytes(source)
    rec = {'schema': 'pr53-independent-command-capture/v1', 'argv': argv,
           'cwd': str(R), 'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
           'actual_execution': False, 'pid': None, 'completed': False, 'exit_code': None,
           'operator_sha256': hashlib.sha256(source).hexdigest(), 'root_approval': False}
    out, err = b'', b''
    try:
        child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        rec.update(actual_execution=True, pid=child.pid)
        out, err = child.communicate()
        rec.update(completed=True, exit_code=child.returncode)
    except BaseException:
        rec['operator_error'] = traceback.format_exc()
    rec['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    for name, body in [('stdout.bin', out), ('stderr.bin', err)]:
        with (dest / name).open('xb') as stream:
            stream.write(body)
            stream.flush()
            os.fsync(stream.fileno())
        rec[name[:-4]] = {'path': name, 'bytes': len(body),
                         'sha256': hashlib.sha256(body).hexdigest()}
    rec['operator_unchanged'] = Path(__file__).read_bytes() == source
    ok = (rec['actual_execution'] is True and rec['completed'] is True
          and type(rec['exit_code']) is int and rec['exit_code'] == 0
          and rec['operator_unchanged'] is True and 'operator_error' not in rec)
    rec['status'] = 'PASS' if ok else 'FAIL'
    (dest / 'CAPTURE.json').write_text(json.dumps(rec, indent=2) + '\n')
    print(json.dumps(rec, sort_keys=True))
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
