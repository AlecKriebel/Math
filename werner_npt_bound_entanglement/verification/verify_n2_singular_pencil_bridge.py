#!/usr/bin/env python3
"""Dependency-free exact checks for the n=2 singular-pencil reduction.

This checks finite algebraic identities and the explicit rational equality
example.  It does not attempt to verify the conjectural uniform positivity
of the 9x9 residual.
"""

from fractions import Fraction as F


def zeros(m, n):
    return [[F(0) for _ in range(n)] for _ in range(m)]


def eye(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def sub(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def flatten(a):
    return [x for row in a for x in row]


def hs_inner(a, b):
    return sum(x * y for x, y in zip(flatten(a), flatten(b)))


def hs_norm2(a):
    return hs_inner(a, a)


def tr0(a):
    n = len(a)
    return sub(a, scale(trace(a) / n, eye(n)))


def matrix_unit(i, j, n=3):
    out = zeros(n, n)
    out[i][j] = F(1)
    return out


def s_matrix(x):
    """Matrix of S_X(Y)=((YX^T)_0,(X^TY)_0), real convention."""
    xt = transpose(x)
    out = zeros(18, 9)
    for col in range(9):
        y = matrix_unit(col // 3, col % 3)
        vals = flatten(tr0(matmul(y, xt))) + flatten(tr0(matmul(xt, y)))
        for row, value in enumerate(vals):
            out[row][col] = value
    return out


def determinant(a):
    a = [row[:] for row in a]
    n = len(a)
    ans = F(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j] != 0), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            ans = -ans
        p = a[j][j]
        ans *= p
        for i in range(j + 1, n):
            q = a[i][j] / p
            for k in range(j + 1, n):
                a[i][k] -= q * a[j][k]
    return ans


def inverse(a):
    n = len(a)
    aug = [a[i][:] + eye(n)[i] for i in range(n)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if aug[i][j] != 0)
        aug[j], aug[pivot] = aug[pivot], aug[j]
        p = aug[j][j]
        aug[j] = [x / p for x in aug[j]]
        for i in range(n):
            if i == j:
                continue
            q = aug[i][j]
            aug[i] = [x - q * y for x, y in zip(aug[i], aug[j])]
    return [row[n:] for row in aug]


def block(a, b, c, d):
    return [ar + br for ar, br in zip(a, b)] + [
        cr + dr for cr, dr in zip(c, d)
    ]


def cross(x, y):
    def eps(i, j, k):
        if len({i, j, k}) < 3:
            return F(0)
        return F(1) if (i, j, k) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else F(-1)

    out = zeros(3, 3)
    for i in range(3):
        for alpha in range(3):
            out[i][alpha] = sum(
                eps(i, j, k)
                * eps(alpha, beta, gamma)
                * x[j][beta]
                * y[k][gamma]
                for j in range(3)
                for k in range(3)
                for beta in range(3)
                for gamma in range(3)
            )
    return out


def main():
    a, b = F(3, 5), F(4, 5)
    d = [[a, F(0), F(0)], [F(0), b, F(0)], [F(0), F(0), F(0)]]
    z = [[b, F(0), F(0)], [F(0), -a, F(0)], [F(0), F(0), F(0)]]

    assert hs_norm2(d) == 1
    assert hs_norm2(z) == 1
    assert hs_inner(d, z) == 0

    sd, sz = s_matrix(d), s_matrix(z)
    gd = sub(scale(F(2), eye(9)), matmul(transpose(sd), sd))

    # Formula (18).
    expected = zeros(9, 9)
    diagonal = [
        F(2) - F(4, 3) * a * a,
        F(1),
        F(1) + b * b,
        F(1),
        F(2) - F(4, 3) * b * b,
        F(1) + a * a,
        F(1) + b * b,
        F(1) + a * a,
        F(2),
    ]
    for i, value in enumerate(diagonal):
        expected[i][i] = value
    expected[0][4] = expected[4][0] = F(2, 3) * a * b
    assert gd == expected

    det_formula = (
        F(8, 3)
        * (1 + a * a * b * b)
        * (1 + a * a) ** 2
        * (1 + b * b) ** 2
    )
    assert determinant(gd) == det_formula
    gd_inv = inverse(gd)
    assert matmul(gd, gd_inv) == eye(9)

    # Exact block Schur congruence for formula (21).
    c = scale(F(-1), matmul(transpose(sd), sz))
    h = sub(scale(F(2), eye(9)), matmul(transpose(sz), sz))
    full = block(gd, c, transpose(c), h)
    residual = sub(h, matmul(matmul(transpose(c), gd_inv), c))
    left = block(eye(9), zeros(9, 9), scale(F(-1), matmul(transpose(c), gd_inv)), eye(9))
    right = transpose(left)
    diagonalized = matmul(matmul(left, full), right)
    assert diagonalized == block(gd, zeros(9, 9), zeros(9, 9), residual)

    # Exact equality and the obstruction to a gap proportional to ||D x Z||^2.
    h0 = [[F(-1, 2), F(0), F(0)], [F(0), F(1, 2), F(0)], [F(0), F(0), F(0)]]
    ld = add(matmul(h0, d), matmul(d, h0))
    lz = add(matmul(h0, z), matmul(z, h0))
    assert 2 * (hs_norm2(h0) + hs_norm2(h0)) == 2
    assert hs_norm2(ld) + hs_norm2(lz) == 2
    dz = cross(d, z)
    assert dz == [[F(0), F(0), F(0)], [F(0), F(0), F(0)], [F(0), F(0), F(7, 25)]]
    assert hs_norm2(dz) == F(49, 625)

    # Both flattening volumes vanish on this common 2x2 support.
    rho_l = add(matmul(d, transpose(d)), matmul(z, transpose(z)))
    rho_r = add(matmul(transpose(d), d), matmul(transpose(z), z))
    assert rho_l == [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(0)]]
    assert rho_r == rho_l
    assert determinant(rho_l) == determinant(rho_r) == 0

    print("verified exact n=2 tangent/singular-pencil identities")
    print("verified exact 9x9 Schur reduction at a=3/5, b=4/5")
    print("verified equality with nonzero full mixed Hodge cross product")


if __name__ == "__main__":
    main()
