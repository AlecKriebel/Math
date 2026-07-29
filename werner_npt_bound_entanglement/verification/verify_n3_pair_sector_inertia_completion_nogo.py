#!/usr/bin/env python3
"""Exact checker for the residual-inertia completion obstruction."""

from fractions import Fraction as F


def zeros(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def scale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def multiply(left, right):
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(len(right))),
                F(0),
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def kron(left, right):
    return [
        [
            left[i // len(right)][j // len(right[0])]
            * right[i % len(right)][j % len(right[0])]
            for j in range(len(left[0]) * len(right[0]))
        ]
        for i in range(len(left) * len(right))
    ]


def det2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def det3(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def block_spinflip(matrix):
    """Apply s(A)=Tr(A)I_2-A to each logical 2x2 block."""
    out = zeros(6, 6)
    for i in range(3):
        for j in range(3):
            block = [
                [matrix[2 * i + a][2 * j + b] for b in range(2)]
                for a in range(2)
            ]
            tr = block[0][0] + block[1][1]
            flipped = [
                [tr - block[0][0], -block[0][1]],
                [-block[1][0], tr - block[1][1]],
            ]
            for a in range(2):
                for b in range(2):
                    out[2 * i + a][2 * j + b] = flipped[a][b]
    return out


def matvec(matrix, vector):
    return [
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), F(0))
        for i in range(len(matrix))
    ]


def main():
    M = [
        [F(1), F(-3, 4), F(-3, 4)],
        [F(-3, 4), F(1), F(-3, 4)],
        [F(-3, 4), F(-3, 4), F(1)],
    ]
    assert all(M[i][i] == 1 for i in range(3))
    for i in range(3):
        for j in range(i + 1, 3):
            principal = [[M[i][i], M[i][j]], [M[j][i], M[j][j]]]
            assert det2(principal) == F(7, 16)
    assert det3(M) == F(-49, 32)

    # An exact eigenbasis certifies inertia(M)=(2,1,0).
    eigenvectors = [
        ([F(1), F(1), F(1)], F(-1, 2)),
        ([F(1), F(-1), F(0)], F(7, 4)),
        ([F(1), F(1), F(-2)], F(7, 4)),
    ]
    for vector, eigenvalue in eigenvectors:
        assert matvec(M, vector) == [eigenvalue * x for x in vector]

    P0 = [[F(1), F(0)], [F(0), F(0)]]
    N = kron(M, P0)
    completion = add(N, block_spinflip(N))
    assert completion == kron(M, eye(2))

    # Every two-component logical principal block is PSD: it is a
    # 2x2 scalar matrix with eigenvalues 1/4 and 7/4, tensored with P0.
    for i in range(3):
        for j in range(i + 1, 3):
            scalar_pair = [[M[i][i], M[i][j]], [M[j][i], M[j][j]]]
            assert det2(scalar_pair) == F(7, 16)
            assert scalar_pair[0][0] == scalar_pair[1][1] == 1

    # N has the three eigenvalues of M in logical sector 0 and three
    # zero eigenvalues in logical sector 1: inertia (2+,1-,3zero).
    for vector, eigenvalue in eigenvectors:
        lifted = []
        for entry in vector:
            lifted.extend([entry, F(0)])
        assert matvec(N, lifted) == [eigenvalue * x for x in lifted]
    for component in range(3):
        logical_one = [F(0)] * 6
        logical_one[2 * component + 1] = F(1)
        assert matvec(N, logical_one) == [F(0)] * 6

    # Formal common-Gram realization N=diag(2 I_2)-G.
    G = add(scale(F(2), eye(6)), scale(F(-1), N))
    assert add(N, G) == scale(F(2), eye(6))

    # The displayed eigenbasis also certifies G>0:
    # eigenvalues 2-lambda(M) in logical sector 0 and 2 in sector 1.
    expected_g_eigenvalues = [F(5, 2), F(1, 4), F(1, 4)]
    for (vector, _), eigenvalue in zip(eigenvectors, expected_g_eigenvalues):
        lifted = []
        for entry in vector:
            lifted.extend([entry, F(0)])
        assert matvec(G, lifted) == [eigenvalue * x for x in lifted]
    for component in range(3):
        logical_one = [F(0)] * 6
        logical_one[2 * component + 1] = F(1)
        assert matvec(G, logical_one) == [F(2) * x for x in logical_one]

    # Each diagonal Gram block is diag(1,2) <= 2 I_2.
    for i in range(3):
        block = [
            [G[2 * i + a][2 * i + b] for b in range(2)]
            for a in range(2)
        ]
        assert block == [[F(1), F(0)], [F(0), F(2)]]

    print("verified: all scalar 1x1 and 2x2 principal minors are positive")
    print("verified: inertia(N) = (2 positive, 1 negative, 3 zero)")
    print("verified: every two-component logical residual is PSD")
    print("verified: N + spinflip(N) = M tensor I_2")
    print("verified: N = diag(2 I_2) - G with G positive definite")
    print("det(M) =", det3(M))


if __name__ == "__main__":
    main()
