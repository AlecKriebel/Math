#!/usr/bin/env python3
"""Exact replay for the finite-image/nonalgebraic-fixed-point countermodel.

The construction is U_m = I_m boxplus I_m on C^(2m), followed by the
scalar omega = q-1.  No floating-point arithmetic is used.
"""

from __future__ import annotations

from collections import defaultdict

import sympy as sp


def block_label(i: int, m: int) -> int:
    return 0 if i < m else 1


def pair_action(i: int, j: int, m: int) -> tuple[int, int]:
    """Permutation action of U_m on a basis pair."""
    if block_label(i, m) == block_label(j, m):
        return i, j
    return j, i


def triple_left(state: tuple[int, int, int], m: int) -> tuple[int, int, int]:
    a, b, c = state
    a, b = pair_action(a, b, m)
    b, c = pair_action(b, c, m)
    a, b = pair_action(a, b, m)
    return a, b, c


def triple_right(state: tuple[int, int, int], m: int) -> tuple[int, int, int]:
    a, b, c = state
    b, c = pair_action(b, c, m)
    a, b = pair_action(a, b, m)
    b, c = pair_action(b, c, m)
    return a, b, c


def commutant_constraint_matrix(m: int, left: bool) -> sp.SparseMatrix:
    """Coefficient matrix for [X tensor I,U]=0 or [I tensor X,U]=0."""
    d = 2 * m
    equations: dict[tuple[int, int, int, int], dict[int, int]] = defaultdict(
        lambda: defaultdict(int)
    )

    # Columns are X_(row,column), flattened as row*d+column.
    for a in range(d):
        for b in range(d):
            # (leg operator) U |a,b>
            c, e = pair_action(a, b, m)
            if left:
                for r in range(d):
                    equations[(r, e, a, b)][r * d + c] += 1
            else:
                for r in range(d):
                    equations[(c, r, a, b)][r * d + e] += 1

            # U (leg operator) |a,b>
            if left:
                for r in range(d):
                    x, y = pair_action(r, b, m)
                    equations[(x, y, a, b)][r * d + a] -= 1
            else:
                for r in range(d):
                    x, y = pair_action(a, r, m)
                    equations[(x, y, a, b)][r * d + b] -= 1

    nonzero_rows = [
        {col: val for col, val in row.items() if val}
        for row in equations.values()
        if any(row.values())
    ]
    entries = {}
    for i, row in enumerate(nonzero_rows):
        for j, value in row.items():
            entries[i, j] = value
    return sp.SparseMatrix(len(nonzero_rows), d * d, entries)


def verify(m: int) -> None:
    d = 2 * m
    q = (1 + sp.I * sp.sqrt(3)) / 2
    omega = q - 1

    # Involution and braid relation are checked on every basis state.
    for a in range(d):
        for b in range(d):
            assert pair_action(*pair_action(a, b, m), m) == (a, b)
            for c in range(d):
                state = (a, b, c)
                assert triple_left(state, m) == triple_right(state, m)

    # Exact normalized partial traces.
    ptr = sp.zeros(d)
    for a in range(d):
        for c in range(d):
            count = 0
            for b in range(d):
                out = pair_action(c, b, m)
                count += int(out == (a, b))
            ptr[a, c] = sp.simplify(omega * sp.Rational(count, d))
    assert ptr == (q - 1) * sp.eye(d) / 2
    hs_norm_sq = sp.simplify(sp.trace(ptr.conjugate().T * ptr) / d)
    assert hs_norm_sq == sp.Rational(1, 4)
    assert hs_norm_sq != sp.Rational(1, d * d)

    # Both one-leg commutants have dimension one.
    left_constraints = commutant_constraint_matrix(m, left=True)
    right_constraints = commutant_constraint_matrix(m, left=False)
    left_nullity = d * d - left_constraints.rank()
    right_nullity = d * d - right_constraints.rank()
    assert left_nullity == right_nullity == 1

    # omega has order three, U has order two, hence S=omega U has order six.
    assert sp.simplify(omega**3 - 1) == 0
    assert sp.simplify(omega**6 - 1) == 0

    print(
        f"m={m}, d={d}: PASS; braid/involution exact, "
        f"partial-trace norm^2={hs_norm_sq}, "
        f"leg nullities=({left_nullity},{right_nullity}), "
        f"|image(B_n)| <= 3 n!"
    )


def main() -> None:
    verify(2)
    verify(3)
    print(
        "PASS: finite braid image plus the exact exceptional scalar partial "
        "trace does not force an algebraic or one-leg fixed point."
    )


if __name__ == "__main__":
    main()
