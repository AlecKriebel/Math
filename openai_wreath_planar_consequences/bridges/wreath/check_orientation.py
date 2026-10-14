#!/usr/bin/env python3
"""Exact falsification controls for the wreath-map algebra.

This uses M_2 of the bicyclic algebra F_2<a,b>/(ab-1), NOT a group
algebra. It supplies a noncommutative test ring with an actual defect,
and a finite group of units with which b fails to commute. It cannot
establish the existence premise of Target A.
"""
import itertools
import json


# Basis monomial (i,j) means b^i a^j. Reduction deletes every adjacent ab.
ZERO = frozenset()
ONE = frozenset({(0, 0)})
A = frozenset({(0, 1)})
B = frozenset({(1, 0)})


def add(x, y):
    return x ^ y


def mul(x, y):
    result = ZERO
    for i, j in x:
        for k, ell in y:
            pair = (i + max(k - j, 0), ell + max(j - k, 0))
            result = result ^ frozenset({pair})
    return result


def mat(a, b, c, d):
    return (a, b, c, d)


Z = mat(ZERO, ZERO, ZERO, ZERO)
I = mat(ONE, ZERO, ZERO, ONE)


def madd(x, y):
    return tuple(add(p, q) for p, q in zip(x, y))


def mmul(x, y):
    return mat(add(mul(x[0], y[0]), mul(x[1], y[2])),
               add(mul(x[0], y[1]), mul(x[1], y[3])),
               add(mul(x[2], y[0]), mul(x[3], y[2])),
               add(mul(x[2], y[1]), mul(x[3], y[3])))


def wmul(x, y):
    r, h = x
    s, k = y
    return (madd(r, mmul(h, s)), mmul(h, k))


def phi(x):
    r, h = x
    return (mmul(r, bb), h)


def sigma(x):
    r, h = x
    return (mmul(r, aa), h)


aa = mat(A, ZERO, ZERO, ONE)
bb = mat(B, ZERO, ZERO, ONE)
ee = madd(I, mmul(bb, aa))
assert mmul(aa, bb) == I
assert mmul(bb, aa) != I
assert ee != Z and mmul(ee, ee) == ee and mmul(ee, bb) == Z

# Distinct normal forms can also be separated by their action on a
# countably infinite basis: a lowers index and kills index zero, while
# b raises index. The finite checks below are just orientation controls.
basis = [frozenset({(i, j)}) for i in range(4) for j in range(4)]
associativity_controls = 0
for x, y, z in itertools.product(basis, repeat=3):
    assert mul(mul(x, y), z) == mul(x, mul(y, z))
    associativity_controls += 1

units = []
for bits in itertools.product((0, 1), repeat=4):
    if (bits[0] * bits[3] + bits[1] * bits[2]) % 2 == 1:
        units.append(tuple(ONE if bit else ZERO for bit in bits))
assert len(units) == 6
for h, k in itertools.product(units, repeat=2):
    assert mmul(h, k) in units

samples = [Z, I, aa, bb, ee, madd(aa, bb),
           mat(A, B, ZERO, ONE), mat(ONE, ZERO, B, A),
           mat(ee[0], A, B, ee[0])]
homomorphism_controls = 0
section_controls = 0
kernel_controls = 0
wrong_orientation_failures = 0
for r, h in itertools.product(samples, units):
    assert phi(sigma((r, h))) == (r, h)
    section_controls += 1
    z = mmul(r, ee)
    assert mmul(z, bb) == Z and mmul(z, ee) == z
    kernel_controls += 1
for r, s, h, k in itertools.product(samples, samples, units, units):
    x, y = (r, h), (s, k)
    assert phi(wmul(x, y)) == wmul(phi(x), phi(y))
    homomorphism_controls += 1
    left = lambda v: (mmul(bb, v[0]), v[1])
    if left(wmul(x, y)) != wmul(left(x), left(y)):
        wrong_orientation_failures += 1
assert wrong_orientation_failures > 0
assert phi((ee, I)) == (Z, I)

print(json.dumps({
    "status": "passed",
    "scope": "exact algebraic controls in a bicyclic matrix ring, not a group-ring counterexample",
    "basis_associativity_controls": associativity_controls,
    "homomorphism_controls": homomorphism_controls,
    "right_inverse_section_controls": section_controls,
    "principal_kernel_controls": kernel_controls,
    "wrong_left_multiplication_failures": wrong_orientation_failures,
    "nonzero_idempotent_kernel_witness": True,
    "target_a_group_ring_premise_established": False
}, indent=2, sort_keys=True))
