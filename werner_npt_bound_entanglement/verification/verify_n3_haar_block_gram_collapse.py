#!/usr/bin/env python3
"""Exact checker for the three-copy Haar block-Gram collapse.

No third-party packages are used.  The 81 linear block equations are
solved over Fraction, and the isotropic-space and canonical-slack
corollaries are checked independently.
"""

from fractions import Fraction as F


D = 3


def delta(a, b):
    return F(int(a == b))


def beta_index(a, b, c, d):
    return ((a * D + b) * D + c) * D + d


def equation_index(r, s, q, t):
    return ((r * D + s) * D + q) * D + t


number_unknowns = D**4
matrix = [[F(0) for _ in range(number_unknowns)] for _ in range(D**4)]
rhs = [F(0) for _ in range(D**4)]

# K_{rs,qt} = delta_{rq} sum_p beta_{sp,tp}
#              - (1/2) beta_{sr,tq}.
# Set gamma=1; homogeneity recovers arbitrary gamma.
for r in range(D):
    for s in range(D):
        for q in range(D):
            for t in range(D):
                row = equation_index(r, s, q, t)
                if r == q:
                    for p in range(D):
                        matrix[row][beta_index(s, p, t, p)] += F(1)
                matrix[row][beta_index(s, r, t, q)] -= F(1, 2)
                rhs[row] = (
                    delta(r, q) * delta(s, t)
                    - F(1, 2) * delta(r, s) * delta(q, t)
                )


def solve_square(a, b):
    """Gauss-Jordan solve over the rationals, asserting uniqueness."""

    n = len(a)
    augmented = [a[row][:] + [b[row]] for row in range(n)]
    pivot_row = 0
    for column in range(n):
        pivot = next(
            (row for row in range(pivot_row, n)
             if augmented[row][column] != 0),
            None,
        )
        assert pivot is not None, ("non-unique system", column)
        augmented[pivot_row], augmented[pivot] = (
            augmented[pivot],
            augmented[pivot_row],
        )
        scale = augmented[pivot_row][column]
        augmented[pivot_row] = [
            value / scale for value in augmented[pivot_row]
        ]
        for row in range(n):
            if row == pivot_row:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    augmented[row][j] - scale * augmented[pivot_row][j]
                    for j in range(n + 1)
                ]
        pivot_row += 1
    assert pivot_row == n
    return [augmented[row][-1] for row in range(n)]


solution = solve_square(matrix, rhs)
for a in range(D):
    for b in range(D):
        for c in range(D):
            for d in range(D):
                expected = delta(a, b) * delta(c, d)
                assert solution[beta_index(a, b, c, d)] == expected

# Independently reconstruct G and K from the solved tensor.
for s in range(D):
    for t in range(D):
        g = sum(
            solution[beta_index(s, p, t, p)] for p in range(D)
        )
        assert g == delta(s, t)

for r in range(D):
    for s in range(D):
        for q in range(D):
            for t in range(D):
                g = sum(
                    solution[beta_index(s, p, t, p)]
                    for p in range(D)
                )
                k = (
                    delta(r, q) * g
                    - F(1, 2)
                    * solution[beta_index(s, r, t, q)]
                )
                expected = (
                    delta(r, q) * delta(s, t)
                    - F(1, 2) * delta(r, s) * delta(q, t)
                )
                assert k == expected

# Pullback B_2(Phi(Z),Phi(W)) = conjugate(tr Z) tr W.
# Rational samples suffice here because the tensor identity was checked
# entrywise above.
z = [
    [F(1), F(2), F(-1)],
    [F(3), F(-4), F(5)],
    [F(0), F(7), F(3)],
]
w = [
    [F(-2), F(1), F(4)],
    [F(6), F(5), F(-3)],
    [F(2), F(0), F(1)],
]
pullback = F(0)
for a in range(D):
    for b in range(D):
        for c in range(D):
            for d in range(D):
                pullback += (
                    z[a][b]
                    * w[c][d]
                    * solution[beta_index(a, b, c, d)]
                )
trace_z = sum(z[a][a] for a in range(D))
trace_w = sum(w[a][a] for a in range(D))
assert pullback == trace_z * trace_w

# Every pair of traceless coefficient matrices has zero pullback.
traceless_basis = []
for a in range(D):
    for b in range(D):
        if a != b:
            element = [[F(0) for _ in range(D)] for _ in range(D)]
            element[a][b] = F(1)
            traceless_basis.append(element)
for a, b in ((0, 1), (1, 2)):
    element = [[F(0) for _ in range(D)] for _ in range(D)]
    element[a][a] = F(1)
    element[b][b] = F(-1)
    traceless_basis.append(element)
assert len(traceless_basis) == 8

for left in traceless_basis:
    for right in traceless_basis:
        value = F(0)
        for a in range(D):
            for b in range(D):
                for c in range(D):
                    for d in range(D):
                        value += (
                            left[a][b]
                            * right[c][d]
                            * solution[beta_index(a, b, c, d)]
                        )
        assert value == 0

# Z=W=I gives Q_2(Tr_i C)=9 gamma.
identity_pullback = sum(
    solution[beta_index(a, a, c, c)]
    for a in range(D)
    for c in range(D)
)
assert identity_pullback == 9

# Canonical endpoint-zero sector arithmetic:
# (4/3 + 2t/3)(1/3 + 2t/3)^2.
w0 = F(4, 27)
w1 = F(2, 3)
w2 = F(8, 9)
w3 = F(8, 27)
assert w0 + w1 + w2 + w3 == 2
haar_slack = F(1, 4) * w1 - w2 + 3 * w3
assert haar_slack == F(1, 6)

