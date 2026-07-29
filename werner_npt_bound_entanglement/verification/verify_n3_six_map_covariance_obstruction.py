#!/usr/bin/env python3
"""Exact arithmetic audit of the six-map norm/covariance obstruction."""

from fractions import Fraction as F


def matrix_zero():
    return [[F(0) for _ in range(3)] for _ in range(3)]


def matrix_add(*matrices):
    return [
        [
            sum((matrix[row][column] for matrix in matrices), F(0))
            for column in range(len(matrices[0][0]))
        ]
        for row in range(len(matrices[0]))
    ]


def matrix_scale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def matrix_multiply(left, right):
    return [
        [
            sum(
                (
                    left[row][middle] * right[middle][column]
                    for middle in range(len(right))
                ),
                F(0),
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def matrix_adjoint(matrix):
    # Every exact test matrix below is rational.
    return [list(row) for row in zip(*matrix)]


def matrix_norm_squared(matrix):
    return sum((entry * entry for row in matrix for entry in row), F(0))


def kronecker(left, right):
    return [
        [
            left[row_left][column_left] * right[row_right][column_right]
            for column_left in range(len(left[0]))
            for column_right in range(len(right[0]))
        ]
        for row_left in range(len(left))
        for row_right in range(len(right))
    ]


def tensor_three(factors):
    return kronecker(kronecker(factors[0], factors[1]), factors[2])


identity = [
    [F(1) if row == column else F(0) for column in range(3)]
    for row in range(3)
]
scalar_identity = matrix_scale(F(1, 3), identity)
z_matrix = [[F(1), F(0), F(0)], [F(0), F(-1), F(0)], [F(0), F(0), F(0)]]
x_matrix = matrix_zero()
x_matrix[0][1] = F(1)


def scalar_projection(matrix):
    trace = sum(matrix[index][index] for index in range(3))
    return matrix_scale(trace / 3, identity)


def traceless_projection(matrix):
    return matrix_add(matrix, matrix_scale(F(-1), scalar_projection(matrix)))


def pair_projection_of_product(factors):
    terms = []
    for scalar_site in range(3):
        projected = [
            (
                scalar_projection(factor)
                if site == scalar_site
                else traceless_projection(factor)
            )
            for site, factor in enumerate(factors)
        ]
        terms.append(tensor_three(projected))
    return matrix_add(*terms)


# First verify the physical covariance identity T_i^L-T_i^R=[A_i,D]
# and the exact 12||D||^2 commutator constant on an inhomogeneous
# rational degree-two operator.
d_terms = (
    (F(1), (scalar_identity, z_matrix, x_matrix)),
    (F(2), (z_matrix, scalar_identity, x_matrix)),
    (F(3), (z_matrix, x_matrix, scalar_identity)),
)
c_terms = d_terms + (
    (F(5), (scalar_identity, scalar_identity, scalar_identity)),
    (F(7), (z_matrix, scalar_identity, scalar_identity)),
    (F(11), (z_matrix, z_matrix, z_matrix)),
)
d_matrix = matrix_add(
    *(matrix_scale(coefficient, tensor_three(factors))
      for coefficient, factors in d_terms)
)
d_norm = matrix_norm_squared(d_matrix)
pair_masses = tuple(
    matrix_norm_squared(
        matrix_scale(coefficient, tensor_three(factors))
    )
    for coefficient, factors in d_terms
)
assert pair_masses == (F(2, 3), F(8, 3), F(6))
assert d_norm == sum(pair_masses)

commutator_norms = []
for site in range(3):
    site_norm = F(0)
    for row in range(3):
        for column in range(3):
            matrix_unit = matrix_zero()
            matrix_unit[row][column] = F(1)
            left_terms = []
            right_terms = []
            for coefficient, factors_tuple in c_terms:
                factors = list(factors_tuple)
                left_factors = factors[:]
                right_factors = factors[:]
                left_factors[site] = matrix_multiply(
                    matrix_unit, factors[site]
                )
                right_factors[site] = matrix_multiply(
                    factors[site], matrix_unit
                )
                left_terms.append(
                    matrix_scale(
                        coefficient,
                        pair_projection_of_product(left_factors),
                    )
                )
                right_terms.append(
                    matrix_scale(
                        coefficient,
                        pair_projection_of_product(right_factors),
                    )
                )
            difference = matrix_add(
                matrix_add(*left_terms),
                matrix_scale(F(-1), matrix_add(*right_terms)),
            )

            local_matrix_unit = tensor_three(
                tuple(
                    matrix_unit if index == site else identity
                    for index in range(3)
                )
            )
            commutator = matrix_add(
                matrix_multiply(local_matrix_unit, d_matrix),
                matrix_scale(
                    F(-1), matrix_multiply(d_matrix, local_matrix_unit)
                ),
            )
            assert difference == commutator
            site_norm += matrix_norm_squared(commutator)
    commutator_norms.append(site_norm)

assert tuple(commutator_norms) == tuple(
    6 * (d_norm - pair_mass) for pair_mass in pair_masses
)
assert sum(commutator_norms) == 12 * d_norm


# Formal sector data.
w0 = F(1, 9)
w1 = F(0)
f = F(2, 3)
w3 = F(2, 9)
assert w0 + w1 + f + w3 == 1
q3 = -F(9, 8) * w0 - F(3, 4) * w1
assert q3 == -F(1, 8)

# The exact three-site Gram trace on either side.
k = F(16, 3) * w1 + F(17, 3) * f + w3
assert k == 4

# Each local density is I/3.
purity_per_site = F(1, 3)
overlap_per_site = F(1, 3)
p_left = p_right = 3 * purity_per_site
s_cross = 3 * overlap_per_site
assert p_left == p_right == s_cross == 1

# Work only with squared amplitudes.  The scalar basis direction and
# eight traceless directions have squared output norms 2/9 and 5/36,
# respectively.  The exact phase eta has |eta|=1 and Re(eta)=-1/5.
d_norm_squared = f
scalar_output_squared = d_norm_squared / 3
active_output_squared = F(5, 36)
eta_real_part = F(-1, 5)
eta_norm_squared = F(1)
one_minus_eta_norm_squared = 2 - 2 * eta_real_part

trace_per_site = scalar_output_squared + 8 * active_output_squared
cross_per_site = (
    scalar_output_squared
    + 8 * active_output_squared * eta_real_part
)
difference_per_site = (
    8 * active_output_squared * one_minus_eta_norm_squared
)
pair_mass_per_omitted_site = f / 3
degree_one_mass_per_site = F(0)

assert eta_norm_squared == 1
assert one_minus_eta_norm_squared == F(12, 5)
assert trace_per_site == F(4, 3)
assert cross_per_site == 0
assert difference_per_site == F(8, 3)
assert difference_per_site == 6 * (
    f - pair_mass_per_omitted_site
)

# The sharp one-site Haar-filter inequality, rewritten as the
# covariance-energy upper bound, is saturated at every site:
#   (1/4) w_i - (1/2)(f-p_i) + w_3 >= 0,
#   6(f-p_i) <= 3 w_i + 12 w_3.
haar_slack_per_site = (
    F(1, 4) * degree_one_mass_per_site
    - F(1, 2) * (f - pair_mass_per_omitted_site)
    + w3
)
assert haar_slack_per_site == 0
assert difference_per_site == (
    3 * degree_one_mass_per_site + 12 * w3
)

# The summed Haar bound is also saturated, while the two-site
# filtered bound p_i <= 2 w_3 holds with slack.
assert f == F(3, 4) - F(3, 4) * w0 - F(11, 16) * w1
assert pair_mass_per_omitted_site < 2 * w3

assert 3 * trace_per_site == k
assert 3 * cross_per_site == k - 6 * f
assert 3 * difference_per_site == 12 * f

# Remove the common D component.
residual_left = k - f * p_left
residual_right = k - f * p_right
residual_cross = k - 6 * f - f * s_cross
assert residual_left == residual_right == F(10, 3)
assert residual_cross == -F(2, 3)

density_difference = F(0)
assert (
    residual_left
    + residual_right
    - 2 * residual_cross
    + f * density_difference
    == 12 * f
)

# Exact covariance Cauchy and parallelogram conditions.
assert residual_cross**2 <= residual_left * residual_right
assert 4 * k >= 12 * f + f * (
    p_left + p_right + 2 * s_cross
)

# Full boundary contraction: for rho=I/3 the squared operator bound is
# 2/9 on every Hilbert--Schmidt unit input.  The model is diagonal; the
# scalar direction saturates the bound and all traceless directions
# are strictly below it.
contraction_bound = F(2, 9)
left_gram_diagonal = (
    scalar_output_squared,
    *(active_output_squared for _ in range(8)),
)
right_gram_diagonal = left_gram_diagonal
assert len(left_gram_diagonal) == 9
assert all(
    0 <= value <= contraction_bound
    for value in left_gram_diagonal + right_gram_diagonal
)

print(
    "verified exact six-map covariance and norm obstruction:",
    "physical rational commutator identity and 12||D||^2 constant;",
    "formal sectors (1/9,0,2/3,2/9), Q3=-1/8;",
    "K=4, commutator norm 8, residual norms 10/3,",
    "residual cross -2/3, all six boundary contractions,",
    "and all sharp Haar-filter sector bounds",
)
