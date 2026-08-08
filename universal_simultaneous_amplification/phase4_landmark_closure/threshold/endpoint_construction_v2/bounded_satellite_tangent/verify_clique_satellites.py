#!/usr/bin/env python3
"""Exact certificate for the dilute K_s satellite formulas."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    r, sigma = sp.symbols("r sigma", positive=True)
    s = sp.symbols("s", integer=True, positive=True)

    bd = r ** (s - 1) * (r - 1) / (r**s - 1)
    db = (s - 1) * (r - 1) * r ** (s - 2) / (s * (r ** (s - 1) - 1))
    p = (r - 1) / r
    z_bd = sigma * (r**s - 1)
    z_db = s * r * (r ** (s - 1) - 1) / ((s - 1) * sigma)
    b = sp.factor(s * (bd * z_bd / ((1 + z_bd) * p) - 1))
    d = sp.factor(s * (db * z_db / ((1 + z_db) * p) - 1))
    assert sp.simplify(b - s * (sigma - 1) / (1 + sigma * (r**s - 1))) == 0
    assert sp.simplify(
        d
        - s
        * (s * r - r**s - (s - 1) * sigma)
        / ((s - 1) * sigma + s * r * (r ** (s - 1) - 1))
    ) == 0

    endpoint = sp.Rational(3, 2)
    signs = {}
    for size in (2, 3, 4):
        expression = sp.factor((d + (r - 1) * b).subs({r: endpoint, s: size}))
        numerator, denominator = sp.together(expression).as_numer_denom()
        signs[size] = (sp.factor(numerator), sp.factor(denominator))

    assert sp.factor(signs[2][0]) == -3 * sigma * (4 * sigma - 1)
    q3 = 80 * sigma**2 - 53 * sigma + 36
    q4 = 304 * sigma**2 - 183 * sigma + 176
    assert sp.rem(signs[3][0], q3, sigma) == 0
    assert sp.rem(signs[4][0], q4, sigma) == 0
    assert sp.discriminant(q3, sigma) < 0
    assert sp.discriminant(q4, sigma) < 0
    assert sp.LC(sp.Poly(q3, sigma)) > 0
    assert sp.LC(sp.Poly(q4, sigma)) > 0

    # Exact base case for the analytic induction
    # (3/2)^s > 3s/2 for every integer s>=5.
    assert endpoint**5 > 5 * endpoint

    print("K2 endpoint:", sp.factor(signs[2][0] / signs[2][1]))
    print("K3 numerator:", signs[3][0])
    print("K4 numerator:", signs[4][0])
    print("PASS exact K_s satellite endpoint classification")


if __name__ == "__main__":
    main()

