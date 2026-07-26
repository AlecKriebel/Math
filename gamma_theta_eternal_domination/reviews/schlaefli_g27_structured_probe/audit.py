#!/usr/bin/env python3
"""Independent set-valued audit of the Schlaefli G(27) k=3 probe.

No code is imported from the author probe or the campaign verifiers.  Graphs,
configurations, moves, and coloring coverage are represented by Python sets.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json


Vertex = tuple[str, int] | tuple[str, int, int]
Configuration = frozenset[Vertex]

VERTICES: tuple[Vertex, ...] = (
    tuple(("E", index) for index in range(1, 7))
    + tuple(("C", index) for index in range(1, 7))
    + tuple(
        ("L", first, second)
        for first in range(1, 7)
        for second in range(first + 1, 7)
    )
)
VERTEX_SET = frozenset(VERTICES)


def label(vertex: Vertex) -> str:
    return "".join(str(part) for part in vertex)


def intersect(first: Vertex, second: Vertex) -> bool:
    """The standard E/C/L incidence rules, independently restated."""

    if first[0] in {"E", "C"} and second[0] in {"E", "C"}:
        if first[0] == second[0]:
            return False
        return first[1] != second[1]
    if first[0] == "L" and second[0] == "L":
        return not {first[1], first[2]}.intersection(
            {second[1], second[2]}
        )
    line = first if first[0] == "L" else second
    singleton = second if first[0] == "L" else first
    return singleton[1] in {line[1], line[2]}


H = {
    vertex: frozenset(
        other
        for other in VERTICES
        if other != vertex and intersect(vertex, other)
    )
    for vertex in VERTICES
}
G = {
    vertex: VERTEX_SET - {vertex} - H[vertex]
    for vertex in VERTICES
}


def h_edges(configuration: Configuration) -> int:
    return sum(
        second in H[first]
        for first, second in combinations(configuration, 2)
    )


def h_centers(configuration: Configuration) -> frozenset[Vertex]:
    common = set(VERTICES)
    for vertex in configuration:
        common.intersection_update(H[vertex])
    return frozenset(common)


def dominates_g(configuration: Configuration) -> bool:
    covered = set(configuration)
    for vertex in configuration:
        covered.update(G[vertex])
    return covered == set(VERTICES)


def is_h_stable(candidate: tuple[Vertex, ...] | Configuration) -> bool:
    return not any(
        second in H[first]
        for first, second in combinations(candidate, 2)
    )


def synchronous_levels(
    configurations: set[Configuration],
) -> list[set[Configuration]]:
    levels = [set(configurations)]
    live = set(configurations)
    while live:
        rejected: set[Configuration] = set()
        for source in live:
            for attack in VERTICES:
                if attack in source:
                    continue
                legal_target = False
                for guard in source:
                    if attack not in G[guard]:
                        continue
                    target = frozenset((source - {guard}) | {attack})
                    if target in live:
                        legal_target = True
                        break
                if not legal_target:
                    rejected.add(source)
                    break
        if not rejected:
            break
        live.difference_update(rejected)
        levels.append(set(live))
    return levels


def residual_three_colorable(
    residual: frozenset[Vertex],
) -> tuple[bool, int]:
    """Exact coloring with ordinary dictionaries and sets."""

    assigned: dict[Vertex, int] = {}
    calls = 0

    def choose() -> Vertex:
        def priority(vertex: Vertex):
            neighbor_colors = {
                assigned[neighbor]
                for neighbor in H[vertex].intersection(residual)
                if neighbor in assigned
            }
            residual_degree = len(H[vertex].intersection(residual))
            return (len(neighbor_colors), residual_degree, label(vertex))

        return max(
            (vertex for vertex in residual if vertex not in assigned),
            key=priority,
        )

    def extend(used_colors: int) -> bool:
        nonlocal calls
        calls += 1
        if len(assigned) == len(residual):
            return True
        vertex = choose()
        forbidden = {
            assigned[neighbor]
            for neighbor in H[vertex].intersection(residual)
            if neighbor in assigned
        }
        for color in range(min(3, used_colors + 1)):
            if color in forbidden:
                continue
            assigned[vertex] = color
            if extend(max(used_colors, color + 1)):
                return True
            del assigned[vertex]
        return False

    answer = extend(0)
    return answer, calls


def edge_digest(adjacency: dict[Vertex, frozenset[Vertex]]) -> str:
    edge_lines = [
        f"{label(first)} {label(second)}"
        for first, second in combinations(VERTICES, 2)
        if second in adjacency[first]
    ]
    return sha256(("\n".join(edge_lines) + "\n").encode("ascii")).hexdigest()


def main() -> None:
    assert len(VERTICES) == 27 and len(VERTEX_SET) == 27
    assert {len(H[vertex]) for vertex in VERTICES} == {10}
    assert {len(G[vertex]) for vertex in VERTICES} == {16}

    pair_common = Counter(
        (
            "H-edge" if second in H[first] else "H-nonedge",
            len(H[first].intersection(H[second])),
        )
        for first, second in combinations(VERTICES, 2)
    )
    assert pair_common == {
        ("H-edge", 1): 135,
        ("H-nonedge", 5): 216,
    }

    triples = tuple(
        frozenset(candidate) for candidate in combinations(VERTICES, 3)
    )
    triple_table = Counter(
        (h_edges(candidate), len(h_centers(candidate)))
        for candidate in triples
    )
    assert triple_table == {
        (0, 3): 720,
        (1, 1): 1080,
        (2, 0): 1080,
        (3, 0): 45,
    }

    k0 = {candidate for candidate in triples if dominates_g(candidate)}
    assert len(k0) == 1125
    assert Counter(h_edges(candidate) for candidate in k0) == {
        2: 1080,
        3: 45,
    }
    levels = synchronous_levels(k0)
    assert [len(level) for level in levels] == [1125, 45, 0]
    assert {h_edges(candidate) for candidate in levels[1]} == {3}

    # Directly check the structural two-attack lemma, without consulting the
    # deletion trace.
    path_lethal_counts = Counter()
    for path in (candidate for candidate in k0 if h_edges(candidate) == 2):
        lethal = [
            attack
            for attack in VERTICES
            if attack not in path
            and all(attack not in H[guard] for guard in path)
        ]
        assert all(
            not dominates_g(frozenset((path - {guard}) | {attack}))
            for attack in lethal
            for guard in path
        )
        path_lethal_counts[len(lethal)] += 1
    assert path_lethal_counts == {4: 1080}

    triangle_first_response_counts = Counter()
    for triangle in (
        candidate for candidate in k0 if h_edges(candidate) == 3
    ):
        for attack in VERTICES:
            if attack in triangle:
                continue
            assert len(H[attack].intersection(triangle)) == 1
            targets = {
                frozenset((triangle - {guard}) | {attack})
                for guard in triangle
                if attack in G[guard]
                and dominates_g(
                    frozenset((triangle - {guard}) | {attack})
                )
            }
            assert targets and {h_edges(target) for target in targets} == {2}
            triangle_first_response_counts[len(targets)] += 1
    assert triangle_first_response_counts == {2: 1080}

    # A second, coverage-style proof that chi(H)>5.  Stable sets in H have
    # order at most six.  A partition of 27 vertices into five such sets would
    # contain two disjoint six-sets; exhaust all of those pairs and show that
    # their 15-vertex residue is never 3-colorable.
    stable_sixes = tuple(
        frozenset(candidate)
        for candidate in combinations(VERTICES, 6)
        if is_h_stable(candidate)
    )
    assert len(stable_sixes) == 72
    assert not any(
        is_h_stable(candidate)
        for candidate in combinations(VERTICES, 7)
    )
    disjoint_six_pairs = tuple(
        (first, second)
        for first, second in combinations(stable_sixes, 2)
        if first.isdisjoint(second)
    )
    assert len(disjoint_six_pairs) == 756
    residual_edge_counts = Counter()
    residual_search_calls = Counter()
    total_residual_calls = 0
    for first, second in disjoint_six_pairs:
        residual = VERTEX_SET - first - second
        residual_edges = sum(
            right in H[left]
            for left, right in combinations(residual, 2)
        )
        residual_edge_counts[residual_edges] += 1
        colorable, calls = residual_three_colorable(residual)
        assert not colorable
        residual_search_calls[calls] += 1
        total_residual_calls += calls

    explicit_six_coloring = (
        frozenset(("E", index) for index in range(1, 7)),
        frozenset(("C", index) for index in range(1, 7)),
        frozenset(("L", 1, index) for index in range(2, 7)),
        frozenset(("L", 2, index) for index in range(3, 7)),
        frozenset(("L", 3, index) for index in range(4, 7)),
        frozenset(
            {
                ("L", 4, 5),
                ("L", 4, 6),
                ("L", 5, 6),
            }
        ),
    )
    assert frozenset().union(*explicit_six_coloring) == VERTEX_SET
    assert sum(map(len, explicit_six_coloring)) == 27
    assert all(is_h_stable(color) for color in explicit_six_coloring)

    # Static parameters.
    assert not any(
        dominates_g(frozenset(candidate))
        for size in (1, 2)
        for candidate in combinations(VERTICES, size)
    )
    h_triangles = [
        candidate for candidate in triples if h_edges(candidate) == 3
    ]
    assert h_triangles and all(dominates_g(candidate) for candidate in h_triangles)
    assert not any(
        h_edges(frozenset(candidate)) == 6
        for candidate in combinations(VERTICES, 4)
    )

    result = {
        "verdict": "ACCEPT_STRUCTURED_K3_STRESS_TEST",
        "status_labels": {
            "static_parameters": "CERTIFIED-FINITE",
            "k3_eternal_nonexistence": "PROVED-FROM-CERTIFIED-LEMMA",
            "universal_conjecture": "UNRESOLVED",
        },
        "scope": "G on 27 vertices; one-guard k=3 only",
        "graph": {
            "h_parameters": [27, 10, 1, 5],
            "g_parameters": [27, 16],
            "g_edge_list_sha256": edge_digest(G),
        },
        "parameters": {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "theta": 6,
            "eternal_3_family_exists": False,
        },
        "triple_table": {
            f"{edges},{centers}": count
            for (edges, centers), count in sorted(triple_table.items())
        },
        "kernel_sizes": [len(level) for level in levels],
        "path_lethal_counts": dict(path_lethal_counts),
        "triangle_first_response_counts": dict(
            triangle_first_response_counts
        ),
        "theta_coverage": {
            "stable_sixes": len(stable_sixes),
            "stable_sevens": 0,
            "disjoint_six_pairs": len(disjoint_six_pairs),
            "residual_edge_counts": dict(sorted(residual_edge_counts.items())),
            "residual_three_color_search_calls": dict(
                sorted(residual_search_calls.items())
            ),
            "total_residual_search_calls": total_residual_calls,
            "six_color_classes": [
                sorted(label(vertex) for vertex in color)
                for color in explicit_six_coloring
            ],
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
