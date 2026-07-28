#!/usr/bin/env python3
"""Standalone verifier for the even two-gate equality control.

This file imports no campaign evaluator and no SAT/search code.  It rebuilds
the graph from its displayed complement-edge list and checks the graph
parameters, greatest one-guard triple kernel, response lists, gate
incidences, and all compatible anchored list colorings.
"""

from __future__ import annotations

import argparse
from collections import deque
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


N = 14
A, B, C = S = (0, 1, 2)
X, Q0, T0, Y0, Z1, Q1, T1, Y1, Z0, U, V = range(3, 14)

H_EDGES = {
    (0, 1), (0, 2), (0, 4), (0, 5), (0, 6), (0, 11),
    (1, 2), (1, 7), (1, 8), (1, 9), (1, 10),
    (2, 3), (2, 12), (2, 13),
    (3, 4), (3, 7), (3, 8), (3, 11), (3, 12),
    (4, 5), (4, 7), (4, 8), (4, 10), (4, 13),
    (5, 6), (5, 9), (5, 11), (5, 12),
    (6, 7), (6, 8), (6, 10), (6, 13),
    (7, 9), (7, 11), (7, 13),
    (8, 9), (8, 11), (8, 13),
    (9, 10), (9, 12),
    (10, 11), (10, 13),
    (11, 13), (12, 13),
}

EXPECTED_LABELED_G6 = "MEXrtIdmdjLQqztC?"
EXPECTED_CANONICAL_G6 = "MGEFK~cfJLBi]f]Z?"
EXPECTED_FAMILY_HASH = (
    "f0c587abd7d7123c822235793049623b02165ae134dd98c22bfa316141b1eaad"
)


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def h_edge(u: int, v: int) -> bool:
    return u != v and edge(u, v) in H_EDGES


def g_edge(u: int, v: int) -> bool:
    return u != v and edge(u, v) not in H_EDGES


