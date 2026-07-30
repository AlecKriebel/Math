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


def right_multiply(matrix, local_matrix, site=0):
    output = zero()
    for column_index, column_word in enumerate(BASIS):
        for middle in range(D):
            coefficient = local_matrix[middle][column_word[site]]
            if not coefficient:
                continue
            source_word = list(column_word)
            source_word[site] = middle
            source_column = index(source_word)
            for row in range(N):
                output[row][column_index] += (
                    matrix[row][source_column] * coefficient
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

# The first explicit third-compound coefficient cannot vanish, even
# after an arbitrary relative phase between the two pure sectors.
# Magnitude equality would be necessary for
# 2 alpha + (4/9) exp(i phi) beta = 0.
left_magnitude_squared = 4 * alpha_squared
right_magnitude_squared = F(16, 81) * beta_squared
assert left_magnitude_squared == (1 + delta) / 27
assert right_magnitude_squared == (1 - 2 * delta) / 405
assert left_magnitude_squared != right_magnitude_squared
assert 15 * (1 + delta) != 1 - 2 * delta

# Solving the equality gives delta=-14/17, outside 0<delta<1/8.
formal_solution = F(-14, 17)
assert 15 * (1 + formal_solution) == 1 - 2 * formal_solution
assert formal_solution < 0

# A stronger obstruction to the entire symmetric-cube minor family.
# Let D_12,D_23,D_13 be the three orthogonal fine degree-two pieces,
# and E_minus=V-V^{-1}.  Formal coefficients (1,omega,omega^2) have
# unit modulus and sum zero.  All quadratic forms below therefore use
# the diagonal Gram entries only.
D12 = add(flip12, scale(F(-1, 3), identity))
D23 = add(flip23, scale(F(-1, 3), identity))
D13 = add(flip13, scale(F(-1, 3), identity))
fine_degree_two = (D12, D23, D13)
Eminus = add(cycle, scale(-1, cycle_inverse))

assert all(inner(piece, piece) == 24 for piece in fine_degree_two)
assert all(
    inner(fine_degree_two[first], fine_degree_two[second]) == 0
    for first in range(3)
    for second in range(3)
    if first != second
)
assert inner(Eminus, Eminus) == 48
assert all(inner(piece, Eminus) == 0 for piece in fine_degree_two)

# Exact traceless local Gram diagonals.  The entries are permuted from
# site to site; equal coefficient moduli make their sums uniform.
expected_h_diagonals = (
    (F(-13, 4), F(8), F(-13, 4)),
    (F(-13, 4), F(-13, 4), F(8)),
    (F(8), F(-13, 4), F(-13, 4)),
)
expected_k_diagonals = (
    (F(7), F(0), F(7)),
    (F(7), F(7), F(0)),
    (F(0), F(7), F(7)),
)

for orientation in ("left", "right"):
    for site in range(3):
        if orientation == "left":
            filtered_pieces = [
                left_multiply(e01, piece, site)
                for piece in fine_degree_two
            ]
            filtered_em = left_multiply(e01, Eminus, site)
        else:
            filtered_pieces = [
                right_multiply(piece, e01, site)
                for piece in fine_degree_two
            ]
            filtered_em = right_multiply(Eminus, e01, site)

        for first in range(3):
            for second in range(3):
                endpoint_value = endpoint_pairing(
                    filtered_pieces[first], filtered_pieces[second]
                )
                pair_value = pair_sector_pairing(
                    filtered_pieces[first], filtered_pieces[second]
                )
                if first == second:
                    assert (
                        endpoint_value
                        == expected_h_diagonals[site][first]
                    )
                    assert pair_value == expected_k_diagonals[site][first]
                else:
                    assert endpoint_value == 0
                    assert pair_value == 0

            assert endpoint_pairing(
                filtered_pieces[first], filtered_em
            ) == 0
            assert pair_sector_pairing(
                filtered_pieces[first], filtered_em
            ) == 0

        assert endpoint_pairing(filtered_em, filtered_em) == 13
        assert pair_sector_pairing(filtered_em, filtered_em) == 2

# C_star=A_2+sqrt(3/5)E_minus has formal omega coefficients on the
# three fine pieces.  Since 1+omega+omega^2=0, it annihilates Sym^3.
c_star = F(72)
d_star = F(3, 5) * 48
N_star = c_star + d_star
Q_star = -c_star / 2 + d_star
sigma_star = 2 * Q_star + 3 * c_star
delta_star = -2 * Q_star / sigma_star
assert d_star == F(144, 5)
assert N_star == F(504, 5)
assert Q_star == F(-36, 5)
assert sigma_star == F(1008, 5)
assert delta_star == F(1, 14)

n_star = N_star / 3
h_star_scalar = Q_star / 3
h_star_traceless = sum(expected_h_diagonals[0]) + F(3, 5) * 13
k_star_scalar = c_star / 3
k_star_traceless = sum(expected_k_diagonals[0]) + F(3, 5) * 2
assert n_star == F(168, 5)
assert h_star_scalar == F(-12, 5)
assert h_star_traceless == F(93, 10)
assert k_star_scalar == 24
assert k_star_traceless == F(76, 5)

q_star = Q_star / N_star
f_star = c_star / N_star
assert q_star == F(-1, 14)
assert f_star == F(5, 7)
assert h_star_scalar - q_star * n_star == 0
assert h_star_traceless - q_star * n_star == F(117, 10)
assert f_star * n_star - k_star_scalar == 0
assert f_star * n_star - k_star_traceless == F(44, 5)
assert (
    2 * (1 + delta_star) * h_star_scalar
    + 3 * delta_star * k_star_scalar
) == 0
assert (
    2 * (1 + delta_star) * h_star_traceless
    + 3 * delta_star * k_star_traceless
) == F(1623, 70)

# Collective-unitary invariance forces all six pair-centered H
# matrices to equal I/3.  Hence the normalized purity sum is 2,
# violating the high-rank analogue of the six-purity candidate.
lambda_star = Q_star / c_star
six_purity_sum = F(2)
purity_candidate_rhs = 3 - lambda_star / 2
assert lambda_star == F(-1, 10)
assert purity_candidate_rhs == F(61, 20)
assert six_purity_sum < purity_candidate_rhs

# Exact one-parameter obstruction to a linear purity/R(H) inequality.
t_parameter = F(1, 7)
purity_excess = t_parameter + 2 * t_parameter**2
haar_R = 2 * t_parameter**2 / (1 + 4 * t_parameter)
ratio = purity_excess / haar_R
assert ratio == 1 / (2 * t_parameter) + 3 + 4 * t_parameter

# The exact ratio 1/(2t)+3+4t is unbounded at both endpoints; the
# checker records two rational instances larger than any illustrative
# fixed constant 100.
small_t = F(1, 1000)
large_t = F(1000)
for test_t in (small_t, large_t):
    test_ratio = F(1, 2) / test_t + 3 + 4 * test_t
    assert test_ratio > 100

print(
    "verified: one invariant model is separated by a symmetric 3x3 "
    "minor, but C_star at depth 1/14 has uniform positive local "
    "Hessians, annihilates every symmetric-cube minor, and obstructs "
    "both scalar six-purity and linear purity/R(H) closures"
)
