#!/usr/bin/env python3
"""Exact replay of the singleton-root Schur and Hellinger reductions.

The universal repayment sign remains open.  This script verifies the exact
linear-algebra reductions, the singleton balance identities underlying the
root-path comparison, and a few explicitly named hostile audits.  It does
not enumerate graphs or portal vectors.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OBSTRUCTION = HERE.parents[1] / "phase4_landmark_closure" / "obstruction"
sys.path.insert(0, str(OBSTRUCTION))

from verify_exact_duals import dual_generator, stationary  # noqa: E402


def row(entries) -> sp.Matrix:
    return sp.Matrix(1, len(entries), entries)


def transition_matrix(weights) -> tuple[sp.Matrix, list[sp.Expr]]:
    degree = [sum(map(sp.sympify, values), sp.Integer(0)) for values in weights]
    transition = sp.Matrix(
        [
            [sp.sympify(weights[i][j]) / degree[i] for j in range(len(weights))]
            for i in range(len(weights))
        ]
    )
    return transition, degree


def singleton_trace(weights, fitness, rule: str):
    """Return the direct and two-stage singleton Schur data."""
    order = len(weights)
    full = (1 << order) - 1
    ambient_generator = dual_generator(weights, fitness, rule)
    ambient_law = stationary(ambient_generator)
    states = list(range(1, full + 1 if rule == "Bd" else full))
    ambient_indices = [state - 1 for state in states]
    generator = ambient_generator.extract(ambient_indices, ambient_indices)
    invariant = row([ambient_law[state - 1] for state in states])
    state_index = {state: index for index, state in enumerate(states)}
    singleton = [state_index[1 << i] for i in range(order)]
    doubleton = [index for index, state in enumerate(states) if state.bit_count() == 2]
    high = [index for index, state in enumerate(states) if state.bit_count() >= 3]
    rest = doubleton + high

    q_ss = generator.extract(singleton, singleton)
    q_sr = generator.extract(singleton, rest)
    q_rs = generator.extract(rest, singleton)
    q_rr = generator.extract(rest, rest)
    green = (-q_rr).inv()

    p = (fitness - 1) / fitness
    reward = sp.Matrix(
        [sp.Rational(state.bit_count(), order) - p for state in states]
    )
    trace = q_ss + q_sr * green * q_rs
    trace_time = sp.ones(order, 1) + q_sr * green * sp.ones(len(rest), 1)
    trace_reward = reward.extract(singleton, [0]) + q_sr * green * reward.extract(rest, [0])

    atoms = invariant.extract([0], singleton)
    total = sp.factor(sum(atoms))
    law = atoms / total
    density = sp.factor(
        sum(invariant[0, index] * state.bit_count() for index, state in enumerate(states))
        / order
    )
    assert atoms * trace == sp.zeros(1, order)
    assert sp.factor((atoms * trace_time)[0] - 1) == 0
    assert sp.factor((atoms * trace_reward)[0] - (density - p)) == 0

    # Associativity check: eliminate ranks >=3, then eliminate rank 2.
    low = singleton + doubleton
    q_ll = generator.extract(low, low)
    q_lh = generator.extract(low, high)
    q_hl = generator.extract(high, low)
    q_hh = generator.extract(high, high)
    high_green = (-q_hh).inv()
    first_trace = q_ll + q_lh * high_green * q_hl
    first_time = sp.ones(len(low), 1) + q_lh * high_green * sp.ones(len(high), 1)
    first_reward = reward.extract(low, [0]) + q_lh * high_green * reward.extract(high, [0])

    double_positions = list(range(order, len(low)))
    q_1ss = first_trace.extract(range(order), range(order))
    q_1sd = first_trace.extract(range(order), double_positions)
    q_1ds = first_trace.extract(double_positions, range(order))
    q_1dd = first_trace.extract(double_positions, double_positions)
    double_green = (-q_1dd).inv()
    second_trace = q_1ss + q_1sd * double_green * q_1ds
    second_time = first_time[:order, :] + q_1sd * double_green * first_time[order:, :]
    second_reward = first_reward[:order, :] + q_1sd * double_green * first_reward[order:, :]
    assert second_trace == trace
    assert second_time == trace_time
    assert second_reward == trace_reward

    return {
        "Q": generator,
        "pi": invariant,
        "state_index": state_index,
        "T": trace,
        "tau": trace_time,
        "phi": trace_reward,
        "u": atoms,
        "c": total,
        "lambda": law,
        "rho": density,
        "bar_phi": sp.factor((law * trace_reward)[0]),
        "p": p,
    }


def singleton_balance_audit(weights, fitness, bd, db) -> None:
    """Check the two exact root balances used in the path comparison."""
    order = len(weights)
    transition, _ = transition_matrix(weights)
    temperature = [sum(transition[j, i] for j in range(order)) for i in range(order)]
    hit = lambda value: value / (fitness - (fitness - 1) * value)

    for i in range(order):
        bd_rhs = sum(
            transition[i, j]
            * (
                bd["u"][0, j]
                + bd["pi"][0, bd["state_index"][(1 << i) | (1 << j)]]
            )
            for j in range(order)
            if j != i
        )
        assert sp.factor(fitness * temperature[i] * bd["u"][0, i] - bd_rhs) == 0

        db_rhs = sum(
            hit(transition[j, i])
            * (
                db["u"][0, j]
                + db["pi"][0, db["state_index"][(1 << i) | (1 << j)]]
            )
            for j in range(order)
            if j != i
        )
        assert sp.factor(db["u"][0, i] - db_rhs) == 0

    # These polynomial identities are the two only inequalities used after
    # multiplying the root balances: Cauchy and the doubleton rebate.
    aa, bb, cc, dd = sp.symbols("aa bb cc dd", nonnegative=True)
    assert sp.expand((aa**2 + bb**2) * (cc**2 + dd**2) - (aa * cc + bb * dd) ** 2) == sp.expand(
        (aa * dd - bb * cc) ** 2
    )


def root_green_bound(weights, fitness, bd, db):
    """Construct the exact kernel L, rebate beta, and Green lower bound."""
    order = len(weights)
    transition, degree = transition_matrix(weights)
    inverse_degree = [1 / value for value in degree]
    temperature = [sum(transition[j, i] for j in range(order)) for i in range(order)]
    kernel = sp.zeros(order, order)
    rebate = sp.zeros(order, 1)
    hellinger = sp.zeros(order, 1)

    for i in range(order):
        hellinger[i] = sp.sqrt(
            inverse_degree[i] * bd["lambda"][0, i] * db["lambda"][0, i]
        )
        for j in range(order):
            if not transition[i, j]:
                continue
            pair = (1 << i) | (1 << j)
            eta_b = bd["pi"][0, bd["state_index"][pair]] / bd["c"]
            eta_d = db["pi"][0, db["state_index"][pair]] / db["c"]
            delta = sp.sqrt(
                (bd["lambda"][0, j] + eta_b)
                * (db["lambda"][0, j] + eta_d)
            ) - sp.sqrt(bd["lambda"][0, j] * db["lambda"][0, j])
            geometric_hit = transition[j, i] / (
                fitness - (fitness - 1) * transition[j, i]
            )
            kernel[i, j] = transition[i, j] / (
                sp.sqrt(fitness * temperature[i])
                * sp.sqrt(fitness - (fitness - 1) * transition[j, i])
            )
            rebate[i] += (
                sp.sqrt(inverse_degree[i])
                / sp.sqrt(fitness * temperature[i])
                * sp.sqrt(transition[i, j] * geometric_hit)
                * delta
            )

    lower = (sp.eye(order) - kernel).inv() * rebate
    for i in range(order):
        superharmonic_gap = sp.simplify(
            hellinger[i] - (kernel * hellinger + rebate)[i]
        )
        green_gap = sp.simplify(hellinger[i] - lower[i])
        assert superharmonic_gap == 0 or float(sp.N(superharmonic_gap, 60)) > 0
        assert green_gap == 0 or float(sp.N(green_gap, 60)) > 0
    return kernel, rebate, lower, hellinger


def exact_p3_replay() -> None:
    weights = (
        (0, 1, 0),
        (1, 0, 1),
        (0, 1, 0),
    )
    fitness = sp.Rational(3, 2)
    bd = singleton_trace(weights, fitness, "Bd")
    db = singleton_trace(weights, fitness, "dB")
    singleton_balance_audit(weights, fitness, bd, db)
    _, _, green_lower, hellinger = root_green_bound(weights, fitness, bd, db)

    assert bd["T"] == sp.Matrix(
        [
            [-sp.Rational(5, 8), sp.Rational(7, 12), sp.Rational(1, 24)],
            [sp.Rational(4, 3), -sp.Rational(8, 3), sp.Rational(4, 3)],
            [sp.Rational(1, 24), sp.Rational(7, 12), -sp.Rational(5, 8)],
        ]
    )
    assert db["T"] == sp.Matrix(
        [
            [-1, 1, 0],
            [sp.Rational(3, 7), -sp.Rational(6, 7), sp.Rational(3, 7)],
            [0, 1, -1],
        ]
    )
    assert bd["lambda"] == row([16, 7, 16]) / 39
    assert db["lambda"] == row([3, 7, 3]) / 13
    assert bd["phi"] == sp.Matrix([10, 40, 10]) / 63
    assert db["phi"] == sp.Matrix([0, 2, 0]) / 21
    assert bd["bar_phi"] == sp.Rational(200, 819)
    assert db["bar_phi"] == sp.Rational(2, 39)
    assert all(sp.simplify(green_lower[i] - hellinger[i]) == 0 for i in range(3))

    q_zero = sp.factor(fitness**3 * bd["bar_phi"] * db["bar_phi"])
    assert q_zero == sp.Rational(50, 1183)
    # The leaf--centre pair is the only nonsymmetric portal pair.  Its
    # scaled quadratic is decreasing on [0,1], so its endpoint value is the
    # exact minimum.
    t = sp.symbols("t", real=True)
    gap = (4 * (1 - t) + 7 * t / sp.sqrt(6)) ** 2 - sp.Rational(50, 7) * (1 - t / 2)
    derivative_at_one = sp.simplify(sp.diff(gap, t).subs(t, 1))
    assert derivative_at_one < 0
    assert sp.diff(gap, t, 2) > 0
    assert sp.simplify(gap.subs(t, 1)) == sp.Rational(193, 42)


def hostile_p4_associativity() -> None:
    weights = (
        (0, 1, 0, 0),
        (1, 0, 2, 0),
        (0, 2, 0, 3),
        (0, 0, 3, 0),
    )
    fitness = sp.Rational(3, 2)
    bd = singleton_trace(weights, fitness, "Bd")
    db = singleton_trace(weights, fitness, "dB")
    singleton_balance_audit(weights, fitness, bd, db)
    root_green_bound(weights, fitness, bd, db)

    # Verify the normalized Schur cancellation and the exact SRR algebra
    # for arbitrary symbolic portal rows.
    gamma = row(sp.symbols("g0:4"))
    alpha = row(sp.symbols("a0:4"))
    raw_gap = sp.expand(
        (bd["u"] * gamma.T)[0] * (db["u"] * alpha.T)[0]
        - fitness**3 * (bd["rho"] - bd["p"]) * (db["rho"] - db["p"])
    )
    reduced_gap = sp.expand(
        bd["c"]
        * db["c"]
        * (
            (bd["lambda"] * gamma.T)[0] * (db["lambda"] * alpha.T)[0]
            - fitness**3 * bd["bar_phi"] * db["bar_phi"]
        )
    )
    assert sp.simplify(raw_gap - reduced_gap) == 0


def raw_entrywise_audit(weights) -> None:
    """Exact finite audit of the stronger raw coefficient inequality."""
    fitness = sp.Rational(3, 2)
    bd = singleton_trace(weights, fitness, "Bd")
    db = singleton_trace(weights, fitness, "dB")
    _, degree = transition_matrix(weights)
    excess_bd = sp.factor(bd["rho"] - bd["p"])
    excess_db = sp.factor(db["rho"] - db["p"])
    assert excess_bd > 0 and excess_db > 0
    target = sp.factor(fitness**3 * excess_bd * excess_db)
    inverse_degree = [1 / value for value in degree]
    for i in range(len(weights)):
        for j in range(len(weights)):
            coefficient = sp.factor(
                bd["u"][0, i] * inverse_degree[j] * db["u"][0, j]
                + bd["u"][0, j] * inverse_degree[i] * db["u"][0, i]
                - target * (inverse_degree[i] + inverse_degree[j])
            )
            assert coefficient > 0, (i, j, coefficient)


def main() -> None:
    exact_p3_replay()
    hostile_p4_associativity()
    raw_entrywise_audit(
        (
            (0, 1, 2, 4),
            (1, 0, 3, 5),
            (2, 3, 0, 7),
            (4, 5, 7, 0),
        )
    )
    raw_entrywise_audit(
        (
            (0, 7, 3, 17),
            (7, 0, 15, 6),
            (3, 15, 0, 5),
            (17, 6, 5, 0),
        )
    )
    print("PASS: direct and two-stage singleton Schur traces agree")
    print("PASS: root normalization, reward, and SRR cancellation identities")
    print("PASS: exact Bd/dB singleton balances and doubleton-rebate algebra")
    print("PASS: exact cross-rule Green lower bound (sharp on unweighted P3)")
    print("PASS: exact all-portal RHR certificate on unweighted P3")
    print("PASS: two named hostile order-four entrywise audits at r=3/2")
    print("OPEN: universal root-Hellinger/Green excursion repayment")


if __name__ == "__main__":
    main()
