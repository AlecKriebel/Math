#!/usr/bin/env python3
"""Exact checks for the pair-sector qubit reduction bridge."""

from fractions import Fraction as F


def zeros(rows, columns):
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def multiply(left, right):
    out = zeros(len(left), len(right[0]))
    for row in range(len(left)):
        for middle in range(len(right)):
            for column in range(len(right[0])):
                out[row][column] += (
                    left[row][middle] * right[middle][column]
                )
    return out


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def outer(vector):
    return [
        [vector[row] * vector[column] for column in range(len(vector))]
        for row in range(len(vector))
    ]


def kronecker(left, right):
    out = zeros(
        len(left) * len(right),
        len(left[0]) * len(right[0]),
    )
    for i in range(len(left)):
        for j in range(len(left[0])):
            for k in range(len(right)):
                for ell in range(len(right[0])):
                    out[i * len(right) + k][j * len(right[0]) + ell] = (
                        left[i][j] * right[k][ell]
                    )
    return out


def add(left, right, right_coefficient=F(1)):
    return [
        [
            left[row][column]
            + right_coefficient * right[row][column]
            for column in range(len(left[0]))
        ]
        for row in range(len(left))
    ]


def partial_transpose_second(matrix):
    out = zeros(4, 4)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    out[2 * a + d][2 * c + b] = (
                        matrix[2 * a + b][2 * c + d]
                    )
    return out


identity_two = [[F(1), F(0)], [F(0), F(1)]]
epsilon = [[F(0), F(1)], [F(-1), F(0)]]

# A generic rational matrix checks every index placement in (1).
matrix = [[F(1), F(2)], [F(3), F(5)]]
vectorized = [matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]]
left_side = partial_transpose_second(outer(vectorized))

matrix_times_epsilon = multiply(matrix, epsilon)
spin_vectorized = [
    matrix_times_epsilon[0][0],
    matrix_times_epsilon[0][1],
    matrix_times_epsilon[1][0],
    matrix_times_epsilon[1][1],
]
right_side = add(
    kronecker(multiply(matrix, transpose(matrix)), identity_two),
    outer(spin_vectorized),
    F(-1),
)
assert left_side == right_side

# Exact sharp logical Gram (4).
sharp_gram = [
    [F(1, 3), F(0), F(0), F(0)],
    [F(0), F(2, 3), F(-1, 3), F(0)],
    [F(0), F(-1, 3), F(2, 3), F(0)],
    [F(0), F(0), F(0), F(1, 3)],
]
sharp_pt = partial_transpose_second(sharp_gram)
expected_pt = [
    [F(1, 3), F(0), F(0), F(-1, 3)],
    [F(0), F(2, 3), F(0), F(0)],
    [F(0), F(0), F(2, 3), F(0)],
    [F(-1, 3), F(0), F(0), F(1, 3)],
]
assert sharp_pt == expected_pt

# Eigenvectors exhibit spectra (5)--(7) without floating point.
standard_00 = [F(1), F(0), F(0), F(0)]
standard_11 = [F(0), F(0), F(0), F(1)]
middle_plus = [F(0), F(1), F(1), F(0)]
middle_minus = [F(0), F(1), F(-1), F(0)]
corner_plus = [F(1), F(0), F(0), F(1)]
corner_minus = [F(1), F(0), F(0), F(-1)]


def matrix_vector_product(matrix_value, vector):
    return [
        sum(matrix_value[row][column] * vector[column]
            for column in range(len(vector)))
        for row in range(len(matrix_value))
    ]


def assert_eigenvector(matrix_value, vector, eigenvalue):
    assert matrix_vector_product(matrix_value, vector) == [
        eigenvalue * entry for entry in vector
    ]


assert_eigenvector(sharp_gram, standard_00, F(1, 3))
assert_eigenvector(sharp_gram, standard_11, F(1, 3))
assert_eigenvector(sharp_gram, middle_plus, F(1, 3))
assert_eigenvector(sharp_gram, middle_minus, F(1))

feature_gram = add(
    sharp_gram,
    kronecker(identity_two, identity_two),
    F(-2, 9),
)
assert_eigenvector(feature_gram, standard_00, F(1, 9))
assert_eigenvector(feature_gram, standard_11, F(1, 9))
assert_eigenvector(feature_gram, middle_plus, F(1, 9))
assert_eigenvector(feature_gram, middle_minus, F(7, 9))

assert_eigenvector(sharp_pt, corner_plus, F(0))
assert_eigenvector(sharp_pt, corner_minus, F(2, 3))
assert_eigenvector(sharp_pt, [F(0), F(1), F(0), F(0)], F(2, 3))
assert_eigenvector(sharp_pt, [F(0), F(0), F(1), F(0)], F(2, 3))

print("exact pair-sector qubit reduction bridge passed")
