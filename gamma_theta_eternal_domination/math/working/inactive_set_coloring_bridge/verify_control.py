#!/usr/bin/env python3
"""Standalone exact verifier for the inactive-C5 boundary control."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DELETION_ORDER = 11
TARGET = 11
ACTIVE = frozenset(range(5, 11))
INACTIVE = frozenset(range(5))
ROOT = frozenset((5, 6, 7))
H_PRIME_EDGES = frozenset(
    {
        (0, 1),
        (0, 4),
        (0, 7),
        (0, 8),
        (1, 2),
        (1, 7),
        (1, 10),
        (2, 3),
        (2, 6),
        (2, 8),
        (2, 9),
        (2, 10),
        (3, 4),
        (3, 5),
        (3, 10),
        (4, 5),
        (4, 8),
        (5, 6),
        (5, 7),
        (6, 7),
        (6, 9),
        (8, 9),
    }
)


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def masks(n: int, size: int):
    for group in itertools.combinations(range(n), size):
        yield sum(1 << vertex for vertex in group)


def graph(order: int, edges) -> tuple[int, ...]:
    adjacency = [0] * order
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return tuple(adjacency)


def complement(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    all_vertices = (1 << len(adjacency)) - 1
    return tuple(
        all_vertices ^ (1 << vertex) ^ row
        for vertex, row in enumerate(adjacency)
    )


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    return all(not (adjacency[v] & state) for v in vertices(state))


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for v in vertices(state):
        covered |= adjacency[v]
    return covered == (1 << len(adjacency)) - 1


def domination_number(adjacency: tuple[int, ...]) -> int:
    return next(
        size
        for size in range(1, len(adjacency) + 1)
        if any(dominates(adjacency, state) for state in masks(len(adjacency), size))
    )


def independence_number(adjacency: tuple[int, ...]) -> int:
    return next(
        size
        for size in range(len(adjacency), 0, -1)
        if any(
            independent(adjacency, state)
            for state in masks(len(adjacency), size)
        )
    )


def independent_domination_number(adjacency: tuple[int, ...]) -> int:
    n = len(adjacency)
    for size in range(1, n + 1):
        for state in masks(n, size):
            if independent(adjacency, state) and dominates(adjacency, state):
                return size
    raise AssertionError


def greatest_family(adjacency: tuple[int, ...], size: int) -> frozenset[int]:
    n = len(adjacency)
    all_vertices = (1 << n) - 1
    family = frozenset(
        state for state in masks(n, size) if dominates(adjacency, state)
    )
    while True:
        retained = frozenset(
            state
            for state in family
            if all(
                any(
                    ((state ^ (1 << guard)) | (1 << attack)) in family
                    for guard in vertices(state & adjacency[attack])
                )
                for attack in vertices(all_vertices ^ state)
            )
        )
        if retained == family:
            return family
        family = retained


def eternal_number(adjacency: tuple[int, ...]) -> int:
    return next(
        size
        for size in range(1, len(adjacency) + 1)
        if greatest_family(adjacency, size)
    )


def proper_colorings(adjacency: tuple[int, ...], colors: int):
    n = len(adjacency)
    assignment = [-1] * n

    def visit():
        uncolored = [v for v in range(n) if assignment[v] < 0]
        if not uncolored:
            yield tuple(assignment)
            return
        vertex = max(
            uncolored,
            key=lambda v: (
                len(
                    {
                        assignment[u]
                        for u in vertices(adjacency[v])
                        if assignment[u] >= 0
                    }
                ),
                adjacency[v].bit_count(),
            ),
        )
        forbidden = {
            assignment[u]
            for u in vertices(adjacency[vertex])
            if assignment[u] >= 0
        }
        for color in range(colors):
            if color not in forbidden:
                assignment[vertex] = color
                yield from visit()
                assignment[vertex] = -1

    yield from visit()


def chromatic_number(adjacency: tuple[int, ...]) -> int:
    return next(
        colors
        for colors in range(1, len(adjacency) + 1)
        if next(proper_colorings(adjacency, colors), None) is not None
    )


def triangles(adjacency: tuple[int, ...]) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(group)
        for group in itertools.combinations(range(len(adjacency)), 3)
        if all(
            adjacency[u] & (1 << v)
            for u, v in itertools.combinations(group, 2)
        )
    )


def graph6(adjacency: tuple[int, ...]) -> str:
    bits = [
        int(bool(adjacency[low] & (1 << high)))
        for high in range(1, len(adjacency))
        for low in range(high)
    ]
    bits += [0] * ((-len(bits)) % 6)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = 2 * value + bit
        payload.append(chr(value + 63))
    return chr(len(adjacency) + 63) + "".join(payload)


def main() -> None:
    h_prime = graph(DELETION_ORDER, H_PRIME_EDGES)
    g_prime = complement(h_prime)
    h_edges = set(H_PRIME_EDGES)
    h_edges.update((r, TARGET) for r in INACTIVE)
    h = graph(12, h_edges)
    g = complement(h)

    assert all(h_prime[u] & h_prime[v] for u, v in itertools.combinations(range(11), 2))
    assert all(h[u] & h[v] for u, v in itertools.combinations(range(12), 2))
    assert {
        tuple(sorted(edge))
        for edge in itertools.combinations(INACTIVE, 2)
        if h_prime[edge[0]] & (1 << edge[1])
    } == {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}

    deletion_triangles = triangles(h_prime)
    assert ROOT in deletion_triangles
    assert all(triangle & ACTIVE for triangle in deletion_triangles)

    # The prescribed static list at x is exactly T intersect A.
    static_lists = {}
    for triangle in deletion_triangles:
        state = sum(1 << v for v in triangle)
        legal = frozenset(
            guard
            for guard in triangle
            if g[guard] & (1 << TARGET)
            and dominates(g, (state ^ (1 << guard)) | (1 << TARGET))
        )
        assert legal == triangle & ACTIVE
        static_lists[",".join(map(str, sorted(triangle)))] = sorted(legal)
    assert frozenset(static_lists["5,6,7"]) == ROOT

    # Ridge components and exact active-color covariance in every coloring.
    ridge_adjacency = [
        [
            j
            for j, other in enumerate(deletion_triangles)
            if j != i and len(triangle & other) == 2
        ]
        for i, triangle in enumerate(deletion_triangles)
    ]
    components = []
    unseen = set(range(len(deletion_triangles)))
    while unseen:
        start = min(unseen)
        stack = [start]
        unseen.remove(start)
        component = []
        while stack:
            current = stack.pop()
            component.append(current)
            for neighbor in ridge_adjacency[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
        components.append(tuple(sorted(component)))

    colorings = tuple(proper_colorings(h_prime, 3))
    assert len(colorings) == 12
    for coloring in colorings:
        component_sets = []
        for component in components:
            sets = {
                frozenset(
                    coloring[v]
                    for v in deletion_triangles[index] & ACTIVE
                )
                for index in component
            }
            assert len(sets) == 1
            component_sets.append(next(iter(sets)))
        intersection = set((0, 1, 2))
        for responder_colors in component_sets:
            intersection &= responder_colors
        absent_from_r = set((0, 1, 2)) - {
            coloring[v] for v in INACTIVE
        }
        assert intersection == absent_from_r == set()

    deletion_parameters = {
        "gamma": domination_number(g_prime),
        "i": independent_domination_number(g_prime),
        "alpha": independence_number(g_prime),
        "gamma_infinity": eternal_number(g_prime),
        "theta": chromatic_number(h_prime),
    }
    full_parameters = {
        "gamma": domination_number(g),
        "i": independent_domination_number(g),
        "alpha": independence_number(g),
        "gamma_infinity": eternal_number(g),
        "theta": chromatic_number(h),
    }
    assert set(deletion_parameters.values()) == {3}
    assert full_parameters == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 4,
        "theta": 4,
    }

    payload = {
        "schema": "inactive-c5-boundary-control-v1",
        "deletion_graph6_labeled": graph6(g_prime),
        "full_graph6_labeled": graph6(g),
        "deletion_parameters": deletion_parameters,
        "full_parameters": full_parameters,
        "target": TARGET,
        "full_static_state": sorted(ROOT),
        "active_set": sorted(ACTIVE),
        "inactive_set_R": sorted(INACTIVE),
        "H_prime_edges": [list(edge) for edge in sorted(H_PRIME_EDGES)],
        "deletion_triangles": [sorted(t) for t in deletion_triangles],
        "ridge_components": [list(component) for component in components],
        "proper_deletion_3_colorings": len(colorings),
        "static_response_lists": static_lists,
        "greatest_family_sizes": {
            "deletion_k3": len(greatest_family(g_prime, 3)),
            "full_k3": len(greatest_family(g, 3)),
            "full_k4": len(greatest_family(g, 4)),
        },
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    (HERE / "control_result.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
