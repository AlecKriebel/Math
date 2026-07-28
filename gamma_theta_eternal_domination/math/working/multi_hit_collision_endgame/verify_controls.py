#!/usr/bin/env python3
"""Standalone fixed controls for the multi-hit collision endgame.

This program uses ordinary Python sets, its own small graph6 decoder, and
a literal synchronous greatest-kernel calculation.  It verifies only the
two fixed controls described in NOTE.md.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    values = [ord(char) - 63 for char in record]
    if not values or not 0 <= values[0] <= 62:
        raise ValueError("only small graph6 records are supported")
    order = values[0]
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    graph = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                graph[low].add(high)
                graph[high].add(low)
            cursor += 1
    return tuple(frozenset(row) for row in graph)


def subsets(order: int, size: int) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(choice)
        for choice in itertools.combinations(range(order), size)
    )


def independent(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(v not in graph[u] for u, v in itertools.combinations(state, 2))


def dominates(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(
        vertex in state or bool(graph[vertex] & state)
        for vertex in range(len(graph))
    )


def maximal_independent(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return independent(graph, state) and dominates(graph, state)


def minimum_size(order: int, predicate) -> int:
    for size in range(1, order + 1):
        if any(predicate(state) for state in subsets(order, size)):
            return size
    raise AssertionError("no witness")


def kernel(
    graph: tuple[frozenset[int], ...], size: int
) -> tuple[set[frozenset[int]], dict[frozenset[int], int]]:
    live = {
        state
        for state in subsets(len(graph), size)
        if dominates(graph, state)
    }
    ranks: dict[frozenset[int], int] = {}
    round_number = 0
    while True:
        doomed: set[frozenset[int]] = set()
        snapshot = set(live)
        for state in snapshot:
            for target in range(len(graph)):
                if target in state:
                    continue
                if not any(
                    target in graph[guard]
                    and state - {guard} | {target} in snapshot
                    for guard in state
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return live, ranks
        round_number += 1
        for state in doomed:
            ranks[state] = round_number
        live.difference_update(doomed)


def parameters(
    graph: tuple[frozenset[int], ...],
) -> tuple[dict[str, int], set[frozenset[int]], dict[frozenset[int], int]]:
    order = len(graph)
    gamma = minimum_size(order, lambda state: dominates(graph, state))
    indep_dom = minimum_size(
        order, lambda state: maximal_independent(graph, state)
    )
    alpha = max(
        size
        for size in range(1, order + 1)
        if any(independent(graph, state) for state in subsets(order, size))
    )
    gamma_infinity = None
    triple_family: set[frozenset[int]] = set()
    triple_ranks: dict[frozenset[int], int] = {}
    for size in range(1, order + 1):
        family, ranks = kernel(graph, size)
        if family and gamma_infinity is None:
            gamma_infinity = size
        if size == 3:
            triple_family = family
            triple_ranks = ranks
    if gamma_infinity is None:
        raise AssertionError("full occupancy must survive")
    return (
        {
            "gamma": gamma,
            "i": indep_dom,
            "alpha": alpha,
            "gamma_infinity": gamma_infinity,
        },
        triple_family,
        triple_ranks,
    )


def rank(
    graph: tuple[frozenset[int], ...],
    family: set[frozenset[int]],
    ranks: dict[frozenset[int], int],
    state: frozenset[int],
) -> int | str:
    if state in family:
        return "S"
    if not dominates(graph, state):
        return 0
    return ranks[state]


def missed(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> list[int]:
    return [
        vertex
        for vertex in range(len(graph))
        if vertex not in state and not bool(graph[vertex] & state)
    ]


def active(
    graph: tuple[frozenset[int], ...],
    family: set[frozenset[int]],
    source: int,
    target: int,
) -> bool:
    for state in subsets(len(graph), 3):
        if source not in state or target in state or not independent(graph, state):
            continue
        if state - {source} | {target} in family:
            return True
    return False


def state_label(state: frozenset[int]) -> str:
    return "".join(str(vertex) for vertex in sorted(state))


def evaluate_control(
    record: str,
    labels: tuple[int, int, int, int, int],
) -> dict[str, object]:
    graph = decode_graph6(record)
    params, family, ranks = parameters(graph)
    u, x, p, q, r = labels
    endpoint = frozenset({x, p, q})
    reverse = frozenset({u, p, q})
    endpoint_hits = sorted(endpoint & graph[r])
    movers = sorted(reverse & graph[r])
    successors = []
    for guard in movers:
        successor = reverse - {guard} | {r}
        successors.append(
            {
                "guard": guard,
                "state": state_label(successor),
                "rank": rank(graph, family, ranks, successor),
                "missed": missed(graph, successor),
            }
        )
    common_xr = sorted(
        vertex
        for vertex in range(len(graph))
        if vertex not in {x, r}
        and vertex not in graph[x]
        and vertex not in graph[r]
    )
    return {
        "graph6": record,
        "parameters": params,
        "greatest_triple_family_size": len(family),
        "positive_rank_histogram": dict(
            (str(key), value)
            for key, value in sorted(Counter(ranks.values()).items())
        ),
        "labels": {"u": u, "x": x, "p": p, "q": q, "r": r},
        "endpoint": state_label(endpoint),
        "reverse": state_label(reverse),
        "reverse_rank": rank(graph, family, ranks, reverse),
        "endpoint_hits": endpoint_hits,
        "reverse_movers": movers,
        "successors": successors,
        "common_nonneighbors_xr": common_xr,
        "xr_dominates": dominates(graph, frozenset({x, r})),
        "p_to_r_active": active(graph, family, p, r),
        "r_to_p_active": active(graph, family, r, p),
        "q_to_r_active": active(graph, family, q, r),
        "r_to_q_active": active(graph, family, r, q),
    }


def main() -> None:
    gejbug = evaluate_control("GEjbug", (0, 4, 3, 5, 7))
    if gejbug["parameters"] != {
        "gamma": 2,
        "i": 2,
        "alpha": 3,
        "gamma_infinity": 3,
    }:
        raise AssertionError(gejbug)
    if gejbug["reverse_rank"] != 1:
        raise AssertionError(gejbug)
    if gejbug["endpoint_hits"] != [3, 5]:
        raise AssertionError(gejbug)
    if gejbug["reverse_movers"] != [0, 3, 5]:
        raise AssertionError(gejbug)
    if [entry["rank"] for entry in gejbug["successors"]] != [0, 0, 0]:
        raise AssertionError(gejbug)
    if gejbug["common_nonneighbors_xr"] or not gejbug["xr_dominates"]:
        raise AssertionError(gejbug)
    if not gejbug["p_to_r_active"] or not gejbug["q_to_r_active"]:
        raise AssertionError(gejbug)
    if gejbug["r_to_p_active"] or gejbug["r_to_q_active"]:
        raise AssertionError(gejbug)

    static = evaluate_control("GCOedo", (6, 0, 2, 1, 7))
    if static["parameters"] != {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 4,
    }:
        raise AssertionError(static)
    if static["reverse_rank"] != 1:
        raise AssertionError(static)
    if static["endpoint_hits"] != [0, 2]:
        raise AssertionError(static)
    if static["reverse_movers"] != [2]:
        raise AssertionError(static)
    if static["successors"] != [
        {"guard": 2, "state": "167", "rank": 0, "missed": [5]}
    ]:
        raise AssertionError(static)

    graph = decode_graph6("GCOedo")
    independent_source = frozenset({5, 6, 7})
    failed_forward = frozenset({0, 5, 7})
    if not independent(graph, independent_source):
        raise AssertionError("GCOedo source is not independent")
    if dominates(graph, failed_forward) or missed(graph, failed_forward) != [1]:
        raise AssertionError("GCOedo forward failure mismatch")

    result = {
        "schema": "multi-hit-collision-controls-v1",
        "status": "VERIFIED_FIXED_CONTROLS",
        "GEjbug": gejbug,
        "GCOedo": {
            **static,
            "independent_private_witness_source": state_label(
                independent_source
            ),
            "failed_forward_state": state_label(failed_forward),
            "failed_forward_missed": missed(graph, failed_forward),
        },
        "scope": {
            "proves": (
                "the two fixed graph controls and their literal "
                "one-guard greatest-kernel data"
            ),
            "does_not_prove": (
                "the symbolic lemmas, elimination of every collision, "
                "greatest-family reciprocity, or the gamma-theta conjecture"
            ),
        },
    }
    expected_path = Path(__file__).with_name("expected_result.json")
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    if result != expected:
        raise AssertionError("computed result differs from expected_result.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
