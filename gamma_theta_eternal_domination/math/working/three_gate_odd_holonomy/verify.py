#!/usr/bin/env python3
"""Standalone verifier for the gamma-dropped odd-boundary control."""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ORDER = 12
GRAPH6 = "KBn]r]vj]lnZ"
ANCHORS = (0, 1, 2)
H_EDGES = {
    (0, 1), (0, 2), (0, 3), (0, 7), (0, 11),
    (1, 2), (1, 4), (1, 8), (1, 9),
    (2, 5), (2, 6), (2, 10),
    (3, 7), (3, 9),
    (4, 8), (4, 10),
    (5, 6), (5, 11),
    (6, 9), (7, 10), (8, 11),
}
EXPECTED_LISTS = {
    3: (1, 2),
    4: (0, 2),
    5: (0, 1),
    6: (0, 1),
    7: (1, 2),
    8: (0, 2),
    9: (0, 2),
    10: (0, 1),
    11: (1, 2),
}
GATES = (
    # (left terminal, right terminal, cap, cap type)
    (6, 3, 9, 1),
    (7, 4, 10, 2),
    (8, 5, 11, 0),
)
CONNECTORS = ((3, 7, 0), (4, 8, 1), (5, 6, 2))


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def encode_graph6(order: int, edges: set[tuple[int, int]]) -> str:
    bits = [
        int((i, j) in edges)
        for j in range(1, order)
        for i in range(j)
    ]
    while len(bits) % 6:
        bits.append(0)
    output = [chr(order + 63)]
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        output.append(chr(value + 63))
    return "".join(output)


def decode_graph6(record: str) -> tuple[int, set[tuple[int, int]]]:
    order = ord(record[0]) - 63
    raw_bits = []
    for character in record[1:]:
        value = ord(character) - 63
        raw_bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = set()
    index = 0
    for j in range(1, order):
        for i in range(j):
            if raw_bits[index]:
                edges.add((i, j))
            index += 1
    return order, edges


def adjacency(
    order: int,
    edges: set[tuple[int, int]],
) -> tuple[frozenset[int], ...]:
    rows = [set() for _ in range(order)]
    for u, v in edges:
        rows[u].add(v)
        rows[v].add(u)
    return tuple(frozenset(row) for row in rows)


def dominates(state: tuple[int, ...], graph: tuple[frozenset[int], ...]) -> bool:
    occupied = set(state)
    return all(
        vertex in occupied or any(vertex in graph[guard] for guard in state)
        for vertex in range(len(graph))
    )


def independent(
    state: tuple[int, ...],
    graph: tuple[frozenset[int], ...],
) -> bool:
    return all(v not in graph[u] for u, v in combinations(state, 2))


def greatest_family(
    size: int,
    graph: tuple[frozenset[int], ...],
) -> set[tuple[int, ...]]:
    order = len(graph)
    family = {
        state
        for state in combinations(range(order), size)
        if dominates(state, graph)
    }
    while True:
        deleted = set()
        for state in family:
            for attacked in range(order):
                if attacked in state:
                    continue
                if not any(
                    attacked in graph[guard]
                    and tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    ) in family
                    for guard in state
                ):
                    deleted.add(state)
                    break
        if not deleted:
            return family
        family -= deleted


def chromatic_number(
    graph: tuple[frozenset[int], ...],
) -> tuple[int, tuple[int, ...]]:
    order = len(graph)

    def search(number: int) -> tuple[int, ...] | None:
        colors = [-1] * order

        def visit() -> bool:
            remaining = [v for v in range(order) if colors[v] < 0]
            if not remaining:
                return True
            vertex = max(
                remaining,
                key=lambda v: (
                    len({colors[w] for w in graph[v] if colors[w] >= 0}),
                    len(graph[v]),
                    -v,
                ),
            )
            forbidden = {
                colors[w] for w in graph[vertex] if colors[w] >= 0
            }
            for color in range(number):
                if color in forbidden:
                    continue
                colors[vertex] = color
                if visit():
                    return True
            colors[vertex] = -1
            return False

        return tuple(colors) if visit() else None

    for number in range(1, order + 1):
        coloring = search(number)
        if coloring is not None:
            return number, coloring
    raise AssertionError("unreachable")


def connected(graph: tuple[frozenset[int], ...]) -> bool:
    seen = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in graph[vertex] - seen:
            seen.add(neighbor)
            frontier.append(neighbor)
    return len(seen) == len(graph)


