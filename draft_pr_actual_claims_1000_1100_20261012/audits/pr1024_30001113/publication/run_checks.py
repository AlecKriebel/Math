#!/usr/bin/env python3
"""Run 39 exact baseline/control cases with Python 3.10+ standard library.

Default output is stdout only. --output saves every execution's complete receipt.
Uses isolated children in normal, -O, -OO modes; this is not a security sandbox,
a universal proof, or replay of the historical UID1000 permission harness.
"""
import argparse
import hashlib
import json
import pathlib
import platform
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def exact_json_equal(actual, expected):
    if type(actual) is not type(expected):
        return False
    if isinstance(actual, dict):
        return (actual.keys() == expected.keys() and
                all(exact_json_equal(actual[k], expected[k]) for k in actual))
    if isinstance(actual, list):
        return (len(actual) == len(expected) and
                all(exact_json_equal(a, b) for a, b in zip(actual, expected)))
    return actual == expected


def execute(path, args, mode, expected, kind, mutation):
    command = [sys.executable, '-I', '-S', '-B']
    if mode:
        command.append('-' + 'O' * mode)
    command.extend([str(path), *args])
    result = subprocess.run(command, cwd=ROOT, capture_output=True,
                            timeout=180, check=False)
    require(result.returncode == expected['expected_exit'],
            str(path.name) + ': unexpected exit for ' + mutation)
    require(result.stdout == expected['stdout'].encode('utf-8'),
            str(path.name) + ': complete stdout mismatch for ' + mutation)
    require(result.stderr == expected['stderr'].encode('utf-8'),
            str(path.name) + ': complete stderr mismatch for ' + mutation)
    require(exact_json_equal(json.loads(result.stdout), json.loads(expected['stdout'])),
            'recursive JSON types/values mismatch')
    return {
        'program': path.relative_to(ROOT).as_posix(), 'args': args,
        'optimization_mode': mode, 'kind': kind, 'mutation': mutation,
        'exit_code': result.returncode,
        'stdout': result.stdout.decode('utf-8'), 'stderr': result.stderr.decode('utf-8'),
        'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
        'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'exact_reference_match': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=pathlib.Path)
    args = parser.parse_args()
    require(sys.version_info >= (3, 10), 'Python 3.10+ required')
    contract = json.loads((ROOT / 'expected/FINITE_CONTRACT.json').read_text())
    independent = json.loads((ROOT / 'expected/verify_functor_identities.json').read_text())
    controls = json.loads((ROOT / 'expected/INDEPENDENT_CONTROLS.json').read_text())
    rows = []
    for mode in (0, 1, 2):
        for case in contract['modes'][str(mode)]:
            mutant = case['mutation'] or 'none'
            if case['program'] == 'check_conjugacy.py':
                path = ROOT / 'checks/check_corrected_case.py'
                argv = [mutant]
                kind = 'baseline' if mutant == 'none' else 'actual_source_mutation'
            elif case['program'] == 'verify_exact.py':
                path = ROOT / 'checks/current/verify_exact.py'
                argv = ['--mutant', mutant]
                kind = 'baseline' if mutant == 'none' else 'runtime_fault_control'
            else:
                raise RuntimeError('unexpected contract program')
            rows.append(execute(path, argv, mode, case, kind, mutant))
        baseline = {'expected_exit': 0, 'stderr': '',
                    'stdout': json.dumps(independent, indent=2, sort_keys=True) + '\n'}
        path = ROOT / 'checks/check_independent_case.py'
        rows.append(execute(path, ['none'], mode, baseline, 'baseline', 'none'))
        for label, reason in controls.items():
            expected = {'expected_exit': 1, 'stderr': '',
                        'stdout': json.dumps({'ok': False, 'mutant': label,
                                              'failure': reason}, sort_keys=True) + '\n'}
            rows.append(execute(path, [label], mode, expected, 'actual_source_mutation', label))
    counts = {kind: sum(row['kind'] == kind for row in rows)
              for kind in ('baseline', 'actual_source_mutation', 'runtime_fault_control')}
    require(counts == {'baseline': 9, 'actual_source_mutation': 12,
                       'runtime_fault_control': 18}, 'execution count differs')
    result = {
        'status': 'PASS', 'total_runs': len(rows), 'counts': counts,
        'complete_stdout_stderr_and_exit_codes_match': True,
        'interpreter': sys.version, 'platform': platform.platform(),
        'historical_uid1000_permission_harness_replayed': False,
        'limits': [
            'Finite exact arithmetic; infinite formal-series and arbitrary-natural-map conclusions are written proofs.',
            'Original source assertion predicates are unchanged in the explicit guard adaptation.',
            'Normal/-O/-OO are tested; neither isolated flags nor controls provide a general security sandbox.',
            'No formal proof-assistant, human peer-review, source-intent or exhaustive-priority certificate.'],
        'runs': rows}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'runs'}, indent=2))


if __name__ == '__main__':
    main()
