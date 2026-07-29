#!/usr/bin/env python3
"""Exact checks for the logical spin-flip pair-sector obstruction.

Only Python's standard library is used.
"""

from fractions import Fraction as F


def add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def mul(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def scale(value, scalar):
    return [[scalar * x for x in row] for row in value]


def spinflip(matrix):
    epsilon = [[F(0), F(1)], [F(-1), F(0)]]
    epsilon_dagger = transpose(epsilon)
    return mul(mul(epsilon, transpose(matrix)), epsilon_dagger)


def eye(size):
    return [
        [F(1 if i == j else 0) for j in range(size)]
        for i in range(size)
    ]


def main():
    # Check s(A)=(Tr A)I-A on a generic rational 2x2 matrix.
    A = [[F(2), F(3)], [F(5), F(7)]]
    assert spinflip(A) == add(
        scale(eye(2), trace(A)),
        scale(A, F(-1)),
    )

    # Sparse physical obstruction to positivity of the spin-flipped Gram.
    # X_1=(|000>,|100>), X_2=0, X_3=(0,-|000>) gives
    # A_11=I, A_33=diag(0,1), A_13=[[0,-1],[0,0]].
    a11 = eye(2)
    a33 = [[F(0), F(0)], [F(0), F(1)]]
    a13 = [[F(0), F(-1)], [F(0), F(0)]]
    sf11 = spinflip(a11)
    sf33 = spinflip(a33)
    sf13 = spinflip(a13)
    spinflip_principal = [
        [sf11[0][0], sf13[0][1]],
        [sf13[0][1], sf33[1][1]],
    ]
    assert spinflip_principal == [[F(1), F(1)], [F(1), F(0)]]
    assert (
        spinflip_principal[0][0] * spinflip_principal[1][1]
        - spinflip_principal[0][1] * spinflip_principal[1][0]
        == F(-1)
    )

    # Exact physical example.
    b = F(4, 81)
    a0 = F(16, 729)
    a1 = F(1, 729)

    # N on each logical diagonal sector is b I_3-a J_3.
    # Its eigenvalues are b-3a and b (twice).
    n0 = (b - 3 * a0, b, b)
    n1 = (b - 3 * a1, b, b)
    assert n0[0] == F(-4, 243)
    assert n1[0] == F(11, 243)
    assert min(n0 + n1) < 0

    d = 2 * b - a0 - a1
    c = a0 + a1
    assert d == F(55, 729)
    assert c == F(17, 729)

    # M=d I_3-c(J_3-I_3) has eigenvalues d-2c,d+c,d+c.
    m_spectrum = (d - 2 * c, d + c, d + c)
    assert m_spectrum == (F(7, 243), F(8, 81), F(8, 81))
    assert all(value > 0 for value in m_spectrum)

    # Fully three-component equality.  The two logical residual blocks
    # are a path Laplacian and a weighted-triangle Laplacian.
    path = [
        [F(1), F(-1), F(0)],
        [F(-1), F(2), F(-1)],
        [F(0), F(-1), F(1)],
    ]
    triangle = [
        [F(3, 2), F(-1), F(-1, 2)],
        [F(-1), F(2), F(-1)],
        [F(-1, 2), F(-1), F(3, 2)],
    ]
    vectors = ([F(1), F(1), F(1)], [F(1), F(0), F(-1)], [F(1), F(-2), F(1)])

    def matvec(matrix, vector):
        return [
            sum(matrix[i][j] * vector[j] for j in range(len(vector)))
            for i in range(len(matrix))
        ]

    assert matvec(path, vectors[0]) == [F(0)] * 3
    assert matvec(path, vectors[1]) == list(vectors[1])
    assert matvec(path, vectors[2]) == [3 * x for x in vectors[2]]
    assert matvec(triangle, vectors[0]) == [F(0)] * 3
    assert matvec(triangle, vectors[1]) == [2 * x for x in vectors[1]]
    assert matvec(triangle, vectors[2]) == [3 * x for x in vectors[2]]
    equality_m = add(path, triangle)
    assert matvec(equality_m, vectors[0]) == [F(0)] * 3
    assert matvec(equality_m, vectors[1]) == [3 * x for x in vectors[1]]
    assert matvec(equality_m, vectors[2]) == [6 * x for x in vectors[2]]

    # Check the polarized 2x2 Cayley--Hamilton identity exactly.
    K1 = [[F(1), F(2)], [F(3), F(5)]]
    K2 = [[F(-2), F(1)], [F(4), F(3)]]
    K3 = [[F(7), F(-1)], [F(2), F(6)]]
    lhs = trace(K1) * trace(K2) * trace(K3)
    rhs = (
        trace(mul(K1, K2)) * trace(K3)
        + trace(mul(K1, K3)) * trace(K2)
        + trace(mul(K2, K3)) * trace(K1)
        - trace(mul(mul(K1, K2), K3))
        - trace(mul(mul(K1, K3), K2))
    )
    assert lhs == rhs

    print("verified: blockwise logical spin flip gives M tensor I_2")
    print("verified: a physical spin-flipped Gram has a -1 principal minor")
    print("verified: the physical naive residual has eigenvalue -4/243")
    print("verified: the corresponding scalar M is strictly positive")
    print("verified: the fully three-component equality has spectra 0,3,6")
    print("verified: the polarized logical three-cycle identity is exact")


if __name__ == "__main__":
    main()
