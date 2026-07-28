#!/usr/bin/env python3
"""Clean direct verifier for the nine-vertex static countermodel.

No search code or third-party package is imported.  Every assertion is
recomputed from the displayed edge list and the one-guard definition.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
H_PRIME_GRAPH6 = "HEhbtjK"
H_PRIME_EDGES = {
    (0, 3), (0, 4), (0, 7), (0, 8),
    (1, 3), (1, 5), (1, 6), (1, 8),
    (2, 4), (2, 5), (2, 6), (2, 7),
    (3, 6), (3, 7), (4, 6), (4, 8),
    (5, 7), (5, 8),
}
ACTIVE = frozenset({1, 2, 5, 7, 8})
INACTIVE = frozenset({0, 3, 4, 6})
TARGET = 9
EXPECTED_COLOR_PARTITIONS = {
    ((0, 1, 2), (3, 4, 5), (6, 7, 8)),
    ((0, 5, 6), (1, 4, 7), (2, 3, 8)),
}


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def adjacency_from_edges(
    order: int, edges: set[tuple[int, int]]
) -> tuple[int, ...]:
    rows = [0] * order
    for u, v in edges:
        assert 0 <= u < v < order
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return tuple(rows)


def decode_graph6(record: str) -> tuple[int, ...]:
    order = ord(record[0]) - 63
    assert 0 <= order <= 62
    bits = []
    for char in record[1:]:
        value = ord(char) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    rows = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            cursor += 1
    return tuple(rows)


def encode_graph6(adjacency: tuple[int, ...]) -> str:
    bits = []
    for high in range(1, len(adjacency)):
        for low in range(high):
            bits.append(1 if adjacency[low] & (1 << high) else 0)
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(len(adjacency) + 63) + "".join(payload)


def complement(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    universe = (1 << len(adjacency)) - 1
    return tuple(universe ^ (1 << v) ^ adjacency[v] for v in range(len(adjacency)))


def masks_of_size(order: int, size: int):
    for subset in itertools.combinations(range(order), size):
        yield sum(1 << vertex for vertex in subset)


def is_clique(adjacency: tuple[int, ...], state: int) -> bool:
    return all(
        adjacency[u] & (1 << v)
        for u, v in itertools.combinations(vertices(state), 2)
    )


def is_independent(adjacency: tuple[int, ...], state: int) -> bool:
    return all(not (adjacency[v] & state) for v in vertices(state))


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in vertices(state):
        covered |= adjacency[vertex]
    return covered == (1 << len(adjacency)) - 1


def maximal_cliques(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    order = len(adjacency)
    answer = []
    for state in range(1, 1 << order):
        if not is_clique(adjacency, state):
            continue
        if all(
            not is_clique(adjacency, state | (1 << outside))
            for outside in vertices(((1 << order) - 1) ^ state)
        ):
            answer.append(state)
    return tuple(answer)


def bipartite(adjacency: tuple[int, ...], allowed: int) -> bool:
    shades: dict[int, int] = {}
    for root in vertices(allowed):
        if root in shades:
            continue
        shades[root] = 0
        stack = [root]
        while stack:
            u = stack.pop()
            for v in vertices(adjacency[u] & allowed):
                if v not in shades:
                    shades[v] = shades[u] ^ 1
                    stack.append(v)
                elif shades[v] == shades[u]:
                    return False
    return True


def coloring_partitions(
    adjacency: tuple[int, ...], number_of_colors: int
) -> set[tuple[tuple[int, ...], ...]]:
    order = len(adjacency)
    colors = [-1] * order
    colors[0] = 0
    answer: set[tuple[tuple[int, ...], ...]] = set()

    def visit(vertex: int) -> None:
        if vertex == order:
            parts = [
                tuple(v for v in range(order) if colors[v] == color)
                for color in range(number_of_colors)
            ]
            answer.add(tuple(sorted(parts)))
            return
        if colors[vertex] >= 0:
            visit(vertex + 1)
            return
        forbidden = {
            colors[u]
            for u in vertices(adjacency[vertex])
            if colors[u] >= 0
        }
        for color in range(number_of_colors):
            if color not in forbidden:
                colors[vertex] = color
                visit(vertex + 1)
                colors[vertex] = -1

    visit(0)
    return answer


def chromatic_number(adjacency: tuple[int, ...]) -> int:
    for colors in range(1, len(adjacency) + 1):
        if coloring_partitions(adjacency, colors):
            return colors
    raise AssertionError("unreachable")


def gamma(adjacency: tuple[int, ...]) -> int:
    for size in range(1, len(adjacency) + 1):
        if any(dominates(adjacency, state)
               for state in masks_of_size(len(adjacency), size)):
            return size
    raise AssertionError("unreachable")


def alpha(adjacency: tuple[int, ...]) -> int:
    return max(
        state.bit_count()
        for state in range(1 << len(adjacency))
        if is_independent(adjacency, state)
    )


def independent_domination_number(adjacency: tuple[int, ...]) -> int:
    return min(
        state.bit_count()
        for state in range(1, 1 << len(adjacency))
        if is_independent(adjacency, state) and dominates(adjacency, state)
    )


def greatest_family(
    adjacency: tuple[int, ...], size: int
) -> tuple[frozenset[int], dict[int, int], list[int]]:
    order = len(adjacency)
    universe = (1 << order) - 1
    family = {
        state for state in masks_of_size(order, size)
        if dominates(adjacency, state)
    }
    ranks: dict[int, int] = {}
    rounds: list[int] = []
    rank = 0
    while True:
        deleted = []
        for state in family:
            for attack in vertices(universe ^ state):
                if not any(
                    ((state ^ (1 << guard)) | (1 << attack)) in family
                    for guard in vertices(state & adjacency[attack])
                ):
                    deleted.append(state)
                    break
        if not deleted:
            return frozenset(family), ranks, rounds
        rank += 1
        rounds.append(len(deleted))
        for state in deleted:
            family.remove(state)
            ranks[state] = rank


def eternal_number(adjacency: tuple[int, ...]) -> int:
    for size in range(1, len(adjacency) + 1):
        family, _ranks, _rounds = greatest_family(adjacency, size)
        if family:
            return size
    raise AssertionError("unreachable")


def run() -> dict[str, object]:
    h_prime = adjacency_from_edges(9, H_PRIME_EDGES)
    assert decode_graph6(H_PRIME_GRAPH6) == h_prime
    assert encode_graph6(h_prime) == H_PRIME_GRAPH6
    facets = maximal_cliques(h_prime)
    assert {facet.bit_count() for facet in facets} == {3}
    assert all(
        h_prime[u] & h_prime[v]
        for u, v in itertools.combinations(range(9), 2)
    )
    colorings = coloring_partitions(h_prime, 3)
    assert colorings == EXPECTED_COLOR_PARTITIONS

    active = sum(1 << vertex for vertex in ACTIVE)
    inactive = sum(1 << vertex for vertex in INACTIVE)
    assert active ^ inactive == (1 << 9) - 1
    assert bipartite(h_prime, inactive)
    assert {
        tuple(sorted((u, v)))
        for u, v in itertools.combinations(INACTIVE, 2)
        if h_prime[u] & (1 << v)
    } == {(0, 3), (0, 4), (3, 6), (4, 6)}
    assert any(facet & ~active == 0 for facet in facets)
    root = sum(1 << v for v in (1, 5, 8))
    assert root in facets and root & ~active == 0

    ridge_pairs = []
    for left, right in itertools.combinations(facets, 2):
        shared = left & right
        if shared.bit_count() == 2:
            left_tip = next(vertices(left ^ shared))
            right_tip = next(vertices(right ^ shared))
            assert ((active >> left_tip) & 1) == ((active >> right_tip) & 1)
            ridge_pairs.append(
                [list(vertices(left)), list(vertices(right))]
            )
    assert not ridge_pairs  # covariance is valid but genuinely vacuous here
    for partition in colorings:
        assert all(any(v in INACTIVE for v in part) for part in partition)

    h_rows = list(h_prime) + [inactive]
    for vertex in INACTIVE:
        h_rows[vertex] |= 1 << TARGET
    h = tuple(h_rows)
    g_prime = complement(h_prime)
    g = complement(h)
    assert chromatic_number(h_prime) == 3
    assert chromatic_number(h) == 4
    assert coloring_partitions(h, 3) == set()

    deletion_family, _deletion_ranks, deletion_rounds = greatest_family(
        g_prime, 3
    )
    assert deletion_family
    target_family, target_ranks, target_rounds = greatest_family(g, 3)
    assert not target_family
    assert target_rounds == [36, 22]
    assert all(target_ranks[facet] == 2 for facet in facets)

    prescribed_successors = []
    for facet in facets:
        responders = facet & active
        assert responders
        for guard in vertices(responders):
            assert g[guard] & (1 << TARGET)
            successor = (facet ^ (1 << guard)) | (1 << TARGET)
            assert dominates(g, successor)
            prescribed_successors.append(
                {
                    "facet": list(vertices(facet)),
                    "guard": guard,
                    "successor": list(vertices(successor)),
                }
            )

    # A literal two-attack refutation of the full root.  First attack x.
    # Whichever active guard answers, the displayed second attack has no
    # one-guard move to a dominating triple.
    second_attack_for_guard = {1: 0, 5: 0, 8: 3}
    adaptive_attack_certificate = []
    for first_guard, second_attack in second_attack_for_guard.items():
        first_successor = (root ^ (1 << first_guard)) | (1 << TARGET)
        assert dominates(g, first_successor)
        assert target_ranks[first_successor] == 1
        attempted_moves = []
        for second_guard in vertices(first_successor & g[second_attack]):
            second_successor = (
                (first_successor ^ (1 << second_guard))
                | (1 << second_attack)
            )
            attempted_moves.append(
                {
                    "guard": second_guard,
                    "successor": list(vertices(second_successor)),
                    "dominates": dominates(g, second_successor),
                }
            )
        assert attempted_moves
        assert not any(move["dominates"] for move in attempted_moves)
        adaptive_attack_certificate.append(
            {
                "first_attack": TARGET,
                "first_guard": first_guard,
                "first_successor": list(vertices(first_successor)),
                "second_attack": second_attack,
                "all_legal_second_moves": attempted_moves,
            }
        )

    dominating_pairs = [
        list(vertices(state))
        for state in masks_of_size(10, 2)
        if dominates(g, state)
    ]
    assert dominating_pairs == [[5, 9]]

    deletion_parameters = {
        "gamma": gamma(g_prime),
        "i": independent_domination_number(g_prime),
        "alpha": alpha(g_prime),
        "gamma_infinity": eternal_number(g_prime),
        "theta": chromatic_number(h_prime),
    }
    target_parameters = {
        "gamma": gamma(g),
        "i": independent_domination_number(g),
        "alpha": alpha(g),
        "gamma_infinity": eternal_number(g),
        "theta": chromatic_number(h),
    }
    assert deletion_parameters == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    assert target_parameters == {
        "gamma": 2,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 4,
        "theta": 4,
    }

    return {
        "schema": "inactive-bipartite-gluing-countermodel-verification-v1",
        "verdict": "PASS",
        "claim_labels": {
            "explicit_countermodel_to_static_implication": "PROVED",
            "minimum_order_through_geng_search": "OBSERVED",
            "universal_gamma3_strengthening": "OPEN",
        },
        "H_prime": {
            "graph6": H_PRIME_GRAPH6,
            "edges": [list(edge) for edge in sorted(H_PRIME_EDGES)],
            "maximal_cliques": [list(vertices(facet)) for facet in facets],
            "color_partitions": [
                [list(part) for part in partition]
                for partition in sorted(colorings)
            ],
            "parameters_of_complement": deletion_parameters,
        },
        "marking": {
            "active_A": sorted(ACTIVE),
            "inactive_R": sorted(INACTIVE),
            "inactive_induced_edges": [[0, 3], [0, 4], [3, 6], [4, 6]],
            "full_active_root": [1, 5, 8],
            "ridge_pairs": ridge_pairs,
            "every_coloring_uses_three_colors_on_R": True,
        },
        "target_extension": {
            "target": TARGET,
            "H_graph6_labeled": encode_graph6(h),
            "G_graph6_labeled": encode_graph6(g),
            "parameters_of_G": target_parameters,
            "dominating_pairs": dominating_pairs,
            "all_prescribed_target_successors_dominate": True,
            "prescribed_successors": prescribed_successors,
            "adaptive_two_attack_refutation_of_full_root":
                adaptive_attack_certificate,
            "dominating_triples_initial": 58,
            "kernel_removed_per_round": target_rounds,
            "every_deletion_facet_has_kernel_rank": 2,
        },
        "deletion_eternal_family_size": len(deletion_family),
        "deletion_kernel_removed_per_round": deletion_rounds,
    }


def main() -> None:
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output = HERE / "countermodel_verification.json"
    output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
