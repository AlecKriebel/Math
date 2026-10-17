#!/usr/bin/env python3
"""Replay the accepted reader certificates, with optimization-safe gates.

Place beside the 15 unchanged certificate files. Run with Python 3 and mpmath
(tested with 1.3.0), optionally with -O or -OO. All work takes place in a fresh
scratch directory; the accepted source and expected-result files stay unchanged.

This is a reproducibility checker, not an additional mathematical argument.
Original source assertions are translated in memory to explicit conditional
exceptions before execution. The source file itself is never rewritten.
Output acceptance uses explicit exact-integer/rational predicates plus equality
to the pinned result payload after removing only measured elapsed-time fields.
"""
import argparse
import ast
import copy
from fractions import Fraction as Q
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

# Filled from the accepted, byte-preserved certificate dependency inventory.
PINS = {
    "certify_entropy_quadrature.py": {
        "sha256": "eea7a43aef50424f9677353378023284149a8c07822a131c92a5e30b8f346e51",
        "bytes": 4047
    },
    "certify_four_circuit.json": {
        "sha256": "b4ea82eacef330d10bec5f4928ddb716ef9194a3cc68bbb36c4eb393d41184a1",
        "bytes": 21947
    },
    "certify_four_circuit.py": {
        "sha256": "99a76918db068aa9b1516a933dad4ebf146d906f4b910940924c55b928684d4d",
        "bytes": 4009
    },
    "certify_green_quadrature.py": {
        "sha256": "eaba430472a6abda676e3168599e38584021cbdca4d85d25244b65f8c1d0f77a",
        "bytes": 2913
    },
    "certify_rational_boxes.py": {
        "sha256": "c6d7a09477867b3cb8d828a52f349b632d6a0e6c35695ee20ed97106b38a79c0",
        "bytes": 1075
    },
    "certify_uniform_027.json": {
        "sha256": "7ab3e56d1f1bb360490b090b51fef76249e4c62c8324984330c3f553e7982e9f",
        "bytes": 668
    },
    "certify_uniform_027.py": {
        "sha256": "afb4c9348c5714d947268d12bc4a04e2da222f9eb28b70abdcab235af7ad6e28",
        "bytes": 3079
    },
    "certify_uniform_odd_family.py": {
        "sha256": "9f70c20634f3185e47b371d47c2a414e36fc04b9c8049c12f3ffd8924609d7fd",
        "bytes": 2926
    },
    "check_middle_exact.json": {
        "sha256": "44a8128947451498e1924b53cb12a9b24cdbaa76196149f77c9f653db8dd5e30",
        "bytes": 249610
    },
    "check_middle_exact.py": {
        "sha256": "10fb2e98a75991799bf4d1f7ffeb30d904ed36d7bc142470307e9e5389182c18",
        "bytes": 1201
    },
    "green_rational_certificate.json": {
        "sha256": "427cdead91d2142539f053005ba4da5cf30abeec356baa2b4f3f8542a0fad834",
        "bytes": 3112
    },
    "quadrature_certificates.json": {
        "sha256": "d1971feff541988fc76a6cf0bf8ff1f6d2fe6c30490008cf3cc15a94fbb0286f",
        "bytes": 5257
    },
    "rational_box_certificates.json": {
        "sha256": "b5401cb9bca39fdc6b581767f86ef8063276563c047a50bfd6190418d484a6ee",
        "bytes": 10941
    },
    "uniform_0211.json": {
        "sha256": "62d5f71b749e0ef97f8079c29dcc37213113ed4ca2b3ec7ffe9ffe97d6dd5e0b",
        "bytes": 749
    },
    "uniform_029.json": {
        "sha256": "f7d2819e934ff4d4e1da509b6fa8ffc5d7367b7b55bf34c8c3af9a7b76e61d70",
        "bytes": 745
    }
}
JOBS = [
    ('certify_uniform_027.py', [], 'certify_uniform_027.json'),
    ('certify_uniform_odd_family.py', ['--K', '9', '--N', '512', '--bins', '1024'], 'uniform_029.json'),
    ('certify_uniform_odd_family.py', ['--K', '11', '--N', '1024', '--bins', '2048'], 'uniform_0211.json'),
    ('certify_four_circuit.py', [], 'certify_four_circuit.json'),
    ('check_middle_exact.py', [], 'check_middle_exact.json'),
    ('certify_entropy_quadrature.py', ['--N', '256'], 'quadrature_certificates.json'),
    ('certify_green_quadrature.py', ['--N', '128'], 'green_rational_certificate.json'),
    ('certify_rational_boxes.py', [], 'rational_box_certificates.json'),
]


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_pins(directory):
    for name, expected in PINS.items():
        path = directory / name
        require(path.is_file(), 'Missing pinned dependency: ' + name)
        require(path.stat().st_size == expected['bytes'], 'Byte-count mismatch: ' + name)
        require(digest(path) == expected['sha256'], 'SHA-256 mismatch: ' + name)


