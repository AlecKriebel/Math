#!/usr/bin/env python3
"""Exact verifier for the intersection-one S4 linear obstruction.

Only standard-library rational arithmetic is used.  The script derives
the [22] representation from the permutation action on perfect
matchings, constructs the four-replica kernel, and checks the exact
negative F_12-even vector.
"""

from fractions import Fraction as F
from itertools import permutations
from math import factorial


def identity(size: int) -> list[list[F]]:
    return [
        [F(int(row == column)) for column in range(size)]
        for row in range(size)
    ]


def transpose(matrix: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*matrix)]


def multiply(
    left: list[list[F]], right: list[list[F]]
) -> list[list[F]]:
    return [
        [
            sum(left[row][k] * right[k][column] for k in range(len(right)))
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def add(
    left: list[list[F]],
    right: list[list[F]],
    left_scale: F = F(1),
    right_scale: F = F(1),
) -> list[list[F]]:
    return [
        [
            left_scale * left[row][column]
            + right_scale * right[row][column]
            for column in range(len(left[0]))
        ]
        for row in range(len(left))
    ]


def kronecker(
    left: list[list[F]], right: list[list[F]]
) -> list[list[F]]:
    left_rows, left_columns = len(left), len(left[0])
    right_rows, right_columns = len(right), len(right[0])
    return [
        [
            left[row // right_rows][column // right_columns]
            * right[row % right_rows][column % right_columns]
            for column in range(left_columns * right_columns)
        ]
        for row in range(left_rows * right_rows)
    ]


def tensor_cube(matrix: list[list[F]]) -> list[list[F]]:
    return kronecker(kronecker(matrix, matrix), matrix)


def matrix_vector(
    matrix: list[list[F]], vector: list[F]
) -> list[F]:
    return [
        sum(matrix[row][column] * vector[column] for column in range(len(vector)))
        for row in range(len(matrix))
    ]


def inner_metric(
    left: list[F],
    metric: list[list[F]],
    right: list[F],
) -> F:
    image = matrix_vector(metric, right)
    return sum(x * y for x, y in zip(left, image))


matchings = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def canonical_matching(
    matching: tuple[tuple[int, int], tuple[int, int]]
) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(sorted(tuple(sorted(pair)) for pair in matching))


canonical_matchings = tuple(
    canonical_matching(matching) for matching in matchings
)


def transposition(first: int, second: int) -> tuple[int, ...]:
    permutation = list(range(4))
    permutation[first], permutation[second] = (
        permutation[second],
        permutation[first],
    )
    return tuple(permutation)


def matching_permutation(
    permutation: tuple[int, ...],
) -> list[list[F]]:
    matrix = [[F(0) for _ in range(3)] for _ in range(3)]
    for column, matching in enumerate(matchings):
        image = canonical_matching(
            tuple(
                (permutation[first], permutation[second])
                for first, second in matching
            )
        )
        matrix[canonical_matchings.index(image)][column] = F(1)
    return matrix


# Columns are e_1=m_0-m_2 and e_2=m_1-m_2.  A sum-zero vector's first
# two matching coordinates are exactly its coordinates in this basis.
matching_basis = [
    [F(1), F(0)],
    [F(0), F(1)],
    [F(-1), F(-1)],
]


def irrep_22(permutation: tuple[int, ...]) -> list[list[F]]:
    image = multiply(matching_permutation(permutation), matching_basis)
    return image[:2]


def swap(first: int, second: int) -> list[list[F]]:
    return irrep_22(transposition(first, second))


metric = [[F(2), F(1)], [F(1), F(2)]]
f12 = swap(0, 1)
assert f12 == [[F(1), F(0)], [F(-1), F(-1)]]

# Every permutation matrix is self-adjoint/unitary in the inherited
# metric in the appropriate inverse sense.  Transpositions suffice here.
for first in range(4):
    for second in range(first + 1, 4):
        transposition_matrix = swap(first, second)
        assert multiply(
            transpose(transposition_matrix), metric
        ) == multiply(metric, transposition_matrix)
        assert multiply(transposition_matrix, transposition_matrix) == identity(2)

local_a = multiply(
    add(identity(2), swap(0, 1), F(1), F(-1, 2)),
    add(identity(2), swap(2, 3), F(1), F(-1, 2)),
)
local_b = multiply(
    multiply(
        multiply(
            add(identity(2), swap(0, 3), F(1), F(-1, 2)),
            add(identity(2), swap(1, 2), F(1), F(-1, 2)),
        ),
        swap(0, 2),
    ),
    swap(1, 3),
)

assert local_a == [[F(1, 4), F(0)], [F(1), F(9, 4)]]
assert local_b == [[F(5, 4), F(-1)], [F(-1), F(5, 4)]]
assert multiply(transpose(local_a), metric) == multiply(metric, local_a)
assert multiply(transpose(local_b), metric) == multiply(metric, local_b)

global_metric = tensor_cube(metric)
global_swap_12 = tensor_cube(f12)
kernel = add(tensor_cube(local_a), tensor_cube(local_b), F(1), F(-1))

vector = [F(value) for value in (-2, 1, 1, -1, 1, -1, -1, 1)]
assert matrix_vector(global_swap_12, vector) == vector
assert inner_metric(vector, global_metric, vector) == F(18)
expectation = inner_metric(vector, global_metric, matrix_vector(kernel, vector))
assert expectation == F(-891, 8)
assert expectation / F(18) == F(-99, 16)


# The repeated-w Veronese image itself can have a negative [22]^3 block
# contribution.  Construct the local [22] central projector from its
# S_4 character and apply it to |0011>.
def cycle_type(permutation: tuple[int, ...]) -> tuple[int, ...]:
    seen: set[int] = set()
    lengths: list[int] = []
    for start in range(4):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


character_22 = {
    (1, 1, 1, 1): F(2),
    (2, 1, 1): F(0),
    (2, 2): F(2),
    (3, 1): F(-1),
    (4,): F(0),
}
characters = {
    "4": {
        (1, 1, 1, 1): F(1),
        (2, 1, 1): F(1),
        (2, 2): F(1),
        (3, 1): F(1),
        (4,): F(1),
    },
    "31": {
        (1, 1, 1, 1): F(3),
        (2, 1, 1): F(1),
        (2, 2): F(-1),
        (3, 1): F(0),
        (4,): F(-1),
    },
    "22": character_22,
}
irrep_dimensions = {"4": 1, "31": 3, "22": 2}


def apply_word_permutation(
    vector: dict[tuple[int, ...], F],
    permutation: tuple[int, ...],
) -> dict[tuple[int, ...], F]:
    out: dict[tuple[int, ...], F] = {}
    for word, coefficient in vector.items():
        image = tuple(word[permutation[index]] for index in range(4))
        out[image] = out.get(image, F(0)) + coefficient
    return {word: coefficient for word, coefficient in out.items() if coefficient}


def vector_linear_combination(
    left: dict[tuple[int, ...], F],
    right: dict[tuple[int, ...], F],
    left_scale: F = F(1),
    right_scale: F = F(1),
) -> dict[tuple[int, ...], F]:
    out: dict[tuple[int, ...], F] = {}
    for word in set(left) | set(right):
        coefficient = (
            left_scale * left.get(word, F(0))
            + right_scale * right.get(word, F(0))
        )
        if coefficient:
            out[word] = coefficient
    return out


def local_inner(
    left: dict[tuple[int, ...], F],
    right: dict[tuple[int, ...], F],
) -> F:
    return sum(
        coefficient * right.get(word, F(0))
        for word, coefficient in left.items()
    )


def apply_swap_to_vector(
    vector: dict[tuple[int, ...], F], first: int, second: int
) -> dict[tuple[int, ...], F]:
    return apply_word_permutation(vector, transposition(first, second))


def apply_i_minus_half_swap(
    vector: dict[tuple[int, ...], F], first: int, second: int
) -> dict[tuple[int, ...], F]:
    return vector_linear_combination(
        vector,
        apply_swap_to_vector(vector, first, second),
        F(1),
        F(-1, 2),
    )


local_word = {(0, 0, 1, 1): F(1)}


def central_projection(
    vector: dict[tuple[int, ...], F], irrep: str
) -> dict[tuple[int, ...], F]:
    out: dict[tuple[int, ...], F] = {}
    for permutation in permutations(range(4)):
        coefficient = (
            F(irrep_dimensions[irrep], 24)
            * characters[irrep][cycle_type(permutation)]
        )
        out = vector_linear_combination(
            out,
            apply_word_permutation(vector, permutation),
            F(1),
            coefficient,
        )
    return out


projected_word = central_projection(local_word, "22")

assert projected_word == {
    (0, 0, 1, 1): F(1, 3),
    (1, 1, 0, 0): F(1, 3),
    (0, 1, 0, 1): F(-1, 6),
    (0, 1, 1, 0): F(-1, 6),
    (1, 0, 0, 1): F(-1, 6),
    (1, 0, 1, 0): F(-1, 6),
}

local_a_image = apply_i_minus_half_swap(
    apply_i_minus_half_swap(projected_word, 2, 3), 0, 1
)
local_b_image = apply_i_minus_half_swap(
    apply_i_minus_half_swap(
        apply_swap_to_vector(
            apply_swap_to_vector(projected_word, 1, 3), 0, 2
        ),
        1,
        2,
    ),
    0,
    3,
)

local_norm = local_inner(projected_word, projected_word)
local_a_expectation = local_inner(projected_word, local_a_image)
local_b_expectation = local_inner(projected_word, local_b_image)
assert local_norm == F(1, 3)
assert local_a_expectation == F(1, 12)
assert local_b_expectation == F(7, 12)
assert local_a_expectation**3 - local_b_expectation**3 == F(-19, 96)

# Resolve the exact cross-isotypic compensation.  Only [4], [31], and
# [22] occur in the orbit of a word with content 2+2.
local_isotypic_data: dict[str, tuple[F, F, F]] = {}
for irrep in ("4", "31", "22"):
    component = central_projection(local_word, irrep)
    a_image = apply_i_minus_half_swap(
        apply_i_minus_half_swap(component, 2, 3), 0, 1
    )
    b_image = apply_i_minus_half_swap(
        apply_i_minus_half_swap(
            apply_swap_to_vector(
                apply_swap_to_vector(component, 1, 3), 0, 2
            ),
            1,
            2,
        ),
        0,
        3,
    )
    local_isotypic_data[irrep] = (
        local_inner(component, component),
        local_inner(component, a_image),
        local_inner(component, b_image),
    )

assert local_isotypic_data == {
    "4": (F(1, 6), F(1, 24), F(1, 24)),
    "31": (F(1, 2), F(1, 8), F(-3, 8)),
    "22": (F(1, 3), F(1, 12), F(7, 12)),
}

triple_contributions: dict[tuple[int, int, int], F] = {}
labels = ("4", "31", "22")
for count_4 in range(4):
    for count_31 in range(4 - count_4):
        count_22 = 3 - count_4 - count_31
        counts = (count_4, count_31, count_22)
        multiplicity = (
            factorial(3)
            // factorial(count_4)
            // factorial(count_31)
            // factorial(count_22)
        )
        a_product = F(multiplicity)
        b_product = F(multiplicity)
        for label, count in zip(labels, counts):
            a_product *= local_isotypic_data[label][1] ** count
            b_product *= local_isotypic_data[label][2] ** count
        triple_contributions[counts] = a_product - b_product

assert triple_contributions == {
    (0, 0, 3): F(-19, 96),
    (0, 1, 2): F(37, 96),
    (0, 2, 1): F(-31, 128),
    (0, 3, 0): F(7, 128),
    (1, 0, 2): F(-1, 24),
    (1, 1, 1): F(11, 192),
    (1, 2, 0): F(-1, 64),
    (2, 0, 1): F(-1, 384),
    (2, 1, 0): F(1, 384),
    (3, 0, 0): F(0),
}
assert sum(triple_contributions.values()) == F(0)

# For w=|000>, u=v=|111>, each full local contraction is respectively
# 1/2, 1/2, and -1/2, so ab-|z|^2=0 despite the negative [22]^3 part.
full_a = F(1, 2) ** 3
full_b = F(1, 2) ** 3
full_z = F(-1, 2) ** 3
assert full_a * full_b - full_z**2 == F(0)

print(
    "verified: [22]^3 vector is F12-even, has norm 18, "
    "and exact expectation -891/8; physical repeated-w block "
    "contribution is -19/96 while the full determinant is zero"
)
