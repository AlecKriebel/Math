"""Exact qutrit obstruction to the proposed 3/2 determinant gap.

The anchor projection and M_Q matrix are reconstructed with rational
arithmetic.  Algebraic coefficients a+b*sqrt(2) are represented as
pairs of Fractions.
"""

from fractions import Fraction as F
from itertools import product


dims = (2, 3, 3, 3)
all_words = list(product(*[range(dimension) for dimension in dims]))
word_to_index = {word: index for index, word in enumerate(all_words)}
dimension = len(all_words)


def zeros(rows: int, columns: int) -> list[list[F]]:
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def add(
    left: list[list[F]], right: list[list[F]]
) -> list[list[F]]:
    return [
        [
            left[row][column] + right[row][column]
            for column in range(len(left[0]))
        ]
        for row in range(len(left))
    ]


def scale(value: F, matrix: list[list[F]]) -> list[list[F]]:
    return [[value * entry for entry in row] for row in matrix]


def trace_replace(
    matrix: list[list[F]], site: int
) -> list[list[F]]:
    out = zeros(dimension, dimension)
    for row_word in all_words:
        for column_word in all_words:
            if row_word[site] != column_word[site]:
                continue
            value = F(0)
            for digit in range(dims[site]):
                source_row = list(row_word)
                source_column = list(column_word)
                source_row[site] = digit
                source_column[site] = digit
                value += matrix[word_to_index[tuple(source_row)]][
                    word_to_index[tuple(source_column)]
                ]
            out[word_to_index[row_word]][word_to_index[column_word]] = value
    return out


# |U> has four amplitudes 1/sqrt(2), so its rank-one projection is
# rational even though the displayed isometry uses sqrt(2).
support = (
    (0, 1, 1, 1),
    (0, 2, 2, 2),
    (1, 1, 0, 0),
    (1, 2, 0, 0),
)
anchor_projection = zeros(dimension, dimension)
for row_word in support:
    for column_word in support:
        anchor_projection[word_to_index[row_word]][
            word_to_index[column_word]
        ] = F(1, 2)


mq = anchor_projection
for physical_site in (1, 2, 3):
    mq = add(
        scale(F(2), trace_replace(mq, physical_site)),
        scale(F(-1), mq),
    )


block_words = (
    (0, 1, 1, 1),
    (1, 2, 0, 0),
    (0, 2, 1, 1),
    (1, 1, 0, 0),
    (0, 1, 2, 2),
    (0, 2, 2, 2),
)
block_indices = tuple(word_to_index[word] for word in block_words)
expected_block = [
    [F(9, 2), F(-1, 2), F(0), F(1, 2), F(0), F(-1, 2)],
    [F(-1, 2), F(3, 2), F(1), F(-1, 2), F(0), F(1, 2)],
    [F(0), F(1), F(3), F(0), F(0), F(0)],
    [F(1, 2), F(-1, 2), F(0), F(3, 2), F(1), F(-1, 2)],
    [F(0), F(0), F(0), F(1), F(3), F(0)],
    [F(-1, 2), F(1, 2), F(0), F(-1, 2), F(0), F(9, 2)],
]
actual_block = [
    [mq[row][column] for column in block_indices]
    for row in block_indices
]
assert actual_block == expected_block

# The block is invariant, not merely principal.
for row in block_indices:
    for column in range(dimension):
        if column not in block_indices:
            assert mq[row][column] == 0
            assert mq[column][row] == 0


# Quadratic numbers are pairs (a,b), representing a+b*sqrt(2).
Quad = tuple[F, F]


def quad_add(left: Quad, right: Quad) -> Quad:
    return left[0] + right[0], left[1] + right[1]


def quad_scale(value: F, number: Quad) -> Quad:
    return value * number[0], value * number[1]


