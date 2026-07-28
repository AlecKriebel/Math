#!/usr/bin/env python3
"""Standalone replay of the sharp repair-square rank boundary.

This checker imports no campaign search or evaluator code.  It decodes one
fixed graph6 record, recomputes the relevant exact parameters and greatest
one-guard kernels, and checks the named repair two-cycle and ranks.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter, deque


GRAPH6 = "NslalntvXzn^{~n||^w"
U, X, P, Q, R, B, A, W, Z = 0, 1, 2, 3, 4, 5, 6, 10, 13


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    values = [ord(char) - 63 for char in record]
    if not values or not 0 <= values[0] <= 62:
        raise ValueError("only short graph6 records are supported")
    order = values[0]
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    needed = order * (order - 1) // 2
    if len(bits) < needed or any(bits[needed:]):
        raise ValueError("truncated or nonzero-padded graph6 record")
    rows = [set() for _ in range(order)]
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                rows[left].add(right)
                rows[right].add(left)
            cursor += 1
    return tuple(frozenset(row) for row in rows)


def subsets(order: int, size: int):
    return tuple(
        frozenset(choice)
        for choice in itertools.combinations(range(order), size)
    )


def independent(graph, state) -> bool:
    return all(
        right not in graph[left]
        for left, right in itertools.combinations(state, 2)
    )


def dominates(graph, state) -> bool:
    return all(
        vertex in state or bool(graph[vertex] & state)
        for vertex in range(len(graph))
    )


def kernel(graph, size: int):
    family = {
        state for state in subsets(len(graph), size) if dominates(graph, state)
    }
    ranks = {}
    waves = []
    round_number = 0
    while True:
        removed = set()
        for state in family:
            for target in range(len(graph)):
                if target in state:
                    continue
                if not any(
                    target in graph[guard]
                    and state - {guard} | {target} in family
                    for guard in state
                ):
                    removed.add(state)
                    break
        if not removed:
            return family, ranks, waves
        round_number += 1
        for state in removed:
            ranks[state] = round_number
        family.difference_update(removed)
        waves.append(len(removed))


def minimum_size(order: int, predicate) -> int:
    for size in range(1, order + 1):
        if any(predicate(state) for state in subsets(order, size)):
            return size
    raise AssertionError("no witness")


def clique_partition_number(graph) -> int:
    order = len(graph)
    vertices = sorted(range(order), key=lambda v: (len(graph[v]), v))
    for count in range(1, order + 1):
        parts = [[] for _ in range(count)]

        def extend(offset: int, used: int) -> bool:
            if offset == order:
                return True
            vertex = vertices[offset]
            for color in range(min(used + 1, count)):
                if color == used and used == count:
                    continue
                if all(member in graph[vertex] for member in parts[color]):
                    parts[color].append(vertex)
                    if extend(offset + 1, max(used, color + 1)):
                        return True
                    parts[color].pop()
            return False

        if extend(0, 0):
            return count
    raise AssertionError("singleton partition must exist")


def active(graph, family, independent_triples, source: int, target: int) -> bool:
    witnesses = [
        state
        for state in independent_triples
        if source in state and target not in state
    ]
    if not witnesses:
        return False
    return any(state - {source} | {target} in family for state in witnesses)


def complement_link(graph, pivot: int):
    vertices = [
        vertex
        for vertex in range(len(graph))
        if vertex != pivot and vertex not in graph[pivot]
    ]
    adjacency = {
        vertex: frozenset(
            other
            for other in vertices
            if other != vertex and other not in graph[vertex]
        )
        for vertex in vertices
    }
    components = []
    unseen = set(vertices)
    while unseen:
        root = min(unseen)
        queue = deque([root])
        unseen.remove(root)
        component = []
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            for other in sorted(adjacency[vertex]):
                if other in unseen:
                    unseen.remove(other)
                    queue.append(other)
        components.append(sorted(component))
    return vertices, adjacency, sorted(components)


def evaluate():
    graph = decode_graph6(GRAPH6)
    order = len(graph)
    gamma = minimum_size(order, lambda state: dominates(graph, state))
    independent_domination = minimum_size(
        order,
        lambda state: independent(graph, state) and dominates(graph, state),
    )
    alpha = max(
        size
        for size in range(1, order + 1)
        if any(independent(graph, state) for state in subsets(order, size))
    )
    theta = clique_partition_number(graph)

    kernels = {size: kernel(graph, size) for size in (1, 2, 3)}
    gamma_infinity = next(size for size in (1, 2, 3) if kernels[size][0])
    family, ranks, waves = kernels[3]
    independent_triples = [
        state for state in subsets(order, 3) if independent(graph, state)
    ]

    orientations = {
        "u_to_x": active(graph, family, independent_triples, U, X),
        "x_to_u": active(graph, family, independent_triples, X, U),
        "z_to_a": active(graph, family, independent_triples, Z, A),
        "a_to_z": active(graph, family, independent_triples, A, Z),
    }
    if orientations != {
        "u_to_x": True,
        "x_to_u": False,
        "z_to_a": True,
        "a_to_z": False,
    }:
        raise AssertionError("wrong active-orientation pattern")

    common_ux_nonneighbors = [
        vertex
        for vertex in range(order)
        if vertex not in (U, X)
        and vertex not in graph[U]
        and vertex not in graph[X]
    ]
    if common_ux_nonneighbors != [W]:
        raise AssertionError("the named pair must have unique common nonneighbor")

    vertices, link_adjacency, components = complement_link(graph, W)
    if vertices != [U, X, A, Z]:
        raise AssertionError("wrong complement-link vertex set")
    if {
        vertex: sorted(neighbors)
        for vertex, neighbors in link_adjacency.items()
    } != {U: [A], X: [Z], A: [U], Z: [X]}:
        raise AssertionError("the complement link is not the named 2K2")
    if components != [[U, A], [X, Z]]:
        raise AssertionError("wrong complement-link components")

    source_completions = [
        vertex
        for vertex in range(order)
        if vertex not in (U, W)
        and vertex not in graph[U]
        and vertex not in graph[W]
    ]
    target_completions = [
        vertex
        for vertex in range(order)
        if vertex not in (X, W)
        and vertex not in graph[X]
        and vertex not in graph[W]
    ]
    if source_completions != [A] or target_completions != [Z]:
        raise AssertionError("the repair completions are not unique")

    original_endpoint = frozenset({X, P, Q})
    original_reverse = frozenset({U, P, Q})
    repaired_source = frozenset({U, W, A})
    repaired_target = frozenset({X, W, Z})
    repaired_corner_from_original = repaired_target - {X} | {U}
    repaired_corner_from_opposite = repaired_source - {A} | {Z}
    repaired_corner = frozenset({U, W, Z})

    if not all(
        state in family
        for state in (original_endpoint, repaired_source, repaired_target)
    ):
        raise AssertionError("a named independent endpoint is not retained")
    if ranks.get(original_reverse) != 1:
        raise AssertionError("the canonical reverse endpoint is not rank one")
    if repaired_corner_from_original != repaired_corner:
        raise AssertionError("wrong original-orientation repair corner")
    if repaired_corner_from_opposite != repaired_corner:
        raise AssertionError("wrong opposite-orientation repair corner")
    if ranks.get(repaired_corner) != 3:
        raise AssertionError("the conserved repair corner is not rank three")

    # Backtracking both link edges applies the repair rule twice.
    repair_cycle = [
        [U, X],
        [Z, A],
        [U, X],
    ]
    if A not in link_adjacency[U] or Z not in link_adjacency[X]:
        raise AssertionError("first repair step is not supported")
    if X not in link_adjacency[Z] or U not in link_adjacency[A]:
        raise AssertionError("repair step does not backtrack")

    dominating_pairs = [
        sorted(state)
        for state in subsets(order, 2)
        if dominates(graph, state)
    ]
    if len(dominating_pairs) != 23 or [U, X] in dominating_pairs:
        raise AssertionError("wrong global-gamma boundary")

    result = {
        "schema": "repair-square-holonomy-boundary-v1",
        "status": "VERIFIED",
        "graph6": GRAPH6,
        "order": order,
        "size": sum(map(len, graph)) // 2,
        "parameters": {
            "gamma": gamma,
            "i": independent_domination,
            "alpha": alpha,
            "gamma_infinity": gamma_infinity,
            "theta": theta,
        },
        "greatest_triple_family_size": len(family),
        "triple_deletion_wave_sizes": waves,
        "triple_positive_rank_histogram": {
            str(rank): count
            for rank, count in sorted(Counter(ranks.values()).items())
        },
        "orientations": orientations,
        "common_ux_nonneighbors": common_ux_nonneighbors,
        "link_at_w": {
            "pivot": W,
            "vertices": vertices,
            "adjacency": {
                str(vertex): sorted(neighbors)
                for vertex, neighbors in sorted(link_adjacency.items())
            },
            "components": components,
        },
        "unique_completions": {
            "u_w": source_completions,
            "x_w": target_completions,
        },
        "rank_boundary": {
            "original_endpoint": sorted(original_endpoint),
            "original_reverse": sorted(original_reverse),
            "original_reverse_rank": ranks[original_reverse],
            "repaired_source": sorted(repaired_source),
            "repaired_target": sorted(repaired_target),
            "shared_repair_corner": sorted(repaired_corner),
            "shared_repair_corner_rank": ranks[repaired_corner],
            "endpoint_symmetric_difference_half": len(
                original_endpoint - repaired_target
            ),
        },
        "repair_oriented_pair_cycle": repair_cycle,
        "dominating_pair_count": len(dominating_pairs),
        "selected_pair_dominates": [U, X] in dominating_pairs,
        "sharp_boundary": (
            "gamma=2<alpha=gamma_infinity=3; the selected asymmetric "
            "pair is nondominating, but 23 other pairs dominate"
        ),
    }
    expected_parameters = {
        "gamma": 2,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    if result["parameters"] != expected_parameters:
        raise AssertionError("wrong exact parameter tuple")
    return result


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
