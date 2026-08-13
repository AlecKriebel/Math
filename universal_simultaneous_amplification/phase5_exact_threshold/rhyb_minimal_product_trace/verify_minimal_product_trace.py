#!/usr/bin/env python3
"""Exact replay of the minimal stationary-product trace identities.

This script verifies reductions only.  It does not assert the open MPER
sign.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
RANK_THREE = HERE.parent / "rhyb_rank_three_renewal"
OBSTRUCTION = HERE.parents[1] / "phase4_landmark_closure" / "obstruction"
sys.path.insert(0, str(RANK_THREE))
sys.path.insert(0, str(OBSTRUCTION))

from verify_exact_duals import dual_generator, stationary  # noqa: E402
from verify_rank_three_renewal import exact_chain_audit  # noqa: E402


def row(values) -> sp.Matrix:
    return sp.Matrix(1, len(values), values)


def hole_identity_audit() -> None:
    weights = (
        (0, 1, 0, 0),
        (1, 0, 2, 0),
        (0, 2, 0, 3),
        (0, 0, 3, 0),
    )
    r = sp.Rational(3, 2)
    order = len(weights)
    full = (1 << order) - 1
    generator = dual_generator(weights, r, "dB")
    invariant = stationary(generator)

    degree = [sum(sp.Rational(x) for x in weights[v]) for v in range(order)]
    transition = [
        [sp.Rational(weights[v][i], degree[v]) for i in range(order)]
        for v in range(order)
    ]
    hit = [
        [
            sp.factor(r * transition[v][i] / (1 + (r - 1) * transition[v][i]))
            for i in range(order)
        ]
        for v in range(order)
    ]
    temperature = [sum(hit[v][i] for v in range(order)) for i in range(order)]

    hole = []
    pair_hole = [[sp.Integer(0) for _ in range(order)] for _ in range(order)]
    for i in range(order):
        hole.append(
            sp.factor(
                sum(
                    invariant[state - 1]
                    for state in range(1, full)
                    if not ((state >> i) & 1)
                )
            )
        )
        for v in range(order):
            pair_hole[i][v] = sp.factor(
                sum(
                    invariant[state - 1]
                    for state in range(1, full)
                    if not ((state >> i) & 1) and not ((state >> v) & 1)
                )
            )

    for i in range(order):
        rhs = sp.factor(
            (
                1
                + sum(hit[v][i] * pair_hole[i][v] for v in range(order))
            )
            / (1 + temperature[i])
        )
        assert sp.factor(hole[i] - rhs) == 0

    sigma = sp.factor(sum(1 / (1 + value) for value in temperature))
    expected_w = sp.factor(
        sum(
            hit[v][i] * pair_hole[i][v] / (1 + temperature[i])
            for i in range(order)
            for v in range(order)
        )
    )
    expected_holes = sp.factor(sum(hole))
    assert sp.factor(expected_holes - sigma - expected_w) == 0

    mean_rank = sp.factor(
        sum(invariant[state - 1] * state.bit_count() for state in range(1, full))
    )
    density = sp.factor(mean_rank / order)
    p = (r - 1) / r
    assert sp.factor(density - p - (order / r - sigma - expected_w) / order) == 0


def minimal_product_algebra(bd, db) -> None:
    r = bd["r"]
    order = bd["s"]
    assert db["r"] == r and db["s"] == order
    p = (r - 1) / r

    density_b = sp.factor(bd["m"] / order)
    density_d = sp.factor(db["m"] / order)
    direct_gap = sp.factor(
        bd["q"] * db["q"]
        - r**3 * (density_b - p) * (density_d - p)
    )

    x_b = sp.factor(bd["M"] - order * p * bd["T"])
    x_d = sp.factor(db["M"] - order * p * db["T"])
    cycle_numerator = sp.factor(
        bd["S"] * db["S"] - r**3 * x_b * x_d / order**2
    )
    assert sp.factor(
        cycle_numerator - bd["T"] * db["T"] * direct_gap
    ) == 0

    pi_b, pi_d = bd["pi_low"], db["pi_low"]
    chi_b = bd["trace_rank"] / order - p * bd["trace_time"]
    chi_d = db["trace_rank"] / order - p * db["trace_time"]
    forcing = (
        bd["trace_singleton"] * db["trace_singleton"].T
        - r**3 * chi_b * chi_d.T
    )
    traced_mean = sp.factor((pi_b * forcing * pi_d.T)[0])
    assert sp.factor(traced_mean - direct_gap) == 0

    product_generator = sp.kronecker_product(
        bd["trace_generator"], sp.eye(db["trace_generator"].rows)
    ) + sp.kronecker_product(
        sp.eye(bd["trace_generator"].rows), db["trace_generator"]
    )
    product_law = sp.kronecker_product(pi_b, pi_d)
    assert product_law * product_generator == sp.zeros(1, product_generator.cols)


def first_level_obstruction_audit() -> None:
    r = sp.symbols("r", positive=True)
    p = (r - 1) / r
    excess = sp.factor(sp.Rational(3, 8) - p)
    assert sp.factor(excess - (8 - 5 * r) / (8 * r)) == 0
    # The isolating interval for R_hyb is contained in (3/2,151/100), and
    # the numerator is still positive at its upper endpoint.
    assert 8 - 5 * sp.Rational(151, 100) > 0
    limiting_target = sp.factor(r**3 * excess**2)
    assert limiting_target != 0
    assert sp.limit(limiting_target, r, sp.Rational(3, 2), dir="+") > 0


def main() -> None:
    hole_identity_audit()
    bd = exact_chain_audit("Bd")
    db = exact_chain_audit("dB")
    minimal_product_algebra(bd, db)
    first_level_obstruction_audit()
    print("PASS: exact dB hole-deficit identity")
    print("PASS: exact minimal-product excursion homogenization")
    print("PASS: exact two-copy singleton/doubleton Schur trace")
    print("PASS: exact rank-three obstruction to first-level proof")
    print("OPEN: minimal product excursion repayment inequality")


if __name__ == "__main__":
    main()
