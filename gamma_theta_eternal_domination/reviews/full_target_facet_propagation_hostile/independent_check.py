#!/usr/bin/env python3
"""Independent checks for the full-target facet-propagation note.

This script imports no campaign evaluator or target-lane code.  It:

* exhausts every labeled graph through order five and every one-guard
  eternal subfamily of dominating triples when alpha is three;
* checks the vertex-star and responder-color assertions literally;
* replays the order-12 full-list control from graph6; and
* constructs the complement of L(K_3,3) directly and checks its parameters
  and six isolated maximum-independent facets.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "math" / "working" / "full_target_facet_propagation" / "NOTE.md"
OUT = Path(__file__).with_name("evidence.json")
DEPENDENCIES = (
    ROOT / "math" / "lemmas" / "maximum_independent_states.md",
    ROOT / "reviews" / "private_lemma_hostile_review.md",
    ROOT / "math" / "working" / "universal_holonomy_critical_graph_referee.md",
    ROOT / "reviews" / "universal_holonomy_critical_graph_cross_review" / "REVIEW.md",
    ROOT / "math" / "working" / "k3_full_list_slice" / "NOTE.md",
    ROOT / "reviews" / "k3_full_list_slice_hostile" / "REVIEW.md",
    ROOT / "reviews" / "k3_full_list_slice_hostile" / "independent_replay_result.json",
    ROOT / "CLAIMS.md",
)


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    n = ord(record[0]) - 63
    bits: list[int] = []
    for char in record[1:]:
        value = ord(char) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [set() for _ in range(n)]
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if bits[cursor]:
                adjacency[low].add(high)
                adjacency[high].add(low)
            cursor += 1
    return tuple(frozenset(row) for row in adjacency)


def graph_from_mask(n: int, mask: int) -> tuple[frozenset[int], ...]:
    adjacency = [set() for _ in range(n)]
    for bit, (u, v) in enumerate(itertools.combinations(range(n), 2)):
        if mask >> bit & 1:
            adjacency[u].add(v)
            adjacency[v].add(u)
    return tuple(frozenset(row) for row in adjacency)


def dominates(graph, state, universe=None) -> bool:
    if universe is None:
        universe = frozenset(range(len(graph)))
    covered = set(state)
    for vertex in state:
        covered.update(graph[vertex] & universe)
    return universe <= covered


def independent(graph, state) -> bool:
    return all(v not in graph[u] for u, v in itertools.combinations(state, 2))


def exact_gamma(graph, universe=None) -> int:
    if universe is None:
        universe = frozenset(range(len(graph)))
    vertices = sorted(universe)
    for size in range(1, len(vertices) + 1):
        if any(
            dominates(graph, frozenset(state), universe)
            for state in itertools.combinations(vertices, size)
        ):
            return size
    raise AssertionError


def exact_alpha(graph, universe=None) -> int:
    if universe is None:
        universe = frozenset(range(len(graph)))
    vertices = sorted(universe)
    for size in range(len(vertices), -1, -1):
        if any(
            independent(graph, state)
            for state in itertools.combinations(vertices, size)
        ):
            return size
    raise AssertionError


def proper_colorings_of_complement(graph, universe, anchored=None):
    vertices = sorted(universe)
    anchored = {} if anchored is None else dict(anchored)
    free = [v for v in vertices if v not in anchored]
    for values in itertools.product(range(3), repeat=len(free)):
        coloring = dict(anchored)
        coloring.update(zip(free, values))
        if all(
            coloring[u] != coloring[v]
            for u, v in itertools.combinations(vertices, 2)
            if v not in graph[u]
        ):
            yield coloring


def theta_at_most_three(graph, universe=None) -> bool:
    if universe is None:
        universe = frozenset(range(len(graph)))
    return next(proper_colorings_of_complement(graph, universe), None) is not None


def dominating_triples(graph, universe=None):
    if universe is None:
        universe = frozenset(range(len(graph)))
    vertices = sorted(universe)
    return tuple(
        frozenset(state)
        for state in itertools.combinations(vertices, 3)
        if dominates(graph, frozenset(state), universe)
    )


def response_table(graph, states, universe=None):
    if universe is None:
        universe = frozenset(range(len(graph)))
    index = {state: i for i, state in enumerate(states)}
    table: list[tuple[int, ...]] = []
    for state in states:
        obligations = []
        for attack in sorted(universe - state):
            successors = 0
            for guard in state:
                successor = (state - {guard}) | {attack}
                if attack in graph[guard] and successor in index:
                    successors |= 1 << index[successor]
            obligations.append(successors)
        table.append(tuple(obligations))
    return tuple(table)


def family_is_eternal(mask: int, table) -> bool:
    for index, obligations in enumerate(table):
        if not (mask >> index & 1):
            continue
        if any(not (successors & mask) for successors in obligations):
            return False
    return bool(mask)


def greatest_family(graph, universe=None):
    states = dominating_triples(graph, universe)
    table = response_table(graph, states, universe)
    live = (1 << len(states)) - 1
    while True:
        dead = 0
        for index, obligations in enumerate(table):
            if live >> index & 1 and any(
                not (successors & live) for successors in obligations
            ):
                dead |= 1 << index
        if not dead:
            return states, live
        live &= ~dead


def ridge_components(facets):
    unseen = set(range(len(facets)))
    components = []
    while unseen:
        root = unseen.pop()
        component = {root}
        stack = [root]
        while stack:
            i = stack.pop()
            neighbors = {
                j for j in unseen if len(facets[i] & facets[j]) == 2
            }
            unseen -= neighbors
            component |= neighbors
            stack.extend(neighbors)
        components.append(frozenset(component))
    return tuple(components)


def active_set(graph, family_states, family_mask, facets, target):
    index = {state: i for i, state in enumerate(family_states)}
    active = set()
    for facet in facets:
        for vertex in facet:
            successor = (facet - {vertex}) | {target}
            if (
                target in graph[vertex]
                and successor in index
                and family_mask >> index[successor] & 1
            ):
                active.add(vertex)
    return frozenset(active)


def audit_theorems_for_family(graph, states, family_mask, counters):
    vertices = frozenset(range(len(graph)))
    family = {
        state for i, state in enumerate(states) if family_mask >> i & 1
    }
    independent_triples = tuple(
        frozenset(state)
        for state in itertools.combinations(vertices, 3)
        if independent(graph, state)
    )
    assert set(independent_triples) <= family

    gamma_graph = exact_gamma(graph)
    theta_graph_le3 = theta_at_most_three(graph)
    for target in vertices:
        deletion = vertices - {target}
        facets = tuple(T for T in independent_triples if target not in T)
        if not facets:
            continue
        components = ridge_components(facets)
        active = active_set(graph, states, family_mask, facets, target)

        # Theorem 2.1 and (2.6)-(2.7).
        for T, U in itertools.combinations(facets, 2):
            for vertex in T & U:
                i_t = vertex in active
                successor_t = (T - {vertex}) | {target}
                listed_t = (
                    target in graph[vertex] and successor_t in family
                )
                successor_u = (U - {vertex}) | {target}
                listed_u = (
                    target in graph[vertex] and successor_u in family
                )
                assert i_t == listed_t == listed_u
        assert all(T & active for T in facets)
        assert active.isdisjoint(deletion - graph[target])
        counters["target_instances"] += 1

        colorings = tuple(proper_colorings_of_complement(graph, deletion))
        for coloring in colorings:
            component_sets = []
            supports = []
            for component in components:
                facet_sets = [
                    frozenset(coloring[v] for v in facets[i] & active)
                    for i in component
                ]
                assert facet_sets and all(s == facet_sets[0] for s in facet_sets)
                assert facet_sets[0]
                support = frozenset().union(*(facets[i] for i in component))
                for r in support & (deletion - graph[target]):
                    assert coloring[r] not in facet_sets[0]
                component_sets.append(facet_sets[0])
                supports.append(support)

            # Corollary 3.2.
            for i, j in itertools.combinations(range(len(components)), 2):
                for vertex in supports[i] & supports[j]:
                    assert (
                        (coloring[vertex] in component_sets[i])
                        == (coloring[vertex] in component_sets[j])
                    )

            # Theorem 4.1, including literal extension.
            deletion_states, deletion_live = greatest_family(graph, deletion)
            deletion_ginf3 = bool(deletion_live)
            if (
                exact_gamma(graph, deletion) == 3
                and exact_alpha(graph, deletion) == 3
                and deletion_ginf3
            ):
                common = set.intersection(*(set(s) for s in component_sets))
                for color in common:
                    assert all(
                        coloring[v] != color
                        for v in deletion - graph[target]
                    )
                    extended = dict(coloring)
                    extended[target] = color
                    assert all(
                        extended[u] != extended[v]
                        for u, v in itertools.combinations(vertices, 2)
                        if v not in graph[u]
                    )
                counters["theorem_4_colorings"] += 1

            # Corollary 4.2 whenever all hypotheses happen to occur.
            full_facets = [T for T in facets if T <= active]
            deletion_theta3 = theta_at_most_three(graph, deletion)
            if (
                gamma_graph == 3
                and exact_alpha(graph) == 3
                and not theta_graph_le3
                and exact_gamma(graph, deletion) == 3
                and exact_alpha(graph, deletion) == 3
                and deletion_ginf3
                and deletion_theta3
                and full_facets
            ):
                assert len(components) >= 3
                counters["corollary_4_2_instances"] += 1
            counters["coloring_instances"] += 1


def exhaustive_small_check():
    counters = {
        "labeled_graphs": 0,
        "alpha_three_graphs": 0,
        "eternal_subfamilies": 0,
        "target_instances": 0,
        "coloring_instances": 0,
        "theorem_4_colorings": 0,
        "corollary_4_2_instances": 0,
    }
    for n in range(1, 6):
        for graph_mask in range(1 << (n * (n - 1) // 2)):
            counters["labeled_graphs"] += 1
            graph = graph_from_mask(n, graph_mask)
            if exact_alpha(graph) != 3:
                continue
            counters["alpha_three_graphs"] += 1
            states = dominating_triples(graph)
            table = response_table(graph, states)
            for family_mask in range(1, 1 << len(states)):
                if not family_is_eternal(family_mask, table):
                    continue
                counters["eternal_subfamilies"] += 1
                audit_theorems_for_family(
                    graph, states, family_mask, counters
                )
    return counters


def order12_control():
    graph = decode_graph6("Ksv`f\\knJVis")
    vertices = frozenset(range(12))
    states, live = greatest_family(graph)
    assert live == (1 << len(states)) - 1
    family = {state for i, state in enumerate(states) if live >> i & 1}
    target = 0
    facets = tuple(
        frozenset(state)
        for state in itertools.combinations(vertices - {target}, 3)
        if independent(graph, state)
    )
    components = ridge_components(facets)
    active = active_set(graph, states, live, facets, target)
    parts = (
        frozenset({1, 5, 8, 11}),
        frozenset({2, 6, 7, 10}),
        frozenset({0, 3, 4, 9}),
    )
    coloring = {v: color for color, part in enumerate(parts) for v in part}
    sets = [
        sorted({coloring[v] + 1 for v in facets[next(iter(C))] & active})
        for C in components
    ]
    deletion = vertices - {target}
    anchored = {1: 0, 2: 1, 3: 2}
    deletion_colorings = tuple(
        proper_colorings_of_complement(graph, deletion, anchored)
    )
    full_colorings = tuple(
        proper_colorings_of_complement(graph, vertices, anchored)
    )
    deletion_intersections = []
    for candidate in deletion_colorings:
        candidate_sets = [
            {
                candidate[v]
                for v in facets[next(iter(component))] & active
            }
            for component in components
        ]
        deletion_intersections.append(
            sorted(set.intersection(*candidate_sets))
        )
    return {
        "parameters": {
            "gamma": exact_gamma(graph),
            "alpha": exact_alpha(graph),
            "gamma_infinity": 3 if live else None,
            "theta": 3 if theta_at_most_three(graph) else ">3",
        },
        "dominating_triples": len(states),
        "greatest_family_states": live.bit_count(),
        "facets_avoiding_target": [sorted(T) for T in facets],
        "ridge_component_sizes": [len(C) for C in components],
        "active_set": sorted(active),
        "complement_neighbors_of_target": sorted(deletion - graph[target]),
        "displayed_full_coloring_responder_sets": sets,
        "displayed_full_coloring_intersection": sorted(
            set.intersection(*(set(s) for s in sets))
        ),
        "anchored_full_graph_colorings": len(full_colorings),
        "anchored_deletion_colorings": len(deletion_colorings),
        "anchored_deletion_intersections_zero_based": deletion_intersections,
        "deletion_gamma": exact_gamma(graph, deletion),
    }


def rook_control():
    # Vertices are the nine edges (row, column) of K_3,3.
    edge_vertices = tuple(itertools.product(range(3), repeat=2))
    graph = []
    for i, (r, c) in enumerate(edge_vertices):
        graph.append(
            frozenset(
                j
                for j, (s, d) in enumerate(edge_vertices)
                if i != j and r != s and c != d
            )
        )
    graph = tuple(graph)
    vertices = frozenset(range(9))
    states, live = greatest_family(graph)
    facets = tuple(
        frozenset(state)
        for state in itertools.combinations(vertices, 3)
        if independent(graph, state)
    )
    components = ridge_components(facets)
    connected = len(
        {
            v
            for start in [0]
            for v in _reachable(graph, start)
        }
    ) == 9
    return {
        "parameters": {
            "gamma": exact_gamma(graph),
            "alpha": exact_alpha(graph),
            "gamma_infinity": 3 if live else None,
            "theta": 3 if theta_at_most_three(graph) else ">3",
        },
        "connected": connected,
        "dominating_triples": len(states),
        "greatest_family_states": live.bit_count(),
        "maximum_independent_facets": [sorted(T) for T in facets],
        "ridge_component_sizes": [len(C) for C in components],
    }


def _reachable(graph, start):
    seen = {start}
    stack = [start]
    while stack:
        vertex = stack.pop()
        new = set(graph[vertex]) - seen
        seen |= new
        stack.extend(new)
    return seen


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    evidence = {
        "target": str(TARGET.relative_to(ROOT)),
        "target_sha256": sha256(TARGET),
        "checker_sha256": None,
        "dependency_sha256": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in DEPENDENCIES
        },
        "small_exhaustive": exhaustive_small_check(),
        "order12_control": order12_control(),
        "rook_control": rook_control(),
    }
    evidence["checker_sha256"] = sha256(Path(__file__))
    OUT.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(json.dumps(evidence, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
