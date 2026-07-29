#!/usr/bin/env python3
"""Exact certificate for the scalar-cross colored-gluing calculation.

This script works in the two-dimensional algebra C[T]/(T^2-(q-1)T-q).
It constructs the braid generators on the AAB color orbit and reports the
coefficients of I and T in R_1 R_2 R_1 - R_2 R_1 R_2.

It also spot-checks the rank parity used in the controlled-middle no-go
lemma for representative odd middle dimensions; the written parity proof
covers every odd dimension. No floating-point arithmetic is used.
"""

from __future__ import annotations

import itertools

import sympy as sp


q, c, u, s, t = sp.symbols("q c u s t")


def add(x: tuple[sp.Expr, sp.Expr], y: tuple[sp.Expr, sp.Expr]):
    return (sp.expand(x[0] + y[0]), sp.expand(x[1] + y[1]))


def multiply(x: tuple[sp.Expr, sp.Expr], y: tuple[sp.Expr, sp.Expr]):
    """Multiply a+bT and d+eT modulo T^2=(q-1)T+q."""

    a, b = x
    d, e = y
    return (
        sp.expand(a * d + b * e * q),
        sp.expand(a * e + b * d + b * e * (q - 1)),
    )


def scalar(x: sp.Expr):
    return (x, sp.Integer(0))


ZERO = scalar(sp.Integer(0))
T = (sp.Integer(0), sp.Integer(1))


def matrix_multiply(left, right):
    rows = len(left)
    inner = len(right)
    cols = len(right[0])
    answer = [[ZERO for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            for k in range(inner):
                answer[i][j] = add(
                    answer[i][j], multiply(left[i][k], right[k][j])
                )
    return answer


def matrix_subtract(left, right):
    return [
        [
            (
                sp.expand(left[i][j][0] - right[i][j][0]),
                sp.expand(left[i][j][1] - right[i][j][1]),
            )
            for j in range(len(left[0]))
        ]
        for i in range(len(left))
    ]


def braid_residual():
    # Color-orbit order: AAB, ABA, BAA.  The scalar mixed block is
    # [[c,t],[s,u]] after identifying B tensor A with A tensor B by the flip.
    r1 = [
        [T, ZERO, ZERO],
        [ZERO, scalar(c), scalar(t)],
        [ZERO, scalar(s), scalar(u)],
    ]
    r2 = [
        [scalar(c), scalar(t), ZERO],
        [scalar(s), scalar(u), ZERO],
        [ZERO, ZERO, T],
    ]
    return matrix_subtract(
        matrix_multiply(matrix_multiply(r1, r2), r1),
        matrix_multiply(matrix_multiply(r2, r1), r2),
    )


EXPECTED = {
    (0, 0): (c * (q - s * t), c * (-c + q - 1)),
    (0, 1): (-c * t * u, 0),
    (1, 0): (-c * s * u, 0),
    (1, 1): (-c * u * (-c + u), 0),
    (1, 2): (c * t * u, 0),
    (2, 1): (c * s * u, 0),
    (2, 2): (-u * (q - s * t), -u * (q - u - 1)),
}


def check_expected(residual):
    for i in range(3):
        for j in range(3):
            actual = residual[i][j]
            expected = EXPECTED.get((i, j), (0, 0))
            assert sp.simplify(actual[0] - expected[0]) == 0
            assert sp.simplify(actual[1] - expected[1]) == 0


def controlled_middle_rank_check(max_odd_b: int = 15):
    """Enumerate the only non-scalar d=2 block ranks after excluding rank 2."""

    for b in range(1, max_odd_b + 1, 2):
        attainable = {
            sum(ranks) for ranks in itertools.product((1, 3), repeat=b)
        }
        assert 2 * b not in attainable
    return list(range(1, max_odd_b + 1, 2))


def main():
    residual = braid_residual()
    check_expected(residual)
    print("Exact AAB scalar-cross braid residual (entry: I coefficient ; T coefficient)")
    for i in range(3):
        for j in range(3):
            identity_coefficient, t_coefficient = residual[i][j]
            if identity_coefficient != 0 or t_coefficient != 0:
                print(
                    f"  ({i},{j}): "
                    f"{sp.factor(identity_coefficient)} ; "
                    f"{sp.factor(t_coefficient)}"
                )

    checked = controlled_middle_rank_check()
    print()
    print(
        "Controlled-middle parity check passed for odd middle dimensions:",
        ", ".join(map(str, checked)),
    )
    print("All assertions passed (exact SymPy arithmetic).")


if __name__ == "__main__":
    main()
