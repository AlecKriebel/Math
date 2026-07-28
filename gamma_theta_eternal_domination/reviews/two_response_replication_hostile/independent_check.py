#!/usr/bin/env python3
"""Clean-room audit of the separated-port two-response control.

This file deliberately imports no campaign code.  It uses integer bit masks,
an anchored clique-partition dynamic program for theta, and a direct
simultaneous greatest-fixed-point computation for the one-guard game.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from functools import lru_cache
from pathlib import Path


GRAPH6 = "MFzvvn{feBKbM{gZ_"
ANCHORS = (0, 1, 2)
S = sum(1 << vertex for vertex in ANCHORS)
DIRECT_LISTS = {
    3: (0, 1, 2),
    4: (0, 1),
    5: (0, 1),
    6: (0, 1),
    7: (1, 2),
    8: (1, 2),
}
CLAIMED_COLORING = [1, 2, 3, 2, 1, 2, 1, 2, 3, 1, 0, 0, 3, 0]


def graph6_adjacency(record: str) -> tuple[int, tuple[int, ...]]:
    """Decode a short graph6 record directly from its six-bit stream."""
    sextets = [ord(character) - 63 for character in record]
    assert sextets and 0 <= sextets[0] <= 62
    order = sextets[0]
    stream = [
        (sextet >> bit_position) & 1
        for sextet in sextets[1:]
        for bit_position in range(5, -1, -1)
    ]
    required = order * (order - 1) // 2
    assert len(stream) >= required
    adjacency = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if stream[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return order, tuple(adjacency)


def masks_of_size(order: int, size: int):
    for vertices in itertools.combinations(range(order), size):
        yield sum(1 << vertex for vertex in vertices)


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def closed_coverage(state: int, adjacency: tuple[int, ...]) -> int:
    coverage = state
    for guard in vertices(state):
        coverage |= adjacency[guard]
    return coverage


def is_dominating(state: int, adjacency: tuple[int, ...], universe: int) -> bool:
    return closed_coverage(state, adjacency) == universe


def is_independent(state: int, adjacency: tuple[int, ...]) -> bool:
    remaining = state
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        remaining ^= bit
        if adjacency[vertex] & remaining:
            return False
    return True


def is_maximal_independent(
    state: int, adjacency: tuple[int, ...], universe: int
) -> bool:
    if not is_independent(state, adjacency):
        return False
    outside = universe ^ state
    return all(adjacency[vertex] & state for vertex in vertices(outside))


def first_size(order: int, predicate) -> int:
    for size in range(order + 1):
        if any(predicate(mask) for mask in masks_of_size(order, size)):
            return size
    raise AssertionError("no feasible set")


def last_size(order: int, predicate) -> int:
    for size in range(order, -1, -1):
        if any(predicate(mask) for mask in masks_of_size(order, size)):
            return size
    raise AssertionError("no feasible set")


def minimum_clique_partition(
    order: int, adjacency: tuple[int, ...]
) -> tuple[int, tuple[int, ...]]:
    """Return theta via a partition DP over cliques of G.

    Each recursive step fixes the lowest remaining vertex, so every partition
    appears exactly once up to the order of its parts.
    """
    universe = (1 << order) - 1
    cliques = [False] * (1 << order)
    cliques[0] = True
    for mask in range(1, 1 << order):
        bit = mask & -mask
        vertex = bit.bit_length() - 1
        rest = mask ^ bit
        cliques[mask] = cliques[rest] and not (rest & ~adjacency[vertex])

    @lru_cache(maxsize=None)
    def solve(remaining: int) -> tuple[int, tuple[int, ...]]:
        if remaining == 0:
            return 0, ()
        pivot = remaining & -remaining
        best_count = order + 1
        best_parts: tuple[int, ...] = ()
        subset = remaining
        while subset:
            if subset & pivot and cliques[subset]:
                suffix_count, suffix_parts = solve(remaining ^ subset)
                candidate = 1 + suffix_count
                if candidate < best_count:
                    best_count = candidate
                    best_parts = (subset,) + suffix_parts
            subset = (subset - 1) & remaining
        return best_count, best_parts

    answer = solve(universe)
    reconstructed = 0
    for part in answer[1]:
        assert cliques[part]
        assert not (reconstructed & part)
        reconstructed |= part
    assert reconstructed == universe
    return answer


def one_guard_kernel(
    order: int, guard_count: int, adjacency: tuple[int, ...], universe: int
) -> tuple[int, list[int], set[int]]:
    alive = {
        state
        for state in masks_of_size(order, guard_count)
        if is_dominating(state, adjacency, universe)
    }
    initial_count = len(alive)
    deletion_rounds: list[int] = []
    while True:
        rejected: set[int] = set()
        for state in alive:
            attacks = universe ^ state
            for attacked in vertices(attacks):
                attacked_bit = 1 << attacked
                response_exists = False
                for guard in vertices(state):
                    guard_bit = 1 << guard
                    if adjacency[guard] & attacked_bit:
                        successor = (state ^ guard_bit) | attacked_bit
                        if successor in alive:
                            response_exists = True
                            break
                if not response_exists:
                    rejected.add(state)
                    break
        if not rejected:
            return initial_count, deletion_rounds, alive
        alive.difference_update(rejected)
        deletion_rounds.append(len(rejected))


def sorted_list(mask: int) -> list[int]:
    return list(vertices(mask))


def missed(state: int, adjacency: tuple[int, ...], universe: int) -> list[int]:
    return sorted_list(universe ^ closed_coverage(state, adjacency))


def failed_attack(
    source_vertices: tuple[int, int, int],
    attack: int,
    adjacency: tuple[int, ...],
    universe: int,
) -> dict[str, object]:
    source = sum(1 << vertex for vertex in source_vertices)
    assert not (source & (1 << attack))
    responses = []
    for guard in vertices(source):
        if adjacency[guard] & (1 << attack):
            successor = (source ^ (1 << guard)) | (1 << attack)
            missed_vertices = missed(successor, adjacency, universe)
            assert missed_vertices
            responses.append(
                {
                    "guard": guard,
                    "missed": missed_vertices,
                    "successor": sorted_list(successor),
                }
            )
    assert responses
    return {
        "attack": attack,
        "responses": responses,
        "source": sorted_list(source),
    }


def calculate() -> dict[str, object]:
    order, adjacency = graph6_adjacency(GRAPH6)
    assert order == 14
    universe = (1 << order) - 1
    edge_count = sum(row.bit_count() for row in adjacency) // 2

    gamma = first_size(
        order, lambda state: is_dominating(state, adjacency, universe)
    )
    independence = last_size(
        order, lambda state: is_independent(state, adjacency)
    )
    independent_domination = first_size(
        order,
        lambda state: is_maximal_independent(state, adjacency, universe),
    )
    theta, clique_parts = minimum_clique_partition(order, adjacency)
    assert len(clique_parts) == theta

    # Validate the separately supplied complement coloring as a clique
    # partition of G.  The DP above proves that fewer parts are impossible.
    assert len(CLAIMED_COLORING) == order
    for left in range(order):
        for right in range(left + 1, order):
            if CLAIMED_COLORING[left] == CLAIMED_COLORING[right]:
                assert adjacency[left] & (1 << right)
    assert len(set(CLAIMED_COLORING)) == theta

    three_initial, three_rounds, three_survivors = one_guard_kernel(
        order, 3, adjacency, universe
    )
    four_initial, four_rounds, four_survivors = one_guard_kernel(
        order, 4, adjacency, universe
    )
    assert not three_survivors
    assert four_survivors
    gamma_infinity = 4

    q_s = [
        vertex
        for vertex in range(order)
        if not (S & (1 << vertex))
        and all(adjacency[vertex] & (1 << anchor) for anchor in ANCHORS)
    ]
    complement_adjacency = tuple(
        (universe ^ (1 << vertex) ^ adjacency[vertex])
        for vertex in range(order)
    )
    signatures = {
        str(vertex): sorted_list(complement_adjacency[vertex] & S)
        for vertex in range(9, 14)
    }

    seed = {S}
    for target, allowed_guards in DIRECT_LISTS.items():
        for guard in allowed_guards:
            seed.add((S ^ (1 << guard)) | (1 << target))
    assert len(seed) == 14
    assert all(is_dominating(state, adjacency, universe) for state in seed)
    seed_lists = {
        str(target): [
            guard
            for guard in ANCHORS
            if ((S ^ (1 << guard)) | (1 << target)) in seed
        ]
        for target in DIRECT_LISTS
    }
    attacks = [
        failed_attack((0, 2, 3), 9, adjacency, universe),
        failed_attack((0, 2, 3), 12, adjacency, universe),
        failed_attack((0, 2, 6), 9, adjacency, universe),
        failed_attack((0, 2, 8), 12, adjacency, universe),
    ]

    return {
        "complement_size": order * (order - 1) // 2 - edge_count,
        "failed_first_attacks": attacks,
        "four_guard_kernel": {
            "deletion_rounds": four_rounds,
            "dominating_configurations": four_initial,
            "survivors": len(four_survivors),
        },
        "graph6": GRAPH6,
        "graph6_sha256": hashlib.sha256(GRAPH6.encode("ascii")).hexdigest(),
        "new_anchor_signatures": signatures,
        "order": order,
        "parameters": {
            "alpha": independence,
            "gamma": gamma,
            "gamma_infinity": gamma_infinity,
            "i": independent_domination,
            "theta": theta,
        },
        "q_s": q_s,
        "schema": "gamma-theta-separated-core-n14-static-control-v1",
        "seed_lists": seed_lists,
        "seed_size": len(seed),
        "size": edge_count,
        "theta_coloring": CLAIMED_COLORING,
        "three_guard_kernel": {
            "deletion_rounds": three_rounds,
            "dominating_configurations": three_initial,
            "survivors": len(three_survivors),
        },
    }


def main() -> None:
    result = calculate()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if len(sys.argv) == 2:
        candidate_path = Path(sys.argv[1])
        candidate = candidate_path.read_bytes()
        assert candidate == rendered.encode("utf-8"), (
            f"byte mismatch against {candidate_path}"
        )
        print(
            "PASS "
            + hashlib.sha256(candidate).hexdigest()
            + " "
            + str(candidate_path)
        )
    elif len(sys.argv) == 1:
        sys.stdout.write(rendered)
    else:
        raise SystemExit(f"usage: {sys.argv[0]} [result.json]")


if __name__ == "__main__":
    main()
