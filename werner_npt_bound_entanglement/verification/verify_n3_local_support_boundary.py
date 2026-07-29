#!/usr/bin/env python3
"""Exact checker for the local compressed-factor decomposition.

This verifier uses only Gaussian rational arithmetic.  It checks the
six product-projector decomposition

    I_4 - |Phi_2><Phi_2|/2

used in the proof of the qutrit three-copy local-support theorem.
The tensor-preservation lemma and the reduction to the already verified
two-copy theorem are proved algebraically in the accompanying note.
"""

from fractions import Fraction


ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
IUNIT = (Fraction(0), Fraction(1))


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def mul(x, y):
    return (x[0] * y[0] - x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


def scale(x, q):
    return (q * x[0], q * x[1])


def conj(x):
    return (x[0], -x[1])


def zero_matrix(rows, columns):
    return [[ZERO for _ in range(columns)] for _ in range(rows)]


def identity(size):
    out = zero_matrix(size, size)
    for i in range(size):
        out[i][i] = ONE
    return out


def matrix_add(first, second):
    return [
        [add(first[i][j], second[i][j])
         for j in range(len(first[0]))]
        for i in range(len(first))
    ]


def matrix_scale(matrix, q):
    return [[scale(value, q) for value in row] for row in matrix]


def outer(vector):
    size = len(vector)
    return [
        [mul(vector[i], conj(vector[j])) for j in range(size)]
        for i in range(size)
    ]


def kron(first, second):
    rows_first, columns_first = len(first), len(first[0])
    rows_second, columns_second = len(second), len(second[0])
    out = zero_matrix(
        rows_first * rows_second, columns_first * columns_second
    )
    for i in range(rows_first):
        for j in range(columns_first):
            for k in range(rows_second):
                for ell in range(columns_second):
                    out[i * rows_second + k][j * columns_second + ell] = (
                        mul(first[i][j], second[k][ell])
                    )
    return out


def projector(vector):
    return outer(vector)


def assert_equal(first, second):
    assert len(first) == len(second)
    assert len(first[0]) == len(second[0])
    for i in range(len(first)):
        for j in range(len(first[0])):
            assert first[i][j] == second[i][j], (
                i, j, first[i][j], second[i][j]
            )


def main():
    half = Fraction(1, 2)

    # Normalized eigenvectors of X, Y, Z.  The common 1/sqrt(2)
    # disappears in their rank-one projectors, so those projectors have
    # Gaussian-rational entries.
    px_plus = [[(half, 0), (half, 0)],
               [(half, 0), (half, 0)]]
    px_minus = [[(half, 0), (-half, 0)],
                [(-half, 0), (half, 0)]]
    py_plus = [[(half, 0), (0, -half)],
               [(0, half), (half, 0)]]
    py_minus = [[(half, 0), (0, half)],
                [(0, -half), (half, 0)]]
    pz_plus = [[ONE, ZERO], [ZERO, ZERO]]
    pz_minus = [[ZERO, ZERO], [ZERO, ONE]]

    rhs = zero_matrix(4, 4)
    for first, second in (
        (px_plus, px_minus),
        (px_minus, px_plus),
        (py_plus, py_plus),
        (py_minus, py_minus),
        (pz_plus, pz_minus),
        (pz_minus, pz_plus),
    ):
        rhs = matrix_add(rhs, matrix_scale(kron(first, second), half))

    phi = [ONE, ZERO, ZERO, ONE]
    lhs = matrix_add(
        identity(4), matrix_scale(projector(phi), -half)
    )
    assert_equal(lhs, rhs)

    # The compressed 2 x 3 factor is the direct sum of the qubit block
    # above and an identity product block on the unused second-side
    # coordinate.  Check its spectrum-free coordinate identity.
    compressed = zero_matrix(6, 6)
    # Basis ordering: (0,0),(0,1),(0,2),(1,0),(1,1),(1,2).
    for i in range(6):
        compressed[i][i] = ONE
    phi23 = [ONE, ZERO, ZERO, ZERO, ONE, ZERO]
    compressed = matrix_add(
        compressed, matrix_scale(projector(phi23), -half)
    )

    embedded = zero_matrix(6, 6)
    qubit_indices = [0, 1, 3, 4]
    for i, ii in enumerate(qubit_indices):
        for j, jj in enumerate(qubit_indices):
            embedded[ii][jj] = lhs[i][j]
    embedded[2][2] = ONE
    embedded[5][5] = ONE
    assert_equal(compressed, embedded)

    print("verified exact six-term separable compressed endpoint factor")


if __name__ == "__main__":
    main()
