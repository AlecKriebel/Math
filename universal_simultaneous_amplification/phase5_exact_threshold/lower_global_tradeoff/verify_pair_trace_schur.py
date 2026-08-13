#!/usr/bin/env python3
"""Exact rational replay for the neutral pair-chain Schur decomposition."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def pair_system(rule: str, weights: sp.Matrix):
    n = weights.rows
    degree = [sum(weights[i, j] for j in range(n)) for i in range(n)]
    rates = sp.zeros(n)
    for i in range(n):
        for j in range(n):
            rates[i, j] = (
                weights[i, j] / degree[j]
                if rule == "Bd"
                else weights[i, j] / degree[i]
            )

    exit_rate = [sum(rates[i, j] for j in range(n)) for i in range(n)]
    states = list(combinations(range(n), 2))
    index = {state: k for k, state in enumerate(states)}
    killed = sp.zeros(len(states))

    for row, (i, j) in enumerate(states):
        killed[row, row] = exit_rate[i] + exit_rate[j]
        for k in range(n):
            if k != j and rates[i, k]:
                killed[row, index[tuple(sorted((k, j)))]] -= rates[i, k]
            if k != i and rates[j, k]:
                killed[row, index[tuple(sorted((i, k)))]] -= rates[j, k]

    total_degree = sum(degree)
    harmonic_degree = sum(1 / value for value in degree)
    C = 1 / harmonic_degree
    load = sp.zeros(len(states), 1)
    for row, (i, j) in enumerate(states):
        if rule == "Bd":
            load[row] = 2 * C * weights[i, j] / (n * degree[i] * degree[j])
        else:
            load[row] = 2 * sum(
                weights[v, i] * weights[v, j] / degree[v]
                for v in range(n)
            ) / (n * total_degree)
    return states, index, killed, load


def check_rule(rule: str, weights: sp.Matrix) -> tuple[sp.Expr, sp.Expr]:
    states, index, killed, load = pair_system(rule, weights)
    full_h = killed.inv() * sp.ones(len(states), 1)
    full_coefficient = sp.factor((load.T * full_h)[0])

    local_indices = [index[(0, 1)], index[(3, 4)]]
    trace_indices = [k for k in range(len(states)) if k not in local_indices]
    L_AA = killed.extract(local_indices, local_indices)
    L_AB = killed.extract(local_indices, trace_indices)
    L_BA = killed.extract(trace_indices, local_indices)
    L_BB = killed.extract(trace_indices, trace_indices)

    green = L_AA.inv()
    local_time = green * sp.ones(len(local_indices), 1)
    exit_kernel = -green * L_AB
    trace_operator = L_BB - L_BA * green * L_AB
    trace_source = sp.ones(len(trace_indices), 1) - L_BA * local_time
    trace_h = trace_operator.inv() * trace_source
    local_h = local_time + exit_kernel * trace_h

    reconstructed = sp.zeros(len(states), 1)
    for row, state_index in enumerate(local_indices):
        reconstructed[state_index] = local_h[row]
    for row, state_index in enumerate(trace_indices):
        reconstructed[state_index] = trace_h[row]
    assert reconstructed == full_h
    assert all(entry >= 0 for entry in green)
    assert all(entry >= 0 for entry in local_time)
    assert all(entry >= 0 for entry in exit_kernel)
    assert all(entry > 0 for entry in trace_source)

    load_A = load.extract(local_indices, [0])
    load_B = load.extract(trace_indices, [0])
    local_coefficient = sp.factor((load_A.T * local_time)[0])
    decomposed = sp.factor(
        (
            load_A.T * local_time
            + (load_B.T + load_A.T * exit_kernel) * trace_h
        )[0]
    )
    assert decomposed == full_coefficient
    return full_coefficient, local_coefficient


def main() -> None:
    weights = sp.zeros(5)
    for i, value in enumerate((5, 1, 1, 5)):
        weights[i, i + 1] = weights[i + 1, i] = sp.Rational(value)

    bd, bd_local = check_rule("Bd", weights)
    db, db_local = check_rule("dB", weights)
    assert bd == sp.Rational(185012, 537055)
    assert db == sp.Rational(1397, 4655)
    assert bd_local == sp.Rational(12, 259)
    assert db_local == 0
    assert sp.factor(db - sp.Rational(3, 10)) == sp.Rational(1, 9310)

    print(f"Bd coefficient={bd}; local occupation={bd_local}")
    print(f"dB coefficient={db}; local occupation={db_local}")
    print("PASS exact pair-chain Schur reconstruction for both rules")
    print("PASS exact load decomposition and frozen weak dB excess")


if __name__ == "__main__":
    main()
