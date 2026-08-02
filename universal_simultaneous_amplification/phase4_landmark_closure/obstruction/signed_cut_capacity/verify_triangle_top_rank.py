#!/usr/bin/env python3
"""Exact certificate for `h_2 >= h_3` on every weighted triangle."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp


SOURCE = Path(__file__).parents[1] / "verify_exact_duals.py"
SPEC = importlib.util.spec_from_file_location("exact_duals", SOURCE)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def main() -> None:
    x, y, z, t = sp.symbols("x y z t", positive=True)
    weights = [[0, x, y], [x, 0, z], [y, z, 0]]
    r = sp.Rational(3, 2)
    a = r - 1
    l_gen = MOD.dual_generator(weights, r, "Bd")
    c_gen = MOD.reversed_arrow_generator(weights, r)
    pi_l = MOD.stationary(l_gen)
    pi_c = MOD.stationary(c_gen)
    normalizer = (1 + a) ** 3 - 1

    def rank_average(k: int):
        states = [state for state in range(1, 8) if state.bit_count() == k]
        return sp.cancel(
            sum(
                (pi_l[state - 1] + pi_c[state - 1])
                * normalizer
                / a**k
                for state in states
            )
            / len(states)
        )

    numerator, denominator = map(
        sp.factor, sp.fraction(sp.factor(rank_average(2) - rank_average(3)))
    )
    e1 = x + y + z
    e2 = x * y + x * z + y * z
    e3 = x * y * z
    polynomial = sp.expand(
        e1**3 * e3
        + 56 * e1**2 * e2**2
        - 60 * e1 * e2 * e3
        - 149 * e2**3
    )
    assert sp.expand(numerator - 95 * polynomial) == 0
    assert all(
        coefficient > 0
        for _, coefficient in sp.Poly(denominator, x, y, z).terms()
    )

    # The polynomial is affine in e3 for fixed e1,e2.  The endpoints of the
    # feasible e3 interval have a zero root or two equal roots.  These are the
    # two exact endpoint factorizations used in the proof.
    assert sp.factor(polynomial.subs(z, 0)) == x**2 * y**2 * (
        56 * x**2 - 37 * x * y + 56 * y**2
    )
    assert sp.factor(polynomial.subs({y: t, z: t})) == (
        3 * t**2 * (x - t) ** 2 * (75 * x**2 + 88 * x * t + 25 * t**2)
    )
    assert (-37) ** 2 - 4 * 56 * 56 < 0

    degrees = (x + y, x + z, y + z)
    p = (
        (0, x / degrees[0], y / degrees[0]),
        (x / degrees[1], 0, z / degrees[1]),
        (y / degrees[2], z / degrees[2], 0),
    )
    g = [
        pi_c[state - 1] * normalizer / a ** state.bit_count()
        for state in range(1, 8)
    ]
    top_tilt = 0
    for state in (3, 5, 6):
        row_cut = sum(
            p[i][j]
            for i in range(3)
            for j in range(3)
            if (state >> i) & 1 and not ((state >> j) & 1)
        )
        reverse_cut = sum(
            p[i][j]
            for i in range(3)
            for j in range(3)
            if not ((state >> i) & 1) and (state >> j) & 1
        )
        top_tilt -= g[state - 1] * r * (row_cut - reverse_cut)
    tilt_num, tilt_den = map(
        sp.factor, sp.fraction(sp.factor(top_tilt))
    )
    assert sp.expand(tilt_num - 855 * polynomial) == 0
    assert all(
        coefficient > 0
        for _, coefficient in sp.Poly(tilt_den, x, y, z).terms()
    )
    print("PASS: symbolic triangle dual stationary laws constructed")
    print("PASS: h_2-h_3 numerator equals 95 times the uvw polynomial")
    print("PASS: denominator has strictly positive coefficients")
    print("PASS: boundary and double-root endpoint factors are nonnegative")
    print("PASS: the same polynomial certifies the top C-dual level tilt")


if __name__ == "__main__":
    main()
