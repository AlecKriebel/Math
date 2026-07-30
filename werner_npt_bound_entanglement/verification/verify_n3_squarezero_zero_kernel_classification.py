#!/usr/bin/env python3
"""Dependency-free exact checks for the zero-kernel classification note."""

from fractions import Fraction as F


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b)))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def matadd(a, b):
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def scale(c, a):
    return [[c * value for value in row] for row in a]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def outer(x, y):
    return [[x_i * y_j for y_j in y] for x_i in x]


def partial_transpose_second(a):
    out = [[F(0) for _ in range(4)] for _ in range(4)]
    for first in range(2):
        for second in range(2):
            for third in range(2):
                for fourth in range(2):
                    row = 2 * first + second
                    col = 2 * third + fourth
                    source_row = 2 * first + fourth
                    source_col = 2 * third + second
                    out[row][col] = a[source_row][source_col]
    return out


def quadratic(a, x):
    return sum(
        x[i] * a[i][j] * x[j]
        for i in range(len(x))
        for j in range(len(x))
    )


def check_rational_obstruction():
    b = [F(4, 5), F(0), F(0), F(3, 5)]
    h = scale(F(25, 36), matadd(eye(4), scale(F(-1), outer(b, b))))
    assert quadratic(h, b) == 0

    h_gamma = partial_transpose_second(h)
    k = matadd(h_gamma, scale(F(-1, 4), eye(4)))
    expected = [
        [F(0), F(0), F(0), F(0)],
        [F(0), F(4, 9), F(-1, 3), F(0)],
        [F(0), F(-1, 3), F(4, 9), F(0)],
        [F(0), F(0), F(0), F(7, 36)],
    ]
    assert k == expected

    # The middle block has eigenvectors (1,1) and (1,-1).
    middle_plus = quadratic(
        [[k[1][1], k[1][2]], [k[2][1], k[2][2]]],
        [F(1), F(1)],
    ) / 2
    middle_minus = quadratic(
        [[k[1][1], k[1][2]], [k[2][1], k[2][2]]],
        [F(1), F(-1)],
    ) / 2
    assert (middle_plus, middle_minus) == (F(1, 9), F(7, 9))
    assert k[0][0] == 0
    assert k[3][3] == F(7, 36)

    # Exact sharp product-margin value:
    # alpha * (1 - largest Schmidt coefficient squared) = 1/4.
    assert F(25, 36) * (1 - F(16, 25)) == F(1, 4)

    # Takagi roots of this X-state are 7/9 and 1/9, so the
    # homogeneous concurrence is 2/3 > 1/2.
    assert F(7, 9) - F(1, 9) == F(2, 3)


def check_kernel_normal_form():
    # A rational positive definite 3 by 3 seed and r=2.
    r = F(2)
    a, b0, c = F(2), F(3), F(5)
    x, y, z = F(1, 3), F(-1, 4), F(1, 5)
    h = [
        [a, x, y, -r * a],
        [x, b0, z, -r * x],
        [y, z, c, -r * y],
        [-r * a, -r * x, -r * y, r * r * a],
    ]
    kernel = [r, F(0), F(0), F(1)]
    image = matmul(h, [[value] for value in kernel])
    assert all(row == [F(0)] for row in image)


def check_scalar_kernel_equations():
    # An abstract singular 2 by 2 principal block.
    h00 = F(9, 16)
    h11 = F(1, 4)
    cross = F(-3, 8)
    assert cross * cross == h00 * h11
    s, t = F(2), F(3)
    assert h00 * s + cross * t == 0
    assert cross * s + h11 * t == 0

    k00 = h00 - F(1, 4)
    k11 = h11 - F(1, 4)
    assert cross * cross == (F(1, 4) + k00) * (F(1, 4) + k11)


def determinant_2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def frobenius_squared(a):
    return sum(value * value for row in a for value in row)


def check_rank_one_scalar_remainder():
    # Equality case: X = lambda I + R, det R = 0, and both
    # eigenvalues lambda and mu lie on the same positive ray.
    lam = F(2)
    r = [[F(1), F(2)], [F(3), F(6)]]
    assert determinant_2(r) == 0
    x = matadd(scale(lam, eye(2)), r)
    mu = lam + r[0][0] + r[1][1]
    singular_gap_squared = (
        frobenius_squared(x) - 2 * abs(determinant_2(x))
    )
    assert determinant_2(x) == lam * mu
    assert singular_gap_squared == frobenius_squared(r)

    # Strict case: the two real eigenvalues point in opposite
    # directions.  The exact gap identity has positive remainder.
    lam = F(2)
    r = [[F(-5), F(0)], [F(0), F(0)]]
    x = matadd(scale(lam, eye(2)), r)
    mu = F(-3)
    singular_gap_squared = (
        frobenius_squared(x) - 2 * abs(determinant_2(x))
    )
    remainder = frobenius_squared(r) - singular_gap_squared
    assert remainder == 2 * (abs(lam) * abs(mu) - lam * mu)
    assert remainder == F(24)


def check_offdiagonal_shortcut_no_go():
    # Exact transverse spin-flip endpoint Gram.
    h = [
        [F(1, 4), F(0), F(0), F(-1, 4)],
        [F(0), F(3, 4), F(0), F(0)],
        [F(0), F(0), F(3, 4), F(0)],
        [F(-1, 4), F(0), F(0), F(1, 4)],
    ]
    kernel = [F(1), F(0), F(0), F(1)]
    assert all(
        row == [F(0)]
        for row in matmul(h, [[value] for value in kernel])
    )

    k = matadd(
        partial_transpose_second(h),
        scale(F(-1, 4), eye(4)),
    )
    expected = [
        [F(0), F(0), F(0), F(0)],
        [F(0), F(1, 2), F(-1, 4), F(0)],
        [F(0), F(-1, 4), F(1, 2), F(0)],
        [F(0), F(0), F(0), F(0)],
    ]
    assert k == expected

    diagonal_product = k[1][1] * k[2][2]
    true_rhs = (F(1, 4) + k[0][0]) * (F(1, 4) + k[3][3])
    crossed_coherence = k[1][2] * k[2][1]
    assert diagonal_product == F(1, 4)
    assert true_rhs == F(1, 16)
    assert diagonal_product == 4 * true_rhs
    assert crossed_coherence == true_rhs


def main():
    check_rational_obstruction()
    check_kernel_normal_form()
    check_scalar_kernel_equations()
    check_rank_one_scalar_remainder()
    check_offdiagonal_shortcut_no_go()
    print("verified exact square-zero zero-kernel classification identities")


if __name__ == "__main__":
    main()
