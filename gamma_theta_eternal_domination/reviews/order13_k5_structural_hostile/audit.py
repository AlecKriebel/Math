#!/usr/bin/env python3
"""Solver-free hostile replay for the order-13, parameter-five note.

This script does not enumerate graph isomorphism classes and does not evaluate
eternal domination.  It freezes the reviewed note and accepted dependencies,
checks the exact textual claim boundary, and independently tests the set and
attachment identities on a few deliberately chosen synthetic graphs.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
TARGET = "math/working/order13_k5_structural.md"
EXPECTED = {
    TARGET: (
        11188,
        "1761c537ce293f1d7e36fd32786ffad0a67f2f7fe9dd4af6aceed346ccec6d37",
    ),
    "math/lemmas/simplicial_neighborhood_reduction.md": (
        6559,
        "87cdebc4177bf7703a53892f84d436c0a52eb5444a6b0ac14663284c0351b25a",
    ),
    "math/lemmas/independent_antineighborhood_projection.md": (
        6735,
        "543df545dea27669645979ce61451091140d4621f1e11cfdeeaa33437f4b5620",
    ),
    "math/lemmas/order12_frontier.md": (
        8120,
        "adb27204d33feb47933f2a4b1e381485b2e1b80c22b56a67b18586c4933c2b75",
    ),
    "reviews/simplicial_neighborhood_reduction_hostile/REVIEW.md": (
        17599,
        "2c8553a28affd20ce44cedb1f860e218b1f6c175f5aec7cb8bb0c8bccb7ac821",
    ),
    "reviews/general_neighborhood_projection_independent/REVIEW.md": (
        18548,
        "4da9ddf1b9d1f4087e5617dc6f6ae2428c0dd1ec576b8f89a3166418e4b7f7cb",
    ),
    "reviews/order12_frontier_second_review/REVIEW.md": (
        5039,
        "875447d219e5670d66be7d6e4b7ec9f9b3b03bba4d2b169b836706b624a92926",
    ),
    "results/independent_antineighborhood_projection_acceptance.json": (
        3308,
        "791de946d25442b02ada35f950cd20d5abe3497141224e340364c30818a1b5a2",
    ),
    "results/order12_frontier_acceptance.json": (
        7726,
        "e3b093085bafd124c228a29ef98c86341a45316dc02e11b565a138afe983d57a",
    ),
    "literature/sources/henning_schiermeyer_yeo_2011_p12.pdf": (
        347893,
        "418199b3a9f9c92974046a6c92b0b11b24cdec51e034f5aa23168c4bdfbb4285",
    ),
}

Vertex = int | str
Edge = frozenset[Vertex]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(first: Vertex, second: Vertex) -> Edge:
    if first == second:
        raise ValueError("loops are forbidden")
    return frozenset((first, second))


def is_clique(part: set[Vertex], edges: set[Edge]) -> bool:
    return all(
        edge(first, second) in edges
        for first in part
        for second in part
        if repr(first) < repr(second)
    )


def closed_neighborhood(
    anchors: Iterable[Vertex],
    vertices: set[Vertex],
    edges: set[Edge],
) -> set[Vertex]:
    anchor_set = set(anchors)
    return anchor_set | {
        vertex
        for vertex in vertices
        if any(edge(vertex, anchor) in edges for anchor in anchor_set if vertex != anchor)
    }


def build_graph(
    q_edges: set[Edge],
    attachment_a: set[int],
    attachment_b: set[int],
) -> tuple[set[Vertex], set[Edge]]:
    q_vertices = set(range(10))
    vertices: set[Vertex] = q_vertices | {"a", "b", "v"}
    edges = set(q_edges)
    edges |= {edge("a", q) for q in attachment_a}
    edges |= {edge("b", q) for q in attachment_b}
    edges |= {edge("v", "a"), edge("v", "b")}
    return vertices, edges


def verify_synthetic_identities() -> int:
    parts = (
        {0, 1, 2},
        {3, 4, 5},
        {6, 7},
        {8, 9},
    )
    q_vertices = set(range(10))
    q_edges = {
        edge(first, second)
        for part in parts
        for first in part
        for second in part
        if first < second
    }
    cases = (
        ({0, 1, 2}, {3, 4, 5}),
        ({0, 3, 6, 8}, {1, 4, 7, 9}),
        (set(range(10)), set()),
        ({2, 4, 6}, {0, 2, 8}),
    )
    checked = 0
    for attachment_a, attachment_b in cases:
        vertices, edges = build_graph(
            q_edges, attachment_a, attachment_b
        )
        if edge("a", "b") in edges:
            raise AssertionError("synthetic construction made ab adjacent")
        if {
            other
            for other in vertices
            if other != "v" and edge("v", other) in edges
        } != {"a", "b"}:
            raise AssertionError("v does not have exactly the named neighbors")

        # Q = G-N[v].
        projected_q = vertices - closed_neighborhood({"v"}, vertices, edges)
        if projected_q != q_vertices:
            raise AssertionError("closed-neighborhood definition of Q failed")

        # R = G-N[{a,b}] = Q-(A union B).
        projected_r = vertices - closed_neighborhood(
            {"a", "b"}, vertices, edges
        )
        if projected_r != q_vertices - (attachment_a | attachment_b):
            raise AssertionError("common-nonneighbor identity for R failed")

        # G-N[{v,q}] = Q-N_Q[q] for every q in Q.
        for q in q_vertices:
            left = vertices - closed_neighborhood({"v", q}, vertices, edges)
            q_closed = {q} | {
                other
                for other in q_vertices
                if other != q and edge(q, other) in q_edges
            }
            if left != q_vertices - q_closed:
                raise AssertionError("two-anchor projection identity failed")

        # Recover the attachment triple from the distinguished degree-two v.
        recovered_q = projected_q
        recovered_a = {
            q for q in recovered_q if edge("a", q) in edges
        }
        recovered_b = {
            q for q in recovered_q if edge("b", q) in edges
        }
        recovered_q_edges = {
            pair for pair in edges if pair <= recovered_q
        }
        if (
            recovered_q_edges != q_edges
            or recovered_a != attachment_a
            or recovered_b != attachment_b
        ):
            raise AssertionError("attachment triple reconstruction failed")

        # If an attachment is complete to a four-clique part, explicitly
        # construct the forbidden five-part clique partition.
        for anchor, mask, partner in (
            ("a", attachment_a, "b"),
            ("b", attachment_b, "a"),
        ):
            for index, part in enumerate(parts):
                if not part <= mask:
                    continue
                partition = [
                    set(other_part) | ({anchor} if position == index else set())
                    for position, other_part in enumerate(parts)
                ]
                partition.append({"v", partner})
                union = set().union(*partition)
                if (
                    len(partition) != 5
                    or union != vertices
                    or sum(map(len, partition)) != len(vertices)
                    or not all(is_clique(block, edges) for block in partition)
                ):
                    raise AssertionError(
                        "five-clique obstruction construction failed"
                    )
        checked += 1
    return checked


def main() -> None:
    bindings: dict[str, dict[str, object]] = {}
    for relative, (expected_size, expected_hash) in EXPECTED.items():
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"missing or unsafe frozen input: {relative}")
        actual_size = path.stat().st_size
        actual_hash = digest(path)
        if (actual_size, actual_hash) != (expected_size, expected_hash):
            raise RuntimeError(
                f"frozen input mismatch: {relative}: "
                f"{actual_size} {actual_hash}"
            )
        bindings[relative] = {
            "size_bytes": actual_size,
            "sha256": actual_hash,
        }

    note = (ROOT / TARGET).read_text(encoding="utf-8")
    normalized_note = " ".join(note.split())
    required_boundaries = (
        "This is a bounded working note, not an accepted campaign claim.",
        "Proposition 5 is a reduction, not an exclusion.",
        "Failure to find a survivor without those artifacts would not exclude the slice.",
        "No analytic contradiction was obtained.",
    )
    if any(marker not in normalized_note for marker in required_boundaries):
        raise RuntimeError("the reviewed note lost a required claim boundary")

    # The only arithmetic needed for the theta claim.
    if not (5 < 6 and 4 + 2 == 6 and (3 * 13) / 8 < 5):
        raise AssertionError("order-13 arithmetic check failed")

    synthetic_cases = verify_synthetic_identities()
    print(
        json.dumps(
            {
                "schema": "gamma-theta-order13-k5-structural-hostile-replay-v1",
                "target": bindings[TARGET],
                "dependency_count": len(bindings) - 1,
                "synthetic_attachment_cases": synthetic_cases,
                "broad_enumeration_performed": False,
                "network_access_required": False,
                "verdict": (
                    "ACCEPT_BOUNDED_STRUCTURAL_REDUCTION_"
                    "WITH_ATTACHMENT_NOTATION_CAVEAT"
                ),
            },
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
