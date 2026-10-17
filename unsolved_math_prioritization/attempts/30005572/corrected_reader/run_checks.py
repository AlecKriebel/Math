#!/usr/bin/env python3
"""Replay the included finite checks in isolated temporary directories.

No network, source PDFs, datasets, or original preparation workspace is needed.
Use --optimized to add -O and -OO where assertions are not the validator.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile

def digest(b):
    return hashlib.sha256(b).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--optimized', action='store_true')
    parser.add_argument('--only', nargs='*', help='Check IDs, for example C15 C16')
    parser.add_argument('--output', type=Path, help='Optional JSON result path')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    spec = json.loads((root / 'CHECK_INVENTORY.json').read_text())
    rows = []
    for check in spec['checks']:
        if args.only and check['id'] not in args.only:
            continue
        script = root / check['script']
        expected_path = root / check['expected']
        source = script.read_bytes()
        expected_bytes = expected_path.read_bytes()
        if digest(source) != check['script_sha256']:
            raise RuntimeError('Script pin mismatch: ' + check['id'])
        if digest(expected_bytes) != check['expected_sha256']:
            raise RuntimeError('Expected-output pin mismatch: ' + check['id'])
        expected = json.loads(expected_bytes)
        modes = check['modes'] if args.optimized else ['normal']
        for mode in modes:
            with tempfile.TemporaryDirectory(prefix='eisenstein_check_') as work:
                temp = Path(work)
                copied = temp / script.name
                shutil.copyfile(script, copied)
                command = [sys.executable]
                if mode != 'normal':
                    command.append(mode)
                command.append(str(copied))
                env = dict(os.environ)
                env.pop('PYTHONOPTIMIZE', None)
                env['PYTHONDONTWRITEBYTECODE'] = '1'
                result = subprocess.run(command, cwd=temp, env=env,
                                        capture_output=True, text=True)
                if result.returncode:
                    raise RuntimeError(check['id'] + ' ' + mode + ' failed:\n'
                                       + result.stdout + result.stderr)
                generated = temp / check['source_result_name']
                if generated.exists():
                    actual_bytes = generated.read_bytes()
                    channel = 'generated_result'
                else:
                    actual_bytes = result.stdout.encode()
                    channel = 'stdout'
                try:
                    actual = json.loads(actual_bytes)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(check['id'] + ' did not emit valid result JSON') from exc
                if actual != expected:
                    raise RuntimeError(check['id'] + ' ' + mode + ' result differs from the frozen JSON')
                row = {'id':check['id'], 'mode':mode, 'status':'PASS',
                       'comparison_channel':channel,
                       'json_values_match':True,
                       'bytes_match':actual_bytes == expected_bytes,
                       'result_sha256':digest(actual_bytes)}
                rows.append(row)
                print(check['id'] + ' ' + mode + ': PASS', file=sys.stderr, flush=True)
    if args.only:
        found = {row['id'] for row in rows}
        missing = set(args.only) - found
        if missing:
            raise RuntimeError('Unknown requested check IDs: ' + ', '.join(sorted(missing)))
    try:
        sympy_version = importlib.metadata.version('sympy')
    except importlib.metadata.PackageNotFoundError:
        sympy_version = None
    report = {'status':'PASS', 'python_version':platform.python_version(),
              'sympy_version':sympy_version, 'check_count':len({r['id'] for r in rows}),
              'execution_count':len(rows), 'results':rows,
              'limits':'These are finite algebra/example checks, not a proof of missing K2 values, q-adic continuity, or full homology calibration.'}
    content = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.write_text(content)
    print(content, end='')

if __name__ == '__main__':
    main()
