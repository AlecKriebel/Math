#!/usr/bin/env python3
"""Exact finite arithmetic controls, not a gauge-theory or manifold verifier.

Python 3 standard library only. Run `python3 verify.py > replay.json`, then
compare replay.json to verification.json. No downloaded sources are required.
"""
import json
from fractions import Fraction as F
from math import gcd

checks = {}


def check(family, condition):
    if not condition:
        raise AssertionError(family)
    checks[family] = checks.get(family, 0) + 1


def kernel_original(k, r):
    # Bauer--Furuta I, Lemma 3.5. Order one denotes the trivial group.
    if k in (0, 4):
        return 1
    if k in (1, 2):
        return gcd(2, r)
    if k == 3:
        return gcd(24, r) if r % 2 == 0 else gcd(24, r - 3) // 2
    raise ValueError(k)


def kernel_survey(k, r):
    # Bauer survey Proposition 6.1, expressed by primary components.
    if k in (0, 4):
        return 1
    if k in (1, 2):
        return 2 if r % 2 == 0 else 1
    if k == 3:
        two_part = (8, 1, 2, 4, 4, 1, 2, 2)[r % 8]
        three_part = 3 if r % 3 == 0 else 1
        return two_part * three_part
    raise ValueError(k)


for r in range(2, 50):
    for k in range(5):
        bp = 2 * r - k - 1
        if bp <= 1:
            continue
        check("published_kernel_formula_crosscheck", kernel_original(k, r) == kernel_survey(k, r))
        if k in (1, 2) and kernel_original(k, r) > 1:
            check("witness_congruence", r % 2 == 0)
            check("witness_congruence", bp % 4 == (2 if k == 1 else 1))

for bp in range(2, 19):
    for bm in range(0, 20):
        chi, sig = 2 + bp + bm, bp - bm
        for r in range(-4, 13):
            c2 = sig + 8 * r  # index-integral arithmetic datum, not realization
            k = F(c2 - 2 * chi - 3 * sig, 4)
            check("index_identity", k == 2 * r - 1 - bp)
            check("index_parity", k.denominator == 1 and int(k) % 2 == (1 + bp) % 2)

k3_models = []
chi, sig = 2, 0
for m in range(1, 9):
    chi, sig = chi + 24 - 2, sig - 16
    bp, bm = 3 * m, 19 * m
    check("connected_sum_recurrence", chi == 22 * m + 2 and sig == -16 * m)
    check("connected_sum_recurrence", chi == 2 + bp + bm and sig == bp - bm)
    check("connected_sum_spin_dimension", F(-2 * chi - 3 * sig, 4) == m - 1)
    k3_models.append({"m": m, "chi": chi, "signature": sig, "b_plus": bp, "b_minus": bm, "spin_dimension": m - 1})

# Q = diag(1,-1,-1), C=(0,1,1) with Q(C)=-2.
def square(v):
    return v[0] ** 2 - v[1] ** 2 - v[2] ** 2


def reflection(v):
    pairing = -v[1] - v[2]
    return (v[0], v[1] + pairing, v[2] + pairing)


for a in range(-5, 6):
    for b in range(-5, 6):
        for c in range(-5, 6):
            v = (a, b, c)
            rv = reflection(v)
            diff = tuple(x - y for x, y in zip(rv, v))
            check("sphere_reflection", reflection(rv) == v)
            check("sphere_reflection", square(rv) == square(v))
            check("sphere_reflection", square(diff) == -2 * (b + c) ** 2)

minus_two_gluing = {"chi": 2 * (24 - 2), "signature": 2 * (-16 + 1), "b1": 0}
minus_two_gluing["b_plus"] = (minus_two_gluing["chi"] - 2 + minus_two_gluing["signature"]) // 2
minus_two_gluing["b_minus"] = (minus_two_gluing["chi"] - 2 - minus_two_gluing["signature"]) // 2
check("minus_two_gluing_arithmetic", minus_two_gluing == {"chi": 44, "signature": -30, "b1": 0, "b_plus": 6, "b_minus": 36})

for n in range(2, 33):
    bp, bm = 4 * n - 2, 20 * n - 2
    chi, sig = 2 + bp + bm, bp - bm
    check("fkm_family_indices", (chi, sig) == (24 * n - 2, -16 * n))
    check("fkm_family_indices", F(-sig, 8) == 2 * n)
    check("fkm_family_indices", F(-2 * chi - 3 * sig, 4) == 1)
    check("fkm_family_target_order", kernel_original(1, 2 * n) == 2)

quotient_degrees = {}
for m in range(1, 129):
    allowed = []
    for q in range(1, 65):
        chi, sig = F(22 * m + 2, q), F(-16 * m, q)
        bp, bm = (chi + sig) / 2 - 1, (chi - sig) / 2 - 1
        integral = all(x.denominator == 1 for x in (chi, sig, bp, bm))
        divisibility = gcd(16, 3 * m + 1) % q == 0
        check("quotient_degree_equivalence", integral == divisibility)
        if integral:
            allowed.append(q)
            check("quotient_betti_nonnegative", bp >= 0 and bm >= 0)
    if m <= 8:
        quotient_degrees[str(m)] = allowed
check("quotient_small_cases", quotient_degrees["2"] == [1])
check("quotient_small_cases", quotient_degrees["3"] == [1, 2])
check("quotient_small_cases", quotient_degrees["4"] == [1])

result = {
    "scope": "Finite exact arithmetic and two published kernel-formula crosschecks only. No manifold is constructed, no BF invariant is computed from a monopole map, and irreducibility is not tested.",
    "assertions_by_family": checks,
    "total_assertions": sum(checks.values()),
    "k3_connected_sum_arithmetic": k3_models,
    "minus_two_gluing_arithmetic": minus_two_gluing,
    "arithmetically_possible_free_oriented_quotient_degrees": quotient_degrees,
    "result": "PASS"
}
print(json.dumps(result, indent=2, sort_keys=True))
