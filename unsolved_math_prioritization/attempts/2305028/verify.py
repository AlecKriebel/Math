#!/usr/bin/env python3
"""Exact arithmetic checks for the independently written proof exposition.

This checks no numerical boundary sampling and makes no claim to formalize
holomorphy or the compactness arguments. Run with Python 3, standard library.
"""
from fractions import Fraction as Q
import json

R = 2**24
M = 2**6 + 2**8
assert M == 320
x0 = Q(1, 16)
cosine_upper = 2 * (1 - x0*x0/2 + x0**4/24)
A_upper = Q(1, 2**18) + Q(1, 2**16)
radial = Q(2*R, R+1)
ratio_lower = radial / (cosine_upper + A_upper)
lam = Q(1001, 1000)
assert cosine_upper == Q(1569793, 786432)
assert A_upper == Q(5, 2**18)
assert ratio_lower == Q(1649267441664, 1646063091521)
assert ratio_lower > lam > 1
c = Q(1, 2*M)
eta = Q(1, 10000)
q = eta*c/4
assert c == Q(1, 640)
assert q == Q(1, 25600000)
assert 0 < q < 1
assert 2*q/(1-q) <= eta*c
limsup_lower = (lam - 2*eta) / (1 + 2*eta)
assert limsup_lower == Q(1668, 1667)
assert limsup_lower > 1
# The tail estimate is homogeneous in epsilon_n; check additional scales
# exactly as a guard against exponent/index mistakes in the implementation.
for n in range(1, 21):
    eps = q**(n-1)
    tail = 2*q**n/(1-q)
    assert tail <= eta*c*eps
    assert (lam*eps*c - 2*eta*eps*c)/(eps*c + 2*eta*eps*c) == limsup_lower

print(json.dumps({
    "all_checks_passed": True,
    "arithmetic": "exact fractions; no floating-point inequalities",
    "R": R,
    "M": M,
    "G_upper": str(cosine_upper),
    "A_upper": str(A_upper),
    "radial_increment": str(radial),
    "half_plane_ratio_lower": str(ratio_lower),
    "lambda": str(lam),
    "c": str(c),
    "eta": str(eta),
    "q": str(q),
    "normalized_tail": str(2*q/(1-q)),
    "tail_budget": str(eta*c),
    "limsup_ratio_lower": str(limsup_lower),
    "extra_scale_checks": 20,
    "scope": "Arithmetic certificate only. Analytic steps are proved in PROOF.md."
}, indent=2, sort_keys=True))