def canonical_family_bytes(family: set[tuple[int, ...]]) -> bytes:
    return "\n".join(
        ",".join(map(str, state)) for state in sorted(family)
    ).encode("ascii")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    all_edges = set(combinations(range(ORDER), 2))
    g_edges = all_edges - H_EDGES
    graph = adjacency(ORDER, g_edges)
    h_graph = adjacency(ORDER, H_EDGES)
    decoded_order, decoded_edges = decode_graph6(GRAPH6)
    assert decoded_order == ORDER
    assert decoded_edges == g_edges
    assert encode_graph6(ORDER, g_edges) == GRAPH6
    assert connected(graph)

    gamma = min(
        size
        for size in range(1, ORDER + 1)
        if any(
            dominates(state, graph)
            for state in combinations(range(ORDER), size)
        )
    )
    alpha = max(
        size
        for size in range(1, ORDER + 1)
        if any(
            independent(state, graph)
            for state in combinations(range(ORDER), size)
        )
    )
    independent_dominating = [
        size
        for size in range(1, ORDER + 1)
        if any(
            independent(state, graph) and dominates(state, graph)
            for state in combinations(range(ORDER), size)
        )
    ]
    theta, theta_coloring = chromatic_number(h_graph)
    families = {size: greatest_family(size, graph) for size in range(1, 4)}
    gamma_infinity = min(size for size, family in families.items() if family)
    family = families[3]

    obligations = 0
    legal_moves = 0
    response_rows = []
    for state in sorted(family):
        for attacked in range(ORDER):
            if attacked in state:
                continue
            legal = []
            for guard in state:
                successor = tuple(
                    sorted((set(state) - {guard}) | {attacked})
                )
                if attacked in graph[guard] and successor in family:
                    legal.append((guard, successor))
            assert legal
            obligations += 1
            legal_moves += len(legal)
            response_rows.append(
                f"{','.join(map(str, state))}|{attacked}|"
                + ";".join(
                    f"{guard}>{','.join(map(str, successor))}"
                    for guard, successor in legal
                )
            )

    lists = {}
    anchor_set = set(ANCHORS)
    for vertex in range(3, ORDER):
        response = tuple(
            omitted
            for omitted in ANCHORS
            if tuple(
                sorted((anchor_set - {omitted}) | {vertex})
            ) in family
        )
        lists[vertex] = response
    assert lists == EXPECTED_LISTS

    for left, right, cap, cap_type in GATES:
        assert pair(cap_type, cap) in H_EDGES
        assert pair(left, cap) in H_EDGES
        assert pair(right, cap) in H_EDGES
        boundary = tuple(sorted((cap_type, left, right)))
        assert not dominates(boundary, graph)
        assert boundary not in family
    for start, end, connector_type in CONNECTORS:
        assert pair(start, end) in H_EDGES
        assert connector_type not in lists[start]
        assert connector_type not in lists[end]
    assert sum(1 for _ in CONNECTORS) % 2 == 1

    special_pairs = ((4, 6), (5, 7), (3, 8))
    assert all(dominates(pair_state, graph) for pair_state in special_pairs)

    result = {
        "schema": "three-gate-odd-holonomy-control-v1",
        "graph6": GRAPH6,
        "order": ORDER,
        "size": len(g_edges),
        "connected": True,
        "parameters": {
            "gamma": gamma,
            "i": min(independent_dominating),
            "alpha": alpha,
            "gamma_infinity": gamma_infinity,
            "theta": theta,
        },
        "greatest_family_sizes": {
            str(size): len(value) for size, value in families.items()
        },
        "greatest_triple_family_sha256": sha256(
            canonical_family_bytes(family)
        ).hexdigest(),
        "obligations": obligations,
        "legal_moves": legal_moves,
        "response_table_sha256": sha256(
            "\n".join(response_rows).encode("ascii")
        ).hexdigest(),
        "lists": {str(vertex): list(value) for vertex, value in lists.items()},
        "theta_coloring_of_H": list(theta_coloring),
        "gates": [list(gate) for gate in GATES],
        "connectors": [list(connector) for connector in CONNECTORS],
        "special_dominating_pairs": [list(value) for value in special_pairs],
    }
    if args.check is not None:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        if result != expected:
            raise SystemExit("result mismatch")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS")


if __name__ == "__main__":
    main()
