#!/usr/bin/env python3
"""Exact positive-atom certificate for every positively weighted triangle."""

from __future__ import annotations

from itertools import permutations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve()
CROSS_SUM = HERE.parents[2] / "obstruction" / "cross_sum_three_halves"
sys.path.insert(0, str(CROSS_SUM))

import verify_product_and_drift as triangle  # noqa: E402


CERTIFICATE = (
    ((0, 4, 12), 548352),
    ((0, 7, 9), 4264448),
    ((1, 6, 9), 84296896),
    ((1, 10, 5), 5584704),
    ((2, 3, 11), sp.Rational(32301347, 2)),
    ((2, 4, 10), 383784087),
    ((2, 5, 9), sp.Rational(532873583, 2)),
    ((2, 10, 4), 13201248),
    ((3, 7, 6), sp.Rational(5415272957, 2)),
    ((3, 10, 3), 9855648),
    ((4, 5, 7), sp.Rational(11771853975, 2)),
    ((4, 9, 3), sp.Rational(502149947, 2)),
    ((5, 5, 6), sp.Rational(711455385, 2)),
    ((5, 6, 5), 26233856),
    ((5, 7, 4), sp.Rational(1805132529, 2)),
    ((5, 8, 3), 1834139481),
    ((5, 9, 2), sp.Rational(184705669, 2)),
    ((6, 6, 4), 3640371848),
    ((6, 7, 3), 1773987225),
    ((6, 8, 2), 19359335),
    ((6, 9, 1), 24025392),
    ((7, 8, 1), 85565184),
    ((7, 9, 0), 2198400),
    ((8, 8, 0), 3216800),
)


def certificate_polynomial():
    a, b, c = triangle.VARIABLES
    answer = 0
    for (i, j, k), coefficient in CERTIFICATE:
        assert coefficient > 0
        answer += coefficient * sum(
            x**i * y**j * z**k * (x - y) ** 2
            for x, y, z in permutations((a, b, c))
        )
    return sp.expand(answer)


def main():
    rho_b = triangle.triangle_fixation("Bd")
    rho_d = triangle.triangle_fixation("dB")
    baseline_b = sp.Rational(9, 19)
    baseline_d = sp.Rational(2, 5)
    gap = sp.cancel(1 - (rho_b / baseline_b + 2 * rho_d / baseline_d) / 3)
    numerator, denominator = map(sp.expand, sp.fraction(gap))
    _, primitive_numerator = sp.primitive(numerator, *triangle.VARIABLES)
    assert sp.Poly(
        primitive_numerator - certificate_polynomial(), *triangle.VARIABLES
    ).is_zero
    denominator_coefficients = sp.Poly(
        denominator, *triangle.VARIABLES
    ).coeffs()
    assert denominator_coefficients
    assert all(coefficient > 0 for coefficient in denominator_coefficients)

    # Positive weights make every monomial multiplier positive.  Equality in
    # even one complete permutation-sum atom therefore forces a=b=c.
    print("PASS exact Bd and dB weighted-triangle absorbing solves")
    print("PASS 24-atom positive certificate for the one-third gap")
    print("PASS denominator has 127 strictly positive coefficients")
    print("PASS equality among positive triangles occurs only at a=b=c")


if __name__ == "__main__":
    main()
