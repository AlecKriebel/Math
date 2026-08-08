#!/usr/bin/env python3
"""Exact verifier for the rank-refined posterior collision experiment.

The proposed finite-baseline reflection inequality remains open.  This
program verifies all identities over ``Fraction``, certifies the frozen
counterexample to the first natural rank weighting, and hostile-screens the
surviving scalar inequality on the deterministic small-graph corpus.
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHI_DIR = HERE.parent / "r2_entropy_certificate" / "chi_square_channel"
sys.path.insert(0, str(CHI_DIR))

from verify_resolvent_identities import solve  # noqa: E402
from verify_direct_flow_screen import (  # noqa: E402
    connected,
    deterministic_graphs,
    exhaustive_graphs,
    matrix_from_edges,
)


def posterior_statistics(weights):
    P, states, _, kernels, pi = solve(weights)
    n = len(P)
    state_count = len(states)
    pi_all = [F(0) for _ in range(1 << n)]
    for state, probability in zip(states, pi):
        pi_all[state] = probability

    mu = [
        [
            sum(
                (pi[source] * kernels[v][source][target]
                 for source in range(state_count)),
                F(0),
            )
            for target in range(state_count)
        ]
        for v in range(n)
    ]

    nu = [[F(0) for _ in range(1 << n)] for _ in range(n)]
    sigma = [[F(0) for _ in range(1 << n)] for _ in range(n)]
    for v in range(n):
        for target, state in enumerate(states):
            if not ((state >> v) & 1):
                nu[v][state] = mu[v][target] - pi[target]
                assert nu[v][state] >= 0
        for state in range(1 << n):
            if not ((state >> v) & 1):
                sigma[v][state] = pi_all[state | (1 << v)]

    def add_one_sample(v, measure):
        result = [F(0) for _ in range(1 << n)]
        for state, mass in enumerate(measure):
            if not mass:
                continue
            for vertex in range(n):
                result[state | (1 << vertex)] += mass * P[v][vertex]
        return result

    # Exact midpoint Cayley identity 2 nu=(sigma+nu)A.
    for v in range(n):
        mixture = [sigma[v][state] + nu[v][state] for state in range(1 << n)]
        image = add_one_sample(v, mixture)
        assert all(2 * nu[v][state] == image[state] for state in range(1 << n))

    mean = F(0)
    collision_excess = F(0)
    naive_weighted_collision = F(0)
    rank_excess = [F(0) for _ in range(n)]
    energy = F(0)
    for target, state in enumerate(states):
        probability = pi[target]
        size = state.bit_count()
        holes = n - size
        e = [
            nu[v][state] / probability
            for v in range(n)
            if not ((state >> v) & 1)
        ]
        assert len(e) == holes
        assert sum(e, F(0)) == size
        square_sum = sum((value * value for value in e), F(0))
        minimum = F(size * size, holes)
        excess = square_sum - minimum
        assert excess >= 0

        mean += probability * size
        energy += probability * square_sum
        collision_excess += probability * excess
        rank_excess[size] += probability * excess
        naive_weighted_collision += probability * F(holes, size) * square_sum

    # The energy is also the raw two-replica sum sum nu_v(B)^2/Pi(B).
    assert energy == sum(
        (
            nu[v][state] ** 2 / pi_all[state]
            for v in range(n)
            for state in states
            if not ((state >> v) & 1)
        ),
        F(0),
    )

    complete_mean = F((n - 1) * 2 ** (n - 2), 2 ** (n - 1) - 1)
    # Surviving finite-baseline two-replica target:
    #   E[J(B)] <= n(m_K-E|B|).
    reflection_slack = n * (complete_mean - mean) - collision_excess
    refined_lhs = mean + collision_excess / n
    assert complete_mean - refined_lhs == reflection_slack / n
    return {
        "mean": mean,
        "complete_mean": complete_mean,
        "energy": energy,
        "collision_excess": collision_excess,
        "rank_excess": rank_excess,
        "naive": naive_weighted_collision,
        "reflection_slack": reflection_slack,
    }


def audit_frozen_witnesses():
    path = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    path_data = posterior_statistics(path)
    assert path_data["mean"] == F(11, 9)
    assert path_data["collision_excess"] == F(1, 6)
    assert path_data["naive"] == F(14, 9)
    assert path_data["naive"] - path_data["complete_mean"] == F(2, 9)
    assert path_data["reflection_slack"] == F(1, 6)

    weighted_path = [[0, 1, 0], [1, 0, 2], [0, 2, 0]]
    weighted_path_data = posterior_statistics(weighted_path)
    assert weighted_path_data["mean"] == F(6, 5)
    assert weighted_path_data["collision_excess"] == F(1, 5)
    assert weighted_path_data["naive"] == F(8, 5)
    assert weighted_path_data["naive"] - weighted_path_data["complete_mean"] == F(4, 15)
    assert weighted_path_data["reflection_slack"] == F(1, 5)

    regular_k4 = [
        [0, 1, 1, 2],
        [1, 0, 2, 1],
        [1, 2, 0, 1],
        [2, 1, 1, 0],
    ]
    k4_data = posterior_statistics(regular_k4)
    assert k4_data["mean"] == F(70, 41)
    assert k4_data["collision_excess"] == F(64, 4305)
    assert k4_data["naive"] == F(2514, 1435)
    assert k4_data["naive"] - k4_data["complete_mean"] == F(54, 1435)
    assert k4_data["reflection_slack"] == F(8, 615)

    split_witness = matrix_from_edges(
        6,
        (3, 300, 2, 5, 1, 3, 3, 1, 300, 1, 1, 1, 20, 1, 1),
    )
    split_data = posterior_statistics(split_witness)
    assert split_data["reflection_slack"] > 0

    print(
        "PASS: naive rank-envelope collision bound is exactly false on "
        "P3 and regular weighted K4"
    )
    print(
        "PASS: surviving reflection slack on P3, weighted P3, K4 = "
        f"{path_data['reflection_slack']}, "
        f"{weighted_path_data['reflection_slack']}, "
        f"{k4_data['reflection_slack']}"
    )
    print(
        "PASS: n=6 split witness has exact positive reflection slack "
        f"(~{float(split_data['reflection_slack']):.12g})"
    )


def screen(label, graphs):
    count = 0
    minimum = None
    naive_violations = 0
    for weights in graphs:
        if not connected(weights):
            continue
        data = posterior_statistics(weights)
        slack = data["reflection_slack"]
        assert slack >= 0, (label, weights, slack)
        if data["naive"] > data["complete_mean"]:
            naive_violations += 1
        if minimum is None or slack < minimum:
            minimum = slack
        count += 1
    assert count and minimum is not None
    minimum_text = "0" if minimum == 0 else f">0 (~{float(minimum):.12g})"
    print(
        f"PASS: {label}: {count} exact graphs; min refined slack={minimum_text}; "
        f"naive violations={naive_violations}"
    )


def main():
    audit_frozen_witnesses()
    screen("n=3 weights in {0,1,2,5}", exhaustive_graphs(3, (0, 1, 2, 5)))
    screen("n=4 weights in {0,1,2}", exhaustive_graphs(4, (0, 1, 2)))
    screen(
        "n=5 deterministic sparse/extreme",
        deterministic_graphs(5, 48, 26080805),
    )
    print("OPEN: universal finite-baseline posterior collision reflection")


if __name__ == "__main__":
    main()