class ExplicitSourceGates(ast.NodeTransformer):
    """Preserve each accepted assert predicate under every Python optimize flag."""
    def visit_Assert(self, node):
        message = node.msg or ast.Constant('Accepted source gate failed at line ' + str(node.lineno))
        failure = ast.Raise(exc=ast.Call(func=ast.Name(id='ArithmeticError', ctx=ast.Load()),
                                       args=[message], keywords=[]), cause=None)
        replacement = ast.If(test=ast.UnaryOp(op=ast.Not(), operand=node.test),
                             body=[failure], orelse=[])
        return ast.copy_location(replacement, node)


def guarded_code(source, filename):
    tree = ExplicitSourceGates().visit(ast.parse(source, filename=filename))
    ast.fix_missing_locations(tree)
    require(not any(isinstance(n, ast.Assert) for n in ast.walk(tree)),
            'A source assertion was not converted to an explicit gate')
    return compile(tree, filename, 'exec', optimize=sys.flags.optimize)


def without_times(value):
    if isinstance(value, dict):
        return {k: without_times(v) for k, v in value.items()
                if k not in ('seconds', 'elapsed_seconds')}
    if isinstance(value, list):
        return [without_times(v) for v in value]
    return value


def check_interval_record(record, key):
    gap = record[key]
    require(Q(gap['lower']) > 0, 'Nonpositive lower endpoint for ' + key)
    require(Q(gap['lower']) <= Q(gap['upper']), 'Reversed interval for ' + key)
    require(record['positive_certified'] is True and record['negative_certified'] is False,
            'Interval sign verdict mismatch')


