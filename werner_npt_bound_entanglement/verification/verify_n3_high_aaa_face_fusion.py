#!/usr/bin/env python3
"""Exact audit of the high-AAA / face-deficit fusion."""

from fractions import Fraction as F


# Symbols are represented as coefficient tuples in
# (constant, delta, u, a, Delta).


def add(*vectors):
    return tuple(sum(entries, F(0)) for entries in zip(*vectors))


def scale(q, vector):
    return tuple(q * entry for entry in vector)


one = (F(1), F(0), F(0), F(0), F(0))
delta = (F(0), F(1), F(0), F(0), F(0))
u = (F(0), F(0), F(1), F(0), F(0))
a = (F(0), F(0), F(0), F(1), F(0))
imbalance = (F(0), F(0), F(0), F(0), F(1))

c = scale(F(1, 3), add(one, delta))
norm = add(scale(F(4), delta), scale(F(3, 4), u), scale(F(9, 4), a))
p = scale(F(1, 2), add(norm, scale(F(-1), imbalance)))

assert c == (F(1, 3), F(1, 3), F(0), F(0), F(0))
assert norm == (F(0), F(4), F(3, 4), F(9, 4), F(0))
assert p == (F(0), F(2), F(3, 8), F(9, 8), F(-1, 2))

# Shifted inequality c < 4/9*(N+p) has residual
# 42 delta+9u+27a-6-4Delta > 0 after multiplication by 18.
shifted_residual = scale(F(18), add(scale(F(4, 9), add(norm, p)), scale(F(-1), c)))
assert shifted_residual == (F(-6), F(42), F(9), F(27), F(-4))

# The triple-Hodge inequality has residual
# 324-2556delta-459u-405a-144Delta = 864e.
K = (F(324), F(-2556), F(-459), F(-405), F(-144))

# Substitution using the inequality orientation:
# 405a > 90+60Delta-630delta-135u, inserted into K.
high_branch = (F(234), F(-1926), F(-324), F(0), F(-204))
assert F(234, 1926) == F(13, 107)

# K>=0 gives Delta <= (...)/144.  Substitution into p gives
# p >= (87delta-9)/8 + 63u/32 + 81a/32.
p_lower = (
    F(-9, 8),
    F(87, 8),
    F(63, 32),
    F(81, 32),
    F(0),
)
substituted = add(
    p,
    scale(F(1, 2), imbalance),
    scale(
        F(1, 288),
        (F(-324), F(2556), F(459), F(405), F(0)),
    ),
)
assert substituted == p_lower

eps = F(1, 10**120)
beta = (F(648) + F(2187) * eps) / (F(5112) + F(21141) * eps)
assert beta > F(13, 107)
assert beta < F(9, 71)
assert F(9, 71) - beta == (
    F(34992) * eps / (F(71) * (F(5112) + F(21141) * eps))
)

# Check the low-AAA rearrangement exactly:
# 324-2556d > (243/2) eps (87d-9).
assert beta == (
    F(324) + F(2187, 2) * eps
) / (
    F(2556) + F(21141, 2) * eps
)

print("high-AAA face fusion: exact audit passed")
