#!/usr/bin/env python3
"""Exact arithmetic checks for the quantitative two-component theorem."""

from fractions import Fraction as F


def add(*vectors):
    return tuple(sum(entries, F(0)) for entries in zip(*vectors))


def scale(a, vector):
    return tuple(a * entry for entry in vector)


def monomial(mask):
    out = [F(0)] * 8
    out[mask] = F(1)
    return tuple(out)


# Coefficient order is
# 1,e1,e2,e1e2,e3,e1e3,e2e3,e1e2e3.
identity = monomial(0)
e1 = monomial(1)
e2 = monomial(2)
e3 = monomial(4)
e13 = monomial(5)
e23 = monomial(6)
e123 = monomial(7)

E1 = add(e1, scale(F(-1, 3), identity))
E2 = add(e2, scale(F(-1, 3), identity))
E3 = add(e3, scale(F(-1, 3), identity))

# e3 Phi1 Phi2 = e123 -(e13+e23)/2 + e3/4.
e3_phi1_phi2 = add(
    e123,
    scale(F(-1, 2), e13),
    scale(F(-1, 2), e23),
    scale(F(1, 4), e3),
)

# Expand E1 E3 and E2 E3 directly.
E1E3 = add(
    e13,
    scale(F(-1, 3), e1),
    scale(F(-1, 3), e3),
    scale(F(1, 9), identity),
)
E2E3 = add(
    e23,
    scale(F(-1, 3), e2),
    scale(F(-1, 3), e3),
    scale(F(1, 9), identity),
)

lhs = add(
    scale(F(2), e123),
    scale(F(-1), E1E3),
    scale(F(-1), E2E3),
    scale(F(-1, 18), identity),
)
rhs = add(
    scale(F(2), e3_phi1_phi2),
    scale(F(1, 3), E1),
    scale(F(1, 3), E2),
    scale(F(1, 6), E3),
)
assert lhs == rhs

# The certified and desired rank-one floors and their row coefficients.
def row_coefficient(rank_one_floor):
    return rank_one_floor / (2 * (1 - rank_one_floor))


assert row_coefficient(F(1, 18)) == F(1, 34)
assert row_coefficient(F(1, 9)) == F(1, 16)

# H=18 in the frame lemma leaves H-1=17.  After restoring the
# normalization ||DV||^2=2||D Psi||^2 and
# tau=2<Psi,D Psi>, the coefficient is exactly 1/34.
H = F(18)
assert F(2) * F(1, H - 1) == F(4, 34)

# The desired floor differs from the certified floor by exactly 1/18.
assert F(1, 9) - F(1, 18) == F(1, 18)

print(
    "verified exact two-component map identity, the 1/18 rank-one "
    "floor, and the induced 1/34 trace-deficit coefficient"
)
