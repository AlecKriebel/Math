#!/usr/bin/env python3
"""Finite diagnostic checks; the analytic proof is REVERSE_THEOREM.md."""
from fractions import Fraction
from math import isclose, log
import json


def factor(n):
    result = []
    p = 2
    while p * p <= n:
        exponent = 0
        while n % p == 0:
            n //= p
            exponent += 1
        if exponent:
            result.append((p, exponent))
        p += 1
    if n > 1:
        result.append((n, 1))
    return result


def mu(n):
    factors = factor(n)
    return 0 if any(k > 1 for _, k in factors) else (-1) ** len(factors)


def phi(n):
    result = n
    for p, _ in factor(n):
        result = result // p * (p - 1)
    return result


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def mangoldt(n):
    fs = factor(n)
    return log(fs[0][0]) if len(fs) == 1 else 0.0


def ramanujan(q, h):
    return sum(d * mu(q // d) for d in divisors(q) if h % d == 0)


max_inverse_error = 0.0
max_derivative_error = 0.0
for n in range(1, 501):
    es = divisors(n)
    inverse = sum(mu(e) for e in es)
    assert inverse == (1 if n == 1 else 0)
    numerator_derivative = -sum(mu(e) * log(n // e) for e in es)
    denominator_derivative = -sum(mu(e) * log(e) for e in es)
    expected = mangoldt(n)
    max_derivative_error = max(max_derivative_error,
                               abs(numerator_derivative + expected),
                               abs(denominator_derivative - expected))
    assert isclose(numerator_derivative, -expected, abs_tol=1e-12)
    assert isclose(denominator_derivative, expected, abs_tol=1e-12)

prime_local_checks = 0
squarefree_q_checks = 0
for h in range(1, 101):
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        cp = p - 1 if h % p == 0 else -1
        nu = 1 if h % p == 0 else 2
        ramanujan_local = 1 + Fraction(cp, (p - 1) ** 2)
        obstruction_local = (1 - Fraction(nu, p)) / (1 - Fraction(1, p)) ** 2
        assert ramanujan_local == obstruction_local
        prime_local_checks += 1
    for q in range(1, 101):
        if mu(q) == 0:
            continue
        factors = [p for p, _ in factor(q)]
        expected_abs = 1
        F = Fraction(1)
        for p in factors:
            expected_abs *= 1 + (p - 2) * (h % p == 0)
            F *= -Fraction(p, p - 1)
        assert abs(ramanujan(q, h)) == expected_abs
        assert F * F / (q * q) == Fraction(1, phi(q) ** 2)
        squarefree_q_checks += 1

# Every finite partial-prime version of the nonnegative S(h) expansion has
# sum_{h<=H} S_P(h) <= H. This checks the exact product cancellation used
# in the proof, rather than relying on approximate infinite products.
mean_bound_checks = 0
for prime_bound in [2, 3, 5, 7, 11, 13]:
    ps = [p for p in range(3, prime_bound + 1) if factor(p) == [(p, 1)]]
    C = Fraction(1)
    reciprocal_mean = Fraction(1)
    for p in ps:
        C *= 1 - Fraction(1, (p - 1) ** 2)
        reciprocal_mean *= 1 + Fraction(1, p * (p - 2))
    assert C * reciprocal_mean == 1
    for H in range(1, 101):
        total = Fraction(0)
        for h in range(2, H + 1, 2):
            value = 2 * C
            for p in ps:
                if h % p == 0:
                    value *= Fraction(p - 1, p - 2)
            total += value
        assert total <= H
        mean_bound_checks += 1

print(json.dumps({
    'status': 'PASS',
    'coefficient_values_checked': 500,
    'maximum_floating_derivative_discrepancy': max_derivative_error,
    'exact_rational_prime_local_checks': prime_local_checks,
    'exact_squarefree_ramanujan_checks': squarefree_q_checks,
    'exact_finite_product_mean_bound_checks': mean_bound_checks,
    'scope': 'Finite diagnostics only; normal convergence, Cauchy transfer, and the infinite singular-series theorem are proved in REVERSE_THEOREM.md.'
}, indent=2))
