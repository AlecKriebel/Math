#!/usr/bin/env python3
"""Clean-room audit of the inactive-set coloring bridge control.

This checker imports no campaign evaluator or search module.  It decodes the
two graph6 records directly, uses ordinary Python sets throughout, and
reconstructs every finite assertion used by the control.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[2]
SOURCE_DIR = CAMPAIGN / "math" / "working" / "inactive_set_coloring_bridge"
SOURCE_HASHES = {
    "NOTE.md": "18847a21646b5692dc585cbe1aa8f4869ae47e39105c0f43f103b497f9e5574f",
    "verify_control.py": "64923c2d09d3312c98d9961bf33dc05e5363488898abab7cca21d496a7a6b521",
    "control_result.json": "1a891b0e65fd8ef363007869ad3797191b8fca96912e11a1b41ab02d82fd2faa",
}

GPRIME_G6 = "JUZeppVvS^_"
G_G6 = "KUZeppVvS^_~"
X = 11
ACTIVE = frozenset(range(5, 11))
R = frozenset(range(5))
ROOT = frozenset((5, 6, 7))
HPRIME_EDGE_WORDS = (
    "01 04 07 08 12 17 1A 23 26 28 29 2A "
    "34 35 3A 45 48 56 57 67 69 89"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canon_edge(u: int, v: int) -> tuple[int, int]:
    assert u != v
    return (u, v) if u < v else (v, u)


def decode_graph6(record: str) -> tuple[int, frozenset[tuple[int, int]]]:
    raw = record.encode("ascii")
    assert raw and all(63 <= byte <= 126 for byte in raw)
    assert raw[0] != 126, "only the small-order graph6 header is needed"
    order = raw[0] - 63
    needed = order * (order - 1) // 2
    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    assert len(bits) >= needed
    assert all(bit == 0 for bit in bits[needed:])
    pairs = (
        (low, high)
        for high in range(1, order)
        for low in range(high)
    )
    edges = frozenset(pair for pair, bit in zip(pairs, bits) if bit)
    return order, edges


def parse_hprime_words() -> frozenset[tuple[int, int]]:
    def vertex(character: str) -> int:
        return 10 if character == "A" else int(character)

    return frozenset(
        canon_edge(vertex(word[0]), vertex(word[1]))
        for word in HPRIME_EDGE_WORDS.split()
    )


def all_edges(order: int) -> frozenset[tuple[int, int]]:
    return frozenset(itertools.combinations(range(order), 2))


def complement_edges(
    order: int, edges: frozenset[tuple[int, int]]
) -> frozenset[tuple[int, int]]:
    return all_edges(order) - edges


def neighborhoods(
    order: int, edges: frozenset[tuple[int, int]]
) -> tuple[frozenset[int], ...]:
    result = [set() for _ in range(order)]
    for u, v in edges:
        result[u].add(v)
        result[v].add(u)
    return tuple(frozenset(row) for row in result)


def dominates(
    order: int, adjacency: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(adjacency[guard])
    return len(covered) == order


def independent(
    adjacency: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(v not in adjacency[u] for u, v in itertools.combinations(state, 2))


def subsets(order: int, size: int):
    return (frozenset(group) for group in itertools.combinations(range(order), size))


def domination_number(
    order: int, adjacency: tuple[frozenset[int], ...]
) -> int:
    for size in range(1, order + 1):
        if any(dominates(order, adjacency, state) for state in subsets(order, size)):
            return size
    raise AssertionError


def independence_number(
    order: int, adjacency: tuple[frozenset[int], ...]
) -> int:
    for size in range(order, 0, -1):
        if any(independent(adjacency, state) for state in subsets(order, size)):
            return size
    raise AssertionError


def maximal_independent_sets(
    order: int, adjacency: tuple[frozenset[int], ...]
) -> tuple[frozenset[int], ...]:
    answer = []
    for size in range(1, order + 1):
        for state in subsets(order, size):
            if independent(adjacency, state) and dominates(order, adjacency, state):
                answer.append(state)
    return tuple(answer)


def colorings(
    order: int,
    adjacency: tuple[frozenset[int], ...],
    palette_size: int,
    stop_after_one: bool = False,
) -> tuple[tuple[int, ...], ...]:
    assignment = [-1] * order
    answer: list[tuple[int, ...]] = []

    def descend() -> bool:
        if all(color >= 0 for color in assignment):
            answer.append(tuple(assignment))
            return stop_after_one
        uncolored = [v for v in range(order) if assignment[v] < 0]
        vertex = max(
            uncolored,
            key=lambda v: (
                len({assignment[w] for w in adjacency[v] if assignment[w] >= 0}),
                len(adjacency[v]),
                -v,
            ),
        )
        forbidden = {assignment[w] for w in adjacency[vertex] if assignment[w] >= 0}
        for color in range(palette_size):
            if color in forbidden:
                continue
            assignment[vertex] = color
            if descend():
                assignment[vertex] = -1
                return True
            assignment[vertex] = -1
        return False

    descend()
    return tuple(answer)


def chromatic_number(
    order: int, adjacency: tuple[frozenset[int], ...]
) -> int:
    for palette_size in range(1, order + 1):
        if colorings(order, adjacency, palette_size, stop_after_one=True):
            return palette_size
    raise AssertionError


def eternal_kernel(
    order: int,
    adjacency: tuple[frozenset[int], ...],
    guards: int,
) -> tuple[frozenset[frozenset[int]], dict[frozenset[int], int], int, int]:
    """Build the colored configuration digraph, then peel losing vertices."""
    configurations = frozenset(
        state
        for state in subsets(order, guards)
        if dominates(order, adjacency, state)
    )
    options: dict[tuple[frozenset[int], int], frozenset[frozenset[int]]] = {}
    obligation_count = 0
    move_count = 0
    for state in configurations:
        for attacked in set(range(order)) - state:
            targets = frozenset(
                state - {guard} | {attacked}
                for guard in state
                if attacked in adjacency[guard]
                and state - {guard} | {attacked} in configurations
            )
            options[(state, attacked)] = targets
            obligation_count += 1
            move_count += len(targets)

    live = set(configurations)
    deletion_rank: dict[frozenset[int], int] = {}
    round_number = 0
    while True:
        doomed = {
            state
            for state in live
            if any(
                not (options[(state, attacked)] & live)
                for attacked in set(range(order)) - state
            )
        }
        if not doomed:
            break
        round_number += 1
        for state in doomed:
            deletion_rank[state] = round_number
        live.difference_update(doomed)

    for state in live:
        assert all(
            options[(state, attacked)] & live
            for attacked in set(range(order)) - state
        )
    return frozenset(live), deletion_rank, obligation_count, move_count


def triangles(
    order: int, adjacency: tuple[frozenset[int], ...]
) -> tuple[frozenset[int], ...]:
    return tuple(
        state
        for state in subsets(order, 3)
        if all(v in adjacency[u] for u, v in itertools.combinations(state, 2))
    )


def ridge_components(
    facets: tuple[frozenset[int], ...]
) -> tuple[tuple[int, ...], ...]:
    neighbors = {
        i: {
            j
            for j in range(len(facets))
            if i != j and len(facets[i] & facets[j]) == 2
        }
        for i in range(len(facets))
    }
    remaining = set(range(len(facets)))
    answer = []
    while remaining:
        component = set()
        frontier = {min(remaining)}
        while frontier:
            current = frontier.pop()
            if current in component:
                continue
            component.add(current)
            frontier.update(neighbors[current] - component)
        remaining.difference_update(component)
        answer.append(tuple(sorted(component)))
    return tuple(answer)


def static_response(
    order: int,
    adjacency: tuple[frozenset[int], ...],
    state: frozenset[int],
    attacked: int,
) -> frozenset[int]:
    assert attacked not in state
    return frozenset(
        guard
        for guard in state
        if attacked in adjacency[guard]
        and dominates(order, adjacency, state - {guard} | {attacked})
    )


def main() -> dict[str, object]:
    actual_hashes = {
        name: sha256(SOURCE_DIR / name)
        for name in SOURCE_HASHES
    }
    assert actual_hashes == SOURCE_HASHES

    n_prime, gprime_edges = decode_graph6(GPRIME_G6)
    n, g_edges = decode_graph6(G_G6)
    assert (n_prime, n) == (11, 12)
    hprime_edges = complement_edges(n_prime, gprime_edges)
    h_edges = complement_edges(n, g_edges)
    word_edges = parse_hprime_words()
    assert hprime_edges == word_edges
    assert h_edges == word_edges | {canon_edge(r, X) for r in R}

    gp = neighborhoods(n_prime, gprime_edges)
    hp = neighborhoods(n_prime, hprime_edges)
    g = neighborhoods(n, g_edges)
    h = neighborhoods(n, h_edges)

    expected_coloring = (
        frozenset((0, 2, 5)),
        frozenset((1, 3, 6, 8)),
        frozenset((4, 7, 9, 10)),
    )
    assert set().union(*expected_coloring) == set(range(n_prime))
    assert all(
        all(v not in hp[u] for u, v in itertools.combinations(part, 2))
        for part in expected_coloring
    )

    deletion_facets = triangles(n_prime, hp)
    expected_facets = (
        frozenset((0, 1, 7)),
        frozenset((0, 4, 8)),
        frozenset((1, 2, 10)),
        frozenset((2, 3, 10)),
        frozenset((2, 6, 9)),
        frozenset((2, 8, 9)),
        frozenset((3, 4, 5)),
        frozenset((5, 6, 7)),
    )
    assert deletion_facets == expected_facets
    components = ridge_components(deletion_facets)
    assert components == ((0,), (1,), (2, 3), (4, 5), (6,), (7,))
    support = set().union(*deletion_facets)
    assert support == set(range(n_prime))

    r_edges = {
        canon_edge(u, v)
        for u, v in itertools.combinations(R, 2)
        if v in hp[u]
    }
    assert r_edges == {
        (0, 1), (1, 2), (2, 3), (3, 4), (0, 4)
    }
    assert not triangles(
        5,
        neighborhoods(5, frozenset(r_edges)),
    )

    deletion_colorings = colorings(n_prime, hp, 3)
    assert len(deletion_colorings) == 12
    covariance_records = []
    for coloring in deletion_colorings:
        component_color_sets = []
        component_identities = []
        for component in components:
            observed = {
                frozenset(coloring[v] for v in deletion_facets[index] & ACTIVE)
                for index in component
            }
            assert len(observed) == 1
            active_colors = next(iter(observed))
            component_color_sets.append(active_colors)
            component_support = set().union(
                *(deletion_facets[index] for index in component)
            )
            rhs = set(range(3)) - {
                coloring[v] for v in R & component_support
            }
            assert active_colors == rhs
            component_identities.append(sorted(rhs))
        global_intersection = set(range(3))
        for active_colors in component_color_sets:
            global_intersection.intersection_update(active_colors)
        global_rhs = set(range(3)) - {coloring[v] for v in R}
        assert global_intersection == global_rhs == set()
        covariance_records.append(component_identities)

    common_neighbor_prime = {
        pair: hp[pair[0]] & hp[pair[1]]
        for pair in itertools.combinations(range(n_prime), 2)
    }
    common_neighbor_full = {
        pair: h[pair[0]] & h[pair[1]]
        for pair in itertools.combinations(range(n), 2)
    }
    assert all(common_neighbor_prime.values())
    assert all(common_neighbor_full.values())

    static_lists = {}
    successor_states = []
    for facet in deletion_facets:
        response = static_response(n, g, facet, X)
        assert response == facet & ACTIVE
        assert response
        for guard in response:
            successor = facet - {guard} | {X}
            assert dominates(n, g, successor)
            successor_states.append(successor)
        static_lists[",".join(map(str, sorted(facet)))] = sorted(response)
    assert static_response(n, g, ROOT, X) == ROOT

    deletion_mis = maximal_independent_sets(n_prime, gp)
    full_mis = maximal_independent_sets(n, g)
    assert {len(state) for state in deletion_mis} == {3}
    assert {len(state) for state in full_mis} == {3}

    deletion_k3, deletion_ranks, deletion_obligations, deletion_moves = (
        eternal_kernel(n_prime, gp, 3)
    )
    full_k3, full_k3_ranks, full_k3_obligations, full_k3_moves = (
        eternal_kernel(n, g, 3)
    )
    full_k4, full_k4_ranks, full_k4_obligations, full_k4_moves = (
        eternal_kernel(n, g, 4)
    )
    assert len(deletion_k3) == 72
    assert not full_k3
    assert len(full_k4) == 427
    assert all(facet in deletion_k3 for facet in deletion_facets)
    assert all(successor in full_k3_ranks for successor in successor_states)

    deletion_parameters = {
        "gamma": domination_number(n_prime, gp),
        "i": min(map(len, deletion_mis)),
        "alpha": independence_number(n_prime, gp),
        "gamma_infinity": 3 if deletion_k3 else None,
        "theta": chromatic_number(n_prime, hp),
    }
    full_parameters = {
        "gamma": domination_number(n, g),
        "i": min(map(len, full_mis)),
        "alpha": independence_number(n, g),
        "gamma_infinity": 4 if full_k4 and not full_k3 else None,
        "theta": chromatic_number(n, h),
    }
    assert deletion_parameters == {
        "gamma": 3, "i": 3, "alpha": 3, "gamma_infinity": 3, "theta": 3
    }
    assert full_parameters == {
        "gamma": 3, "i": 3, "alpha": 3, "gamma_infinity": 4, "theta": 4
    }

    assert chromatic_number(6, neighborhoods(
        6,
        frozenset(r_edges) | {canon_edge(v, 5) for v in range(5)},
    )) == 4
    assert not colorings(n, h, 3)
    assert colorings(n, h, 4, stop_after_one=True)

    recomputed_source_payload = {
        "schema": "inactive-c5-boundary-control-v1",
        "deletion_graph6_labeled": GPRIME_G6,
        "full_graph6_labeled": G_G6,
        "deletion_parameters": deletion_parameters,
        "full_parameters": full_parameters,
        "target": X,
        "full_static_state": sorted(ROOT),
        "active_set": sorted(ACTIVE),
        "inactive_set_R": sorted(R),
        "H_prime_edges": [list(edge) for edge in sorted(hprime_edges)],
        "deletion_triangles": [sorted(facet) for facet in deletion_facets],
        "ridge_components": [list(component) for component in components],
        "proper_deletion_3_colorings": len(deletion_colorings),
        "static_response_lists": static_lists,
        "greatest_family_sizes": {
            "deletion_k3": len(deletion_k3),
            "full_k3": len(full_k3),
            "full_k4": len(full_k4),
        },
    }
    source_payload = json.loads((SOURCE_DIR / "control_result.json").read_text())
    assert source_payload == recomputed_source_payload

    result = {
        "schema": "inactive-set-coloring-bridge-hostile-audit-v1",
        "verdict": "PASS",
        "source_sha256": actual_hashes,
        "graph6": {
            "deletion": GPRIME_G6,
            "full": G_G6,
            "decoded_edges_G_prime": len(gprime_edges),
            "decoded_edges_G": len(g_edges),
        },
        "parameters": {
            "deletion": deletion_parameters,
            "full": full_parameters,
        },
        "well_covered": {
            "deletion_maximal_independent_sets": len(deletion_mis),
            "deletion_sizes": sorted({len(state) for state in deletion_mis}),
            "full_maximal_independent_sets": len(full_mis),
            "full_sizes": sorted({len(state) for state in full_mis}),
        },
        "kernel": {
            "deletion_k3_live": len(deletion_k3),
            "deletion_k3_deleted": len(deletion_ranks),
            "deletion_k3_obligations": deletion_obligations,
            "deletion_k3_moves": deletion_moves,
            "full_k3_live": len(full_k3),
            "full_k3_deleted": len(full_k3_ranks),
            "full_k3_rounds": max(full_k3_ranks.values()),
            "full_k3_obligations": full_k3_obligations,
            "full_k3_moves": full_k3_moves,
            "static_successor_rank_range": [
                min(full_k3_ranks[state] for state in successor_states),
                max(full_k3_ranks[state] for state in successor_states),
            ],
            "full_k4_live": len(full_k4),
            "full_k4_deleted": len(full_k4_ranks),
            "full_k4_obligations": full_k4_obligations,
            "full_k4_moves": full_k4_moves,
        },
        "facet_structure": {
            "triangles": [sorted(facet) for facet in deletion_facets],
            "ridge_components": [list(component) for component in components],
            "support": sorted(support),
            "inactive_induced_edges": [list(edge) for edge in sorted(r_edges)],
            "inactive_triangle_free": True,
        },
        "coloring_covariance": {
            "deletion_three_colorings": len(deletion_colorings),
            "all_use_three_colors_on_R": True,
            "component_identity_checked_for_every_coloring": True,
            "global_identity_checked_for_every_coloring": True,
            "distinct_component_profiles": len(
                {tuple(map(tuple, profile)) for profile in covariance_records}
            ),
        },
        "static_target": {
            "lists": static_lists,
            "root_full": True,
            "all_listed_successors_dominate": True,
            "successor_count_with_multiplicity": len(successor_states),
            "no_eternal_triple_family": True,
        },
        "common_neighbor_checks": {
            "deletion_pairs": len(common_neighbor_prime),
            "full_pairs": len(common_neighbor_full),
            "all_pass": True,
        },
        "control_result_json_exact_match": True,
        "scope": (
            "The control meets the static and one-target-step conditions but "
            "has gamma_infinity=theta=4; it is not a counterexample and does "
            "not supply an eternal triple-family."
        ),
    }
    return result


if __name__ == "__main__":
    computed = main()
    if len(sys.argv) == 2:
        recorded = json.loads(Path(sys.argv[1]).read_text())
        assert recorded == computed
        print("PASS: recorded hostile evidence equals clean-room recomputation")
    else:
        print(json.dumps(computed, indent=2, sort_keys=True))
