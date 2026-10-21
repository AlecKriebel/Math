#!/usr/bin/env python3
"""Standalone recorder; intentionally does not import candidate code."""
import argparse
import datetime
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent

def native_utc():
    p = subprocess.run(['/bin/date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], cwd=HERE, capture_output=True)
    return {'argv': p.args, 'exit': p.returncode,
            'stdout': p.stdout.decode('utf-8', 'replace'),
            'stderr': p.stderr.decode('utf-8', 'replace')}

ap = argparse.ArgumentParser()
ap.add_argument('--name', required=True)
ap.add_argument('command', nargs=argparse.REMAINDER)
ns = ap.parse_args()
argv = ns.command[1:] if ns.command[:1] == ['--'] else ns.command
if not argv:
    ap.error('no command')
base = HERE / 'runs' / ns.name
base.mkdir(parents=True, exist_ok=False)
start = native_utc()
record = {'argv': argv, 'cwd': str(HERE), 'start_native_date': start}
try:
    p = subprocess.run(argv, cwd=HERE, capture_output=True)
    out, err, status = p.stdout, p.stderr, p.returncode
except BaseException as e:
    out, err, status = b'', repr(e).encode(), None
    record['runner_exception'] = repr(e)
end = native_utc()
(base / 'stdout.bin').write_bytes(out)
(base / 'stderr.bin').write_bytes(err)
(base / 'stdout.txt').write_text(out.decode('utf-8', 'replace'))
(base / 'stderr.txt').write_text(err.decode('utf-8', 'replace'))
record.update({'end_native_date': end, 'exit': status,
               'stdout_bytes': len(out), 'stderr_bytes': len(err)})
(base / 'record.json').write_text(json.dumps(record, indent=2) + '\n')
sys.stdout.buffer.write(out)
sys.stderr.buffer.write(err)
print('\nNATIVE_RUN_RECORD ' + str(base / 'record.json'), file=sys.stderr)
sys.exit(status if status is not None and status >= 0 else 1)
