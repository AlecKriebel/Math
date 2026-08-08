#!/usr/bin/env python3
"""Exact hostile audit of permutation-orbit midpoint symmetrization at r=2.

The conjectured direction is

    rho_dB((W + sigma.W)/2, 2) >= rho_dB(W, 2).

It would permit iterative symmetrization to the complete conductance matrix.
The nonregular statement was already false in the phase-four orbital audit;
we replay that witness and an independently found simplification.  The
regular-conductance subcase is screened separately on exact rational data.
Finite survival of the regular subcase is evidence only.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
from random import Random

import networkx as nx

from exact_fixation import Q, as_float, connected, fixation, matrix_from_edges


def conjugate(weights, permutation):
    n = len(weights)
    return [
        [weights[permutation[u]][permutation[v]] for v in range(n)]
        for u in range(n)
    ]


def midpoint(left, right):
    return [
        [(left[u][v] + right[u][v]) / 2 for v in range(len(left))]
        for u in range(len(left))
    ]


def slack(weights, permutation):
    endpoint = fixation(weights, "dB")
    conjugated = conjugate(weights, permutation)
    assert fixation(conjugated, "dB") == endpoint
    middle = fixation(midpoint(weights, conjugated), "dB")
    return middle - endpoint, endpoint, middle


def phase4_nonregular_witness():
    # Path 2--0--4--1--3 with the exact conductances stored in the phase-four
    # orbital-symmetrization certificate.
    n = 5
    weights = [[Q(0) for _ in range(n)] for _ in range(n)]
    for u, v, value in (
        (0, 2, Q(5)),
        (0, 4, Q(1)),
        (1, 3, Q(20)),
        (1, 4, Q(1, 10)),
    ):
        weights[u][v] = weights[v][u] = value
    return weights, (1, 0, 2, 3, 4)


def simple_nonregular_witness():
    # Independently found path 0--1--2--3--4, with one heavy end edge.  The
    # permutation is the transposition (0 3).
    weights = matrix_from_edges(5, (5, 0, 0, 0, 1, 0, 0, 1, 0, 1))
    return weights, (3, 1, 2, 0, 4)


def perfect_matchings(n):
    def recurse(vertices):
        if not vertices:
            yield ()
            return
        u = vertices[0]
        for position in range(1, len(vertices)):
            v = vertices[position]
            rest = vertices[1:position] + vertices[position + 1 :]
            for matching in recurse(rest):
                yield ((u, v),) + matching

    return list(recurse(tuple(range(n))))


def hamilton_cycles(n):
    answer = set()
    for tail in permutations(range(1, n)):
        if tail[0] > tail[-1]:
            continue
        order = (0,) + tail
        cycle = tuple(
            sorted(tuple(sorted((order[i], order[(i + 1) % n]))) for i in range(n))
        )
        answer.add(cycle)
    return sorted(answer)


def sum_components(n, components, choices):
    weights = [[Q(0) for _ in range(n)] for _ in range(n)]
    for component, coefficient in choices:
        for u, v in component:
            weights[u][v] += coefficient
            weights[v][u] += coefficient
    degrees = [sum(row, Q(0)) for row in weights]
    assert len(set(map(str, degrees))) == 1
    return weights


def regular_corpus():
    rng = Random(26080810)

    # Every connected unweighted regular graph in the atlas through n=7.
    atlas = nx.graph_atlas_g()
    for atlas_id, graph in enumerate(atlas):
        n = len(graph)
        if not 3 <= n <= 7 or not nx.is_connected(graph):
            continue
        degrees = [degree for _, degree in graph.degree()]
        if len(set(degrees)) != 1:
            continue
        weights = [
            [Q(int(u != v and graph.has_edge(u, v))) for v in range(n)]
            for u in range(n)
        ]
        all_permutations = list(permutations(range(n)))
        if n <= 5:
            selected = all_permutations
        else:
            selected = rng.sample(all_permutations, min(20, len(all_permutations)))
        for permutation in selected:
            yield f"atlas-{atlas_id}", weights, permutation

    # Sums of perfect matchings (even n) or Hamilton cycles (odd n) are
    # automatically regular, while retaining highly nonuniform conductances.
    for n in range(4, 8):
        components = perfect_matchings(n) if n % 2 == 0 else hamilton_cycles(n)
        trials = 20 if n <= 5 else 10
        permutations_per_trial = 10
        for trial in range(trials):
            count = rng.randint(1, min(8, len(components)))
            choices = [
                (rng.choice(components), Q(rng.choice((1, 2, 5, 20, 1000))))
                for _ in range(count)
            ]
            weights = sum_components(n, components, choices)
            if not connected(weights):
                continue
            for _ in range(permutations_per_trial):
                permutation = tuple(rng.sample(range(n), n))
                yield f"regular-sum-n{n}-trial{trial}", weights, permutation


def main() -> None:
    for label, builder in (
        ("phase4-path", phase4_nonregular_witness),
        ("simple-path", simple_nonregular_witness),
    ):
        weights, permutation = builder()
        gap, endpoint, middle = slack(weights, permutation)
        assert gap < 0
        print(
            f"EXACT NONREGULAR REFUTATION {label}: gap={gap} "
            f"(~{as_float(gap):.17g}); endpoint~{as_float(endpoint):.17g}; "
            f"midpoint~{as_float(middle):.17g}"
        )

    tested = 0
    failures = []
    smallest = None
    for label, weights, permutation in regular_corpus():
        gap, endpoint, middle = slack(weights, permutation)
        record = (gap, endpoint, middle, label, weights, permutation)
        if smallest is None or gap < smallest[0]:
            smallest = record
        if gap < 0:
            failures.append(record)
            break
        tested += 1
    assert smallest is not None
    gap, endpoint, middle, label, weights, permutation = smallest
    print(f"EXACT REGULAR MIDPOINT SCREEN: {tested + len(failures)} cases")
    print(
        "smallest regular slack:", label, gap, f"(~{as_float(gap):.17g})",
        "permutation=", permutation,
    )
    if failures:
        print("EXACT REGULAR PERMUTATION-MIDPOINT COUNTEREXAMPLE FOUND")
        print("weights=", [[str(value) for value in row] for row in weights])
    else:
        print("No regular-conductance midpoint failure in the finite corpus.")
        print("The regular orbital conjecture remains OPEN.")


if __name__ == "__main__":
    main()