print("verified: unique 81-entry block-Gram collapse")
print("verified: 8-dimensional traceless coefficient space is isotropic")
print("verified: Q2(Tr_i C) = 9 gamma")
print("verified: canonical Q3-zero example has Haar slack 1/6")


# ---------------------------------------------------------------------------
# Fixed-left two-copy strictness: exact canonical checks
# ---------------------------------------------------------------------------


def matrix_unit(row, column):
    matrix_value = [[F(0) for _ in range(D)] for _ in range(D)]
    matrix_value[row][column] = F(1)
    return matrix_value


def matrix_add(*matrices):
    return [
        [
            sum(matrix_value[row][column] for matrix_value in matrices)
            for column in range(D)
        ]
        for row in range(D)
    ]


def matrix_scale(scalar, matrix_value):
    return [
        [scalar * matrix_value[row][column] for column in range(D)]
        for row in range(D)
    ]


def flatten(matrix_value):
    return [
        matrix_value[row][column]
        for row in range(D)
        for column in range(D)
    ]


def epsilon(i, j, k):
    if len({i, j, k}) < 3:
        return F(0)
    inversions = int(i > j) + int(i > k) + int(j > k)
    return F(-1 if inversions % 2 else 1)


def cross(left, right):
    output = [[F(0) for _ in range(D)] for _ in range(D)]
    for i in range(D):
        for alpha in range(D):
            value = F(0)
            for j in range(D):
                for k in range(D):
                    first_sign = epsilon(i, j, k)
                    if not first_sign:
                        continue
                    for beta in range(D):
                        for gamma in range(D):
                            second_sign = epsilon(alpha, beta, gamma)
                            if second_sign:
                                value += (
                                    first_sign
                                    * second_sign
                                    * left[j][beta]
                                    * right[k][gamma]
                                )
            output[i][alpha] = value
    return output


e11 = matrix_unit(0, 0)
e22 = matrix_unit(1, 1)
e33 = matrix_unit(2, 2)
a = F(3, 5)
b = F(4, 5)
d_matrix = matrix_add(matrix_scale(a, e11), matrix_scale(b, e22))
z_split = e33

assert cross(d_matrix, d_matrix) == matrix_scale(2 * a * b, e33)
cross_d_e33 = cross(d_matrix, e33)
assert cross_d_e33 == matrix_add(
    matrix_scale(b, e11),
    matrix_scale(a, e22),
)
assert cross(cross_d_e33, z_split) == d_matrix

# In the split branch, w=t E33 gives K w=tD, so the equality equations
# force y=-tD and C_D y=-2tab E33.  The final term is nonzero.
assert cross(matrix_scale(-1, d_matrix), d_matrix) == matrix_scale(
    -2 * a * b,
    e33,
)


def pair_index(first, second):
    return D * first + second


def partial_trace_two_copy(matrix_value, site):
    """Partial trace of a 9x9 coefficient matrix over one qutrit."""

    output = [[F(0) for _ in range(D)] for _ in range(D)]
    for row in range(D):
        for column in range(D):
            value = F(0)
            for traced in range(D):
                if site == 0:
                    source_row = pair_index(traced, row)
                    source_column = pair_index(traced, column)
                else:
                    source_row = pair_index(row, traced)
                    source_column = pair_index(column, traced)
                value += matrix_value[source_row][source_column]
            output[row][column] = value
    return output


def matrix_hs(left, right):
    return sum(
        left[row][column] * right[row][column]
        for row in range(len(left))
        for column in range(len(left[row]))
    )


def matrix_trace(matrix_value):
    return sum(
        matrix_value[index][index] for index in range(len(matrix_value))
    )


def b2_matrix(left, right):
    return (
        matrix_hs(left, right)
        - F(1, 2)
        * (
            matrix_hs(
                partial_trace_two_copy(left, 0),
                partial_trace_two_copy(right, 0),
            )
            + matrix_hs(
                partial_trace_two_copy(left, 1),
                partial_trace_two_copy(right, 1),
            )
        )
        + F(1, 4) * matrix_trace(left) * matrix_trace(right)
    )


def rank_rational(matrix_value):
    work = [row[:] for row in matrix_value]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == 0:
                continue
            scale = work[row][column]
            work[row] = [
                work[row][entry] - scale * work[pivot_row][entry]
                for entry in range(column_count)
            ]
        pivot_row += 1
    return pivot_row


def fixed_left_matrix(first_column, second_column):
    """Return the exact 18x18 Gram matrix W -> Q2(U W^T)."""

    columns = (flatten(first_column), flatten(second_column))
    rank_one_basis = []
    for code_column in range(2):
        for right_entry in range(D * D):
            coefficient = [
                [F(0) for _ in range(D * D)]
                for _ in range(D * D)
            ]
            for left_entry in range(D * D):
                coefficient[left_entry][right_entry] = (
                    columns[code_column][left_entry]
                )
            rank_one_basis.append(coefficient)
    return [
        [b2_matrix(left, right) for right in rank_one_basis]
        for left in rank_one_basis
    ]


z_core = matrix_add(matrix_scale(b, e11), matrix_scale(-a, e22))
e21 = matrix_unit(1, 0)

split_compression = fixed_left_matrix(d_matrix, z_split)
core_compression = fixed_left_matrix(d_matrix, z_core)
product_compression = fixed_left_matrix(e11, e21)

assert rank_rational(split_compression) == 18
assert rank_rational(core_compression) == 17
assert rank_rational(product_compression) == 15

print("verified: canonical split branch violates the final equality condition")
print("verified: split/core/product fixed-left nullities are 0/1/3")
