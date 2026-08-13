#!/usr/bin/env python3
"""Exact hostile audit of the rank-three renewal reduction.

This script deliberately checks identities only.  It does not screen graphs
or claim the open rank-three excursion repayment inequality.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


OBSTRUCTION = (
    Path(__file__).resolve().parents[2]
    / "phase4_landmark_closure"
    / "obstruction"
)
sys.path.insert(0, str(OBSTRUCTION))

from verify_exact_duals import dual_generator, stationary  # noqa: E402


def row(values) -> sp.Matrix:
    return sp.Matrix(1, len(values), values)


def col(values) -> sp.Matrix:
    return sp.Matrix(len(values), 1, values)


def k2_boundary_audit() -> None:
    """Check the low-only boundary and every BDM source normalization."""
    r = sp.symbols("r", positive=True)
    bd_generator = sp.Matrix(
        [
            [-r, 1, r - 1],
            [1, -r, r - 1],
            [1, 1, -2],
        ]
    )
    bd_law = row([1 / (r + 1), 1 / (r + 1), (r - 1) / (r + 1)])
    db_generator = sp.Matrix([[-1, 1], [1, -1]])
    db_law = row([sp.Rational(1, 2), sp.Rational(1, 2)])
    assert bd_generator * sp.ones(3, 1) == sp.zeros(3, 1)
    assert db_generator * sp.ones(2, 1) == sp.zeros(2, 1)
    assert sp.simplify(bd_law * bd_generator) == sp.zeros(1, 3)
    assert db_law * db_generator == sp.zeros(1, 2)
    assert sp.factor(sum(bd_law) - 1) == 0
    assert sum(db_law) == 1

    # Every positive portal law gives the same weighted singleton atom by
    # symmetry.  The mean-rank normalizations agree with the bounded-module
    # variables a and b.
    x_1, x_2 = sp.symbols("x_1 x_2", positive=True)
    gamma = [x_1 / (x_1 + x_2), x_2 / (x_1 + x_2)]
    # Both K2 degrees are one, so the dB degree-reweighted portal law is the
    # same gamma.  Check the source averages before simplifying them.
    q_b = sp.factor(sum(gamma[i] * bd_law[i] for i in range(2)))
    q_d = sp.factor(sum(gamma[i] * db_law[i] for i in range(2)))
    assert sp.factor(q_b - 1 / (r + 1)) == 0
    assert sp.factor(q_d - sp.Rational(1, 2)) == 0
    m_b = sp.factor(sum(bd_law[i] * (1, 1, 2)[i] for i in range(3)))
    m_d = sp.Integer(1)
    b = sp.factor(m_b / 2)
    a = sp.factor(m_d / (2 * (r - 1)))
    assert sp.factor(b - r / (r + 1)) == 0
    assert sp.factor(a - 1 / (2 * (r - 1))) == 0

    constant = r * (r - 1) ** 2
    big_k = sp.factor(constant / (q_b * q_d))
    assert big_k == 2 * r * (r - 1) ** 2 * (r + 1)
    middle = sp.factor(big_k * (r * b + r * a - r) - r)
    discriminant = sp.factor(
        middle**2 - 4 * (r - r * b) * big_k * (r - r * a)
    )
    hybrid = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    assert sp.factor(discriminant - r**2 * hybrid) == 0


def exact_chain_audit(rule: str):
    # A nonregular path makes every orientation and degree factor visible.
    weights = (
        (0, 1, 0, 0),
        (1, 0, 2, 0),
        (0, 2, 0, 3),
        (0, 0, 3, 0),
    )
    r = sp.Rational(3, 2)
    order = len(weights)
    full = (1 << order) - 1
    full_generator = dual_generator(weights, r, rule)
    full_stationary = stationary(full_generator)

    # The loopless dB full state has no incoming transition and zero
    # stationary mass.  Bd uses every nonempty state.
    states = list(range(1, full + 1 if rule == "Bd" else full))
    positions = {state: place for place, state in enumerate(states)}
    indices = [state - 1 for state in states]
    generator = full_generator.extract(indices, indices)
    invariant = row([full_stationary[state - 1] for state in states])
    assert sp.factor(sum(invariant) - 1) == 0
    assert invariant * generator == sp.zeros(1, len(states))

    low_states = [state for state in states if state.bit_count() <= 2]
    high_states = [state for state in states if state.bit_count() >= 3]
    low = [positions[state] for state in low_states]
    high = [positions[state] for state in high_states]
    qmm = generator.extract(low, low)
    qmp = generator.extract(low, high)
    qpm = generator.extract(high, low)
    qpp = generator.extract(high, high)
    pi_m = invariant.extract([0], low)
    pi_p = invariant.extract([0], high)

    eta = pi_p * qpm
    xi = pi_m * qmp
    g_m = (-qmm).inv()
    g_p = (-qpp).inv()
    assert pi_m == eta * g_m
    assert pi_p == xi * g_p

    one_m = sp.ones(len(low), 1)
    one_p = sp.ones(len(high), 1)
    current = sp.factor((eta * one_m)[0])
    assert current > 0
    assert sp.factor(current - (xi * one_p)[0]) == 0

    nu_m = eta / current
    nu_p = xi / current
    exit_m = g_m * qmp
    exit_p = g_p * qpm
    assert exit_m * one_p == one_m
    assert exit_p * one_m == one_p
    assert nu_m * exit_m == nu_p
    assert nu_p * exit_p == nu_m
    assert nu_m * exit_m * exit_p == nu_m

    # Check the explicit triple-to-doubleton current.  These formulae are
    # reconstructed from P rather than read from the generator block.
    degree = [sum(map(sp.Rational, weights[i])) for i in range(order)]
    transition = [
        [sp.Rational(weights[i][j], degree[i]) for j in range(order)]
        for i in range(order)
    ]
    pi_by_state = {
        state: full_stationary[state - 1] for state in range(1, full + 1)
    }
    for place, state in enumerate(low_states):
        if state.bit_count() == 1:
            assert eta[place] == 0
            continue
        expected = sp.Integer(0)
        members = [i for i in range(order) if (state >> i) & 1]
        for k in range(order):
            if (state >> k) & 1:
                continue
            triple = state | (1 << k)
            if rule == "Bd":
                down = sum((transition[u][k] for u in members), sp.Integer(0))
            else:
                x = sum((transition[k][u] for u in members), sp.Integer(0))
                down = sp.factor(x / (r - (r - 1) * x))
            expected += pi_by_state[triple] * down
        assert sp.factor(eta[place] - expected) == 0

    # Refine the low block into ranks one and two and verify the exact Schur
    # repayment missing from singleton stationarity.
    rank_one = [i for i, state in enumerate(low_states) if state.bit_count() == 1]
    rank_two = [i for i, state in enumerate(low_states) if state.bit_count() == 2]
    killed = -qmm
    m11 = killed.extract(rank_one, rank_one)
    m12 = killed.extract(rank_one, rank_two)
    m21 = killed.extract(rank_two, rank_one)
    m22 = killed.extract(rank_two, rank_two)
    singleton = pi_m.extract([0], rank_one)
    doubleton = pi_m.extract([0], rank_two)
    eta_two = eta.extract([0], rank_two)
    assert singleton * m11 + doubleton * m21 == sp.zeros(1, len(rank_one))
    assert singleton * m12 + doubleton * m22 == eta_two
    schur = m22 - m21 * m11.inv() * m12
    replay_doubleton = eta_two * schur.inv()
    replay_singleton = -replay_doubleton * m21 * m11.inv()
    assert replay_doubleton == doubleton
    assert replay_singleton == singleton
    assert all(value >= 0 for value in schur.inv())
    assert all(value >= 0 for value in -m21 * m11.inv())

    # Portal rewards use a deliberately nonuniform load.  The dB portal law
    # carries the exact inverse-degree reweighting.
    load = [sp.Rational(value) for value in (1, 2, 3, 4)]
    if rule == "Bd":
        portal = [value / sum(load) for value in load]
    else:
        raw = [load[i] / degree[i] for i in range(order)]
        portal = [value / sum(raw) for value in raw]
    singleton_reward = col(
        [
            portal[state.bit_length() - 1] if state.bit_count() == 1 else 0
            for state in low_states
        ]
    )
    rank_m = col([state.bit_count() for state in low_states])
    rank_p = col([state.bit_count() for state in high_states])

    t_m = sp.factor((nu_m * g_m * one_m)[0])
    t_p = sp.factor((nu_p * g_p * one_p)[0])
    total_time = sp.factor(t_m + t_p)
    m_m = sp.factor((nu_m * g_m * rank_m)[0])
    m_p = sp.factor((nu_p * g_p * rank_p)[0])
    total_rank = sp.factor(m_m + m_p)
    singleton_time = sp.factor((nu_m * g_m * singleton_reward)[0])

    direct_mean = sp.factor(
        sum(
            invariant[place] * state.bit_count()
            for place, state in enumerate(states)
        )
    )
    direct_singleton = sp.factor(
        sum(
            invariant[positions[1 << i]] * portal[i]
            for i in range(order)
        )
    )
    assert sp.factor(current * total_time - 1) == 0
    assert sp.factor(current * total_rank - direct_mean) == 0
    assert sp.factor(current * singleton_time - direct_singleton) == 0
    assert sp.factor(total_rank / total_time - direct_mean) == 0
    assert sp.factor(singleton_time / total_time - direct_singleton) == 0

    # Exact stochastic Schur trace and its Green-corrected rewards.
    trace_generator = qmm + qmp * g_p * qpm
    assert trace_generator * one_m == sp.zeros(len(low), 1)
    assert pi_m * trace_generator == sp.zeros(1, len(low))
    assert all(
        trace_generator[i, j] >= 0
        for i in range(len(low))
        for j in range(len(low))
        if i != j
    )
    trace_time = one_m + qmp * g_p * one_p
    trace_rank = rank_m + qmp * g_p * rank_p
    assert sp.factor((pi_m * trace_time)[0] - 1) == 0
    assert sp.factor((pi_m * trace_rank)[0] - direct_mean) == 0
    assert sp.factor((pi_m * singleton_reward)[0] - direct_singleton) == 0

    return {
        "r": r,
        "s": sp.Integer(order),
        "T": total_time,
        "M": total_rank,
        "S": singleton_time,
        "m": direct_mean,
        "q": direct_singleton,
        "pi_low": pi_m,
        "trace_generator": trace_generator,
        "trace_time": trace_time,
        "trace_rank": trace_rank,
        "trace_singleton": singleton_reward,
    }


def cycle_algebra(bd, db) -> None:
    r, order = bd["r"], bd["s"]
    assert db["r"] == r and db["s"] == order
    a_cycle = sp.factor(db["M"] / (order * (r - 1)))
    b_cycle = sp.factor(bd["M"] / order)
    a = sp.factor(db["m"] / (order * (r - 1)))
    b = sp.factor(bd["m"] / order)
    assert sp.factor(a - a_cycle / db["T"]) == 0
    assert sp.factor(b - b_cycle / bd["T"]) == 0
    assert sp.factor(bd["q"] - bd["S"] / bd["T"]) == 0
    assert sp.factor(db["q"] - db["S"] / db["T"]) == 0

    # Check the homogenization underlying RTER without relying on radical
    # simplification or on either sign branch.
    assert sp.factor(bd["T"] * db["T"] * a * b - a_cycle * b_cycle) == 0
    assert sp.factor(
        bd["T"] * db["T"] * (1 - a) * (1 - b)
        - (db["T"] - a_cycle) * (bd["T"] - b_cycle)
    ) == 0

    # Check the exact product-chain quadratic in cycle coordinates at a
    # nontrivial rational z.  No sign is asserted.
    z = sp.Rational(7, 5)
    constant = r * (r - 1) ** 2
    direct_gap = sp.factor(
        constant * ((1 + z) * (1 - a) - z * b)
        + z * bd["q"] * db["q"] * (1 + z * (1 - b))
    )
    cycle_gap = sp.factor(
        constant
        * bd["T"]
        * (
            (1 + z) * bd["T"] * (db["T"] - a_cycle)
            - z * b_cycle * db["T"]
        )
        + z
        * bd["S"]
        * db["S"]
        * ((1 + z) * bd["T"] - z * b_cycle)
    )
    assert sp.factor(cycle_gap - bd["T"] ** 2 * db["T"] * direct_gap) == 0

    # Check the mean of the fully traced three-copy forcing.  Factorization
    # avoids ever constructing the 1000-by-1000 product generator.
    pi_b, pi_d = bd["pi_low"], db["pi_low"]
    tau_b, tau_d = bd["trace_time"], db["trace_time"]
    kap_b, kap_d = bd["trace_rank"], db["trace_rank"]
    sing_b, sing_d = bd["trace_singleton"], db["trace_singleton"]
    eb_tau = sp.factor((pi_b * tau_b)[0])
    ed_tau = sp.factor((pi_d * tau_d)[0])
    eb_kap = sp.factor((pi_b * kap_b)[0])
    ed_kap = sp.factor((pi_d * kap_d)[0])
    eb_sing = sp.factor((pi_b * sing_b)[0])
    ed_sing = sp.factor((pi_d * sing_d)[0])
    traced_mean = sp.factor(
        constant
        * (1 + z)
        * eb_tau**2
        * (ed_tau - ed_kap / (order * (r - 1)))
        - constant * z * eb_tau * eb_kap * ed_tau / order
        + z
        * eb_sing
        * ed_sing
        * ((1 + z) * eb_tau - z * eb_kap / order)
    )
    assert sp.factor(traced_mean - direct_gap) == 0


def main() -> None:
    k2_boundary_audit()
    bd = exact_chain_audit("Bd")
    db = exact_chain_audit("dB")
    cycle_algebra(bd, db)
    print("PASS: exact K2 low-only boundary and BDM source normalization")
    print("PASS: exact triple-to-doubleton entrance currents")
    print("PASS: exact rank-two Schur repayment")
    print("PASS: exact alternating-excursion Palm laws")
    print("PASS: exact cycle rewards and product-chain homogenization")
    print("PASS: exact low-sector trace of the three-copy forcing")
    print("OPEN: rank-three excursion repayment inequality at R_hyb")


if __name__ == "__main__":
    main()
