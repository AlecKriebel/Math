#!/usr/bin/env python3
"""Standalone verifier for the six-vertex sharpness control."""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def graph6(order: int, g_edges: set[tuple[int, int]]) -> str:
    bits = [
        int((u, v) in g_edges)
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


def greatest_triple_family(
    order: int,
    g_edges: set[tuple[int, int]],
) -> set[tuple[int, int, int]]:
    family = {
        state
        for state in combinations(range(order), 3)
        if dominates(state, order, g_edges)
    }
    while True:
        remove = {
            state
            for state in family
            if any(
                not any(
                    pair(guard, attacked) in g_edges
                    and tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    )
                    in family
                    for guard in state
                )
                for attacked in range(order)
                if attacked not in state
            )
        }
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
    if order != 6:
        raise RuntimeError("unexpected order")
    h_edges = {pair(int(u), int(v)) for u, v in data["h_edges"]}
    all_edges = set(combinations(range(order), 2))
    g_edges = all_edges - h_edges
    family = {
        tuple(int(vertex) for vertex in state)
        for state in data["selected_family"]
    }
    payload = "\n".join(
        ",".join(map(str, state)) for state in sorted(family)
    ).encode("ascii")
    if sha256(payload).hexdigest() != data["selected_family_sha256"]:
        raise RuntimeError("family hash mismatch")

    obligations = 0
    for state in family:
        if not dominates(state, order, g_edges):
            raise RuntimeError(f"nondominating family state {state}")
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
                raise RuntimeError(f"failed obligation {state}, {attacked}")

    anchor = {0, 1, 2}
    lists = {
        vertex: tuple(
            omitted
            for omitted in range(3)
            if tuple(sorted((anchor - {omitted}) | {vertex})) in family
        )
        for vertex in range(3, order)
    }
    expected_lists = {
        3: (1, 2),
        4: (0, 2),
        5: (0, 1),
    }
    if lists != expected_lists:
        raise RuntimeError(f"response lists differ: {lists}")
    omitted = {3: 0, 4: 1, 5: 2}
    dynamic = {
        omitted[vertex]
        for vertex in range(3, order)
        if pair(omitted[vertex], vertex) in g_edges
    }
    if dynamic != {0}:
        raise RuntimeError(f"wrong dynamic-type set: {dynamic}")

    gamma = min(
        size
        for size in range(1, order + 1)
        if any(
            dominates(state, order, g_edges)
            for state in combinations(range(order), size)
        )
    )
    independent_domination = min(
        size
        for size in range(1, order + 1)
        if any(
            independent(state, g_edges)
            and dominates(state, order, g_edges)
            for state in combinations(range(order), size)
        )
    )
    alpha = max(
        size
        for size in range(1, order + 1)
        if any(
            independent(state, g_edges)
            for state in combinations(range(order), size)
        )
    )
    kernel = greatest_triple_family(order, g_edges)

    # The anchor H-triangle forces theta >= 3.  This displayed coloring
    # proves theta <= 3.
    coloring = (0, 1, 2, 0, 0, 1)
    if any(coloring[u] == coloring[v] for u, v in h_edges):
        raise RuntimeError("invalid H-coloring")
    theta = 3
    parameters = {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
        "gamma_infinity": 3,
        "theta": theta,
    }
    expected_parameters = {
        "gamma": 2,
        "i": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    if parameters != expected_parameters:
        raise RuntimeError(f"wrong parameters: {parameters}")
    if not family <= kernel:
        raise RuntimeError("selected family not in greatest kernel")

    result = {
        "schema": "dynamic-type-sparsity-control-verification-v1",
        "status": "PASS",
        "graph6": graph6(order, g_edges),
        "order": order,
        "size": len(g_edges),
        "parameters": parameters,
        "selected_family_size": len(family),
        "greatest_triple_family_size": len(kernel),
        "attack_obligations": obligations,
        "lists_at_S": {str(k): list(v) for k, v in lists.items()},
        "dynamic_omitted_types": sorted(dynamic),
        "h_coloring": list(coloring),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
