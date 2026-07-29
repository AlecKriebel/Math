#!/usr/bin/env python3
"""Exact checker for the two-negative-direction logical residual."""

from fractions import Fraction as Fq


def zeros(rows, cols):
    return [[Fq(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = Fq(1)
    return out


def add(*matrices):
    rows, cols = len(matrices[0]), len(matrices[0][0])
    return [
        [sum((matrix[i][j] for matrix in matrices), Fq(0))
         for j in range(cols)]
        for i in range(rows)
    ]


def scale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    return [
        [
            sum((left[i][k] * right[k][j]
                 for k in range(len(right))), Fq(0))
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


def hs_inner(left, right):
    return sum(
        (left[i][j] * right[i][j]
         for i in range(len(left))
         for j in range(len(left[0]))),
        Fq(0),
    )


def trace(matrix):
    return sum((matrix[i][i] for i in range(len(matrix))), Fq(0))


def index(word):
    return 9 * word[0] + 3 * word[1] + word[2]


def embed_pair(pair_matrix, spectator):
    """Insert an identity on `spectator`; pair sites stay ordered."""
    out = zeros(27, 27)
    pair_sites = [site for site in range(3) if site != spectator]
    for a0 in range(3):
        for a1 in range(3):
            for a2 in range(3):
                row = (a0, a1, a2)
                for b0 in range(3):
                    for b1 in range(3):
                        for b2 in range(3):
                            col = (b0, b1, b2)
                            if row[spectator] != col[spectator]:
                                continue
                            pair_row = 3 * row[pair_sites[0]] + row[pair_sites[1]]
                            pair_col = 3 * col[pair_sites[0]] + col[pair_sites[1]]
                            out[index(row)][index(col)] = pair_matrix[pair_row][pair_col]
    return out


def block_matrix(blocks):
    block_rows = len(blocks)
    block_cols = len(blocks[0])
    rows = len(blocks[0][0])
    cols = len(blocks[0][0][0])
    out = zeros(block_rows * rows, block_cols * cols)
    for i in range(block_rows):
        for j in range(block_cols):
            for a in range(rows):
                for b in range(cols):
                    out[i * rows + a][j * cols + b] = blocks[i][j][a][b]
    return out


def submatrix(matrix, order):
    return [[matrix[i][j] for j in order] for i in order]


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


def main():
    I = eye(3)
    E = zeros(3, 3)
    E[0][1] = Fq(1)
    P = transpose(E)
    Z0 = [
        [Fq(1), Fq(0), Fq(0)],
        [Fq(0), Fq(-1, 2), Fq(0)],
        [Fq(0), Fq(0), Fq(-1, 2)],
    ]
    Z1 = [
        [Fq(-1, 2), Fq(0), Fq(0)],
        [Fq(0), Fq(1), Fq(0)],
        [Fq(0), Fq(0), Fq(-1, 2)],
    ]
    assert trace(E) == trace(P) == trace(Z0) == trace(Z1) == 0

    B1 = add(kron(E, E), kron(P, P))
    B2 = scale(Fq(2, 3), add(kron(P, Z0), kron(E, Z1)))
    B3 = B2
    pair_coefficients = [B1, B2, B3]
    budgets = [hs_inner(B, B) for B in pair_coefficients]
    assert budgets == [Fq(2), Fq(4, 3), Fq(4, 3)]

    # Partial traces of every pair coefficient vanish.
    for B in pair_coefficients:
        for first in (True, False):
            reduced = zeros(3, 3)
            for a in range(3):
                for b in range(3):
                    for t in range(3):
                        if first:
                            reduced[a][b] += B[3 * t + a][3 * t + b]
                        else:
                            reduced[a][b] += B[3 * a + t][3 * b + t]
            assert reduced == zeros(3, 3)

    V = zeros(27, 2)
    V[index((0, 0, 0))][0] = Fq(1)
    V[index((1, 1, 1))][1] = Fq(1)
    assert multiply(transpose(V), V) == eye(2)

    operators = [
        embed_pair(B1, 0),
        embed_pair(B2, 1),
        embed_pair(B3, 2),
    ]
    X = [multiply(operator, V) for operator in operators]

    expected = [zeros(27, 2) for _ in range(3)]
    expected[0][index((0, 1, 1))][0] = Fq(1)
    expected[0][index((1, 0, 0))][1] = Fq(1)
    expected[1][index((1, 0, 0))][0] = Fq(2, 3)
    expected[1][index((0, 1, 1))][1] = Fq(2, 3)
    expected[2][index((1, 0, 0))][0] = Fq(2, 3)
    expected[2][index((0, 1, 1))][1] = Fq(2, 3)
    assert X == expected

    A = [
        [multiply(transpose(X[i]), X[j]) for j in range(3)]
        for i in range(3)
    ]
    N_blocks = [
        [
            add(
                scale(budgets[i] if i == j else Fq(0), eye(2)),
                scale(Fq(-1), A[i][j]),
            )
            for j in range(3)
        ]
        for i in range(3)
    ]
    N = block_matrix(N_blocks)

    # The two aligned-output triples give identical 3x3 blocks.
    order = [0, 3, 5, 1, 2, 4]
    H = [
        [Fq(1), Fq(-2, 3), Fq(-2, 3)],
        [Fq(-2, 3), Fq(8, 9), Fq(-4, 9)],
        [Fq(-2, 3), Fq(-4, 9), Fq(8, 9)],
    ]
    assert submatrix(N, order) == block_matrix(
        [[H, zeros(3, 3)], [zeros(3, 3), H]]
    )

    # Exact LDL pivots: +,+,- in each block.
    delta1 = H[0][0]
    delta2 = det2([row[:2] for row in H[:2]])
    delta3 = det3(H)
    assert (delta1, delta2, delta3) == (
        Fq(1), Fq(4, 9), Fq(-16, 27)
    )
    assert (delta1, delta2 / delta1, delta3 / delta2) == (
        Fq(1), Fq(4, 9), Fq(-4, 3)
    )

    # The exterior-square quadratic form is strictly negative.
    q = [[Fq(1)], [Fq(1)], [Fq(1)]]
    p = [[Fq(0)], [Fq(1)], [Fq(-1)]]
    qHq = multiply(transpose(q), multiply(H, q))[0][0]
    pHp = multiply(transpose(p), multiply(H, p))[0][0]
    qHp = multiply(transpose(q), multiply(H, p))[0][0]
    assert (qHq, pHp, qHp) == (Fq(-7, 9), Fq(8, 3), Fq(0))
    assert qHq * pHp - qHp * qHp == Fq(-56, 27)

    # The actual scalar deficit is strictly positive.
    d = [2 * budgets[i] - trace(A[i][i]) for i in range(3)]
    c12, c13, c23 = trace(A[0][1]), trace(A[0][2]), trace(A[1][2])
    assert d == [Fq(2), Fq(16, 9), Fq(16, 9)]
    assert (c12, c13, c23) == (Fq(0), Fq(0), Fq(8, 9))
    M = [
        [d[0], -c12, -c13],
        [-c12, d[1], -c23],
        [-c13, -c23, d[2]],
    ]
    assert det3(M) == Fq(128, 27)

    print("verified exact doubly-traceless physical construction")
    print("inertia(N) = (4 positive, 2 negative, 0 zero)")
    print("wedge-square negative value =", qHq * pHp - qHp * qHp)
    print("det(M) =", det3(M))


if __name__ == "__main__":
    main()