def check_result(name, value):
    if name in ('certify_uniform_027.json', 'uniform_029.json', 'uniform_0211.json'):
        require(value['status'] == 'PASS', 'Uniform verdict failed')
        require(int(value['minimum_normalized_lower_numerator']) > 0, 'Uniform lower bound failed')
        require(int(value['lower_denominator']) > 0, 'Uniform denominator failed')
    elif name == 'certify_four_circuit.json':
        require(int(value['raw_first_difference']) == 184968806400, 'First raw moment difference failed')
        fixed = value['fixed_p5']
        require(Q(fixed['tail']) >= 0, 'Negative tail')
        require(Q(fixed['partial']) + Q(fixed['tail']) == Q(fixed['upper_bound']), 'Fixed bound sum failed')
        require(Q(fixed['upper_bound']) < -Q(1, 4), 'Fixed p=5 strict bound failed')
        uniform = value['uniform_4_lt_p_lt_6']
        numerators = list(map(int, uniform['all_lower_numerators']))
        require(len(numerators) == uniform['bins'] == 256, 'Uniform cell count failed')
        minimum = min(numerators)
        scale = int(uniform['scale'])
        require(scale > 0 and minimum > 0, 'Four-circuit positivity failed')
        require(minimum == int(uniform['minimum_lower_numerator']), 'Minimum mismatch')
        require(minimum * 40000000 > scale, 'Four-circuit rational lower bound failed')
        require(numerators.index(minimum) == uniform['worst_cell'], 'Worst-cell mismatch')
        require(value['source_sha256'] == PINS['certify_four_circuit.py']['sha256'], 'Recorded source pin failed')
    elif name == 'check_middle_exact.json':
        require(value['verdict'] == 'PASS', 'Middle verdict failed')
        require([r['N'] for r in value['records']] == list(range(3, 100)), 'Middle index range failed')
        total = Q(0)
        for record in value['records']:
            ratios = list(map(Q, record['ratios_by_R']))
            require(len(ratios) == record['N'] + 1, 'Middle ratio count failed')
            maximum = max(ratios)
            require(maximum == Q(record['maximum']), 'Middle maximum failed')
            require(ratios.index(maximum) == record['maximizing_R'], 'Middle maximizing index failed')
            total += maximum
        require(total == Q(value['small_sum']) < Q(7, 125), 'Middle finite rational sum failed')
        negative = Q(3, 2) * (Q(7, 125) + Q(236, 99**2)) + Q(1, 8)
        require(Q(value['negative_upper_bound']) == negative == Q(800803, 3267000) < Q(1, 4),
                'Middle negative upper bound failed')
        require(Q(value['gap_below_one_quarter']) == Q(1, 4) - negative > 0, 'Middle gap failed')
        require(value['coefficient_cases'] == 5044 and value['resonance_cases'] == 58740, 'Middle case count failed')
    elif name == 'quadrature_certificates.json':
        require(len(value) == 3, 'Entropy record count failed')
        for record in value:
            check_interval_record(record, 'normalized_entropy_gap')
            check_interval_record(record, 'unnormalized_entropy_gap')
    elif name == 'green_rational_certificate.json':
        require(0 < Q(value['case']['rho_over_support']) < 1, 'Green radius failed')
        require(value['N_each_angle'] == 128 and value['N_each_angle'] % 2 == 0, 'Green angle grid failed')
        check_interval_record(value, 'normalized_green_gap')
        check_interval_record(value, 'unnormalized_green_gap')
    elif name == 'rational_box_certificates.json':
        require(len(value) == 2, 'Box count failed')
        for box in value:
            require([r['signs'] for r in box['sign_certificates']] == [[-1, 1], [1, -1], [-1, -1]],
                    'Box sign coverage failed')
            for record in box['sign_certificates']:
                check_interval_record(record, 'normalized_entropy_gap')
            lower = min(Q(r['normalized_entropy_gap']['lower']) for r in box['sign_certificates'])
            require(Q(box['minimum_certified_delta']) == lower > 0, 'Box lower bound failed')
            require(Q(box['rational_power_upper_endpoint']) == 2 + 7 * lower > 2, 'Box power interval failed')
    else:
        raise ArithmeticError('Unrecognized result: ' + name)


def compare_result(name, actual, expected):
    check_result(name, actual)
    require(without_times(actual) == without_times(expected),
            'Result differs from pinned payload (only elapsed-time fields are ignored): ' + name)


def must_reject(label, function):
    try:
        function()
    except ArithmeticError:
        return label
    raise ArithmeticError('Negative control was accepted: ' + label)


