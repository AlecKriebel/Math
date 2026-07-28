#!/usr/bin/env python3
"""Clean ordinary-set verifier for the equality-free boundary graph.

The verifier does not import campaign evaluator or search code.  It decodes
the graph6 record, recomputes gamma, i, alpha, gamma-infinity, theta, the
greatest triple-family, every attack obligation, and the stated asymmetric
complementary exchange.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


GRAPH6 = "GEjbug"
EXPECTED_EDGES = {
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
}
S = frozenset({0, 1, 2})
T = frozenset({3, 4, 5})
U = 0
X = 4


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    values = [ord(char) - 63 for char in record]
    n = values[0]
    if not (0 <= n <= 62):
        raise ValueError("only small graph6 records are accepted")
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


def edges(graph: tuple[frozenset[int], ...]) -> set[tuple[int, int]]:
    return {
        (u, v)
        for u in range(len(graph))
        for v in range(u + 1, len(graph))
        if v in graph[u]
    }


def dominates(graph: tuple[frozenset[int], ...], state: frozenset[int]) -> bool:
    return all(
        vertex in state or bool(graph[vertex] & state)
        for vertex in range(len(graph))
    )


def independent(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(v not in graph[u] for u, v in itertools.combinations(state, 2))


def maximal_independent(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return independent(graph, state) and all(
        vertex in state or bool(graph[vertex] & state)
        for vertex in range(len(graph))
    )


def subsets(n: int, size: int) -> tuple[frozenset[int], ...]:
    return tuple(frozenset(comb) for comb in itertools.combinations(range(n), size))


def minimum_size(n: int, predicate) -> int:
    for size in range(1, n + 1):
        if any(predicate(state) for state in subsets(n, size)):
            return size
    raise AssertionError("predicate has no nonempty witness")


def greatest_family(
    graph: tuple[frozenset[int], ...], size: int
) -> tuple[frozenset[frozenset[int]], tuple[int, ...]]:
    family = {
        state for state in subsets(len(graph), size) if dominates(graph, state)
    }
    waves: list[int] = []
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
            return frozenset(family), tuple(waves)
        family.difference_update(removed)
        waves.append(len(removed))


def family_digest(family: frozenset[frozenset[int]]) -> str:
    serialization = "\n".join(
        ",".join(map(str, sorted(state)))
        for state in sorted(family, key=lambda item: tuple(sorted(item)))
    ) + "\n"
    return hashlib.sha256(serialization.encode("ascii")).hexdigest()


def chromatic_number_of_complement(
    graph: tuple[frozenset[int], ...]
) -> tuple[int, tuple[int, ...]]:
    n = len(graph)
    complement = tuple(
        frozenset(range(n)) - {v} - graph[v] for v in range(n)
    )
    order = tuple(sorted(range(n), key=lambda v: (-len(complement[v]), v)))

    def coloring_with(colors: int) -> tuple[int, ...] | None:
        assignment = [-1] * n

        def visit(position: int) -> bool:
            if position == n:
                return True
            vertex = order[position]
            forbidden = {
                assignment[other]
                for other in complement[vertex]
                if assignment[other] >= 0
            }
            for color in range(colors):
                if color in forbidden:
                    continue
                assignment[vertex] = color
                if visit(position + 1):
                    return True
                assignment[vertex] = -1
            return False

        return tuple(assignment) if visit(0) else None

    for count in range(1, n + 1):
        witness = coloring_with(count)
        if witness is not None:
            return count, witness
    raise AssertionError("coloring search failed")


def verify() -> dict[str, object]:
    graph = decode_graph6(GRAPH6)
    if edges(graph) != EXPECTED_EDGES:
        raise AssertionError("graph6/edge-list mismatch")
    n = len(graph)
    gamma = minimum_size(n, lambda state: dominates(graph, state))
    independent_domination = minimum_size(
        n, lambda state: maximal_independent(graph, state)
    )
    alpha = max(
        size
        for size in range(1, n + 1)
        if any(independent(graph, state) for state in subsets(n, size))
    )
    theta, complement_coloring = chromatic_number_of_complement(graph)

    kernels: dict[int, frozenset[frozenset[int]]] = {}
    kernel_waves: dict[int, tuple[int, ...]] = {}
    gamma_infinity = None
    for size in range(1, n + 1):
        family, waves = greatest_family(graph, size)
        kernels[size] = family
        kernel_waves[size] = waves
        if family and gamma_infinity is None:
            gamma_infinity = size
    if gamma_infinity is None:
        raise AssertionError("full occupancy must be eternal")
    family = kernels[3]

    obligations = 0
    legal_moves = 0
    for state in family:
        if not dominates(graph, state):
            raise AssertionError("retained state does not dominate")
        for target in range(n):
            if target in state:
                continue
            obligations += 1
            replies = [
                guard
                for guard in state
                if target in graph[guard]
                and state - {guard} | {target} in family
            ]
            if not replies:
                raise AssertionError((sorted(state), target))
            legal_moves += len(replies)

    if not independent(graph, S) or not independent(graph, T):
        raise AssertionError("endpoint triples are not independent")
    forward = S - {U} | {X}
    reverse = T - {X} | {U}
    if forward not in family or reverse in family:
        raise AssertionError("claimed greatest-family asymmetry failed")
    if not dominates(graph, forward) or not dominates(graph, reverse):
        raise AssertionError("both exchange states should dominate")
    if X not in graph[U]:
        raise AssertionError("selected exchange is not a graph edge")

    failed_attack = 7
    failed_successors = []
    for guard in sorted(reverse):
        if failed_attack not in graph[guard]:
            continue
        successor = reverse - {guard} | {failed_attack}
        undominated = [
            vertex
            for vertex in range(n)
            if vertex not in successor and not (graph[vertex] & successor)
        ]
        failed_successors.append(
            {
                "guard": guard,
                "successor": sorted(successor),
                "undominated_vertices": undominated,
            }
        )
        if dominates(graph, successor):
            raise AssertionError("attack 7 unexpectedly has a dominating reply")
    if not failed_successors:
        raise AssertionError("failed attack has no adjacent guard")

    parameters = {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
        "gamma_infinity": gamma_infinity,
        "theta": theta,
    }
    if parameters != {
        "gamma": 2,
        "i": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }:
        raise AssertionError(parameters)

    return {
        "schema": "greatest-family-reciprocity-boundary-v1",
        "status": "VERIFIED",
        "graph": {
            "graph6": GRAPH6,
            "order": n,
            "size": len(EXPECTED_EDGES),
            "edges": [list(edge) for edge in sorted(EXPECTED_EDGES)],
            "graph6_sha256": hashlib.sha256(GRAPH6.encode("ascii")).hexdigest(),
        },
        "parameters": parameters,
        "complement_coloring": list(complement_coloring),
        "greatest_three_family": {
            "size": len(family),
            "sha256": family_digest(family),
            "states": [
                sorted(state)
                for state in sorted(family, key=lambda item: tuple(sorted(item)))
            ],
            "attack_obligations": obligations,
            "legal_retained_moves": legal_moves,
            "lower_kernel_deletion_waves": {
                str(size): list(kernel_waves[size]) for size in (1, 2)
            },
        },
        "nonreciprocal_exchange": {
            "S": sorted(S),
            "T": sorted(T),
            "u": U,
            "x": X,
            "forward_state": sorted(forward),
            "forward_in_greatest_family": True,
            "reverse_state": sorted(reverse),
            "reverse_dominates": True,
            "reverse_in_greatest_family": False,
            "failed_attack_at_reverse": failed_attack,
            "all_legal_successors_fail_domination": failed_successors,
        },
        "scope": {
            "refutes": (
                "greatest-family pairwise complementary-exchange reciprocity "
                "without the hypothesis gamma=alpha"
            ),
            "does_not_refute": (
                "reciprocity under gamma=alpha=gamma_infinity, mutual "
                "base exchange, or the gamma-theta conjecture"
            ),
        },
    }


def main() -> None:
    result = verify()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output = Path(__file__).with_name("countermodel_result.json")
    output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
