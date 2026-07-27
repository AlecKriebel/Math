#!/usr/bin/env python3
"""Clean-room check of the nine-vertex mixed-witness diagnostic.

This file intentionally imports no campaign evaluator.  Graph parameters,
one-guard closure, the restoration-filtered family, and graph6 encoding are
implemented directly with ordinary Python sets and tuples.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json


N = 9
A, B, C, X0, X1, X2, X3, W, Y = range(N)
S = frozenset((A, B, C))

NONEDGES = {
    frozenset(pair)
    for pair in (
        (A, B),
        (A, C),
        (B, C),
        (X0, X1),
        (X1, X2),
        (X2, X3),
        (W, X1),
        (W, X2),
        (Y, C),
        (Y, W),
    )
}
EDGES = {
    frozenset(pair)
    for pair in combinations(range(N), 2)
    if frozenset(pair) not in NONEDGES
}

TARGET_LISTS = {
    X0: frozenset((A,)),
    X1: frozenset((A, C)),
    X2: frozenset((B, C)),
    X3: frozenset((B,)),
    W: frozenset((A, B, C)),
    Y: frozenset((B,)),
}


def adjacent(u: int, v: int) -> bool:
    return u != v and frozenset((u, v)) in EDGES


def dominates(state: frozenset[int]) -> bool:
    return all(v in state or any(adjacent(v, u) for u in state) for v in range(N))


def independent(state: frozenset[int]) -> bool:
    return all(not adjacent(u, v) for u, v in combinations(state, 2))


def all_ksets(k: int):
    return [frozenset(c) for c in combinations(range(N), k)]


def greatest_closed_family(candidates: set[frozenset[int]]):
    """Delete any state with an attack having no successor still retained."""
    live = set(candidates)
    rounds = []
    while True:
        doomed = set()
        for state in live:
            for attack in set(range(N)) - state:
                successors = {
                    state - {guard} | {attack}
                    for guard in state
                    if adjacent(guard, attack)
                    and (state - {guard} | {attack}) in live
                }
                if not successors:
                    doomed.add(state)
                    break
        if not doomed:
            return live, rounds
        rounds.append(len(doomed))
        live -= doomed


def graph6() -> str:
    # For n <= 62, graph6 uses one size byte followed by upper-triangle bits
    # in column-major order: (0,1),(0,2),(1,2),(0,3),...
    bits = [
        1 if adjacent(i, j) else 0
        for j in range(1, N)
        for i in range(j)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    chars = [chr(N + 63)]
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = (value << 1) | bit
        chars.append(chr(value + 63))
    return "".join(chars)


def chromatic_number_of_complement() -> int:
    comp_neighbors = {
        v: {u for u in range(N) if u != v and not adjacent(u, v)}
        for v in range(N)
    }
    order = sorted(range(N), key=lambda v: (-len(comp_neighbors[v]), v))
    for colors in range(1, N + 1):
        assignment: dict[int, int] = {}

        def extend(index: int) -> bool:
            if index == N:
                return True
            v = order[index]
            forbidden = {
                assignment[u] for u in comp_neighbors[v] if u in assignment
            }
            for color in range(colors):
                if color not in forbidden:
                    assignment[v] = color
                    if extend(index + 1):
                        return True
                    del assignment[v]
            return False

        if extend(0):
            return colors
    raise AssertionError("unreachable")


def exact_lists(family: set[frozenset[int]]):
    return {
        x: sorted(
            u
            for u in S
            if adjacent(u, x) and (S - {u} | {x}) in family
        )
        for x in range(N)
        if x not in S
    }


def check_every_obligation(family: set[frozenset[int]]) -> int:
    obligations = 0
    for state in family:
        assert dominates(state)
        for attack in set(range(N)) - state:
            obligations += 1
            witnesses = [
                guard
                for guard in state
                if adjacent(guard, attack)
                and (state - {guard} | {attack}) in family
            ]
            assert witnesses, (state, attack)
    return obligations


def main() -> None:
    dominating_by_k = {
        k: set(filter(dominates, all_ksets(k))) for k in range(1, N + 1)
    }
    gamma = min(k for k, states in dominating_by_k.items() if states)

    independent_sets = [
        state
        for k in range(N + 1)
        for state in all_ksets(k)
        if independent(state)
    ]
    alpha = max(map(len, independent_sets))

    greatest_by_k = {}
    deletion_rounds_by_k = {}
    for k in range(1, N + 1):
        family, rounds = greatest_closed_family(dominating_by_k[k])
        greatest_by_k[k] = family
        deletion_rounds_by_k[k] = rounds
    gamma_infinity = min(k for k, family in greatest_by_k.items() if family)

    restoration_candidates = set()
    for state in dominating_by_k[3]:
        missing = S - state
        outside = state - S
        available = set().union(*(TARGET_LISTS[x] for x in outside)) if outside else set()
        if missing <= available:
            restoration_candidates.add(state)

    restricted_family, restricted_rounds = greatest_closed_family(
        restoration_candidates
    )
    obligations = check_every_obligation(restricted_family)
    state_manifest = ";".join(
        ",".join(map(str, sorted(state)))
        for state in sorted(restricted_family, key=lambda d: tuple(sorted(d)))
    )

    result = {
        "graph6": graph6(),
        "order": N,
        "size": len(EDGES),
        "nonedges": [sorted(pair) for pair in sorted(NONEDGES, key=lambda p: tuple(sorted(p)))],
        "parameters": {
            "gamma": gamma,
            "alpha": alpha,
            "gamma_infinity": gamma_infinity,
            "theta": chromatic_number_of_complement(),
        },
        "greatest_family_sizes_k1_k3": {
            str(k): len(greatest_by_k[k]) for k in range(1, 4)
        },
        "greatest_deletion_rounds_k1_k3": {
            str(k): deletion_rounds_by_k[k] for k in range(1, 4)
        },
        "restoration_candidate_count": len(restoration_candidates),
        "restricted_deletion_rounds": restricted_rounds,
        "restricted_family_size": len(restricted_family),
        "restricted_attack_obligations": obligations,
        "restricted_exact_lists": exact_lists(restricted_family),
        "restricted_state_manifest_sha256": sha256(state_manifest.encode()).hexdigest(),
    }

    expected = {
        "graph6": "HFzvvf]",
        "parameters": {
            "gamma": 2,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        },
        "restricted_family_size": 55,
        "restricted_attack_obligations": 330,
        "restricted_exact_lists": {
            X0: [A],
            X1: [A, C],
            X2: [B, C],
            X3: [B],
            W: [A, B, C],
            Y: [B],
        },
    }
    assert result["graph6"] == expected["graph6"]
    assert result["parameters"] == expected["parameters"]
    assert result["restricted_family_size"] == expected["restricted_family_size"]
    assert (
        result["restricted_attack_obligations"]
        == expected["restricted_attack_obligations"]
    )
    assert result["restricted_exact_lists"] == expected["restricted_exact_lists"]

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
