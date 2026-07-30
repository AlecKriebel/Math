#!/usr/bin/env python3
"""Exact checker for the Latin normal-frame and graph-Hessian formulas.

All arithmetic below is over the Gaussian rationals.  The checker
independently verifies:

* the rank-two third-exterior derivative and its Hilbert--Schmidt norm;
* the sign and factor two in the graph second fundamental form;
* exact vanishing of all third minors on the graph curve;
* the Lagrange-Hessian sign in a one-dimensional normal calibration;
* the previously derived qutrit Latin Haar-frame endpoint constants.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, permutations, product


@dataclass(frozen=True)
class QI:
    re: F = F(0)
    im: F = F(0)

    @staticmethod
    def make(value):
        if isinstance(value, QI):
            return value
        return QI(F(value), F(0))

    def __add__(self, other):
        other = QI.make(other)
        return QI(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return QI(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-QI.make(other))

    def __rsub__(self, other):
        return QI.make(other) - self

    def __mul__(self, other):
        other = QI.make(other)
        return QI(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    __rmul__ = __mul__

    def conjugate(self):
        return QI(self.re, -self.im)

    def inverse(self):
        denominator = self.re * self.re + self.im * self.im
        assert denominator
        return QI(self.re / denominator, -self.im / denominator)

    def __truediv__(self, other):
        return self * QI.make(other).inverse()

    def abs_squared(self):
        return self.re * self.re + self.im * self.im


ZERO = QI()
ONE = QI(1)
I = QI(0, 1)


def zero_matrix(rows, columns):
    return [[ZERO for _ in range(columns)] for _ in range(rows)]


def add_matrix(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def scale_matrix(scalar, matrix):
    return [[scalar * value for value in row] for row in matrix]


def multiply_matrix(left, right):
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(len(right))),
                ZERO,
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def conjugate_transpose(matrix):
    return [
        [matrix[i][j].conjugate() for i in range(len(matrix))]
        for j in range(len(matrix[0]))
    ]


def hs_inner(left, right):
    return sum(
        (
            left[i][j].conjugate() * right[i][j]
            for i in range(len(left))
            for j in range(len(left[0]))
        ),
        ZERO,
    )


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix):
    size = len(matrix)
    return sum(
        (
            permutation_sign(p)
            * product_entries(matrix[i][p[i]] for i in range(size))
            for p in permutations(range(size))
        ),
        ZERO,
    )


def product_entries(entries):
    value = ONE
    for entry in entries:
        value *= entry
    return value


def polynomial_add(left, right):
    size = max(len(left), len(right))
    out = [ZERO] * size
    for index in range(size):
        if index < len(left):
            out[index] += left[index]
        if index < len(right):
            out[index] += right[index]
    return out


def polynomial_multiply(left, right):
    out = [ZERO] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            out[i + j] += left_value * right_value
    return out


def minor_polynomial(base, velocity, row_indices, column_indices):
    result = [ZERO]
    for p in permutations(range(3)):
        term = [ONE]
        for i in range(3):
            term = polynomial_multiply(
                term,
                [
                    base[row_indices[i]][column_indices[p[i]]],
                    velocity[row_indices[i]][column_indices[p[i]]],
                ],
            )
        term = [permutation_sign(p) * coefficient for coefficient in term]
        result = polynomial_add(result, term)
    while len(result) < 4:
        result.append(ZERO)
    return result


def exterior_derivatives(base, velocity):
    size = len(base)
    triples = list(combinations(range(size), 3))
    first = zero_matrix(len(triples), len(triples))
    second = zero_matrix(len(triples), len(triples))
    for i, rows in enumerate(triples):
        for j, columns in enumerate(triples):
            polynomial = minor_polynomial(base, velocity, rows, columns)
            first[i][j] = polynomial[1]
            second[i][j] = 2 * polynomial[2]
    return triples, first, second


# A genuinely complex rational rank-two calibration in dimension five.
n = 5
s1 = QI(2)
s2 = QI(F(3, 2))
delta = s1 * s2
C = zero_matrix(n, n)
C[0][0] = s1
C[1][1] = s2

Z = zero_matrix(n, n)
for row in range(n):
    for column in range(n):
        Z[row][column] = QI(
            F(2 * row - column + 1, 7),
            F(row + 3 * column - 2, 11),
        )

triples, first, _ = exterior_derivatives(C, Z)
for i, rows in enumerate(triples):
    for j, columns in enumerate(triples):
        expected = ZERO
        if rows[:2] == (0, 1) and columns[:2] == (0, 1):
            expected = delta * Z[rows[2]][columns[2]]
        assert first[i][j] == expected

normal_norm_squared = sum(
    (
        Z[row][column].abs_squared()
        for row in range(2, n)
        for column in range(2, n)
    ),
    F(0),
)
first_norm_squared = sum(
    (entry.abs_squared() for row in first for entry in row),
    F(0),
)
assert first_norm_squared == delta.abs_squared() * normal_norm_squared


# Tangent graph curvature: the lower-right block of the velocity is zero.
Z_tangent = [[entry for entry in row] for row in Z]
for row in range(2, n):
    for column in range(2, n):
        Z_tangent[row][column] = ZERO

B = [row[2:] for row in Z_tangent[:2]]
D = [row[:2] for row in Z_tangent[2:]]
sigma_inverse = [
    [ONE / s1, ZERO],
    [ZERO, ONE / s2],
]
normal_acceleration_block = scale_matrix(
    QI(2), multiply_matrix(multiply_matrix(D, sigma_inverse), B)
)
W = zero_matrix(n, n)
for row in range(n - 2):
    for column in range(n - 2):
        W[row + 2][column + 2] = normal_acceleration_block[row][column]

_, _, second_tangent = exterior_derivatives(C, Z_tangent)
_, first_acceleration, _ = exterior_derivatives(C, W)
for i in range(len(triples)):
    for j in range(len(triples)):
        assert second_tangent[i][j] == -first_acceleration[i][j]


def inverse_two_by_two(matrix):
    determinant_value = (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )
    return [
        [matrix[1][1] / determinant_value, -matrix[0][1] / determinant_value],
        [-matrix[1][0] / determinant_value, matrix[0][0] / determinant_value],
    ]


# Evaluate the exact graph at a nonzero rational t and check every third minor.
t = QI(F(1, 7))
A = [row[:2] for row in Z_tangent[:2]]
M = add_matrix([[s1, ZERO], [ZERO, s2]], scale_matrix(t, A))
M_inverse = inverse_two_by_two(M)
graph = zero_matrix(n, n)
for row in range(2):
    for column in range(2):
        graph[row][column] = M[row][column]
for row in range(2):
    for column in range(n - 2):
        graph[row][column + 2] = t * B[row][column]
for row in range(n - 2):
    for column in range(2):
        graph[row + 2][column] = t * D[row][column]
bottom_right = scale_matrix(
    t * t, multiply_matrix(multiply_matrix(D, M_inverse), B)
)
for row in range(n - 2):
    for column in range(n - 2):
        graph[row + 2][column + 2] = bottom_right[row][column]
for rows in triples:
    for columns in triples:
        submatrix = [[graph[i][j] for j in columns] for i in rows]
        assert determinant(submatrix) == ZERO


# One-dimensional normal calibration of the Lagrange-Hessian sign.
# Work in dimension three, so the sole third minor is the determinant.
C3 = zero_matrix(3, 3)
C3[0][0] = QI(2)
C3[1][1] = QI(3)
Z3 = zero_matrix(3, 3)
Z3[0][2] = ONE + I
Z3[1][2] = QI(2) - I
Z3[2][0] = QI(3) + I
Z3[2][1] = -ONE + 2 * I
_, _, second3 = exterior_derivatives(C3, Z3)
d2_determinant = second3[0][0]

B3 = [row[2:] for row in Z3[:2]]
D3 = [row[:2] for row in Z3[2:]]
sigma3_inverse = [[QI(F(1, 2)), ZERO], [ZERO, QI(F(1, 3))]]
curvature_scalar = multiply_matrix(
    multiply_matrix(D3, sigma3_inverse), B3
)[0][0]
assert d2_determinant == -2 * QI(6) * curvature_scalar

r = QI(5)
mu = r / QI(6)
lagrange_curvature = -(mu.conjugate() * d2_determinant).re
normal_residual_curvature = (2 * r.conjugate() * curvature_scalar).re
assert lagrange_curvature == normal_residual_curvature


# Independently recheck the exact qutrit Latin Haar-frame endpoints.
class_sizes = (1, 3, 2)
sign_character = (1, -1, 1)
characters = {
    "S": (1, 1, 1),
    "M": (2, 0, -1),
    "A": (1, -1, 1),
}
permutation_dimensions = {"S": 1, "M": 2, "A": 1}
physical_dimensions = {"S": 10, "M": 8, "A": 1}
frame_eigenvalues = []
for labels in product(("S", "M", "A"), repeat=3):
    character_sum = sum(
        class_sizes[index]
        * sign_character[index]
        * product_entries(
            QI(characters[label][index]) for label in labels
        ).re
        for index in range(3)
    )
    multiplicity = F(character_sum, 6)
    assert multiplicity in (0, 1)
    if not multiplicity:
        continue
    permutation_dimension = 1
    physical_dimension = 1
    for label in labels:
        permutation_dimension *= permutation_dimensions[label]
        physical_dimension *= physical_dimensions[label]
    frame_eigenvalues.append(
        F(permutation_dimension, 36 * physical_dimension)
    )

assert len(frame_eigenvalues) == 11
assert min(frame_eigenvalues) == F(1, 5760)
assert max(frame_eigenvalues) == F(1, 36)

print(
    "verified: rank-two exterior differential, Latin normal-frame "
    "constants, graph curvature sign/factor two, and quotient "
    "Lagrange-Hessian calibration"
)
