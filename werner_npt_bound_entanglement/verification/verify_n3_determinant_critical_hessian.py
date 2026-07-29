#!/usr/bin/env python3
"""Exact audit of the determinant-critical Hessian identities."""

from __future__ import annotations

from fractions import Fraction as F


def zeros(rows: int, columns: int) -> list[list[F]]:
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def transpose(matrix: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*matrix)]


def add(*matrices: list[list[F]]) -> list[list[F]]:
    return [
        [sum((matrix[i][j] for matrix in matrices), F(0))
         for j in range(len(matrices[0][0]))]
        for i in range(len(matrices[0]))
    ]


def scale(value: F, matrix: list[list[F]]) -> list[list[F]]:
    return [[value * entry for entry in row] for row in matrix]


def multiply(
    left: list[list[F]], right: list[list[F]]
) -> list[list[F]]:
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(len(right))),
                F(0),
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def trace(matrix: list[list[F]]) -> F:
    return sum((matrix[i][i] for i in range(len(matrix))), F(0))


def inner(left: list[list[F]], right: list[list[F]]) -> F:
    return sum(
        (
            left[i][j] * right[i][j]
            for i in range(len(left))
            for j in range(len(left[0]))
        ),
        F(0),
    )


def norm_squared(matrix: list[list[F]]) -> F:
    return inner(matrix, matrix)


def flatten(matrix: list[list[F]]) -> list[F]:
    return [entry for row in matrix for entry in row]


def unflatten(vector: list[F], size: int) -> list[list[F]]:
    return [
        vector[size * row:size * (row + 1)]
        for row in range(size)
    ]


def apply_superoperator(
    superoperator: list[list[F]], matrix: list[list[F]]
) -> list[list[F]]:
    vector = flatten(matrix)
    image = [
        sum(
            (superoperator[i][j] * vector[j] for j in range(len(vector))),
            F(0),
        )
        for i in range(len(vector))
    ]
    return unflatten(image, len(matrix))


def block_matrix(
    top_left: list[list[F]],
    top_right: list[list[F]],
    bottom_left: list[list[F]],
    bottom_right: list[list[F]],
) -> list[list[F]]:
    size = len(top_left)
    return [
        top_left[row] + top_right[row]
        for row in range(size)
    ] + [
        bottom_left[row] + bottom_right[row]
        for row in range(size)
    ]


# Critical rank-two point in a 2 + 2 row/column decomposition.
sigma = [[F(2), F(0)], [F(0), F(1, 2)]]
sigma_inverse = [[F(1, 2), F(0)], [F(0), F(2)]]
zero2 = zeros(2, 2)
c = block_matrix(sigma, zero2, zero2, zero2)
n_gradient = block_matrix(sigma_inverse, zero2, zero2, zero2)
normal_residual = [[F(1), F(2)], [F(-1), F(1, 3)]]
r_full = block_matrix(zero2, zero2, zero2, normal_residual)
critical_value = F(-1)
target_image = add(scale(critical_value, n_gradient), r_full)

# Build an exact real self-adjoint superoperator sending C to the
# prescribed critical image.  A large positive term on C-perp makes
# the test Hessian comfortably nonnegative without changing L(C).
c_vector = flatten(c)
d_vector = flatten(target_image)
c_norm = sum((value * value for value in c_vector), F(0))
c_dot_d = sum(
    (c_vector[i] * d_vector[i] for i in range(len(c_vector))), F(0)
)
dimension = len(c_vector)
superoperator = zeros(dimension, dimension)
for i in range(dimension):
    for j in range(dimension):
        superoperator[i][j] = (
            (d_vector[i] * c_vector[j] + c_vector[i] * d_vector[j])
            / c_norm
            - c_dot_d * c_vector[i] * c_vector[j] / c_norm**2
        )
        # Add 100 times the orthogonal projector off span(C).
        superoperator[i][j] += F(100) * (
            int(i == j) - c_vector[i] * c_vector[j] / c_norm
        )
assert superoperator == transpose(superoperator)
assert apply_superoperator(superoperator, c) == target_image

