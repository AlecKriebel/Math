#!/usr/bin/env python3
"""Clean-room audit of the 13-vertex physical-literal control.

This verifier imports no campaign or source verifier code.  It decodes the
claimed graph6 record into integer adjacency masks, separately reconstructs
the word graph and transversal family, and checks the exact one-guard game,
parameters, response lists, full frozen-color bipartition, and transport
failure.
"""

from __future__ import annotations

from functools import lru_cache
import hashlib
import itertools
import json
import sys


GRAPH6 = "LFzJbZYhdrDZdM"
NAMES = ("a", "b", "c", "q", "v", "z", "u", "v'", "r", "d", "e", "c'", "a'")
NAME_TO_VERTEX = {name: vertex for vertex, name in enumerate(NAMES)}
A, B, C, Q, V, Z, U, VP, R, D, E, CP, AP = range(13)
ANCHORS = (A, B, C)
S = sum(1 << vertex for vertex in ANCHORS)

WORDS = (
    (0, 0),
    (1, 1),
    (2, 2),
    (0, 1),
    (1, 2),
    (1, 0),
    (2, 1),
    (1, 2),
    (0, 1),
    (2, 0),
    (0, 2),
    (2, 2),
    (0, 0),
)
EXTRA_EDGES = ((C, Q), (A, V), (V, R))

# This is a literal transcription of the triangular human witness table.
HUMAN_WITNESS_ROWS = (
    "c b v' u c v' u c b b b b",
    "a d d c a a c e d a c",
    "z a' r a a z b b a b",
    "d c' v d z v z z v",
    "q a' q d q u q u",
    "e q c q u q c",
    "a z v z a v",
    "d q u a u",
    "v' z z c",
    "b b b",
    "b b",
    "b",
)


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def masks_of_size(order: int, size: int):
    for choice in itertools.combinations(range(order), size):
        yield sum(1 << vertex for vertex in choice)


