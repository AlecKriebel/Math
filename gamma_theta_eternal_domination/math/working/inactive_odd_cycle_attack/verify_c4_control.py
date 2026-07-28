#!/usr/bin/env python3
"""Standalone exact verifier for the inactive-C4 parity control."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
H_EDGES = {
    (0, 1), (0, 3), (0, 9), (0, 10), (0, 12), (0, 15),
    (1, 2), (1, 4), (1, 5), (1, 10), (1, 13), (1, 14), (1, 15),
    (2, 3), (2, 7), (2, 9), (2, 10), (2, 12), (2, 15),
    (3, 4), (3, 5), (3, 10), (3, 13), (3, 14),
    (4, 5), (4, 11), (4, 12),
    (5, 6), (5, 7), (5, 9),
    (6, 7), (6, 9), (6, 11), (6, 13),
    (7, 8), (7, 12), (7, 14),
    (8, 9), (8, 10), (8, 11), (8, 14), (8, 15),
    (9, 12), (9, 14), (10, 11),
    (11, 12), (11, 13), (11, 15), (13, 14),
}
TARGET = 15
ROOT = frozenset((5, 6, 7))


def graph(order: int, edges: set[tuple[int, int]]) -> tuple[int, ...]:
    rows = [0] * order
    for first, second in edges:
        rows[first] |= 1 << second
        rows[second] |= 1 << first
    return tuple(rows)


def complement(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    full = (1 << len(adjacency)) - 1
    return tuple(
        (full ^ (1 << vertex) ^ adjacency[vertex])
        for vertex in range(len(adjacency))
    )


def masks(order: int, size: int):
    for state in itertools.combinations(range(order), size):
        yield sum(1 << vertex for vertex in state)


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for guard in vertices(state):
        covered |= adjacency[guard]
    return covered == (1 << len(adjacency)) - 1


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    return all(not (adjacency[vertex] & state) for vertex in vertices(state))


def domination_number(adjacency: tuple[int, ...]) -> int:
    for size in range(1, len(adjacency) + 1):
        if any(dominates(adjacency, state) for state in masks(len(adjacency), size)):
            return size
    raise AssertionError("finite graph has no dominating set")


def independence_number(adjacency: tuple[int, ...]) -> int:
    for size in range(len(adjacency), -1, -1):
        if any(independent(adjacency, state) for state in masks(len(adjacency), size)):
            return size
    raise AssertionError


def independent_domination_number(adjacency: tuple[int, ...]) -> int:
    for size in range(1, len(adjacency) + 1):
        if any(
            independent(adjacency, state) and dominates(adjacency, state)
            for state in masks(len(adjacency), size)
        ):
            return size
    raise AssertionError


def greatest_family(adjacency: tuple[int, ...], size: int) -> frozenset[int]:
    order = len(adjacency)
    family = {
        state for state in masks(order, size) if dominates(adjacency, state)
    }
    changed = True
    while changed:
        changed = False
        delete: set[int] = set()
        for state in family:
            for attacked in range(order):
                if state >> attacked & 1:
                    continue
                responses = False
                for guard in vertices(state):
                    if not (adjacency[guard] >> attacked & 1):
                        continue
                    successor = (state ^ (1 << guard)) | (1 << attacked)
                    if successor in family:
                        responses = True
                        break
                if not responses:
                    delete.add(state)
                    break
        if delete:
            family.difference_update(delete)
            changed = True
    return frozenset(family)


def eternal_number(adjacency: tuple[int, ...]) -> int:
    for size in range(1, len(adjacency) + 1):
        if greatest_family(adjacency, size):
            return size
    raise AssertionError


def colorable(adjacency: tuple[int, ...], colors: int) -> bool:
    order = len(adjacency)
    assignment = [-1] * order

    def visit(colored: int) -> bool:
        if colored == order:
            return True
        candidates = [v for v in range(order) if assignment[v] < 0]
        vertex = max(
            candidates,
            key=lambda v: (
                len({assignment[u] for u in vertices(adjacency[v])
                     if assignment[u] >= 0}),
                (adjacency[v] & sum(1 << u for u in candidates)).bit_count(),
            ),
        )
        forbidden = {
            assignment[neighbor]
            for neighbor in vertices(adjacency[vertex])
            if assignment[neighbor] >= 0
        }
        for color in range(colors):
            if color in forbidden:
                continue
            assignment[vertex] = color
            if visit(colored + 1):
                return True
            assignment[vertex] = -1
        return False

    return visit(0)


def chromatic_number(adjacency: tuple[int, ...]) -> int:
    for colors in range(1, len(adjacency) + 1):
        if colorable(adjacency, colors):
            return colors
    raise AssertionError


def graph6(adjacency: tuple[int, ...]) -> str:
    order = len(adjacency)
    if order > 62:
        raise ValueError("small graph6 encoder only")
    bits = [
        int(bool(adjacency[low] & (1 << high)))
        for high in range(1, order)
        for low in range(high)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = 2 * value + bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def parameters(adjacency: tuple[int, ...]) -> dict[str, int]:
    return {
        "gamma": domination_number(adjacency),
        "i": independent_domination_number(adjacency),
        "alpha": independence_number(adjacency),
        "gamma_infinity": eternal_number(adjacency),
        "theta": chromatic_number(complement(adjacency)),
    }


def main() -> None:
    h = graph(16, H_EDGES)
    g = complement(h)
    deletion_g = tuple(
        row & ((1 << TARGET) - 1)
        for row in g[:TARGET]
    )
    kernel = greatest_family(g, 3)
    triangles = tuple(
        frozenset(state)
        for state in itertools.combinations(range(TARGET), 3)
        if all(
            h[first] >> second & 1
            for first, second in itertools.combinations(state, 2)
        )
    )

    active: set[int] = set()
    inactive: set[int] = set()
    for vertex in range(TARGET):
        containing = [state for state in triangles if vertex in state]
        assert containing
        statuses = {
            bool(g[vertex] >> TARGET & 1)
            and sum(
                1 << member
                for member in ((set(state) - {vertex}) | {TARGET})
            ) in kernel
            for state in containing
        }
        assert len(statuses) == 1
        (active if next(iter(statuses)) else inactive).add(vertex)

    root_successors = {
        guard: sum(
            1 << vertex
            for vertex in ((set(ROOT) - {guard}) | {TARGET})
        )
        for guard in ROOT
    }
    assert all(successor in kernel for successor in root_successors.values())
    assert {0, 1, 2, 3} <= inactive
    inactive_edges = {
        tuple(sorted((first, second)))
        for first, second in itertools.combinations(inactive, 2)
        if h[first] >> second & 1
    }
    assert {(0, 1), (1, 2), (2, 3), (0, 3)} <= inactive_edges
    assert (0, 2) not in inactive_edges and (1, 3) not in inactive_edges

    full_parameters = parameters(g)
    deletion_parameters = parameters(deletion_g)
    assert set(full_parameters.values()) == {3}
    assert set(deletion_parameters.values()) == {3}
    payload = {
        "schema": "inactive-c4-parity-control-v1",
        "graph6_G": graph6(g),
        "H_edges": [list(edge) for edge in sorted(H_EDGES)],
        "target": TARGET,
        "root": sorted(ROOT),
        "full_parameters": full_parameters,
        "deletion_parameters": deletion_parameters,
        "greatest_triple_kernel_size": len(kernel),
        "deletion_triangle_count": len(triangles),
        "active_set": sorted(active),
        "inactive_set": sorted(inactive),
        "inactive_induced_edges": [
            list(edge) for edge in sorted(inactive_edges)
        ],
        "named_inactive_induced_C4": [0, 1, 2, 3, 0],
        "root_full_in_greatest_kernel": True,
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    result = HERE / "c4_control.json"
    result.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
