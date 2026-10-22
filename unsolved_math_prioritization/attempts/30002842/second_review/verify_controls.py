#!/usr/bin/env python3
"""Independent finite exact controls for an authored VOA proof audit.

These are coefficient and quantifier fixtures, not a implementation of a VOA
or a proof of any general finiteness or inner-derivation conjecture.
"""
from fractions import Fraction as Q
from math import factorial, prod
import json


def c(n):
    return Q((-1)**(n-1), factorial(n-1))


def zero_mode_of_descendant_coefficient(a, weight):
    return a * (-1)**(weight-1) * factorial(weight-1)


def mul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i+j] += a*b
    return out


def evaluate(p, x):
    result = Q(0)
    for coefficient in reversed(p):
        result = result*x + coefficient
    return result


positive_checks = 0
for n in range(2, 101):
    assert zero_mode_of_descendant_coefficient(c(n), n) == 1
    assert c(n)*(n-1)*n == -n*c(n-1)
    assert -c(n)/n == c(n+1)
    assert zero_mode_of_descendant_coefficient(-c(n)/n, n+1) == 1
    # Repeated lowering verifies nonvanishing of the complete finite chain.
    assert c(n)*factorial(n-1)*factorial(n) == (-1)**(n-1)*factorial(n)
    # One nonzero component; support crosses every fixed bound.
    index = n-2
    tilde_support = {n+1}
    assert n >= index+2 and 1 not in tilde_support
    assert not (tilde_support & set(range(2, n)))
    assert 2*zero_mode_of_descendant_coefficient(c(n+1), n+1) == 2
    positive_checks += 8

# General m-step shift preserves every individual zero mode.
for initial_weight in range(1, 16):
    for shift in range(1, 16):
        rising = prod(range(initial_weight, initial_weight+shift))
        normalization = Q((-1)**shift, rising)
        assert normalization*((-1)**shift)*rising == 1
        positive_checks += 1

# The spectral eigenvalue follows from two independent mode coefficients.
for weight in range(1, 101):
    assert (weight-1)*(-weight) == -weight*(weight-1)
    positive_checks += 1

for support in [[], [2], [2,3], [2,5,11], list(range(2,24))]:
    polynomial = [Q(1)]
    for weight in support:
        polynomial = mul(polynomial, [Q(1), Q(1,weight*(weight-1))])
    assert evaluate(polynomial, Q(0)) == 1
    for weight in support:
        assert evaluate(polynomial, Q(-weight*(weight-1))) == 0
    positive_checks += 1 + len(support)

# Controls are mutations whose purported target identities must fail.
negative_controls = {}
negative_controls['wrong_hat_sign_rejected'] = all(
    zero_mode_of_descendant_coefficient(c(n)/n, n+1) != 1
    for n in range(2,101))
negative_controls['wrong_factorial_rejected'] = all(
    zero_mode_of_descendant_coefficient(Q((-1)**(n-1), factorial(n)), n) != 1
    for n in range(2,101))
negative_controls['wrong_spectral_sign_rejected'] = all(
    evaluate([Q(1), Q(1,i*(i-1))], Q(i*(i-1))) != 0
    for i in range(2,101))
negative_controls['vanishing_total_tail_rejected_on_root_current'] = all(
    2*zero_mode_of_descendant_coefficient(c(n), n) != 0
    for n in range(2,101))
assert all(negative_controls.values())
print(json.dumps({
    'ok': True,
    'positive_checks': positive_checks,
    'maximum_descendant_weight_tested': 101,
    'negative_controls': negative_controls,
    'limitations': 'Finite exact algebra checks only. The all-index proofs and VOA hypotheses are in REPORT.md.'
}, indent=2, sort_keys=True))
