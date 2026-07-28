#!/usr/bin/env python3
"""Clean-room audit of the 12-vertex gamma=3 static gluing control.

The implementation is deliberately independent of the candidate verifier:
graphs and configurations are integer bit masks, graph6 is decoded afresh,
colorings are unlabeled set partitions, and the eternal kernel is rebuilt by
parallel greatest-fixed-point deletion.  No campaign graph/game module and no
candidate source file is imported.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path


REVIEW_DIR = Path(__file__).resolve().parent
CAMPAIGN = REVIEW_DIR.parents[1]
CANDIDATE = CAMPAIGN / "math/working/gamma3_bipartite_gluing"
LABELG = CAMPAIGN / "tools/nauty2_9_3/labelg"

CANDIDATE_MANIFEST_SHA256 = (
    "89edc267a7ec289de682b78428a0d20237e9ba9081c2289593547679301bc08b"
)
LABELG_SHA256 = (
    "ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0"
)

H_PRIME_G6 = "JEhbtjKk@o_"
H_G6 = "KEhbtjKk@om_"
G_G6 = "KxU[ISrR}NP^"
CANONICAL_G6 = (
    "J``E@SV^Tx?",
    "K_?@h]SRNr^Q",
    "Kq]p`SVJw~W^",
)

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

ACTIVE_VERTICES = (0, 4, 6, 7, 8, 9, 10)
INACTIVE_VERTICES = (1, 2, 3, 5)
FULL_ROOT_VERTICES = (0, 4, 8)
TARGET = 11

EXPECTED_FACETS = (
    (0, 3, 7),
    (0, 3, 9),
    (0, 4, 8),
    (1, 3, 6),
    (1, 5, 8),
    (2, 4, 6),
    (2, 4, 10),
    (2, 5, 7),
    (2, 9, 10),
    (3, 9, 10),
)
EXPECTED_COVARIANCE_CLASSES = (
    (0, 6, 10),
    (1,),
    (2, 3),
    (4, 7, 9),
    (5,),
    (8,),
)
EXPECTED_COLORING = (
    (0, 5, 6, 10),
    (1, 4, 7, 9),
    (2, 3, 8),
)
EXPECTED_ATTACK_TREE = {
    "attack": 1,
    "children": [
        {
            "guard": 0,
            "state": [1, 4, 8],
            "subtree": {
                "attack": 9,
                "children": [
                    {
                        "guard": 4,
                        "state": [1, 8, 9],
                        "subtree": {
                            "attack": 7,
                            "children": [],
                            "rank": 1,
                            "state": [1, 8, 9],
                        },
                    },
                    {
                        "guard": 8,
                        "state": [1, 4, 9],
                        "subtree": {
                            "attack": 2,
                            "children": [],
                            "rank": 1,
                            "state": [1, 4, 9],
                        },
                    },
                ],
                "rank": 2,
                "state": [1, 4, 8],
            },
        },
        {
            "guard": 4,
            "state": [0, 1, 8],
            "subtree": {
                "attack": 11,
                "children": [],
                "rank": 1,
                "state": [0, 1, 8],
            },
        },
    ],
    "rank": 3,
    "state": [0, 4, 8],
}


Graph = tuple[int, ...]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mask(vertices: tuple[int, ...] | list[int]) -> int:
    value = 0
    for vertex in vertices:
        value |= 1 << vertex
    return value


def vertices(state: int) -> list[int]:
    answer: list[int] = []
    while state:
        bit = state & -state
        answer.append(bit.bit_length() - 1)
        state ^= bit
    return answer


def from_edges(order: int, edges: tuple[tuple[int, int], ...]) -> Graph:
    rows = [0] * order
    seen: set[tuple[int, int]] = set()
    for first, second in edges:
        assert 0 <= first < second < order
        assert (first, second) not in seen
        seen.add((first, second))
        rows[first] |= 1 << second
        rows[second] |= 1 << first
    return tuple(rows)


def decode_graph6(record: str) -> Graph:
    raw = record.encode("ascii")
    assert raw and 63 <= raw[0] <= 125
    order = raw[0] - 63
    assert order <= 62
    required_bits = order * (order - 1) // 2
    required_payload = (required_bits + 5) // 6
    assert len(raw) == 1 + required_payload
    bits: list[int] = []
    for character in raw[1:]:
        value = character - 63
        assert 0 <= value <= 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    assert not any(bits[required_bits:])
    rows = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            cursor += 1
    return tuple(rows)


def complement(graph: Graph) -> Graph:
    universe = (1 << len(graph)) - 1
    return tuple(
        universe & ~(1 << vertex) & ~graph[vertex]
        for vertex in range(len(graph))
    )


def add_vertex(graph: Graph, neighbors: int) -> Graph:
    order = len(graph)
    rows = list(graph) + [neighbors]
    for vertex in vertices(neighbors):
        rows[vertex] |= 1 << order
    return tuple(rows)


def states_of_size(order: int, size: int):
    for choice in itertools.combinations(range(order), size):
        yield mask(list(choice))


def dominates(graph: Graph, state: int) -> bool:
    covered = state
    for vertex in vertices(state):
        covered |= graph[vertex]
    return covered == (1 << len(graph)) - 1


def is_independent(graph: Graph, state: int) -> bool:
    return all(not (graph[vertex] & (state ^ (1 << vertex)))
               for vertex in vertices(state))


def is_clique(graph: Graph, state: int) -> bool:
    return all(
        (state ^ (1 << vertex)) & ~graph[vertex] == 0
        for vertex in vertices(state)
    )


def domination_number(graph: Graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, state)
               for state in states_of_size(len(graph), size)):
            return size
    raise AssertionError


def independence_number(graph: Graph) -> int:
    for size in range(len(graph), -1, -1):
        if any(is_independent(graph, state)
               for state in states_of_size(len(graph), size)):
            return size
    raise AssertionError


def independent_domination_number(graph: Graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(
            is_independent(graph, state) and dominates(graph, state)
            for state in states_of_size(len(graph), size)
        ):
            return size
    raise AssertionError


def coloring_partitions(graph: Graph, limit: int) -> tuple[tuple[tuple[int, ...], ...], ...]:
    """Enumerate unlabeled proper set partitions into at most ``limit`` blocks."""

    order = len(graph)
    answers: list[tuple[tuple[int, ...], ...]] = []

    def extend(vertex: int, blocks: list[int]) -> None:
        if vertex == order:
            answers.append(tuple(tuple(vertices(block)) for block in blocks))
            return
        bit = 1 << vertex
        for index, block in enumerate(blocks):
            if graph[vertex] & block:
                continue
            blocks[index] |= bit
            extend(vertex + 1, blocks)
            blocks[index] ^= bit
        if len(blocks) < limit:
            blocks.append(bit)
            extend(vertex + 1, blocks)
            blocks.pop()

    extend(0, [])
    return tuple(answers)


def chromatic_number(graph: Graph) -> int:
    for colors in range(1, len(graph) + 1):
        if coloring_partitions(graph, colors):
            return colors
    raise AssertionError


def maximal_cliques(graph: Graph) -> tuple[int, ...]:
    answer: list[int] = []
    universe = (1 << len(graph)) - 1
    for state in range(1, universe + 1):
        if not is_clique(graph, state):
            continue
        outside = universe ^ state
        if all((state & ~graph[vertex]) != 0 for vertex in vertices(outside)):
            answer.append(state)
    return tuple(answer)


def pair_common_neighbors(graph: Graph) -> dict[str, int]:
    witnesses: dict[str, int] = {}
    for first, second in itertools.combinations(range(len(graph)), 2):
        common = graph[first] & graph[second]
        assert common
        witnesses[f"{first}-{second}"] = vertices(common)[0]
    return witnesses


def covariance_data(facets: tuple[int, ...], order: int):
    parent = list(range(order))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def merge(first: int, second: int) -> None:
        first = root(first)
        second = root(second)
        if first != second:
            if first > second:
                first, second = second, first
            parent[second] = first

    exchanges: list[dict[str, list[int] | int]] = []
    for first, second in itertools.combinations(facets, 2):
        ridge = first & second
        if ridge.bit_count() != 2:
            continue
        left = vertices(first ^ ridge)[0]
        right = vertices(second ^ ridge)[0]
        merge(left, right)
        exchanges.append(
            {
                "ridge": vertices(ridge),
                "opposites": [min(left, right), max(left, right)],
            }
        )
    groups: dict[int, list[int]] = {}
    for vertex in range(order):
        groups.setdefault(root(vertex), []).append(vertex)
    classes = tuple(sorted(tuple(group) for group in groups.values()))
    exchanges.sort(key=lambda item: (item["ridge"], item["opposites"]))
    return classes, exchanges


def eternal_kernel(graph: Graph, guards: int):
    order = len(graph)
    current = {
        state for state in states_of_size(order, guards)
        if dominates(graph, state)
    }
    initial_size = len(current)
    rank: dict[int, int] = {}
    failing_attack: dict[int, int] = {}
    wave_sizes: list[int] = []
    round_number = 0
    while True:
        doomed: dict[int, int] = {}
        for state in sorted(current):
            for attack in range(order):
                attack_bit = 1 << attack
                if state & attack_bit:
                    continue
                succeeds = False
                for guard in vertices(state):
                    if not (graph[guard] & attack_bit):
                        continue
                    successor = (state ^ (1 << guard)) | attack_bit
                    if successor in current:
                        succeeds = True
                        break
                if not succeeds:
                    doomed[state] = attack
                    break
        if not doomed:
            break
        round_number += 1
        wave_sizes.append(len(doomed))
        for state, attack in doomed.items():
            rank[state] = round_number
            failing_attack[state] = attack
        current.difference_update(doomed)
    return {
        "initial_size": initial_size,
        "family": current,
        "rank": rank,
        "failing_attack": failing_attack,
        "wave_sizes": wave_sizes,
    }


def audit_eternal_family(graph: Graph, family: set[int]) -> int:
    obligations = 0
    for state in family:
        assert dominates(graph, state)
        for attack in range(len(graph)):
            attack_bit = 1 << attack
            if state & attack_bit:
                continue
            obligations += 1
            assert any(
                graph[guard] & attack_bit
                and ((state ^ (1 << guard)) | attack_bit) in family
                for guard in vertices(state)
            )
    return obligations


def defeat_tree(
    graph: Graph,
    state: int,
    rank: dict[int, int],
    failing_attack: dict[int, int],
) -> dict[str, object]:
    state_rank = rank[state]
    attack = failing_attack[state]
    attack_bit = 1 << attack
    children: list[dict[str, object]] = []
    for guard in vertices(state):
        if not (graph[guard] & attack_bit):
            continue
        successor = (state ^ (1 << guard)) | attack_bit
        if not dominates(graph, successor):
            continue
        assert successor in rank and rank[successor] < state_rank
        children.append(
            {
                "guard": guard,
                "state": vertices(successor),
                "subtree": defeat_tree(
                    graph, successor, rank, failing_attack
                ),
            }
        )
    return {
        "state": vertices(state),
        "rank": state_rank,
        "attack": attack,
        "children": children,
    }


def parameter_tuple(graph: Graph, complement_graph: Graph, eternal: int) -> tuple[int, ...]:
    return (
        domination_number(graph),
        independent_domination_number(graph),
        independence_number(graph),
        eternal,
        chromatic_number(complement_graph),
    )


def verify_manifest() -> dict[str, object]:
    manifest_path = CANDIDATE / "MANIFEST.json"
    assert sha256(manifest_path) == CANDIDATE_MANIFEST_SHA256
    document = json.loads(manifest_path.read_text(encoding="utf-8"))
    checked: dict[str, str] = {}
    for section in ("rigorous_files", "observed_discovery_files"):
        for entry in document[section]:
            relative = entry["path"]
            path = CAMPAIGN / relative
            digest = sha256(path)
            assert digest == entry["sha256"]
            checked[relative] = digest
    return {
        "candidate_manifest_sha256": CANDIDATE_MANIFEST_SHA256,
        "listed_files_checked": len(checked),
        "all_listed_hashes_match": True,
        "files": checked,
    }


def canonical_records() -> dict[str, object]:
    assert LABELG.is_file()
    assert sha256(LABELG) == LABELG_SHA256
    completed = subprocess.run(
        (str(LABELG), "-q", "-g"),
        input="\n".join((H_PRIME_G6, H_G6, G_G6)) + "\n",
        text=True,
        encoding="ascii",
        capture_output=True,
        check=True,
    )
    records = tuple(completed.stdout.splitlines())
    assert records == CANONICAL_G6
    return {
        "tool": "pinned nauty 2.9.3 labelg",
        "tool_sha256": LABELG_SHA256,
        "records": list(records),
    }


def main() -> None:
    active = mask(list(ACTIVE_VERTICES))
    inactive = mask(list(INACTIVE_VERTICES))
    root = mask(list(FULL_ROOT_VERTICES))
    target_bit = 1 << TARGET

    h_prime = from_edges(11, H_PRIME_EDGES)
    assert decode_graph6(H_PRIME_G6) == h_prime
    h = add_vertex(h_prime, inactive)
    assert decode_graph6(H_G6) == h
    g_prime = complement(h_prime)
    g = complement(h)
    assert decode_graph6(G_G6) == g

    h_prime_pair_witnesses = pair_common_neighbors(h_prime)
    h_pair_witnesses = pair_common_neighbors(h)
    assert len(h_prime_pair_witnesses) == 55
    assert len(h_pair_witnesses) == 66

    maximal = maximal_cliques(h_prime)
    facets = tuple(
        state for state in states_of_size(11, 3)
        if is_clique(h_prime, state)
    )
    expected_facets = tuple(mask(list(group)) for group in EXPECTED_FACETS)
    assert set(maximal) == set(facets) == set(expected_facets)
    assert all(state.bit_count() == 3 for state in maximal)

    classes, exchanges = covariance_data(facets, 11)
    assert classes == EXPECTED_COVARIANCE_CLASSES
    assert exchanges
    assert all(
        (mask(list(group)) & inactive) in (0, mask(list(group)))
        for group in classes
    )
    assert root in facets and root & ~active == 0
    assert all(facet & active for facet in facets)

    physical_b = h[TARGET]
    assert physical_b == inactive
    assert all(h_prime[vertex] & physical_b for vertex in range(11))
    total_domination_witness = {
        str(vertex): vertices(h_prime[vertex] & physical_b)[0]
        for vertex in range(11)
    }
    induced_b_edges = tuple(
        edge for edge in H_PRIME_EDGES
        if (physical_b & (1 << edge[0])) and (physical_b & (1 << edge[1]))
    )
    assert induced_b_edges == ((1, 3), (1, 5), (2, 5))
    induced_b_degrees = {
        vertex: (h_prime[vertex] & physical_b).bit_count()
        for vertex in INACTIVE_VERTICES
    }
    assert sorted(induced_b_degrees.values()) == [1, 1, 2, 2]

    anchor_spokes = {
        str(anchor): vertices(h_prime[anchor] & physical_b)
        for anchor in FULL_ROOT_VERTICES
    }
    assert anchor_spokes == {"0": [3], "4": [2], "8": [1, 5]}
    assert all(
        (h_prime[vertex] & root).bit_count() <= 1
        for vertex in INACTIVE_VERTICES
    )

    successors: list[dict[str, object]] = []
    for facet in sorted(facets):
        for guard in vertices(facet & active):
            assert g[guard] & target_bit
            successor = (facet ^ (1 << guard)) | target_bit
            assert dominates(g, successor)
            successors.append(
                {
                    "facet": vertices(facet),
                    "guard": guard,
                    "successor": vertices(successor),
                }
            )
    assert len(successors) == 18

    deletion_colorings = coloring_partitions(h_prime, 3)
    assert deletion_colorings == (EXPECTED_COLORING,)
    assert len({
        index
        for index, block in enumerate(EXPECTED_COLORING)
        if mask(list(block)) & inactive
    }) == 3
    assert not coloring_partitions(h, 3)
    assert coloring_partitions(h, 4)

    g_prime_k3 = eternal_kernel(g_prime, 3)
    assert len(g_prime_k3["family"]) == 48
    g_prime_obligations = audit_eternal_family(
        g_prime, g_prime_k3["family"]
    )
    assert g_prime_obligations == 384

    g_k3 = eternal_kernel(g, 3)
    assert g_k3["wave_sizes"] == [47, 56, 3]
    assert not g_k3["family"]
    g_k4 = eternal_kernel(g, 4)
    assert g_k4["wave_sizes"] == []
    assert len(g_k4["family"]) == 404
    g_k4_obligations = audit_eternal_family(g, g_k4["family"])
    assert g_k4_obligations == 3232

    g_prime_parameters = parameter_tuple(g_prime, h_prime, 3)
    g_parameters = parameter_tuple(g, h, 4)
    assert g_prime_parameters == (3, 3, 3, 3, 3)
    assert g_parameters == (3, 3, 3, 4, 4)

    tree = defeat_tree(
        g, root, g_k3["rank"], g_k3["failing_attack"]
    )
    assert tree == EXPECTED_ATTACK_TREE

    result = {
        "schema": "gamma3-bipartite-gluing-hostile-audit-v1",
        "verdict": "PASS",
        "proof_audit": {
            "exact_target_translation": "PASS",
            "B_subset_R": "PASS by the direct implication b in N_H(x) => bx not in E(G) => b not in A_x",
            "full_root_anchor_pure_witnesses": "PASS",
            "editorial_correction_applied": (
                "The candidate was revised during hostile review to remove "
                "the unnecessary maximum-independent-triple sentence and "
                "prove B subset R directly from the physical nonedge to x."
            ),
        },
        "graph_data": {
            "H_prime_order": 11,
            "H_order": 12,
            "H_prime_edges": [list(edge) for edge in H_PRIME_EDGES],
            "labeled_graph6": {
                "H_prime": H_PRIME_G6,
                "H": H_G6,
                "G": G_G6,
            },
            "canonical_graph6": canonical_records(),
        },
        "static_geometry": {
            "every_pair_common_neighbor_counts": {
                "H_prime": len(h_prime_pair_witnesses),
                "H": len(h_pair_witnesses),
            },
            "maximal_cliques": [
                vertices(state) for state in sorted(maximal)
            ],
            "all_maximal_cliques_are_triangles": True,
            "covariance_exchanges": exchanges,
            "covariance_classes": [list(group) for group in classes],
            "covariance_nonvacuous": True,
            "active_A": list(ACTIVE_VERTICES),
            "inactive_R": list(INACTIVE_VERTICES),
            "full_active_root": list(FULL_ROOT_VERTICES),
            "B_equals_R": True,
            "H_prime_induced_B_edges": [
                list(edge) for edge in induced_b_edges
            ],
            "H_prime_induced_B_is_P4": True,
            "B_total_domination_witness": total_domination_witness,
            "anchor_spokes_in_B": anchor_spokes,
            "each_B_vertex_sees_at_most_one_root_anchor": True,
            "active_target_successor_count": len(successors),
            "active_target_successors": successors,
            "all_active_target_successors_are_legal_and_dominating": True,
            "unique_H_prime_three_coloring_modulo_permutation": [
                list(block) for block in EXPECTED_COLORING
            ],
            "all_three_colors_used_on_R": True,
        },
        "exact_parameters": {
            "G_prime": {
                "tuple_gamma_i_alpha_gamma_infinity_theta": list(
                    g_prime_parameters
                ),
                "three_kernel_initial_size": g_prime_k3["initial_size"],
                "three_kernel_wave_sizes": g_prime_k3["wave_sizes"],
                "three_kernel_size": len(g_prime_k3["family"]),
                "retained_family_obligations": g_prime_obligations,
            },
            "G": {
                "tuple_gamma_i_alpha_gamma_infinity_theta": list(
                    g_parameters
                ),
                "three_kernel_initial_size": g_k3["initial_size"],
                "three_kernel_wave_sizes": g_k3["wave_sizes"],
                "three_kernel_size": len(g_k3["family"]),
                "four_kernel_initial_size": g_k4["initial_size"],
                "four_kernel_wave_sizes": g_k4["wave_sizes"],
                "four_kernel_size": len(g_k4["family"]),
                "four_kernel_obligations": g_k4_obligations,
            },
        },
        "full_root_rank_three_adaptive_defeat": tree,
        "candidate_manifest": verify_manifest(),
        "scope": {
            "static_gamma3_shortcut_refuted": True,
            "dynamic_equality_gluing_theorem_refuted": False,
            "complete_k3_case_proved_or_refuted": False,
            "universal_gamma_theta_conjecture_resolved": False,
            "reason": (
                "The 12-vertex target graph has gamma=3 but "
                "gamma_infinity=theta=4, so it is a static boundary "
                "control rather than a conjecture counterexample."
            ),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
