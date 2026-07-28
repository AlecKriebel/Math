#!/usr/bin/env python3
"""Standalone bitset verifier for the full-target coloring-choice control."""

from __future__ import annotations

import itertools
import json


GRAPH6 = r"Ksv`f\knJVis"
TARGET = 0
ROOT = frozenset((1, 2, 3))


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def masks(order: int, size: int):
    for group in itertools.combinations(range(order), size):
        yield sum(1 << vertex for vertex in group)


def decode_graph6(record: str) -> tuple[int, ...]:
    raw = record.encode("ascii")
    order = raw[0] - 63
    bit_count = order * (order - 1) // 2
    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if len(raw) != 1 + (bit_count + 5) // 6 or any(bits[bit_count:]):
        raise AssertionError("noncanonical short graph6")
    adjacency = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return tuple(adjacency)


def induced(
    adjacency: tuple[int, ...], retained: tuple[int, ...]
) -> tuple[int, ...]:
    index = {old: new for new, old in enumerate(retained)}
    answer = [0] * len(retained)
    for old_u in retained:
        for old_v in vertices(adjacency[old_u]):
            if old_v in index:
                answer[index[old_u]] |= 1 << index[old_v]
    return tuple(answer)


def complement(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    all_vertices = (1 << len(adjacency)) - 1
    return tuple(
        all_vertices ^ (1 << vertex) ^ row
        for vertex, row in enumerate(adjacency)
    )


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    return all(not (adjacency[vertex] & state) for vertex in vertices(state))


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in vertices(state):
        covered |= adjacency[vertex]
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
    return next(
        size
        for size in range(1, len(adjacency) + 1)
        if any(
            independent(adjacency, state) and dominates(adjacency, state)
            for state in masks(len(adjacency), size)
        )
    )


def greatest_family(adjacency: tuple[int, ...], size: int) -> frozenset[int]:
    order = len(adjacency)
    all_vertices = (1 << order) - 1
    family = frozenset(
        state
        for state in masks(order, size)
        if dominates(adjacency, state)
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


def proper_colorings(adjacency: tuple[int, ...], color_count: int):
    assignment = [-1] * len(adjacency)

    def visit():
        uncolored = [v for v, color in enumerate(assignment) if color < 0]
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
        for color in range(color_count):
            if color not in forbidden:
                assignment[vertex] = color
                yield from visit()
                assignment[vertex] = -1

    yield from visit()


def chromatic_number(adjacency: tuple[int, ...]) -> int:
    return next(
        color_count
        for color_count in range(1, len(adjacency) + 1)
        if next(proper_colorings(adjacency, color_count), None) is not None
    )


def parameter_record(adjacency: tuple[int, ...]) -> dict[str, int]:
    return {
        "gamma": domination_number(adjacency),
        "i": independent_domination_number(adjacency),
        "alpha": independence_number(adjacency),
        "gamma_infinity": eternal_number(adjacency),
        "theta": chromatic_number(complement(adjacency)),
    }


def main() -> None:
    graph = decode_graph6(GRAPH6)
    order = len(graph)
    deletion_vertices = tuple(v for v in range(order) if v != TARGET)
    deletion = induced(graph, deletion_vertices)
    family = greatest_family(graph, 3)
    root_mask = sum(1 << vertex for vertex in ROOT)

    assert independent(graph, root_mask)
    root_responses = frozenset(
        guard
        for guard in ROOT
        if graph[guard] & (1 << TARGET)
        and ((root_mask ^ (1 << guard)) | (1 << TARGET)) in family
    )
    assert root_responses == ROOT

    facets = tuple(
        state
        for state in masks(order, 3)
        if not (state & (1 << TARGET)) and independent(graph, state)
    )
    active = frozenset(
        guard
        for state in facets
        for guard in vertices(state)
        if graph[guard] & (1 << TARGET)
        and ((state ^ (1 << guard)) | (1 << TARGET)) in family
    )
    inactive = frozenset(deletion_vertices) - active
    complement_neighbors = frozenset(
        vertex
        for vertex in deletion_vertices
        if not (graph[vertex] & (1 << TARGET))
    )
    assert inactive == complement_neighbors == frozenset((6, 8, 10, 11))

    deletion_complement = complement(deletion)
    colorings = tuple(proper_colorings(deletion_complement, 3))
    color_use_counts: dict[int, int] = {}
    missing_color_counts = {0: 0, 1: 0, 2: 0}
    old_to_new = {old: new for new, old in enumerate(deletion_vertices)}
    for coloring in colorings:
        colors_on_inactive = {
            coloring[old_to_new[vertex]] for vertex in inactive
        }
        color_use_counts[len(colors_on_inactive)] = (
            color_use_counts.get(len(colors_on_inactive), 0) + 1
        )
        for color in set(range(3)) - colors_on_inactive:
            missing_color_counts[color] += 1

    assert len(colorings) == 12
    assert color_use_counts == {2: 6, 3: 6}
    assert missing_color_counts == {0: 2, 1: 2, 2: 2}

    full_parameters = parameter_record(graph)
    deletion_parameters = parameter_record(deletion)
    assert full_parameters == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    assert deletion_parameters["gamma"] == 2
    assert deletion_parameters["alpha"] == 3
    assert deletion_parameters["gamma_infinity"] == 3
    assert deletion_parameters["theta"] == 3

    payload = {
        "schema": "all-k-extension-positive-control-v1",
        "graph6_labeled": GRAPH6,
        "target": TARGET,
        "root": sorted(ROOT),
        "full_parameters": full_parameters,
        "deletion_parameters": deletion_parameters,
        "greatest_family_size_k3": len(family),
        "full_root_response": sorted(root_responses),
        "active_set": sorted(active),
        "inactive_set": sorted(inactive),
        "proper_deletion_3_colorings": len(colorings),
        "inactive_color_use_counts": {
            str(key): value for key, value in sorted(color_use_counts.items())
        },
        "missing_color_counts": {
            str(key): value for key, value in sorted(missing_color_counts.items())
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
