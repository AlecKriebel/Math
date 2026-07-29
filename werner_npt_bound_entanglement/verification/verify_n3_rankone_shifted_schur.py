#!/usr/bin/env python3
"""Dependency-free exact check of the shifted rank-one Schur reduction."""

from fractions import Fraction as F


def zeros(rows, columns):
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def eye(size):
    out = zeros(size, size)
    for index in range(size):
        out[index][index] = F(1)
    return out


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


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


def outer(left, right):
    return [
        [left[i] * right[j] for j in range(len(right))]
        for i in range(len(left))
    ]


def inverse(matrix):
    size = len(matrix)
    work = [
        matrix[row][:] + eye(size)[row]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next(
            row
            for row in range(column, size)
            if work[row][column] != 0
        )
        work[column], work[pivot] = work[pivot], work[column]
        value = work[column][column]
        work[column] = [entry / value for entry in work[column]]
        for row in range(size):
            if row == column:
                continue
            value = work[row][column]
            if value:
                work[row] = [
                    work[row][j] - value * work[column][j]
                    for j in range(2 * size)
                ]
    return [row[size:] for row in work]


def determinant_three(matrix):
    return (
        matrix[0][0]
        * (
            matrix[1][1] * matrix[2][2]
            - matrix[1][2] * matrix[2][1]
        )
        - matrix[0][1]
        * (
            matrix[1][0] * matrix[2][2]
            - matrix[1][2] * matrix[2][0]
        )
        + matrix[0][2]
        * (
            matrix[1][0] * matrix[2][1]
            - matrix[1][1] * matrix[2][0]
        )
    )


def positive_definite_ldl(matrix):
    """Exact unpivoted LDL test for a symmetric positive-definite matrix."""
    size = len(matrix)
    lower = zeros(size, size)
    diagonal = [F(0) for _ in range(size)]
    for i in range(size):
        lower[i][i] = F(1)
        diagonal[i] = matrix[i][i] - sum(
            lower[i][k] * lower[i][k] * diagonal[k]
            for k in range(i)
        )
        assert diagonal[i] > 0
        for j in range(i + 1, size):
            lower[j][i] = (
                matrix[j][i]
                - sum(
                    lower[j][k] * lower[i][k] * diagonal[k]
                    for k in range(i)
                )
            ) / diagonal[i]
    return True


def epsilon(i, j, k):
    if len({i, j, k}) < 3:
        return 0
    sequence = (i, j, k)
    inversions = sum(
        sequence[left] > sequence[right]
        for left in range(3)
        for right in range(left + 1, 3)
    )
    return -1 if inversions % 2 else 1


def matrix_index(row, column):
    return 3 * row + column


def cross_map(anchor):
    """Matrix of Y -> Y cross anchor in row-major vectorization."""
    out = zeros(9, 9)
    for output_row in range(3):
        for output_column in range(3):
            output = matrix_index(output_row, output_column)
            for input_row in range(3):
                for input_column in range(3):
                    source = matrix_index(input_row, input_column)
                    out[output][source] = sum(
                        F(
                            epsilon(output_row, input_row, anchor_row)
                            * epsilon(
                                output_column,
                                input_column,
                                anchor_column,
                            )
                        )
                        * anchor[anchor_row][anchor_column]
                        for anchor_row in range(3)
                        for anchor_column in range(3)
                    )
    return out


def flatten(matrix):
    return [entry for row in matrix for entry in row]


def block_matrix(top_left, top_right, bottom_left, bottom_right):
    top = [
        top_left[row] + top_right[row]
        for row in range(len(top_left))
    ]
    bottom = [
        bottom_left[row] + bottom_right[row]
        for row in range(len(bottom_left))
    ]
    return top + bottom


def physical_index(logical, left, right):
    return 9 * logical + 3 * left + right


def trace_replace(matrix, site):
    reduced = zeros(6, 6)
    if site == 1:
        for logical in range(2):
            for right in range(3):
                for other_logical in range(2):
                    for other_right in range(3):
                        reduced[3 * logical + right][
                            3 * other_logical + other_right
                        ] = sum(
                            matrix[
                                physical_index(logical, left, right)
                            ][
                                physical_index(
                                    other_logical,
                                    left,
                                    other_right,
                                )
                            ]
                            for left in range(3)
                        )
        out = zeros(18, 18)
        for left in range(3):
            for logical in range(2):
                for right in range(3):
                    for other_logical in range(2):
                        for other_right in range(3):
                            out[
                                physical_index(logical, left, right)
                            ][
                                physical_index(
                                    other_logical,
                                    left,
                                    other_right,
                                )
                            ] = reduced[3 * logical + right][
                                3 * other_logical + other_right
                            ]
        return out
    for logical in range(2):
        for left in range(3):
            for other_logical in range(2):
                for other_left in range(3):
                    reduced[3 * logical + left][
                        3 * other_logical + other_left
                    ] = sum(
                        matrix[
                            physical_index(logical, left, right)
                        ][
                            physical_index(
                                other_logical,
                                other_left,
                                right,
                            )
                        ]
                        for right in range(3)
                    )
    out = zeros(18, 18)
    for right in range(3):
        for logical in range(2):
            for left in range(3):
                for other_logical in range(2):
                    for other_left in range(3):
                        out[
                            physical_index(logical, left, right)
                        ][
                            physical_index(
                                other_logical,
                                other_left,
                                right,
                            )
                        ] = reduced[3 * logical + left][
                            3 * other_logical + other_left
                        ]
    return out


def endpoint(vector):
    projection = outer(vector, vector)
    first = add(scale(2, trace_replace(projection, 1)), scale(-1, projection))
    return add(scale(2, trace_replace(first, 2)), scale(-1, first))


def marginal(left, right, side):
    if side == "left":
        return add(
            multiply(left, transpose(left)),
            multiply(right, transpose(right)),
        )
    return add(
        multiply(transpose(left), left),
        multiply(transpose(right), right),
    )


def wedge_squared(first, second):
    return sum(
        (
            first[i] * second[j] - first[j] * second[i]
        )
        ** 2
        for i in range(3)
        for j in range(i + 1, 3)
    )


# A fully rational, genuinely transverse singular-pencil frame.
a = F(3, 5)
b = F(4, 5)
d_matrix = [
    [a, F(0), F(0)],
    [F(0), b, F(0)],
    [F(0), F(0), F(0)],
]
z_matrix = [
    [F(2, 5), F(1, 2), F(0)],
    [F(0), F(-3, 10), F(0)],
    [F(1, 2), F(0), F(1, 2)],
]
d_vector = flatten(d_matrix)
z_vector = flatten(z_matrix)
assert sum(value * value for value in d_vector) == 1
assert sum(value * value for value in z_vector) == 1
assert sum(
    d_vector[index] * z_vector[index]
    for index in range(9)
) == 0

rho_left = marginal(d_matrix, z_matrix, "left")
rho_right = marginal(d_matrix, z_matrix, "right")
det_left = determinant_three(rho_left)
det_right = determinant_three(rho_right)
assert det_left == F(1203, 5000)
assert det_right == F(587, 5000)
delta = det_left + det_right
assert delta == F(179, 500)

# Check the singular-gauge Cauchy--Binet formula.
rows = z_matrix
columns = transpose(z_matrix)
det_z = determinant_three(z_matrix)
det_left_cb = (
    a * a * b * b * sum(value * value for value in rows[2])
    + a * a * wedge_squared(rows[1], rows[2])
    + b * b * wedge_squared(rows[0], rows[2])
    + det_z * det_z
)
det_right_cb = (
    a * a * b * b * sum(value * value for value in columns[2])
    + a * a * wedge_squared(columns[1], columns[2])
    + b * b * wedge_squared(columns[0], columns[2])
    + det_z * det_z
)
assert det_left_cb == det_left
assert det_right_cb == det_right

c_d = cross_map(d_matrix)
c_z = cross_map(z_matrix)
a_operator = multiply(transpose(c_d), c_d)
b_operator = multiply(transpose(c_z), c_z)
k_operator = multiply(transpose(c_z), c_d)
h_vector = d_vector + z_vector

positive_part = block_matrix(
    add(eye(9), a_operator),
    k_operator,
    transpose(k_operator),
    add(eye(9), b_operator),
)
g_operator = add(
    positive_part,
    scale(F(-1, 2), outer(h_vector, h_vector)),
)

u_vector = d_vector + z_vector
m_operator = endpoint(u_vector)
assert m_operator == scale(2, g_operator)

# Strong coefficient-one shift: theta=delta/2.
theta = delta / 2
eta = 1 - theta
h_theta = add(
    add(scale(eta, eye(9)), a_operator),
    scale(F(-1, 2), outer(d_vector, d_vector)),
)
j_operator = add(
    k_operator,
    scale(F(-1, 2), outer(d_vector, z_vector)),
)
l_theta = add(
    add(scale(eta, eye(9)), b_operator),
    scale(F(-1, 2), outer(z_vector, z_vector)),
)
h_inverse = inverse(h_theta)
schur = add(
    l_theta,
    scale(
        -1,
        multiply(
            multiply(transpose(j_operator), h_inverse),
            j_operator,
        ),
    ),
)

shifted_g = add(g_operator, scale(-theta, eye(18)))
left_factor = block_matrix(
    eye(9),
    zeros(9, 9),
    multiply(transpose(j_operator), h_inverse),
    eye(9),
)
middle = block_matrix(
    h_theta,
    zeros(9, 9),
    zeros(9, 9),
    schur,
)
right_factor = block_matrix(
    eye(9),
    multiply(h_inverse, j_operator),
    zeros(9, 9),
    eye(9),
)
assert multiply(multiply(left_factor, middle), right_factor) == shifted_g

# Verify the explicit exceptional 2x2 inverse block in (23).
eta_block_determinant = (
    eta * eta + eta / 2 + 2 * a * a * b * b - F(1, 2)
)
predicted_diagonal_inverse = [
    [
        (eta + a * a - b * b / 2) / eta_block_determinant,
        -a * b / (2 * eta_block_determinant),
    ],
    [
        -a * b / (2 * eta_block_determinant),
        (eta + b * b - a * a / 2) / eta_block_determinant,
    ],
]
diagonal_indices = (matrix_index(0, 0), matrix_index(1, 1))
actual_diagonal_inverse = [
    [h_inverse[i][j] for j in diagonal_indices]
    for i in diagonal_indices
]
assert actual_diagonal_inverse == predicted_diagonal_inverse

# This rational instance satisfies the conjectural strong residual.
assert positive_definite_ldl(h_theta)
assert positive_definite_ldl(schur)
assert positive_definite_ldl(
    add(m_operator, scale(-delta, eye(18)))
)

print("exact rank-one shifted Schur reduction passed")
