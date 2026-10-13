#!/usr/bin/env python3
"""Replay the included exact finite checks and actual source mutations.

Uses Python's standard library, isolated child interpreters, and a temporary
directory for mutants. Default output is stdout only. --output saves the full
execution receipt there. This is formula testing, not a universal proof,
security sandbox, source-intent decision, or novelty certificate.
"""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def mathematical_payload(value):
    # These two expressly identified fields describe execution, not mathematics.
    return {k: v for k, v in value.items() if k not in ('uid', 'optimization')}


def execute(path, mode):
    command = [sys.executable, '-I', '-S', '-B']
    if mode:
        command.append('-' + 'O' * mode)
    command.append(str(path))
    result = subprocess.run(command, cwd=path.parent, capture_output=True,
                            timeout=180, check=False)
    return {
        'program': path.name, 'optimization_mode': mode,
        'exit_code': result.returncode,
        'source_sha256': digest(path.read_bytes()),
        'stdout_sha256': digest(result.stdout),
        'stdout': result.stdout.decode('utf-8'),
        'stderr': result.stderr.decode('utf-8'),
    }


def replace_once(source, before, after):
    require(source.count(before) == 1, 'mutation anchor is not unique')
    return source.replace(before, after, 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=pathlib.Path,
                        help='optional full receipt JSON file')
    args = parser.parse_args()
    names = ('check_collision_witness', 'independent_kernel_check',
             'independent_exact_check')
    receipts = []
    for mode in (0, 1, 2):
        for name in names:
            expected = json.loads((ROOT / 'expected' / (name + '.json')).read_text())
            row = execute(ROOT / 'checks' / (name + '.py'), mode)
            require(row['exit_code'] == 0, name + ' did not exit successfully')
            require(row['stderr'] == '', name + ' wrote unexpected stderr')
            actual = json.loads(row['stdout'])
            require(actual.get('status', actual.get('verdict')) == 'PASS',
                    name + ' did not report PASS')
            require(mathematical_payload(actual) == mathematical_payload(expected),
                    name + ' mathematical output differs from the pinned reference')
            if 'optimization' in actual:
                require(actual['optimization'] == mode, 'optimization identity differs')
            row['actual_execution_identity'] = {
                k: actual[k] for k in ('uid', 'optimization') if k in actual}
            row['mathematical_reference_match'] = True
            row['kind'] = 'baseline'
            receipts.append(row)

    source = (ROOT / 'checks' / 'independent_kernel_check.py').read_text()
    ratio = ('return tuple((p[v][0]-p[u][0])/(q[v][0]-q[u][0]) '
             'for u,v in edges)')
    mutations = (
        ('reverse_ratio', ratio,
         'return tuple((q[v][0]-q[u][0])/(p[v][0]-p[u][0]) for u,v in edges)',
         'transported vector not equilibrium'),
        ('omit_ratio', ratio, 'return tuple(Q(1) for _ in edges)',
         'transported vector not equilibrium'),
        ('negative_ratio', ratio,
         'return tuple(-(p[v][0]-p[u][0])/(q[v][0]-q[u][0]) for u,v in edges)',
         'sign-preserving invertibility'),
        ('erase_zero_sign', 'return (x > 0) - (x < 0)',
         'return 1 if x == 0 else (x > 0) - (x < 0)',
         'accepted semantic mutant: allow zero-to-positive coordinate'),
        ('zero_singleton_witness', 'unit=tuple(Q(k==j) for k in range(len(edges)))',
         'unit=tuple(Q(0) for k in range(len(edges)))',
         'separated singleton retained'),
        ('same_force_both_endpoints', 'p[u][r]-p[i][r] if i==v',
         'p[i][r]-p[u][r] if i==v', 'cycle-space nullity'),
    )
    with tempfile.TemporaryDirectory(prefix='stress-partition-checks-') as temporary:
        for label, before, after, reason in mutations:
            path = pathlib.Path(temporary) / (label + '.py')
            path.write_text(replace_once(source, before, after))
            for mode in (0, 1, 2):
                row = execute(path, mode)
                require(row['exit_code'] == 1, label + ' did not reject the actual mutant')
                require(row['stderr'] == '', label + ' failed by an unexpected exception')
                require(json.loads(row['stdout']) == {'status': 'FAIL', 'reason': reason},
                        label + ' did not fail for the intended reason')
                row.update(kind='actual_source_mutation', mutation=label,
                           intended_rejection=True)
                receipts.append(row)

    result = {
        'status': 'PASS', 'baseline_runs': 9, 'actual_source_mutation_runs': 18,
        'all_mathematical_references_match': True,
        'all_mutations_rejected_for_intended_reasons': True,
        'interpreter': sys.version,
        'historical_uid1000_permission_harness_replayed': False,
        'limits': [
            'Finite exact-rational diagnostics; the written proof supplies all-n,d and connectedness claims.',
            'Execution UID and optimization are separately checked/reported; all mathematical JSON fields must match.',
            'Isolated Python flags are not a general security sandbox.',
            'No source-intent, first-priority, formal proof-assistant, or human-peer-review certificate.',
        ],
        'runs': receipts,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'runs'}, indent=2))


if __name__ == '__main__':
    main()
