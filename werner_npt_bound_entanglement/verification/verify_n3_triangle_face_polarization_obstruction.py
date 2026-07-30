#!/usr/bin/env python3
"""Exact checks for the strict-triangle face-polarization obstruction."""

from fractions import Fraction as F


def mat_vec(matrix, vector):
    return [
        sum(matrix[i][j] * vector[j] for j in range(len(vector)))
        for i in range(len(matrix))
    ]


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def add(left, right):
    return [x + y for x, y in zip(left, right)]


def scale(value, vector):
    return [value * x for x in vector]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def mat_add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def mat_scale(value, matrix):
    return [[value * x for x in row] for row in matrix]


def outer(left, right):
    return [[x * y for y in right] for x in left]


def determinant3(matrix):
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return (
        a * (e * i - f * h)
        - b * (d * i - f * g)
        + c * (d * h - e * g)
    )


def main():
    # A nontrivial exact rational audit of the general polarization.
    S_diag = [F(2), F(3)]
    S_inv = [F(1, 2), F(1, 3)]
    T = [
        [[F(1), F(0)], [F(1), F(1)]],
        [[F(0), F(1)], [F(2), F(0)]],
        [[F(1), F(1)], [F(0), F(2)]],
    ]
    coeff = [
        [F(1), F(2)],
        [F(2), F(-1)],
        [F(1), F(3)],
    ]
    y_edge = [mat_vec(T[e], coeff[e]) for e in range(3)]

    def s_inverse(vector):
        return [S_inv[i] * vector[i] for i in range(2)]

    def s_apply(vector):
        return [S_diag[i] * vector[i] for i in range(2)]

    def weighted(left, right):
        return dot(left, s_inverse(right))

    d_edge = [
        2 * dot(coeff[e], coeff[e]) - weighted(y_edge[e], y_edge[e])
        for e in range(3)
    ]
    c12 = weighted(y_edge[0], y_edge[1])
    c13 = weighted(y_edge[0], y_edge[2])
    c23 = weighted(y_edge[1], y_edge[2])
    alpha = c12 / d_edge[0]
    beta = c13 / d_edge[0]
    m_general = c23 + c12 * c13 / d_edge[0]
    A_general = d_edge[1] - c12 * c12 / d_edge[0]
    B_general = d_edge[2] - c13 * c13 / d_edge[0]

    zero = [F(0), F(0)]
    b = [scale(alpha, coeff[0]), coeff[1], zero]
    b_prime = [scale(beta, coeff[0]), zero, coeff[2]]
    y = add(scale(alpha, y_edge[0]), y_edge[1])
    y_prime = add(scale(beta, y_edge[0]), y_edge[2])
    z = s_inverse(y)
    z_prime = s_inverse(y_prime)

    def defect(left, right, left_y, right_y):
        return (
            2 * sum(dot(left[e], right[e]) for e in range(3))
            - dot(left_y, s_inverse(right_y))
        )

    assert defect(b, b, y, y) == A_general
    assert defect(b_prime, b_prime, y_prime, y_prime) == B_general
    assert defect(b, b_prime, y, y_prime) == -m_general

    a = [
        add(b[e], scale(F(-1, 2), mat_vec(transpose(T[e]), z)))
        for e in range(3)
    ]
    a_prime = [
        add(
            b_prime[e],
            scale(F(-1, 2), mat_vec(transpose(T[e]), z_prime)),
        )
        for e in range(3)
    ]

    frame_sum = [[F(0), F(0)], [F(0), F(0)]]
    frames = []
    for edge_map in T:
        columns = transpose(edge_map)
        frame = mat_scale(
            F(1, 2),
            mat_add(
                outer(columns[0], columns[0]),
                outer(columns[1], columns[1]),
            ),
        )
        frames.append(frame)
        frame_sum = mat_add(frame_sum, frame)
    H = [
        [
            (S_diag[i] if i == j else F(0)) - frame_sum[i][j]
            for j in range(2)
        ]
        for i in range(2)
    ]

    polarized = (
        2 * sum(dot(a[e], a_prime[e]) for e in range(3))
        + dot(z, mat_vec(H, z_prime))
    )
    assert polarized == -m_general

    f23 = mat_add(frames[1], frames[2])
    h_explicit = (
        m_general
        - 2 * dot(a[0], a_prime[0])
        - dot(z, mat_vec(f23, z_prime))
    )
    assert dot(z, mat_vec(H, z_prime)) == h_explicit
    assert dot(y_edge[1], z_prime) == m_general
    assert dot(z, y_edge[2]) == m_general

    # Scalar frame data: S=1, F_e=2/5 and T_e^2=4/5.
    S = F(1)
    frame = F(2, 5)
    face = S - 2 * frame
    full = S - 3 * frame
    assert face == F(1, 5)
    assert face == frame / 2
    assert full == -F(1, 5)

    # For B_e=1, ||T_e B_e||^2=4/5.
    d = F(2) - F(4, 5)
    c = F(4, 5)
    assert d == F(6, 5)

    A = d - c * c / d
    B = A
    m = c + c * c / d
    assert A == B == F(2, 3)
    assert m == F(4, 3)
    assert m * m == 4 * A * B
    assert m * m > A * B

    G = [
        [d, -c, -c],
        [-c, d, -c],
        [-c, -c, d],
    ]
    assert determinant3(G) == -F(8, 5)

    # Exact eigenvectors: all-ones has eigenvalue -2/5;
    # the sum-zero plane has eigenvalue 2.
    one = [F(1), F(1), F(1)]
    x = [F(1), F(-1), F(0)]
    assert mat_vec(G, one) == [F(-2, 5)] * 3
    assert mat_vec(G, x) == [F(2), F(-2), F(0)]
    assert dot(one, x) == 0

    # Every 2x2 principal minor is strictly positive.
    assert d * d - c * c == F(4, 5)

    # The normalized Bargmann correlations are strictly interior.
    z = c / d
    assert z == F(2, 3)
    assert abs(z) < 1
    bargmann = 1 - 3 * z * z - 2 * z * z * z
    assert bargmann == F(-25, 27)

    print("verified exact strict-triangle polarization obstruction")
    print(f"face residual = {face}, full residual = {full}")
    print(f"A = B = {A}, m = {m}, |m|^2/(AB) = 4")


if __name__ == "__main__":
    main()
