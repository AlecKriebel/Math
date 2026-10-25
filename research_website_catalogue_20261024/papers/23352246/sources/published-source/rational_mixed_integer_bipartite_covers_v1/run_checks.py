#!/usr/bin/env python3
"""Replay exact small-case arithmetic and actual-source faults, Python 3.10+.

Standard library only. Three unchanged arithmetic checkers in normal/-O/-OO;
five independently validated actual source mutations per mode. Optional
--output saves complete receipts. Finite enumeration is not a polynomial
optimizer, a universal proof or a historical UID1000 permission-harness replay.
"""
import argparse
import hashlib
import json
import pathlib
import platform
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
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


def execute(path, mode, argv, expected, kind, mutation=None):
    command = [sys.executable, '-I', '-S', '-B']
    if mode:
        command.append('-' + 'O' * mode)
    command.extend([str(path), *argv])
    result = subprocess.run(command, cwd=ROOT, capture_output=True,
                            timeout=180, check=False)
    require(result.returncode == expected['exit'], path.name + ': wrong exit')
    require(result.stdout == expected['stdout'].encode(), path.name + ': complete stdout mismatch')
    require(result.stderr == expected['stderr'].encode(), path.name + ': complete stderr mismatch')
    actual = json.loads(result.stdout)
    require(exact_json_equal(actual, json.loads(expected['stdout'])), 'recursive JSON types/values differ')
    if 'python_optimize' in actual:
        require(type(actual['python_optimize']) is int and actual['python_optimize'] == mode,
                'original optimization mode differs')
    if 'optimization_mode' in actual:
        require(type(actual['optimization_mode']) is int and actual['optimization_mode'] == mode,
                'independent optimization mode differs')
    return {'program': path.relative_to(ROOT).as_posix(), 'optimization': mode,
            'args': argv, 'kind': kind, 'mutation': mutation,
            'exit_code': result.returncode, 'stdout': result.stdout.decode(),
            'stderr': result.stderr.decode(), 'complete_reference_match': True,
            'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'stdout_sha256': hashlib.sha256(result.stdout).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=pathlib.Path)
    args = parser.parse_args()
    require(sys.version_info >= (3, 10), 'Python 3.10+ required')
    contract = json.loads((ROOT / 'expected/ORIGINAL_FINITE_CONTRACT.json').read_text())
    reference = json.loads((ROOT / 'expected/independent_exact_check.json').read_text())
    faults = json.loads((ROOT / 'checks/SOURCE_MUTATIONS.json').read_text())
    rows = []
    for mode in (0, 1, 2):
        original = [case for case in contract['modes'][str(mode)]
                    if case['program'] == 'current/exact_checks.py' and case['mutation'] is None]
        require(len(original) == 1, 'original baseline not unique')
        row = original[0]
        rows.append(execute(ROOT / 'checks/exact_checks.py', mode, [],
                            {'exit': row['expected_exit'], 'stdout': row['stdout'],
                             'stderr': row['stderr']}, 'baseline'))
        rows.append(execute(ROOT / 'checks/independent_exact_check.py', mode, [],
                            {'exit': 0, 'stdout': json.dumps(reference, sort_keys=True) + '\n',
                             'stderr': ''}, 'baseline'))
        output = (ROOT / 'expected' / ('independent_ring_value_checks_mode' + str(mode) + '.stdout')).read_text()
        rows.append(execute(ROOT / 'checks/independent_ring_value_checks.py', mode, [],
                            {'exit': 0, 'stdout': output, 'stderr': ''}, 'baseline'))
        for label, fault in faults.items():
            expected = {'exit': 1, 'stderr': '',
                        'stdout': json.dumps({'status': 'INTENDED_REJECTION',
                                              'mutation': label, 'reason': fault['reason']},
                                             sort_keys=True) + '\n'}
            row = execute(ROOT / 'checks/check_mutated_case.py', mode, [label],
                          expected, 'actual_source_mutation', label)
            row['mutated_checker_sha256'] = fault['mutant_sha256']
            rows.append(row)
    require(len(rows) == 24, '24 total executions required')
    result = {'status': 'PASS', 'baseline_runs': 9, 'actual_source_mutation_runs': 15,
              'complete_stdout_stderr_exit_codes_match': True,
              'interpreter': sys.version, 'platform': platform.platform(),
              'historical_uid1000_permission_harness_replayed': False,
              'limits': ['Finite exact enumeration corroborates formulas and boundary cases, not a polynomial implementation or universal theorem.',
                         'All original arithmetic sources are unchanged; faults are applied only in child memory.',
                         'Isolated flags are not a general security sandbox.',
                         'No formal proof-assistant, human peer-review or exhaustive priority certificate.'],
              'runs': rows}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'runs'}, indent=2))


if __name__ == '__main__':
    main()
