#!/usr/bin/env python3
"""Exact checks for the logical Cayley/residual pair-sector identities.

This script uses only the Python standard library and Fraction arithmetic.
"""

from fractions import Fraction as F
from itertools import combinations


def zeros(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def add(a, b):
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def scale(s, a):
    return [[s * value for value in row] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    out = zeros(len(a), len(b[0]))
    for i in range(len(a)):
        for k in range(len(b)):
            if a[i][k]:
                for j in range(len(b[0])):
                    out[i][j] += a[i][k] * b[k][j]
    return out


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def inner(a, b):
    return sum(
        (a[i][j] * b[i][j] for i in range(len(a)) for j in range(len(a[0]))),
        F(0),
    )


def kron(a, b):
    out = zeros(len(a) * len(b), len(a[0]) * len(b[0]))
    for i in range(len(a)):
        for j in range(len(a[0])):
            for k in range(len(b)):
                for ell in range(len(b[0])):
                    out[i * len(b) + k][j * len(b[0]) + ell] = (
                        a[i][j] * b[k][ell]
                    )
    return out


def matrix_unit(row, col, n=3):
    out = zeros(n, n)
    out[row][col] = F(1)
    return out


def idx(word):
    value = 0
    for digit in word:
        value = 3 * value + digit
    return value


def word(value, length):
    out = [0] * length
    for pos in range(length - 1, -1, -1):
        out[pos] = value % 3
        value //= 3
    return tuple(out)


def embed_pair(b, spectator):
    out = zeros(27, 27)
    active = [site for site in range(3) if site != spectator]
    for row in range(27):
        rw = word(row, 3)
        for col in range(27):
            cw = word(col, 3)
            if rw[spectator] != cw[spectator]:
                continue
            rr = 3 * rw[active[0]] + rw[active[1]]
            cc = 3 * cw[active[0]] + cw[active[1]]
            out[row][col] = b[rr][cc]
    return out


def partial_trace_pair(b, site):
    out = zeros(3, 3)
    for row in range(3):
        for col in range(3):
            for contracted in range(3):
                if site == 0:
                    rr = 3 * contracted + row
                    cc = 3 * contracted + col
                else:
                    rr = 3 * row + contracted
                    cc = 3 * col + contracted
                out[row][col] += b[rr][cc]
    return out


def determinant3(a):
    return (
        a[0][0] * a[1][1] * a[2][2]
        + a[0][1] * a[1][2] * a[2][0]
        + a[0][2] * a[1][0] * a[2][1]
        - a[0][2] * a[1][1] * a[2][0]
        - a[0][1] * a[1][0] * a[2][2]
        - a[0][0] * a[1][2] * a[2][1]
    )


def principal_minor(a, indices):
    if len(indices) == 1:
        return a[indices[0]][indices[0]]
    if len(indices) == 2:
        i, j = indices
        return a[i][i] * a[j][j] - a[i][j] * a[j][i]
    return determinant3(a)


def assert_psd_3(a):
    for size in (1, 2, 3):
        for indices in combinations(range(3), size):
            assert principal_minor(a, indices) >= 0


def main():
    z = zeros(3, 3)
    z[0][0], z[1][1] = F(1), F(-1)
    e = matrix_unit(1, 0)
    t = matrix_unit(1, 2)

    # Each coefficient is doubly traceless.  The T tensor T term is an
    # inactive norm reserve on the chosen code.
    common = add(scale(F(2, 3), kron(z, e)), scale(F(1, 3), kron(t, t)))
    coefficients = [common, common, kron(t, t)]
    for b in coefficients:
        assert partial_trace_pair(b, 0) == zeros(3, 3)
        assert partial_trace_pair(b, 1) == zeros(3, 3)

    bnorm = [inner(b, b) for b in coefficients]
    assert bnorm == [F(1), F(1), F(1)]

    v = zeros(27, 2)
    v[idx((0, 0, 0))][0] = F(1)
    v[idx((1, 1, 0))][1] = F(1)
    assert matmul(transpose(v), v) == eye(2)

    operators = [embed_pair(coefficients[i], i) for i in range(3)]
    x = [matmul(operator, v) for operator in operators]
    assert x[0] == x[1]
    assert x[2] == zeros(27, 2)

    a = [
        [matmul(transpose(x[i]), x[j]) for j in range(3)]
        for i in range(3)
    ]
    half_active = scale(F(4, 9), eye(2))
    assert a[0][0] == half_active
    assert a[0][1] == half_active
    assert a[1][1] == half_active

    logical_residual = [
        add(scale(bnorm[i], eye(2)), scale(F(-1), a[i][i]))
        for i in range(3)
    ]
    assert logical_residual == [
        scale(F(5, 9), eye(2)),
        scale(F(5, 9), eye(2)),
        eye(2),
    ]

    c = [[trace(a[i][j]) for j in range(3)] for i in range(3)]
    d = [trace(logical_residual[i]) for i in range(3)]
    assert d == [F(10, 9), F(10, 9), F(2)]
    assert c[0][1] == F(8, 9)
    assert c[0][2] == c[1][2] == F(0)

    m = zeros(3, 3)
    for i in range(3):
        m[i][i] = d[i]
        for j in range(3):
            if i != j:
                m[i][j] = -c[i][j]
    assert_psd_3(m)
    assert determinant3(m) == F(8, 9)

    # The physical residuals R_i=b_i I-X_i X_i^T are diagonal and PSD.
    physical_residual = [
        add(scale(bnorm[i], eye(27)), scale(F(-1), matmul(x[i], transpose(x[i]))))
        for i in range(3)
    ]
    for residual in physical_residual:
        for i in range(27):
            for j in range(27):
                if i != j:
                    assert residual[i][j] == 0
            assert residual[i][i] >= 0

    # For each residual label i, g^(i) is a genuine scalar Gram matrix.
    g = []
    for i in range(3):
        gi = zeros(3, 3)
        for j in range(3):
            for k in range(3):
                gi[j][k] = trace(
                    matmul(
                        transpose(x[j]),
                        matmul(physical_residual[i], x[k]),
                    )
                )
                rhs = bnorm[i] * c[j][k] - trace(
                    matmul(a[j][i], a[i][k])
                )
                assert gi[j][k] == rhs
        assert_psd_3(gi)
        g.append(gi)

    # The Cayley pair terms need not be positive.
    delta = [[F(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            delta[i][j] = trace(
                matmul(logical_residual[i], logical_residual[j])
            ) - c[i][j] * c[j][i]
    assert delta[0][1] == F(-14, 81)
    assert delta[0][2] == delta[1][2] == F(10, 9)

    # Nevertheless the true two-component minor is positive because of
    # the logical spin-flip complement.
    spin_e2 = add(scale(trace(logical_residual[1]), eye(2)),
                  scale(F(-1), logical_residual[1]))
    pair_minor = d[0] * d[1] - c[0][1] * c[1][0]
    assert pair_minor == F(4, 9)
    assert pair_minor == delta[0][1] + trace(
        matmul(logical_residual[0], spin_e2)
    )

    # Exact Cayley-on-E determinant identity.
    pair_sum = (
        d[2] * delta[0][1]
        + d[1] * delta[0][2]
        + d[0] * delta[1][2]
    )
    cubic_e = trace(
        matmul(
            matmul(logical_residual[0], logical_residual[1]),
            logical_residual[2],
        )
    )
    cycle = c[0][1] * c[1][2] * c[2][0]
    assert pair_sum == F(172, 81)
    assert cubic_e == F(50, 81)
    assert determinant3(m) == pair_sum - 2 * (cubic_e + cycle)

    # Exact Cayley/residual expansion of the scalar logical cycle.
    t_plus = trace(matmul(matmul(a[0][1], a[1][2]), a[2][0]))
    t_cross = trace(matmul(matmul(a[0][1], a[2][0]), a[1][2]))
    residual_cycle_rhs = (
        bnorm[1] * c[0][2] * c[2][0]
        + bnorm[0] * c[1][2] * c[2][1]
        + bnorm[2] * c[0][1] * c[1][0]
        - g[1][0][2] * c[2][0]
        - g[0][2][1] * c[1][2]
        - g[2][1][0] * c[0][1]
        - t_plus
        - t_cross
    )
    assert cycle == residual_cycle_rhs == F(0)

    print("exact Cayley/residual identities verified")
    print("Delta_12 =", delta[0][1])
    print("det M =", determinant3(m))


if __name__ == "__main__":
    main()
