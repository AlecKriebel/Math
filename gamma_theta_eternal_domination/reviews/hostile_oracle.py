#!/usr/bin/env python3
"""Review-only independent checks for the two gamma-theta evaluator stacks.

This file deliberately does not import either verifier's tests or search
driver.  Its tiny oracle represents a graph as a Boolean adjacency matrix and,
through order four, enumerates every nonempty family of dominating
configurations directly from the definition.
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
from itertools import combinations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from verifier_a.core import (  # noqa: E402
    BitGraph,
    alpha as alpha_a,
    clique_cover as clique_cover_a,
    domination_number as gamma_a,
    eternal_domination_number as eternal_number_a,
    eternal_fixed_point as eternal_family_a,
    independent_domination_number as independent_gamma_a,
    theta as theta_a,
)
from verifier_b import (  # noqa: E402
    Graph,
    clique_cover_number as theta_b,
    domination_number as gamma_b,
    eternal_domination_decision as eternal_decision_b,
    eternal_domination_number as eternal_number_b,
    find_eternal_family as eternal_family_b,
    independence_number as alpha_b,
    independent_domination_number as independent_gamma_b,
    make_eternal_certificate as make_certificate_b,
    minimum_clique_partition as clique_partition_b,
)


Matrix = tuple[tuple[bool, ...], ...]
Configuration = frozenset[int]


def matrix_from_edges(order: int, edges: tuple[tuple[int, int], ...]) -> Matrix:
    rows = [[False] * order for _ in range(order)]
    for first, second in edges:
        rows[first][second] = True
        rows[second][first] = True
    return tuple(tuple(row) for row in rows)


def edge_tuple(matrix: Matrix) -> tuple[tuple[int, int], ...]:
    return tuple(
        (first, second)
        for first in range(len(matrix))
        for second in range(first + 1, len(matrix))
        if matrix[first][second]
    )


def configurations(order: int, size: int) -> tuple[Configuration, ...]:
    if size < 0 or size > order:
        return ()
    return tuple(frozenset(candidate) for candidate in combinations(range(order), size))


def dominates(matrix: Matrix, chosen: Configuration) -> bool:
    return all(
        vertex in chosen
        or any(matrix[vertex][guard] for guard in chosen)
        for vertex in range(len(matrix))
    )


def independent(matrix: Matrix, chosen: Configuration) -> bool:
    return all(not matrix[first][second] for first, second in combinations(chosen, 2))


def gamma_oracle(matrix: Matrix) -> int:
    for size in range(len(matrix) + 1):
        if any(dominates(matrix, chosen) for chosen in configurations(len(matrix), size)):
            return size
    raise AssertionError


def independent_gamma_oracle(matrix: Matrix) -> int:
    for size in range(len(matrix) + 1):
        if any(
            independent(matrix, chosen) and dominates(matrix, chosen)
            for chosen in configurations(len(matrix), size)
        ):
            return size
    raise AssertionError


def alpha_oracle(matrix: Matrix) -> int:
    for size in range(len(matrix), -1, -1):
        if any(independent(matrix, chosen) for chosen in configurations(len(matrix), size)):
            return size
    raise AssertionError


def theta_oracle(matrix: Matrix) -> int:
    """Brute-force clique-part labels, without graph complementation."""

    order = len(matrix)
    if order == 0:
        return 0
    for part_count in range(1, order + 1):
        for assignment in product(range(part_count), repeat=order):
            if all(
                assignment[first] != assignment[second] or matrix[first][second]
                for first in range(order)
                for second in range(first + 1, order)
            ):
                return part_count
    raise AssertionError


def family_is_eternal(
    matrix: Matrix, guard_count: int, proposed: frozenset[Configuration]
) -> bool:
    if not proposed:
        return False
    vertices = frozenset(range(len(matrix)))
    for source in proposed:
        if len(source) != guard_count or not dominates(matrix, source):
            return False
        for attack in vertices - source:
            if not any(
                matrix[guard][attack]
                and frozenset((source - {guard}) | {attack}) in proposed
                for guard in source
            ):
                return False
    return True


def eternal_by_family_enumeration(matrix: Matrix, guard_count: int) -> bool:
    """Definition-level oracle used only when the state universe is tiny."""

    eligible = tuple(
        chosen
        for chosen in configurations(len(matrix), guard_count)
        if dominates(matrix, chosen)
    )
    for family_code in range(1, 1 << len(eligible)):
        family = frozenset(
            eligible[position]
            for position in range(len(eligible))
            if family_code & (1 << position)
        )
        if family_is_eternal(matrix, guard_count, family):
            return True
    return False


def eternal_by_synchronous_deletion(
    matrix: Matrix, guard_count: int
) -> frozenset[Configuration]:
    """Independent Jacobi-style fixed point for larger differential probes."""

    alive = {
        chosen
        for chosen in configurations(len(matrix), guard_count)
        if dominates(matrix, chosen)
    }
    vertices = set(range(len(matrix)))
    while alive:
        doomed = {
            source
            for source in alive
            if any(
                not any(
                    matrix[guard][attack]
                    and frozenset((source - {guard}) | {attack}) in alive
                    for guard in source
                )
                for attack in vertices - set(source)
            )
        }
        if not doomed:
            return frozenset(alive)
        alive -= doomed
    return frozenset()


def as_a(matrix: Matrix) -> BitGraph:
    return BitGraph.from_edges(len(matrix), edge_tuple(matrix))


def as_b(matrix: Matrix) -> Graph:
    return Graph.from_edges(len(matrix), edge_tuple(matrix))


def normalize_a_family(result, order: int) -> frozenset[Configuration]:
    return frozenset(
        frozenset(vertex for vertex in range(order) if mask & (1 << vertex))
        for mask in result.family
    )


def response_certificate_a_is_valid(matrix: Matrix, result) -> bool:
    family = normalize_a_family(result, len(matrix))
    if not family:
        return False
    for source_mask in result.family:
        source = frozenset(
            vertex
            for vertex in range(len(matrix))
            if source_mask & (1 << vertex)
        )
        if len(source) != result.k or not dominates(matrix, source):
            return False
        for attack in set(range(len(matrix))) - set(source):
            response = result.responses.get((source_mask, attack))
            if response is None:
                return False
            guard, target_mask = response
            if not isinstance(guard, int) or guard not in source:
                return False
            if not matrix[guard][attack]:
                return False
            target = frozenset(
                vertex
                for vertex in range(len(matrix))
                if target_mask & (1 << vertex)
            )
            if target != frozenset((source - {guard}) | {attack}):
                return False
            if target not in family or not dominates(matrix, target):
                return False
    return True


def response_certificate_b_is_valid(matrix: Matrix, certificate) -> bool:
    if certificate is None or not family_is_eternal(
        matrix, certificate.guard_count, certificate.family
    ):
        return False
    expected = {
        (source, attack)
        for source in certificate.family
        for attack in set(range(len(matrix))) - set(source)
    }
    recorded = set()
    for move in certificate.responses:
        pair = (move.source, move.attack)
        if pair in recorded or pair not in expected:
            return False
        recorded.add(pair)
        if move.guard not in move.source:
            return False
        if not matrix[move.guard][move.attack]:
            return False
        if move.target != frozenset(
            (move.source - {move.guard}) | {move.attack}
        ):
            return False
        if move.target not in certificate.family:
            return False
    return recorded == expected


def partition_is_valid(matrix: Matrix, parts: tuple[Configuration, ...]) -> bool:
    vertices = set(range(len(matrix)))
    seen: set[int] = set()
    for part in parts:
        if not part or seen.intersection(part):
            return False
        if any(
            not matrix[first][second] for first, second in combinations(part, 2)
        ):
            return False
        seen.update(part)
    return seen == vertices


def compare_to_oracles(matrix: Matrix, enumerate_families: bool) -> None:
    graph_a = as_a(matrix)
    graph_b = as_b(matrix)
    expected = (
        gamma_oracle(matrix),
        independent_gamma_oracle(matrix),
        alpha_oracle(matrix),
        theta_oracle(matrix),
    )
    actual_a = (
        gamma_a(graph_a),
        independent_gamma_a(graph_a),
        alpha_a(graph_a),
        theta_a(graph_a),
    )
    actual_b = (
        gamma_b(graph_b),
        independent_gamma_b(graph_b),
        alpha_b(graph_b),
        theta_b(graph_b),
    )
    assert actual_a == expected, (graph_a.to_graph6(), "A invariants", actual_a, expected)
    assert actual_b == expected, (graph_a.to_graph6(), "B invariants", actual_b, expected)
    cover_a = clique_cover_a(graph_a)
    parts_a = tuple(
        frozenset(
            vertex for vertex in range(len(matrix)) if part & (1 << vertex)
        )
        for part in cover_a.parts
    )
    parts_b = clique_partition_b(graph_b)
    assert cover_a.value == len(parts_a) == expected[-1]
    assert len(parts_b) == expected[-1]
    assert partition_is_valid(matrix, parts_a), (graph_a.to_graph6(), "A partition")
    assert partition_is_valid(matrix, parts_b), (graph_a.to_graph6(), "B partition")

    for guard_count in range(len(matrix) + 1):
        oracle_family = eternal_by_synchronous_deletion(matrix, guard_count)
        result_a = eternal_family_a(graph_a, guard_count)
        family_a = normalize_a_family(result_a, len(matrix))
        family_b = eternal_family_b(graph_b, guard_count) or frozenset()
        assert family_a == oracle_family, (
            graph_a.to_graph6(),
            guard_count,
            "A family",
            family_a,
            oracle_family,
        )
        assert family_b == oracle_family, (
            graph_a.to_graph6(),
            guard_count,
            "B family",
            family_b,
            oracle_family,
        )
        assert eternal_decision_b(graph_b, guard_count) == bool(oracle_family), (
            graph_a.to_graph6(),
            guard_count,
            "B decision",
        )
        if enumerate_families:
            brute = eternal_by_family_enumeration(matrix, guard_count)
            assert brute == bool(oracle_family), (
                graph_a.to_graph6(),
                guard_count,
                "fixed point versus family enumeration",
            )

    expected_eternal = next(
        size
        for size in range(len(matrix) + 1)
        if eternal_by_synchronous_deletion(matrix, size)
    )
    assert eternal_number_a(graph_a) == expected_eternal
    assert eternal_number_b(graph_b) == expected_eternal
    assert response_certificate_a_is_valid(
        matrix, eternal_family_a(graph_a, expected_eternal)
    )
    assert response_certificate_b_is_valid(
        matrix, make_certificate_b(graph_b, expected_eternal)
    )


def all_labeled(order: int):
    possible = tuple(combinations(range(order), 2))
    for code in range(1 << len(possible)):
        edges = tuple(
            edge for position, edge in enumerate(possible) if code & (1 << position)
        )
        yield matrix_from_edges(order, edges)


def cross_check_matrix(matrix: Matrix) -> None:
    graph_a = as_a(matrix)
    graph_b = as_b(matrix)
    values_a = (
        gamma_a(graph_a),
        independent_gamma_a(graph_a),
        alpha_a(graph_a),
        eternal_number_a(graph_a),
        theta_a(graph_a),
    )
    values_b = (
        gamma_b(graph_b),
        independent_gamma_b(graph_b),
        alpha_b(graph_b),
        eternal_number_b(graph_b),
        theta_b(graph_b),
    )
    assert values_a == values_b, (graph_a.to_graph6(), values_a, values_b)
    cover_a = clique_cover_a(graph_a)
    parts_a = tuple(
        frozenset(
            vertex for vertex in range(len(matrix)) if part & (1 << vertex)
        )
        for part in cover_a.parts
    )
    parts_b = clique_partition_b(graph_b)
    assert cover_a.value == len(parts_a) == values_a[-1]
    assert len(parts_b) == values_b[-1]
    assert partition_is_valid(matrix, parts_a), (graph_a.to_graph6(), "A partition")
    assert partition_is_valid(matrix, parts_b), (graph_a.to_graph6(), "B partition")
    for guard_count in range(len(matrix) + 1):
        family_a = normalize_a_family(
            eternal_family_a(graph_a, guard_count), len(matrix)
        )
        family_b = eternal_family_b(graph_b, guard_count) or frozenset()
        assert family_a == family_b, (
            graph_a.to_graph6(),
            guard_count,
            len(family_a),
            len(family_b),
        )


def parse_showg_edges(records: list[str], showg: Path) -> list[Matrix]:
    completed = subprocess.run(
        [str(showg), "-qe"],
        input="\n".join(records) + "\n",
        text=True,
        capture_output=True,
        check=True,
    )
    tokens = iter(map(int, completed.stdout.split()))
    matrices: list[Matrix] = []
    for _record in records:
        order = next(tokens)
        size = next(tokens)
        edges = tuple((next(tokens), next(tokens)) for _ in range(size))
        matrices.append(matrix_from_edges(order, edges))
    try:
        extra = next(tokens)
    except StopIteration:
        extra = None
    assert extra is None, ("unexpected showg output", extra)
    return matrices


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sync-max", type=int, default=5)
    parser.add_argument("--family-max", type=int, default=4)
    parser.add_argument("--connected-order", type=int, default=8)
    parser.add_argument("--random-count", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=270725)
    args = parser.parse_args()

    started = time.perf_counter()
    oracle_cases = 0
    for order in range(args.sync_max + 1):
        for matrix in all_labeled(order):
            compare_to_oracles(matrix, enumerate_families=order <= args.family_max)
            oracle_cases += 1

    geng = ROOT / "tools" / "nauty2_9_3" / "geng"
    showg = ROOT / "tools" / "nauty2_9_3" / "showg"
    generated = subprocess.run(
        [str(geng), "-cq", str(args.connected_order)],
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    external_matrices = parse_showg_edges(generated, showg)
    assert len(generated) == len(external_matrices)
    for record, matrix in zip(generated, external_matrices):
        assert as_a(matrix).to_graph6() == record, ("A graph6", record)
        assert as_b(matrix).to_graph6() == record, ("B graph6", record)
        parsed_a = BitGraph.from_graph6(record)
        parsed_b = Graph.from_graph6(record)
        assert tuple(
            (first, second)
            for first in range(parsed_a.n)
            for second in range(first + 1, parsed_a.n)
            if parsed_a.adj[first] & (1 << second)
        ) == edge_tuple(matrix), ("A graph6 parse", record)
        assert tuple(parsed_b.edges()) == edge_tuple(matrix), ("B graph6 parse", record)
        cross_check_matrix(matrix)

    generator = random.Random(args.seed)
    random_cases = 0
    probabilities = (0.05, 0.15, 0.3, 0.5, 0.7, 0.85, 0.95)
    for _ in range(args.random_count):
        order = generator.randint(5, 11)
        probability = generator.choice(probabilities)
        matrix = matrix_from_edges(
            order,
            tuple(
                (first, second)
                for first in range(order)
                for second in range(first + 1, order)
                if generator.random() < probability
            ),
        )
        cross_check_matrix(matrix)
        random_cases += 1

    print(
        json.dumps(
            {
                "outcome": "all hostile comparisons agreed",
                "labeled_oracle_cases": oracle_cases,
                "explicit_family_enumeration_through": args.family_max,
                "synchronous_oracle_through": args.sync_max,
                "connected_unlabeled_order": args.connected_order,
                "connected_unlabeled_cases": len(generated),
                "graph6_semantics_checked_by": str(showg),
                "random_cases": random_cases,
                "random_order_range": [5, 11],
                "seed": args.seed,
                "wall_seconds": time.perf_counter() - started,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