def self_test(directory):
    tests = []
    tests.append(must_reject('source assert False remains a failing explicit gate',
                            lambda: exec(guarded_code('assert False, "negative control"', '<self-test>'), {})))
    mutations = {
        'certify_uniform_027.json': lambda x: x.update(minimum_normalized_lower_numerator=0),
        'uniform_029.json': lambda x: x.update(status='FAIL'),
        'uniform_0211.json': lambda x: x.update(lower_denominator='0'),
        'certify_four_circuit.json': lambda x: x['uniform_4_lt_p_lt_6']['all_lower_numerators'].__setitem__(0, '0'),
        'check_middle_exact.json': lambda x: x.update(small_sum='7/125'),
        'quadrature_certificates.json': lambda x: x[0]['normalized_entropy_gap'].update(lower='0'),
        'green_rational_certificate.json': lambda x: x['case'].update(rho_over_support='1'),
        'rational_box_certificates.json': lambda x: x[0].update(rational_power_upper_endpoint='2'),
    }
    for name, mutate in mutations.items():
        bad = json.loads((directory / name).read_text())
        mutate(bad)
        tests.append(must_reject(name + ' bad exact gate', lambda: check_result(name, bad)))
    name = 'certify_uniform_027.json'
    expected = json.loads((directory / name).read_text())
    bad = copy.deepcopy(expected)
    bad['precision_bits'] += 1
    tests.append(must_reject('otherwise-positive payload mismatch', lambda: compare_result(name, bad, expected)))
    return tests


def worker(arguments):
    path = Path(arguments[0]).resolve()
    require(path.name in PINS and path.suffix == '.py', 'Unrecognized source worker')
    require(digest(path) == PINS[path.name]['sha256'], 'Worker source pin failed')
    sys.path.insert(0, str(path.parent))
    sys.argv = [str(path)] + arguments[1:]
    namespace = {'__name__': '__main__', '__file__': str(path), '__package__': None}
    exec(guarded_code(path.read_text(), str(path)), namespace)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--worker':
        worker(sys.argv[2:])
        return
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true', help='Check pins and negative controls without replaying')
    parser.add_argument('--output-dir', type=Path, help='New empty directory for scratch scripts, results, and logs')
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    check_pins(directory)
    controls = self_test(directory)
    if args.self_test:
        print(json.dumps({'status': 'PASS', 'optimization': sys.flags.optimize, 'negative_controls_rejected': controls}, indent=2))
        return
    if args.output_dir:
        work = args.output_dir.resolve()
        require(not work.exists(), 'Output directory must not exist: ' + str(work))
        work.mkdir(parents=True)
    else:
        work = Path(tempfile.mkdtemp(prefix='majorant-reader-certificates-'))
    for name in PINS:
        shutil.copyfile(directory / name, work / name)
    mode = [] if sys.flags.optimize == 0 else ['-O' if sys.flags.optimize == 1 else '-OO']
    records = []
    for script, arguments, output in JOBS:
        (work / output).unlink()  # A stale expected output must never count as a replay.
        command = [sys.executable] + mode + [str(Path(__file__).resolve()), '--worker', str(work / script)] + arguments
        result = subprocess.run(command, cwd=work, text=True, capture_output=True)
        (work / (output + '.stdout')).write_text(result.stdout)
        (work / (output + '.stderr')).write_text(result.stderr)
        require(result.returncode == 0, 'Source execution failed: ' + script + '\n' + result.stderr)
        if script == 'check_middle_exact.py':
            (work / output).write_text(result.stdout)
        require((work / output).is_file(), 'Source produced no output: ' + script)
        actual = json.loads((work / output).read_text())
        expected = json.loads((directory / output).read_text())
        compare_result(output, actual, expected)
        record = {'output': output, 'status': 'PASS', 'exact_predicates': 'PASS',
                  'pinned_payload_except_elapsed_time': 'IDENTICAL', 'sha256': digest(work / output),
                  'bytes': (work / output).stat().st_size, 'command': command}
        records.append(record)
        print('PASS ' + output, flush=True)
    check_pins(directory)
    report = {'status': 'PASS', 'python': sys.version, 'optimization': sys.flags.optimize,
              'mpmath_version': importlib.metadata.version('mpmath'), 'negative_controls_rejected': controls,
              'original_dependency_files_preserved': True, 'records': records,
              'scope': 'Reproducibility only; no new mathematical argument, pass, or classification claim.'}
    (work / 'REPLAY_REPORT.json').write_text(json.dumps(report, indent=2) + '\n')
    print('All eight certificate jobs passed. Report: ' + str(work / 'REPLAY_REPORT.json'))


if __name__ == '__main__':
    main()
