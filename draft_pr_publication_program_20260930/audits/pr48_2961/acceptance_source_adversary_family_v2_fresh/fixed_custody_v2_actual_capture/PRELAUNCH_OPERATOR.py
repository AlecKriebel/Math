"""Capture only this reviewer's independent private model or readonly audit."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

F = Path(__file__).absolute().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, indent=2) + '\n').encode()


def put(path, raw):
    with path.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def main():
    p = argparse.ArgumentParser()
    p.add_argument('name')
    p.add_argument('source', choices=['private_controls.py', 'audit_fixed_inputs.py', 'audit_fixed_inputs_v2.py'])
    a = p.parse_args()
    if not a.name or '/' in a.name or a.name in {'.', '..'}:
        raise ValueError('Only a new adjacent capture folder')
    dest = F / a.name
    dest.mkdir(mode=0o700)
    source = F / a.source
    sb = source.read_bytes()
    ob = Path(__file__).read_bytes()
    argv = ['/usr/bin/python3', '-B', str(source)]
    pre = {'argv': argv, 'cwd': str(F), 'source_sha256': sha(sb),
           'operator_sha256': sha(ob), 'production_imported_compiled_executed': False}
    put(dest / 'PRELAUNCH.json', encoded(pre))
    put(dest / 'PRELAUNCH_SOURCE.py', sb)
    put(dest / 'PRELAUNCH_OPERATOR.py', ob)
    rec = {'schema': 'pr48-v2-fresh-source-adversary-private-capture/v1',
           **pre, 'operator_pid': os.getpid(),
           'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
           'stdin_supplied': False, 'actual_execution': False, 'completed': False}
    child = subprocess.Popen(argv, cwd=F, stdin=subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    rec.update(actual_execution=True, pid=child.pid)
    out, err = child.communicate()
    rec.update(completed=True, exit_code=child.returncode,
               finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
               source_unchanged=source.read_bytes() == sb,
               operator_unchanged=Path(__file__).read_bytes() == ob)
    for channel, raw in [('stdout', out), ('stderr', err)]:
        put(dest / (channel + '.bin'), raw)
        rec[channel] = {'path': channel + '.bin', 'bytes': len(raw), 'sha256': sha(raw)}
    rec['status'] = ('PASS' if child.returncode == 0 and rec['source_unchanged']
                     and rec['operator_unchanged'] else 'FAIL')
    put(dest / 'CAPTURE.json', encoded(rec))
    print(json.dumps(rec, sort_keys=True))
    return 0 if rec['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
