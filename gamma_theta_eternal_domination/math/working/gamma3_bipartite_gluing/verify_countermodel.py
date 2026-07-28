#!/usr/bin/env python3
"""Standalone exact verifier for the gamma=3 static gluing countermodel.

This implementation uses ordinary Python sets and combinations.  It imports
neither the discovery scripts nor a campaign graph/game core.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
VertexSet = frozenset[int]
Graph = tuple[VertexSet, ...]

H_PRIME_EDGES = (
    (0, 3),
    (0, 4),
    (0, 7),
    (0, 8),
    (0, 9),
    (1, 3),
    (1, 5),
    (1, 6),
    (1, 8),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 7),
    (2, 9),
    (2, 10),
    (3, 6),
    (3, 7),
    (3, 9),
    (3, 10),
    (4, 6),
    (4, 8),
    (4, 10),
    (5, 7),
    (5, 8),
    (9, 10),
)
ACTIVE = frozenset((0, 4, 6, 7, 8, 9, 10))
INACTIVE = frozenset((1, 2, 3, 5))
FULL_ROOT = frozenset((0, 4, 8))
TARGET = 11


def graph_from_edges(order: int, edges: tuple[tuple[int, int], ...]) -> Graph:
    rows = [set() for _ in range(order)]
    for u, v in edges:
        if not 0 <= u < v < order:
            raise AssertionError("bad edge")
        rows[u].add(v)
        rows[v].add(u)
    return tuple(frozenset(row) for row in rows)


def complement(graph: Graph) -> Graph:
    universe = set(range(len(graph)))
    return tuple(
        frozenset(universe - {vertex} - set(graph[vertex]))
        for vertex in range(len(graph))
    )


def add_target(graph: Graph, neighborhood: VertexSet) -> Graph:
    rows = [set(row) for row in graph] + [set(neighborhood)]
    for vertex in neighborhood:
        rows[vertex].add(len(graph))
    return tuple(frozenset(row) for row in rows)


def graph6(graph: Graph) -> str:
    if len(graph) > 62:
        raise ValueError("short graph6 only")
    bits = []
    for high in range(1, len(graph)):
        for low in range(high):
            bits.append(int(high in graph[low]))
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(63 + value))
    return chr(63 + len(graph)) + "".join(payload)


def subsets(order: int, size: int):
    yield from (
        frozenset(group)
        for group in itertools.combinations(range(order), size)
    )


def independent(graph: Graph, state: VertexSet) -> bool:
    return all(graph[v].isdisjoint(state - {v}) for v in state)


def clique(graph: Graph, state: VertexSet) -> bool:
    return all(state - {v} <= graph[v] for v in state)


def dominates(graph: Graph, state: VertexSet) -> bool:
    covered = set(state)
    for vertex in state:
        covered.update(graph[vertex])
    return len(covered) == len(graph)


def gamma(graph: Graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, state) for state in subsets(len(graph), size)):
            return size
    raise AssertionError("finite graph has no dominating set")


def alpha(graph: Graph) -> int:
    for size in range(len(graph), 0, -1):
        if any(independent(graph, state) for state in subsets(len(graph), size)):
            return size
    return 0


def independent_domination(graph: Graph) -> int:
    values = []
    for size in range(1, len(graph) + 1):
        for state in subsets(len(graph), size):
            if independent(graph, state) and all(
                vertex in state or graph[vertex] & state
                for vertex in range(len(graph))
            ):
                values.append(size)
        if values:
            return min(values)
    raise AssertionError("no maximal independent set")


def coloring_partitions(graph: Graph, colors: int) -> tuple[tuple[tuple[int, ...], ...], ...]:
    order = len(graph)
    assignments = [-1] * order
    answers: set[tuple[tuple[int, ...], ...]] = set()

    def visit(vertex: int, used: int) -> None:
        if vertex == order:
            if used <= colors:
                parts = [
                    tuple(v for v in range(order) if assignments[v] == color)
                    for color in range(used)
                ]
                answers.add(tuple(sorted(parts)))
            return
        forbidden = {assignments[u] for u in graph[vertex] if assignments[u] >= 0}
        for color in range(min(used + 1, colors)):
            if color in forbidden:
                continue
            if color == used and used == colors:
                continue
            assignments[vertex] = color
            visit(vertex + 1, max(used, color + 1))
            assignments[vertex] = -1

    visit(0, 0)
    return tuple(sorted(answers))


def chromatic_number(graph: Graph) -> int:
    for colors in range(1, len(graph) + 1):
        if coloring_partitions(graph, colors):
            return colors
    raise AssertionError("no coloring")


def maximal_cliques(graph: Graph) -> tuple[VertexSet, ...]:
    answer = []
    for size in range(1, len(graph) + 1):
        for state in subsets(len(graph), size):
            if clique(graph, state) and not any(
                state < larger and clique(graph, larger)
                for larger in subsets(len(graph), size + 1)
            ):
                answer.append(state)
    # The immediate-size extension test above is sufficient for a clique.
    return tuple(answer)


def every_pair_common_neighbor(graph: Graph) -> bool:
    return all(
        graph[u] & graph[v]
        for u, v in itertools.combinations(range(len(graph)), 2)
    )


def common_neighbor_witnesses(graph: Graph) -> dict[str, int]:
    answer = {}
    for u, v in itertools.combinations(range(len(graph)), 2):
        witnesses = graph[u] & graph[v]
        if not witnesses:
            raise AssertionError(f"pair {u},{v} has no common neighbor")
        answer[f"{u}-{v}"] = min(witnesses)
    return answer


def induced_bipartition(
    graph: Graph, vertices: VertexSet
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    side: dict[int, int] = {}
    for start in sorted(vertices):
        if start in side:
            continue
        side[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for other in graph[vertex] & vertices:
                if other not in side:
                    side[other] = 1 - side[vertex]
                    queue.append(other)
                elif side[other] == side[vertex]:
                    raise AssertionError("induced graph is not bipartite")
    return (
        tuple(sorted(v for v in vertices if side[v] == 0)),
        tuple(sorted(v for v in vertices if side[v] == 1)),
    )


def triangle_facets(graph: Graph) -> tuple[VertexSet, ...]:
    return tuple(
        state for state in subsets(len(graph), 3) if clique(graph, state)
    )


def covariance_classes(
    facets: tuple[VertexSet, ...], order: int
) -> tuple[tuple[int, ...], ...]:
    parent = list(range(order))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def union(first: int, second: int) -> None:
        first_root = find(first)
        second_root = find(second)
        if first_root != second_root:
            parent[second_root] = first_root

    for first, second in itertools.combinations(facets, 2):
        if len(first & second) == 2:
            union(next(iter(first - second)), next(iter(second - first)))
    groups: dict[int, list[int]] = {}
    for vertex in range(order):
        groups.setdefault(find(vertex), []).append(vertex)
    return tuple(sorted(tuple(sorted(group)) for group in groups.values()))


def greatest_family(
    graph: Graph, size: int
) -> tuple[VertexSet, dict[VertexSet, int], list[int], dict[VertexSet, int]]:
    family = {
        state
        for state in subsets(len(graph), size)
        if dominates(graph, state)
    }
    ranks: dict[VertexSet, int] = {}
    witness_attack: dict[VertexSet, int] = {}
    removed_per_round = []
    round_number = 0
    while True:
        delete: list[tuple[VertexSet, int]] = []
        for state in sorted(family, key=lambda item: tuple(item)):
            for attack in range(len(graph)):
                if attack in state:
                    continue
                if not any(
                    attack in graph[guard]
                    and (state - {guard}) | {attack} in family
                    for guard in state
                ):
                    delete.append((state, attack))
                    break
        if not delete:
            return (
                frozenset(family),
                ranks,
                removed_per_round,
                witness_attack,
            )
        round_number += 1
        removed_per_round.append(len(delete))
        for state, attack in delete:
            family.remove(state)
            ranks[state] = round_number
            witness_attack[state] = attack


def literal_family_audit(graph: Graph, family: VertexSet) -> int:
    obligations = 0
    for state in family:
        if not dominates(graph, state):
            raise AssertionError("nondominating retained state")
        for attack in range(len(graph)):
            if attack in state:
                continue
            obligations += 1
            if not any(
                attack in graph[guard]
                and (state - {guard}) | {attack} in family
                for guard in state
            ):
                raise AssertionError("family is not one-guard closed")
    return obligations


def attack_tree(
    graph: Graph,
    root: VertexSet,
    ranks: dict[VertexSet, int],
    witness_attack: dict[VertexSet, int],
) -> dict[str, object]:
    rank = ranks[root]
    attack = witness_attack[root]
    children = []
    for guard in sorted(root):
        successor = (root - {guard}) | {attack}
        if attack not in graph[guard] or not dominates(graph, successor):
            continue
        child_rank = ranks.get(successor)
        if child_rank is None or child_rank >= rank:
            raise AssertionError("rank witness has nondecreasing successor")
        children.append(
            {
                "guard": guard,
                "successor": sorted(successor),
                "subtree": attack_tree(
                    graph, successor, ranks, witness_attack
                ),
            }
        )
    return {
        "state": sorted(root),
        "rank": rank,
        "attack": attack,
        "legal_dominating_successors": children,
    }


def main() -> None:
    h_prime = graph_from_edges(11, H_PRIME_EDGES)
    h = add_target(h_prime, INACTIVE)
    g_prime = complement(h_prime)
    g = complement(h)
    assert graph6(h_prime) == "JEhbtjKk@o_"
    assert graph6(h) == "KEhbtjKk@om_"
    assert graph6(g) == "KxU[ISrR}NP^"
    assert every_pair_common_neighbor(h_prime)
    assert every_pair_common_neighbor(h)
    assert all(h_prime[vertex] & INACTIVE for vertex in range(11))
    bipartition = induced_bipartition(h_prime, INACTIVE)
    facets = triangle_facets(h_prime)
    maximal = maximal_cliques(h_prime)
    assert set(facets) == set(maximal)
    classes = covariance_classes(facets, 11)
    assert all(
        set(block) <= ACTIVE or set(block) <= INACTIVE for block in classes
    )
    assert FULL_ROOT in facets and FULL_ROOT <= ACTIVE
    assert all(facet & ACTIVE for facet in facets)

    successor_obligations = 0
    successor_records = []
    for facet in facets:
        for guard in facet & ACTIVE:
            successor_obligations += 1
            successor = (facet - {guard}) | {TARGET}
            assert TARGET in g[guard]
            assert dominates(g, successor)
            successor_records.append(
                {
                    "facet": sorted(facet),
                    "guard": guard,
                    "successor": sorted(successor),
                }
            )

    h_prime_colorings = coloring_partitions(h_prime, 3)
    assert len(h_prime_colorings) == 1
    assert all(
        len({index for index, part in enumerate(parts) if set(part) & INACTIVE})
        == 3
        for parts in h_prime_colorings
    )
    assert not coloring_partitions(h, 3)
    assert coloring_partitions(h, 4)

    family3_prime, ranks3_prime, removed3_prime, witness3_prime = (
        greatest_family(g_prime, 3)
    )
    del ranks3_prime, removed3_prime, witness3_prime
    obligations3_prime = literal_family_audit(g_prime, family3_prime)
    family3, ranks3, removed3, witness3 = greatest_family(g, 3)
    assert not family3
    family4, _ranks4, removed4, _witness4 = greatest_family(g, 4)
    assert family4
    obligations4 = literal_family_audit(g, family4)
    root_tree = attack_tree(g, FULL_ROOT, ranks3, witness3)

    result = {
        "schema": "gamma3-bipartite-gluing-countermodel-verification-v1",
        "verdict": "PASS",
        "model": {
            "attacks": "unoccupied vertices only",
            "movement": "exactly one guard along one G-edge",
            "state_requirement": "every retained state dominates G",
        },
        "graphs": {
            "H_prime_graph6_labeled": graph6(h_prime),
            "H_graph6_labeled": graph6(h),
            "G_graph6_labeled": graph6(g),
            "H_prime_order": len(h_prime),
            "H_order": len(h),
            "H_prime_edges": [list(edge) for edge in H_PRIME_EDGES],
            "target": TARGET,
        },
        "marking": {
            "active_A": sorted(ACTIVE),
            "inactive_R": sorted(INACTIVE),
            "physical_N_H_x": sorted(h[TARGET]),
            "R_equals_physical_N_H_x": h[TARGET] == INACTIVE,
            "R_bipartition": [list(side) for side in bipartition],
            "R_total_dominates_H_prime": True,
            "R_total_domination_witness": {
                str(vertex): min(h_prime[vertex] & INACTIVE)
                for vertex in range(11)
            },
            "covariance_classes": [list(block) for block in classes],
            "covariance_is_nonvacuous": any(len(block) > 1 for block in classes),
            "full_active_root": sorted(FULL_ROOT),
        },
        "static_checks": {
            "H_prime_every_pair_common_neighbor": True,
            "H_every_pair_common_neighbor": True,
            "H_prime_common_neighbor_witnesses": (
                common_neighbor_witnesses(h_prime)
            ),
            "H_common_neighbor_witnesses": common_neighbor_witnesses(h),
            "maximal_H_prime_cliques": [
                sorted(state) for state in sorted(maximal, key=lambda x: tuple(x))
            ],
            "all_maximal_cliques_are_triangles": True,
            "every_facet_meets_A": True,
            "active_successor_obligations": successor_obligations,
            "active_target_successors": successor_records,
            "all_active_target_successors_dominate": True,
            "H_prime_three_coloring_partitions": [
                [list(part) for part in parts] for parts in h_prime_colorings
            ],
            "every_H_prime_three_coloring_uses_all_colors_on_R": True,
        },
        "parameters": {
            "G_prime": {
                "gamma": gamma(g_prime),
                "i": independent_domination(g_prime),
                "alpha": alpha(g_prime),
                "gamma_infinity": 3 if family3_prime else 4,
                "theta": chromatic_number(h_prime),
                "greatest_family_size": len(family3_prime),
                "one_guard_obligations": obligations3_prime,
            },
            "G": {
                "gamma": gamma(g),
                "i": independent_domination(g),
                "alpha": alpha(g),
                "gamma_infinity": 4,
                "theta": chromatic_number(h),
                "three_kernel_removed_per_round": removed3,
                "four_kernel_size": len(family4),
                "four_kernel_removed_per_round": removed4,
                "four_family_one_guard_obligations": obligations4,
            },
        },
        "full_root_three_guard_attack_tree": root_tree,
        "claim_boundary": {
            "static_gamma3_gluing_implication_refuted": True,
            "dynamic_equality_gluing_implication_refuted": False,
            "gamma_theta_counterexample": False,
            "reason": "the target extension has gamma_infinity 4, not 3",
        },
    }
    assert tuple(result["parameters"]["G_prime"][key] for key in (
        "gamma", "i", "alpha", "gamma_infinity", "theta"
    )) == (3, 3, 3, 3, 3)
    assert tuple(result["parameters"]["G"][key] for key in (
        "gamma", "i", "alpha", "gamma_infinity", "theta"
    )) == (3, 3, 3, 4, 4)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output = HERE / "countermodel_verification.json"
    output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
