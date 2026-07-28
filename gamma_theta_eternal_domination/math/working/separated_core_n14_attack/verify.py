#!/usr/bin/env python3
"""Independent verifier for the 14-vertex tight static control."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


GRAPH6 = "MFzvvn{feBKbM{gZ_"
S = frozenset((0, 1, 2))
DESIRED_LISTS = {
    3: frozenset((0, 1, 2)),
    4: frozenset((0, 1)),
    5: frozenset((0, 1)),
    6: frozenset((0, 1)),
    7: frozenset((1, 2)),
    8: frozenset((1, 2)),
}


def decode_graph6(record: str) -> tuple[int, set[tuple[int, int]]]:
    values = [ord(char) - 63 for char in record]
    if not values or not 0 <= values[0] < 63:
        raise ValueError("only short graph6 records are supported")
    n = values[0]
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    needed = n * (n - 1) // 2
    if len(bits) < needed:
        raise ValueError("truncated graph6 record")
    edges: set[tuple[int, int]] = set()
    index = 0
    for v in range(1, n):
        for u in range(v):
            if bits[index]:
                edges.add((u, v))
            index += 1
    return n, edges


def neighborhoods(
    n: int, edges: set[tuple[int, int]]
) -> tuple[frozenset[int], ...]:
    result = [set() for _ in range(n)]
    for u, v in edges:
        result[u].add(v)
        result[v].add(u)
    return tuple(frozenset(row) for row in result)


def dominates(
    state: frozenset[int],
    adjacency: tuple[frozenset[int], ...],
) -> bool:
    return all(
        vertex in state
        or any(vertex in adjacency[guard] for guard in state)
        for vertex in range(len(adjacency))
    )


def independent(
    state: frozenset[int],
    adjacency: tuple[frozenset[int], ...],
) -> bool:
    return all(
        v not in adjacency[u]
        for u, v in itertools.combinations(sorted(state), 2)
    )


def minimum_size(
    n: int,
    predicate,
) -> int:
    for size in range(n + 1):
        if any(
            predicate(frozenset(state))
            for state in itertools.combinations(range(n), size)
        ):
            return size
    raise AssertionError("no feasible subset")


def maximum_size(
    n: int,
    predicate,
) -> int:
    for size in range(n, -1, -1):
        if any(
            predicate(frozenset(state))
            for state in itertools.combinations(range(n), size)
        ):
            return size
    raise AssertionError("no feasible subset")


def chromatic_number(
    adjacency: tuple[frozenset[int], ...],
) -> tuple[int, list[int]]:
    n = len(adjacency)
    order = sorted(range(n), key=lambda vertex: (-len(adjacency[vertex]), vertex))

    def color_with(k: int) -> list[int] | None:
        colors = [-1] * n

        def visit(position: int) -> bool:
            if position == n:
                return True
            vertex = order[position]
            forbidden = {
                colors[neighbor]
                for neighbor in adjacency[vertex]
                if colors[neighbor] >= 0
            }
            for color in range(k):
                if color in forbidden:
                    continue
                colors[vertex] = color
                if visit(position + 1):
                    return True
            colors[vertex] = -1
            return False

        return colors if visit(0) else None

    for k in range(1, n + 1):
        coloring = color_with(k)
        if coloring is not None:
            return k, coloring
    raise AssertionError("coloring search failed")


def eternal_kernel(
    n: int,
    size: int,
    adjacency: tuple[frozenset[int], ...],
) -> tuple[int, list[int], set[frozenset[int]]]:
    kernel = {
        frozenset(state)
        for state in itertools.combinations(range(n), size)
        if dominates(frozenset(state), adjacency)
    }
    initial = len(kernel)
    rounds: list[int] = []
    vertices = frozenset(range(n))
    while True:
        dead: set[frozenset[int]] = set()
        for state in kernel:
            for attack in vertices - state:
                if not any(
                    attack in adjacency[guard]
                    and frozenset((state - {guard}) | {attack}) in kernel
                    for guard in state
                ):
                    dead.add(state)
                    break
        if not dead:
            return initial, rounds, kernel
        kernel -= dead
        rounds.append(len(dead))


def missed_vertices(
    state: frozenset[int],
    adjacency: tuple[frozenset[int], ...],
) -> list[int]:
    return [
        vertex
        for vertex in range(len(adjacency))
        if vertex not in state
        and all(vertex not in adjacency[guard] for guard in state)
    ]


def attack_certificate(
    source: frozenset[int],
    attack: int,
    adjacency: tuple[frozenset[int], ...],
) -> dict[str, object]:
    responses = []
    for guard in sorted(source):
        if attack not in adjacency[guard]:
            continue
        successor = frozenset((source - {guard}) | {attack})
        responses.append(
            {
                "guard": guard,
                "successor": sorted(successor),
                "missed": missed_vertices(successor, adjacency),
            }
        )
    assert responses
    assert all(item["missed"] for item in responses)
    return {
        "source": sorted(source),
        "attack": attack,
        "responses": responses,
    }


def calculate() -> dict[str, object]:
    n, graph_edges = decode_graph6(GRAPH6)
    all_edges = set(itertools.combinations(range(n), 2))
    complement_edges = all_edges - graph_edges
    graph_adjacency = neighborhoods(n, graph_edges)
    complement_adjacency = neighborhoods(n, complement_edges)

    gamma = minimum_size(
        n, lambda state: dominates(state, graph_adjacency)
    )
    alpha = maximum_size(
        n, lambda state: independent(state, graph_adjacency)
    )
    independent_domination = minimum_size(
        n,
        lambda state: independent(state, graph_adjacency)
        and dominates(state, graph_adjacency),
    )
    theta, coloring = chromatic_number(complement_adjacency)

    triple_initial, triple_rounds, triple_kernel = eternal_kernel(
        n, 3, graph_adjacency
    )
    four_initial, four_rounds, four_kernel = eternal_kernel(
        n, 4, graph_adjacency
    )
    assert not triple_kernel
    assert four_kernel

    q_s = [
        vertex
        for vertex in range(n)
        if vertex not in S
        and all(anchor in graph_adjacency[vertex] for anchor in S)
    ]
    signatures = {
        str(vertex): sorted(complement_adjacency[vertex] & S)
        for vertex in range(9, 14)
    }

    seed = {S}
    for target, allowed in DESIRED_LISTS.items():
        for guard in allowed:
            seed.add(frozenset((S - {guard}) | {target}))
    assert len(seed) == 14
    assert all(dominates(state, graph_adjacency) for state in seed)
    seed_lists = {
        str(target): sorted(
            guard
            for guard in S
            if frozenset((S - {guard}) | {target}) in seed
        )
        for target in DESIRED_LISTS
    }

    attacks = [
        attack_certificate(frozenset((0, 2, 3)), 9, graph_adjacency),
        attack_certificate(frozenset((0, 2, 3)), 12, graph_adjacency),
        attack_certificate(frozenset((0, 2, 6)), 9, graph_adjacency),
        attack_certificate(frozenset((0, 2, 8)), 12, graph_adjacency),
    ]

    return {
        "schema": "gamma-theta-separated-core-n14-static-control-v1",
        "graph6": GRAPH6,
        "graph6_sha256": hashlib.sha256(GRAPH6.encode("ascii")).hexdigest(),
        "order": n,
        "size": len(graph_edges),
        "complement_size": len(complement_edges),
        "parameters": {
            "gamma": gamma,
            "i": independent_domination,
            "alpha": alpha,
            "gamma_infinity": 4,
            "theta": theta,
        },
        "theta_coloring": coloring,
        "q_s": q_s,
        "new_anchor_signatures": signatures,
        "seed_size": len(seed),
        "seed_lists": seed_lists,
        "three_guard_kernel": {
            "dominating_configurations": triple_initial,
            "deletion_rounds": triple_rounds,
            "survivors": len(triple_kernel),
        },
        "four_guard_kernel": {
            "dominating_configurations": four_initial,
            "deletion_rounds": four_rounds,
            "survivors": len(four_kernel),
        },
        "failed_first_attacks": attacks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = calculate()
    if args.check is not None:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        if result != expected:
            raise SystemExit("result mismatch")
        print("PASS: independently reconstructed static control and attacks")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
