#!/usr/bin/env python3
"""Exact diagnostic for two OPEN r=2 module invariants.

Passing this finite rational library is not a universal proof.  Every forward
absorbing equation is nevertheless built directly from dB updating and solved
over Q with FLINT.
"""

from __future__ import annotations

from itertools import combinations

import networkx as nx
from flint import arb, fmpq, fmpq_mat


def fixation_singletons(weights, fitness):
    order = len(weights)
    full = (1 << order) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    matrix = fmpq_mat(len(states), len(states))
    rhs = fmpq_mat(len(states), 1)
    for state, row in index.items():
        changes = []
        for target in range(order):
            mutant_mass = sum(
                (
                    weights[parent][target]
                    for parent in range(order)
                    if (state >> parent) & 1
                ),
                fmpq(0),
            )
            resident_mass = sum(
                (
                    weights[parent][target]
                    for parent in range(order)
                    if not ((state >> parent) & 1)
                ),
                fmpq(0),
            )
            denominator = fitness * mutant_mass + resident_mass
            assert denominator > 0
            if (state >> target) & 1:
                rate = resident_mass / denominator
                target_state = state & ~(1 << target)
            else:
                rate = fitness * mutant_mass / denominator
                target_state = state | (1 << target)
            if rate:
                changes.append((target_state, rate))
        changing = sum((rate for _, rate in changes), fmpq(0))
        assert changing > 0
        matrix[row, row] = 1
        for target_state, rate in changes:
            probability = rate / changing
            if target_state == full:
                rhs[row, 0] += probability
            elif target_state:
                matrix[row, index[target_state]] -= probability
    solution = matrix.solve(rhs)
    assert matrix * solution == rhs
    return [solution[index[1 << vertex], 0] for vertex in range(order)]


def check_invariants(weights):
    order = len(weights)
    degrees = [sum(row, fmpq(0)) for row in weights]
    assert all(degree > 0 for degree in degrees)
    alpha = fixation_singletons(weights, fmpq(2))
    beta = fixation_singletons(weights, fmpq(1, 2))
    mass = sum(alpha, fmpq(0))
    first_margin = fmpq(order) - 2 * mass
    assert first_margin >= 0
    weighted_alpha = sum(
        (value / degree for value, degree in zip(alpha, degrees)), fmpq(0)
    )
    weighted_beta = sum(
        (value / degree for value, degree in zip(beta, degrees)), fmpq(0)
    )
    denominator = 2 * mass - order + 1
    second_margin = None
    if denominator > 0:
        second_margin = mass * weighted_beta - denominator * weighted_alpha
        assert second_margin >= 0
    return first_margin, second_margin


def atlas_weights(graph, graph_index, pattern):
    order = len(graph)
    weights = [[fmpq(0) for _ in range(order)] for _ in range(order)]
    edge_number = 0
    for left in range(order):
        for right in range(left + 1, order):
            if not graph.has_edge(left, right):
                continue
            if pattern == 0:
                value = 1
            elif pattern == 1:
                value = 1 + ((left + 2) * (right + 3) * (graph_index + 5)) % 17
            elif pattern == 2:
                value = 3**edge_number
            else:
                raise ValueError(pattern)
            weights[left][right] = weights[right][left] = fmpq(value)
            edge_number += 1
    return weights


def complete_rational_weights(order, seed):
    weights = [[fmpq(0) for _ in range(order)] for _ in range(order)]
    for edge, (left, right) in enumerate(combinations(range(order), 2)):
        numerator = 1 + ((left + 3) * (right + 5) * (seed + 7) + edge**2) % 23
        denominator = 1 + ((left + 1) * (right + 2) + seed + edge) % 7
        value = fmpq(numerator, denominator)
        weights[left][right] = weights[right][left] = value
    return weights


def main():
    records = []
    for graph_index, graph in enumerate(nx.graph_atlas_g()):
        order = len(graph)
        if not (2 <= order <= 6) or not nx.is_connected(graph):
            continue
        patterns = range(3) if order <= 5 else range(1)
        for pattern in patterns:
            records.append(
                check_invariants(atlas_weights(graph, graph_index, pattern))
            )

    for order in range(3, 7):
        for seed in range(1, 13):
            records.append(check_invariants(complete_rational_weights(order, seed)))

    first_margins = [first for first, _ in records]
    second_margins = [second for _, second in records if second is not None]
    assert second_margins
    print(f"PASS: {len(records)} exact rational module graphs")
    print(
        "PASS OPEN (M1) finite audit; minimum margin",
        f"{float(arb(min(first_margins))):.12g}",
    )
    print(
        f"PASS OPEN (M2) finite audit on {len(second_margins)} applicable graphs;",
        "minimum margin",
        f"{float(arb(min(second_margins))):.12g}",
    )

    # Exact falsification of a tempting graph-independent reciprocal-fitness
    # ratio.  This is independent of the open invariant assertions above.
    triangle = [
        [fmpq(0), fmpq(1), fmpq(2)],
        [fmpq(1), fmpq(0), fmpq(3)],
        [fmpq(2), fmpq(3), fmpq(0)],
    ]
    alpha = fixation_singletons(triangle, fmpq(2))
    beta = fixation_singletons(triangle, fmpq(1, 2))
    rho_two = sum(alpha, fmpq(0)) / 3
    rho_half = sum(beta, fmpq(0)) / 3
    assert rho_two == fmpq(18764, 43223)
    assert rho_half == fmpq(30154, 129669)
    assert rho_two / rho_half == fmpq(28146, 15077) != 2
    degrees = [fmpq(3), fmpq(4), fmpq(5)]
    weighted_alpha = sum(
        (value / degree for value, degree in zip(alpha, degrees)), fmpq(0)
    )
    weighted_beta = sum(
        (value / degree for value, degree in zip(beta, degrees)), fmpq(0)
    )
    assert weighted_alpha / weighted_beta == fmpq(428540, 222057) != 2
    print("PASS: exact reciprocal-fitness ratio counterexample")


if __name__ == "__main__":
    main()
