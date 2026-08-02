#!/usr/bin/env python3
"""Derive exact symbolic adjoint rank gaps on a weighted triangle."""

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
    x, y, z = sp.symbols("x y z", positive=True)
    weights = [[0, x, y], [x, 0, z], [y, z, 0]]
    r = sp.Rational(3, 2)
    selection = r - 1
    l_gen = MOD.dual_generator(weights, r, "Bd")
    c_gen = MOD.reversed_arrow_generator(weights, r)
    pi_l = MOD.stationary(l_gen)
    pi_c = MOD.stationary(c_gen)
    normalizer = (1 + selection) ** 3 - 1
    rank = []
    for k in range(1, 4):
        states = [state for state in range(1, 8) if state.bit_count() == k]
        value = sum(
            (pi_l[state - 1] + pi_c[state - 1])
            * normalizer
            / selection**k
            for state in states
        ) / len(states)
        rank.append(sp.cancel(value))
    numerators = []
    for k in range(2):
        gap = sp.factor(rank[k] - rank[k + 1])
        numerator, denominator = map(sp.factor, sp.fraction(gap))
        numerators.append(numerator)
        print(f"h_{k + 1}-h_{k + 2} numerator:")
        print(numerator)
        print("denominator:")
        print(denominator)
    print("gcd of rank-gap numerators:")
    print(sp.factor(sp.gcd(numerators[0], numerators[1])))
    print("first numerator in elementary symmetric polynomials:")
    print(sp.symmetrize(numerators[0] / 19, [x, y, z], formal=True)[0])
    for k in (1, 2):
        centered = sp.factor(2 - rank[k])
        centered_num, _ = map(sp.factor, sp.fraction(centered))
        print(f"2-h_{k + 1} numerator:")
        print(centered_num)
    degrees = (x + y, x + z, y + z)
    p = (
        (0, x / degrees[0], y / degrees[0]),
        (x / degrees[1], 0, z / degrees[1]),
        (y / degrees[2], z / degrees[2], 0),
    )
    f_density = [
        pi_l[state - 1] * ((1 + selection) ** 3 - 1)
        / selection ** state.bit_count()
        for state in range(1, 8)
    ]
    g_density = [
        pi_c[state - 1] * ((1 + selection) ** 3 - 1)
        / selection ** state.bit_count()
        for state in range(1, 8)
    ]
    for k in (1, 2):
        f_tilt = 0
        g_tilt = 0
        for state in range(1, 8):
            if state.bit_count() != k:
                continue
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
            potential = r * (row_cut - reverse_cut)
            f_tilt += f_density[state - 1] * potential
            g_tilt += g_density[state - 1] * potential
        print(f"level {k} fV numerator factor:")
        print(sp.factor(sp.fraction(sp.factor(f_tilt))[0]))
        print(f"level {k} -gV numerator factor:")
        print(sp.factor(-sp.fraction(sp.factor(g_tilt))[0]))


if __name__ == "__main__":
    main()
