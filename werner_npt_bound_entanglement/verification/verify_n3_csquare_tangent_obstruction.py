#!/usr/bin/env python3
"""Exact checker for the C^2 tangent obstruction.

Only the Python standard library is used.  Arithmetic takes place in
Q(sqrt(3))[t].  The checker constructs the full 27 by 27 coefficient
matrix, performs all simultaneous partial traces, and verifies the
identities in notes/agent_n3_csquare_tangent_obstruction.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product


@dataclass(frozen=True)
class R:
    """a + b sqrt(3), with a,b rational."""

    a: Q = Q(0)
    b: Q = Q(0)

    def __add__(self, other: object) -> "R":
        other = as_r(other)
        return R(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self) -> "R":
        return R(-self.a, -self.b)

    def __sub__(self, other: object) -> "R":
        return self + (-as_r(other))

    def __rsub__(self, other: object) -> "R":
        return as_r(other) - self

    def __mul__(self, other: object) -> "R":
        other = as_r(other)
        return R(
            self.a * other.a + 3 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__


def as_r(value: object) -> R:
    if isinstance(value, R):
        return value
    return R(Q(value))  # type: ignore[arg-type]


ZERO_R = R()
ONE_R = R(Q(1))
INV_SQRT3 = R(Q(0), Q(1, 3))


@dataclass(frozen=True)
class Poly:
    """Polynomial of degree at most four with coefficients in Q(sqrt(3))."""

    coefficients: tuple[R, ...] = ()

    def __add__(self, other: object) -> "Poly":
        other = as_poly(other)
        size = max(len(self.coefficients), len(other.coefficients))
        out = []
        for index in range(size):
            left = (
                self.coefficients[index]
                if index < len(self.coefficients)
                else ZERO_R
            )
            right = (
                other.coefficients[index]
                if index < len(other.coefficients)
                else ZERO_R
            )
            out.append(left + right)
        while out and out[-1] == ZERO_R:
            out.pop()
        return Poly(tuple(out))

    __radd__ = __add__

    def __neg__(self) -> "Poly":
        return Poly(tuple(-value for value in self.coefficients))

    def __sub__(self, other: object) -> "Poly":
        return self + (-as_poly(other))

    def __rsub__(self, other: object) -> "Poly":
        return as_poly(other) - self

    def __mul__(self, other: object) -> "Poly":
        other = as_poly(other)
        if not self.coefficients or not other.coefficients:
            return Poly()
        out = [ZERO_R] * (
            len(self.coefficients) + len(other.coefficients) - 1
        )
        for left_index, left in enumerate(self.coefficients):
            for right_index, right in enumerate(other.coefficients):
                out[left_index + right_index] = (
                    out[left_index + right_index] + left * right
                )
        return Poly(tuple(out))

    __rmul__ = __mul__


def as_poly(value: object) -> Poly:
    if isinstance(value, Poly):
        return value
    return Poly((as_r(value),))


ZERO = Poly()
ONE = Poly((ONE_R,))
T = Poly((ZERO_R, ONE_R))

D = 3
N_SITES = 3
BASIS = list(product(range(D), repeat=N_SITES))
INDEX = {word: index for index, word in enumerate(BASIS)}
MATRIX_SIZE = D**N_SITES


def zero_matrix(size: int) -> list[list[Poly]]:
    return [[ZERO for _ in range(size)] for _ in range(size)]


def outer(left: list[R], right: list[R]) -> list[list[Poly]]:
    return [
        [as_poly(left[row] * right[column])
         for column in range(MATRIX_SIZE)]
        for row in range(MATRIX_SIZE)
    ]


def add_scaled(
    left: list[list[Poly]],
    scalar: Poly,
    right: list[list[Poly]],
) -> list[list[Poly]]:
    return [
        [
            left[row][column] + scalar * right[row][column]
            for column in range(len(left[0]))
        ]
        for row in range(len(left))
    ]


def matrix_product(
    left: list[list[Poly]],
    right: list[list[Poly]],
) -> list[list[Poly]]:
    return [
        [
            sum(
                (left[row][middle] * right[middle][column]
                 for middle in range(len(right))),
                ZERO,
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def hs_norm_squared(matrix: list[list[Poly]]) -> Poly:
    # Every coefficient in the construction is real.
    return sum(
        (entry * entry for row in matrix for entry in row),
        ZERO,
    )


def partial_trace(
    matrix: list[list[Poly]],
    traced: tuple[int, ...],
) -> list[list[Poly]]:
    remaining = tuple(
        site for site in range(N_SITES) if site not in traced
    )
    remaining_words = list(product(range(D), repeat=len(remaining)))
    traced_words = list(product(range(D), repeat=len(traced)))
    out = zero_matrix(len(remaining_words))
    for row_index, row_remaining in enumerate(remaining_words):
        for column_index, column_remaining in enumerate(remaining_words):
            value = ZERO
            for traced_word in traced_words:
                row = [0] * N_SITES
                column = [0] * N_SITES
                for position, site in enumerate(remaining):
                    row[site] = row_remaining[position]
                    column[site] = column_remaining[position]
                for position, site in enumerate(traced):
                    row[site] = traced_word[position]
                    column[site] = traced_word[position]
                value += matrix[
                    INDEX[tuple(row)]
                ][
                    INDEX[tuple(column)]
                ]
            out[row_index][column_index] = value
    return out


def basis_vector(words: tuple[tuple[int, ...], ...]) -> list[R]:
    vector = [ZERO_R] * MATRIX_SIZE
    for word in words:
        vector[INDEX[word]] = INV_SQRT3
    return vector


x = [ZERO_R] * MATRIX_SIZE
x[INDEX[(0, 0, 0)]] = ONE_R
y = basis_vector(((0, 0, 1), (0, 1, 0), (1, 0, 0)))
z = basis_vector(((0, 1, 1), (1, 0, 1), (1, 1, 0)))

C = add_scaled(outer(x, y), T, outer(y, z))

N_value = hs_norm_squared(C)
S_value = sum(
    (hs_norm_squared(partial_trace(C, (site,)))
     for site in range(N_SITES)),
    ZERO,
)
P_value = sum(
    (
        hs_norm_squared(partial_trace(C, pair))
        for pair in ((0, 1), (0, 2), (1, 2))
    ),
    ZERO,
)
C_squared_norm = hs_norm_squared(matrix_product(C, C))

assert N_value == Poly((ONE_R, ZERO_R, ONE_R))
assert S_value == Poly(
    (R(Q(2)), R(Q(0), Q(4, 3)), R(Q(4, 3)))
)
assert P_value == Poly(
    (R(Q(1)), R(Q(0), Q(4, 3)), R(Q(4, 3)))
)
assert C_squared_norm == Poly((ZERO_R, ZERO_R, ONE_R))

A0 = 3 * N_value - 2 * S_value + P_value
assert A0 == Poly(
    (ZERO_R, R(Q(0), Q(-4, 3)), R(Q(5, 3)))
)

# Since the two dyads in C have orthogonal initial and final vectors,
# the singular values are 1,t for 0<t<=1.  Therefore D=t.
F_value = A0 + 2 * T
assert F_value == Poly(
    (ZERO_R, R(Q(2), Q(-4, 3)), R(Q(5, 3)))
)

# Exact rational comparison used for c=1/4 and t=1/100:
# sqrt(3)<7/4, so 4/sqrt(3)>16/7.
upper_bound = (Q(9, 4) - Q(16, 7)) * Q(1, 100) + Q(5, 3) * Q(
    1, 10_000
)
assert upper_bound == -Q(1, 2800) + Q(1, 6000)
assert upper_bound < 0

print("verified exact C^2 tangent obstruction")
print("N =", N_value)
print("S =", S_value)
print("P =", P_value)
print("||C^2||^2 =", C_squared_norm)
print("F =", F_value)
print("c=1/4 rational upper bound at t=1/100 =", upper_bound)
