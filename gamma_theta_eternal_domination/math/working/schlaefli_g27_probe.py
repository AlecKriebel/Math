#!/usr/bin/env python3
"""Exact bit-mask probe for the 27-line Schlaefli graph.

This is a bounded structured stress test for the one-guard model.  It
reconstructs the intersection graph H of the 27 lines from the E/C/L incidence
rules and sets G = complement(H).  It does not compute gamma-infinity above
three.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json


LABELS = (
    tuple(f"E{i}" for i in range(1, 7))
    + tuple(f"C{i}" for i in range(1, 7))
    + tuple(
        f"L{i}{j}"
        for i in range(1, 7)
        for j in range(i + 1, 7)
    )
)
ORDER = len(LABELS)
FULL = (1 << ORDER) - 1


def decode(label: str) -> tuple[str, tuple[int, ...]]:
    return label[0], tuple(int(character) for character in label[1:])


def lines_intersect(first: str, second: str) -> bool:
    """Return adjacency in the 27-line intersection graph H."""

    first_type, first_indices = decode(first)
    second_type, second_indices = decode(second)
    if first_type == second_type and first_type in {"E", "C"}:
        return False
    if {first_type, second_type} == {"E", "C"}:
        e_index = (
            first_indices[0] if first_type == "E" else second_indices[0]
        )
        c_index = (
            first_indices[0] if first_type == "C" else second_indices[0]
        )
        return e_index != c_index
    if first_type == second_type == "L":
        return set(first_indices).isdisjoint(second_indices)
    if first_type == "L":
        first_type, second_type = second_type, first_type
        first_indices, second_indices = second_indices, first_indices
    assert second_type == "L" and first_type in {"E", "C"}
    return first_indices[0] in second_indices


def adjacency_masks() -> tuple[tuple[int, ...], tuple[int, ...]]:
    h_adjacency = [0] * ORDER
    for first, second in combinations(range(ORDER), 2):
        if lines_intersect(LABELS[first], LABELS[second]):
            h_adjacency[first] |= 1 << second
            h_adjacency[second] |= 1 << first
    g_adjacency = [
        FULL ^ (1 << vertex) ^ h_adjacency[vertex]
        for vertex in range(ORDER)
    ]
    return tuple(h_adjacency), tuple(g_adjacency)


H_ADJACENCY, G_ADJACENCY = adjacency_masks()


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def subset_mask(candidate: tuple[int, ...]) -> int:
    mask = 0
    for vertex in candidate:
        mask |= 1 << vertex
    return mask


def h_edge_count(mask: int) -> int:
    return (
        sum((H_ADJACENCY[vertex] & mask).bit_count() for vertex in vertices(mask))
        // 2
    )


def common_h_neighbors(mask: int) -> int:
    common = FULL
    for vertex in vertices(mask):
        common &= H_ADJACENCY[vertex]
    return common


def dominates_g(mask: int) -> bool:
    covered = mask
    for vertex in vertices(mask):
        covered |= G_ADJACENCY[vertex]
    return covered == FULL


def graph6(adjacency: tuple[int, ...]) -> str:
    if ORDER > 62:
        raise AssertionError("this compact encoder expects order at most 62")
    bits: list[int] = []
    for higher in range(1, ORDER):
        for lower in range(higher):
            bits.append(int(bool(adjacency[lower] & (1 << higher))))
    while len(bits) % 6:
        bits.append(0)
    values = [ORDER]
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = 2 * value + bit
        values.append(value)
    return "".join(chr(value + 63) for value in values)


def edge_digest(adjacency: tuple[int, ...]) -> str:
    edge_lines = [
        f"{LABELS[first]} {LABELS[second]}"
        for first, second in combinations(range(ORDER), 2)
        if adjacency[first] & (1 << second)
    ]
    return sha256(("\n".join(edge_lines) + "\n").encode("ascii")).hexdigest()


def exact_coloring(
    adjacency: tuple[int, ...], color_count: int
) -> tuple[tuple[int, ...] | None, int]:
    """Complete DSATUR search with canonical color-name introduction."""

    assigned = [-1] * ORDER
    calls = 0

    def choose_vertex() -> int:
        choices = []
        for vertex in range(ORDER):
            if assigned[vertex] >= 0:
                continue
            neighbor_colors = {
                assigned[neighbor]
                for neighbor in vertices(adjacency[vertex])
                if assigned[neighbor] >= 0
            }
            choices.append(
                (
                    len(neighbor_colors),
                    adjacency[vertex].bit_count(),
                    -vertex,
                    vertex,
                )
            )
        return max(choices)[3]

    def extend(used_color_count: int) -> bool:
        nonlocal calls
        calls += 1
        if all(color >= 0 for color in assigned):
            return True
        vertex = choose_vertex()
        forbidden = {
            assigned[neighbor]
            for neighbor in vertices(adjacency[vertex])
            if assigned[neighbor] >= 0
        }
        available_names = min(color_count, used_color_count + 1)
        for color in range(available_names):
            if color in forbidden:
                continue
            assigned[vertex] = color
            if extend(max(used_color_count, color + 1)):
                return True
            assigned[vertex] = -1
        return False

    found = extend(0)
    return (tuple(assigned) if found else None), calls


def synchronous_kernel(
    configurations: set[int],
) -> tuple[list[set[int]], list[dict[int, int]]]:
    """Greatest-fixed-point deletion with simultaneous rounds."""

    levels = [set(configurations)]
    witnesses: list[dict[int, int]] = []
    active = set(configurations)
    while active:
        doomed: set[int] = set()
        attack_witness: dict[int, int] = {}
        for configuration in active:
            for attacked in range(ORDER):
                attacked_bit = 1 << attacked
                if configuration & attacked_bit:
                    continue
                response_exists = False
                for guard in vertices(configuration & G_ADJACENCY[attacked]):
                    successor = configuration ^ (1 << guard) ^ attacked_bit
                    if successor in active:
                        response_exists = True
                        break
                if not response_exists:
                    doomed.add(configuration)
                    attack_witness[configuration] = attacked
                    break
        witnesses.append(attack_witness)
        if not doomed:
            break
        active -= doomed
        levels.append(set(active))
    return levels, witnesses


def main() -> None:
    assert ORDER == 27
    assert len(set(LABELS)) == ORDER
    assert {mask.bit_count() for mask in H_ADJACENCY} == {10}
    assert {mask.bit_count() for mask in G_ADJACENCY} == {16}

    adjacent_common = Counter()
    nonadjacent_common = Counter()
    for first, second in combinations(range(ORDER), 2):
        common = (
            H_ADJACENCY[first] & H_ADJACENCY[second]
        ).bit_count()
        if H_ADJACENCY[first] & (1 << second):
            adjacent_common[common] += 1
        else:
            nonadjacent_common[common] += 1
    assert adjacent_common == {1: 135}
    assert nonadjacent_common == {5: 216}

    triple_table: Counter[tuple[int, int]] = Counter()
    dominating_triples: set[int] = set()
    for candidate in combinations(range(ORDER), 3):
        mask = subset_mask(candidate)
        edge_count = h_edge_count(mask)
        center_count = common_h_neighbors(mask).bit_count()
        triple_table[(edge_count, center_count)] += 1
        if dominates_g(mask):
            dominating_triples.add(mask)
    assert triple_table == {
        (0, 3): 720,
        (1, 1): 1080,
        (2, 0): 1080,
        (3, 0): 45,
    }
    assert len(dominating_triples) == 1125

    # No one- or two-set dominates; triangles supply independent dominating
    # triples, and lambda=1 rules out an H-clique of order four.
    assert not any(
        dominates_g(subset_mask(candidate))
        for size in (1, 2)
        for candidate in combinations(range(ORDER), size)
    )
    assert any(h_edge_count(mask) == 3 for mask in dominating_triples)
    assert not any(
        all(
            H_ADJACENCY[first] & (1 << second)
            for first, second in combinations(candidate, 2)
        )
        for candidate in combinations(range(ORDER), 4)
    )

    levels, witnesses = synchronous_kernel(dominating_triples)
    level_sizes = [len(level) for level in levels]
    assert level_sizes == [1125, 45, 0]
    assert {h_edge_count(mask) for mask in levels[1]} == {3}
    assert len(witnesses[0]) == 1080
    assert len(witnesses[1]) == 45

    path_lethal_attack_counts = Counter()
    for configuration in dominating_triples:
        if h_edge_count(configuration) != 2:
            continue
        lethal = 0
        for attacked in range(ORDER):
            attacked_bit = 1 << attacked
            if configuration & attacked_bit:
                continue
            if all(
                not (
                    subset_mask((attacked,))
                    & H_ADJACENCY[guard]
                )
                for guard in vertices(configuration)
            ):
                lethal += 1
        path_lethal_attack_counts[lethal] += 1
    assert path_lethal_attack_counts == {4: 1080}

    triangle_external_degrees = Counter()
    triangle_attack_response_counts = Counter()
    triangle_successor_types = Counter()
    for configuration in dominating_triples:
        if h_edge_count(configuration) != 3:
            continue
        for attacked in range(ORDER):
            attacked_bit = 1 << attacked
            if configuration & attacked_bit:
                continue
            triangle_external_degrees[
                (H_ADJACENCY[attacked] & configuration).bit_count()
            ] += 1
            response_count = 0
            for guard in vertices(configuration & G_ADJACENCY[attacked]):
                successor = configuration ^ (1 << guard) ^ attacked_bit
                if successor in dominating_triples:
                    response_count += 1
                    triangle_successor_types[h_edge_count(successor)] += 1
            triangle_attack_response_counts[response_count] += 1
    assert triangle_external_degrees == {1: 1080}
    assert triangle_attack_response_counts == {2: 1080}
    assert triangle_successor_types == {2: 2160}

    five_coloring, five_calls = exact_coloring(H_ADJACENCY, 5)
    six_coloring, six_calls = exact_coloring(H_ADJACENCY, 6)
    assert five_coloring is None
    assert six_coloring is not None

    representative = {
        "start": ["E1", "C2", "L12"],
        "first_attack": "E2",
        "response_if_C2_moves": ["E1", "E2", "L12"],
        "then_attack": "E3",
        "response_if_E1_moves": ["C2", "E2", "L12"],
        "then_attack_alternative": "L13",
    }

    result = {
        "status": "CERTIFIED-STRUCTURED-STRESS-TEST",
        "scope": "one-guard k=3 only; no gamma-infinity value above 3",
        "graph": {
            "order": ORDER,
            "h_size": sum(mask.bit_count() for mask in H_ADJACENCY) // 2,
            "g_size": sum(mask.bit_count() for mask in G_ADJACENCY) // 2,
            "h_degree": 10,
            "g_degree": 16,
            "h_srg_parameters": [27, 10, 1, 5],
            "labeled_g_graph6": graph6(G_ADJACENCY),
            "labeled_g_edge_list_sha256": edge_digest(G_ADJACENCY),
        },
        "parameters": {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "theta": 6,
            "eternal_3_family_exists": False,
        },
        "triple_table_h_edges_common_centers": {
            f"{edges},{centers}": count
            for (edges, centers), count in sorted(triple_table.items())
        },
        "synchronous_kernel_sizes": level_sizes,
        "k0_types": {"H_triangle": 45, "H_induced_P3": 1080},
        "path_lethal_attack_counts": dict(path_lethal_attack_counts),
        "triangle_external_h_degree_counts": dict(
            triangle_external_degrees
        ),
        "triangle_dominating_response_counts": dict(
            triangle_attack_response_counts
        ),
        "triangle_successor_h_edge_counts": dict(
            triangle_successor_types
        ),
        "coloring_search": {
            "five_colorable": False,
            "five_calls": five_calls,
            "six_colorable": True,
            "six_calls": six_calls,
            "six_coloring": list(six_coloring),
        },
        "representative_two_attack_tree": representative,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
