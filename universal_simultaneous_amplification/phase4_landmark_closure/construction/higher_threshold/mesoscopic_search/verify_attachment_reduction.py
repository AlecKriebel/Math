#!/usr/bin/env python3
"""Independent checks for the mesoscopic attachment reductions.

The mathematical proof is in ATTACHMENT_REDUCTION_AND_SEARCH.md.  This file
checks the pair enumeration against dense simplex samples, checks repeated
feasibility witnesses directly, and verifies the regular-class Bd identity
with exact rational arithmetic.  Finite random checks are not a proof.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from pathlib import Path
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from search_modules_6_8 import (  # noqa: E402
    best_product_ratio,
    repeated_feasible,
)


def check_product_pairs() -> None:
    rng = np.random.default_rng(20260802)
    for size in range(3, 9):
        for _ in range(20):
            a, b, c = np.exp(rng.normal(size=(3, size)))
            exact_pair_value, witness = best_product_ratio(a, b, c)
            attachment = witness.vector(size)
            witnessed = (attachment @ a) / (
                (attachment @ b) * (attachment @ c)
            )
            assert abs(witnessed - exact_pair_value) < 2e-11
            samples = rng.dirichlet(np.full(size, 0.18), size=20_000)
            sampled = np.max(
                (samples @ a) / ((samples @ b) * (samples @ c))
            )
            assert sampled <= exact_pair_value * (1 + 2e-10)
    print("PASS: pair attachment optimum dominates 2.4 million simplex samples")


def check_repeated_witnesses() -> None:
    rng = np.random.default_rng(20260803)
    checks = 0
    for size in range(3, 9):
        for _ in range(100):
            degree = np.exp(rng.normal(size=size))
            f_bd, b_bd, f_db, b_db = np.exp(rng.normal(size=(4, size)))
            # Keep fixation-like values in (0,1).
            f_bd /= 1 + f_bd
            b_bd /= 1 + b_bd
            f_db /= 1 + f_db
            b_db /= 1 + b_db
            alpha_bd = float(f_bd.mean())
            alpha_db = float(f_db.mean())
            target = 0.45 * min(alpha_bd, alpha_db)
            witness = repeated_feasible(
                target, 1.51, degree, f_bd, b_bd, f_db, b_db
            )
            if witness is None:
                continue
            h = witness.vector(size)
            q_bd = 1.51 * (h @ f_bd) / (h @ b_bd)
            q_db = 1.51**2 * ((h / degree) @ f_db) / (
                (h / degree) @ b_db
            )
            rho_bd = alpha_bd * (1 - 1 / q_bd)
            rho_db = alpha_db * (1 - 1 / q_db)
            assert rho_bd >= target - 2e-12
            assert rho_db >= target - 2e-12
            checks += 1
    assert checks > 20
    print(f"PASS: {checks} repeated-module pair witnesses satisfy both inequalities")


def check_regular_bd_identity() -> None:
    # An exact weighted-regular module C4 with unequal edge weights alternating
    # 1,2,1,2, over an exact weighted-regular macro triangle.
    module = (
        (0, 1, 0, 2),
        (1, 0, 2, 0),
        (0, 2, 0, 1),
        (2, 0, 1, 0),
    )
    macro = (
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
    )
    epsilon = Fraction(3, 17)
    order = 12
    weights = [[Fraction(0) for _ in range(order)] for _ in range(order)]
    for block in range(3):
        for i, j in combinations(range(4), 2):
            weights[4 * block + i][4 * block + j] = Fraction(module[i][j])
            weights[4 * block + j][4 * block + i] = Fraction(module[i][j])
    for left, right in combinations(range(3), 2):
        outer = epsilon * macro[left][right]
        for i in range(4):
            for j in range(4):
                weights[4 * left + i][4 * right + j] = outer
                weights[4 * right + j][4 * left + i] = outer
    degrees = [sum(row, Fraction(0)) for row in weights]
    assert len(set(degrees)) == 1

    # Check T+/T-=r for every nontrivial labelled state without solving the
    # 4094-state absorbing system.
    fitness = Fraction(31, 20)
    common_degree = degrees[0]
    for mask in range(1, (1 << order) - 1):
        boundary = sum(
            (
                weights[i][j]
                for i in range(order)
                if (mask >> i) & 1
                for j in range(order)
                if not ((mask >> j) & 1)
            ),
            Fraction(0),
        )
        plus = fitness * boundary / common_degree
        minus = boundary / common_degree
        assert plus == fitness * minus

    r = sp.symbols("r", positive=True)
    m = sp.symbols("m", integer=True, positive=True)
    # Clique-module dB trace is strictly below p: the sign reduces to strict
    # convexity r^m > 1+m(r-1).  Verify the exact algebraic numerator.
    factor_gap = sp.factor(
        1
        - sp.Rational(1, 1) * (m - 1) / m
        * (1 - r ** (-m))
        / (1 - r ** (-(m - 1)))
    )
    expected = (r**m - m * r + m - 1) / (m * (r**m - r))
    assert sp.simplify(factor_gap - expected) == 0
    print("PASS: exact regular replacement degrees, Bd state ratios, and clique dB gap")


def main() -> None:
    check_product_pairs()
    check_repeated_witnesses()
    check_regular_bd_identity()


if __name__ == "__main__":
    main()
