#!/usr/bin/env python3
"""Fail-closed replay and wrong-expectation tests, including inherited -OO.

No output file is written unless --output is explicitly supplied.
"""
from pathlib import Path
import argparse
import ast
import datetime
import hashlib
import json
import os
import subprocess
import sys


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def main(output=None):
    base = Path(__file__).resolve().parent
    checker = base / 'independent_goeritz.py'
    require(not any(isinstance(x, ast.Assert) for x in ast.walk(ast.parse(checker.read_text()))),
            'Removable Python assertion in mathematical checker')
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
              for p in base.iterdir() if p.is_file()}
    rows = []
    for name, flags, inherited, expected_opt in [
        ('normal', [], None, 0), ('-O', ['-O'], None, 1),
        ('-OO', ['-OO'], None, 2), ('actual inherited PYTHONOPTIMIZE=2', [], '2', 2)]:
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        if inherited:
            env['PYTHONOPTIMIZE'] = inherited
        command = [sys.executable, *flags, str(checker)]
        run = subprocess.run(command, capture_output=True, text=True, env=env)
        require(run.returncode == 0, f'{name} normal replay failed: {run.stderr}')
        data = json.loads(run.stdout)
        require(data['python_optimization'] == expected_opt, 'Optimization mode not actually exercised')
        require(data['inertia'] == [23, 25, 0], 'Replay inertia mismatch')
        require(data['link_signature'] == -2 and data['mirror_signature'] == 2,
                'Replay signature mismatch')
        require(data['bareiss_determinant'] == -7154819319988224, 'Replay determinant mismatch')
        bad = subprocess.run(command + ['--expect-signature', '-1'],
                             capture_output=True, text=True, env=env)
        require(bad.returncode != 0, f'{name} accepted an intentionally wrong expectation')
        require('Wrong numerical expectation' in bad.stderr,
                f'{name} rejected for a reason other than wrong expectation')
        require(not bad.stdout, 'Failed replay emitted a successful result')
        rows.append({'mode': name, 'observed_python_optimization': data['python_optimization'],
                     'normal_exit': run.returncode, 'signature': data['link_signature'],
                     'inertia': data['inertia'], 'determinant': data['bareiss_determinant'],
                     'wrong_signature_expectation': -1, 'wrong_expectation_exit': bad.returncode,
                     'wrong_expectation_rejected_for_correct_reason': True,
                     'stdout_only_default': True})
    after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
             for p in base.iterdir() if p.is_file()}
    require(before == after, 'Default replay mutated a review artifact')
    result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'checker_sha256': hashlib.sha256(checker.read_bytes()).hexdigest(),
              'checker_contains_python_assert': False,
              'all_four_modes_passed': True, 'all_four_modes_rejected_wrong_expectation': True,
              'default_replay_changed_files': False, 'modes': rows}
    body = json.dumps(result, indent=2) + '\n'
    if output:
        Path(output).write_text(body)
    print(body, end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', help='Explicit output file for the replay report')
    main(parser.parse_args().output)
