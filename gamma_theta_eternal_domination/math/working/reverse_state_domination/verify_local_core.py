#!/usr/bin/env python3
"""Exhaust the six-vertex local core of reverse-state domination.

This is a proof sanity check, not a graph-universe coverage computation.
It checks all edge assignments left free by the local argument, including
the possible identities a=p and a=q.
"""

from __future__ import annotations

import itertools
import json


def edge(u: str, v: str) -> frozenset[str]:
    if u == v:
        raise ValueError("loops are not edges")
    return frozenset((u, v))


def dominates_vertex(
    state: frozenset[str],
    vertex: str,
    edges: frozenset[frozenset[str]],
) -> bool:
    return vertex in state or any(edge(guard, vertex) in edges for guard in state)


def check_case(a_value: str) -> dict[str, int | str]:
    aliases = {"u": "u", "x": "x", "p": "p", "q": "q", "r": "r", "a": a_value}
    vertices = tuple(sorted(set(aliases.values())))
    possible_edges = tuple(
        edge(left, right) for left, right in itertools.combinations(vertices, 2)
    )

    required_edges = {edge("u", "x"), edge("x", "r")}
    forbidden_pairs = (
        ("x", "p"),
        ("x", "q"),
        ("p", "q"),
        ("r", "u"),
        ("r", "p"),
        ("r", "q"),
        ("u", aliases["a"]),
        ("r", aliases["a"]),
    )
    forbidden_edges = {
        edge(left, right) for left, right in forbidden_pairs if left != right
    }

    counts = {
        "all_assignments": 0,
        "base_hypotheses": 0,
        "D_locally_dominates_p_q": 0,
        "closure_at_p_has_locally_dominating_successor": 0,
    }

    for bits in range(1 << len(possible_edges)):
        counts["all_assignments"] += 1
        edges = frozenset(
            possible_edges[index]
            for index in range(len(possible_edges))
            if bits & (1 << index)
        )
        if not required_edges.issubset(edges):
            continue
        if forbidden_edges.intersection(edges):
            continue
        counts["base_hypotheses"] += 1

        D = frozenset(("x", "r", aliases["a"]))
        if len(D) != 3:
            raise AssertionError("D must remain a triple in every identity case")
        if not all(dominates_vertex(D, target, edges) for target in ("p", "q")):
            continue
        counts["D_locally_dominates_p_q"] += 1

        # If p=a, then p is occupied and this closure obligation is not
        # invoked.  The preceding local-domination test must already have
        # eliminated the case because D misses q.
        if "p" in D:
            raise AssertionError("the a=p case survived local domination")

        has_acceptable_successor = False
        for guard in D:
            if edge(guard, "p") not in edges:
                continue
            successor = D.difference({guard}) | {"p"}
            if dominates_vertex(successor, "q", edges):
                has_acceptable_successor = True
                break
        if has_acceptable_successor:
            counts["closure_at_p_has_locally_dominating_successor"] += 1

    assert counts["closure_at_p_has_locally_dominating_successor"] == 0
    return {"a_identity": a_value, **counts}


def main() -> None:
    cases = [check_case("p"), check_case("q"), check_case("a")]
    assert all(
        case["closure_at_p_has_locally_dominating_successor"] == 0
        for case in cases
    )
    result = {
        "schema": "reverse-state-domination-local-core-v1",
        "classification": "LOCAL_SANITY_CHECK",
        "cases": cases,
        "conclusion": (
            "No local edge assignment satisfies the reverse-state "
            "non-domination hypothesis together with the necessary "
            "domination and one-guard closure consequences for D."
        ),
        "scope_guardrail": (
            "This exhausts only the proof's local edge cases. The "
            "all-graph theorem is established by the accompanying "
            "mathematical proof, not by finite graph enumeration."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
