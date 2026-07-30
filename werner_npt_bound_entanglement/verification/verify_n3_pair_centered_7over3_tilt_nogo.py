#!/usr/bin/env python3
"""Exact rank-two obstruction to the coefficient-7/3 repair."""

from fractions import Fraction as F

from verify_n3_pair_centered_purity_nogo import (
    N_SITES,
    add,
    basis_index,
    hermitian_part,
    hs_inner,
    multiply,
    partial_trace_to_site,
    scale,
    sector_component,
    transpose,
    zero,
)


def outer(left, right):
    matrix = zero()
    for row, left_value in left.items():
        for column, right_value in right.items():
            matrix[basis_index(row)][basis_index(column)] += (
                left_value * right_value
            )
    return matrix


def vector(words):
    return {word: F(coefficient) for word, coefficient in words}


def vector_add(left, right, coefficient):
    result = dict(left)
    for word, value in right.items():
        result[word] = result.get(word, F(0)) + coefficient * value
        if result[word] == 0:
            del result[word]
    return result


u0 = vector(
    [((0, 0, 0), 1), ((1, 0, 1), 1), ((2, 0, 2), 1)]
)
u1 = vector(
    [((0, 1, 0), 1), ((1, 1, 1), 1), ((2, 1, 2), 1)]
)
x = vector([((0, 2, 1), 1)])


def tilted_matrix(t):
    left = vector_add(u0, x, t)
    right = vector_add(u0, x, -t)
    return scale(F(1, 3), add(outer(left, right), outer(u1, u1)))


def pair_data(matrix):
    sectors = [sector_component(matrix, mask) for mask in range(8)]
    pair = zero()
    for mask, component in enumerate(sectors):
        if mask.bit_count() == 2:
            pair = add(pair, component)
    c = hs_inner(pair, pair)
    endpoint = zero()
    eigenvalues = (F(-1, 8), F(1, 4), F(-1, 2), F(1))
    for mask, component in enumerate(sectors):
        endpoint = add(
            endpoint,
            scale(eigenvalues[mask.bit_count()], component),
        )
    q = hs_inner(matrix, endpoint)
    local_sum = F(0)
    for product_matrix in (
        multiply(matrix, transpose(pair)),
        multiply(transpose(pair), matrix),
    ):
        for site in range(N_SITES):
            marginal = hermitian_part(
                partial_trace_to_site(product_matrix, site)
            )
            local_sum += hs_inner(marginal, marginal)
    return q, c, local_sum


def deficit(t):
    q, c, local_sum = pair_data(tilted_matrix(t))
    value = local_sum - F(7, 3) * c * c + q * c / 2
    return value, q, c, local_sum


# The factorization in tilted_matrix has two columns on both sides, so
# every matrix in the path has rank at most two.
value, q, c, local_sum = deficit(F(1, 2))
assert q == F(113, 1152) > 0
assert c == F(401, 324)
assert local_sum == F(61463, 17496)
assert value == F(-10021, 20155392) < 0


def interpolate_degree_eight():
    points = [F(integer) for integer in range(-4, 5)]
    augmented = [
        [point**degree for degree in range(9)] + [deficit(point)[0]]
        for point in points
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
            entry / pivot for entry in augmented[column]
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


coefficients = interpolate_degree_eight()
assert coefficients == [
    0,
    0,
    F(-8, 2187),
    0,
    F(-118, 19683),
    0,
    F(952, 19683),
    0,
    F(731, 78732),
]

print("verified: coefficient-7/3 pair-centered repair is false")
print("second-order coefficient:", coefficients[2])
print("exact t=1/2 deficit:", value)
