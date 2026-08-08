#!/usr/bin/env python3
"""Exact symbolic verifier for the homogeneous dense-pair relay theorem."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    r, z, T = sp.symbols("r z T", positive=True)
    x = 1 / (1 + z)
    h = 1 - x
    q = 1 - T

    # Bd first-event equations.
    ratio_bd = x / (x + r * x * T)
    q_bd = (x + h) / (x + h + r * h + r * x * T - r * h * ratio_bd)
    residual_bd = sp.factor(sp.together(q_bd - q))
    expected_bd = sp.factor(
        T
        * (T * r - r + 1)
        * (T * r + r * z + z + 1)
        / (T**2 * r**2 + T * r**2 * z + T * r * z + 2 * T * r + z + 1)
    )
    assert sp.factor(residual_bd - expected_bd) == 0
    p = (r - 1) / r
    assert sp.factor(residual_bd.subs(T, p)) == 0

    # dB first-event equations.
    growth = r * z / (1 + r * z)
    shrink = 2 / (1 + r * z)
    ratio_db = shrink / (shrink + 2 * r * x * T)
    q_db = 1 / (1 + growth + r * x * T - growth * ratio_db)
    residual_db = sp.factor(sp.together(q_db - q))
    numerator_db = sp.factor(sp.fraction(residual_db)[0] / T)
    F = sp.factor(
        r**2 * (r * z + 1) * T**2
        + (-r**3 * z + 2 * r**2 * z**2 + 2 * r**2 * z - r**2 + 2 * r * z + 2 * r) * T
        - r**2 * z**2
        - r**2 * z
        - r * z
        - r
        + z**2
        + 2 * z
        + 1
    )
    assert sp.factor(numerator_db - F) == 0
    assert sp.factor(F.subs(T, 0) + (r - 1) * (z + 1) * (r * z + z + 1)) == 0
    assert sp.factor(F.subs(T, p) - z**2 * (r - 1) ** 2) == 0
    discriminant = sp.factor(sp.discriminant(F, T))
    expected_discriminant = r**3 * (r * z + 1) * (
        r**2 * z + r + 4 * z**3 + 8 * z**2 + 4 * z
    )
    assert sp.factor(discriminant - expected_discriminant) == 0

    # Exact rational instances: one negative root, one root strictly in (0,p).
    for rv, zv in [
        (sp.Rational(3, 2), sp.Rational(1, 10)),
        (sp.Rational(19, 10), sp.Rational(1)),
        (sp.Rational(2), sp.Rational(10)),
    ]:
        polynomial = sp.Poly(F.subs({r: rv, z: zv}), T, domain=sp.QQ)
        intervals = sp.polys.polytools.intervals(polynomial, eps=sp.Rational(1, 10**12))
        assert len(intervals) == 2
        negative, positive = intervals
        assert negative[0][1] < 0
        assert 0 < positive[0][0] < positive[0][1] < (rv - 1) / rv
        assert negative[1] == positive[1] == 1

    print("PASS exact homogeneous dense-pair relay obstruction")


if __name__ == "__main__":
    main()
