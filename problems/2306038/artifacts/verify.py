#!/usr/bin/env python3
"""Exact auxiliary checks, not a formal verification of Milin's theorem."""
from fractions import Fraction as F
from math import comb
import json

# Q(sqrt(2)), represented by pairs of rationals.
def add(x, y):
    return (x[0] + y[0], x[1] + y[1])

def mul(x, y):
    return (x[0]*y[0] + 2*x[1]*y[1], x[0]*y[1] + x[1]*y[0])

one = (F(1), F(0))
sqrt2_minus_one = (F(-1), F(1))
beta = mul(sqrt2_minus_one, sqrt2_minus_one)
assert beta == (F(3), F(-2))
assert mul(beta, (F(3), F(2))) == one
half_beta = (beta[0]/2, beta[1]/2)
assert add(half_beta, half_beta) == beta
# 7/5 < sqrt(2) < 10/7; the upper bound yields beta > 1/7.
assert F(7, 5)**2 < 2 < F(10, 7)**2
assert 3 - 2*F(10, 7) == F(1, 7) > 0

abel_cases = 0
for n in range(1, 51):
    x = [F((3*k+1) % 11, k+2) for k in range(1, n+1)]
    alpha = [F(1, k*k) for k in range(1, n+1)]
    sums, current = [], F(0)
    for v in x:
        current += v
        sums.append(current)
    lhs = sum((alpha[k]*x[k] for k in range(n)), F(0))
    rhs = alpha[-1]*sums[-1] + sum(
        ((alpha[k]-alpha[k+1])*sums[k] for k in range(n-1)), F(0))
    assert lhs == rhs
    assert n*alpha[-1] + sum(
        ((k+1)*(alpha[k]-alpha[k+1]) for k in range(n-1)), F(0)) == sum(alpha, F(0))
    A = max(sums[k]/(k+1) for k in range(n))
    assert lhs <= A*sum(alpha, F(0))
    abel_cases += 1

# Classical endpoint example f(z)=z(1-z^4)^(-1/2).
a = [F(comb(2*m, m), 4**m) for m in range(101)]
assert a[0] == 1 and a[1] == F(1, 2)
for m in range(100):
    assert a[m+1] == a[m]*F(2*m+1, 2*m+2)
    assert (2*m+1)**2 - 4*m*(m+1) == 1
for m in range(1, 101):
    assert a[m]**2 >= F(1, 4*m)

b = [a[k//2] if k % 2 == 0 else F(0) for k in range(202)]
d = [None] + [abs(b[k])-abs(b[k-1]) for k in range(1, 202)]
assert d[1] == -1
for m in range(1, 101):
    assert d[2*m] == a[m] and d[2*m+1] == -a[m]
for M in range(1, 101):
    assert sum((d[k]**2 for k in range(1, 2*M+2)), F(0)) == 1+2*sum((a[m]**2 for m in range(1, M+1)), F(0))

# Coefficients of (u-v)(1+uv): u-v+u^2 v-uv^2.
# These equal u(1-v^2)-v(1-u^2), the cross-multiplication numerator.
left = {(1, 0): 1, (0, 1): -1, (2, 1): 1, (1, 2): -1}
right = {(1, 0): 1, (1, 2): -1, (0, 1): -1, (2, 1): 1}
assert left == right

print(json.dumps({
    "all_checks_passed": True,
    "arithmetic": "exact integers and rational pairs in Q(sqrt(2))",
    "beta_coefficients": [str(v) for v in beta],
    "beta_positive_lower_bound": "1/7",
    "factor_of_two_substitution": True,
    "abel_identity_cases": abel_cases,
    "endpoint_recurrence_cases": 100,
    "endpoint_lower_bound_cases": 100,
    "endpoint_partial_sum_cases": 100,
    "injectivity_cross_multiplication_identity": True,
    "analytic_theorem_formally_verified": False
}, indent=2, sort_keys=True))
