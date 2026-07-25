#!/usr/bin/env python3
"""Exact raw-determinant check for the nonzero-gamma triple-root exclusion."""

from __future__ import annotations

import os
import sympy as sp


if not __debug__:
    raise SystemExit("refusing optimized Python: fail-closed checks required")


def check(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


x, y, z = sp.symbols("x y z")
s, gamma, u, v, w, alpha = sp.symbols("s gamma u v w alpha")
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
W = gamma * x**2 + z * (u * x + v * y + w * z)

charts = {
    "quadratic_y": x**3 + y**2 * z + alpha * x * z**2,
    "mixed_xy": x**3 + x * y * z,
    "linear_y": x**3 + y * z**2,
}
mutation = os.environ.get("GAMMA_NONZERO_MUTATION", "strict")

for label, q in charts.items():
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

    if label == "quadratic_y":
        actual = determinant.coeff_monomial(x**4 * y * z)
        expected = 4 * gamma * s
    elif label == "mixed_xy":
        first = determinant.coeff_monomial(x**5 * z)
        second = (
            -sp.Rational(1, 6)
            * determinant.coeff_monomial(x**3 * y * z**2)
            + determinant.coeff_monomial(x * y**2 * z**3)
        )
        expected_first = s * (2 * gamma - 3 * v)
        expected_second = -s * (gamma + v) / 3
        if mutation == "mixed_xy_first":
            expected_first += 1
        if mutation == "mixed_xy_second":
            expected_second += 1
        check(
            sp.expand(first - expected_first) == 0,
            "mixed_xy: first obstruction",
        )
        check(
            sp.expand(second - expected_second) == 0,
            "mixed_xy: second obstruction",
        )
        continue
    else:
        actual = (
            sp.Rational(2, 3) * determinant.coeff_monomial(x**4 * z**2)
            + determinant.coeff_monomial(x * y * z**4)
        )
        expected = sp.Rational(10, 3) * gamma * s

    if mutation == label:
        expected += 1
    check(sp.expand(actual - expected) == 0, f"{label}: obstruction")

if mutation != "strict":
    raise SystemExit(f"FAIL: unknown or escaped mutation {mutation}")

print("VERTICAL_TRIPLE_GAMMA_NONZERO_SYMPY_PASS_D4E821")
