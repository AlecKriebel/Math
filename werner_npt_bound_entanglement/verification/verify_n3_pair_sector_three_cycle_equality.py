#!/usr/bin/env python3
"""Dependency-free exact checker for the three-cycle equality."""

from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Q2:
    """The real quadratic field Q(sqrt(2))."""

    a: F = F(0)
    b: F = F(0)

    def __add__(self, other):
        other = as_q2(other)
        return Q2(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q2(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-as_q2(other))

    def __rsub__(self, other):
        return as_q2(other) - self

    def __mul__(self, other):
        other = as_q2(other)
        return Q2(
            self.a * other.a + 2 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = as_q2(other)
        denominator = other.a * other.a - 2 * other.b * other.b
        return self * Q2(other.a / denominator, -other.b / denominator)


def as_q2(value):
    return value if isinstance(value, Q2) else Q2(F(value), F(0))


ZERO = Q2()
ONE = Q2(F(1))
INV_SQRT2 = Q2(F(0), F(1, 2))


def index(word):
    return 9 * word[0] + 3 * word[1] + word[2]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


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


def add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def matvec(matrix, vector):
    return [
        sum((as_q2(matrix[i][j]) * vector[j] for j in range(len(vector))), ZERO)
        for i in range(len(matrix))
    ]


def inner(left, right):
    # Every entry in this certificate is real.
    return sum((x * y for x, y in zip(left, right)), ZERO)


def hs_norm_squared(matrix):
    return sum(
        (value * value for row in matrix for value in row),
        F(0),
    )


def main():
    identity = eye(3)
    z = [[F(0) for _ in range(3)] for _ in range(3)]
    s = [[F(0) for _ in range(3)] for _ in range(3)]
    e = [[F(0) for _ in range(3)] for _ in range(3)]
    f = [[F(0) for _ in range(3)] for _ in range(3)]
    for i, value in enumerate((1, -1, 0)):
        z[i][i] = F(value)
    for i, value in enumerate((1, 0, -1)):
        s[i][i] = F(value)
    e[2][0] = F(1)
    f[1][0] = F(1)

    b1 = kron(z, e)
    b2 = add(kron(z, e), kron(f, s))
    b3 = kron(f, z)
    d1 = kron(identity, b1)
    d2 = add(kron(z, kron(identity, e)), kron(f, kron(identity, s)))
    d3 = kron(b3, identity)

    assert hs_norm_squared(b1) == F(2)
    assert hs_norm_squared(b2) == F(4)
    assert hs_norm_squared(b3) == F(2)

    u = [ZERO for _ in range(27)]
    v = [ZERO for _ in range(27)]
    u[index((0, 0, 0))] = ONE
    v[index((1, 1, 0))] = INV_SQRT2
    v[index((0, 1, 2))] = INV_SQRT2
    assert inner(u, u) == ONE
    assert inner(v, v) == ONE
    assert inner(u, v) == ZERO

    outputs = [(matvec(d, u), matvec(d, v)) for d in (d1, d2, d3)]
    h = [[ZERO for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            h[i][j] = inner(outputs[i][0], outputs[j][0]) + inner(
                outputs[i][1], outputs[j][1]
            )

    assert [h[i][i] for i in range(3)] == [
        Q2(F(3, 2)),
        Q2(F(4)),
        Q2(F(3, 2)),
    ]
    assert h[0][1] == h[1][0] == Q2(F(2))
    assert h[1][2] == h[2][1] == Q2(F(2))
    assert h[0][2] == h[2][0] == Q2(F(1, 2))

    b_norms = (F(2), F(4), F(2))
    diagonals = [Q2(2 * b_norms[i]) - h[i][i] for i in range(3)]
    assert diagonals == [Q2(F(5, 2)), Q2(F(4)), Q2(F(5, 2))]

    m = [
        [F(5, 2), F(-2), F(-1, 2)],
        [F(-2), F(4), F(-2)],
        [F(-1, 2), F(-2), F(5, 2)],
    ]
    q = (F(1), F(-2), F(1))
    r = (F(1), F(0), F(-1))
    gram = [
        [q[i] * q[j] + F(3, 2) * r[i] * r[j] for j in range(3)]
        for i in range(3)
    ]
    assert m == gram
    assert all(sum(row) == 0 for row in m)

    principal_determinants = (
        m[0][0] * m[1][1] - m[0][1] * m[1][0],
        m[0][0] * m[2][2] - m[0][2] * m[2][0],
        m[1][1] * m[2][2] - m[1][2] * m[2][1],
    )
    assert principal_determinants == (F(6), F(6), F(6))

    total_u = [sum((outputs[i][0][k] for i in range(3)), ZERO) for k in range(27)]
    total_v = [sum((outputs[i][1][k] for i in range(3)), ZERO) for k in range(27)]
    total_output_squared = inner(total_u, total_u) + inner(total_v, total_v)
    assert total_output_squared == Q2(F(16))
    assert total_output_squared == Q2(2 * sum(b_norms))

    # Exact failure of the squared normalized-row condition:
    # (2/sqrt(10) + 2/sqrt(10)) > 1 iff 16 > 10.
    assert F(16) > F(10)

    # General sparse-family factor at a second rational point.
    z0, z1, z2 = F(10), F(-9), F(-1)
    a, b, c = F(1), F(-1), F(0)
    d = z0 * z0 + F(3, 2) * z1 * z1 + 2 * z2 * z2
    middle = 2 * a * a + 2 * b * b + 4 * c * c
    cross = z0 * a + z1 * b
    outer_cross = z1 * z1 / 2
    factor = (d + outer_cross) * (
        middle * (d - outer_cross) - 2 * cross * cross
    )
    direct = (
        d * d * middle
        - 2 * d * cross * cross
        - middle * outer_cross * outer_cross
        - 2 * cross * cross * outer_cross
    )
    assert factor == direct == F(2640)

    # Coordinate-free Gram remainder in the standard active plane:
    # t=(a,b,c), z=(z0,z1,z2).
    active_wedge = (a * z1 - b * z0) ** 2
    q_t_p_z = 2 * c * c * (z0 * z0 + z1 * z1)
    p_t_q_z = 2 * z2 * z2 * (a * a + b * b)
    q_t_q_z = 4 * c * c * z2 * z2
    delta = (
        (a * a + b * b + 2 * c * c)
        * (z0 * z0 + z1 * z1 + 2 * z2 * z2)
        - (z0 * a + z1 * b) ** 2
    )
    assert delta == active_wedge + q_t_p_z + p_t_q_z + q_t_q_z

    # Verify the coherent three-square completion at a rational lambda.
    lam1, lam2, lam3 = F(2), F(-3), F(5)
    left = (
        d * lam1 * lam1
        + middle * lam2 * lam2
        + d * lam3 * lam3
        - 2 * cross * lam1 * lam2
        - 2 * outer_cross * lam1 * lam3
        - 2 * cross * lam2 * lam3
    )
    right = (
        (d + outer_cross) * (lam1 - lam3) ** 2 / 2
        + middle
        * (lam2 - cross * (lam1 + lam3) / middle) ** 2
        + delta * (lam1 + lam3) ** 2 / middle
    )
    assert left == right

    print("three-cycle equality and sparse Cauchy factor: exact checks passed")


if __name__ == "__main__":
    main()
