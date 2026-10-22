#!/usr/bin/env python3
"""Exact finite sanity checks. No numerical approximation or analytic existence proof."""
from fractions import Fraction as F
from collections import defaultdict
import json

counts = defaultdict(int)

def check(category, condition):
    if not condition:
        raise AssertionError(category)
    counts[category] += 1

def determinant(a):
    a = [[F(x) for x in row] for row in a]
    d = F(1)
    for k in range(len(a)):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            d = -d
        p = a[k][k]
        d *= p
        for i in range(k+1, len(a)):
            q = a[i][k] / p
            for j in range(k, len(a)):
                a[i][j] -= q * a[k][j]
    return d

# The (n+1)-dimensional off-diagonal-one matrix has eigenvalues
# n on the constant vector and -1 on the sum-zero subspace.
# Thus det = n*(-1)**n and alpha_j = sum(a_i)/n - a_j.
for n in range(1, 21):
    matrix = [[int(i != j) for j in range(n+1)] for i in range(n+1)]
    check('determinants', determinant(matrix) == (-1)**n * n)

for n in range(1, 33):
    vectors = [[F(int(i == j)) for i in range(n+1)] for j in range(n+1)]
    vectors += [[F((i+1)**2 - 7*i, i+2) for i in range(n+1)]]
    for a in vectors:
        A = sum(a, F(0)) / n
        alpha = [A - x for x in a]
        check('coefficient_sum', sum(alpha, F(0)) == A)
        for j in range(n+1):
            check('linear_system', sum((alpha[i] for i in range(n+1) if i != j), F(0)) == a[j])
            # If only the j-th exponential differs from 1, Carroll's
            # combination reduces algebraically to (w-a_j)*t+a_j.
            w, t = F(13, 7), F(-11, 5)
            lhs = (w - sum(alpha, F(0))) * t
            lhs += sum((alpha[i] * (t if i == j else 1) for i in range(n+1)), F(0))
            check('single_active_factor', lhs == (w-a[j])*t+a[j])

for k in range(2, 129):
    for length in range(1, 21):
        finite_tail = sum((F(1, 2**m) for m in range(k+1, k+length+1)), F(0))
        remaining_tail = F(1, 2**(k+length))
        check('geometric_tail', finite_tail + remaining_tail == F(1, 2**k))
    lower = F(2**k) - F(1, 2**k)
    check('lower_bound', lower > 2**(k-1))
    check('lower_bound_increasing', F(2**(k+1))-F(1, 2**(k+1)) > lower)

# Boundary cap endpoints in turns: theta_j = 1-2**(-j).
angles = [1-F(1, 2**j) for j in range(65)]
for j in range(64):
    check('arc_widths', angles[j+1] - angles[j] == F(1, 2**(j+1)))
    check('arc_nonempty', angles[j] < angles[j+1] < 1)
for n in range(1, 65):
    check('arc_partial_sum', sum((F(1, 2**(j+1)) for j in range(n)), F(0)) == 1-F(1, 2**n))

result = {
    'problem_id': 2305050,
    'arithmetic': 'exact rational; Python standard library',
    'passed': True,
    'assertions_by_category': dict(sorted(counts.items())),
    'total_assertions': sum(counts.values()),
    'scope': 'Finite auxiliary checks only. No formal analytic existence verification.',
    'analytic_input': 'Carroll (1979), Theorems 1 and 2; credited classical dependencies.'
}
print(json.dumps(result, indent=2, sort_keys=True))
