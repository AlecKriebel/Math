#!/usr/bin/python3
"""Exact regression checks for the weighted-lift family, d = 3,...,8.

This is not a proof for all d.  See VERIFICATION.md.
"""

from fractions import Fraction
import sympy as sp

x, y, z = sp.symbols("x y z")


def family(d: int):
    u = 1 + x * y
    gamma = 1 - sp.Rational(d, d - 1) * x * y + x**2 * z
    A = sp.cancel(
        ((d - 2) * u + u**2 - (d - 1) * u**d * gamma ** (d - 2))
        / ((d - 2) * x**2)
    )
    B = sp.cancel(
        ((d - 2) + 2 * u - d * u ** (d - 1) * gamma ** (d - 2))
        / ((d - 2) * x)
    )
    C = sp.expand(x * gamma)
    assert all(expr.is_polynomial(x, y, z) for expr in (A, B, C))
    return tuple(sp.expand(expr) for expr in (A, B, C))


def collision_point(d: int, root: int):
    s = Fraction(4 - 2**d, d - 2)
    p = Fraction(2 * root - d * root ** (d - 1), d - 2)
    gamma = s - p
    xx = 1 / gamma
    u = Fraction(root, 1) / gamma
    yy = (u - 1) / xx
    zz = (gamma - 1 + Fraction(d, d - 1) * (u - 1)) / (xx * xx)
    return xx, yy, zz, s


for degree in range(3, 9):
    mapping = family(degree)
    jacobian = sp.Matrix(mapping).jacobian((x, y, z)).det()
    assert sp.expand(jacobian) == 1

    points = []
    for root_value in (1, 2):
        xx, yy, zz, target = collision_point(degree, root_value)
        image = tuple(
            sp.cancel(expr.subs({x: xx, y: yy, z: zz}))
            for expr in mapping
        )
        target_value = sp.Rational(target.numerator, target.denominator)
        assert image == (target_value, target_value, 1)
        points.append((xx, yy, zz))
    assert points[0] != points[1]

print("PASS: exact SymPy Jacobian and collision checks for d=3,...,8")
