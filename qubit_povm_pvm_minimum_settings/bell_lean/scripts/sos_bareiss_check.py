#!/usr/bin/env python3
"""Independent fraction-free positivity check of the integer SOS Gram matrix.

This script does not read or trust the supplied LDL factors.  It recomputes each
leading principal determinant with integer Bareiss elimination and compares its
successive determinant ratios against those LDL pivots.  Positivity together
with real symmetry is the ordinary Sylvester criterion.  The noncommutative
identity is checked separately by sos_checks.py.  This is not Lean verification.
"""
from __future__ import annotations
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def determinant(a: list[list[int]]) -> int:
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError('not a square matrix')
    if n == 0:
        return 1
    b = [row[:] for row in a]
    previous, sign = 1, 1
    for k in range(n - 1):
        if b[k][k] == 0:
            replacement = next((i for i in range(k + 1, n) if b[i][k] != 0), None)
            if replacement is None:
                return 0
            b[k], b[replacement] = b[replacement], b[k]
            sign = -sign
        pivot = b[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = pivot * b[i][j] - b[i][k] * b[k][j]
                value, remainder = divmod(numerator, previous)
                if remainder:
                    raise ArithmeticError('Bareiss division was not exact')
                b[i][j] = value
        for i in range(k + 1, n):
            b[i][k] = 0
        previous = pivot
    return sign * b[-1][-1]


def main() -> None:
    raw = (ROOT / 'certificates/binary_pair_sos.json').read_bytes()
    data = json.loads(raw)
    r = data['gram_integer_numerator']
    if len(r) != 12 or any(len(row) != 12 for row in r):
        raise ValueError('expected a 12-by-12 certificate')
    if not all(type(x) is int for row in r for x in row):
        raise TypeError('the numerator must be genuinely integral')
    if not all(r[i][j] == r[j][i] for i in range(12) for j in range(12)):
        raise ValueError('Gram numerator is not symmetric')
    minors = [determinant([row[:k] for row in r[:k]]) for k in range(1, 13)]
    if not all(m > 0 for m in minors):
        raise ValueError('not all leading principal minors are positive')
    denominator = Fraction(data['gram_common_denominator'])
    if denominator <= 0:
        raise ValueError('denominator is not positive')
    previous = 1
    for i, minor in enumerate(minors):
        pivot = Fraction(minor, previous) / denominator
        if pivot != Fraction(data['ldl_positive_diagonal'][i]):
            raise ValueError(f'independent pivot comparison failed at {i}')
        previous = minor
    # Small algorithm regressions include singular and pivot-swap cases.
    tests = [([], 1), ([[0, 1], [1, 0]], -1), ([[1, 2], [2, 4]], 0),
             ([[1, 2, 3], [4, 5, 6], [7, 8, 10]], -3)]
    for matrix, expected in tests:
        if determinant(matrix) != expected:
            raise AssertionError('Bareiss regression failed')
    report = {
        'status': 'passed',
        'lean_kernel_checked': False,
        'arithmetic': 'fraction-free integer Bareiss elimination',
        'ldl_factors_used_to_compute_determinants': False,
        'positive_leading_principal_minors': minors,
        'independent_ldl_pivot_comparisons': 12,
        'small_algorithm_regressions': len(tests),
        'certificate_sha256': hashlib.sha256(raw).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'Gram positivity only; sos_checks.py checks the separate word identity.'
    }
    (ROOT / 'reports/sos_bareiss_check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