def decode_graph6(record: str) -> tuple[int, tuple[int, ...]]:
    """Decode the short graph6 format without a graph package."""
    sextets = [ord(character) - 63 for character in record]
    assert sextets and 0 <= sextets[0] <= 62
    order = sextets[0]
    stream = [
        (value >> shift) & 1
        for value in sextets[1:]
        for shift in range(5, -1, -1)
    ]
    needed = order * (order - 1) // 2
    assert len(stream) >= needed
    adjacency = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if stream[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return order, tuple(adjacency)


def word_adjacency() -> tuple[int, ...]:
    """Reconstruct the graph independently from words and exceptional edges."""
    rows = [0] * len(WORDS)
    extras = {frozenset(edge) for edge in EXTRA_EDGES}
    for left, right in itertools.combinations(range(len(WORDS)), 2):
        adjacent = (
            WORDS[left][0] == WORDS[right][0]
            or WORDS[left][1] == WORDS[right][1]
            or frozenset((left, right)) in extras
        )
        if adjacent:
            rows[left] |= 1 << right
            rows[right] |= 1 << left
    return tuple(rows)


def closed_coverage(state: int, adjacency: tuple[int, ...]) -> int:
    coverage = state
    for guard in vertices(state):
        coverage |= adjacency[guard]
    return coverage


def is_dominating(state: int, adjacency: tuple[int, ...], universe: int) -> bool:
    return closed_coverage(state, adjacency) == universe


def is_independent(state: int, adjacency: tuple[int, ...]) -> bool:
    remaining = state
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        remaining ^= bit
        if adjacency[vertex] & remaining:
            return False
    return True


def is_maximal_independent(
    state: int, adjacency: tuple[int, ...], universe: int
) -> bool:
    if not is_independent(state, adjacency):
        return False
    return all(adjacency[vertex] & state for vertex in vertices(universe ^ state))


def first_size(order: int, predicate) -> int:
    for size in range(order + 1):
        if any(predicate(mask) for mask in masks_of_size(order, size)):
            return size
    raise AssertionError("no feasible subset")


def last_size(order: int, predicate) -> int:
    for size in range(order, -1, -1):
        if any(predicate(mask) for mask in masks_of_size(order, size)):
            return size
    raise AssertionError("no feasible subset")


def minimum_clique_partition(
    order: int, adjacency: tuple[int, ...]
) -> tuple[int, tuple[int, ...]]:
    """Compute theta by an anchored partition DP over G-cliques."""
    universe = (1 << order) - 1
    clique = [False] * (1 << order)
    clique[0] = True
    for mask in range(1, 1 << order):
        bit = mask & -mask
        vertex = bit.bit_length() - 1
        rest = mask ^ bit
        clique[mask] = clique[rest] and not (rest & ~adjacency[vertex])

    @lru_cache(maxsize=None)
    def solve(remaining: int) -> tuple[int, tuple[int, ...]]:
        if not remaining:
            return 0, ()
        pivot = remaining & -remaining
        best = order + 1
        parts: tuple[int, ...] = ()
        subset = remaining
        while subset:
            if subset & pivot and clique[subset]:
                tail_count, tail = solve(remaining ^ subset)
                if 1 + tail_count < best:
                    best = 1 + tail_count
                    parts = (subset,) + tail
            subset = (subset - 1) & remaining
        return best, parts

    answer = solve(universe)
    assert sum(part.bit_count() for part in answer[1]) == order
    assert all(clique[part] for part in answer[1])
    return answer


def transversal_family(coordinate: int) -> set[int]:
    classes = [
        [vertex for vertex, word in enumerate(WORDS) if word[coordinate] == color]
        for color in range(3)
    ]
    return {
        sum(1 << vertex for vertex in choice)
        for choice in itertools.product(*classes)
    }


def response_lists(family: set[int]) -> dict[int, tuple[int, ...]]:
    return {
        vertex: tuple(
            anchor
            for anchor in ANCHORS
            if (S ^ (1 << anchor) | (1 << vertex)) in family
        )
        for vertex in range(13)
        if not (S & (1 << vertex))
    }


def audit_family(
    family: set[int], adjacency: tuple[int, ...], universe: int
) -> int:
    obligations = 0
    for state in family:
        assert state.bit_count() == 3
        assert is_dominating(state, adjacency, universe)
        for attack in vertices(universe ^ state):
            obligations += 1
            attack_bit = 1 << attack
            successors = []
            for guard in vertices(state):
                if adjacency[guard] & attack_bit:
                    successor = state ^ (1 << guard) | attack_bit
                    if successor in family:
                        successors.append(successor)
            assert successors
            assert all(is_dominating(successor, adjacency, universe)
                       for successor in successors)
    return obligations


def eternal_kernel(
    order: int, size: int, adjacency: tuple[int, ...], universe: int
) -> tuple[int, tuple[int, ...], set[int]]:
    alive = {
        state
        for state in masks_of_size(order, size)
        if is_dominating(state, adjacency, universe)
    }
    initial = len(alive)
    rounds: list[int] = []
    while True:
        rejected = set()
        for state in alive:
            for attack in vertices(universe ^ state):
                attack_bit = 1 << attack
                if not any(
                    adjacency[guard] & attack_bit
                    and (state ^ (1 << guard) | attack_bit) in alive
                    for guard in vertices(state)
                ):
                    rejected.add(state)
                    break
        if not rejected:
            return initial, tuple(rounds), alive
        alive.difference_update(rejected)
        rounds.append(len(rejected))


def mask_vertices(mask: int) -> tuple[int, ...]:
    return tuple(vertices(mask))


def family_hash(family: set[int]) -> str:
    payload = "".join(
        ",".join(map(str, mask_vertices(state))) + "\n"
        for state in sorted(family, key=mask_vertices)
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def complement_rows(adjacency: tuple[int, ...], universe: int) -> tuple[int, ...]:
    return tuple(
        universe ^ (1 << vertex) ^ adjacency[vertex]
        for vertex in range(len(adjacency))
    )


def bipartition(
    induced_vertices: set[int], complement: tuple[int, ...]
) -> tuple[dict[int, int], dict[int, int]]:
    """Color every component and explicitly audit every induced H-edge."""
    colors: dict[int, int] = {}
    components: dict[int, int] = {}
    component_id = 0
    for root in sorted(induced_vertices):
        if root in colors:
            continue
        colors[root] = 0
        components[root] = component_id
        queue = [root]
        while queue:
            left = queue.pop(0)
            for right in sorted(induced_vertices):
                if not (complement[left] & (1 << right)):
                    continue
                if right not in colors:
                    colors[right] = colors[left] ^ 1
                    components[right] = component_id
                    queue.append(right)
                else:
                    assert components[right] == component_id
                    assert colors[right] == (colors[left] ^ 1)
        component_id += 1
    for left, right in itertools.combinations(sorted(induced_vertices), 2):
        if complement[left] & (1 << right):
            assert components[left] == components[right]
            assert colors[left] != colors[right]
    return colors, components


def audit_human_witness_table(complement: tuple[int, ...]) -> int:
    count = 0
    for left, row in enumerate(HUMAN_WITNESS_ROWS):
        witnesses = row.split()
        assert len(witnesses) == 12 - left
        for offset, name in enumerate(witnesses, start=1):
            right = left + offset
            witness = NAME_TO_VERTEX[name]
            assert witness not in (left, right)
            assert complement[left] & (1 << witness)
            assert complement[right] & (1 << witness)
            count += 1
    return count


def connected(adjacency: tuple[int, ...]) -> bool:
    seen = {0}
    stack = [0]
    while stack:
        left = stack.pop()
        for right in vertices(adjacency[left]):
            if right not in seen:
                seen.add(right)
                stack.append(right)
    return len(seen) == len(adjacency)


def calculate() -> dict[str, object]:
    order, adjacency = decode_graph6(GRAPH6)
    assert order == 13
    assert adjacency == word_adjacency()
    universe = (1 << order) - 1
    complement = complement_rows(adjacency, universe)
    assert connected(adjacency)

    edge_count = sum(row.bit_count() for row in adjacency) // 2
    assert edge_count == 43
    gamma = first_size(
        order, lambda state: is_dominating(state, adjacency, universe)
    )
    alpha = last_size(order, lambda state: is_independent(state, adjacency))
    independent_domination = first_size(
        order,
        lambda state: is_maximal_independent(state, adjacency, universe),
    )
    theta, clique_parts = minimum_clique_partition(order, adjacency)
    assert (gamma, independent_domination, alpha, theta) == (3, 3, 3, 3)
    assert is_independent(S, adjacency) and is_dominating(S, adjacency, universe)

    f0 = transversal_family(0)
    f1 = transversal_family(1)
    family = f0 | f1
    assert (len(f0), len(f1), len(family)) == (80, 80, 142)
    obligations = audit_family(family, adjacency, universe)
    assert obligations == 1420
    serialized_hash = family_hash(family)
    assert serialized_hash == (
        "9e49fca49aceff56168e0aef5cd825b5a55ec73a901985daec7bc03a9022e4aa"
    )

    triple_initial, triple_rounds, triple_kernel = eternal_kernel(
        order, 3, adjacency, universe
    )
    assert triple_kernel == family

    lists = response_lists(family)
    assert all(1 <= len(response_list) <= 2 for response_list in lists.values())
    assert lists[Q] == (A, B)
    assert lists[V] == (B, C)
    assert lists[Z] == lists[R] == (A, B)

    w_c = {vertex for vertex, values in lists.items() if C not in values}
    b_c = {A, B} | w_c
    colors, components = bipartition(b_c, complement)
    assert components[Q] == components[Z] == components[R]
    assert colors[Q] == colors[R] != colors[Z]

    physical = sorted(
        vertex
        for vertex, values in lists.items()
        if values == (A, B) and complement[C] & (1 << vertex)
    )
    same_component = [
        vertex for vertex in physical if components.get(vertex) == components[Q]
    ]
    same_sign = [
        vertex for vertex in same_component if colors[vertex] == colors[Q]
    ]
    preserving_clause = [
        vertex for vertex in same_sign if complement[vertex] & (1 << V)
    ]
    assert physical == [Z, R]
    assert same_component == [Z, R]
    assert same_sign == [R]
    assert preserving_clause == []
    assert complement[Q] & (1 << V)
    assert adjacency[R] & (1 << V)
    assert complement[Q] & (1 << Z)
    assert complement[Z] & (1 << R)

    # The human triangular certificate has one valid outside common
    # H-neighbor for every pair and never uses an endpoint as its witness.
    human_witness_count = audit_human_witness_table(complement)
    assert human_witness_count == order * (order - 1) // 2
    common_witness_count = sum(
        any(
            witness not in (left, right)
            and complement[left] & (1 << witness)
            and complement[right] & (1 << witness)
            for witness in range(order)
        )
        for left, right in itertools.combinations(range(order), 2)
    )
    assert common_witness_count == human_witness_count == 78

    return {
        "classification": "exact equality control; not a counterexample",
        "graph6": GRAPH6,
        "order": order,
        "size": edge_count,
        "connected": True,
        "parameters": {
            "gamma": gamma,
            "i": independent_domination,
            "alpha": alpha,
            "gamma_infinity": 3,
            "theta": theta,
        },
        "partition_family_sizes": [len(f0), len(f1)],
        "union_family_size": len(family),
        "family_sha256": serialized_hash,
        "one_guard_obligations": obligations,
        "three_guard_kernel": {
            "dominating_configurations": triple_initial,
            "deletion_rounds": list(triple_rounds),
            "survivors": len(triple_kernel),
            "contains_supplied_family": True,
        },
        "lists_at_S": {str(vertex): list(values) for vertex, values in lists.items()},
        "full_lists": [
            vertex for vertex, values in lists.items() if len(values) == 3
        ],
        "B_c": {
            "vertices": sorted(b_c),
            "H_edges": [
                [left, right]
                for left, right in itertools.combinations(sorted(b_c), 2)
                if complement[left] & (1 << right)
            ],
            "component": {str(vertex): components[vertex] for vertex in sorted(b_c)},
            "parity": {str(vertex): colors[vertex] for vertex in sorted(b_c)},
        },
        "transport_failure": {
            "qv_is_H_edge": True,
            "physical_exact_ab": physical,
            "same_component_physical_exact_ab": same_component,
            "same_sign_physical_exact_ab": same_sign,
            "same_sign_preserving_qv": preserving_clause,
            "rv_is_G_edge": True,
            "even_H_path": [Q, Z, R],
        },
        "human_common_H_witnesses_checked": human_witness_count,
        "minimum_clique_partition": [
            list(mask_vertices(part)) for part in clique_parts
        ],
    }


def main() -> None:
    output = calculate()
    payload = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if len(sys.argv) == 2:
        with open(sys.argv[1], "rb") as handle:
            assert handle.read() == payload.encode("utf-8")
    else:
        sys.stdout.write(payload)


if __name__ == "__main__":
    main()
