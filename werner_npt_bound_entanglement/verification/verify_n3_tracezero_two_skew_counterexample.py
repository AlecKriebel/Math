#!/usr/bin/env python3
"""Exact trace-zero counterexample to the unrestricted two-skew bound.

This does not violate the Werner endpoint inequality.  It shows that
the stronger exterior inequality

    3 N - 2 S + P + 2 s1 s2 >= 0

is false even for trace-zero rank-two matrices.  Consequently its
surviving square-zero version must use C^2=0 essentially.
"""

from fractions import Fraction as F


ZERO = (F(0), F(0))


def g(real=0, imaginary=0):
    return (F(real), F(imaginary))


def gadd(left, right):
    return (left[0] + right[0], left[1] + right[1])


def gmul(left, right):
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gconj(value):
    return (value[0], -value[1])


def gnorm(value):
    return value[0] * value[0] + value[1] * value[1]


def gsum(values):
    answer = ZERO
    for value in values:
        answer = gadd(answer, value)
    return answer


LEFT8 = [
    [g(6, 5), g(3, -3)],
    [g(-2, 0), g(-1, 3)],
    [g(2, 0), g(0, -3)],
    [g(11, 0), g(-1, -7)],
    [g(-1, -1), g(-2, 2)],
    [g(-7, -8), g(-5, 6)],
    [g(9, 5), g(3, -7)],
    [g(-28, -9), g(1, -12)],
]

RIGHT8 = [
    [g(F(2, 61), F(876, 61)), g(19, -6)],
    [g(-4, -12), g(3, -1)],
    [g(7, 10), g(-2, 2)],
    [g(-9, -8), g(4, -5)],
    [g(2, -12), g(3, 0)],
    [g(1, 12), g(-7, 1)],
    [g(-4, -11), g(6, -3)],
    [g(0, 2), g(3, -3)],
]

BINARY_INDICES = (0, 1, 3, 4, 9, 10, 12, 13)


def embed(frame):
    out = [[ZERO, ZERO] for _ in range(27)]
    for source, target in enumerate(BINARY_INDICES):
        out[target] = frame[source]
    return out


LEFT = embed(LEFT8)
RIGHT = embed(RIGHT8)


def inner_column(left, right, first, second):
    return gsum(
        gmul(gconj(left[row][first]), right[row][second])
        for row in range(27)
    )


def gram_determinant(frame):
    diagonal0 = sum(gnorm(frame[row][0]) for row in range(27))
    diagonal1 = sum(gnorm(frame[row][1]) for row in range(27))
    off = inner_column(frame, frame, 0, 1)
    return diagonal0 * diagonal1 - gnorm(off)


OVERLAP = [
    [inner_column(RIGHT, LEFT, row, column) for column in range(2)]
    for row in range(2)
]
TRACE = gadd(OVERLAP[0][0], OVERLAP[1][1])
assert TRACE == ZERO
assert any(value != ZERO for row in OVERLAP for value in row)

DET_LEFT = gram_determinant(LEFT)
DET_RIGHT = gram_determinant(RIGHT)
assert DET_LEFT > 0 and DET_RIGHT > 0

# C=LEFT*RIGHT^* has rank exactly two because both factors do.
C = [[ZERO for _ in range(27)] for _ in range(27)]
for row in range(27):
    for column in range(27):
        C[row][column] = gsum(
            gmul(LEFT[row][logical], gconj(RIGHT[column][logical]))
            for logical in range(2)
        )


def words(length):
    if length == 0:
        return [()]
    return [
        tuple(
            (index // (3 ** (length - 1 - position))) % 3
            for position in range(length)
        )
        for index in range(3**length)
    ]


def encode(word):
    return 9 * word[0] + 3 * word[1] + word[2]


def partial_trace(matrix, traced):
    traced = tuple(sorted(traced))
    remaining = tuple(site for site in range(3) if site not in traced)
    out = [
        [ZERO for _ in range(3 ** len(remaining))]
        for _ in range(3 ** len(remaining))
    ]
    for output_row, row_word in enumerate(words(len(remaining))):
        for output_column, column_word in enumerate(words(len(remaining))):
            terms = []
            for traced_word in words(len(traced)):
                row = [0, 0, 0]
                column = [0, 0, 0]
                for position, site in enumerate(remaining):
                    row[site] = row_word[position]
                    column[site] = column_word[position]
                for position, site in enumerate(traced):
                    row[site] = column[site] = traced_word[position]
                terms.append(C[encode(row)][encode(column)])
            out[output_row][output_column] = gsum(terms)
    return out


def matrix_norm(matrix):
    return sum(gnorm(value) for row in matrix for value in row)


NORM = matrix_norm(C)
SINGLE = sum(matrix_norm(partial_trace(C, (site,))) for site in range(3))
PAIR = sum(
    matrix_norm(partial_trace(C, sites))
    for sites in ((0, 1), (0, 2), (1, 2))
)
LINEAR_PART = 3 * NORM - 2 * SINGLE + PAIR
EXTERIOR_SQUARED = DET_LEFT * DET_RIGHT
FOUR_Q3 = 4 * NORM - 2 * SINGLE + PAIR

# Since s1*s2=sqrt(EXTERIOR_SQUARED), the target expression is
# LINEAR_PART + 2*sqrt(EXTERIOR_SQUARED).  Its strict negativity is
# certified without numerical square roots.
assert LINEAR_PART < 0
assert LINEAR_PART * LINEAR_PART > 4 * EXTERIOR_SQUARED
assert FOUR_Q3 > 0

print("trace =", TRACE)
print("overlap =", OVERLAP)
print("det(left Gram) =", DET_LEFT)
print("det(right Gram) =", DET_RIGHT)
print("N, S, P =", NORM, SINGLE, PAIR)
print("linear part =", LINEAR_PART)
print("exterior square =", EXTERIOR_SQUARED)
print("four times endpoint Q3 =", FOUR_Q3)
print(
    "radical-free margin =",
    LINEAR_PART * LINEAR_PART - 4 * EXTERIOR_SQUARED,
)
print("all exact trace-zero two-skew counterexample checks passed")
