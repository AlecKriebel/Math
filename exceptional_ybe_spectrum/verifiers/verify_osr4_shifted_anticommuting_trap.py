#!/usr/bin/env python3
"""Exact verifier for the d=6 OSR-four shifted-anticommuting trap."""

from __future__ import annotations

import sympy as sp


def kron(*matrices: sp.MatrixBase) -> sp.SparseMatrix:
    out: sp.MatrixBase = sp.SparseMatrix([[1]])
    for matrix in matrices:
        out = sp.kronecker_product(out, matrix)
    return sp.SparseMatrix(out)


def is_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def partial_trace_first(matrix: sp.MatrixBase, d: int) -> sp.SparseMatrix:
    return sp.SparseMatrix(
        d * d,
        d * d,
        lambda row, column: sum(
            matrix[
                (site * d * d) + row,
                (site * d * d) + column,
            ]
            for site in range(d)
        ),
    )


def partial_trace_last(matrix: sp.MatrixBase, d: int) -> sp.SparseMatrix:
    return sp.SparseMatrix(
        d * d,
        d * d,
        lambda row, column: sum(
            matrix[
                (row // d) * d * d + (row % d) * d + site,
                (column // d) * d * d + (column % d) * d + site,
            ]
            for site in range(d)
        ),
    )


def partial_trace_site_first_two(
    matrix: sp.MatrixBase, d: int
) -> sp.SparseMatrix:
    return sp.SparseMatrix(
        d,
        d,
        lambda b, e: sum(
            matrix[d * a + b, d * a + e] for a in range(d)
        ),
    )


def partial_trace_site_second_two(
    matrix: sp.MatrixBase, d: int
) -> sp.SparseMatrix:
    return sp.SparseMatrix(
        d,
        d,
        lambda a, c: sum(
            matrix[d * a + b, d * c + b] for b in range(d)
        ),
    )


def realignment(matrix: sp.MatrixBase, d: int) -> sp.SparseMatrix:
    return sp.SparseMatrix(
        d * d,
        d * d,
        lambda row, column: matrix[
            d * (row // d) + column // d,
            d * (row % d) + column % d,
        ],
    )


def squared_norm(matrix: sp.MatrixBase) -> sp.Expr:
    return sp.simplify(
        sum(sp.conjugate(entry) * entry for entry in matrix)
    )


def stacked_sandwich(
    outer: tuple[sp.MatrixBase, ...],
    tests: tuple[sp.MatrixBase, ...],
) -> sp.Matrix:
    columns = []
    for first in range(4):
        for second in range(4):
            columns.append(
                sp.Matrix.vstack(
                    *[
                        sp.Matrix(
                            outer[first] * test * outer[second]
                        ).reshape(36, 1)
                        for test in tests
                    ]
                )
            )
    return sp.Matrix.hstack(*columns)


def hermitian_coordinates(matrix: sp.MatrixBase) -> sp.Matrix:
    coordinates = [sp.simplify(matrix[index, index]) for index in range(4)]
    for row in range(4):
        for column in range(row + 1, 4):
            real, imaginary = sp.expand_complex(
                matrix[row, column]
            ).as_real_imag()
            coordinates.extend([sp.simplify(real), sp.simplify(imaginary)])
    return sp.Matrix(coordinates)


def hermitian_kernel_basis(
    stacked: sp.MatrixBase,
) -> list[sp.Matrix]:
    candidates = []
    for vector in stacked.nullspace():
        coefficient = sp.Matrix(4, 4, list(vector))
        candidates.extend(
            [
                sp.simplify(coefficient + coefficient.H),
                sp.simplify((coefficient - coefficient.H) / sp.I),
            ]
        )

    selected: list[sp.Matrix] = []
    coordinate_matrix = sp.zeros(16, 0)
    rank = 0
    for candidate in candidates:
        if candidate == sp.zeros(4):
            continue
        enlarged = coordinate_matrix.row_join(
            hermitian_coordinates(candidate)
        )
        enlarged_rank = enlarged.rank()
        if enlarged_rank > rank:
            selected.append(candidate)
            coordinate_matrix = enlarged
            rank = enlarged_rank
    return selected


def signature(matrix: sp.MatrixBase) -> tuple[int, int, int, int]:
    positive = 0
    negative = 0
    zero = 0
    for eigenvalue, multiplicity in matrix.eigenvals().items():
        if eigenvalue == 0:
            zero += multiplicity
        elif sp.N(eigenvalue, 50) > 0:
            positive += multiplicity
        else:
            negative += multiplicity
    return matrix.rank(), positive, negative, zero


def main() -> None:
    d = 6
    i2 = sp.eye(2)
    x = sp.Matrix([[0, 1], [1, 0]])
    y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    z = sp.diag(1, -1)
    p0 = sp.diag(1, 0, 0)
    p1 = sp.eye(3) - p0
    x12 = sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]])
    z12 = sp.diag(0, 1, -1)
    c = 1 / sp.sqrt(2)

    c0 = p0 + c * p1
    c1 = c * p1
    s0 = c * x12
    s1 = p0 + c * z12

    assert is_zero(c0 * s0 - s0 * c0)
    assert is_zero(c1 * s1 - s1 * c1)
    assert is_zero(c0**2 + s0**2 - sp.eye(3))
    assert is_zero(c1**2 + s1**2 - sp.eye(3))
    right_qutrit_columns = sp.Matrix.hstack(
        *[sp.Matrix(value).reshape(9, 1) for value in (c0, c1, s0, s1)]
    )
    assert right_qutrit_columns.rank() == 4

    left = (
        kron(x, p0),
        kron(x, p1),
        kron(y, p0),
        kron(y, p1),
    )
    right = (
        kron(z, c0),
        kron(z, c1),
        kron(z, s0),
        kron(z, s1),
    )
    h = sum(
        (kron(left[index], right[index]) for index in range(4)),
        sp.zeros(d * d),
    )
    h = sp.SparseMatrix(h)

    assert is_zero(h.H - h)
    assert is_zero(h * h - sp.eye(d * d))
    assert sp.trace(h) == 0
    assert is_zero(partial_trace_site_first_two(h, d))
    assert is_zero(partial_trace_site_second_two(h, d))
    assert realignment(h, d).rank() == 4
    assert all(
        is_zero(right[i] * left[j] + left[j] * right[i])
        for i in range(4)
        for j in range(4)
    )

    identity_d = sp.eye(d)
    ss = kron(h, identity_d)
    tt = kron(identity_d, h)
    assert is_zero(ss * tt + tt * ss)

    residual = sp.SparseMatrix(
        ss * tt * ss
        - tt * ss * tt
        - sp.Rational(1, 3) * (ss - tt)
    )
    assert is_zero(residual - sp.Rational(2, 3) * (ss - tt))
    assert squared_norm(residual) == 192

    n3 = d**3
    grad_s = sp.Rational(2, n3) * (
        tt * ss * residual
        + residual * ss * tt
        - tt * residual * tt
        - residual / 3
    )
    grad_t = sp.Rational(2, n3) * (
        ss * residual * ss
        - ss * tt * residual
        - residual * tt * ss
        + residual / 3
    )
    gradient_h = partial_trace_last(grad_s, d) + partial_trace_first(grad_t, d)
    assert is_zero(
        gradient_h - sp.Rational(64, 9 * d * d) * h
    )

    stack_right_given_left = stacked_sandwich(
        right, (sp.eye(d), *left)
    )
    stack_left_given_right = stacked_sandwich(
        left, (sp.eye(d), *right)
    )
    assert stack_right_given_left.shape == (5 * d * d, 16)
    assert stack_left_given_right.shape == (5 * d * d, 16)
    assert stack_right_given_left.rank() == 5
    assert stack_left_given_right.rank() == 4
    assert len(stack_right_given_left.nullspace()) == 11
    assert len(stack_left_given_right.nullspace()) == 12

    hermitian_right_given_left = hermitian_kernel_basis(
        stack_right_given_left
    )
    hermitian_left_given_right = hermitian_kernel_basis(
        stack_left_given_right
    )
    assert len(hermitian_right_given_left) == 11
    assert len(hermitian_left_given_right) == 12
    signatures_right_given_left = [
        signature(matrix) for matrix in hermitian_right_given_left
    ]
    signatures_left_given_right = [
        signature(matrix) for matrix in hermitian_left_given_right
    ]
    assert signatures_right_given_left.count((2, 1, 1, 2)) == 10
    assert signatures_right_given_left.count((3, 2, 1, 1)) == 1
    assert signatures_left_given_right == [(2, 1, 1, 2)] * 12

    print("PASS exact d=6 Hermitian involution and zero marginals")
    print("PASS exact operator-Schmidt rank 4")
    print("PASS shifted anticommutation H12 H23 = -H23 H12")
    print("PASS exceptional residual squared norm 192 (normalized 8/9)")
    print("PASS normalized residual gradient = 64/(9d^2) H")
    print("PASS stacked K_{R|L}: rank 5, kernel dimension 11")
    print("PASS stacked K_{L|R}: rank 4, kernel dimension 12")
    print("PASS Hermitian kernel bases: 11 and 12 exact generators")
    print("PASS generator signatures R|L: 10*(1,1,2), 1*(2,1,1)")
    print("PASS generator signatures L|R: 12*(1,1,2)")
    print("SCOPE exact stationary optimizer trap, not an exceptional solution")


if __name__ == "__main__":
    main()
