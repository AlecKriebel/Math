#!/usr/bin/env python3
"""Independent finite control for the repair-square normal form.

This checks the accepted graph FCXfO and its displayed proper eternal
family directly from edge and state literals.  It intentionally does not
compute or assume greatest-family reciprocity.
"""

from __future__ import annotations

import hashlib
import itertools
import json


VERTICES = frozenset(range(7))
EDGES = {
    frozenset(edge)
    for edge in (
        (0, 3),
        (0, 6),
        (1, 4),
        (1, 5),
        (1, 6),
        (2, 4),
        (2, 5),
        (2, 6),
        (4, 6),
    )
}
FAMILY = {
    frozenset(state)
    for state in (
        (0, 1, 2),
        (0, 1, 4),
        (0, 1, 6),
        (0, 2, 4),
        (0, 2, 5),
        (0, 2, 6),
        (0, 4, 5),
        (0, 5, 6),
        (1, 2, 3),
        (1, 3, 4),
        (1, 3, 6),
        (2, 3, 4),
        (2, 3, 5),
        (2, 3, 6),
        (3, 4, 5),
        (3, 5, 6),
    )
}


def adjacent(u: int, v: int) -> bool:
    return frozenset((u, v)) in EDGES


def dominates(state: frozenset[int]) -> bool:
    return all(
        vertex in state or any(adjacent(vertex, guard) for guard in state)
        for vertex in VERTICES
    )


def successors(state: frozenset[int], attacked: int) -> set[frozenset[int]]:
    return {
        state.difference({guard}) | {attacked}
        for guard in state
        if adjacent(guard, attacked)
    }


def response_list(reference: frozenset[int], attacked: int) -> list[int]:
    return sorted(
        guard
        for guard in reference
        if adjacent(guard, attacked)
        and reference.difference({guard}) | {attacked} in FAMILY
    )


def main() -> None:
    assert all(len(state) == 3 and dominates(state) for state in FAMILY)
    obligations = 0
    retained_moves = 0
    for state in FAMILY:
        for attacked in VERTICES.difference(state):
            obligations += 1
            retained = successors(state, attacked).intersection(FAMILY)
            assert retained
            retained_moves += len(retained)

    u, x, w, a, z = 1, 4, 0, 2, 5
    S = frozenset((u, w, a))
    T = frozenset((x, w, z))
    D = frozenset((x, w, a))
    O = frozenset((u, w, z))
    R = frozenset((u, x, w))
    P = frozenset((a, z, w))

    assert {S, T, D, R, P}.issubset(FAMILY)
    assert O not in FAMILY
    cycle_edges = {
        frozenset((u, x)),
        frozenset((x, a)),
        frozenset((a, z)),
        frozenset((z, u)),
    }
    diagonals = {frozenset((u, a)), frozenset((x, z))}
    assert cycle_edges.issubset(EDGES)
    assert diagonals.isdisjoint(EDGES)

    lists = {
        "L_S(x)": response_list(S, x),
        "L_T(u)": response_list(T, u),
        "L_S(z)": response_list(S, z),
        "L_T(a)": response_list(T, a),
    }
    assert lists == {
        "L_S(x)": [u, a],
        "L_T(u)": [z],
        "L_S(z)": [u],
        "L_T(a)": [x, z],
    }

    blocker = 3
    assert response_list(S, blocker) == [w]
    assert response_list(T, blocker) == [w]
    assert not successors(O, blocker).intersection(FAMILY)

    serialization = "\n".join(
        "".join(str(vertex) for vertex in sorted(state))
        for state in sorted(FAMILY, key=lambda state: tuple(sorted(state)))
    )
    result = {
        "schema": "coinductive-reciprocity-control-v1",
        "graph6": "FCXfO",
        "family_size": len(FAMILY),
        "family_sha256": hashlib.sha256(serialization.encode()).hexdigest(),
        "attack_obligations": obligations,
        "retained_moves": retained_moves,
        "repair_square": {
            "u": u,
            "x": x,
            "w": w,
            "a": a,
            "z": z,
            "retained": [
                sorted(state) for state in (S, T, D, R, P)
            ],
            "omitted": sorted(O),
            "response_lists": lists,
            "blocker": blocker,
            "blocker_type": "shared-pivot-active",
        },
        "scope_guardrail": (
            "This is a proper-family control for the repair-square theorem. "
            "The greatest family of FCXfO contains the omitted corner."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
