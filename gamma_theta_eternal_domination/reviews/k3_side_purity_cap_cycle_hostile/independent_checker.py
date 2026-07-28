#!/usr/bin/env python3
"""Clean-room hostile replay for the k=3 side-purity cap-cycle control.

This checker uses integer bit masks and standard-library exhaustive search.
It does not import the working verifier or any campaign graph/search helper.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


RECORD = "GCXfVG"
ORDER = 8
ALL = (1 << ORDER) - 1
ANCHORS = (0, 1, 2)
REFERENCE = sum(1 << vertex for vertex in ANCHORS)
OUTSIDE = (3, 4, 5, 6, 7)
RIM = (4, 5, 6, 7)

CAMPAIGN = Path(__file__).resolve().parents[2]
TARGETS = {
    "math/working/k3_side_purity_cap_cycle/NOTE.md":
        "64312289f6d3d87a4c302692c92901caeb9788b16354493e07be01920549f11b",
    "math/working/k3_side_purity_cap_cycle/RESEARCH_LOG.md":
        "a2874b9c1736efc22aed3e56b7017e4f4a08e5e537874d593a39b71fd4d81a3a",
    "math/working/k3_side_purity_cap_cycle/result.json":
        "f9dd30333986b0c984910fe3e13464c28bd64a98d85932c8e2df14f805fb1998",
    "math/working/k3_side_purity_cap_cycle/verify.py":
        "decdf31f361222f5959b1c590aab48c7acd9b37736d8b5b897e3f3f0ab2932d4",
    "math/working/k3_long_bicycle_connectors/NOTE.md":
        "d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10",
    "math/working/k3_cross_state_attack.md":
        "3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68",
    "math/reductions.md":
        "d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 16), b""):
            digest.update(block)
    return digest.hexdigest()


def vertices(mask: int) -> tuple[int, ...]:
    return tuple(vertex for vertex in range(ORDER) if mask & (1 << vertex))


def mask_of(items) -> int:
    answer = 0
    for item in items:
        answer |= 1 << item
    return answer


def decode_small_graph6(record: str) -> tuple[int, ...]:
    """Decode the short-order graph6 form directly from its bit stream."""
    data = [ord(character) - 63 for character in record]
    assert data and 0 <= data[0] <= 62
    order = data[0]
    assert order == ORDER
    stream = []
    for sextet in data[1:]:
        assert 0 <= sextet < 64
        stream.extend((sextet >> shift) & 1 for shift in (5, 4, 3, 2, 1, 0))
    assert len(stream) >= order * (order - 1) // 2

    adjacency = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if stream[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return tuple(adjacency)


def adjacency_from_documented_edges() -> tuple[int, ...]:
    documented = {
        (0, 3),
        (0, 6),
        (0, 7),
        *((1, rim_vertex) for rim_vertex in RIM),
        *((2, rim_vertex) for rim_vertex in RIM),
        (4, 6),
        (5, 7),
    }
    adjacency = [0] * ORDER
    for left, right in documented:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    return tuple(adjacency)


def edge_list(adjacency: tuple[int, ...]) -> list[list[int]]:
    return [
        [left, right]
        for right in range(1, ORDER)
        for left in range(right)
        if adjacency[left] & (1 << right)
    ]


def complement(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(ALL ^ adjacency[vertex] ^ (1 << vertex) for vertex in range(ORDER))


def connected(adjacency: tuple[int, ...]) -> bool:
    reached = 1
    frontier = 1
    while frontier:
        next_frontier = 0
        for vertex in vertices(frontier):
            next_frontier |= adjacency[vertex]
        next_frontier &= ~reached
        reached |= next_frontier
        frontier = next_frontier
    return reached == ALL


def dominates(state: int, adjacency: tuple[int, ...]) -> bool:
    covered = state
    for guard in vertices(state):
        covered |= adjacency[guard]
    return covered == ALL


def independent(state: int, adjacency: tuple[int, ...]) -> bool:
    for vertex in vertices(state):
        if adjacency[vertex] & state:
            return False
    return True


def masks_of_size(size: int) -> tuple[int, ...]:
    return tuple(mask_of(choice) for choice in itertools.combinations(range(ORDER), size))


def move_successors(
    state: int,
    attack: int,
    adjacency: tuple[int, ...],
) -> set[int]:
    return {
        (state ^ (1 << guard)) | (1 << attack)
        for guard in vertices(state)
        if adjacency[guard] & (1 << attack)
    }


def greatest_eternal_kernel(
    guard_count: int,
    adjacency: tuple[int, ...],
) -> tuple[set[int], int, list[int]]:
    family = {
        state
        for state in masks_of_size(guard_count)
        if dominates(state, adjacency)
    }
    initial = len(family)
    rounds = []
    while True:
        doomed = set()
        for state in family:
            for attack in range(ORDER):
                if state & (1 << attack):
                    continue
                if not (move_successors(state, attack, adjacency) & family):
                    doomed.add(state)
                    break
        if not doomed:
            return family, initial, rounds
        rounds.append(len(doomed))
        family.difference_update(doomed)


def domination_number(adjacency: tuple[int, ...]) -> int:
    return next(
        size
        for size in range(1, ORDER + 1)
        if any(dominates(state, adjacency) for state in masks_of_size(size))
    )


def independence_number(adjacency: tuple[int, ...]) -> int:
    return max(
        len(vertices(state))
        for state in range(1 << ORDER)
        if independent(state, adjacency)
    )


def colorable(adjacency: tuple[int, ...], color_count: int) -> bool:
    """Test proper coloring by a fresh canonical backtracking partition."""
    order = sorted(range(ORDER), key=lambda vertex: adjacency[vertex].bit_count(), reverse=True)
    assigned = [-1] * ORDER

    def search(position: int, used_colors: int) -> bool:
        if position == ORDER:
            return True
        vertex = order[position]
        forbidden = {
            assigned[neighbor]
            for neighbor in vertices(adjacency[vertex])
            if assigned[neighbor] >= 0
        }
        for color in range(min(used_colors + 1, color_count)):
            if color in forbidden:
                continue
            assigned[vertex] = color
            if search(position + 1, max(used_colors, color + 1)):
                return True
            assigned[vertex] = -1
        return False

    return search(0, 0)


def chromatic_number(adjacency: tuple[int, ...]) -> int:
    return next(number for number in range(1, ORDER + 1) if colorable(adjacency, number))


def response_lists(family: set[int], adjacency: tuple[int, ...]) -> dict[int, set[int]]:
    answer = {}
    for outside in OUTSIDE:
        response = set()
        for anchor in ANCHORS:
            successor = (REFERENCE ^ (1 << anchor)) | (1 << outside)
            if successor in family:
                assert adjacency[anchor] & (1 << outside)
                response.add(anchor)
        answer[outside] = response
    return answer


def compatible_list_colorings(
    h_adjacency: tuple[int, ...],
    lists: dict[int, set[int]],
) -> list[dict[int, int]]:
    answer = []
    for choices in itertools.product(*(sorted(lists[vertex]) for vertex in OUTSIDE)):
        assignment = dict(zip(OUTSIDE, choices))
        if all(
            assignment[left] != assignment[right]
            for left, right in itertools.combinations(OUTSIDE, 2)
            if h_adjacency[left] & (1 << right)
        ):
            answer.append(assignment)
    return answer


def induced_edges(
    selected: tuple[int, ...],
    adjacency: tuple[int, ...],
) -> list[list[int]]:
    return [
        [left, right]
        for left, right in itertools.combinations(selected, 2)
        if adjacency[left] & (1 << right)
    ]


def common_neighbors(
    left: int,
    right: int,
    adjacency: tuple[int, ...],
) -> list[int]:
    return list(vertices(adjacency[left] & adjacency[right]))


def count_c079_embeddings(
    h_adjacency: tuple[int, ...],
    lists: dict[int, set[int]],
    anchor: int,
) -> int:
    positive = {vertex for vertex in OUTSIDE if anchor in lists[vertex]}
    omitting = {vertex for vertex in OUTSIDE if anchor not in lists[vertex]}
    count = 0

    def extend(path: tuple[int, ...]) -> None:
        nonlocal count
        path_length = len(path) - 1
        if path_length >= 1 and path_length % 2 == 1:
            endpoints = (path[0], path[-1])
            for positive_vertex in positive:
                if positive_vertex in path:
                    continue
                for hub in OUTSIDE:
                    displayed = {positive_vertex, hub, *path}
                    if len(displayed) != len(path) + 2:
                        continue
                    if not (h_adjacency[positive_vertex] & (1 << hub)):
                        continue
                    if all(h_adjacency[hub] & (1 << endpoint) for endpoint in endpoints):
                        count += 1
        last = path[-1]
        for next_vertex in sorted(omitting - set(path)):
            if h_adjacency[last] & (1 << next_vertex):
                extend((*path, next_vertex))

    for start in sorted(omitting):
        extend((start,))
    return count


def state_label(state: int) -> str:
    return "".join(str(vertex) for vertex in vertices(state))


def build_result() -> dict:
    current_hashes = {relative: sha256(CAMPAIGN / relative) for relative in TARGETS}
    assert current_hashes == TARGETS

    adjacency = decode_small_graph6(RECORD)
    documented_adjacency = adjacency_from_documented_edges()
    assert adjacency == documented_adjacency
    h_adjacency = complement(adjacency)
    assert len(edge_list(adjacency)) == 13
    assert len(edge_list(h_adjacency)) == 15
    assert connected(adjacency)

    kernels = {}
    kernel_sets = {}
    for guard_count in (1, 2, 3):
        family, initial, rounds = greatest_eternal_kernel(guard_count, adjacency)
        kernel_sets[guard_count] = family
        kernels[str(guard_count)] = {
            "deletion_round_sizes": rounds,
            "dominating_states_initially": initial,
            "greatest_eternal_family_size": len(family),
        }

    family = kernel_sets[3]
    remainder = {1, 2, 4, 5, 6, 7}
    excluded_pairs = {frozenset({4, 6}), frozenset({5, 7})}
    formula_family = {
        (1 << pole) | mask_of(pair)
        for pole in (0, 3)
        for pair in itertools.combinations(sorted(remainder), 2)
        if frozenset(pair) not in excluded_pairs
    }
    all_dominating_triples = {
        state for state in masks_of_size(3) if dominates(state, adjacency)
    }
    assert family == formula_family == all_dominating_triples
    assert len(family) == 26

    obligation_count = 0
    retained_response_counts = []
    for state in family:
        for attack in range(ORDER):
            if state & (1 << attack):
                continue
            obligation_count += 1
            retained = move_successors(state, attack, adjacency) & family
            assert retained
            retained_response_counts.append(len(retained))
    assert obligation_count == 130

    lists = response_lists(family, adjacency)
    assert lists == {
        3: {0},
        4: {1, 2},
        5: {1, 2},
        6: {1, 2},
        7: {1, 2},
    }
    list_colorings = compatible_list_colorings(h_adjacency, lists)
    assert list_colorings == [
        {3: 0, 4: 1, 5: 2, 6: 1, 7: 2},
        {3: 0, 4: 2, 5: 1, 6: 2, 7: 1},
    ]

    gamma = domination_number(adjacency)
    alpha = independence_number(adjacency)
    gamma_infinity = next(size for size in (1, 2, 3) if kernel_sets[size])
    theta = chromatic_number(h_adjacency)
    assert (gamma, alpha, gamma_infinity, theta) == (3, 3, 3, 3)

    clique_partition = ((0, 3), (1, 4, 6), (2, 5, 7))
    assert mask_of(itertools.chain.from_iterable(clique_partition)) == ALL
    assert all(
        adjacency[left] & (1 << right)
        for part in clique_partition
        for left, right in itertools.combinations(part, 2)
    )

    rim_edges = induced_edges(RIM, h_adjacency)
    expected_rim_edges = [[4, 5], [4, 7], [5, 6], [6, 7]]
    assert rim_edges == expected_rim_edges
    cap_neighborhoods = {
        f"{left}{right}": common_neighbors(left, right, h_adjacency)
        for left, right in rim_edges
    }
    assert all(3 in neighborhood for neighborhood in cap_neighborhoods.values())
    assert cap_neighborhoods["67"] == [3]
    assert adjacency[0] & (1 << 6)
    assert adjacency[0] & (1 << 7)

    c079_counts = {
        str(anchor): count_c079_embeddings(h_adjacency, lists, anchor)
        for anchor in ANCHORS
    }
    assert c079_counts == {"0": 0, "1": 0, "2": 0}

    complement_k4s = [
        list(choice)
        for choice in itertools.combinations(range(ORDER), 4)
        if all(
            h_adjacency[left] & (1 << right)
            for left, right in itertools.combinations(choice, 2)
        )
    ]
    dominating_pairs = [
        list(choice)
        for choice in itertools.combinations(range(ORDER), 2)
        if dominates(mask_of(choice), adjacency)
    ]
    every_pair_has_common_h_neighbor = all(
        h_adjacency[left] & h_adjacency[right]
        for left, right in itertools.combinations(range(ORDER), 2)
    )
    assert not complement_k4s
    assert not dominating_pairs
    assert every_pair_has_common_h_neighbor

    return {
        "certificate": {
            "c079_embedding_counts_by_anchor": c079_counts,
            "cap_common_h_neighborhoods": cap_neighborhoods,
            "clique_partition": [list(part) for part in clique_partition],
            "compatible_list_colorings": [
                {str(vertex): color for vertex, color in coloring.items()}
                for coloring in list_colorings
            ],
            "complement_k4_count": len(complement_k4s),
            "dominating_pair_count": len(dominating_pairs),
            "every_pair_has_common_h_neighbor": every_pair_has_common_h_neighbor,
            "fully_dynamic_rim_edge": [6, 7],
            "fully_dynamic_rim_edge_unique_cap": 3,
            "lists": {
                str(vertex): sorted(response)
                for vertex, response in sorted(lists.items())
            },
            "repeated_cap_vertex": 3,
            "rim_bipartition": [[4, 6], [5, 7]],
            "rim_edges": rim_edges,
        },
        "eternal_family": {
            "all_dominating_triples_equal_greatest_family": True,
            "greatest_kernels": kernels,
            "retained_response_maximum": max(retained_response_counts),
            "retained_response_minimum": min(retained_response_counts),
            "states": [
                state_label(state)
                for state in sorted(family, key=vertices)
            ],
            "unoccupied_attack_obligations": obligation_count,
        },
        "graph": {
            "connected": True,
            "g_edge_count": len(edge_list(adjacency)),
            "g_edges": edge_list(adjacency),
            "graph6": RECORD,
            "h_edge_count": len(edge_list(h_adjacency)),
            "h_edges": edge_list(h_adjacency),
            "order": ORDER,
        },
        "independence": {
            "imports_working_verifier": False,
            "representation": "integer bit masks; exhaustive standard-library search",
        },
        "parameters": {
            "alpha": alpha,
            "gamma": gamma,
            "gamma_infinity": gamma_infinity,
            "theta": theta,
        },
        "schema": "k3-side-purity-cap-cycle-hostile-v1",
        "status": "PASS",
        "target_sha256": current_hashes,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    arguments = parser.parse_args()
    result = build_result()
    if arguments.check is not None:
        expected = json.loads(arguments.check.read_text(encoding="utf-8"))
        assert result == expected
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
