#!/usr/bin/env python3
"""Exact sector audit for the normal-residual/Fierz-Hessian reduction."""

from fractions import Fraction as F


# Coefficient vectors use the order (x,a,c,d).
N = (F(1), F(1), F(1), F(1))
q = (F(-1, 8), F(1, 4), F(-1, 2), F(1))
G = (F(0), F(1, 4), F(-1), F(3))
Xi = (F(-5), F(4), F(-1, 2), F(7, 4))
L2 = (F(1, 64), F(1, 16), F(1, 4), F(1))


def add(*vectors):
    return tuple(sum(entries, F(0)) for entries in zip(*vectors))


def scale(number, vector):
    return tuple(number * entry for entry in vector)


# ||L(C)||^2 = 5N/48 -21q/8 +9G/8 +Xi/12.
reconstructed = add(
    scale(F(5, 48), N),
    scale(F(-21, 8), q),
    scale(F(9, 8), G),
    scale(F(1, 12), Xi),
)
assert reconstructed == L2

# The exact endpoint target is the familiar fusion remainder.
# 204G+45a+16Xi-108c = 640q.
a = (F(0), F(1), F(0), F(0))
c = (F(0), F(0), F(1), F(0))
fusion = add(
    scale(F(204), G),
    scale(F(45), a),
    scale(F(16), Xi),
    scale(F(-108), c),
)
assert fusion == scale(F(640), q)

# The scalar tight-frame collapse cannot conflict with a negative q.
# For -1/2 <= q < 0, even the bare lower part of (1) lies strictly
# below 123(1-q)/8.  Its difference has positive coefficients when
# t=-q lies in (0,1/2].
# RHS - [5/48 -21q/8 -q^2] = 733/48 -51q/4 +q^2.
assert F(123, 8) - F(5, 48) == F(733, 48)
assert F(-123, 8) + F(21, 8) == F(-51, 4)

print("normal-residual Fierz-Hessian sector identities: exact")
