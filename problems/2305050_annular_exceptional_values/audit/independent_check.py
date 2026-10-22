#!/usr/bin/env python3
"""Independent exact auxiliary audit; no analytic existence claims."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import subprocess
import sys

F = Fraction
root = Path(__file__).resolve().parent.parent
source = root / 'original'
if not source.is_dir():
    source = root
rerun = subprocess.check_output([sys.executable, str(source / 'verify.py')])
expected_bytes = (source / 'verification.json').read_bytes()
assert rerun == expected_bytes
claimed = json.loads(rerun)

# Counts are derived separately from the test's control flow.
expected_counts = {
    'arc_nonempty': 64,
    'arc_partial_sum': 64,
    'arc_widths': 64,
    'coefficient_sum': sum(n + 2 for n in range(1, 33)),
    'determinants': 20,
    'geometric_tail': 127 * 20,
    'linear_system': sum((n + 1) * (n + 2) for n in range(1, 33)),
    'lower_bound': 127,
    'lower_bound_increasing': 127,
    'single_active_factor': sum((n + 1) * (n + 2) for n in range(1, 33)),
}
assert claimed['assertions_by_category'] == expected_counts
assert sum(expected_counts.values()) == 29774 == claimed['total_assertions']

# Fraction-free Bareiss elimination is independent of the supplied
# determinant routine's rational Gaussian elimination.
def bareiss(a):
    a = [list(row) for row in a]
    sign = 1
    previous = 1
    for k in range(len(a) - 1):
        if a[k][k] == 0:
            p = next(i for i in range(k + 1, len(a)) if a[i][k])
            a[k], a[p] = a[p], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]

for n in range(1, 21):
    matrix = [[int(i != j) for j in range(n + 1)] for i in range(n + 1)]
    assert bareiss(matrix) == n * (-1) ** n

# Solve all right-hand sides simultaneously. The formula under audit is
# used only for comparison after Gaussian-Jordan elimination has solved.
solved_vectors = 0
checked_equations = 0
additional_factor_checks = 0
for n in range(1, 33):
    size = n + 1
    samples = [[F(int(i == j)) for i in range(size)] for j in range(size)]
    samples += [[F((i + 1) ** 2 - 7 * i, i + 2) for i in range(size)]]
    a = [[F(int(i != j)) for j in range(size)] + [v[i] for v in samples]
         for i in range(size)]
    for col in range(size):
        pivot = next(row for row in range(col, size) if a[row][col])
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [v / scale for v in a[col]]
        for row in range(size):
            if row == col:
                continue
            q = a[row][col]
            a[row] = [x - q * y for x, y in zip(a[row], a[col])]
    for v_index, v in enumerate(samples):
        alpha = [a[row][size + v_index] for row in range(size)]
        S = sum(v, F(0)) / n
        assert alpha == [S - x for x in v]
        assert sum(alpha, F(0)) == S
        solved_vectors += 1
        for j in range(size):
            assert sum(alpha[i] for i in range(size) if i != j) == v[j]
            checked_equations += 1
            for w, t in [(F(0), F(0)), (F(2, 3), F(1)),
                         (F(-17, 11), F(23, 13))]:
                factors = [t if i == j else F(1) for i in range(size)]
                prod = F(1)
                for factor in factors:
                    prod *= factor
                lhs = (w - sum(alpha, F(0))) * prod
                lhs += sum(alpha[i] * factors[i] for i in range(size))
                assert lhs == (w - v[j]) * t + v[j]
                additional_factor_checks += 1

for k in range(2, 129):
    for length in range(1, 21):
        # Algebraically independent closed form of the finite geometric sum.
        finite = F(2 ** length - 1, 2 ** (k + length))
        assert finite + F(1, 2 ** (k + length)) == F(1, 2 ** k)
    assert 2 ** k - F(1, 2 ** k) > 2 ** (k - 1)
    assert 2 ** (k + 1) - F(1, 2 ** (k + 1)) > 2 ** k - F(1, 2 ** k)
for j in range(64):
    left, right = 1 - F(1, 2 ** j), 1 - F(1, 2 ** (j + 1))
    assert 0 <= left < right < 1
    assert right - left == F(1, 2 ** (j + 1))
for n in range(1, 65):
    assert sum(F(1, 2 ** j) for j in range(1, n + 1)) == 1 - F(1, 2 ** n)

result = {
    'problem_id': 2305050,
    'passed': True,
    'original_output_byte_identical': True,
    'original_output_sha256': hashlib.sha256(rerun).hexdigest(),
    'independently_derived_original_counts': expected_counts,
    'original_total_assertions': sum(expected_counts.values()),
    'independent_determinants_bareiss': 20,
    'independently_solved_rhs_vectors': solved_vectors,
    'independent_linear_equations': checked_equations,
    'additional_single_factor_checks': additional_factor_checks,
    'scope': 'Exact finite auxiliary checks only; mathematical identities also proved in the audit report. No analytic existence proof by computation.'
}
assert solved_vectors == 592
assert checked_equations == 13088
assert additional_factor_checks == 39264
print(json.dumps(result, indent=2, sort_keys=True))
