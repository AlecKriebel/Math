#!/usr/bin/env python3
"""Exact replay of the paired root-tree/operator reduction.

This script checks identities on one nonregular rational weighted four-path.
It does not assert the open paired root-tree sign.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OBSTRUCTION = HERE.parents[1] / "phase4_landmark_closure" / "obstruction"
sys.path.insert(0, str(OBSTRUCTION))

from verify_exact_duals import (  # noqa: E402
    dual_generator,
    local_sample_kernels,
    reversed_arrow_generator,
    stationary,
)


WEIGHTS = (
    (0, 1, 0, 0),
    (1, 0, 2, 0),
    (0, 2, 0, 3),
    (0, 0, 3, 0),
)
FITNESS = sp.Rational(3, 2)


def row(values) -> sp.Matrix:
    return sp.Matrix(1, len(values), values)


def diagonal_cofactors(matrix: sp.Matrix) -> list[sp.Expr]:
    return [
        sp.factor(matrix.minor_submatrix(i, i).det())
        for i in range(matrix.rows)
    ]


def recurrent_data(rule: str):
    order = len(WEIGHTS)
    full = (1 << order) - 1
    ambient = dual_generator(WEIGHTS, FITNESS, rule)
    ambient_law = stationary(ambient)
    states = list(range(1, full + 1 if rule == "Bd" else full))
    indices = [state - 1 for state in states]
    generator = ambient.extract(indices, indices)
    invariant = row([ambient_law[state - 1] for state in states])
    assert invariant * generator == sp.zeros(1, len(states))
    assert sp.factor(sum(invariant) - 1) == 0

    tree = diagonal_cofactors(-generator)
    assert all(value > 0 for value in tree)
    partition = sp.factor(sum(tree))
    tree_law = row([sp.factor(value / partition) for value in tree])
    assert tree_law == invariant

    p = (FITNESS - 1) / FITNESS
    excess_mark = sp.Matrix(
        [sp.Rational(state.bit_count(), order) - p for state in states]
    )
    singleton_indices = [
        i for i, state in enumerate(states) if state.bit_count() == 1
    ]
    rest_indices = [
        i for i, state in enumerate(states) if state.bit_count() >= 2
    ]
    load = [sp.Rational(value) for value in (1, 2, 3, 4)]
    degree = [sum(map(sp.Rational, row_)) for row_ in WEIGHTS]
    if rule == "Bd":
        portal = [value / sum(load) for value in load]
    else:
        raw = [load[i] / degree[i] for i in range(order)]
        portal = [value / sum(raw) for value in raw]
    portal_mark = sp.zeros(len(states), 1)
    for place in singleton_indices:
        vertex = states[place].bit_length() - 1
        portal_mark[place] = portal[vertex]

    tree_row = row(tree)
    tree_excess = sp.factor((tree_row * excess_mark)[0])
    tree_portal = sp.factor((tree_row * portal_mark)[0])
    stationary_excess = sp.factor((invariant * excess_mark)[0])
    stationary_portal = sp.factor((invariant * portal_mark)[0])
    assert sp.factor(stationary_excess - tree_excess / partition) == 0
    assert sp.factor(stationary_portal - tree_portal / partition) == 0

    # The diagonal derivative of det(-Q+t diag(h)) is its cofactor pairing.
    # Check it independently on every coordinate mark and then by linearity.
    for i in range(len(states)):
        coordinate = sp.zeros(len(states), 1)
        coordinate[i] = 1
        derivative = (-generator).minor_submatrix(i, i).det()
        assert sp.factor(derivative - (tree_row * coordinate)[0]) == 0

    q_ss = generator.extract(singleton_indices, singleton_indices)
    q_sr = generator.extract(singleton_indices, rest_indices)
    q_rs = generator.extract(rest_indices, singleton_indices)
    q_rr = generator.extract(rest_indices, rest_indices)
    green = (-q_rr).inv()
    trace = q_ss + q_sr * green * q_rs
    g_singleton = excess_mark.extract(singleton_indices, [0])
    g_rest = excess_mark.extract(rest_indices, [0])
    phi = g_singleton + q_sr * green * g_rest

    psi = sp.zeros(len(states), 1)
    psi_rest = green * g_rest
    for local, global_index in enumerate(rest_indices):
        psi[global_index] = psi_rest[local]
    gauged = excess_mark + generator * psi
    assert gauged.extract(singleton_indices, [0]) == phi
    assert gauged.extract(rest_indices, [0]) == sp.zeros(len(rest_indices), 1)
    assert sp.factor((tree_row * generator * psi)[0]) == 0
    assert sp.factor((tree_row * gauged)[0] - tree_excess) == 0

    trace_tree = diagonal_cofactors(-trace)
    rest_determinant = sp.factor((-q_rr).det())
    for local, global_index in enumerate(singleton_indices):
        assert sp.factor(
            tree[global_index] - rest_determinant * trace_tree[local]
        ) == 0
    assert sp.factor(
        sum(
            tree[global_index] * phi[local]
            for local, global_index in enumerate(singleton_indices)
        )
        - tree_excess
    ) == 0

    return {
        "states": states,
        "generator": generator,
        "tree": tree,
        "partition": partition,
        "tree_excess": tree_excess,
        "tree_portal": tree_portal,
        "stationary_excess": stationary_excess,
        "stationary_portal": stationary_portal,
    }


def paired_tree_cancellation_audit(bd, db) -> None:
    raw_gap = sp.factor(
        bd["stationary_portal"] * db["stationary_portal"]
        - FITNESS**3 * bd["stationary_excess"] * db["stationary_excess"]
    )
    tree_gap = sp.factor(
        bd["tree_portal"] * db["tree_portal"]
        - FITNESS**3 * bd["tree_excess"] * db["tree_excess"]
    )
    assert sp.factor(
        tree_gap - bd["partition"] * db["partition"] * raw_gap
    ) == 0

    # The Lagrange orientation square, written with generic square roots as
    # independent variables, is a polynomial identity.
    x = sp.symbols("x0:4", real=True)
    y = sp.symbols("y0:4", real=True)
    square = sp.Rational(1, 2) * sum(
        (x[i] * y[j] - x[j] * y[i]) ** 2
        for i in range(4)
        for j in range(4)
    )
    determinant = sum(value**2 for value in x) * sum(
        value**2 for value in y
    ) - sum(x[i] * y[i] for i in range(4)) ** 2
    assert sp.expand(square - determinant) == 0


def weighted_adjoint_audit(bd) -> None:
    order = len(WEIGHTS)
    full = (1 << order) - 1
    left = dual_generator(WEIGHTS, FITNESS, "Bd")
    reverse = reversed_arrow_generator(WEIGHTS, FITNESS)
    reference = sp.diag(
        *[
            (FITNESS - 1) ** state.bit_count()
            for state in range(1, full + 1)
        ]
    )
    adjoint = reference.inv() * left.T * reference

    degree = [sum(map(sp.Rational, row_)) for row_ in WEIGHTS]
    transition = [
        [sp.Rational(WEIGHTS[i][j], degree[i]) for j in range(order)]
        for i in range(order)
    ]
    potential = []
    for state in range(1, full + 1):
        row_cut = sum(
            transition[i][j]
            for i in range(order)
            for j in range(order)
            if (state >> i) & 1 and not ((state >> j) & 1)
        )
        column_cut = sum(
            transition[j][i]
            for i in range(order)
            for j in range(order)
            if (state >> i) & 1 and not ((state >> j) & 1)
        )
        potential.append(sp.factor(FITNESS * (row_cut - column_cut)))
    schrodinger = reverse + sp.diag(*potential)
    assert adjoint == schrodinger

    # Every diagonally marked determinant is similarity invariant.  It is
    # enough to compare all diagonal cofactors, the coefficients linear in
    # an arbitrary mark.
    adjoint_tree = diagonal_cofactors(-schrodinger)
    assert adjoint_tree == bd["tree"]


def geometric_resolvent_audit(db) -> None:
    order = len(WEIGHTS)
    full = (1 << order) - 1
    identity = sp.eye(full)
    aggregate = sp.zeros(full, full)
    a = (FITNESS - 1) / FITNESS
    for target in range(order):
        selective, neutral, burst = local_sample_kernels(
            WEIGHTS, FITNESS, target
        )
        local_c = neutral - identity + (FITNESS - 1) * (
            selective - identity
        )
        resolvent = (identity - a * selective).inv()
        assert all(value >= 0 for value in resolvent)
        assert sp.simplify(
            burst - identity - resolvent * local_c / FITNESS
        ) == sp.zeros(full, full)
        aggregate += resolvent * local_c / FITNESS
    ambient_db = dual_generator(WEIGHTS, FITNESS, "dB")
    assert aggregate == ambient_db

    # Restricting away the transient full state recovers the recurrent
    # operator whose cofactors occur in PTR.
    proper = list(range(full - 1))
    assert aggregate.extract(proper, proper) == db["generator"]


def cut_envelope_audit() -> None:
    order = len(WEIGHTS)
    full = (1 << order) - 1
    degree = [sum(map(sp.Rational, row_)) for row_ in WEIGHTS]
    transition = [
        [sp.Rational(WEIGHTS[i][j], degree[i]) for j in range(order)]
        for i in range(order)
    ]
    odds = {}
    for state in range(1, full):
        row_cut = sum(
            transition[i][j]
            for i in range(order)
            for j in range(order)
            if (state >> i) & 1 and not ((state >> j) & 1)
        )
        column_cut = sum(
            transition[i][j]
            for i in range(order)
            for j in range(order)
            if not ((state >> i) & 1) and (state >> j) & 1
        )
        assert row_cut > 0 and column_cut > 0
        kappa = sp.factor(row_cut / column_cut)
        bd_odds = sp.factor(FITNESS * kappa)

        mutant_mass = [
            sum(
                transition[i][j]
                for j in range(order)
                if (state >> j) & 1
            )
            for i in range(order)
        ]
        db_up = FITNESS * sum(
            mutant_mass[i] / (1 + (FITNESS - 1) * mutant_mass[i])
            for i in range(order)
            if not ((state >> i) & 1)
        )
        db_down = sum(
            (1 - mutant_mass[i])
            / (1 + (FITNESS - 1) * mutant_mass[i])
            for i in range(order)
            if (state >> i) & 1
        )
        db_odds = sp.factor(db_up / db_down)
        assert db_odds <= FITNESS**2 / kappa
        odds[state] = (kappa, bd_odds, db_odds)

    for state_a, (kappa_a, bd_a, db_a) in odds.items():
        for state_b, (kappa_b, bd_b, db_b) in odds.items():
            assert bd_a * db_b <= FITNESS**3 * kappa_a / kappa_b
            assert (bd_a * db_b) * (bd_b * db_a) <= FITNESS**6


def main() -> None:
    bd = recurrent_data("Bd")
    db = recurrent_data("dB")
    paired_tree_cancellation_audit(bd, db)
    weighted_adjoint_audit(bd)
    geometric_resolvent_audit(db)
    cut_envelope_audit()
    print("PASS: root-tree cofactors and marked determinant derivatives")
    print("PASS: exact Poisson gauge and singleton Schur cofactor trace")
    print("PASS: exact cancellation to paired root-tree repayment")
    print("PASS: Bd marked determinant under weighted adjunction")
    print("PASS: dB positive targetwise resolvent sum")
    print("PASS: swapped two-copy cut-odds envelope")
    print("OPEN: paired root-tree operator inequality")


if __name__ == "__main__":
    main()
