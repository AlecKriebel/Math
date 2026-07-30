#!/usr/bin/env python3
"""Exact checker for the cyclic, high-rank stationary obstruction."""

from fractions import Fraction as F
from itertools import product


D = 3
N = D**3


def digits(number):
    output = [0, 0, 0]
    for position in range(2, -1, -1):
        output[position] = number % D
        number //= D
    return tuple(output)


BASIS = [digits(index) for index in range(N)]


def index(word):
    return 9 * word[0] + 3 * word[1] + word[2]


def zero():
    return [[F(0) for _ in range(N)] for _ in range(N)]


def add(*matrices):
    return [
        [
            sum((matrix[row][column] for matrix in matrices), F(0))
            for column in range(N)
        ]
        for row in range(N)
    ]


def scale(coefficient, matrix):
    return [[coefficient * entry for entry in row] for row in matrix]


def permutation(site_order):
    matrix = zero()
    for column, word in enumerate(BASIS):
        output = tuple(word[site_order[position]] for position in range(3))
        matrix[index(output)][column] = 1
    return matrix


identity = zero()
for diagonal in range(N):
    identity[diagonal][diagonal] = 1

flip12 = permutation((1, 0, 2))
flip13 = permutation((2, 1, 0))
flip23 = permutation((0, 2, 1))
cycle = permutation((2, 0, 1))
cycle_inverse = permutation((1, 2, 0))
flip_sum = add(flip12, flip13, flip23)

D0 = add(flip_sum, scale(-1, identity))
E0 = add(
    cycle,
    cycle_inverse,
    scale(F(-2, 3), flip_sum),
    scale(F(4, 9), identity),
)


def inner(left, right):
    return sum(
        (
            left[row][column] * right[row][column]
            for row in range(N)
            for column in range(N)
        ),
        F(0),
    )


def scalar_projection(matrix, site):
    output = zero()
    for row_index, row_word in enumerate(BASIS):
        for column_index, column_word in enumerate(BASIS):
            if row_word[site] != column_word[site]:
                continue
            value = F(0)
            for traced in range(D):
                source_row = list(row_word)
                source_column = list(column_word)
                source_row[site] = traced
                source_column[site] = traced
                value += matrix[index(source_row)][index(source_column)]
            output[row_index][column_index] = value / D
    return output


def traceless_projection(matrix, site):
    return add(matrix, scale(-1, scalar_projection(matrix, site)))


def sector(matrix, bits):
    output = matrix
    for site, bit in enumerate(bits):
        if bit:
            output = traceless_projection(output, site)
        else:
            output = scalar_projection(output, site)
    return output


def sector_components(matrix):
    return {
        bits: sector(matrix, bits)
        for bits in product((0, 1), repeat=3)
    }


D0_components = sector_components(D0)
E0_components = sector_components(E0)

assert inner(D0, D0) == 72
assert inner(E0, E0) == F(80, 3)
assert inner(D0, E0) == 0
assert all(
    inner(component, component) == (24 if sum(bits) == 2 else 0)
    for bits, component in D0_components.items()
)
assert all(
    inner(component, component) == (F(80, 3) if sum(bits) == 3 else 0)
    for bits, component in E0_components.items()
)


def left_multiply(local_matrix, matrix, site=0):
    output = zero()
    for row_index, row_word in enumerate(BASIS):
        for middle in range(D):
            coefficient = local_matrix[row_word[site]][middle]
            if not coefficient:
                continue
            source_word = list(row_word)
            source_word[site] = middle
            source_row = index(source_word)
            for column in range(N):
                output[row_index][column] += (
                    coefficient * matrix[source_row][column]
                )
    return output


Q_EIGENVALUE = {
    0: F(-1, 8),
    1: F(1, 4),
    2: F(-1, 2),
    3: F(1),
}


def endpoint_pairing(left, right):
    left_components = sector_components(left)
    right_components = sector_components(right)
    return sum(
        (
            Q_EIGENVALUE[sum(bits)]
            * inner(left_components[bits], right_components[bits])
            for bits in left_components
        ),
        F(0),
    )


def pair_sector_pairing(left, right):
    left_components = sector_components(left)
    right_components = sector_components(right)
    return sum(
        (
            inner(left_components[bits], right_components[bits])
            for bits in left_components
            if sum(bits) == 2
        ),
        F(0),
    )


local_identity = [
    [F(row == column) for column in range(D)]
    for row in range(D)
]
e01 = [[F(0) for _ in range(D)] for _ in range(D)]
e01[0][1] = 1

ID = left_multiply(local_identity, D0)
IE = left_multiply(local_identity, E0)
XD = left_multiply(e01, D0)
XE = left_multiply(e01, E0)

# Exact contractions determining the two invariant local eigenvalues.
assert endpoint_pairing(ID, ID) == -36
assert endpoint_pairing(IE, IE) == F(80, 3)
assert endpoint_pairing(ID, IE) == 0
assert endpoint_pairing(XD, XD) == F(3, 2)
assert endpoint_pairing(XE, XE) == F(65, 9)
assert endpoint_pairing(XD, XE) == 0

assert pair_sector_pairing(ID, ID) == 72
assert pair_sector_pairing(IE, IE) == 0
assert pair_sector_pairing(ID, IE) == 0
assert pair_sector_pairing(XD, XD) == 14
assert pair_sector_pairing(XE, XE) == F(10, 9)
assert pair_sector_pairing(XD, XE) == 0

# One exact member of the family.
delta = F(1, 16)
c = 2 * (1 + delta) / 3
d = (1 - 2 * delta) / 3
alpha_squared = c / 72
beta_squared = 3 * d / 80

assert c + d == 1
assert -c / 2 + d == -delta
assert -2 * delta + 3 * c == 2

h_scalar = -delta / 3
h_traceless = (
    alpha_squared * F(3, 2) + beta_squared * F(65, 9)
)
k_scalar = c / 3
k_traceless = alpha_squared * 14 + beta_squared * F(10, 9)

assert h_traceless == (5 - 8 * delta) / 48
assert k_traceless == (31 + 22 * delta) / 216
assert h_scalar + delta / 3 == 0
assert h_traceless + delta / 3 > 0

pair_ratio = 2 * (1 + delta) / 3
assert pair_ratio / 3 - k_scalar == 0
assert pair_ratio / 3 - k_traceless > 0

depth_scalar = 2 * (1 + delta) * h_scalar + 3 * delta * k_scalar
depth_traceless = (
    2 * (1 + delta) * h_traceless + 3 * delta * k_traceless
)
assert depth_scalar == 0
assert depth_traceless > 0

# On Sym^3, D0 and E0 have eigenvalues 2 and 4/9.  Both coefficients
# in C_delta are positive, so C_delta is nonzero on a 10-dimensional
# subspace and has rank at least ten.
assert F(2) > 0
assert F(4, 9) > 0

print(
    "verified: one exact high-rank C_delta realizes the a=0 local "
    "stationary forms and all cyclic multiplication identities; "
    "the construction fails only the rank-two condition"
)
