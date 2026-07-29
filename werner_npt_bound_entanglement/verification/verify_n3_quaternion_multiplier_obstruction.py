"""Exact checker for the separate quaternion-multiplier obstruction.

Only standard-library rational arithmetic is used.  The script checks:

* orthonormality of the rational three-qubit anchor;
* the three exact weighted Fierz-energy ratios;
* strict violation of every squared multiplier bound with constant 3; and
* the rank and displayed kernel of the coupled four-channel Gram.
"""

from fractions import Fraction as F
from itertools import product


def zeros(rows: int, columns: int) -> list[list[F]]:
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def identity(size: int) -> list[list[F]]:
    out = zeros(size, size)
    for index in range(size):
        out[index][index] = F(1)
    return out


def transpose(matrix: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*matrix)]


def multiply(
    left: list[list[F]], right: list[list[F]]
) -> list[list[F]]:
    return [
        [
            sum(
                left[row][middle] * right[middle][column]
                for middle in range(len(right))
            )
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


def index(word: tuple[int, int, int]) -> int:
    return 4 * word[0] + 2 * word[1] + word[2]


def partial_transpose(
    matrix: list[list[F]], site: int
) -> list[list[F]]:
    out = zeros(8, 8)
    for row_word in product(range(2), repeat=3):
        for column_word in product(range(2), repeat=3):
            source_row = list(row_word)
            source_column = list(column_word)
            source_row[site], source_column[site] = (
                source_column[site],
                source_row[site],
            )
            out[index(row_word)][index(column_word)] = matrix[
                index(tuple(source_row))
            ][index(tuple(source_column))]
    return out


def weighted_energy(
    anchor: list[list[F]],
    test: list[list[F]],
    logical: list[list[F]],
) -> F:
    physical = multiply(
        multiply(test, transpose(logical)), transpose(anchor)
    )
    filtered = physical
    for site in range(3):
        filtered = add(
            filtered,
            partial_transpose(filtered, site),
            F(2),
            F(-1),
        )
    return sum(
        physical[row][column] * filtered[row][column]
        for row in range(8)
        for column in range(8)
    ) / 8


I = [[F(1), F(0)], [F(0), F(1)]]
X = [[F(0), F(1)], [F(1), F(0)]]
Z = [[F(1), F(0)], [F(0), F(-1)]]
EPSILON = [[F(0), F(1)], [F(-1), F(0)]]


U = zeros(8, 2)
U[0][0] = F(1)
U[1][1] = F(3, 5)
U[2][1] = F(4, 5)
assert multiply(transpose(U), U) == identity(2)


def test_from_interleaved(entries: dict[int, int]) -> list[list[F]]:
    out = zeros(8, 2)
    for coordinate, value in entries.items():
        out[coordinate // 2][coordinate % 2] = F(value)
    return out


tests = {
    "I": (
        I,
        test_from_interleaved({1: -4, 2: -5, 4: -4, 7: -5}),
        F(9237, 200),
        F(143, 10),
    ),
    "X": (
        X,
        test_from_interleaved({2: 4, 4: 4, 7: 5}),
        F(1921, 50),
        F(521, 50),
    ),
    "Z": (
        Z,
        test_from_interleaved({1: -4, 2: 5, 4: 4, 7: 5}),
        F(9237, 200),
        F(143, 10),
    ),
}

for logical, test, expected_negative, expected_positive in tests.values():
    negative = weighted_energy(U, test, EPSILON)
    positive = weighted_energy(U, test, logical)
    assert negative == expected_negative
    assert positive == expected_positive
    assert negative - 3 * positive > 0


def quadratic_gram(logical: list[list[F]]) -> list[list[F]]:
    gram = zeros(16, 16)
    for column in range(16):
        basis_test = zeros(8, 2)
        basis_test[column // 2][column % 2] = F(1)
        for row in range(column + 1):
            other_test = zeros(8, 2)
            other_test[row // 2][row % 2] = F(1)
            diagonal_sum = weighted_energy(
                U,
                add(basis_test, other_test),
                logical,
            )
            value = (
                diagonal_sum
                - weighted_energy(U, basis_test, logical)
                - weighted_energy(U, other_test, logical)
            ) / 2
            if row == column:
                value = weighted_energy(U, basis_test, logical)
            gram[row][column] = value
            gram[column][row] = value
    return gram


grams = {name: quadratic_gram(logical) for name, logical in {
    "I": I,
    "X": X,
    "Z": Z,
    "E": EPSILON,
}.items()}
coupled = add(
    add(grams["I"], grams["X"]),
    add(grams["Z"], grams["E"], F(1), F(-1)),
)


def determinant(matrix: list[list[F]]) -> F:
    work = [row[:] for row in matrix]
    size = len(work)
    value = F(1)
    for pivot_column in range(size):
        pivot_row = next(
            (
                row
                for row in range(pivot_column, size)
                if work[row][pivot_column]
            ),
            None,
        )
        if pivot_row is None:
            return F(0)
        if pivot_row != pivot_column:
            work[pivot_column], work[pivot_row] = (
                work[pivot_row],
                work[pivot_column],
            )
            value = -value
        pivot = work[pivot_column][pivot_column]
        value *= pivot
        for row in range(pivot_column + 1, size):
            coefficient = work[row][pivot_column] / pivot
            if coefficient:
                for column in range(pivot_column + 1, size):
                    work[row][column] -= (
                        coefficient * work[pivot_column][column]
                    )
        for row in range(pivot_column + 1, size):
            work[row][pivot_column] = F(0)
    return value


# The generalized characteristic determinants have degree at most 16.
# Agreement at 17 rational points therefore verifies the exact factorizations
# in the note, after normalizing both sides at lambda=0.
det_negative = determinant(grams["E"])
assert det_negative


def polynomial_iz(value: F) -> F:
    return (
        (value - 1) ** 8
        * (1875 * value * value - 6826 * value + 2451) ** 2
        * (2451 * value * value - 6826 * value + 1875) ** 2
    )


def polynomial_x(value: F) -> F:
    return (
        (value - 3) ** 2
        * (value - 1) ** 8
        * (3 * value - 1) ** 2
        * (2451 * value * value - 9706 * value + 2451) ** 2
    )


for positive_name, claimed in (
    ("I", polynomial_iz),
    ("Z", polynomial_iz),
    ("X", polynomial_x),
):
    claimed_zero = claimed(F(0))
    for integer in range(17):
        value = F(integer)
        pencil = add(
            grams["E"], grams[positive_name], F(1), -value
        )
        assert (
            determinant(pencil) * claimed_zero
            == det_negative * claimed(value)
        )


def matrix_rank(matrix: list[list[F]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for pivot_column in range(columns):
        nonzero = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][pivot_column]
            ),
            None,
        )
        if nonzero is None:
            continue
        work[pivot_row], work[nonzero] = (
            work[nonzero],
            work[pivot_row],
        )
        pivot = work[pivot_row][pivot_column]
        work[pivot_row] = [entry / pivot for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            coefficient = work[row][pivot_column]
            if coefficient:
                work[row] = [
                    work[row][column]
                    - coefficient * work[pivot_row][column]
                    for column in range(columns)
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


assert matrix_rank(coupled) == 14
kernel_vectors = [
    {
        2: F(4, 5),
        4: F(3, 5),
        7: F(1),
    },
    {
        10: F(4, 5),
        12: F(3, 5),
        15: F(1),
    },
]
for entries in kernel_vectors:
    vector = [entries.get(index, F(0)) for index in range(16)]
    assert all(
        sum(coupled[row][column] * vector[column]
            for column in range(16)) == 0
        for row in range(16)
    )


print(
    "verified: rational three-qubit anchor; three strict >3 "
    "quaternion-multiplier ratios; coupled Gram rank and kernel"
)
