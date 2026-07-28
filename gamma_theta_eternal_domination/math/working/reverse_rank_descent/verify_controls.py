#!/usr/bin/env python3
"""Standalone exact controls for finite-horizon star-rank transport.

This checker imports no campaign evaluator.  It uses ordinary Python sets,
decodes four fixed graph6 records, computes the static parameters and
literal greatest triple kernel, checks every star-Lipschitz comparison in
each graph, and verifies the four displayed sharp controls.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter


GRAPHS = ("HCOe`Z{", "HCRdnat", "HEjejrr", "GEjbug")


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    values = [ord(char) - 63 for char in record]
    if not values or not (0 <= values[0] <= 62):
        raise ValueError("only small graph6 records are supported")
    n = values[0]
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    graph = [set() for _ in range(n)]
    cursor = 0
    for column in range(1, n):
        for row in range(column):
            if bits[cursor]:
                graph[row].add(column)
                graph[column].add(row)
            cursor += 1
    return tuple(frozenset(neighbors) for neighbors in graph)


def subsets(n: int, size: int) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(choice) for choice in itertools.combinations(range(n), size)
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


def minimum_size(n: int, predicate) -> int:
    for size in range(1, n + 1):
        if any(predicate(state) for state in subsets(n, size)):
            return size
    raise AssertionError("no witness")


def parameters(
    graph: tuple[frozenset[int], ...],
) -> tuple[dict[str, int], set[frozenset[int]], dict[frozenset[int], int]]:
    n = len(graph)
    gamma = minimum_size(n, lambda state: dominates(graph, state))
    indep_dom = minimum_size(n, lambda state: maximal_independent(graph, state))
    alpha = max(
        size
        for size in range(1, n + 1)
        if any(independent(graph, state) for state in subsets(n, size))
    )

    gamma_inf = None
    triple_family: set[frozenset[int]] = set()
    triple_ranks: dict[frozenset[int], int] = {}
    for size in range(1, n + 1):
        family, ranks = kernel(graph, size)
        if family and gamma_inf is None:
            gamma_inf = size
        if size == 3:
            triple_family = family
            triple_ranks = ranks
    if gamma_inf is None:
        raise AssertionError("full occupancy must survive")
    return (
        {
            "gamma": gamma,
            "i": indep_dom,
            "alpha": alpha,
            "gamma_infinity": gamma_inf,
        },
        triple_family,
        triple_ranks,
    )


def kernel(
    graph: tuple[frozenset[int], ...], size: int
) -> tuple[set[frozenset[int]], dict[frozenset[int], int]]:
    family = {
        state for state in subsets(len(graph), size) if dominates(graph, state)
    }
    ranks: dict[frozenset[int], int] = {}
    round_number = 0
    while True:
        removed: set[frozenset[int]] = set()
        for state in family:
            for target in range(len(graph)):
                if target in state:
                    continue
                if not any(
                    target in graph[guard]
                    and state - {guard} | {target} in family
                    for guard in state
                ):
                    removed.add(state)
                    break
        if not removed:
            return family, ranks
        round_number += 1
        for state in removed:
            ranks[state] = round_number
        family.difference_update(removed)


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


def state_label(state: frozenset[int]) -> str:
    return "".join(map(str, sorted(state)))


def check_all_star_pairs(
    graph: tuple[frozenset[int], ...],
    family: set[frozenset[int]],
    ranks: dict[frozenset[int], int],
) -> dict[str, int]:
    n = len(graph)
    independent_triples = [
        state for state in subsets(n, 3) if independent(graph, state)
    ]
    counts: Counter[str] = Counter()
    for first_index, first in enumerate(independent_triples):
        for second in independent_triples[first_index + 1 :]:
            shared = first & second
            if not shared:
                continue
            distance = len(first - second)
            for responder in shared:
                for target in range(n):
                    if target in first or target in second:
                        continue
                    left = first - {responder} | {target}
                    right = second - {responder} | {target}
                    left_rank = rank(graph, family, ranks, left)
                    right_rank = rank(graph, family, ranks, right)
                    counts["comparisons"] += 1
                    if left_rank == "S" or right_rank == "S":
                        if left_rank != right_rank:
                            raise AssertionError(
                                ("survival mismatch", first, second, target)
                            )
                        counts["survivor_pairs"] += 1
                    else:
                        if abs(left_rank - right_rank) > distance:
                            raise AssertionError(
                                (
                                    "Lipschitz violation",
                                    first,
                                    second,
                                    responder,
                                    target,
                                    left_rank,
                                    right_rank,
                                    distance,
                                )
                            )
                        counts["finite_pairs"] += 1
                        if abs(left_rank - right_rank) == distance:
                            counts["sharp_finite_pairs"] += 1
    return dict(sorted(counts.items()))


def graph_digest(graph: tuple[frozenset[int], ...]) -> str:
    edge_text = "\n".join(
        f"{u} {v}"
        for u in range(len(graph))
        for v in range(u + 1, len(graph))
        if v in graph[u]
    ) + "\n"
    return hashlib.sha256(edge_text.encode("ascii")).hexdigest()


def evaluate() -> dict[str, object]:
    data: dict[
        str,
        tuple[
            tuple[frozenset[int], ...],
            dict[str, int],
            set[frozenset[int]],
            dict[frozenset[int], int],
        ],
    ] = {}
    summaries: dict[str, object] = {}
    for record in GRAPHS:
        graph = decode_graph6(record)
        params, family, ranks = parameters(graph)
        data[record] = (graph, params, family, ranks)
        summaries[record] = {
            "order": len(graph),
            "size": sum(len(neighbors) for neighbors in graph) // 2,
            "edge_list_sha256": graph_digest(graph),
            "parameters": params,
            "greatest_triple_family_size": len(family),
            "positive_rank_histogram": {
                str(key): value
                for key, value in sorted(Counter(ranks.values()).items())
            },
            "all_star_pairs": check_all_star_pairs(graph, family, ranks),
        }

    # Sharp unit Lipschitz control under equality.
    graph, params, family, ranks = data["HCOe`Z{"]
    if params != {"gamma": 3, "i": 3, "alpha": 3, "gamma_infinity": 3}:
        raise AssertionError(params)
    first = frozenset({0, 1, 2})
    second = frozenset({0, 1, 7})
    left = frozenset({1, 2, 8})
    right = frozenset({1, 7, 8})
    unit = {
        "graph6": "HCOe`Z{",
        "responder": 0,
        "target": 8,
        "source_states": [state_label(first), state_label(second)],
        "exchange_distance": len(first - second),
        "endpoint_states": [state_label(left), state_label(right)],
        "endpoint_ranks": [
            rank(graph, family, ranks, left),
            rank(graph, family, ranks, right),
        ],
    }
    if unit["exchange_distance"] != 1 or unit["endpoint_ranks"] != [1, 2]:
        raise AssertionError(unit)

    # Sharp distance-two Lipschitz control under equality.
    graph, params, family, ranks = data["HCRdnat"]
    if params != {"gamma": 3, "i": 3, "alpha": 3, "gamma_infinity": 3}:
        raise AssertionError(params)
    first = frozenset({0, 1, 2})
    second = frozenset({2, 3, 4})
    left = frozenset({0, 1, 8})
    right = frozenset({3, 4, 8})
    distance_two = {
        "graph6": "HCRdnat",
        "responder": 2,
        "target": 8,
        "source_states": [state_label(first), state_label(second)],
        "exchange_distance": len(first - second),
        "endpoint_states": [state_label(left), state_label(right)],
        "endpoint_ranks": [
            rank(graph, family, ranks, left),
            rank(graph, family, ranks, right),
        ],
    }
    if (
        distance_two["exchange_distance"] != 2
        or distance_two["endpoint_ranks"] != [3, 1]
    ):
        raise AssertionError(distance_two)

    # Exact single-hit rank descent.
    graph, params, family, ranks = data["HEjejrr"]
    source = frozenset({0, 1, 2})
    endpoint = frozenset({4, 5, 8})
    forward = source - {0} | {4}
    reverse = endpoint - {4} | {0}
    attack = 3
    endpoint_neighbors = sorted(endpoint & graph[attack])
    successor = reverse - {8} | {attack}
    next_endpoint = endpoint - {8} | {attack}
    single_hit = {
        "graph6": "HEjejrr",
        "parameters": params,
        "source_state": state_label(source),
        "endpoint_state": state_label(endpoint),
        "u": 0,
        "x": 4,
        "forward_state": state_label(forward),
        "forward_survives": forward in family,
        "reverse_state": state_label(reverse),
        "reverse_rank": rank(graph, family, ranks, reverse),
        "deleting_attack": attack,
        "endpoint_neighbors": endpoint_neighbors,
        "next_independent_endpoint": state_label(next_endpoint),
        "successor_state": state_label(successor),
        "successor_rank": rank(graph, family, ranks, successor),
    }
    if single_hit["forward_survives"] is not True:
        raise AssertionError(single_hit)
    if single_hit["reverse_rank"] != 2:
        raise AssertionError(single_hit)
    if endpoint_neighbors != [8] or not independent(graph, next_endpoint):
        raise AssertionError(single_hit)
    if single_hit["successor_rank"] != 1:
        raise AssertionError(single_hit)
    for guard in reverse & graph[attack]:
        candidate = reverse - {guard} | {attack}
        candidate_rank = rank(graph, family, ranks, candidate)
        if candidate_rank == "S" or candidate_rank >= 2:
            raise AssertionError(("not a round-two deleting attack", guard))

    # Rank-one multi-hit collision boundary.
    graph, params, family, ranks = data["GEjbug"]
    source = frozenset({0, 1, 2})
    endpoint = frozenset({3, 4, 5})
    forward = source - {0} | {4}
    reverse = endpoint - {4} | {0}
    attack = 7
    legal_successors = []
    for guard in sorted(reverse & graph[attack]):
        candidate = reverse - {guard} | {attack}
        legal_successors.append(
            {
                "guard": guard,
                "state": state_label(candidate),
                "rank": rank(graph, family, ranks, candidate),
            }
        )
    collision = {
        "graph6": "GEjbug",
        "parameters": params,
        "source_state": state_label(source),
        "endpoint_state": state_label(endpoint),
        "u": 0,
        "x": 4,
        "forward_state": state_label(forward),
        "forward_survives": forward in family,
        "reverse_state": state_label(reverse),
        "reverse_rank": rank(graph, family, ranks, reverse),
        "deleting_attack": attack,
        "endpoint_neighbors": sorted(endpoint & graph[attack]),
        "legal_successors": legal_successors,
    }
    if collision["forward_survives"] is not True:
        raise AssertionError(collision)
    if collision["reverse_rank"] != 1:
        raise AssertionError(collision)
    if collision["endpoint_neighbors"] != [3, 5]:
        raise AssertionError(collision)
    if any(item["rank"] != 0 for item in legal_successors):
        raise AssertionError(collision)

    return {
        "schema": "reverse-rank-descent-controls-v1",
        "status": "VERIFIED",
        "graphs": summaries,
        "sharp_unit_lipschitz": unit,
        "sharp_distance_two_lipschitz": distance_two,
        "single_hit_exact_descent": single_hit,
        "rank_one_collision_boundary": collision,
        "scope": {
            "proves": (
                "the fixed finite controls and exhaustive star-pair checks "
                "reported here"
            ),
            "does_not_prove": (
                "the symbolic theorem, survivor reciprocity, a complete "
                "parameter case, or the gamma-theta conjecture"
            ),
        },
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
