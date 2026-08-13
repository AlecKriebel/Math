#!/usr/bin/env python3
"""Exact four-path proof that Moran chains are not Schur closed."""

import sympy as sp


def bd_transition(A, B, r, neighbors):
    """One-step Bd probability from mutant set A to B."""
    n = len(neighbors)
    total_fitness = r * len(A) + (n - len(A))
    out = 0
    for parent, nbrs in neighbors.items():
        parent_fitness = r if parent in A else 1
        for target in nbrs:
            new = set(A)
            if parent in A:
                new.add(target)
            else:
                new.discard(target)
            if frozenset(new) == B:
                out += parent_fitness / total_fitness / len(nbrs)
    return sp.factor(out)


def db_transition(A, B, r, neighbors):
    """One-step dB probability from mutant set A to B."""
    n = len(neighbors)
    out = 0
    for target, nbrs in neighbors.items():
        parent_total = sum(r if parent in A else 1 for parent in nbrs)
        for parent in nbrs:
            new = set(A)
            if parent in A:
                new.add(target)
            else:
                new.discard(target)
            if frozenset(new) == B:
                parent_fitness = r if parent in A else 1
                out += sp.Rational(1, n) * parent_fitness / parent_total
    return sp.factor(out)


def main() -> None:
    r = sp.symbols("r", positive=True)

    # X={1}, Y={1,2}, Z={1,2,3} on the unweighted path 1-2-3-4.
    neighbors = {1: (2,), 2: (1, 3), 3: (2, 4), 4: (3,)}
    X = frozenset({1})
    Y = frozenset({1, 2})
    Z = frozenset({1, 2, 3})

    q_b_xy = bd_transition(X, Y, r, neighbors)
    q_b_yz = bd_transition(Y, Z, r, neighbors)
    q_b_yy = bd_transition(Y, Y, r, neighbors)

    q_d_xy = db_transition(X, Y, r, neighbors)
    q_d_yz = db_transition(Y, Z, r, neighbors)
    q_d_yy = db_transition(Y, Y, r, neighbors)

    assert sp.simplify(q_b_xy - r / (r + 3)) == 0
    assert sp.simplify(q_b_yz - r / (4 * (r + 1))) == 0
    assert sp.simplify(q_b_yy - sp.Rational(3, 4)) == 0
    assert sp.simplify(q_d_xy - r / (4 * (r + 1))) == 0
    assert sp.simplify(q_d_yz - r / (4 * (r + 1))) == 0
    assert sp.simplify(q_d_yy - sp.Rational(3, 4)) == 0

    tr_b = sp.factor(q_b_xy * q_b_yz / (1 - q_b_yy))
    tr_d = sp.factor(q_d_xy * q_d_yz / (1 - q_d_yy))

    assert sp.simplify(tr_b - r**2 / ((r + 1) * (r + 3))) == 0
    assert sp.simplify(tr_d - r**2 / (4 * (r + 1) ** 2)) == 0
    assert sp.simplify(tr_b / tr_d - 4 * (r + 1) / (r + 3)) == 0

    # The retained endpoints differ at vertices 2 and 3, hence this
    # positive trace edge is forbidden in every one-site Moran update.
    assert len(X.symmetric_difference(Z)) == 2

    print("Moran Schur nonclosure on P4: PASS")


if __name__ == "__main__":
    main()
