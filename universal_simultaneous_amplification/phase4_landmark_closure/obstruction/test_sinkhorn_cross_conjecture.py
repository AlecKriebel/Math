#!/usr/bin/env python3
"""Exact finite diagnostic for the open symmetric-Sinkhorn cross inequalities.

For an undirected weighted graph W with degrees d_i, define

    T(W)_ij = W_ij / (d_i d_j).

The two inequalities tested here are

    rho_dB(W,r) + rho_Bd(T(W),r) <= rho_dB(K_n,r)+rho_Bd(K_n,r),
    rho_Bd(W,r) + rho_dB(T(W),r) <= rho_dB(K_n,r)+rho_Bd(K_n,r).

They are OPEN.  This program performs only a deterministic exact finite
screen; it must not be cited as a proof.  The absorbing generators themselves
are imported from the independently checked exact-dual verifier.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp

from verify_exact_duals import fixation_values, forward_generator


FITNESSES = (sp.Rational(3, 2), sp.Integer(2), sp.Integer(3))


def density(weights, fitness, rule):
    order = len(weights)
    values = fixation_values(forward_generator(weights, fitness, rule))
    return sp.cancel(sum(values[1 << i] for i in range(order)) / order)


def complete_baseline(order, fitness, rule):
    p = 1 - 1 / fitness
    if rule == "Bd":
        return sp.cancel(p / (1 - fitness ** (-order)))
    return sp.cancel(
        p * sp.Rational(order - 1, order)
        / (1 - fitness ** (1 - order))
    )


def transform(weights):
    order = len(weights)
    degree = [sum(map(sp.sympify, row), sp.Integer(0)) for row in weights]
    transformed = tuple(
        tuple(
            sp.Integer(0)
            if i == j
            else sp.cancel(sp.sympify(weights[i][j]) / (degree[i] * degree[j]))
            for j in range(order)
        )
        for i in range(order)
    )

    # The transition kernel of T(W) is exactly the normalized transpose Q.
    transition = [
        [sp.sympify(weights[i][j]) / degree[i] for j in range(order)]
        for i in range(order)
    ]
    temperature = [
        sum(transition[j][i] for j in range(order))
        for i in range(order)
    ]
    transformed_degree = [sum(row) for row in transformed]
    assert all(
        sp.cancel(transformed_degree[i] - temperature[i] / degree[i]) == 0
        for i in range(order)
    )
    for i in range(order):
        for j in range(order):
            actual = (
                transformed[i][j] / transformed_degree[i]
                if transformed_degree[i]
                else 0
            )
            expected = transition[j][i] / temperature[i]
            assert sp.cancel(actual - expected) == 0
    return transformed


def connected(adjacency):
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex] - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    return len(reached) == len(adjacency)


def small_graphs():
    for order in (3, 4):
        edges = list(combinations(range(order), 2))
        for support_mask in range(1, 1 << len(edges)):
            adjacency = [set() for _ in range(order)]
            for edge_index, (i, j) in enumerate(edges):
                if (support_mask >> edge_index) & 1:
                    adjacency[i].add(j)
                    adjacency[j].add(i)
            if not connected(adjacency):
                continue
            for pattern in range(3):
                weights = [
                    [sp.Integer(0) for _ in range(order)]
                    for _ in range(order)
                ]
                for edge_index, (i, j) in enumerate(edges):
                    if not ((support_mask >> edge_index) & 1):
                        continue
                    if pattern == 0:
                        value = sp.Integer(1)
                    elif pattern == 1:
                        value = sp.Integer(
                            1 + ((edge_index + 2) * (support_mask + 3)) % 13
                        )
                    else:
                        value = sp.Integer(5**edge_index)
                    weights[i][j] = weights[j][i] = value
                yield tuple(map(tuple, weights))


def five_vertex_graphs():
    order = 5
    for family in range(3):
        for seed in range(3):
            weights = [[sp.Integer(0) for _ in range(order)] for _ in range(order)]
            if family == 0:
                edges = [(i, i + 1) for i in range(order - 1)]
            elif family == 1:
                edges = [(0, i) for i in range(1, order)]
            else:
                edges = [(i, (i + 1) % order) for i in range(order)]
            for edge_index, (i, j) in enumerate(edges):
                value = sp.Integer(1 + ((edge_index + 2) * (seed + 3) ** 2) % 17)
                weights[i][j] = weights[j][i] = value
            yield tuple(map(tuple, weights))

    # Three deterministic chorded paths.
    for seed in range(3):
        weights = [[sp.Integer(0) for _ in range(order)] for _ in range(order)]
        edges = ((0, 1), (1, 2), (2, 3), (3, 4), (0, 2), (1, 4))
        for edge_index, (i, j) in enumerate(edges):
            value = sp.Integer(
                1 + ((edge_index + 3) * (seed + 5) + edge_index**2) % 19
            )
            weights[i][j] = weights[j][i] = value
        yield tuple(map(tuple, weights))


def main():
    graph_count = 0
    comparison_count = 0
    least_positive_gap = None
    for weights in (*small_graphs(), *five_vertex_graphs()):
        order = len(weights)
        transformed = transform(weights)
        for fitness in FITNESSES:
            benchmark = complete_baseline(
                order, fitness, "Bd"
            ) + complete_baseline(order, fitness, "dB")
            for first_rule, second_rule in (("dB", "Bd"), ("Bd", "dB")):
                gap = sp.cancel(
                    benchmark
                    - density(weights, fitness, first_rule)
                    - density(transformed, fitness, second_rule)
                )
                assert gap >= 0, (
                    order, fitness, first_rule, second_rule, gap, weights
                )
                if gap > 0 and (
                    least_positive_gap is None or gap < least_positive_gap
                ):
                    least_positive_gap = gap
                comparison_count += 1
        graph_count += 1

    print(
        "PASS: both OPEN Sinkhorn cross inequalities survived "
        f"{comparison_count} exact comparisons on {graph_count} rational graphs"
    )
    print(f"least strictly positive gap = {least_positive_gap}")


if __name__ == "__main__":
    main()
