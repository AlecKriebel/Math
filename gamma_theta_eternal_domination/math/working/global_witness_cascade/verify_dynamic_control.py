#!/usr/bin/env python3
"""Standalone verifier for the all-dynamic three-witness control."""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def graph6(order: int, edges: set[tuple[int, int]]) -> str:
    bits = [
        int((u, v) in edges)
        for v in range(1, order)
        for u in range(v)
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


def dominates(
    state: tuple[int, ...],
    order: int,
    g_edges: set[tuple[int, int]],
) -> bool:
    occupied = set(state)
    return all(
        vertex in occupied
        or any(pair(vertex, guard) in g_edges for guard in state)
        for vertex in range(order)
    )


def independent(
    state: tuple[int, ...],
    g_edges: set[tuple[int, int]],
) -> bool:
    return all(pair(u, v) not in g_edges for u, v in combinations(state, 2))


def greatest_family(
    order: int,
    g_edges: set[tuple[int, int]],
) -> set[tuple[int, int, int]]:
    family = {
        state
        for state in combinations(range(order), 3)
        if dominates(state, order, g_edges)
    }
    while True:
        remove = set()
        for state in family:
            for attacked in range(order):
                if attacked in state:
                    continue
                if not any(
                    pair(guard, attacked) in g_edges
                    and tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    )
                    in family
                    for guard in state
                ):
                    remove.add(state)
                    break
        if not remove:
            return family
        family -= remove


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = json.loads(args.check.read_text(encoding="utf-8"))
    order = int(data["order"])
    h_edges = {
        pair(int(u), int(v)) for u, v in data["h_edges"]
    }
    all_edges = set(combinations(range(order), 2))
    g_edges = all_edges - h_edges
    family = {
        tuple(int(vertex) for vertex in state)
        for state in data["selected_family"]
    }
    if any(tuple(sorted(state)) != state or len(state) != 3 for state in family):
        raise RuntimeError("malformed family state")
    if len(family) != int(data["selected_family_size"]):
        raise RuntimeError("family size mismatch")
    serialization = "\n".join(
        ",".join(map(str, state)) for state in sorted(family)
    ).encode("ascii")
    if sha256(serialization).hexdigest() != data["selected_family_sha256"]:
        raise RuntimeError("family hash mismatch")

    if graph6(order, g_edges) != data["graph6"]:
        raise RuntimeError("graph6 mismatch")
    if len(g_edges) != int(data["size"]):
        raise RuntimeError("edge-count mismatch")
    if not all(dominates(state, order, g_edges) for state in family):
        raise RuntimeError("family contains a nondominating state")

    obligations = 0
    for state in family:
        for attacked in range(order):
            if attacked in state:
                continue
            obligations += 1
            if not any(
                pair(guard, attacked) in g_edges
                and tuple(sorted((set(state) - {guard}) | {attacked}))
                in family
                for guard in state
            ):
                raise RuntimeError(
                    f"failed attack obligation {state}, {attacked}"
                )

    anchor = {0, 1, 2}
    lists = {
        vertex: [
            omitted
            for omitted in range(3)
            if tuple(sorted((anchor - {omitted}) | {vertex})) in family
        ]
        for vertex in range(3, order)
    }
    expected_lists = {
        int(vertex): [int(color) for color in colors]
        for vertex, colors in data["direct_lists"].items()
    }
    if lists != expected_lists:
        raise RuntimeError("direct response-list mismatch")
    if any(len(colors) != 2 for colors in lists.values()):
        raise RuntimeError("an outside list is not exact-two")

    dominating_pairs = [
        state
        for state in combinations(range(order), 2)
        if dominates(state, order, g_edges)
    ]
    if any(
        dominates((vertex,), order, g_edges) for vertex in range(order)
    ):
        raise RuntimeError("unexpected dominating singleton")
    if len(dominating_pairs) != int(data["dominating_pair_count"]):
        raise RuntimeError("dominating-pair count mismatch")
    if not any(independent(state, g_edges) for state in dominating_pairs):
        raise RuntimeError("no independent dominating pair")
    if not independent((0, 1, 2), g_edges):
        raise RuntimeError("anchor is not independent")
    if any(
        independent(state, g_edges)
        for state in combinations(range(order), 4)
    ):
        raise RuntimeError("independent four-set found")

    coloring = [int(color) for color in data["h_coloring"]]
    if len(coloring) != order or max(coloring) >= 3 or min(coloring) < 0:
        raise RuntimeError("malformed three-coloring")
    if any(coloring[u] == coloring[v] for u, v in h_edges):
        raise RuntimeError("invalid complement coloring")
    if not all(pair(u, v) in h_edges for u, v in combinations((0, 1, 2), 2)):
        raise RuntimeError("anchor is not an H-triangle")

    kernel = greatest_family(order, g_edges)
    if len(kernel) != int(data["greatest_triple_family_size"]):
        raise RuntimeError("greatest-kernel size mismatch")

    # Full canonical gates: right 3,4,5; left 6,7,8; caps 9,10,11;
    # original ports 12,13,14; physicalization middles 15,16,17.
    types = (0, 1, 2)
    for index in range(3):
        left = 6 + index
        right = 3 + index
        cap = 9 + index
        original = 12 + index
        middle = 15 + index
        left_type = types[index - 1]
        right_type = types[index]
        third = ({0, 1, 2} - {left_type, right_type}).pop()
        required_h = (
            (left_type, left),
            (right_type, right),
            (third, cap),
            (left, cap),
            (right, cap),
            (left, original),
            (original, middle),
            (middle, right),
        )
        if not all(pair(u, v) in h_edges for u, v in required_h):
            raise RuntimeError(f"missing full-gate edge at gate {index}")
        if pair(left, right) in h_edges:
            raise RuntimeError(f"failed incidence is not in G at gate {index}")
    for u, v in ((3, 7), (4, 8), (5, 6)):
        if pair(u, v) not in h_edges:
            raise RuntimeError("missing length-one connector")

    critical = ((4, 6, 18, 0), (5, 7, 19, 1), (3, 8, 20, 2))
    for u, v, q, omitted in critical:
        if pair(u, q) not in h_edges or pair(v, q) not in h_edges:
            raise RuntimeError("missing critical witness arm")
        if pair(omitted, q) in h_edges:
            raise RuntimeError("critical witness is not dynamic")
        if lists[q] != sorted({0, 1, 2} - {omitted}):
            raise RuntimeError("critical witness has wrong type")

    expected_parameters = {
        "gamma": 2,
        "i": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    if data["parameters"] != expected_parameters:
        raise RuntimeError("parameter declaration mismatch")

    result = {
        "schema": "dynamic-three-witness-control-verification-v1",
        "status": "PASS",
        "graph6": data["graph6"],
        "order": order,
        "size": len(g_edges),
        "parameters": expected_parameters,
        "selected_family_size": len(family),
        "greatest_triple_family_size": len(kernel),
        "attack_obligations": obligations,
        "dominating_pair_count": len(dominating_pairs),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
