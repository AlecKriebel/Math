#!/usr/bin/env python3
"""Exact checks for the split-plane fixed-left spectrum.

The script uses a tiny multivariate polynomial implementation over
fractions.  No third-party package is required.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations


# Monomials are exponent triples for (a,b,x).
Poly = dict[tuple[int, int, int], F]


def const(value: int | F) -> Poly:
    value = F(value)
    return {} if value == 0 else {(0, 0, 0): value}


def var(index: int) -> Poly:
    exponent = [0, 0, 0]
    exponent[index] = 1
    return {tuple(exponent): F(1)}


def add(*terms: Poly) -> Poly:
    out: Poly = {}
    for term in terms:
        for monomial, coefficient in term.items():
            out[monomial] = out.get(monomial, F(0)) + coefficient
            if out[monomial] == 0:
                del out[monomial]
    return out


def neg(term: Poly) -> Poly:
    return {monomial: -coefficient for monomial, coefficient in term.items()}


def sub(left: Poly, right: Poly) -> Poly:
    return add(left, neg(right))


def mul(*terms: Poly) -> Poly:
    out = const(1)
    for term in terms:
        new: Poly = {}
        for left_monomial, left_coefficient in out.items():
            for right_monomial, right_coefficient in term.items():
                monomial = tuple(
                    left_monomial[i] + right_monomial[i] for i in range(3)
                )
                new[monomial] = (
                    new.get(monomial, F(0))
                    + left_coefficient * right_coefficient
                )
        out = {m: c for m, c in new.items() if c}
    return out


def scale(value: int | F, term: Poly) -> Poly:
    return {monomial: F(value) * coefficient for monomial, coefficient in term.items()}


def determinant3(matrix: list[list[Poly]]) -> Poly:
    out: Poly = {}
    for permutation in permutations(range(3)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
        term = mul(*(matrix[i][permutation[i]] for i in range(3)))
        out = add(out, scale(-1 if inversions & 1 else 1, term))
    return out


def matrix(rows: int, columns: int) -> list[list[Poly]]:
    return [[const(0) for _ in range(columns)] for _ in range(rows)]


def inner(left: list[list[Poly]], right: list[list[Poly]]) -> Poly:
    return add(
        *(
            mul(left[i][j], right[i][j])
            for i in range(len(left))
            for j in range(len(left[0]))
        )
    )


def trace(value: list[list[Poly]]) -> Poly:
    return add(*(value[i][i] for i in range(len(value))))


def partial_trace(value: list[list[Poly]], site: int) -> list[list[Poly]]:
    out = matrix(3, 3)
    if site == 0:
        for j in range(3):
            for ell in range(3):
                out[j][ell] = add(
                    *(value[3 * i + j][3 * i + ell] for i in range(3))
                )
    else:
        for i in range(3):
            for k in range(3):
                out[i][k] = add(
                    *(value[3 * i + j][3 * k + j] for j in range(3))
                )
    return out


def endpoint_pair(
    left: list[list[Poly]], right: list[list[Poly]]
) -> Poly:
    return add(
        inner(left, right),
        scale(
            F(-1, 2),
            add(
                inner(partial_trace(left, 0), partial_trace(right, 0)),
                inner(partial_trace(left, 1), partial_trace(right, 1)),
            ),
        ),
        scale(F(1, 4), mul(trace(left), trace(right))),
    )


def main() -> None:
    a, b, x = var(0), var(1), var(2)
    a2, b2 = mul(a, a), mul(b, b)
    ab = mul(a, b)

    expected_h_block = [
        [
            add(scale(F(1, 4), a2), b2),
            scale(F(1, 4), ab),
            scale(F(1, 4), a),
        ],
        [
            scale(F(1, 4), ab),
            add(a2, scale(F(1, 4), b2)),
            scale(F(1, 4), b),
        ],
        [
            scale(F(1, 4), a),
            scale(F(1, 4), b),
            const(F(1, 4)),
        ],
    ]
    characteristic_block = [
        [
            sub(x, add(scale(F(1, 4), a2), b2)),
            scale(F(-1, 4), ab),
            scale(F(-1, 4), a),
        ],
        [
            scale(F(-1, 4), ab),
            sub(x, add(a2, scale(F(1, 4), b2))),
            scale(F(-1, 4), b),
        ],
        [
            scale(F(-1, 4), a),
            scale(F(-1, 4), b),
            sub(x, const(F(1, 4))),
        ],
    ]
    # Derive the full fixed-left matrix directly from C=Dy^T+Zw^T.
    d = matrix(3, 3)
    d[0][0], d[1][1] = a, b
    z = matrix(3, 3)
    z[2][2] = const(1)
    basis_matrices: list[list[list[Poly]]] = []
    for coordinate in range(18):
        row, column = divmod(coordinate, 2)
        w_column = matrix(3, 3)
        for physical_row in range(3):
            for physical_column in range(3):
                physical_index = 3 * physical_row + physical_column
                if column == 0:
                    w_column[physical_row][physical_column] = (
                        d[row // 3][row % 3]
                        if physical_index == row
                        else const(0)
                    )
                else:
                    w_column[physical_row][physical_column] = (
                        z[row // 3][row % 3]
                        if physical_index == row
                        else const(0)
                    )

        # The preceding compact construction is easier to audit in its
        # defining outer-product form.
        c = matrix(9, 9)
        for output in range(9):
            for input_index in range(9):
                if input_index != row:
                    continue
                code_column = column
                code_vector = (
                    d[output // 3][output % 3]
                    if code_column == 0
                    else z[output // 3][output % 3]
                )
                c[output][input_index] = code_vector
        basis_matrices.append(c)

    h = [
        [
            endpoint_pair(basis_matrices[i], basis_matrices[j])
            for j in range(18)
        ]
        for i in range(18)
    ]
    exceptional = [0, 8, 17]  # (y_11,y_22,w_33)
    derived_block = [
        [h[i][j] for j in exceptional] for i in exceptional
    ]
    assert derived_block == expected_h_block
    for i in range(18):
        for j in range(18):
            if i != j and not (i in exceptional and j in exceptional):
                assert h[i][j] == const(0)

    expected_diagonal = {
        1: const(1),
        2: scale(F(1, 2), add(a2, b2)),
        3: const(1),
        4: add(scale(F(1, 2), a2), b2),
        5: const(F(1, 2)),
        6: scale(F(1, 2), add(a2, b2)),
        7: const(1),
        9: const(1),
        10: add(a2, scale(F(1, 2), b2)),
        11: const(F(1, 2)),
        12: add(scale(F(1, 2), a2), b2),
        13: const(F(1, 2)),
        14: add(a2, scale(F(1, 2), b2)),
        15: const(F(1, 2)),
        16: add(a2, b2),
    }
    for index, value in expected_diagonal.items():
        assert h[index][index] == value

    characteristic = determinant3(characteristic_block)

    target = scale(
        F(1, 4),
        mul(
            sub(scale(2, x), const(1)),
            add(
                scale(2, mul(x, x)),
                scale(-2, x),
                mul(a2, b2),
            ),
        ),
    )
    constraint_multiple = scale(
        F(-1, 4),
        mul(
            x,
            sub(add(a2, b2), const(1)),
            add(neg(a2), neg(b2), scale(5, x), const(-2)),
        ),
    )
    assert sub(characteristic, target) == constraint_multiple

    # Exact arithmetic in Q(sqrt(2)) at a^2=b^2=1/2.
    def quadratic_add(
        left: tuple[F, F], right: tuple[F, F]
    ) -> tuple[F, F]:
        return left[0] + right[0], left[1] + right[1]

    def quadratic_mul(
        left: tuple[F, F], right: tuple[F, F]
    ) -> tuple[F, F]:
        return (
            left[0] * right[0] + 2 * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0],
        )

    lam = (F(1, 2), F(-1, 4))  # (2-sqrt(2))/4
    polynomial_value = quadratic_add(
        quadratic_add(quadratic_mul(lam, lam), (-lam[0], -lam[1])),
        (F(1, 8), F(0)),
    )
    assert polynomial_value == (F(0), F(0))
    assert (4 * lam[0], 4 * lam[1]) == (F(2), F(-1))

    print("verified: split-plane characteristic polynomial and sharp constants")


if __name__ == "__main__":
    main()
