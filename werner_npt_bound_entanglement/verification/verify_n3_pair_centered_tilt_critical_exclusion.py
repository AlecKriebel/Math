#!/usr/bin/env python3
"""Exact quotient-Euler exclusion of the opposite-tilt no-go path."""

from fractions import Fraction as F

from verify_n3_pair_centered_purity_nogo import (
    add,
    endpoint_operator,
    hs_inner,
    multiply,
    scale,
    sector_component,
    subtract,
    transpose,
    zero,
)
from verify_n3_pair_centered_7over3_tilt_nogo import (
    deficit,
    outer,
    tilted_matrix,
    u0,
    vector_add,
    x,
)


def pair_component(matrix):
    result = zero()
    for mask in range(8):
        if mask.bit_count() == 2:
            result = add(result, sector_component(matrix, mask))
    return result


def matrix_coefficient(left, matrix, right):
    total = F(0)
    for row_word, left_value in left.items():
        for col_word, right_value in right.items():
            # outer(left,right) supplies a convenient exact matrix unit.
            unit = outer({row_word: 1}, {col_word: 1})
            total += left_value * right_value * hs_inner(unit, matrix)
    return total


def euler_components(t):
    matrix = tilted_matrix(t)
    _, q, c, _ = deficit(t)
    pair = pair_component(matrix)
    numerator = subtract(
        scale(c, endpoint_operator(matrix)),
        scale(q, pair),
    )
    left0 = vector_add(u0, x, t)
    right0 = vector_add(u0, x, -t)
    left_component = matrix_coefficient(left0, numerator, x)
    right_component = matrix_coefficient(x, numerator, right0)
    return left_component, right_component


def interpolate(values):
    points = [F(integer) for integer in range(-4, 5)]
    augmented = [
        [point**degree for degree in range(9)] + [value]
        for point, value in zip(points, values)
    ]
    for column in range(9):
        pivot_row = next(
            row
            for row in range(column, 9)
            if augmented[row][column]
        )
        augmented[column], augmented[pivot_row] = (
            augmented[pivot_row], augmented[column]
        )
        pivot = augmented[column][column]
        augmented[column] = [
            value / pivot for value in augmented[column]
        ]
        for row in range(9):
            if row == column or augmented[row][column] == 0:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                augmented[row][index]
                - factor * augmented[column][index]
                for index in range(10)
            ]
    return [augmented[index][9] for index in range(9)]


left_coefficients = interpolate(
    [euler_components(F(integer))[0] for integer in range(-4, 5)]
)
right_coefficients = interpolate(
    [euler_components(F(integer))[1] for integer in range(-4, 5)]
)
assert left_coefficients == [
    0,
    F(-56, 81),
    0,
    F(-4, 81),
    0,
    F(2, 81),
    0,
    0,
    0,
]
assert right_coefficients == [-value for value in left_coefficients]

# Exact quotient Hessian at the flag--Bell zero.
c0 = tilted_matrix(F(0))
residual0 = endpoint_operator(c0)
d_left = scale(F(1, 3), outer(x, u0))
d_right = scale(F(1, 3), outer(u0, x))
normal_second = scale(F(-1, 3), outer(x, x))


def endpoint_pair(left, right):
    return hs_inner(left, endpoint_operator(right))


assert endpoint_pair(d_left, d_left) == F(2, 9)
assert endpoint_pair(d_right, d_right) == F(2, 9)
assert endpoint_pair(d_left, d_right) == 0
assert hs_inner(residual0, normal_second) == F(-1, 36)

tangent = subtract(d_left, d_right)
assert endpoint_pair(tangent, tangent) == F(4, 9)
quotient_hessian = (
    endpoint_pair(tangent, tangent)
    + 2 * hs_inner(residual0, normal_second)
)
assert quotient_hessian == F(7, 18) > 0

print("verified: opposite tilt is excluded by quotient criticality")
print("linear Euler coefficient:", left_coefficients[1])
print("quotient Hessian coefficient:", quotient_hessian)
