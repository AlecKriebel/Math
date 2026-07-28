#!/usr/bin/env python3
"""Exact checks for the original-edge incidence controls.

This verifier is deliberately self-contained.  It reconstructs both graphs
from short coordinate descriptions, computes their greatest one-guard
triple kernels from the definition, and checks the physical-representative
incidence statements used in NOTE.md.
"""

from __future__ import annotations

import argparse
from collections import deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


A, B, C, Q, V, Z, U, VP, R, D, E, CP, AP = range(13)
S = frozenset((A, B, C))

WORDS = (
    (0, 0),  # a
    (1, 1),  # b
    (2, 2),  # c
    (0, 1),  # q
    (1, 2),  # v
    (1, 0),  # z
    (2, 1),  # u
    (1, 2),  # v'
    (0, 1),  # r
    (2, 0),  # d
    (0, 2),  # e
    (2, 2),  # c'
    (0, 0),  # a'
)

BASE_EXTRA_G = {
    frozenset((C, Q)),
    frozenset((A, V)),
    frozenset((V, R)),
}


def edge(first: int, second: int) -> tuple[int, int]:
    return (first, second) if first < second else (second, first)


def base_edges() -> set[tuple[int, int]]:
    answer: set[tuple[int, int]] = set()
    for first, second in combinations(range(13), 2):
        if (
            WORDS[first][0] == WORDS[second][0]
            or WORDS[first][1] == WORDS[second][1]
            or frozenset((first, second)) in BASE_EXTRA_G
        ):
            answer.add((first, second))
    return answer


def control_14() -> tuple[int, set[tuple[int, int]]]:
    graph_edges = base_edges()
    graph_edges.add(edge(R, D))
    for neighbor in (A, C, Z, U, D, CP, AP):
        graph_edges.add(edge(13, neighbor))
    return 14, graph_edges


def control_15() -> tuple[int, set[tuple[int, int]]]:
    order, graph_edges = control_14()
    assert order == 14
    graph_edges.add(edge(R, VP))
    for neighbor in (A, B, C, V, Z, VP, E, CP):
        graph_edges.add(edge(14, neighbor))
    return 15, graph_edges


