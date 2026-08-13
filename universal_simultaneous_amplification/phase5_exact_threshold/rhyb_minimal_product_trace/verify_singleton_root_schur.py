#!/usr/bin/env python3
"""Exact replay for the singleton-root Schur and Cauchy reductions.

The script verifies reductions and the stated P3 obstruction.  It does not
assert the open universal singleton-root repayment inequality.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OBSTRUCTION = HERE.parents[1] / "phase4_landmark_closure" / "obstruction"
sys.path.insert(0, str(OBSTRUCTION))

from verify_exact_duals import dual_generator, stationary  # noqa: E402


def row(values) -> sp.Matrix:
    return sp.Matrix(1, len(values), values)


def singleton_trace(weights, fitness, rule: str):
    """Return the direct and rank-three-first singleton Schur data."""
    order = len(weights)
    full = (1 << order) - 1
    ambient_generator = dual_generator(weights, fitness, rule)
    ambient_law = stationary(ambient_generator)

    states = list(range(1, full + 1 if rule == "Bd" else full))
    ambient_indices = [state - 1 for state in states]
    generator = ambient_generator.extract(ambient_indices, ambient_indices)
    invariant = row([ambient_law[state - 1] for state in states])
    assert invariant * generator == sp.zeros(1, len(states))
    assert sp.factor(sum(invariant) - 1) == 0

    singleton = [i for i, state in enumerate(states) if state.bit_count() == 1]
    rest = [i for i, state in enumerate(states) if state.bit_count() >= 2]
    doubleton = [i for i, state in enumerate(states) if state.bit_count() == 2]
    high = [i for i, state in enumerate(states) if state.bit_count() >= 3]

    q_ss = generator.extract(singleton, singleton)
    q_sr = generator.extract(singleton, rest)
    q_rs = generator.extract(rest, singleton)
    q_rr = generator.extract(rest, rest)
    green_rest = (-q_rr).inv()
    direct_trace = q_ss + q_sr * green_rest * q_rs

    p = (fitness - 1) / fitness
    g_singleton = sp.Matrix(
        [sp.Rational(states[i].bit_count(), order) - p for i in singleton]
    )
    g_rest = sp.Matrix(
        [sp.Rational(states[i].bit_count(), order) - p for i in rest]
    )
    direct_time = (
        sp.ones(len(singleton), 1)
        + q_sr * green_rest * sp.ones(len(rest), 1)
    )
    direct_excess = g_singleton + q_sr * green_rest * g_rest

    singleton_law = invariant.extract([0], singleton)
    rest_law = invariant.extract([0], rest)
    assert rest_law == singleton_law * q_sr * green_rest
    assert singleton_law * direct_trace == sp.zeros(1, len(singleton))
    assert sp.factor((singleton_law * direct_time)[0] - 1) == 0

    density = sp.factor(
        sum(
            invariant[i] * sp.Rational(state.bit_count(), order)
            for i, state in enumerate(states)
        )
    )
    assert sp.factor((singleton_law * direct_excess)[0] - density + p) == 0

    # Associativity: eliminate ranks >=3, then eliminate rank 2.
    low = singleton + doubleton
    q_ll = generator.extract(low, low)
    g_low = sp.Matrix(
        [sp.Rational(states[i].bit_count(), order) - p for i in low]
    )
    one_low = sp.ones(len(low), 1)
    if high:
        q_lh = generator.extract(low, high)
        q_hl = generator.extract(high, low)
        q_hh = generator.extract(high, high)
        green_high = (-q_hh).inv()
        low_trace = q_ll + q_lh * green_high * q_hl
        high_reward = sp.Matrix(
            [sp.Rational(states[i].bit_count(), order) - p for i in high]
        )
        low_excess = g_low + q_lh * green_high * high_reward
        low_time = one_low + q_lh * green_high * sp.ones(len(high), 1)
    else:
        low_trace = q_ll
        low_excess = g_low
        low_time = one_low

    number_singletons = len(singleton)
    low_singletons = list(range(number_singletons))
    low_doubletons = list(range(number_singletons, len(low)))
    tt_ss = low_trace.extract(low_singletons, low_singletons)
    tt_sd = low_trace.extract(low_singletons, low_doubletons)
    tt_ds = low_trace.extract(low_doubletons, low_singletons)
    tt_dd = low_trace.extract(low_doubletons, low_doubletons)
    green_doubleton = (-tt_dd).inv()
    staged_trace = tt_ss + tt_sd * green_doubleton * tt_ds
    staged_excess = (
        low_excess.extract(low_singletons, [0])
        + tt_sd
        * green_doubleton
        * low_excess.extract(low_doubletons, [0])
    )
    staged_time = (
        low_time.extract(low_singletons, [0])
        + tt_sd * green_doubleton * low_time.extract(low_doubletons, [0])
    )

    assert staged_trace == direct_trace
    assert staged_excess == direct_excess
    assert staged_time == direct_time

    singleton_total = sp.factor(sum(singleton_law))
    root_law = singleton_law / singleton_total
    mean_excursion_excess = sp.factor((root_law * direct_excess)[0])
    assert sp.factor(
        density - p - singleton_total * mean_excursion_excess
    ) == 0

    degree = [sum(map(sp.Rational, weights[i])) for i in range(order)]
    return {
        "states": states,
        "generator": generator,
        "trace": direct_trace,
        "time": direct_time,
        "phi": direct_excess,
        "singleton": singleton_law,
        "singleton_total": singleton_total,
        "lambda": root_law,
        "bar_phi": mean_excursion_excess,
        "rho": density,
        "degree": degree,
    }


def hostile_four_path_audit() -> None:
    weights = (
        (0, 1, 0, 0),
        (1, 0, 2, 0),
        (0, 2, 0, 3),
        (0, 0, 3, 0),
    )
    fitness = sp.Rational(3, 2)
    load = [sp.Rational(value) for value in (1, 2, 3, 4)]
    bd = singleton_trace(weights, fitness, "Bd")
    db = singleton_trace(weights, fitness, "dB")

    gamma = sp.Matrix([value / sum(load) for value in load])
    db_raw = [load[i] / db["degree"][i] for i in range(len(load))]
    alpha = sp.Matrix([value / sum(db_raw) for value in db_raw])

    q_b = sp.factor((bd["singleton"] * gamma)[0])
    q_d = sp.factor((db["singleton"] * alpha)[0])
    p = (fitness - 1) / fitness
    raw_gap = sp.factor(
        q_b * q_d - fitness**3 * (bd["rho"] - p) * (db["rho"] - p)
    )
    normalized_gap = sp.factor(
        (bd["lambda"] * gamma)[0] * (db["lambda"] * alpha)[0]
        - fitness**3 * bd["bar_phi"] * db["bar_phi"]
    )
    assert sp.factor(
        raw_gap
        - bd["singleton_total"] * db["singleton_total"] * normalized_gap
    ) == 0


def generic_cauchy_audit() -> None:
    x = sp.symbols("x0:4", real=True)
    y = sp.symbols("y0:4", real=True)
    determinant = sp.Rational(1, 2) * sum(
        (x[i] * y[j] - x[j] * y[i]) ** 2
        for i in range(4)
        for j in range(4)
    )
    expected = sum(value**2 for value in x) * sum(
        value**2 for value in y
    ) - sum(x[i] * y[i] for i in range(4)) ** 2
    assert sp.expand(determinant - expected) == 0


def p3_obstruction_audit() -> None:
    weights = (
        (0, 1, 0),
        (1, 0, 1),
        (0, 1, 0),
    )
    fitness = sp.Rational(3, 2)
    bd = singleton_trace(weights, fitness, "Bd")
    db = singleton_trace(weights, fitness, "dB")

    expected_bd_trace = sp.Matrix(
        [
            [-sp.Rational(5, 8), sp.Rational(7, 12), sp.Rational(1, 24)],
            [sp.Rational(4, 3), -sp.Rational(8, 3), sp.Rational(4, 3)],
            [sp.Rational(1, 24), sp.Rational(7, 12), -sp.Rational(5, 8)],
        ]
    )
    expected_db_trace = sp.Matrix(
        [
            [-1, 1, 0],
            [sp.Rational(3, 7), -sp.Rational(6, 7), sp.Rational(3, 7)],
            [0, 1, -1],
        ]
    )
    assert bd["trace"] == expected_bd_trace
    assert db["trace"] == expected_db_trace
    assert bd["trace"][0, 2] == sp.Rational(1, 24)
    assert db["trace"][2, 0] == 0

    assert bd["lambda"] == row(
        [sp.Rational(16, 39), sp.Rational(7, 39), sp.Rational(16, 39)]
    )
    assert db["lambda"] == row(
        [sp.Rational(3, 13), sp.Rational(7, 13), sp.Rational(3, 13)]
    )
    assert bd["phi"] == sp.Matrix(
        [sp.Rational(10, 63), sp.Rational(40, 63), sp.Rational(10, 63)]
    )
    assert db["phi"] == sp.Matrix([0, sp.Rational(2, 21), 0])
    assert bd["bar_phi"] == sp.Rational(200, 819)
    assert db["bar_phi"] == sp.Rational(2, 39)
    root_target = sp.factor(
        fitness**3 * bd["bar_phi"] * db["bar_phi"]
    )
    assert root_target == sp.Rational(50, 1183)

    # Root-Hellinger pair test.  Leaves have identical (a,e), so only a
    # leaf--centre mixture is nontrivial.  The scaled quadratic is decreasing
    # on [0,1], and its endpoint minimum is positive.
    t = sp.symbols("t", real=True)
    delta = 7 / sp.sqrt(6) - 4
    scaled_gap = sp.expand((4 + delta * t) ** 2 - sp.Rational(50, 7) * (1 - t / 2))
    derivative = sp.diff(scaled_gap, t)
    assert sp.simplify(sp.diff(derivative, t) - 2 * delta**2) == 0
    endpoint_derivative = sp.simplify(derivative.subs(t, 1))
    assert endpoint_derivative == sp.Rational(418, 21) - 56 / sp.sqrt(6)
    # Both sides are positive, so squaring proves the strict sign.
    assert 418**2 * 6 < 1176**2
    assert sp.simplify(scaled_gap.subs(t, 1)) == sp.Rational(193, 42)

    # The exact same-state cut-odds envelope cannot be applied to the
    # independent two-copy trace: cross-state products already exceed r^3.
    # On P3, Bd at {L} has odds 3 and dB at {L,C} has odds 5/2.
    assert sp.Rational(3) * sp.Rational(5, 2) > fitness**3


def stored_entrywise_audit() -> None:
    """Exact audits on two stored hostile witnesses; not a class proof."""
    fitness = sp.Rational(3, 2)
    p = (fitness - 1) / fitness
    witnesses = (
        (
            (0, 1, 2, 4),
            (1, 0, 3, 5),
            (2, 3, 0, 7),
            (4, 5, 7, 0),
        ),
        (
            (0, 7, 3, 17),
            (7, 0, 15, 6),
            (3, 15, 0, 5),
            (17, 6, 5, 0),
        ),
    )
    for weights in witnesses:
        bd = singleton_trace(weights, fitness, "Bd")
        db = singleton_trace(weights, fitness, "dB")
        target = sp.factor(
            fitness**3
            * max(bd["rho"] - p, sp.Integer(0))
            * max(db["rho"] - p, sp.Integer(0))
        )
        order = len(weights)
        for i in range(order):
            for j in range(i, order):
                entry_gap = sp.factor(
                    bd["singleton"][i] * db["singleton"][j]
                    / db["degree"][j]
                    + bd["singleton"][j] * db["singleton"][i]
                    / db["degree"][i]
                    - target
                    * (
                        sp.Rational(1, db["degree"][i])
                        + sp.Rational(1, db["degree"][j])
                    )
                )
                assert entry_gap > 0


def main() -> None:
    hostile_four_path_audit()
    generic_cauchy_audit()
    p3_obstruction_audit()
    stored_entrywise_audit()
    print("PASS: direct singleton Schur trace and two-stage associativity")
    print("PASS: exact singleton-mass cancellation in the minimal product")
    print("PASS: exact root-law Cauchy determinant decomposition")
    print("PASS: P3 refutes a common-conductance cross-rule trace adjoint")
    print("PASS: P3 root-Hellinger repayment for every portal")
    print("PASS: finite entrywise audits on two stored witnesses at r=3/2")
    print("OPEN: universal singleton-root repayment inequality")


if __name__ == "__main__":
    main()