def graph6_encode_g() -> str:
    bits = [
        int(g_edge(low, high))
        for high in range(1, N)
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
    return chr(63 + N) + "".join(payload)


def dominates(state: frozenset[int]) -> bool:
    return all(
        vertex in state
        or any(g_edge(vertex, guard) for guard in state)
        for vertex in range(N)
    )


def independent(state: frozenset[int]) -> bool:
    return all(not g_edge(u, v) for u, v in combinations(state, 2))


def connected() -> bool:
    seen = {0}
    queue = [0]
    while queue:
        u = queue.pop()
        for v in range(N):
            if v not in seen and g_edge(u, v):
                seen.add(v)
                queue.append(v)
    return len(seen) == N


def greatest_eternal_family() -> tuple[
    frozenset[frozenset[int]], tuple[int, ...]
]:
    family = {
        frozenset(state)
        for state in combinations(range(N), 3)
        if dominates(frozenset(state))
    }
    rounds: list[int] = []
    while True:
        removed = {
            state
            for state in family
            if any(
                not any(
                    g_edge(guard, attacked)
                    and frozenset((set(state) - {guard}) | {attacked})
                    in family
                    for guard in state
                )
                for attacked in range(N)
                if attacked not in state
            )
        }
        if not removed:
            return frozenset(family), tuple(rounds)
        rounds.append(len(removed))
        family -= removed


def family_hash(family: frozenset[frozenset[int]]) -> str:
    payload = "".join(
        ",".join(map(str, sorted(state))) + "\n"
        for state in sorted(family, key=lambda item: tuple(sorted(item)))
    ).encode("ascii")
    return sha256(payload).hexdigest()


def response_lists(
    family: frozenset[frozenset[int]],
) -> dict[int, frozenset[int]]:
    reference = set(S)
    return {
        vertex: frozenset(
            anchor
            for anchor in S
            if frozenset((reference - {anchor}) | {vertex}) in family
        )
        for vertex in range(3, N)
    }


def complement_coloring(color_count: int) -> list[int] | None:
    colors = [-1] * N
    degrees = [
        sum(h_edge(vertex, other) for other in range(N))
        for vertex in range(N)
    ]

    def visit(colored: int) -> bool:
        if colored == N:
            return True
        uncolored = [vertex for vertex in range(N) if colors[vertex] < 0]
        vertex = max(
            uncolored,
            key=lambda item: (
                len(
                    {
                        colors[other]
                        for other in range(N)
                        if colors[other] >= 0 and h_edge(item, other)
                    }
                ),
                degrees[item],
                -item,
            ),
        )
        forbidden = {
            colors[other]
            for other in range(N)
            if colors[other] >= 0 and h_edge(vertex, other)
        }
        for color in range(color_count):
            if color not in forbidden:
                colors[vertex] = color
                if visit(colored + 1):
                    return True
                colors[vertex] = -1
        return False

    return colors if visit(0) else None


def independent_domination_number() -> int:
    for size in range(1, N + 1):
        for state in combinations(range(N), size):
            chosen = frozenset(state)
            if independent(chosen) and dominates(chosen):
                return size
    raise AssertionError("finite graph has a maximal independent set")


def bipartition(vertices: set[int]) -> tuple[dict[int, int], dict[int, int]]:
    parity: dict[int, int] = {}
    component: dict[int, int] = {}
    component_id = 0
    for root in sorted(vertices):
        if root in parity:
            continue
        parity[root] = 0
        component[root] = component_id
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in sorted(vertices):
                if not h_edge(u, v):
                    continue
                if v not in parity:
                    parity[v] = parity[u] ^ 1
                    component[v] = component_id
                    queue.append(v)
                else:
                    assert parity[v] == parity[u] ^ 1
        component_id += 1
    return parity, component


def compatible_list_colorings(
    lists: dict[int, frozenset[int]],
) -> list[dict[int, int]]:
    assignment = {A: A, B: B, C: C}
    outside = set(range(3, N))
    answers: list[dict[int, int]] = []

    def visit(uncolored: set[int]) -> None:
        if not uncolored:
            answers.append(dict(sorted(assignment.items())))
            return
        vertex = min(uncolored, key=lambda item: (len(lists[item]), item))
        forbidden = {
            assignment[other]
            for other in assignment
            if h_edge(vertex, other)
        }
        for color in sorted(lists[vertex]):
            if color not in forbidden:
                assignment[vertex] = color
                visit(uncolored - {vertex})
                del assignment[vertex]

    visit(outside)
    return answers


def build_result() -> dict[str, object]:
    assert all(u < v for u, v in H_EDGES)
    assert len(H_EDGES) == 44
    assert graph6_encode_g() == EXPECTED_LABELED_G6
    assert connected()
    assert independent(frozenset(S))
    assert dominates(frozenset(S))

    # gamma = 3.
    assert not any(
        dominates(frozenset((u, v)))
        for u, v in combinations(range(N), 2)
    )

    # alpha = 3 and i = 3.
    assert not any(
        independent(frozenset(state))
        for state in combinations(range(N), 4)
    )
    assert independent_domination_number() == 3

    family, deletion_rounds = greatest_eternal_family()
    assert len(family) == 172
    assert deletion_rounds == ()
    assert frozenset(S) in family
    assert family_hash(family) == EXPECTED_FAMILY_HASH
    obligations = 0
    for state in family:
        assert dominates(state)
        for attacked in range(N):
            if attacked in state:
                continue
            obligations += 1
            assert any(
                g_edge(guard, attacked)
                and frozenset((set(state) - {guard}) | {attacked}) in family
                for guard in state
            )
    assert obligations == 172 * 11

    lists = response_lists(family)
    expected_lists = {
        X: frozenset((A, B)),
        Q0: frozenset((B, C)),
        T0: frozenset((B, C)),
        Y0: frozenset((B, C)),
        Z1: frozenset((A, C)),
        Q1: frozenset((A, C)),
        T1: frozenset((A, C)),
        Y1: frozenset((A, C)),
        Z0: frozenset((B, C)),
        U: frozenset((A, B)),
        V: frozenset((A, B)),
    }
    assert lists == expected_lists

    # Gate 0: original clause X-Q0, same-sign path Q0-T0-Y0,
    # failed representative incidence X-Y0, and tight cap Z1.
    # Gate 1 is the cyclic counterpart.
    required_h = {
        edge(C, X),
        edge(X, Q0), edge(Q0, T0), edge(T0, Y0),
        edge(B, Z1), edge(X, Z1), edge(Y0, Z1),
        edge(X, Q1), edge(Q1, T1), edge(T1, Y1),
        edge(A, Z0), edge(X, Z0), edge(Y1, Z0),
    }
    assert required_h <= H_EDGES
    assert g_edge(X, Y0) and g_edge(X, Y1)
    assert g_edge(Y0, Z0)

    for omitted, first, middle, last in (
        (A, Q0, T0, Y0),
        (B, Q1, T1, Y1),
    ):
        projected = (
            set(S) - {omitted}
        ) | {
            vertex
            for vertex, response in lists.items()
            if omitted not in response
        }
        parity, component = bipartition(projected)
        assert component[first] == component[last]
        assert parity[first] == parity[last]
        assert h_edge(first, middle) and h_edge(middle, last)

    list_colorings = compatible_list_colorings(lists)
    assert len(list_colorings) == 2
    assert complement_coloring(2) is None
    coloring = complement_coloring(3)
    assert coloring is not None

    return {
        "schema": "gamma-theta-third-color-even-gate-control-v1",
        "classification": "exact equality control; trivial gate holonomy",
        "universal_conjecture_resolved": False,
        "labeled_graph6": EXPECTED_LABELED_G6,
        "canonical_graph6": EXPECTED_CANONICAL_G6,
        "order": N,
        "size": (N * (N - 1) // 2) - len(H_EDGES),
        "connected": True,
        "parameters": {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        },
        "greatest_triple_family_size": len(family),
        "greatest_triple_family_sha256": EXPECTED_FAMILY_HASH,
        "greatest_kernel_deletion_rounds": list(deletion_rounds),
        "one_guard_obligations": obligations,
        "lists_at_S": {
            str(vertex): sorted(response)
            for vertex, response in sorted(lists.items())
        },
        "compatible_anchored_list_colorings": [
            {str(vertex): color for vertex, color in item.items()}
            for item in list_colorings
        ],
        "one_complement_3_coloring": coloring,
        "gate_paths": [[Q0, T0, Y0], [Q1, T1, Y1]],
        "failed_joint_incidences": [[X, Y0], [X, Y1]],
        "tight_caps": [
            {"endpoints": [X, Y0], "cap": Z1},
            {"endpoints": [X, Y1], "cap": Z0},
        ],
        "absent_odd_return_edge_in_H": [Y0, Z0],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = build_result()
    if args.check is not None:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        assert result == expected
        print("PASS")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
