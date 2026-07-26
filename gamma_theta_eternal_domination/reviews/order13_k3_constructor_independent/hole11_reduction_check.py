#!/usr/bin/env python3
"""Independent finite sanity check of the two-outside-vertex C11 reduction.

Vertices 0,...,10 induce C11 in H=complement(G); x=11 and y=12 are the
outside vertices.  X and Y are the respective sets of rim nonneighbors in H,
equivalently their rim neighbors in G.

No SAT solver and no campaign implementation is imported.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


L = 11
N = 13
X_VERTEX = 11
Y_VERTEX = 12
RIM = frozenset(range(L))


def cyclic_distance(a: int, b: int) -> int:
    delta = (a - b) % L
    return min(delta, L - delta)


def transformed(
    subset: frozenset[int],
    shift: int,
    reflection: int,
) -> frozenset[int]:
    return frozenset((reflection * v + shift) % L for v in subset)


def orbit_key(
    first: frozenset[int],
    second: frozenset[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    images = []
    for reflection in (-1, 1):
        for shift in range(L):
            a = tuple(sorted(transformed(first, shift, reflection)))
            b = tuple(sorted(transformed(second, shift, reflection)))
            images.append((a, b))
            images.append((b, a))
    return min(images)


def allowed_pairs() -> list[tuple[frozenset[int], frozenset[int]]]:
    """Enumerate nonempty X,Y for which every cross distance is exactly two."""
    result = []
    for mask in range(1, 1 << L):
        first = frozenset(v for v in range(L) if mask & (1 << v))
        common = set(RIM)
        for a in first:
            common &= {((a - 2) % L), ((a + 2) % L)}
        for size in range(1, len(common) + 1):
            for values in itertools.combinations(sorted(common), size):
                second = frozenset(values)
                if all(
                    cyclic_distance(a, b) == 2
                    for a in first
                    for b in second
                ):
                    result.append((first, second))
    return result


def g_edge(
    a: int,
    b: int,
    first: frozenset[int],
    second: frozenset[int],
) -> bool:
    if a == b:
        return False
    if a < L and b < L:
        return cyclic_distance(a, b) != 1
    if b < L:
        a, b = b, a
    if a < L and b == X_VERTEX:
        return a in first
    if a < L and b == Y_VERTEX:
        return a in second
    if {a, b} == {X_VERTEX, Y_VERTEX}:
        # omega(H)<=3 forces xy to be a nonedge of H, hence an edge of G.
        return True
    raise AssertionError((a, b))


def dominates(
    state: tuple[int, int, int],
    first: frozenset[int],
    second: frozenset[int],
) -> bool:
    occupied = frozenset(state)
    return all(
        v in occupied
        or any(g_edge(v, guard, first, second) for guard in occupied)
        for v in range(N)
    )


def independent(
    state: tuple[int, int, int],
    first: frozenset[int],
    second: frozenset[int],
) -> bool:
    return all(
        not g_edge(a, b, first, second)
        for a, b in itertools.combinations(state, 2)
    )


def dominating_successors(
    state: tuple[int, int, int],
    attack: int,
    first: frozenset[int],
    second: frozenset[int],
) -> tuple[tuple[int, int, int], ...]:
    if attack in state:
        raise AssertionError("the check attempted an occupied attack")
    successors = []
    for guard in state:
        if not g_edge(guard, attack, first, second):
            continue
        successor = tuple(sorted((set(state) - {guard}) | {attack}))
        if dominates(successor, first, second):
            successors.append(successor)
    return tuple(successors)


def has_rim_edge_disjoint_from(
    forbidden: frozenset[int],
) -> bool:
    return any(
        i not in forbidden and (i + 1) % L not in forbidden
        for i in range(L)
    )


def run() -> dict[str, object]:
    possibilities = allowed_pairs()
    orbits: dict[
        tuple[tuple[int, ...], tuple[int, ...]],
        list[tuple[frozenset[int], frozenset[int]]],
    ] = {}
    for pair in possibilities:
        orbits.setdefault(orbit_key(*pair), []).append(pair)

    target_keys = {
        orbit_key(frozenset({0}), frozenset({2})),
        orbit_key(frozenset({0}), frozenset({2, 9})),
    }
    if set(orbits) != target_keys:
        raise AssertionError({"unexpected_orbits": sorted(orbits)})

    # If xy were an H-edge, any rim H-edge disjoint from X union Y would make
    # a K4 with x,y.  Check that such an edge exists in every classified case.
    if not all(
        has_rim_edge_disjoint_from(first | second)
        for first, second in possibilities
    ):
        raise AssertionError("omega(H)<=3 does not force xy nonadjacent")

    attack_evidence = []
    initial = (4, 5, X_VERTEX)
    for second in (frozenset({2}), frozenset({2, 9})):
        first = frozenset({0})
        if not independent(initial, first, second):
            raise AssertionError("initial state is not independent")
        if not dominates(initial, first, second):
            raise AssertionError("maximum independent state fails to dominate")
        after_zero = dominating_successors(initial, 0, first, second)
        expected_zero = ((0, 5, X_VERTEX), (0, 4, X_VERTEX))
        if after_zero != expected_zero:
            raise AssertionError(("attack 0", second, after_zero))
        dead_branch = dominating_successors((0, 4, X_VERTEX), 2, first, second)
        if dead_branch:
            raise AssertionError(("attack 2 unexpectedly answered", second, dead_branch))
        after_seven = dominating_successors((0, 5, X_VERTEX), 7, first, second)
        if after_seven != ((0, 7, X_VERTEX),):
            raise AssertionError(("attack 7", second, after_seven))
        after_nine = dominating_successors((0, 7, X_VERTEX), 9, first, second)
        if after_nine:
            raise AssertionError(("attack 9 unexpectedly answered", second, after_nine))
        attack_evidence.append(
            {
                "X": sorted(first),
                "Y": sorted(second),
                "initial_state": list(initial),
                "initial_independent_and_dominating": True,
                "attack_0_dominating_successors": [list(v) for v in after_zero],
                "branch_0_4_11_attack_2_successors": [],
                "branch_0_5_11_attack_7_successors": [
                    list(after_seven[0])
                ],
                "state_0_7_11_attack_9_successors": [],
            }
        )

    source = Path(__file__).read_bytes()
    return {
        "schema": "gamma-theta-order13-k3-hole11-reduction-check-v1",
        "schema_version": 1,
        "definitions": {
            "H": "complement(G)",
            "X": "rim nonneighbors in H of outside vertex 11",
            "Y": "rim nonneighbors in H of outside vertex 12",
        },
        "logical_chain_checked": [
            "X and Y are nonempty by hub-freeness",
            "rim-edge common-neighbor forcing gives X intersection Y empty",
            "every rim pair has an H-common neighbor",
            "for a in X and b in Y neither outside vertex can witness the pair",
            "the only rim common neighbor occurs at cyclic distance two",
            "D22 times outside-swap has exactly two nonempty-set orbits",
            "a rim edge disjoint from X union Y makes xy an H-nonedge by no-K4",
        ],
        "ordered_set_pairs_before_quotient": len(possibilities),
        "orbit_count": len(orbits),
        "orbit_representatives": [
            {"X": [0], "Y": [2]},
            {"X": [0], "Y": [2, 9]},
        ],
        "xy_is_forced_nonedge_of_H": True,
        "attack_tree_checks": attack_evidence,
        "verdict": "AGREE_NO_INDEXING_FLAW_FOUND",
        "claim_boundary": (
            "Finite sanity check of the stated reduction and attack tree; "
            "the accompanying written argument must supply the implications "
            "from the accepted pair-common-neighbor and maximum-independent-"
            "state lemmas."
        ),
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "source_size_bytes": len(source),
    }


def main() -> int:
    print(json.dumps(run(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
