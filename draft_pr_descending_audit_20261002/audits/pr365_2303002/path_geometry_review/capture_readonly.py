#!/usr/bin/env python3
"""Run named read-only commands with complete, compressed stream receipts."""
import datetime, gzip, hashlib, json, os, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
CAP = ROOT / 'captures'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def capture(label, argv, cwd=None, timeout=120):
    if (CAP / (label + '.receipt.json')).exists():
        raise ValueError('Receipt label already exists: ' + label)
    cwd = str(cwd or ROOT)
    changes = {'GIT_OPTIONAL_LOCKS': '0', 'GIT_NO_LAZY_FETCH': '1',
               'PYTHONDONTWRITEBYTECODE': '1'}
    env = dict(os.environ, **changes)
    started = utc()
    try:
        proc = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=timeout)
        out, err, code = proc.stdout, proc.stderr, proc.returncode
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        out, err, code = exc.stdout or b'', exc.stderr or b'', None
        timed_out = True
    receipt = {'label': label, 'argv': list(argv), 'cwd': cwd, 'environment_changes': changes,
               'start_utc': started, 'end_utc': utc(), 'exit_code': code,
               'timed_out': timed_out}
    for stream, data in [('stdout', out), ('stderr', err)]:
        target = CAP / (label + '.' + stream + '.gz')
        target.write_bytes(gzip.compress(data, mtime=0))
        receipt[stream] = {'path': str(target.relative_to(ROOT)), 'bytes': len(data),
                           'sha256': hashlib.sha256(data).hexdigest()}
    (CAP / (label + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    return receipt

if __name__ == '__main__':
    label, *argv = sys.argv[1:]
    receipt = capture(label, argv)
    print(json.dumps(receipt, indent=2))