# The diagonal critical equations force reciprocal rank-one energies
# and a strict reverse-Cauchy defect when lambda is negative.
rank_one_a = F(1, 4)
singular_square = F(2)
rank_one_b = singular_square**2 * rank_one_a
negative_lambda = F(-1, 8)
crossed_c = negative_lambda - singular_square * rank_one_a
assert negative_lambda == crossed_c + rank_one_b / singular_square
assert crossed_c < 0
assert crossed_c**2 - rank_one_a * rank_one_b == (
    negative_lambda**2
    - 2 * negative_lambda * singular_square * rank_one_a
)
assert crossed_c**2 > rank_one_a * rank_one_b

# General core and two-sided plane velocity.
core_velocity = [[F(1), F(2)], [F(-1), F(-1, 4)]]
x = [[F(1), F(2)], [F(-1), F(1)]]
z = [[F(2), F(-1)], [F(1), F(3)]]
tangent_trace = trace(multiply(sigma_inverse, core_velocity))
assert tangent_trace == 0
square_trace = trace(
    multiply(
        multiply(sigma_inverse, core_velocity),
        multiply(sigma_inverse, core_velocity),
    )
)
core_acceleration = [[2 * square_trace, F(0)], [F(0), F(0)]]
assert trace(multiply(sigma_inverse, core_acceleration)) == square_trace

d_core = block_matrix(core_velocity, zero2, zero2, zero2)
d_left = block_matrix(
    zero2, zero2, multiply(x, sigma), zero2
)
d_right = block_matrix(
    zero2, multiply(sigma, z), zero2, zero2
)
d_total = add(d_core, d_left, d_right)

top_left_acceleration = add(
    core_acceleration,
    scale(F(-1), multiply(multiply(transpose(x), x), sigma)),
    scale(F(-1), multiply(sigma, multiply(z, transpose(z)))),
)
top_right_acceleration = scale(F(2), multiply(core_velocity, z))
bottom_left_acceleration = scale(F(2), multiply(x, core_velocity))
normal_acceleration = scale(F(2), multiply(multiply(x, sigma), z))
second_derivative = block_matrix(
    top_left_acceleration,
    top_right_acceleration,
    bottom_left_acceleration,
    normal_acceleration,
)

q_of_tangent = inner(
    d_total, apply_superoperator(superoperator, d_total)
)
direct_half_hessian = q_of_tangent + inner(target_image, second_derivative)
formula_half_hessian = (
    q_of_tangent
    + critical_value * square_trace
    - critical_value * (norm_squared(x) + norm_squared(z))
    + 2 * inner(normal_residual, multiply(multiply(x, sigma), z))
)
assert direct_half_hessian == formula_half_hessian
assert formula_half_hessian > 0

# The two-leakage phase decomposition and its sharp budget.
a_value = (
    inner(d_left, apply_superoperator(superoperator, d_left))
    - critical_value * norm_squared(x)
)
b_value = (
    inner(d_right, apply_superoperator(superoperator, d_right))
    - critical_value * norm_squared(z)
)
p_value = inner(d_left, apply_superoperator(superoperator, d_right))
q_value = inner(normal_residual, multiply(multiply(x, sigma), z))
assert a_value >= 0 and b_value >= 0
assert (abs(p_value) + abs(q_value)) ** 2 <= a_value * b_value

# Exact fixed-pencil solution in one magic companion direction.
lambda_zero = F(-1)
lambda_good = F(3, 2)
z0_square = F(25, 16)
z1_square = F(9, 16)  # coefficient is 3i/4, so its square is -9/16
assert z0_square - z1_square == 1
good_energy = lambda_zero * z0_square + lambda_good * z1_square
assert good_energy >= lambda_zero
assert lambda_zero + lambda_good > 0  # the strict rank-one test

lambda_bad = F(1, 2)
bad_energy = lambda_zero * z0_square + lambda_bad * z1_square
assert lambda_zero + lambda_bad < 0
assert bad_energy < lambda_zero

print(
    "verified exact determinant constraints, complete critical Hessian, "
    "coupled two-leakage budget, and fixed-pencil magic solution"
)
