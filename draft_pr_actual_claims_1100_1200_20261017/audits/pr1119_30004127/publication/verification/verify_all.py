#!/usr/bin/env python3
"""Reproduce six finite controls without changing the supplied package.

Python 3.10+; standard library only. The analytic proofs, rather than these
finite checks, establish the universal statements. Both execution modes run
explicit checking exceptions, including after optimization disables asserts.
"""
import argparse
import ast
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def normalize(value, fields):
    value = dict(value)
    for field in fields:
        value.pop(field, None)
    return value


def run_control(job):
    spec, optimized = job
    source = HERE / spec['file']
    raw = source.read_bytes()
    if hashlib.sha256(raw).hexdigest() != spec['sha256']:
        raise RuntimeError('Checker fingerprint mismatch: ' + spec['file'])
    if any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(raw))):
        raise RuntimeError('Optimization-sensitive assertion: ' + spec['file'])
    expected = json.loads((HERE / spec['expected']).read_text())
    with tempfile.TemporaryDirectory(prefix='vdf-control-') as temporary:
        copied = Path(temporary) / source.name
        copied.write_bytes(raw)
        command = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(copied)]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(spec['file'] + ': ' + result.stderr[-4000:])
        if spec['result_file']:
            actual = json.loads(copied.with_name(spec['result_file']).read_text())
        else:
            actual = json.loads(result.stdout)
    if normalize(actual, spec['ignored_result_fields']) != expected:
        raise RuntimeError('Mathematical result mismatch: ' + spec['file'])
    return {'checker': spec['file'], 'optimized': optimized,
            'expected_results_equal': True, 'sha256': spec['sha256']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['both', 'ordinary', 'optimized'], default='both')
    args = parser.parse_args()
    specs = json.loads((HERE / 'CONTROL_PLAN.json').read_text())
    modes = [False, True] if args.mode == 'both' else [args.mode == 'optimized']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        rows = list(executor.map(run_control, [(spec, opt) for spec in specs for opt in modes]))
    print(json.dumps({'status': 'PASS', 'controls': len(specs), 'runs': rows,
                      'finite_evidence_only': True}, indent=2))


if __name__ == '__main__':
    main()
