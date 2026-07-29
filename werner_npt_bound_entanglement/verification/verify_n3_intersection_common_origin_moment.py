#!/usr/bin/env python3
"""Exact checks for the n=3 common-origin moment note.

Only fractions and deterministic finite-dimensional contractions are
used.  No floating-point arithmetic or external package is needed.
"""

from fractions import Fraction as F
from itertools import combinations, product


def zeros(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def sub(a, b):
    return [
        [a[i][j] - b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def scale(c, a):
    return [[c * value for value in row] for row in a]


def matmul(a, b):
    bt = transpose(b)
    return [
        [sum(x * y for x, y in zip(row, col)) for col in bt]
        for row in a
    ]


def kron(a, b):
    out = zeros(len(a) * len(b), len(a[0]) * len(b[0]))
    for i, j, k, ell in product(
        range(len(a)),
        range(len(a[0])),
        range(len(b)),
        range(len(b[0])),
    ):
        out[i * len(b) + k][j * len(b[0]) + ell] = a[i][j] * b[k][ell]
    return out


def determinant(a):
    a = [row[:] for row in a]
    n = len(a)
    sign = F(1)
    value = F(1)
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            a[pivot], a[col] = a[col], a[pivot]
            sign = -sign
        p = a[col][col]
        value *= p
        for row in range(col + 1, n):
            coefficient = a[row][col] / p
            for j in range(col + 1, n):
                a[row][j] -= coefficient * a[col][j]
    return sign * value


def all_principal_minors_nonnegative(a):
    n = len(a)
    for size in range(1, n + 1):
        for indices in combinations(range(n), size):
            block = [[a[i][j] for j in indices] for i in indices]
            assert determinant(block) >= 0


def swap(d):
    out = zeros(d * d, d * d)
    for i, j in product(range(d), repeat=2):
        out[d * j + i][d * i + j] = F(1)
    return out


def rational_frame(output, environment, rotation):
    """First three columns after one exact rational Givens rotation."""
    matrix = eye(output * environment)
    i, j, cosine_num, sine_num, denominator = rotation
    c = F(cosine_num, denominator)
    s = F(sine_num, denominator)
    old_i = matrix[i][:]
    old_j = matrix[j][:]
    matrix[i] = [c * x - s * y for x, y in zip(old_i, old_j)]
    matrix[j] = [s * x + c * y for x, y in zip(old_i, old_j)]
    return [row[:3] for row in matrix]


def rational_frame_many(output, environment, rotations):
    matrix = eye(output * environment)
    for i, j, cosine_num, sine_num, denominator in rotations:
        c = F(cosine_num, denominator)
        s = F(sine_num, denominator)
        old_i = matrix[i][:]
        old_j = matrix[j][:]
        matrix[i] = [c * x - s * y for x, y in zip(old_i, old_j)]
        matrix[j] = [s * x + c * y for x, y in zip(old_i, old_j)]
    return [row[:3] for row in matrix]


def compressed_one_cut_swap(frame, output, environment):
    """(V^T tensor V^T)(F_output tensor I)(V tensor V)."""
    # Reshape each logical column as an output-by-environment matrix.
    tensors = []
    for logical in range(3):
        tensors.append(
            [
                [
                    frame[environment * row + env][logical]
                    for env in range(environment)
                ]
                for row in range(output)
            ]
        )

    # rho[c,a] = Tr_environment |V c><V a|.
    rho = [[None for _ in range(3)] for _ in range(3)]
    for c, a in product(range(3), repeat=2):
        block = zeros(output, output)
        for r, s, env in product(
            range(output), range(output), range(environment)
        ):
            block[r][s] += tensors[c][r][env] * tensors[a][s][env]
        rho[c][a] = block

    out = zeros(9, 9)
    for a, b, c, d in product(range(3), repeat=4):
        value = F(0)
        product_matrix = matmul(rho[c][a], rho[d][b])
        for r in range(output):
            value += product_matrix[r][r]
        out[3 * a + b][3 * c + d] = value
    return out


def parity_bounds(k, logical_swap):
    identity = eye(9)
    p_plus = scale(F(1, 2), add(identity, logical_swap))
    p_minus = scale(F(1, 2), sub(identity, logical_swap))
    lower = add(scale(F(1, 8), p_plus), scale(F(3, 8), p_minus))
    upper = add(scale(F(9, 8), p_plus), scale(F(27, 8), p_minus))
    all_principal_minors_nonnegative(sub(k, lower))
    all_principal_minors_nonnegative(sub(upper, k))


def hand_model():
    k = zeros(9, 9)
    entries = [
        (0, 0, F(1, 4)),
        (1, 1, F(5, 8)),
        (1, 2, F(1, 8)),
        (1, 6, F(3, 8)),
        (2, 1, F(1, 8)),
        (2, 2, F(5, 8)),
        (2, 3, F(3, 8)),
        (3, 2, F(3, 8)),
        (3, 3, F(5, 8)),
        (3, 6, F(1, 8)),
        (4, 4, F(3, 5)),
        (4, 8, F(1, 5)),
        (5, 5, F(2, 5)),
        (6, 1, F(3, 8)),
        (6, 3, F(1, 8)),
        (6, 6, F(5, 8)),
        (7, 7, F(2, 5)),
        (8, 4, F(1, 5)),
        (8, 8, F(3, 5)),
    ]
    for i, j, value in entries:
        k[i][j] = value
    return k


def main():
    logical_swap = swap(3)

    # Section 3: a common commuting-dilation/leakage model with a
    # negative crossed partial-transpose minor.
    k0 = hand_model()
    assert matmul(k0, logical_swap) == matmul(logical_swap, k0)
    parity_bounds(k0, logical_swap)
    a0, b0, z0 = k0[0][0], k0[5][5], k0[2][3]
    assert (a0, b0, z0) == (F(1, 4), F(2, 5), F(3, 8))
    assert a0 * b0 - z0 * z0 == F(-13, 320)

    # The explicit equal first moment from the POVM construction.
    identity = eye(9)
    p_plus = scale(F(1, 2), add(identity, logical_swap))
    p_minus = scale(F(1, 2), sub(identity, logical_swap))
    k_plus = matmul(k0, p_plus)
    k_minus = matmul(k0, p_minus)
    r0 = add(
        sub(scale(F(7, 6), p_plus), scale(F(4, 3), k_plus)),
        sub(scale(F(1, 2), p_minus), scale(F(4, 9), k_minus)),
    )
    r_sum = scale(F(3), r0)
    recovered = add(
        sub(identity, scale(F(1, 8), logical_swap)),
        add(scale(F(-1, 2), r_sum), scale(F(1, 4), matmul(r_sum, logical_swap))),
    )
    assert recovered == k0

    # Equal R_i reduce the 27-by-27 leakage Gram to two 9-by-9
    # blocks: diagonal-off_diagonal (multiplicity two) and
    # diagonal+2*off_diagonal (multiplicity one).
    diagonal = sub(identity, matmul(r0, r0))
    off_diagonal = sub(matmul(r0, logical_swap), matmul(r0, r0))
    all_principal_minors_nonnegative(sub(diagonal, off_diagonal))
    all_principal_minors_nonnegative(
        add(diagonal, scale(F(2), off_diagonal))
    )

    # Section 4: each R_i separately has a genuine one-cut isometric
    # origin in C^2 tensor C^2.
    specifications = [
        (2, 2, (0, 3, 5, -12, 13)),
        (2, 2, (2, 1, 3, 4, 5)),
        (2, 2, (3, 1, 5, -12, 13)),
    ]
    moments = []
    for output, environment, rotation in specifications:
        frame = rational_frame(output, environment, rotation)
        assert matmul(transpose(frame), frame) == eye(3)
        moment = compressed_one_cut_swap(frame, output, environment)
        assert transpose(moment) == moment
        assert matmul(moment, logical_swap) == matmul(logical_swap, moment)
        moments.append(moment)

    r_sum = zeros(9, 9)
    for moment in moments:
        r_sum = add(r_sum, moment)
    k1 = add(
        sub(identity, scale(F(1, 8), logical_swap)),
        add(scale(F(-1, 2), r_sum), scale(F(1, 4), matmul(r_sum, logical_swap))),
    )
    assert matmul(k1, logical_swap) == matmul(logical_swap, k1)
    parity_bounds(k1, logical_swap)

    a1, b1, z1 = k1[0][0], k1[5][5], k1[2][3]
    assert a1 == F(42961, 228488)
    assert b1 == F(48457, 105625)
    assert z1 == F(9, 25)
    assert a1 * b1 - z1 * z1 == F(-209202211, 4826809000)

    # Build the simultaneous leakage matrix proposed by a common W.
    leakage1 = zeros(27, 27)
    for i, j in product(range(3), repeat=2):
        if i == j:
            block = sub(identity, matmul(moments[i], moments[i]))
        else:
            k = 3 - i - j
            block = sub(
                matmul(moments[k], logical_swap),
                matmul(moments[i], moments[j]),
            )
        for row, col in product(range(9), repeat=2):
            leakage1[9 * i + row][9 * j + col] = block[row][col]

    first = 9 + 1
    second = 18 + 1
    separator = [
        [leakage1[first][first], leakage1[first][second]],
        [leakage1[second][first], leakage1[second][second]],
    ]
    assert separator == [
        [F(0), F(135, 169)],
        [F(135, 169), F(144, 169)],
    ]
    assert determinant(separator) == F(-18225, 28561)

    # Section 5: one identical genuine channel moment satisfies the
    # leakage Gram condition as well, but the crossed minor remains
    # negative.  What is absent is a common rank-one tripartite
    # Stinespring tensor.
    frame = rational_frame_many(
        3,
        2,
        [
            (4, 0, 5, -12, 13),
            (2, 1, 20, 21, 29),
            (5, 0, 3, 4, 5),
        ],
    )
    assert frame == [
        [F(3, 13), F(0), F(0)],
        [F(0), F(20, 29), F(21, 29)],
        [F(0), F(-21, 29), F(20, 29)],
        [F(0), F(0), F(0)],
        [F(12, 13), F(0), F(0)],
        [F(-4, 13), F(0), F(0)],
    ]
    assert matmul(transpose(frame), frame) == eye(3)
    repeated = compressed_one_cut_swap(frame, 3, 2)
    repeated_sum = scale(F(3), repeated)
    k2 = add(
        sub(identity, scale(F(1, 8), logical_swap)),
        add(
            scale(F(-1, 2), repeated_sum),
            scale(F(1, 4), matmul(repeated_sum, logical_swap)),
        ),
    )
    parity_bounds(k2, logical_swap)
    a2, b2, z2 = k2[0][0], k2[5][5], k2[2][3]
    assert a2 == F(30289, 228488)
    assert b2 == F(442681, 707281)
    assert z2 == F(89145, 142129)
    assert a2 * b2 - z2 * z2 == F(-50166283391, 161605221128)

    diagonal2 = sub(identity, matmul(repeated, repeated))
    off_diagonal2 = sub(
        matmul(repeated, logical_swap),
        matmul(repeated, repeated),
    )
    all_principal_minors_nonnegative(sub(diagonal2, off_diagonal2))
    all_principal_minors_nonnegative(
        add(diagonal2, scale(F(2), off_diagonal2))
    )

    # Common-Stinespring separator.  In the rotated logical vector
    # y=(20 e1+21 e2)/29, the channel output is a product vector.
    y = [[F(0)], [F(20, 29)], [F(21, 29)]]
    vy = matmul(frame, y)
    assert vy == [[F(0)], [F(1)], [F(0)], [F(0)], [F(0)], [F(0)]]

    # V z, z=e0, as an output-by-environment matrix.
    vz = [frame[row][0] for row in range(6)]
    assert vz == [F(3, 13), F(0), F(0), F(0), F(12, 13), F(-4, 13)]
    # Overlap of rho_z with rho_y=|0><0| is the squared norm of
    # output-row zero.  The transition norm uses environment-column one.
    marginal_overlap = vz[0] * vz[0] + vz[1] * vz[1]
    transition_norm = vz[1] * vz[1] + vz[3] * vz[3] + vz[5] * vz[5]
    assert marginal_overlap == F(9, 169)
    assert transition_norm == F(16, 169)
    assert 2 * 3 * transition_norm > 3 * marginal_overlap

    print(
        "verified: common leakage, separate one-cut origins, and their "
        "first-moment conjunction admit exact negative crossed minors; "
        "joint leakage separator = -18225/28561"
    )


if __name__ == "__main__":
    main()
