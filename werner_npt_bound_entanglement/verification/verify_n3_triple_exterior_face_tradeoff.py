#!/usr/bin/env python3
"""Exact arithmetic audit for the triple-exterior face tradeoff."""

from fractions import Fraction as F


# Sector-to-face identities.
# Coordinates are ordered as (R, S, a, c, p).
x = (F(-4, 9), F(0), F(4, 3), F(2, 3), F(0))
d = (F(0), F(1, 9), F(-1, 12), F(1, 3), F(0))


def add(*vectors):
    return tuple(sum(entries, F(0)) for entries in zip(*vectors))


def scale(q, vector):
    return tuple(q * entry for entry in vector)


# 24*(J3+p/3) = -24*x+12*a-6*c+3*d+8*p.
unit_R = (F(1), F(0), F(0), F(0), F(0))
unit_S = (F(0), F(1), F(0), F(0), F(0))
unit_a = (F(0), F(0), F(1), F(0), F(0))
unit_c = (F(0), F(0), F(0), F(1), F(0))
unit_p = (F(0), F(0), F(0), F(0), F(1))

triple = add(
    scale(F(-24), x),
    scale(F(12), unit_a),
    scale(F(-6), unit_c),
    scale(F(3), d),
    scale(F(8), unit_p),
)
assert triple == (F(32, 3), F(1, 3), F(-81, 4), F(-21), F(8))

# Multiplying the preceding identity by 12 yields the p-retaining
# tradeoff 128R+4S+96p >= 252c+243a.
triple12 = scale(F(12), triple)
assert triple12 == (F(128), F(4), F(-243), F(-252), F(96))

# N = 2c + 9a/4 + (S-4R)/9 and 2p=N-Delta.
# Substitute 96p=48N-48Delta in the p-retaining tradeoff.
coeff_R = F(128) + F(48) * F(-4, 9)
coeff_S = F(4) + F(48) * F(1, 9)
coeff_a = F(-243) + F(48) * F(9, 4)
coeff_c = F(-252) + F(48) * F(2)
coeff_delta = F(-48)
assert (coeff_R, coeff_S, coeff_a, coeff_c, coeff_delta) == (
    F(320, 3),
    F(28, 3),
    F(-135),
    F(-156),
    F(-48),
)

# After multiplication by 3:
# 320R+28S >= 468c+405a+144Delta.
assert tuple(
    F(3) * q
    for q in (coeff_R, coeff_S, coeff_a, coeff_c, coeff_delta)
) == (F(320), F(28), F(-405), F(-468), F(-144))

# Negative-depth substitution:
# R=3/2*(1-5 delta)*(1-L),
# S=3/4*(1-5 delta)*L,
# c=(1+delta)/3.
# The residual is
# 324 - 2556 delta - 459(1-5delta)L - 405a - 144Delta.
constant = F(320) * F(3, 2) - F(468) * F(1, 3)
delta = F(320) * F(3, 2) * F(-5) - F(468) * F(1, 3)
L = -F(320) * F(3, 2) + F(28) * F(3, 4)
assert (constant, delta, L) == (F(324), F(-2556), F(-459))

# The depth intercept reduces exactly to 9/71 and improves 3/22.
assert F(324, 2556) == F(9, 71)
assert F(9, 71) < F(3, 22)

print("triple-exterior face tradeoff: exact audit passed")
