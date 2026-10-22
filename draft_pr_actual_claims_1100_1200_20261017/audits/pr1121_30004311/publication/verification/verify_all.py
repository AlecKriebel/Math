#!/usr/bin/env python3
"""Run four unchanged exact programs in temporary mirrors; Python 3.10+ stdlib.

These finite falsification controls supplement the universal written proofs.
No dependencies or network access are needed. Normal and optimized modes are
both checked by default; all four original programs use explicit failures.
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
ROOT = HERE.parent
AUDIT = ROOT / 'audit' if (ROOT / 'audit').is_dir() else ROOT.parent


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def mathematical(value, finite):
    if not finite:
        return value
    value = json.loads(json.dumps(value))
    for field in ['started_utc', 'completed_utc', 'python_version']:
        value.pop(field, None)
    for stage in value['stages']:
        stage.pop('seconds', None)
    return value


def run_control(job):
    spec, optimized = job
    raw = (AUDIT / spec['file']).read_bytes()
    if digest(raw) != spec['sha256']:
        raise RuntimeError('Checker fingerprint mismatch: ' + spec['file'])
    if any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(raw))):
        raise RuntimeError('Optimization-sensitive assertion: ' + spec['file'])
    proof = (AUDIT / 'inputs/PROOF.md').read_bytes()
    if digest(proof) != '68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75':
        raise RuntimeError('Frozen original proof changed')
    expected_raw = (AUDIT / spec['expected']).read_bytes()
    if digest(expected_raw) != spec['expected_sha256']:
        raise RuntimeError('Expected result fingerprint mismatch')
    expected = json.loads(expected_raw)
    if spec['historical_symbolic_receipt']:
        if expected['code_sha256'] != digest(raw) or any(row['exit_code'] for row in expected['runs']):
            raise RuntimeError('Invalid historical symbolic receipt')
        expected = expected['runs'][int(optimized)]['result']
    with tempfile.TemporaryDirectory(prefix='brace-verification-') as temporary:
        mirror = Path(temporary) / 'audit'
        source = mirror / spec['file']
        source.parent.mkdir(parents=True)
        source.write_bytes(raw)
        (mirror / 'inputs').mkdir()
        (mirror / 'inputs/PROOF.md').write_bytes(proof)
        command = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(source)]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(spec['file'] + ': ' + result.stderr[-4000:])
        actual = json.loads(source.with_name(spec['result_file']).read_text()
                            if spec['result_file'] else result.stdout)
        if mathematical(actual, spec['finite']) != mathematical(expected, spec['finite']):
            raise RuntimeError('Mathematical result mismatch: ' + spec['file'])
        for name, pin in spec['certificates'].items():
            emitted = source.with_name(name).read_bytes()
            if digest(emitted) != pin['sha256'] or len(emitted) != pin['bytes']:
                raise RuntimeError('Seed certificate mismatch: ' + name)
    return {'checker': spec['file'], 'optimized': optimized,
            'sha256': spec['sha256'], 'expected_mathematics_equal': True,
            'seed_certificates_equal': sorted(spec['certificates'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['both', 'ordinary', 'optimized'], default='both')
    args = parser.parse_args()
    specs = json.loads((HERE / 'CONTROL_PLAN.json').read_text())
    modes = [False, True] if args.mode == 'both' else [args.mode == 'optimized']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(run_control, [(spec, mode) for spec in specs for mode in modes]))
    print(json.dumps({'status': 'PASS', 'controls': len(specs), 'runs': results,
                      'finite_evidence_only': True}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