def quad_multiply(left: Quad, right: Quad) -> Quad:
    return (
        left[0] * right[0] + 2 * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


zero: Quad = (F(0), F(0))
one: Quad = (F(1), F(0))
minus_one_minus_root_two: Quad = (F(-1), F(-1))
vector: list[Quad] = [
    zero,
    minus_one_minus_root_two,
    one,
    minus_one_minus_root_two,
    one,
    zero,
]
eigenvalue: Quad = (F(2), F(-1))

matrix_vector: list[Quad] = []
for row in range(6):
    value = zero
    for column in range(6):
        value = quad_add(
            value,
            quad_scale(expected_block[row][column], vector[column]),
        )
    matrix_vector.append(value)
assert matrix_vector == [
    quad_multiply(eigenvalue, entry) for entry in vector
]

norm_squared = zero
expectation = zero
for row in range(6):
    norm_squared = quad_add(
        norm_squared, quad_multiply(vector[row], vector[row])
    )
    expectation = quad_add(
        expectation, quad_multiply(vector[row], matrix_vector[row])
    )
assert norm_squared == (F(8), F(4))
assert expectation == (F(8), F(0))


def reduced_code_matrix(site: int) -> list[list[F]]:
    """rho_site=Tr_{K,other physical sites}|U><U|."""

    out = zeros(3, 3)
    omitted = tuple(index for index in range(4) if index != site)
    omitted_words = list(product(*[range(dims[index]) for index in omitted]))
    for row_digit in range(3):
        for column_digit in range(3):
            value = F(0)
            for omitted_word in omitted_words:
                row = [0] * 4
                column = [0] * 4
                row[site] = row_digit
                column[site] = column_digit
                for index, digit in zip(omitted, omitted_word):
                    row[index] = digit
                    column[index] = digit
                value += anchor_projection[word_to_index[tuple(row)]][
                    word_to_index[tuple(column)]
                ]
            out[row_digit][column_digit] = value
    return out


def determinant_three(matrix: list[list[F]]) -> F:
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


local_determinants = tuple(
    determinant_three(reduced_code_matrix(site))
    for site in (1, 2, 3)
)
assert local_determinants == (F(0), F(1, 4), F(1, 4))
determinant_sum = sum(local_determinants)
assert determinant_sum == F(1, 2)

# Exact violation:
# <x,M_Q x> - (3/2) sum(det rho_i) ||x||^2
# = 2-3*sqrt(2) < 0.
gap = quad_add(
    expectation,
    quad_scale(F(-3, 2) * determinant_sum, norm_squared),
)
assert gap == (F(2), F(-3))
assert gap[0] > 0 and gap[0] ** 2 < 2 * gap[1] ** 2


print(
    "verified: exact qutrit isometry; local determinants "
    "(0,1/4,1/4); invariant M_Q block; eigenvalue 2-sqrt(2); "
    "3/2 determinant-gap violation 2-3sqrt(2)<0"
)


# Stronger obstruction: an exact tensor-factorized zero anchor with
# positive local determinant sum.  Its six support amplitudes are
# 1/sqrt(3), so the projection again has rational entries.
factor_support = tuple(
    (logical, physical, physical, logical)
    for logical in range(2)
    for physical in range(3)
)
factor_projection = zeros(dimension, dimension)
for row_word in factor_support:
    for column_word in factor_support:
        factor_projection[word_to_index[row_word]][
            word_to_index[column_word]
        ] = F(1, 3)

factor_mq = factor_projection
for physical_site in (1, 2, 3):
    factor_mq = add(
        scale(F(2), trace_replace(factor_mq, physical_site)),
        scale(F(-1), factor_mq),
    )


def reduced_code_matrix_from_projection(
    projection: list[list[F]], site: int
) -> list[list[F]]:
    out = zeros(3, 3)
    omitted = tuple(index for index in range(4) if index != site)
    omitted_words = list(product(*[range(dims[index]) for index in omitted]))
    for row_digit in range(3):
        for column_digit in range(3):
            value = F(0)
            for omitted_word in omitted_words:
                row = [0] * 4
                column = [0] * 4
                row[site] = row_digit
                column[site] = column_digit
                for index, digit in zip(omitted, omitted_word):
                    row[index] = digit
                    column[index] = digit
                value += projection[word_to_index[tuple(row)]][
                    word_to_index[tuple(column)]
                ]
            out[row_digit][column_digit] = value
    return out


factor_determinants = tuple(
    determinant_three(
        reduced_code_matrix_from_projection(
            factor_projection, physical_site
        )
    )
    for physical_site in (1, 2, 3)
)
assert factor_determinants == (F(8, 27), F(8, 27), F(0))
assert sum(factor_determinants) == F(16, 27)

# |00>_{12} tensor (|00>+|11>)_{K3} is an exact kernel vector.
kernel = [F(0)] * dimension
kernel[word_to_index[(0, 0, 0, 0)]] = F(1)
kernel[word_to_index[(1, 0, 0, 1)]] = F(1)
kernel_image = [
    sum(factor_mq[row][column] * kernel[column]
        for column in range(dimension))
    for row in range(dimension)
]
assert kernel_image == [F(0)] * dimension

print(
    "verified: tensor-factorized qutrit anchor has determinant sum "
    "16/27 and an exact nonzero M_Q kernel; every positive scalar "
    "determinant-gap coefficient fails"
)
