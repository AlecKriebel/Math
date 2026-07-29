#!/usr/bin/env python3
"""Dependency-free exact checker for the logical block-Gram obstruction."""

from fractions import Fraction as F


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def zero(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def kron(left, right):
    return [
        [
            left[i][j] * right[k][ell]
            for j in range(len(left[0]))
            for ell in range(len(right[0]))
        ]
        for i in range(len(left))
        for k in range(len(right))
    ]


def scale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def matvec(matrix, vector):
    return [
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), F(0))
        for i in range(len(matrix))
    ]


def inner(left, right):
    return sum((x * y for x, y in zip(left, right)), F(0))


def hs_norm_squared(matrix):
    return sum((x * x for row in matrix for x in row), F(0))


def trace(matrix):
    return sum((matrix[i][i] for i in range(len(matrix))), F(0))


def index(word):
    return 9 * word[0] + 3 * word[1] + word[2]


def basis_vector(word):
    out = [F(0) for _ in range(27)]
    out[index(word)] = F(1)
    return out


def main():
    identity = eye(3)
    e = zero(3, 3)
    f = zero(3, 3)
    z = zero(3, 3)
    e[0][1] = F(1)
    f[1][0] = F(1)
    for i, value in enumerate((F(1), F(-1, 2), F(-1, 2))):
        z[i][i] = value
    assert trace(e) == trace(f) == trace(z) == 0

    b1 = kron(e, e)
    b2 = scale(F(2, 3), kron(f, z))
    b3 = scale(F(2, 3), kron(f, z))
    d1 = kron(identity, b1)
    d2 = scale(F(2, 3), kron(f, kron(identity, z)))
    d3 = scale(F(2, 3), kron(f, kron(z, identity)))

    b_norms = (
        hs_norm_squared(b1),
        hs_norm_squared(b2),
        hs_norm_squared(b3),
    )
    assert b_norms == (F(1), F(2, 3), F(2, 3))

    u = basis_vector((0, 0, 0))
    v = basis_vector((1, 1, 1))
    assert inner(u, u) == inner(v, v) == 1
    assert inner(u, v) == 0

    # q_1=|1>, q_2=q_3=|0>.
    selected_outputs = (matvec(d1, v), matvec(d2, u), matvec(d3, u))
    target = basis_vector((1, 0, 0))
    assert selected_outputs[0] == target
    assert selected_outputs[1] == [F(2, 3) * x for x in target]
    assert selected_outputs[2] == [F(2, 3) * x for x in target]
    total = [
        sum((selected_outputs[i][k] for i in range(3)), F(0))
        for k in range(27)
    ]
    output_norm = inner(total, total)
    input_budget = sum(b_norms, F(0))
    assert output_norm == F(49, 9)
    assert input_budget == F(7, 3)
    assert output_norm / input_budget == F(7, 3)
    assert input_budget - output_norm == F(-28, 9)

    # The ordinary scalar deficit still is positive definite.
    outputs = [(matvec(d, u), matvec(d, v)) for d in (d1, d2, d3)]
    h = [
        [
            inner(outputs[i][0], outputs[j][0])
            + inner(outputs[i][1], outputs[j][1])
            for j in range(3)
        ]
        for i in range(3)
    ]
    assert h == [
        [F(1), F(0), F(0)],
        [F(0), F(4, 9), F(4, 9)],
        [F(0), F(4, 9), F(4, 9)],
    ]
    m = [
        [
            (2 * b_norms[i] if i == j else F(0)) - h[i][j]
            for j in range(3)
        ]
        for i in range(3)
    ]
    assert m == [
        [F(1), F(0), F(0)],
        [F(0), F(8, 9), F(-4, 9)],
        [F(0), F(-4, 9), F(8, 9)],
    ]
    assert m[0][0] > 0
    assert m[1][1] * m[2][2] - m[1][2] * m[2][1] == F(16, 27) > 0
    assert (
        m[0][0]
        * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        == F(16, 27)
    )

    print("logical block-Gram quotient:", output_norm / input_budget)
    print("logical block-Gram deficit:", input_budget - output_norm)
    print("scalar determinant:", F(16, 27))


if __name__ == "__main__":
    main()
