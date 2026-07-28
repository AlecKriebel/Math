#!/usr/bin/env python3
"""Clean-room audit of the inactive-bipartite gluing countermodel.

This checker imports no candidate or campaign code.  Graphs are represented
by Python sets, colorings by canonical set partitions, and eternal families
by frozensets of frozenset configurations.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
CANDIDATE = CAMPAIGN / "math" / "working" / "inactive_bipartite_gluing"

CANDIDATE_MANIFEST_SHA256 = (
    "c4d13fbd5834f261e786d9088843ef3e40ef9a90e552d565417ae2df87a51d4a"
)

H_PRIME_GRAPH6 = "HEhbtjK"
H_GRAPH6 = "IEhbtjKe_"
G_GRAPH6 = "IxU[ISrXW"
ACTIVE = frozenset({1, 2, 5, 7, 8})
INACTIVE = frozenset({0, 3, 4, 6})
TARGET = 9
ROOT = frozenset({1, 5, 8})

# Vertex v of H' represents BASE_EDGE[v] in K_{3,3}.
BASE_EDGE = {
    0: ("a2", "b1"),
    1: ("a0", "b2"),
    2: ("a1", "b0"),
    3: ("a0", "b1"),
    4: ("a2", "b0"),
    5: ("a1", "b2"),
    6: ("a0", "b0"),
    7: ("a1", "b1"),
    8: ("a2", "b2"),
}

EXPECTED_FACETS = {
    frozenset({1, 3, 6}),
    frozenset({2, 4, 6}),
    frozenset({0, 3, 7}),
    frozenset({2, 5, 7}),
    frozenset({0, 4, 8}),
    frozenset({1, 5, 8}),
}

EXPECTED_COLOR_PARTITIONS = {
    ((0, 1, 2), (3, 4, 5), (6, 7, 8)),
    ((0, 5, 6), (1, 4, 7), (2, 3, 8)),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph_from_edges(
    order: int, edges: set[frozenset[int]]
) -> tuple[frozenset[int], ...]:
    neighborhoods = [set() for _ in range(order)]
    for edge in edges:
        assert len(edge) == 2
        u, v = tuple(edge)
        assert 0 <= u < order and 0 <= v < order and u != v
        neighborhoods[u].add(v)
        neighborhoods[v].add(u)
    return tuple(frozenset(row) for row in neighborhoods)


def edge_set(graph: tuple[frozenset[int], ...]) -> set[frozenset[int]]:
    return {
        frozenset({u, v})
        for u in range(len(graph))
        for v in graph[u]
        if u < v
    }


def graph6_decode(record: str) -> tuple[frozenset[int], ...]:
    """Decode the small-order graph6 format directly from its bit stream."""
    assert record and record[0] != "~"
    order = ord(record[0]) - 63
    assert 0 <= order <= 62
    stream: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value <= 63
        stream.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    assert len(stream) >= needed
    assert not any(stream[needed:])
    edges: set[frozenset[int]] = set()
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if stream[cursor]:
                edges.add(frozenset({low, high}))
            cursor += 1
    return graph_from_edges(order, edges)


def graph6_encode(graph: tuple[frozenset[int], ...]) -> str:
    order = len(graph)
    assert order <= 62
    stream = [
        int(high in graph[low])
        for high in range(1, order)
        for low in range(high)
    ]
    while len(stream) % 6:
        stream.append(0)
    payload: list[str] = []
    for start in range(0, len(stream), 6):
        value = 0
        for bit in stream[start : start + 6]:
            value = 2 * value + bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def complement(
    graph: tuple[frozenset[int], ...]
) -> tuple[frozenset[int], ...]:
    vertices = set(range(len(graph)))
    return tuple(
        frozenset(vertices - {vertex} - set(graph[vertex]))
        for vertex in range(len(graph))
    )


def subsets(order: int, size: int):
    for combination in itertools.combinations(range(order), size):
        yield frozenset(combination)


def is_clique(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(v in graph[u] for u, v in itertools.combinations(state, 2))


def is_independent(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(v not in graph[u] for u, v in itertools.combinations(state, 2))


def dominates(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    covered = set(state)
    for vertex in state:
        covered.update(graph[vertex])
    return len(covered) == len(graph)


def maximal_cliques(
    graph: tuple[frozenset[int], ...]
) -> set[frozenset[int]]:
    answer: set[frozenset[int]] = set()
    order = len(graph)
    for size in range(1, order + 1):
        for state in subsets(order, size):
            if not is_clique(graph, state):
                continue
            if not any(
                all(old in graph[new] for old in state)
                for new in set(range(order)) - set(state)
            ):
                answer.add(state)
    return answer


def proper_partitions(
    graph: tuple[frozenset[int], ...], colors: int
) -> set[tuple[tuple[int, ...], ...]]:
    """Enumerate proper partitions into exactly `colors` nonempty classes.

    Restricted-growth labels remove all color-name permutations before a
    solution is recorded.
    """
    order = len(graph)
    assignment = [-1] * order
    assignment[0] = 0
    answer: set[tuple[tuple[int, ...], ...]] = set()

    def visit(vertex: int, largest_used: int) -> None:
        if vertex == order:
            if largest_used + 1 == colors:
                classes = tuple(
                    tuple(v for v, shade in enumerate(assignment) if shade == c)
                    for c in range(colors)
                )
                answer.add(tuple(sorted(classes)))
            return
        upper = min(colors - 1, largest_used + 1)
        for shade in range(upper + 1):
            if any(
                assignment[neighbor] == shade
                for neighbor in graph[vertex]
                if neighbor < vertex
            ):
                continue
            assignment[vertex] = shade
            visit(vertex + 1, max(largest_used, shade))
            assignment[vertex] = -1

    visit(1, 0)
    return answer


def chromatic_number(graph: tuple[frozenset[int], ...]) -> int:
    for colors in range(1, len(graph) + 1):
        if proper_partitions(graph, colors):
            return colors
    raise AssertionError("no coloring found")


def domination_number(graph: tuple[frozenset[int], ...]) -> int:
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, state) for state in subsets(len(graph), size)):
            return size
    raise AssertionError("no dominating set found")


def independence_number(graph: tuple[frozenset[int], ...]) -> int:
    for size in range(len(graph), -1, -1):
        if any(
            is_independent(graph, state)
            for state in subsets(len(graph), size)
        ):
            return size
    raise AssertionError("no independent set found")


def independent_domination_number(
    graph: tuple[frozenset[int], ...]
) -> int:
    for size in range(1, len(graph) + 1):
        if any(
            is_independent(graph, state) and dominates(graph, state)
            for state in subsets(len(graph), size)
        ):
            return size
    raise AssertionError("no independent dominating set found")


def legal_successors(
    graph: tuple[frozenset[int], ...],
    state: frozenset[int],
    attack: int,
) -> dict[int, frozenset[int]]:
    assert attack not in state
    return {
        guard: frozenset((set(state) - {guard}) | {attack})
        for guard in state
        if attack in graph[guard]
    }


def greatest_eternal_family(
    graph: tuple[frozenset[int], ...], size: int
) -> tuple[
    frozenset[frozenset[int]],
    dict[frozenset[int], int],
    list[int],
    int,
]:
    """Synchronous greatest-fixed-point deletion from the definition."""
    family = {
        state
        for state in subsets(len(graph), size)
        if dominates(graph, state)
    }
    initial = len(family)
    ranks: dict[frozenset[int], int] = {}
    rounds: list[int] = []
    round_number = 0
    while True:
        doomed: set[frozenset[int]] = set()
        for state in family:
            for attack in set(range(len(graph))) - set(state):
                successors = legal_successors(graph, state, attack)
                if not any(successor in family for successor in successors.values()):
                    doomed.add(state)
                    break
        if not doomed:
            return frozenset(family), ranks, rounds, initial
        round_number += 1
        rounds.append(len(doomed))
        for state in doomed:
            ranks[state] = round_number
        family.difference_update(doomed)


def eternal_number(graph: tuple[frozenset[int], ...]) -> tuple[int, dict[int, object]]:
    trace: dict[int, object] = {}
    for size in range(1, len(graph) + 1):
        family, ranks, rounds, initial = greatest_eternal_family(graph, size)
        trace[size] = {
            "dominating_states_initial": initial,
            "removed_per_round": rounds,
            "survivors": len(family),
            "maximum_deletion_rank": max(ranks.values(), default=0),
        }
        if family:
            return size, trace
    raise AssertionError("no eternal family found")


def graph_parameters(
    graph: tuple[frozenset[int], ...]
) -> tuple[dict[str, int], dict[int, object]]:
    eternal, trace = eternal_number(graph)
    return {
        "gamma": domination_number(graph),
        "i": independent_domination_number(graph),
        "alpha": independence_number(graph),
        "gamma_infinity": eternal,
        "theta": chromatic_number(complement(graph)),
    }, trace


def as_lists(states: set[frozenset[int]]) -> list[list[int]]:
    return sorted([sorted(state) for state in states])


def audit_candidate_package() -> dict[str, object]:
    manifest_path = CANDIDATE / "MANIFEST.json"
    assert sha256(manifest_path) == CANDIDATE_MANIFEST_SHA256
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["schema"] == "inactive-bipartite-gluing-package-v1"
    assert manifest["frozen_at"] == "2026-07-28T07:21:00-07:00"
    labels = [claim["label"] for claim in manifest["claims"]]
    assert labels == ["PROVED", "PROVED", "OBSERVED", "OBSERVED", "OPEN"]
    assert manifest["witness"] == {
        "H_prime_graph6": H_PRIME_GRAPH6,
        "H_with_target_graph6_labeled": H_GRAPH6,
        "G_with_target_graph6_labeled": G_GRAPH6,
        "active_A": sorted(ACTIVE),
        "inactive_R": sorted(INACTIVE),
        "full_active_root": sorted(ROOT),
    }
    checked: dict[str, str] = {}
    for relative, expected in manifest["files_sha256"].items():
        assert Path(relative).name == relative
        actual = sha256(CANDIDATE / relative)
        assert actual == expected
        checked[relative] = actual
    assert len(checked) == 8
    return {
        "manifest_sha256": CANDIDATE_MANIFEST_SHA256,
        "listed_hashes_checked": len(checked),
    }


def run() -> dict[str, object]:
    package = audit_candidate_package()

    # Reconstruct H' as L(K_{3,3}), independently of the displayed edge list.
    assert set(BASE_EDGE.values()) == {
        (f"a{i}", f"b{j}") for i in range(3) for j in range(3)
    }
    line_edges = {
        frozenset({u, v})
        for u, v in itertools.combinations(range(9), 2)
        if set(BASE_EDGE[u]) & set(BASE_EDGE[v])
    }
    h_prime = graph_from_edges(9, line_edges)
    assert graph6_decode(H_PRIME_GRAPH6) == h_prime
    assert graph6_encode(h_prime) == H_PRIME_GRAPH6
    assert len(line_edges) == 18
    assert {len(row) for row in h_prime} == {4}

    facets = maximal_cliques(h_prime)
    assert facets == EXPECTED_FACETS
    assert {len(facet) for facet in facets} == {3}
    star_facets = {
        frozenset(
            vertex
            for vertex, endpoints in BASE_EDGE.items()
            if endpoint in endpoints
        )
        for endpoint in [f"a{i}" for i in range(3)]
        + [f"b{j}" for j in range(3)]
    }
    assert star_facets == facets

    common_neighbor_witnesses = {
        (u, v): sorted(h_prime[u] & h_prime[v])
        for u, v in itertools.combinations(range(9), 2)
    }
    assert all(common_neighbor_witnesses.values())

    g_prime = complement(h_prime)
    deletion_parameters, deletion_eternal_trace = graph_parameters(g_prime)
    assert deletion_parameters == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    deletion_kernel, _, deletion_rounds, deletion_initial = (
        greatest_eternal_family(g_prime, 3)
    )
    assert deletion_initial == 48
    assert len(deletion_kernel) == 48
    assert deletion_rounds == []

    colorings = proper_partitions(h_prime, 3)
    assert colorings == EXPECTED_COLOR_PARTITIONS

    # Marking, facet hitting, vacuous ridge covariance, and inactive C4.
    assert ACTIVE.isdisjoint(INACTIVE)
    assert ACTIVE | INACTIVE == frozenset(range(9))
    assert all(facet & ACTIVE for facet in facets)
    assert ROOT in facets and ROOT <= ACTIVE
    ridge_pairs = [
        (left, right)
        for left, right in itertools.combinations(facets, 2)
        if len(left & right) == 2
    ]
    assert ridge_pairs == []
    covariance_holds = all(
        bool((left - right) & ACTIVE) == bool((right - left) & ACTIVE)
        for left, right in ridge_pairs
    )
    assert covariance_holds
    inactive_edges = {
        edge for edge in line_edges if edge <= INACTIVE
    }
    expected_c4 = {
        frozenset({0, 3}),
        frozenset({3, 6}),
        frozenset({6, 4}),
        frozenset({4, 0}),
    }
    assert inactive_edges == expected_c4
    assert all(
        all(any(vertex in INACTIVE for vertex in color_class)
            for color_class in partition)
        for partition in colorings
    )

    # Add x adjacent in H exactly to R, then pass to G=complement(H).
    h_edges = set(line_edges)
    h_edges.update(frozenset({TARGET, vertex}) for vertex in INACTIVE)
    h = graph_from_edges(10, h_edges)
    g = complement(h)
    assert graph6_encode(h) == H_GRAPH6
    assert graph6_decode(H_GRAPH6) == h
    assert graph6_encode(g) == G_GRAPH6
    assert graph6_decode(G_GRAPH6) == g
    assert h[TARGET] == INACTIVE
    assert g[TARGET] == ACTIVE

    target_parameters, target_eternal_trace = graph_parameters(g)
    assert target_parameters == {
        "gamma": 2,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 4,
        "theta": 4,
    }
    assert chromatic_number(h) == 4
    assert not proper_partitions(h, 3)
    assert proper_partitions(h, 4)

    dominating_pairs = {
        state
        for state in subsets(10, 2)
        if dominates(g, state)
    }
    assert dominating_pairs == {frozenset({5, TARGET})}

    target_kernel_2, _, target_rounds_2, target_initial_2 = (
        greatest_eternal_family(g, 2)
    )
    target_kernel_3, target_ranks_3, target_rounds_3, target_initial_3 = (
        greatest_eternal_family(g, 3)
    )
    target_kernel_4, _, target_rounds_4, target_initial_4 = (
        greatest_eternal_family(g, 4)
    )
    assert target_initial_2 == 1
    assert not target_kernel_2
    assert target_rounds_2 == [1]
    assert target_initial_3 == 58
    assert not target_kernel_3
    assert target_rounds_3 == [36, 22]
    assert target_kernel_4
    assert all(target_ranks_3[facet] == 2 for facet in facets)

    prescribed: list[dict[str, object]] = []
    for facet in sorted(facets, key=lambda item: tuple(sorted(item))):
        responders = facet & ACTIVE
        assert responders == {
            guard for guard in facet if TARGET in g[guard]
        }
        for guard in sorted(responders):
            successor = frozenset((set(facet) - {guard}) | {TARGET})
            assert dominates(g, successor)
            prescribed.append(
                {
                    "facet": sorted(facet),
                    "guard": guard,
                    "successor": sorted(successor),
                }
            )
    assert len(prescribed) == 10

    # Literal adaptive two-attack tree, checking occupiedness and every move.
    assert TARGET not in ROOT
    first_moves = legal_successors(g, ROOT, TARGET)
    assert set(first_moves) == {1, 5, 8}
    second_attack = {1: 0, 5: 0, 8: 3}
    expected_second_guard = {1: 5, 5: 1, 8: 5}
    attack_tree: list[dict[str, object]] = []
    for first_guard in sorted(first_moves):
        first_state = first_moves[first_guard]
        assert dominates(g, first_state)
        assert target_ranks_3[first_state] == 1
        attack = second_attack[first_guard]
        assert attack not in first_state
        replies = legal_successors(g, first_state, attack)
        assert set(replies) == {expected_second_guard[first_guard]}
        assert all(not dominates(g, successor) for successor in replies.values())
        attack_tree.append(
            {
                "first_attack": TARGET,
                "first_guard": first_guard,
                "first_successor": sorted(first_state),
                "second_attack": attack,
                "legal_second_replies": [
                    {
                        "guard": guard,
                        "successor": sorted(successor),
                        "dominates": dominates(g, successor),
                    }
                    for guard, successor in sorted(replies.items())
                ],
            }
        )

    return {
        "schema": "inactive-bipartite-gluing-hostile-result-v1",
        "verdict": "PASS",
        "candidate_package": package,
        "H_prime": {
            "graph6": H_PRIME_GRAPH6,
            "identified_as_line_graph_K33": True,
            "order": 9,
            "size": len(line_edges),
            "maximal_cliques": as_lists(facets),
            "all_distinct_pairs_have_common_neighbor": True,
            "proper_3_colorings_modulo_color_permutations": [
                [list(color_class) for color_class in partition]
                for partition in sorted(colorings)
            ],
            "parameters_of_complement": deletion_parameters,
            "greatest_triple_family_size": len(deletion_kernel),
        },
        "marking": {
            "active_A": sorted(ACTIVE),
            "inactive_R": sorted(INACTIVE),
            "every_facet_is_hit_by_A": True,
            "full_active_root": sorted(ROOT),
            "ridge_pairs": [],
            "ridge_covariance": "PASS_VACUOUSLY",
            "nontrivial_ridge_transport_exhibited": False,
            "H_prime_induced_on_R": "C4: 0-3-6-4-0",
            "every_3_coloring_uses_all_3_colors_on_R": True,
        },
        "target_extension": {
            "H_graph6_labeled": H_GRAPH6,
            "G_graph6_labeled": G_GRAPH6,
            "target": TARGET,
            "H_neighborhood_of_target": sorted(h[TARGET]),
            "G_neighborhood_of_target": sorted(g[TARGET]),
            "parameters_of_G": target_parameters,
            "dominating_pairs": as_lists(dominating_pairs),
            "two_guard_kernel": target_eternal_trace[2],
            "three_guard_kernel": {
                "dominating_states_initial": target_initial_3,
                "removed_per_round": target_rounds_3,
                "survivors": len(target_kernel_3),
                "all_six_deletion_facets_have_rank": 2,
            },
            "four_guard_kernel": {
                "dominating_states_initial": target_initial_4,
                "removed_per_round": target_rounds_4,
                "survivors": len(target_kernel_4),
            },
            "prescribed_one_step_successors_checked": len(prescribed),
            "adaptive_two_attack_tree": attack_tree,
        },
        "scope": {
            "static_equality_plus_covariance_plus_bipartite_R_gluing":
                "REFUTED",
            "gamma_equals_3_equality_specific_gluing": "OPEN",
            "complete_k3_conjecture": "OPEN",
            "universal_gamma_theta_conjecture": "OPEN",
            "bounded_minimum_order_and_order10_absence": "OBSERVED_ONLY",
        },
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
