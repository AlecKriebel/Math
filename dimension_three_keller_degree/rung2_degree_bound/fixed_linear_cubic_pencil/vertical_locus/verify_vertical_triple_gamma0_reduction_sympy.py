#!/usr/bin/env python3
"""Exact raw-determinant check for the triple-root gamma=0 reduction."""

from __future__ import annotations

import os
import sympy as sp


if not __debug__:
    raise SystemExit("refusing optimized Python: fail-closed checks required")


def check(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


x, y, z = sp.symbols("x y z")
s, u, v, w, alpha = sp.symbols("s u v w alpha")
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
t = sp.symbols("t0:9")
l = sp.symbols("l0:9")
quadratics = (x**2, x * y, y**2, x * z, y * z, z**2)
cubics = (
    x**3,
    x**2 * y,
    x * y**2,
    y**3,
    x**2 * z,
    x * y * z,
    y**2 * z,
    x * z**2,
    y * z**2,
)
A = sum(coefficient * monomial for coefficient, monomial in zip(a, quadratics))
B = sum(coefficient * monomial for coefficient, monomial in zip(b, quadratics))
V = sum(coefficient * monomial for coefficient, monomial in zip(t, cubics))
L = sp.Matrix(3, 3, l)
W = z * (u * x + v * y + w * z)

charts = {
    "quadratic_y": (
        x**3 + y**2 * z + alpha * x * z**2,
        (
            (sp.Rational(1, 3), x**3 * y * z**2),
            (1, y**3 * z**3),
        ),
        sp.Rational(8, 3) * s * u,
    ),
    "mixed_xy": (
        x**3 + x * y * z,
        (
            (-sp.Rational(1, 9), x**4 * z**2),
            (-sp.Rational(1, 3), x**2 * y * z**3),
            (1, y**2 * z**4),
        ),
        -sp.Rational(4, 9) * s * u,
    ),
    "linear_y": (
        x**3 + y * z**2,
        (
            (sp.Rational(1, 3), x**3 * z**3),
            (1, y * z**5),
        ),
        sp.Rational(4, 3) * s * u,
    ),
}

mutation = os.environ.get("GAMMA0_REDUCTION_MUTATION", "strict")

for label, (q, combination, expected_u) in charts.items():
    H2 = sp.Matrix((A, B, W))
    H3 = sp.Matrix((sp.Rational(4, 3) * z * W + s * q, V, z**3))
    H4 = sp.Matrix((z**4, z * q, 0))
    determinant = sp.Poly(
        sp.expand(
            (L + H2.jacobian((x, y, z)) + H3.jacobian((x, y, z))
             + H4.jacobian((x, y, z))).det()
        ),
        x,
        y,
        z,
    )

    expected_v = -3 * s * v
    if mutation == f"{label}_v":
        expected_v += 1
    check(
        sp.expand(determinant.coeff_monomial(x**5 * z) - expected_v) == 0,
        f"{label}: coefficient killing v",
    )

    obstruction = sp.factor(
        sum(
            coefficient * determinant.coeff_monomial(monomial)
            for coefficient, monomial in combination
        ).subs(v, 0)
    )
    if mutation == f"{label}_u":
        expected_u += 1
    check(
        sp.expand(obstruction - expected_u) == 0,
        f"{label}: coefficient combination killing u",
    )

if mutation != "strict":
    raise SystemExit(f"FAIL: unknown or escaped mutation {mutation}")

print("VERTICAL_TRIPLE_GAMMA0_REDUCTION_SYMPY_PASS_5C7A91")
