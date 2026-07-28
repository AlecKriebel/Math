#!/usr/bin/env python3
"""Cross-check the fixed Hslaghb canonical-core boundary control.

The two input JSON files are produced by the campaign's structurally
independent verifier A and verifier B.  This script compares their exact
parameter projections, independently decodes graph6, checks the labeled
seven-vertex core and the two extension neighborhoods, and recomputes the
literal greatest triple kernel using ordinary frozensets.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


GRAPH6 = "Hslaghb"
LABELS = {"u": 0, "x": 1, "p": 2, "q": 3, "r": 4, "b": 5, "c": 6}
EXPECTED = {
    "graph6": GRAPH6,
    "n": 9,
    "m": 17,
    "gamma": 3,
    "i": 3,
    "alpha": 3,
    "gamma_infinity_one_guard": 4,
    "theta": 4,
}


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    payload = record.encode("ascii")
    if not payload or payload[0] > 126:
        raise ValueError("invalid graph6 record")
    order = payload[0] - 63
    if not 0 <= order <= 62:
        raise ValueError("only small graph6 records are supported")
    bits = []
    for byte in payload[1:]:
        value = byte - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 payload")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    graph = [set() for _ in range(order)]
    offset = 0
    for right in range(1, order):
        for left in range(right):
            if bits[offset]:
                graph[left].add(right)
                graph[right].add(left)
            offset += 1
    return tuple(frozenset(row) for row in graph)


def dominates(graph, state) -> bool:
    occupied = set(state)
    return all(
        target in occupied
        or any(target in graph[guard] for guard in occupied)
        for target in range(len(graph))
    )


def greatest_triple_kernel(graph):
    family = {
        frozenset(state)
        for state in itertools.combinations(range(len(graph)), 3)
        if dominates(graph, state)
    }
    initial = len(family)
    deleted_per_round = []
    while True:
        remove = set()
        for state in family:
            for target in range(len(graph)):
                if target in state:
                    continue
                if not any(
                    target in graph[guard]
                    and (state - {guard}) | {target} in family
                    for guard in state
                ):
                    remove.add(state)
                    break
        if not remove:
            break
        family.difference_update(remove)
        deleted_per_round.append(len(remove))
    return initial, deleted_per_round, family


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verifier-a", type=Path, required=True)
    parser.add_argument("--verifier-b", type=Path, required=True)
    arguments = parser.parse_args()
    result_a = json.loads(arguments.verifier_a.read_text(encoding="utf-8"))
    result_b = json.loads(arguments.verifier_b.read_text(encoding="utf-8"))
    projection_a = {key: result_a[key] for key in EXPECTED}
    projection_b = {key: result_b[key] for key in EXPECTED}
    assert projection_a == EXPECTED
    assert projection_b == EXPECTED

    graph = decode_graph6(GRAPH6)
    size = sum(map(len, graph)) // 2
    assert len(graph) == EXPECTED["n"] and size == EXPECTED["m"]

    core = set(LABELS.values())
    expected_core_g_edges = {
        frozenset((LABELS[left], LABELS[right]))
        for left, right in (
            ("u", "x"),
            ("u", "p"),
            ("u", "q"),
            ("u", "r"),
            ("p", "r"),
            ("q", "r"),
            ("p", "b"),
            ("q", "c"),
            ("x", "b"),
            ("x", "c"),
            ("b", "c"),
        )
    }
    actual_core_g_edges = {
        frozenset((left, right))
        for left, right in itertools.combinations(core, 2)
        if right in graph[left]
    }
    assert actual_core_g_edges == expected_core_g_edges

    h_core_neighborhoods = {}
    for vertex in (7, 8):
        h_neighbors = sorted(core - set(graph[vertex]))
        h_core_neighborhoods[str(vertex)] = h_neighbors
    assert h_core_neighborhoods == {
        "7": [0, 1, 2, 4, 6],
        "8": [0, 3, 4, 5],
    }

    initial, deleted_per_round, family = greatest_triple_kernel(graph)
    assert not family
    output = {
        "schema": "rank-one-ur1-boundary-control-v1",
        "graph6": GRAPH6,
        "graph6_ascii_sha256": hashlib.sha256(
            GRAPH6.encode("ascii")
        ).hexdigest(),
        "parameters": EXPECTED,
        "verifier_a_b_agreement": True,
        "core_labels": LABELS,
        "extension_H_core_neighborhoods": h_core_neighborhoods,
        "dominating_triples_initial": initial,
        "triple_kernel_deleted_per_round": deleted_per_round,
        "triple_kernel_final_size": len(family),
        "verdict": "PASS",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
