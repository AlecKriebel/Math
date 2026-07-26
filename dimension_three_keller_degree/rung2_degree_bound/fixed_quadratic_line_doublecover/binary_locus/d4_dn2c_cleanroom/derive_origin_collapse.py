#!/usr/bin/env python3
"""Exact full-lower descent on the zero-contact DN2C chart."""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, weight = sp.symbols("p q r weight")
coords = (p, q, r)
h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand(h * (p - 2 * q))

x, y = sp.symbols("x y")
uc = sp.symbols("uc0:4")
vc = sp.symbols("vc0:4")
tc = sp.symbols("tc0:3")
ab = sp.symbols("ab0:3")
bb = sp.symbols("bb0:3")
ell = sp.symbols("ell0:8")

binary3 = (p**3, p**2 * q, p * q**2, q**3)
binary2 = (p**2, p * q, q**2)
U = sum(value * monomial for value, monomial in zip(uc, binary3))
V = sum(value * monomial for value, monomial in zip(vc, binary3))
T = sum(value * monomial for value, monomial in zip(tc, binary2))
A = (
    sum(value * monomial for value, monomial in zip(ab, binary2))
    + r * (x * (p + 2 * q) + 4 * y * (p + q))
)
B = (
    sum(value * monomial for value, monomial in zip(bb, binary2))
    + r * x * q
)
linear = sp.Matrix(
    (
        (ell[0], ell[1], ell[2]),
        (ell[3], ell[4], ell[5]),
        (ell[6], ell[7], 3 * y),
    )
)

H2 = sp.Matrix((A, B, T))
H3 = sp.Matrix((U, V, R))
H4 = sp.Matrix((P, Q, 0))
determinant = sp.Poly(
    sp.expand(
        (
            linear
            + weight * H2.jacobian(coords)
            + weight**2 * H3.jacobian(coords)
            + weight**3 * H4.jacobian(coords)
        ).det()
    ),
    weight,
)
assert sp.expand(determinant.coeff_monomial(weight**7)) == 0
assert sp.expand(determinant.coeff_monomial(weight**6)) == 0

LOWER = set(uc + vc + tc + ab + bb + ell)


def scan(level: int) -> list[tuple[tuple[int, int, int], sp.Expr]]:
    expression = sp.Poly(
        sp.expand(determinant.coeff_monomial(weight**level)),
        p,
        q,
        r,
    )
    lower_free = []
    print("LEVEL", level)
    for rdegree in range(level + 1):
        for pdegree in range(level - rdegree, -1, -1):
            exponent = (pdegree, level - rdegree - pdegree, rdegree)
            value = expression.coeff_monomial(
                p ** exponent[0] * q ** exponent[1] * r ** exponent[2]
            )
            dependencies = value.free_symbols & LOWER
            if value != 0 and not dependencies:
                value = sp.factor(value)
                lower_free.append((exponent, value))
                print("  LOWER_FREE", exponent, value)
    return lower_free


free5 = scan(5)
free4 = scan(4)
expected4 = {
    (3, 0, 1): -3 * x**2,
    (2, 1, 1): 24 * y * (x + y),
    (1, 2, 1): 3 * (x + 4 * y) * (3 * x + 4 * y),
    (0, 3, 1): 6 * (x + 2 * y) ** 2,
}
assert set(dict(free4)) == set(expected4)
assert all(
    sp.factor(dict(free4)[exponent] - expected) == 0
    for exponent, expected in expected4.items()
)
assert free5 == []
# The first equation gives x=0; the second then gives y=0 in
# characteristic zero.  Together with the already-encoded absence of
# r^2 terms, all six r-dependent coefficients of A,B vanish.
print("COUNTS", len(free5), len(free4))

print("D4_DN2C_ORIGIN_COLLAPSE_SCAN_PASS")
