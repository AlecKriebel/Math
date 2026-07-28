#!/usr/bin/env python3
"""Exhaust the labeled two-vertex extensions of the graph ``GEjbug``.

The 17 extension bits are the adjacencies from new vertices 8 and 9 to the
eight old vertices, plus edge 89.  Old-old edges are fixed.  The program
checks alpha=gamma=gamma_infinity=3 exactly and tests greatest-family
complementary-exchange reciprocity for all maximum independent triples.

This covers only this explicitly stated labeled extension class.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

from search_countermodel import (
    dominates,
    edge_list,
    find_violation,
    graph6,
    greatest_kernel,
    independent,
    mask_vertices,
)


BASE_EDGES = (
    (0, 3),
    (0, 4),
    (0, 5),
    (0, 7),
    (1, 3),
    (1, 5),
    (1, 6),
    (1, 7),
    (2, 4),
    (2, 5),
    (2, 6),
    (3, 6),
    (3, 7),
    (4, 6),
    (5, 7),
)


def base_adjacency() -> list[int]:
    adj = [0] * 10
    for u, v in BASE_EDGES:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def extension(mask: int) -> tuple[int, ...]:
    adj = base_adjacency()
    for old in range(8):
        if mask & (1 << old):
            adj[8] |= 1 << old
            adj[old] |= 1 << 8
        if mask & (1 << (8 + old)):
            adj[9] |= 1 << old
            adj[old] |= 1 << 9
    if mask & (1 << 16):
        adj[8] |= 1 << 9
        adj[9] |= 1 << 8
    return tuple(adj)


FOUR_SETS = tuple(
    sum(1 << v for v in comb) for comb in itertools.combinations(range(10), 4)
)
PAIRS = tuple(
    (u, v) for u in range(10) for v in range(u + 1, 10)
)


def alpha_at_most_three(adj: tuple[int, ...]) -> bool:
    return all(not independent(adj, state) for state in FOUR_SETS)


def gamma_at_least_three(adj: tuple[int, ...]) -> bool:
    all_mask = (1 << 10) - 1
    closed = tuple(adj[v] | (1 << v) for v in range(10))
    return all(
        (closed[u] | closed[v]) != all_mask for u, v in PAIRS
    )


def serialize_family(family: frozenset[int]) -> list[list[int]]:
    return [mask_vertices(state) for state in sorted(family)]


def run(args: argparse.Namespace) -> dict[str, object]:
    start = time.monotonic()
    totals = {
        "extension_masks": 0,
        "alpha_equals_three": 0,
        "gamma_equals_three": 0,
        "eternal_equality": 0,
        "independent_state_pairs": 0,
        "reciprocity_violations": 0,
    }
    first: dict[str, object] | None = None
    limit = min(args.stop, 1 << 17)
    for mask in range(args.start, limit):
        totals["extension_masks"] += 1
        adj = extension(mask)
        if not alpha_at_most_three(adj):
            continue
        totals["alpha_equals_three"] += 1  # old 012 remains independent
        if not gamma_at_least_three(adj):
            continue
        totals["gamma_equals_three"] += 1
        family, waves = greatest_kernel(adj, 3)
        if not family:
            continue
        totals["eternal_equality"] += 1
        independent_states = tuple(
            state for state in family if independent(adj, state)
        )
        totals["independent_state_pairs"] += (
            len(independent_states) * (len(independent_states) - 1) // 2
        )
        violation = find_violation(adj, family)
        if violation is None:
            continue
        totals["reciprocity_violations"] += 1
        first = {
            "extension_mask": mask,
            "extension_mask_binary": f"{mask:017b}",
            "graph6": graph6(adj),
            "edges": edge_list(adj),
            "greatest_family_size": len(family),
            "greatest_family": serialize_family(family),
            "kernel_deletion_waves": list(waves),
            "violation": violation,
        }
        if args.first_only:
            break

    payload = {
        "schema": "GEjbug-two-vertex-extension-exhaustion-v1",
        "status": (
            "COUNTERMODEL_FOUND"
            if first is not None
            else "NO_VIOLATION_IN_COMPLETED_RANGE"
        ),
        "scope": {
            "base_graph6": "GEjbug",
            "base_order": 8,
            "new_vertices": [8, 9],
            "free_bits": 17,
            "mask_range": [args.start, limit],
            "complete_labeled_extension_class": (
                args.start == 0 and limit == 1 << 17 and not args.first_only
            ),
            "old_old_edges_fixed": True,
        },
        "model": {
            "attacks": "unoccupied only",
            "movement": "one guard along one edge",
            "family": "literal greatest fixed point of dominating triples",
        },
        "totals": totals,
        "first_violation": first,
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }
    payload["sha256_without_this_field"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int, default=1 << 17)
    parser.add_argument("--first-only", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = run(args)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