def graph6_encode(order: int, graph_edges: set[tuple[int, int]]) -> str:
    bits = [
        int((low, high) in graph_edges)
        for high in range(1, order)
        for low in range(high)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = (value << 1) | bit
        payload.append(chr(63 + value))
    return chr(63 + order) + "".join(payload)


def adjacency(
    order: int, graph_edges: set[tuple[int, int]]
) -> tuple[frozenset[int], ...]:
    rows = [set() for _ in range(order)]
    for first, second in graph_edges:
        rows[first].add(second)
        rows[second].add(first)
    return tuple(frozenset(row) for row in rows)


def g_edge(
    rows: tuple[frozenset[int], ...], first: int, second: int
) -> bool:
    return second in rows[first]


def h_edge(
    rows: tuple[frozenset[int], ...], first: int, second: int
) -> bool:
    return first != second and second not in rows[first]


def dominates(
    rows: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(
        vertex in state
        or any(g_edge(rows, vertex, guard) for guard in state)
        for vertex in range(len(rows))
    )


def independent(
    rows: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(
        not g_edge(rows, first, second)
        for first, second in combinations(state, 2)
    )


def connected(rows: tuple[frozenset[int], ...]) -> bool:
    seen = {0}
    queue = [0]
    while queue:
        vertex = queue.pop()
        for neighbor in rows[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == len(rows)


def greatest_triple_family(
    rows: tuple[frozenset[int], ...]
) -> frozenset[frozenset[int]]:
    order = len(rows)
    family = {
        frozenset(state)
        for state in combinations(range(order), 3)
        if dominates(rows, frozenset(state))
    }
    while True:
        removed = set()
        for state in family:
            for attack in set(range(order)) - set(state):
                successors = {
                    frozenset((set(state) - {guard}) | {attack})
                    for guard in state
                    if g_edge(rows, guard, attack)
                }
                if not (successors & family):
                    removed.add(state)
                    break
        if not removed:
            return frozenset(family)
        family -= removed


def verify_family(
    rows: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
) -> int:
    obligations = 0
    order = len(rows)
    for state in family:
        assert dominates(rows, state)
        for attack in set(range(order)) - set(state):
            obligations += 1
            assert any(
                g_edge(rows, guard, attack)
                and frozenset((set(state) - {guard}) | {attack}) in family
                for guard in state
            )
    return obligations


def response_lists(
    rows: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
) -> dict[int, frozenset[int]]:
    return {
        vertex: frozenset(
            anchor
            for anchor in S
            if g_edge(rows, anchor, vertex)
            and frozenset((set(S) - {anchor}) | {vertex}) in family
        )
        for vertex in range(3, len(rows))
    }


def bipartition(
    rows: tuple[frozenset[int], ...], vertices: set[int]
) -> tuple[dict[int, int], dict[int, int]]:
    parity: dict[int, int] = {}
    component: dict[int, int] = {}
    component_number = 0
    for root in sorted(vertices):
        if root in parity:
            continue
        parity[root] = 0
        component[root] = component_number
        queue = deque([root])
        while queue:
            first = queue.popleft()
            for second in sorted(vertices):
                if not h_edge(rows, first, second):
                    continue
                if second not in parity:
                    parity[second] = parity[first] ^ 1
                    component[second] = component_number
                    queue.append(second)
                else:
                    assert parity[second] == (parity[first] ^ 1)
        component_number += 1
    return parity, component


def same_sign_physical_representatives(
    rows: tuple[frozenset[int], ...],
    lists: dict[int, frozenset[int]],
    port: int,
) -> list[int]:
    omitted = next(iter(set(S) - set(lists[port])))
    projected = (
        set(S) - {omitted}
    ) | {
        vertex
        for vertex, response in lists.items()
        if omitted not in response
    }
    parity, component = bipartition(rows, projected)
    return sorted(
        vertex
        for vertex, response in lists.items()
        if response == lists[port]
        and h_edge(rows, omitted, vertex)
        and component.get(vertex) == component.get(port)
        and parity.get(vertex) == parity.get(port)
    )


def direct_list_colorings(
    rows: tuple[frozenset[int], ...],
    lists: dict[int, frozenset[int]],
) -> list[dict[int, int]]:
    order = sorted(lists, key=lambda vertex: (len(lists[vertex]), vertex))
    assignment: dict[int, int] = {}
    answer: list[dict[int, int]] = []

    def visit(position: int) -> None:
        if position == len(order):
            answer.append(dict(assignment))
            return
        vertex = order[position]
        forbidden = {
            assignment[other]
            for other in assignment
            if h_edge(rows, vertex, other)
        }
        for color in sorted(lists[vertex]):
            if color not in forbidden:
                assignment[vertex] = color
                visit(position + 1)
                del assignment[vertex]

    visit(0)
    return answer


def complement_coloring(
    rows: tuple[frozenset[int], ...], color_count: int
) -> list[int] | None:
    order = len(rows)
    h_degree = [
        sum(h_edge(rows, vertex, other) for other in range(order))
        for vertex in range(order)
    ]
    vertices = sorted(range(order), key=lambda vertex: (-h_degree[vertex], vertex))
    colors = [-1] * order

    def visit(position: int) -> bool:
        if position == order:
            return True
        vertex = vertices[position]
        forbidden = {
            colors[other]
            for other in range(order)
            if colors[other] >= 0 and h_edge(rows, vertex, other)
        }
        for color in range(color_count):
            if color not in forbidden:
                colors[vertex] = color
                if visit(position + 1):
                    return True
                colors[vertex] = -1
        return False

    return colors if visit(0) else None


def family_hash(family: frozenset[frozenset[int]]) -> str:
    payload = "".join(
        ",".join(map(str, sorted(state))) + "\n"
        for state in sorted(family, key=lambda state: tuple(sorted(state)))
    ).encode("ascii")
    return sha256(payload).hexdigest()


def cap_rows(
    rows: tuple[frozenset[int], ...],
    lists: dict[int, frozenset[int]],
    first: int,
    second: int,
) -> list[dict[str, object]]:
    return [
        {
            "vertex": cap,
            "list": sorted(lists[cap]),
            "anchor_signature": sorted(
                anchor for anchor in S if h_edge(rows, anchor, cap)
            ),
        }
        for cap in range(len(rows))
        if cap not in (first, second)
        and h_edge(rows, first, cap)
        and h_edge(rows, second, cap)
    ]


def audit_control(
    name: str,
    constructor,
    expected_graph6: str,
    expected_family_size: int,
) -> tuple[dict[str, object], tuple[frozenset[int], ...]]:
    order, graph_edges = constructor()
    rows = adjacency(order, graph_edges)
    assert graph6_encode(order, graph_edges) == expected_graph6
    assert connected(rows)
    assert independent(rows, S)
    assert dominates(rows, S)
    assert not any(
        dominates(rows, frozenset(pair))
        for pair in combinations(range(order), 2)
    )
    assert not any(
        independent(rows, frozenset(group))
        for group in combinations(range(order), 4)
    )

    coloring = complement_coloring(rows, 3)
    assert coloring is not None
    assert all(
        coloring[first] != coloring[second]
        for first, second in combinations(range(order), 2)
        if h_edge(rows, first, second)
    )

    family = greatest_triple_family(rows)
    assert len(family) == expected_family_size
    assert S in family
    obligations = verify_family(rows, family)
    assert obligations == len(family) * (order - 3)
    lists = response_lists(rows, family)
    assert all(0 < len(response) < 3 for response in lists.values())
    list_colorings = direct_list_colorings(rows, lists)
    assert len(list_colorings) == 2

    record: dict[str, object] = {
        "name": name,
        "classification": "exact equality control; response formula satisfiable",
        "graph6": expected_graph6,
        "order": order,
        "size": len(graph_edges),
        "connected": True,
        "parameters": {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        },
        "greatest_triple_family_size": len(family),
        "greatest_triple_family_sha256": family_hash(family),
        "one_guard_obligations": obligations,
        "lists_at_S": {
            str(vertex): sorted(response)
            for vertex, response in lists.items()
        },
        "complement_3_coloring": coloring,
        "compatible_list_colorings": [
            {str(vertex): color for vertex, color in sorted(item.items())}
            for item in list_colorings
        ],
    }
    return record, (rows, lists)


def build_result() -> dict[str, object]:
    first, (rows14, lists14) = audit_control(
        "two-specified-edge retention failure",
        control_14,
        "MFzJbZYhlrDZdMhd_",
        177,
    )
    reps_q_14 = same_sign_physical_representatives(rows14, lists14, Q)
    assert reps_q_14 == [R]
    assert h_edge(rows14, Q, V) and h_edge(rows14, Q, D)
    assert g_edge(rows14, R, V) and g_edge(rows14, R, D)
    caps_rv_14 = cap_rows(rows14, lists14, R, V)
    caps_rd_14 = cap_rows(rows14, lists14, R, D)
    assert caps_rv_14 == [
        {"vertex": 13, "list": [A, C], "anchor_signature": [B]}
    ]
    assert caps_rd_14 == [
        {"vertex": VP, "list": [B, C], "anchor_signature": [A]}
    ]
    first["incidence_failure"] = {
        "original_port": Q,
        "unique_same_sign_physical_representative": R,
        "specified_original_clause_edges": [[Q, V], [Q, D]],
        "representative_pairs_are_G_edges": [[R, V], [R, D]],
        "tight_caps": {
            f"{R},{V}": caps_rv_14,
            f"{R},{D}": caps_rd_14,
        },
    }

    second, (rows15, lists15) = audit_control(
        "joint-endpoint physicalization failure",
        control_15,
        "NFzJbZZhlrDZdMhd|h_",
        216,
    )
    reps_q_15 = same_sign_physical_representatives(rows15, lists15, Q)
    reps_v_15 = same_sign_physical_representatives(rows15, lists15, V)
    assert reps_q_15 == [R]
    assert reps_v_15 == [VP]
    assert h_edge(rows15, Q, V)
    assert g_edge(rows15, R, VP)
    caps_15 = cap_rows(rows15, lists15, R, VP)
    assert caps_15 == [
        {"vertex": 13, "list": [A, C], "anchor_signature": [B]}
    ]
    second["incidence_failure"] = {
        "original_clause_edge": [Q, V],
        "same_sign_physical_representatives": {
            str(Q): reps_q_15,
            str(V): reps_v_15,
        },
        "all_representative_pairs_are_G_edges": [[R, VP]],
        "unique_tight_cap": caps_15,
    }

    return {
        "schema": "gamma-theta-original-edge-incidence-controls-v1",
        "universal_conjecture_resolved": False,
        "controls": [first, second],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = build_result()
    if args.check is not None:
        expected = json.loads(args.check.read_text())
        assert result == expected
        print("PASS")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
