#!/usr/bin/env python3
"""Discovery search for a nonnegative atom certificate for `h_1-h_2`."""

from __future__ import annotations

import importlib.util
from itertools import permutations
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
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
    a = r - 1
    pi_l = MOD.stationary(MOD.dual_generator(weights, r, "Bd"))
    pi_c = MOD.stationary(MOD.reversed_arrow_generator(weights, r))
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

    numerator = sp.Poly(
        sp.factor(sp.fraction(sp.factor(rank_average(1) - rank_average(2)))[0] / 19),
        x,
        y,
        z,
    )
    monomials = [
        (i, j, 18 - i - j)
        for i in range(19)
        for j in range(19 - i)
    ]
    atoms = []
    labels = []
    for i in range(17):
        for j in range(17 - i):
            k = 16 - i - j
            atom = sp.Poly(
                sum(
                    u**i * v**j * w**k * (u - v) ** 2
                    for u, v, w in permutations((x, y, z))
                ),
                x,
                y,
                z,
            )
            atoms.append(atom)
            labels.append((i, j, k))

    def coefficient(poly: sp.Poly, powers):
        return float(poly.coeff_monomial(x ** powers[0] * y ** powers[1] * z ** powers[2]))

    matrix = np.array(
        [[coefficient(atom, powers) for atom in atoms] for powers in monomials],
        dtype=float,
    )
    target = np.array([coefficient(numerator, powers) for powers in monomials])
    row_scale = np.maximum(np.max(np.abs(matrix), axis=1), np.abs(target))
    keep = row_scale > 0
    scaled_matrix = matrix[keep] / row_scale[keep, None]
    scaled_target = target[keep] / row_scale[keep]
    result = linprog(
        np.ones(len(atoms)),
        A_eq=scaled_matrix,
        b_eq=scaled_target,
        bounds=(0, None),
        method="highs",
        options={"dual_feasibility_tolerance": 1e-9,
                 "primal_feasibility_tolerance": 1e-9},
    )
    print(result.message)
    if not result.success:
        return
    support = [index for index, value in enumerate(result.x) if value > 1e-7]
    print("support size", len(support))
    print([(labels[index], result.x[index]) for index in support])
    residual = np.max(np.abs(matrix @ result.x - target))
    print("absolute coefficient residual", residual)


if __name__ == "__main__":
    main()
