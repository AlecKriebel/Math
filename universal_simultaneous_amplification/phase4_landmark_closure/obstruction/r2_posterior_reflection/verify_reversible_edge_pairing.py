#!/usr/bin/env python3
"""Exact audit of the natural reversible original-edge pairing.

The whole weighted-reflection slack has an exact directed-edge expansion.
This verifier checks that expansion and certifies that pairing the two
orientations of each undirected edge does not give termwise positivity.
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
OBSTRUCTION = HERE.parent
CHI_DIR = OBSTRUCTION / "r2_entropy_certificate" / "chi_square_channel"
COLLISION_DIR = OBSTRUCTION / "r2_collision_closure"
sys.path.insert(0, str(CHI_DIR))
sys.path.insert(0, str(COLLISION_DIR))

from verify_resolvent_identities import solve  # noqa: E402
from verify_direct_flow_screen import connected, exhaustive_graphs  # noqa: E402
from verify_weighted_reflection import sharp_coefficient  # noqa: E402


def paired_edge_scores(weights):
    P, states, _, kernels, pi = solve(weights)
    n = len(P)
    full = 1 << n
    pi_all = [F(0) for _ in range(full)]
    for state, probability in zip(states, pi):
        pi_all[state] = probability

    nu = [[F(0) for _ in range(full)] for _ in range(n)]
    sigma = [[F(0) for _ in range(full)] for _ in range(n)]
    for v in range(n):
        for position, state in enumerate(states):
            if not ((state >> v) & 1):
                nu[v][state] = sum(
                    (pi[source] * kernels[v][source][position]
                     for source in range(len(states))),
                    F(0),
                ) - pi_all[state]
        for state in range(full):
            if not ((state >> v) & 1):
                sigma[v][state] = pi_all[state | (1 << v)]

    q = [[F(0) for _ in range(full)] for _ in range(n)]
    complete_per_vertex = F(
        (n - 1) * 2 ** (n - 2),
        n * (2 ** (n - 1) - 1),
    )
    static_by_target = []
    for v in range(n):
        occupied_mass = sum(
            (pi_all[state] for state in states if (state >> v) & 1),
            F(0),
        )
        static = complete_per_vertex - occupied_mass
        for state in states:
            if (state >> v) & 1:
                continue
            r_mass = pi_all[state]
            source = sigma[v][state]
            output = nu[v][state]
            k = state.bit_count()
            coefficient = sharp_coefficient(n, k)
            if r_mass + source:
                static += coefficient * r_mass * source / (r_mass + source)
            static -= coefficient * F(k, n) * r_mass
            if (r_mass + output) and (r_mass + source):
                q[v][state] = (
                    coefficient * r_mass * r_mass
                    / ((r_mass + output) * (r_mass + source))
                )
        static_by_target.append(static)

    directed = [[F(0) for _ in range(n)] for _ in range(n)]
    for v in range(n):
        for i in range(n):
            if i == v or not P[v][i]:
                continue
            drift = sum(
                (
                    (sigma[v][state] + nu[v][state])
                    * (q[v][state | (1 << i)] - q[v][state])
                    for state in range(full)
                    if not ((state >> v) & 1)
                ),
                F(0),
            )
            directed[v][i] = P[v][i] * (static_by_target[v] + drift)

    pairs = []
    for v in range(n):
        for i in range(v + 1, n):
            if P[v][i] or P[i][v]:
                pairs.append((v, i, directed[v][i] + directed[i][v]))
    total = sum((value for _, _, value in pairs), F(0))
    return total, pairs


def audit_witnesses() -> None:
    path = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    total, pairs = paired_edge_scores(path)
    assert total == F(7, 144)
    assert [value for _, _, value in pairs] == [F(7, 288), F(7, 288)]

    triangle = [[0, 1, 1], [1, 0, 5], [1, 5, 0]]
    total, pairs = paired_edge_scores(triangle)
    assert total == F(286144, 5929503)
    assert pairs[0][2] == pairs[1][2] == -F(24292724, 11580319359)
    assert pairs[2][2] == F(7688920, 146586321)

    path4 = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0],
    ]
    total, pairs = paired_edge_scores(path4)
    assert total > 0
    assert pairs[0][2] == pairs[1][2] == F(749525873, 9421011600)
    assert pairs[2][2] == -F(20641618, 374699325)

    regular_k4 = [
        [0, 1, 1, 2],
        [1, 0, 2, 1],
        [1, 2, 0, 1],
        [2, 1, 1, 0],
    ]
    total, pairs = paired_edge_scores(regular_k4)
    assert total == F(368, 123123)
    negative = [value for _, _, value in pairs if value < 0]
    assert negative == [-F(253349, 17729712)] * 4
    print("PASS: exact whole-slack original-edge expansion")
    print("PASS: reversible edge-pair positivity is exactly false, even on P4")


def screen(label, graphs, expected_graphs, expected_pairs) -> None:
    graph_count = 0
    pair_count = 0
    for weights in graphs:
        if not connected(weights):
            continue
        total, pairs = paired_edge_scores(weights)
        assert total >= 0
        negative = [value for _, _, value in pairs if value < 0]
        if negative:
            graph_count += 1
            pair_count += len(negative)
    assert (graph_count, pair_count) == (expected_graphs, expected_pairs)
    print(
        f"PASS: {label}: negative edge pair in {graph_count} graphs; "
        f"{pair_count} negative pairs"
    )


def main() -> None:
    audit_witnesses()
    screen(
        "n=3 weights in {0,1,2,5}",
        exhaustive_graphs(3, (0, 1, 2, 5)),
        24,
        33,
    )
    screen(
        "n=4 weights in {0,1,2}",
        exhaustive_graphs(4, (0, 1, 2)),
        544,
        930,
    )
    print("OPEN: aggregate reversible pairing beyond individual edges")


if __name__ == "__main__":
    main()
