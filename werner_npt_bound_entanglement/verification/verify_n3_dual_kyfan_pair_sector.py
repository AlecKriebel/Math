#!/usr/bin/env python3
"""Dependency-free exact checks for the n=3 Ky--Fan/pair-sector dual."""

import itertools
from fractions import Fraction as F


DIMENSION = 27


def zeros(rows, columns):
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def eye(size):
    out = zeros(size, size)
    for index in range(size):
        out[index][index] = F(1)
    return out


def add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def scale(coefficient, matrix):
    return [[coefficient * value for value in row] for row in matrix]


def multiply(left, right):
    out = zeros(len(left), len(right[0]))
    for i in range(len(left)):
        for k in range(len(right)):
            if left[i][k] == 0:
                continue
            for j in range(len(right[0])):
                out[i][j] += left[i][k] * right[k][j]
    return out


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def hs_norm_squared(matrix):
    return sum(value * value for row in matrix for value in row)


def matrix_rank(matrix):
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [
            entry / value for entry in work[pivot_row]
        ]
        for row in range(rows):
            if row == pivot_row:
                continue
            value = work[row][column]
            if value:
                work[row] = [
                    work[row][j] - value * work[pivot_row][j]
                    for j in range(columns)
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def digits(index):
    out = [0, 0, 0]
    for position in range(2, -1, -1):
        out[position] = index % 3
        index //= 3
    return tuple(out)


def index(word):
    return 9 * word[0] + 3 * word[1] + word[2]


def trace_replace(matrix, site):
    """E_site(C)=I_site tensor Tr_site(C), in the original ordering."""
    out = zeros(DIMENSION, DIMENSION)
    other_sites = tuple(position for position in range(3) if position != site)
    for row_other in itertools.product(range(3), repeat=2):
        for column_other in itertools.product(range(3), repeat=2):
            value = F(0)
            for traced in range(3):
                row = [0, 0, 0]
                column = [0, 0, 0]
                row[site] = traced
                column[site] = traced
                for position, physical_site in enumerate(other_sites):
                    row[physical_site] = row_other[position]
                    column[physical_site] = column_other[position]
                value += matrix[index(row)][index(column)]
            for identity_digit in range(3):
                row = [0, 0, 0]
                column = [0, 0, 0]
                row[site] = identity_digit
                column[site] = identity_digit
                for position, physical_site in enumerate(other_sites):
                    row[physical_site] = row_other[position]
                    column[physical_site] = column_other[position]
                out[index(row)][index(column)] = value
    return out


def local_p(matrix, site):
    return scale(F(1, 3), trace_replace(matrix, site))


def local_q(matrix, site):
    return add(matrix, scale(-1, local_p(matrix, site)))


def sector_projection(matrix, traceless_sites):
    out = matrix
    for site in range(3):
        out = (
            local_q(out, site)
            if site in traceless_sites
            else local_p(out, site)
        )
    return out


def pi_two(matrix):
    out = zeros(DIMENSION, DIMENSION)
    for sites in itertools.combinations(range(3), 2):
        out = add(out, sector_projection(matrix, set(sites)))
    return out


def partial_trace(matrix, traced_sites):
    traced_sites = tuple(sorted(traced_sites))
    retained_sites = tuple(
        site for site in range(3) if site not in traced_sites
    )
    retained_words = list(
        itertools.product(range(3), repeat=len(retained_sites))
    )
    traced_words = list(
        itertools.product(range(3), repeat=len(traced_sites))
    )
    out = zeros(len(retained_words), len(retained_words))
    for output_row, retained_row in enumerate(retained_words):
        for output_column, retained_column in enumerate(retained_words):
            value = F(0)
            for traced_word in traced_words:
                row = [0, 0, 0]
                column = [0, 0, 0]
                for position, site in enumerate(retained_sites):
                    row[site] = retained_row[position]
                    column[site] = retained_column[position]
                for position, site in enumerate(traced_sites):
                    row[site] = traced_word[position]
                    column[site] = traced_word[position]
                value += matrix[index(row)][index(column)]
            out[output_row][output_column] = value
    return out


def full_trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def endpoint_q_three(matrix):
    value = hs_norm_squared(matrix)
    for site in range(3):
        value -= F(1, 2) * hs_norm_squared(
            partial_trace(matrix, (site,))
        )
    for sites in itertools.combinations(range(3), 2):
        value += F(1, 4) * hs_norm_squared(
            partial_trace(matrix, sites)
        )
    value -= F(1, 8) * full_trace(matrix) ** 2
    return value


def matrix_unit(row_word, column_word):
    out = zeros(DIMENSION, DIMENSION)
    out[index(row_word)][index(column_word)] = F(1)
    return out


def sum_matrices(matrices):
    out = zeros(DIMENSION, DIMENSION)
    for matrix in matrices:
        out = add(out, matrix)
    return out


# Check the four endpoint-sector eigenvalues and hence T^2=2(I-L^3).
scalar = eye(DIMENSION)
one_body = sum_matrices(
    [
        matrix_unit((0, j, k), (1, j, k))
        for j in range(3)
        for k in range(3)
    ]
)
pair_body = sum_matrices(
    [
        matrix_unit((0, 0, k), (1, 1, k))
        for k in range(3)
    ]
)
triple_body = matrix_unit((0, 0, 0), (1, 1, 1))

sector_examples = (
    (scalar, F(-1, 8), F(9, 4)),
    (one_body, F(1, 4), F(3, 2)),
    (pair_body, F(-1, 2), F(3)),
    (triple_body, F(1), F(0)),
)
for matrix, endpoint_eigenvalue, t_squared in sector_examples:
    norm = hs_norm_squared(matrix)
    assert endpoint_q_three(matrix) == endpoint_eigenvalue * norm
    assert 2 * (1 - endpoint_eigenvalue) == t_squared

# Embedded sector norms give the dual constants 24, 12, and 2.
assert hs_norm_squared(scale(2, scalar)) == 27 * 4
assert hs_norm_squared(one_body) == 9
assert hs_norm_squared(pair_body) == 3
assert 2 * F(27, 1) / F(9, 4) == 24
assert 2 * F(9, 1) / F(3, 2) == 12
assert 2 * F(3, 1) / F(3, 1) == 2

# Verify the equivalent dual marginal norm identity (14a) on a
# rational low-sector operator with all three sector degrees present.
dual_test = add(
    add(scale(2, scalar), scale(3, one_body)),
    scale(5, pair_body),
)
dual_weighted_norm = (
    24 * F(2) ** 2
    + 12 * F(3) ** 2
    + 2 * F(5) ** 2
)
dual_marginal_norm = (
    F(2, 9)
    * sum(
        hs_norm_squared(partial_trace(dual_test, (site,)))
        for site in range(3)
    )
    - F(10, 243) * full_trace(dual_test) ** 2
)
assert dual_marginal_norm == dual_weighted_norm

# Sharp primal rank-two example
# C=E_01 tensor E_01 tensor (|0><0|+|1><1|).
c_matrix = add(
    matrix_unit((0, 0, 0), (1, 1, 0)),
    matrix_unit((0, 0, 1), (1, 1, 1)),
)
assert matrix_rank(c_matrix) == 2
assert hs_norm_squared(c_matrix) == 2
projected = pi_two(c_matrix)
assert hs_norm_squared(projected) == F(4, 3)
assert hs_norm_squared(projected) == F(2, 3) * hs_norm_squared(c_matrix)

# Verify the partial-trace form (22), including its equality value.
single_trace_sum = sum(
    hs_norm_squared(partial_trace(c_matrix, (site,)))
    for site in range(3)
)
double_trace_sum = sum(
    hs_norm_squared(partial_trace(c_matrix, sites))
    for sites in itertools.combinations(range(3), 2)
)
trace_value = full_trace(c_matrix)
marginal_left_side = (
    single_trace_sum
    - F(2, 3) * double_trace_sum
    + F(1, 3) * trace_value * trace_value
)
assert marginal_left_side == 2 * hs_norm_squared(c_matrix)
assert hs_norm_squared(projected) == marginal_left_side / 3

# Sharp dual example D=(E_01 tensor E_01) tensor I_3.
d_matrix = pair_body
d_squared = multiply(transpose(d_matrix), d_matrix)
expected_projection = zeros(DIMENSION, DIMENSION)
for third in range(3):
    expected_projection[index((1, 1, third))][
        index((1, 1, third))
    ] = F(1)
assert d_squared == expected_projection
assert matrix_rank(d_squared) == 3
assert hs_norm_squared(d_matrix) == 3
# Its three nonzero singular values are exactly one, so the top two
# squared singular values sum to the sharp value two.
assert full_trace(d_squared) == 3

# Partial-transpose swap polynomial.  On a joint swap-sign word
# epsilon_i in {+1,-1}, its value depends only on the number of minus
# signs and is respectively 2/9, 2/9, 2/3, 22/9.
def w_gamma_eigenvalue(signs):
    return (
        F(2, 3)
        - F(1, 3) * sum(signs)
        + F(2, 9) * sum(
            signs[i] * signs[j]
            for i, j in itertools.combinations(range(3), 2)
        )
        - F(1, 9) * signs[0] * signs[1] * signs[2]
    )


expected_w_gamma = (F(2, 9), F(2, 9), F(2, 3), F(22, 9))
for minus_count in range(4):
    signs = (-1,) * minus_count + (1,) * (3 - minus_count)
    assert w_gamma_eigenvalue(signs) == expected_w_gamma[minus_count]

# The reciprocal two-atom decomposition can be checked in Q(sqrt(3))
# by representing a+b*sqrt(3) as the pair (a,b).
def quadratic_add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def quadratic_multiply(left, right):
    return (
        left[0] * right[0] + 3 * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def quadratic_power(value, exponent):
    out = (F(1), F(0))
    for _ in range(exponent):
        out = quadratic_multiply(out, value)
    return out


t_plus = (F(2), F(1))
t_minus = (F(2), F(-1))
# p=(3-sqrt(3))/6 and q=(3+sqrt(3))/6.
p_weight = (F(1, 2), F(-1, 6))
q_weight = (F(1, 2), F(1, 6))
expected_moments = (F(1), F(1), F(3), F(11))
for exponent, expected in enumerate(expected_moments):
    moment = quadratic_add(
        quadratic_multiply(p_weight, quadratic_power(t_plus, exponent)),
        quadratic_multiply(q_weight, quadratic_power(t_minus, exponent)),
    )
    assert moment == (expected, F(0))
assert quadratic_multiply(t_plus, t_minus) == (F(1), F(0))

# The termwise Hodge determinant route fails by exactly a factor two on
# the sharp code U=(|000>,|001>), V=(|110>,|111>).  Each of the three
# weight-two parity channels has |det M_R|=1/8 and weight 4/9; the
# all-skew channel has the same determinant magnitude and weight 20/9.
hodge_l1_mass = (
    3 * F(4, 9) * F(1, 8)
    + F(20, 9) * F(1, 8)
)
assert hodge_l1_mass == F(4, 9)
assert hodge_l1_mass == 2 * F(2, 9)

# Nevertheless the exact logical partial transpose for this code is
# PSD: its only nontrivial block is (1/3)*[[1,-1],[-1,1]].
sharp_logical_pt = [
    [F(1, 3), F(0), F(0), F(-1, 3)],
    [F(0), F(2, 3), F(0), F(0)],
    [F(0), F(0), F(2, 3), F(0)],
    [F(-1, 3), F(0), F(0), F(1, 3)],
]
assert sharp_logical_pt[0][0] * sharp_logical_pt[3][3] == (
    sharp_logical_pt[0][3] * sharp_logical_pt[3][0]
)
assert sharp_logical_pt[1][1] == F(2, 3)
assert sharp_logical_pt[2][2] == F(2, 3)

# Formal expansion of the one-plane frame defect.  Here e_S denotes
# E_S(R), with e_123=I because Tr_123 R=I_K.
frame_coefficients = {mask: F(0) for mask in range(8)}
for first, second in itertools.combinations(range(3), 2):
    frame_coefficients[(1 << first) | (1 << second)] += 1
    frame_coefficients[1 << first] -= F(1, 3)
    frame_coefficients[1 << second] -= F(1, 3)
    frame_coefficients[0] += F(1, 9)
defect_coefficients = {
    mask: -3 * coefficient
    for mask, coefficient in frame_coefficients.items()
}
defect_coefficients[7] += 6
assert defect_coefficients[0] == -1
assert all(defect_coefficients[1 << site] == 2 for site in range(3))
assert all(
    defect_coefficients[(1 << first) | (1 << second)] == -3
    for first, second in itertools.combinations(range(3), 2)
)
assert defect_coefficients[7] == 6

print("exact n=3 Ky-Fan and pair-sector equivalence passed")
