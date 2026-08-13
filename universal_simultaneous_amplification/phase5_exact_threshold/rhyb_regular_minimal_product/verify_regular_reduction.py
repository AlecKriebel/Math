#!/usr/bin/env python3
"""Exact replay of the regular-module minimal-product reduction.

This verifier checks identities, one noncomplete regular rational K4, and
the rank-three pseudo-law obstruction.  It does not enumerate graphs and
does not assert the open universal vertexwise dB inequality.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OBSTRUCTION = HERE.parents[1] / "phase4_landmark_closure" / "obstruction"
sys.path.insert(0, str(OBSTRUCTION))

from verify_exact_duals import dual_generator, stationary  # noqa: E402


def recurrent_dB(weights, fitness):
    order = len(weights)
    full = (1 << order) - 1
    generator = dual_generator(weights, fitness, "dB")
    law = stationary(generator)
    return generator, law, range(1, full)


def symbolic_regular_reduction() -> None:
    r, z = sp.symbols("r z", positive=True)
    s = sp.symbols("s", integer=True, positive=True)
    singleton = (r - 1) / (r**s - 1)
    density = (r - 1) * r ** (s - 1) / (r**s - 1)
    p = (r - 1) / r
    assert sp.factor(density - p - singleton / r) == 0

    # Direct cancellation of the active MP expression.
    q_d, rho_d = sp.symbols("q_d rho_d", positive=True)
    raw_gap = singleton * q_d - r**3 * (density - p) * (rho_d - p)
    reduced_gap = singleton * (q_d - r**2 * (rho_d - p))
    assert sp.factor(raw_gap - reduced_gap) == 0


def exact_regular_k4_audit() -> None:
    # Every regular weighted K4 has opposite edge weights (a,b,c).  This
    # rational point is noncomplete and positive.
    a, b, c = sp.Rational(3, 5), sp.Rational(3, 10), sp.Rational(1, 10)
    weights = (
        (0, a, b, c),
        (a, 0, c, b),
        (b, c, 0, a),
        (c, b, a, 0),
    )
    fitness = sp.Rational(3, 2)
    order = len(weights)
    full = (1 << order) - 1

    # Directly verify the regular Bd product law.
    bd_law = stationary(dual_generator(weights, fitness, "Bd"))
    normalizer = fitness**order - 1
    expected_bd = [
        sp.factor((fitness - 1) ** state.bit_count() / normalizer)
        for state in range(1, full + 1)
    ]
    assert bd_law == expected_bd

    _, db_law, proper_states = recurrent_dB(weights, fitness)
    p = (fitness - 1) / fitness
    density = sp.factor(
        sum(db_law[state - 1] * state.bit_count() for state in proper_states)
        / order
    )
    singleton = [db_law[(1 << vertex) - 1] for vertex in range(order)]
    target = sp.factor(fitness**2 * max(density - p, 0))
    assert all(value - target > 0 for value in singleton)

    # Exact singleton entrance balance.
    transition = sp.Matrix(weights)  # degrees are all one
    hit = lambda value: value / (fitness - (fitness - 1) * value)
    for i in range(order):
        rhs = sum(
            hit(transition[j, i])
            * (
                singleton[j]
                + db_law[((1 << i) | (1 << j)) - 1]
            )
            for j in range(order)
            if j != i
        )
        assert sp.factor(singleton[i] - rhs) == 0

    # Exact hole identity.
    hit_matrix = sp.Matrix(
        order,
        order,
        lambda v, i: fitness * transition[v, i]
        / (1 + (fitness - 1) * transition[v, i]),
    )
    temperature = [sum(hit_matrix[v, i] for v in range(order)) for i in range(order)]
    sigma = sum(1 / (1 + temperature[i]) for i in range(order))
    mean_holes = sp.factor(order * (1 - density))
    mean_collision = sp.Integer(0)
    for state in proper_states:
        holes = [i for i in range(order) if not ((state >> i) & 1)]
        collision = sum(
            hit_matrix[v, i] / (1 + temperature[i])
            for i in holes
            for v in holes
        )
        mean_collision += db_law[state - 1] * collision
    assert sp.factor(mean_holes - sigma - mean_collision) == 0
    assert sp.factor(
        order * (density - p)
        - (sp.Rational(order, 1) / fitness - sigma - mean_collision)
    ) == 0


def rank_three_pseudolaw_obstruction() -> None:
    order = 8
    fitness = sp.Rational(3, 2)
    weights = tuple(
        tuple(0 if i == j else sp.Rational(1, order - 1) for j in range(order))
        for i in range(order)
    )
    _, genuine, proper_states = recurrent_dB(weights, fitness)
    epsilon = sp.Rational(1, 1000)

    pseudo = {state: sp.Integer(0) for state in proper_states}
    low_mass = sp.Integer(0)
    for state in proper_states:
        if state.bit_count() <= 2:
            pseudo[state] = epsilon * genuine[state - 1]
            low_mass += pseudo[state]
    rank_three = (1 << 0) | (1 << 1) | (1 << 2)
    pseudo[rank_three] += 1 - low_mass
    assert sum(pseudo.values()) == 1
    assert all(value >= 0 for value in pseudo.values())

    # Homogeneity preserves every singleton equation exactly.
    transition = sp.Matrix(weights)
    hit = lambda value: value / (fitness - (fitness - 1) * value)
    for i in range(order):
        lhs = pseudo[1 << i]
        rhs = sum(
            hit(transition[j, i])
            * (pseudo[1 << j] + pseudo[(1 << i) | (1 << j)])
            for j in range(order)
            if j != i
        )
        assert sp.factor(lhs - rhs) == 0

    density = sp.factor(
        sum(pseudo[state] * state.bit_count() for state in proper_states) / order
    )
    p = (fitness - 1) / fitness
    target = sp.factor(fitness**2 * (density - p))
    assert density > p
    assert all(pseudo[1 << i] < target for i in range(order))


def main() -> None:
    symbolic_regular_reduction()
    exact_regular_k4_audit()
    rank_three_pseudolaw_obstruction()
    print("PASS: regular Bd law and MP-to-vertexwise-dB equivalence")
    print("PASS: exact regular K4 singleton and hole identities")
    print("PASS: first-level-only proof exactly obstructed by rank-three pseudo-law")
    print("OPEN: universal regular vertexwise dB repayment")


if __name__ == "__main__":
    main()
