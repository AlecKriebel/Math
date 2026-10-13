#!/usr/bin/env python3
"""Capture exact replay streams without copying the author packet or modifying it."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'snapshot' / 'unsolved_math_prioritization' / 'attempts' / '30004435'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(label, arguments, expected=None):
    started = datetime.now(timezone.utc).isoformat(timespec='seconds')
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    proc = subprocess.run([sys.executable, *map(str, arguments)], cwd=HERE,
                          env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = HERE/'artifacts'/f'{label}.stdout.txt'
    err = HERE/'artifacts'/f'{label}.stderr.txt'
    out.write_bytes(proc.stdout)
    err.write_bytes(proc.stderr)
    r = {'label': label, 'started_utc': started,
         'ended_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
         'command_arguments': [sys.executable, *map(str, arguments)],
         'exit_code': proc.returncode, 'stdout_path': str(out.relative_to(HERE)),
         'stderr_path': str(err.relative_to(HERE)),
         'stdout_sha256': sha(proc.stdout), 'stderr_sha256': sha(proc.stderr)}
    if expected is not None:
        b = expected.read_bytes()
        r['frozen_receipt_path'] = str(expected.relative_to(AUTHOR))
        r['frozen_receipt_sha256'] = sha(b)
        r['stdout_equals_frozen_receipt'] = proc.stdout == b
    return r


if __name__ == '__main__':
    results = [run(f'author_turn{n}', [AUTHOR/f'verify_turn{n}.py'],
                   AUTHOR/f'TURN_{n}_CHECKS.json') for n in range(1, 6)]
    results.append(run('old_review_verification',
                       [AUTHOR/'final_review'/'verify_review.py', '--author-dir', AUTHOR]))
    results.append(run('old_review_controls',
                       [AUTHOR/'final_review'/'independent_checks.py'],
                       AUTHOR/'final_review'/'INDEPENDENT_CHECKS.json'))
    success = all(x['exit_code'] == 0 and x.get('stdout_equals_frozen_receipt', True)
                  for x in results)
    report = {'status': 'pass' if success else 'fail',
              'purpose': 'complete exact replay with individual stdout/stderr preservation',
              'python': sys.version, 'results': results}
    (HERE/'artifacts'/'REPLAY_REPORT.json').write_text(
        json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': report['status'], 'runs': len(results),
                      'report': 'artifacts/REPLAY_REPORT.json'}, indent=2))
    if not success:
        raise SystemExit(1)
