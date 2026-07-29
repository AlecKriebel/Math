"""Exact checks for the three-copy exterior/Koszul recouplings.

Only standard-library rational arithmetic is used.  The script verifies
the Pauli-exterior scalar identity through swap moments, the
universal-inversion frame identity, and the two exact transverse zero
stress tests in the accompanying note.
"""

from fractions import Fraction as F
from itertools import combinations, product


def zero_matrix(size: int) -> list[list[F]]:
    return [[F(0) for _ in range(size)] for _ in range(size)]


def matrix_multiply(
    left: list[list[F]], right: list[list[F]]
) -> list[list[F]]:
    size = len(left)
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(size))
            for j in range(size)
        ]
        for i in range(size)
    ]


def matrix_add(
    left: list[list[F]], right: list[list[F]]
) -> list[list[F]]:
    return [
        [left[i][j] + right[i][j] for j in range(len(left))]
        for i in range(len(left))
    ]


def transpose(matrix: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*matrix)]


def words(dims: tuple[int, ...]) -> list[tuple[int, ...]]:
    return list(product(*[range(d) for d in dims]))


def inner(
    left: dict[tuple[int, ...], F],
    right: dict[tuple[int, ...], F],
) -> F:
    return sum(value * right.get(word, F(0)) for word, value in left.items())


def reduced_density(
    vector: dict[tuple[int, ...], F],
    dims: tuple[int, ...],
    kept: tuple[int, ...],
) -> dict[tuple[tuple[int, ...], tuple[int, ...]], F]:
    omitted = tuple(i for i in range(len(dims)) if i not in kept)
    kept_words = words(tuple(dims[i] for i in kept))
    omitted_words = words(tuple(dims[i] for i in omitted))
    out: dict[tuple[tuple[int, ...], tuple[int, ...]], F] = {}
    for row_kept in kept_words:
        for column_kept in kept_words:
            value = F(0)
            for omitted_word in omitted_words:
                row = [0] * len(dims)
                column = [0] * len(dims)
                for site, digit in zip(kept, row_kept):
                    row[site] = digit
                for site, digit in zip(kept, column_kept):
                    column[site] = digit
                for site, digit in zip(omitted, omitted_word):
                    row[site] = digit
                    column[site] = digit
                value += (
                    vector.get(tuple(row), F(0))
                    * vector.get(tuple(column), F(0))
                )
            if value:
                out[row_kept, column_kept] = value
    return out


def matrix_overlap(
    left: dict[tuple[tuple[int, ...], tuple[int, ...]], F],
    right: dict[tuple[tuple[int, ...], tuple[int, ...]], F],
) -> F:
    return sum(
        value * right.get((column, row), F(0))
        for (row, column), value in left.items()
    )


def q(
    left: dict[tuple[int, ...], F],
    right: dict[tuple[int, ...], F],
    dims: tuple[int, ...],
    kept: tuple[int, ...],
) -> F:
    return matrix_overlap(
        reduced_density(left, dims, kept),
        reduced_density(right, dims, kept),
    )


def moment_table(
    left: dict[tuple[int, ...], F],
    right: dict[tuple[int, ...], F],
    dims: tuple[int, ...],
) -> list[F]:
    return [
        q(
            left,
            right,
            dims,
            tuple(i for i in range(len(dims)) if mask >> i & 1),
        )
        for mask in range(1 << len(dims))
    ]


def sector_weights(moments: list[F]) -> dict[tuple[int, ...], F]:
    number_of_parties = (len(moments)).bit_length() - 1
    out: dict[tuple[int, ...], F] = {}
    for parity in product(range(2), repeat=number_of_parties):
        value = F(0)
        for mask, moment in enumerate(moments):
            exponent = sum(
                parity[site]
                for site in range(number_of_parties)
                if mask >> site & 1
            )
            value += (-1) ** exponent * moment
        out[parity] = value / (1 << number_of_parties)
    return out


def m_from_sectors(
    sectors: dict[tuple[int, ...], F], subset: tuple[int, ...]
) -> F:
    return F(2) ** len(subset) * sum(
        value
        for parity, value in sectors.items()
        if all(parity[site] == 1 for site in subset)
    )


def defect_data(
    left: dict[tuple[int, ...], F],
    right: dict[tuple[int, ...], F],
    dims: tuple[int, ...],
) -> dict[str, F]:
    assert len(dims) == 4  # K,1,2,3

    q_k = q(left, right, dims, (0,))
    q_ki = sum(q(left, right, dims, (0, i)) for i in (1, 2, 3))
    q_i = sum(q(left, right, dims, (i,)) for i in (1, 2, 3))
    q_kij = sum(
        q(left, right, dims, (0, i, j))
        for i, j in combinations((1, 2, 3), 2)
    )
    norm_product = inner(left, left) * inner(right, right)
    global_overlap = inner(left, right) ** 2

    d0 = 3 * q_k - 2 * q_ki + q_i
    d = 3 * q_k - 2 * q_ki + q_kij + (norm_product - global_overlap) / 2
    q3 = q_k - q_ki / 2 + q_kij / 4 - global_overlap / 8

    def diagonal_d0(vector: dict[tuple[int, ...], F]) -> F:
        return (
            3 * q(vector, vector, dims, (0,))
            - 2 * sum(q(vector, vector, dims, (0, i)) for i in (1, 2, 3))
            + sum(q(vector, vector, dims, (i,)) for i in (1, 2, 3))
        )

    delta_left = diagonal_d0(left)
    delta_right = diagonal_d0(right)
    x_difference_squared = 2 * d0 - delta_left - delta_right

    sectors = sector_weights(moment_table(left, right, dims))
    exterior_residual = sum(
        (4 * sum(parity[1:]) - 5) * value
        for parity, value in sectors.items()
        if sum(parity) % 2 == 1
    )

    universal_rhs = m_from_sectors(sectors, (0,))
    for size in (1, 2, 3):
        for physical_subset in combinations((1, 2, 3), size):
            universal_rhs += m_from_sectors(sectors, physical_subset)
            universal_rhs -= m_from_sectors(
                sectors, (0,) + physical_subset
            )
    assert universal_rhs == 2 * d

    return {
        "Q3": q3,
        "D": d,
        "D0": d0,
        "delta_left": delta_left,
        "delta_right": delta_right,
        "x_difference_squared": x_difference_squared,
        "exterior_residual": exterior_residual,
        "universal_rhs": universal_rhs,
    }


def odd_even_defects(
    left: dict[tuple[int, ...], F],
    right: dict[tuple[int, ...], F],
    dims: tuple[int, ...],
) -> tuple[F, F]:
    sectors = sector_weights(moment_table(left, right, dims))
    odd = F(0)
    even = F(0)
    for parity, weight in sectors.items():
        k = parity[0]
        r = sum(parity[1:])
        coefficient = F((-1) ** k * (3**r - 2) + 1, 2)
        if (k + r) % 2:
            odd += coefficient * weight
        else:
            even += coefficient * weight
    return odd, even


def eight_q3(
    left: dict[tuple[int, ...], F],
    right: dict[tuple[int, ...], F],
    dims: tuple[int, ...],
) -> F:
    """The exact quadratic form <right,M_Q(P_left)right>."""
    value = 8 * q(left, right, dims, (0,))
    value -= 4 * sum(
        q(left, right, dims, (0, site)) for site in (1, 2, 3)
    )
    value += 2 * sum(
        q(left, right, dims, (0, first, second))
        for first, second in combinations((1, 2, 3), 2)
    )
    value -= q(left, right, dims, (0, 1, 2, 3))
    return value


def coefficient_matrix_from_anchors(
    left: dict[tuple[int, ...], F],
    right: dict[tuple[int, ...], F],
    dims: tuple[int, ...],
) -> dict[tuple[tuple[int, ...], tuple[int, ...]], F]:
    """C=Tr_K |left><right|, with no marginal-matching assumption."""
    physical_words = words(dims[1:])
    out: dict[tuple[tuple[int, ...], tuple[int, ...]], F] = {}
    for row in physical_words:
        for column in physical_words:
            value = sum(
                left.get((k,) + row, F(0))
                * right.get((k,) + column, F(0))
                for k in range(dims[0])
            )
            if value:
                out[row, column] = value
    return out


def coefficient_partial_trace_norm(
    matrix: dict[tuple[tuple[int, ...], tuple[int, ...]], F],
    physical_dims: tuple[int, ...],
    traced: tuple[int, ...],
) -> F:
    remaining = tuple(
        site for site in range(len(physical_dims)) if site not in traced
    )
    remaining_words = words(tuple(physical_dims[site] for site in remaining))
    traced_words = words(tuple(physical_dims[site] for site in traced))
    norm = F(0)
    for row_remaining in remaining_words:
        for column_remaining in remaining_words:
            value = F(0)
            for traced_word in traced_words:
                row = [0] * len(physical_dims)
                column = [0] * len(physical_dims)
                for site, digit in zip(remaining, row_remaining):
                    row[site] = digit
                for site, digit in zip(remaining, column_remaining):
                    column[site] = digit
                for site, digit in zip(traced, traced_word):
                    row[site] = digit
                    column[site] = digit
                value += matrix.get((tuple(row), tuple(column)), F(0))
            norm += value * value
    return norm


def coefficient_q3(
    matrix: dict[tuple[tuple[int, ...], tuple[int, ...]], F],
    physical_dims: tuple[int, ...],
) -> F:
    value = F(0)
    for size in range(4):
        for traced in combinations(range(3), size):
            value += F(-1, 2) ** size * coefficient_partial_trace_norm(
                matrix, physical_dims, traced
            )
    return value


def quadratic_gram_matrix(
    form,
    basis_words: list[tuple[int, ...]],
) -> list[list[F]]:
    """Recover a real symmetric Gram matrix by exact polarization."""
    size = len(basis_words)
    basis = [{word: F(1)} for word in basis_words]
    diagonal = [form(vector) for vector in basis]
    matrix = zero_matrix(size)
    for row in range(size):
        matrix[row][row] = diagonal[row]
        for column in range(row + 1, size):
            pair = {
                basis_words[row]: F(1),
                basis_words[column]: F(1),
            }
            entry = (
                form(pair) - diagonal[row] - diagonal[column]
            ) / 2
            matrix[row][column] = entry
            matrix[column][row] = entry
    return matrix


def exact_ldl(matrix: list[list[F]]) -> tuple[list[list[F]], list[F]]:
    """Exact unpivoted LDL^T decomposition of a symmetric matrix."""
    size = len(matrix)
    lower = zero_matrix(size)
    pivots = [F(0)] * size
    for row in range(size):
        lower[row][row] = F(1)
        pivots[row] = matrix[row][row] - sum(
            lower[row][k] ** 2 * pivots[k] for k in range(row)
        )
        assert pivots[row] != 0
        for next_row in range(row + 1, size):
            lower[next_row][row] = (
                matrix[next_row][row]
                - sum(
                    lower[next_row][k] * lower[row][k] * pivots[k]
                    for k in range(row)
                )
            ) / pivots[row]

    # Independently reconstruct every entry.
    for row in range(size):
        for column in range(size):
            assert matrix[row][column] == sum(
                lower[row][k] * pivots[k] * lower[column][k]
                for k in range(size)
            )
    return lower, pivots


# First-principles qutrit matrix-unit check of
# R(X)=sum_{a<b} A_ab X^T A_ab^dagger.
for row_index in range(3):
    for column_index in range(3):
        matrix_unit = zero_matrix(3)
        matrix_unit[row_index][column_index] = F(1)
        kraus_sum = zero_matrix(3)
        for a, b in combinations(range(3), 2):
            skew = zero_matrix(3)
            skew[a][b] = F(1)
            skew[b][a] = F(-1)
            term = matrix_multiply(
                matrix_multiply(skew, transpose(matrix_unit)),
                transpose(skew),
            )
            kraus_sum = matrix_add(kraus_sum, term)
        reduction = zero_matrix(3)
        if row_index == column_index:
            for diagonal in range(3):
                reduction[diagonal][diagonal] = F(1)
        reduction[row_index][column_index] -= F(1)
        assert kraus_sum == reduction


# Coefficient audit of the Mobius identity (40).  A monomial containing
# K occurs once.  A physical monomial of size r occurs 2^r-1 times.
for contains_k in (False, True):
    for physical_size in range(4):
        number_of_nonempty_subsets = 2**physical_size - 1
        right_coefficient = F(1) if contains_k else F(0)  # M_K
        right_coefficient += number_of_nonempty_subsets
        if contains_k:
            right_coefficient -= number_of_nonempty_subsets

        # R_glob supplies every nonempty local-reduction monomial once.
        left_coefficient = F(1) if contains_k or physical_size else F(0)
        if not contains_k and physical_size == 2:
            left_coefficient += 2  # 2 sum_{i<j} R_i R_j
        if not contains_k and physical_size == 3:
            left_coefficient += 6  # 6 R_1 R_2 R_3
        assert right_coefficient == left_coefficient


# The unshifted 8-versus-8 cube does not require equal K marginals.
# This deliberately unbalanced pair gives a rank-at-most-two coefficient
# matrix as a sum of two dyads.  Direct coefficient-matrix contraction
# agrees with the anchor quadratic form exactly.
unmatched_dims = (2, 2, 2, 2)
unmatched_a = {
    (0, 0, 0, 0): F(1),
    (1, 1, 1, 1): F(2),
}
unmatched_b = {
    (0, 0, 0, 1): F(1),
    (0, 0, 1, 0): F(3),
    (1, 1, 0, 0): F(5),
}
assert (
    sum(value * value for word, value in unmatched_a.items() if word[0] == 0),
    sum(value * value for word, value in unmatched_a.items() if word[0] == 1),
) == (F(1), F(4))
assert (
    sum(value * value for word, value in unmatched_b.items() if word[0] == 0),
    sum(value * value for word, value in unmatched_b.items() if word[0] == 1),
) == (F(10), F(25))
unmatched_c = coefficient_matrix_from_anchors(
    unmatched_a, unmatched_b, unmatched_dims
)
assert eight_q3(unmatched_a, unmatched_b, unmatched_dims) == (
    8 * coefficient_q3(unmatched_c, unmatched_dims[1:])
)


# The normalized transverse spin-flip boundary from
# agent_n3_transverse_anchor_boundary.md.
dims_boundary = (2, 2, 2, 2)
boundary_a: dict[tuple[int, ...], F] = {}
boundary_b: dict[tuple[int, ...], F] = {}
for word, value in (
    ((0, 0, 0, 0), 1),
    ((0, 0, 1, 1), 1),
    ((1, 1, 0, 0), 1),
    ((1, 1, 1, 1), -1),
):
    boundary_a[word] = F(value, 2)
for word, value in (
    ((0, 0, 0, 0), -1),
    ((0, 0, 1, 1), 1),
    ((1, 1, 0, 0), 1),
    ((1, 1, 1, 1), 1),
):
    boundary_b[word] = F(value, 2)

boundary = defect_data(boundary_a, boundary_b, dims_boundary)
assert boundary == {
    "Q3": F(0),
    "D": F(0),
    "D0": F(1),
    "delta_left": F(1),
    "delta_right": F(1),
    "x_difference_squared": F(0),
    "exterior_residual": F(-1),
    "universal_rhs": F(0),
}


# An unnormalized matched purification of
# P_2 tensor |0><1| tensor |0><0|.  All coefficients are integral.
dims_nilpotent = (2, 2, 2, 2)
nilpotent_a = {
    (0, 0, 0, 0): F(1),
    (1, 1, 0, 0): F(1),
}
nilpotent_b = {
    (0, 0, 1, 0): F(1),
    (1, 1, 1, 0): F(1),
}

nilpotent = defect_data(nilpotent_a, nilpotent_b, dims_nilpotent)
assert nilpotent == {
    "Q3": F(0),
    "D": F(0),
    "D0": F(0),
    "delta_left": F(0),
    "delta_right": F(0),
    "x_difference_squared": F(0),
    "exterior_residual": F(0),
    "universal_rhs": F(0),
}


# A non-equal-singular-value product equality.  The matched purification
# has Schmidt weights 1 and 4, so its amplitudes 1 and 2 are rational.
weighted_a = {
    (0, 0, 0, 0): F(1),
    (1, 1, 0, 0): F(2),
}
weighted = defect_data(weighted_a, weighted_a, (2, 2, 2, 2))
assert weighted["Q3"] == F(9, 8)
assert weighted["D"] == F(0)
assert 2 * weighted["D"] == 8 * weighted["Q3"] - (F(4) - F(1)) ** 2


# The phase-average formula isolates the even-total-parity bracket.  The
# tempting conditional completion
#
#   D_even < 0 => D_odd >= (delta_A+delta_B)/4
#
# is nevertheless false.  This rational perturbation of the transverse
# spin-flip boundary has equal K marginals 2 I_2.  Its first left singular
# vector is rotated through the Pythagorean pair (3/5,4/5).
conditional_a = {
    (0, 0, 0, 0): F(3, 5),
    (0, 0, 1, 1): F(3, 5),
    (0, 0, 0, 1): F(4, 5),
    (0, 0, 1, 0): F(4, 5),
    (1, 1, 0, 0): F(1),
    (1, 1, 1, 1): F(-1),
}
conditional_b = {
    (0, 0, 0, 0): F(-1),
    (0, 0, 1, 1): F(1),
    (1, 1, 0, 0): F(1),
    (1, 1, 1, 1): F(1),
}
conditional = defect_data(conditional_a, conditional_b, dims_boundary)
conditional_odd, conditional_even = odd_even_defects(
    conditional_a, conditional_b, dims_boundary
)
assert conditional["delta_left"] == F(7696, 625)
assert conditional["delta_right"] == F(16)
assert conditional_odd == F(176, 25)
assert conditional_even == F(-96, 25)
assert conditional_odd + conditional_even == conditional["D"] == F(16, 5)
assert conditional_even < 0
assert (
    conditional_odd
    - (conditional["delta_left"] + conditional["delta_right"]) / 4
    == F(-24, 625)
)


# Exact coefficient audit for the odd-parity anchor.  In the commuting
# local-reduction variables R_j=E_j-id, its nonzero monomials have
# coefficient 1/2 on every singleton and pair, coefficient 2 on the
# physical triple, and coefficient 1/2 on the four-party monomial.
odd_q_coefficients: list[F] = []
for traced_mask in range(16):
    coefficient = F(0)
    for sector_mask in range(16):
        k = sector_mask & 1
        r = bin(sector_mask >> 1).count("1")
        target = (
            F((-1) ** k * (3**r - 2) + 1, 2)
            if (k + r) % 2
            else F(0)
        )
        coefficient += (
            (-1) ** bin(sector_mask & traced_mask).count("1") * target
        )
    odd_q_coefficients.append(coefficient / 16)

odd_reduction_coefficients = []
for reduction_mask in range(16):
    coefficient = F(0)
    for e_mask in range(16):
        if e_mask & reduction_mask == reduction_mask:
            # q_T is the expectation of E_{T^c}(P).
            coefficient += odd_q_coefficients[(~e_mask) & 15]
    odd_reduction_coefficients.append(coefficient)

expected_odd_reduction_coefficients = [F(0)] * 16
for mask in range(1, 16):
    if bin(mask).count("1") in (1, 2) or mask == 15:
        expected_odd_reduction_coefficients[mask] = F(1, 2)
expected_odd_reduction_coefficients[0b1110] = F(2)
for mask in (0b0111, 0b1011, 0b1101):
    expected_odd_reduction_coefficients[mask] = F(0)
assert odd_reduction_coefficients == expected_odd_reduction_coefficients


# The separated odd anchor is not positive.  This sparse integral pair
# embeds in K=2 and three qutrit physical spaces; its third physical
# coordinate is fixed at zero.
odd_failure_dims = (2, 3, 3, 3)
odd_failure_a = {
    (0, 0, 0, 0): F(-1),
    (0, 1, 2, 0): F(1),
    (0, 2, 1, 0): F(-1),
    (1, 1, 2, 0): F(1),
}
odd_failure_b = {
    (1, 0, 0, 0): F(1),
    (1, 1, 2, 0): F(-1),
    (1, 2, 1, 0): F(1),
}
odd_failure_odd, odd_failure_even = odd_even_defects(
    odd_failure_a, odd_failure_b, odd_failure_dims
)
odd_failure = defect_data(
    odd_failure_a, odd_failure_b, odd_failure_dims
)
assert odd_failure_odd == F(-1, 2)
assert odd_failure_even == F(8)
assert odd_failure["D"] == F(15, 2)
assert odd_failure["Q3"] == F(9, 8)

# This negative odd bracket is not a negative direction of the complete
# Q3 anchor.  Delete the spectator qutrit, construct M_Q exactly by
# polarization, and certify positive definiteness by rational LDL^T.
# Restoring the spectator tensors this matrix with
# 2 I_3 - |0><0|, which is also positive definite.
odd_failure_base_dims = (2, 3, 3, 1)
odd_failure_base_a = {
    word: coefficient
    for word, coefficient in odd_failure_a.items()
}
base_words = words(odd_failure_base_dims)
mq_matrix = quadratic_gram_matrix(
    lambda vector: eight_q3(
        odd_failure_base_a, vector, odd_failure_base_dims
    ),
    base_words,
)
_, mq_pivots = exact_ldl(mq_matrix)
assert mq_pivots == [
    F(9),
    F(8),
    F(8),
    F(8),
    F(8),
    F(80, 9),
    F(8),
    F(44, 5),
    F(8),
    F(24, 11),
    F(2),
    F(3, 2),
    F(3, 2),
    F(3, 2),
    F(2, 3),
    F(2),
    F(2),
    F(3, 2),
]
assert all(pivot > 0 for pivot in mq_pivots)


# Exact 8-versus-8 Koszul-cube obstruction.  A contraction which routes
# every K union S exterior frame only to the frame with the same S is
# impossible: the spin-flip and nilpotent equality vectors require
# transfers between different cube vertices.
boundary_sectors = sector_weights(
    moment_table(boundary_a, boundary_b, dims_boundary)
)
boundary_cube = {}
for physical_mask in range(8):
    subset = tuple(
        site + 1 for site in range(3) if physical_mask >> site & 1
    )
    boundary_cube[subset] = (
        m_from_sectors(boundary_sectors, subset),
        m_from_sectors(boundary_sectors, (0,) + subset),
    )
assert boundary_cube[(1, 2, 3)] == (F(1, 2), F(1))
assert sum(
    non_k - with_k for non_k, with_k in boundary_cube.values()
) == F(0)

# No convex mixture of the four odd cube translations, fixed by the
# spin-flip anchor, can dominate every input vertexwise.  On the kernel
# vector, equality of the total row sums forces equality at every vertex.
# The S={2},{3} equations have the following exact coefficient rows after
# subtracting one quarter of the normalization equation:
odd_translation_masks = (0b001, 0b010, 0b100, 0b111)
boundary_non_k = []
boundary_with_k = []
for physical_mask in range(8):
    subset = tuple(
        site + 1 for site in range(3) if physical_mask >> site & 1
    )
    boundary_non_k.append(boundary_cube[subset][0])
    boundary_with_k.append(boundary_cube[subset][1])
assert [
    boundary_non_k[0b010 ^ translation] - F(1, 4)
    for translation in odd_translation_masks
] == [F(0), F(3, 4), F(1, 4), F(0)]
assert [
    boundary_non_k[0b100 ^ translation] - F(1, 4)
    for translation in odd_translation_masks
] == [F(0), F(1, 4), F(3, 4), F(0)]
# Nonnegative weights therefore have lambda_2=lambda_3=0.  The 123
# equation and normalization then uniquely give lambda_1=0, lambda_123=1.
assert [
    boundary_non_k[0b111 ^ translation]
    for translation in odd_translation_masks
] == [F(1, 2), F(1, 4), F(1, 4), F(1)]
assert boundary_with_k[0b111] == F(1)

# Pure complement routing fails for a second input with the same anchor.
boundary_basis_b = {(0, 0, 0, 0): F(1)}
boundary_basis_sectors = sector_weights(
    moment_table(boundary_a, boundary_basis_b, dims_boundary)
)
boundary_basis_m_empty = m_from_sectors(boundary_basis_sectors, ())
boundary_basis_m_all = m_from_sectors(
    boundary_basis_sectors, (1, 2, 3)
)
boundary_basis_m_k = m_from_sectors(boundary_basis_sectors, (0,))
assert (
    boundary_basis_m_empty,
    boundary_basis_m_all,
    boundary_basis_m_k,
) == (F(1), F(1, 4), F(1, 2))
assert boundary_basis_m_k > boundary_basis_m_all

nilpotent_sectors = sector_weights(
    moment_table(nilpotent_a, nilpotent_b, dims_nilpotent)
)
nilpotent_cube = {}
for physical_mask in range(8):
    subset = tuple(
        site + 1 for site in range(3) if physical_mask >> site & 1
    )
    nilpotent_cube[subset] = (
        m_from_sectors(nilpotent_sectors, subset),
        m_from_sectors(nilpotent_sectors, (0,) + subset),
    )
assert nilpotent_cube[(1,)] == (F(2), F(4))
assert nilpotent_cube[(1, 2)] == (F(2), F(4))
assert sum(
    non_k - with_k for non_k, with_k in nilpotent_cube.values()
) == F(0)


# Removing the physical commutation hypothesis from the five-gamma flag
# lemma loses an exact factor two.  Here A=Phi+_{K1}|00> and
# B=Phi-_{K1}|00>, both unnormalized.  With transition observable Z_1
# and diagonal observable X_1, the two flag-Clifford expectations are
# both T=2, although the physical observables anticommute.
bell_plus = {
    (0, 0, 0, 0): F(1),
    (1, 1, 0, 0): F(1),
}
bell_minus = {
    (0, 0, 0, 0): F(1),
    (1, 1, 0, 0): F(-1),
}


def apply_paulis(
    vector: dict[tuple[int, ...], F],
    x_sites: tuple[int, ...] = (),
    z_sites: tuple[int, ...] = (),
) -> dict[tuple[int, ...], F]:
    out: dict[tuple[int, ...], F] = {}
    for word, value in vector.items():
        image = list(word)
        phase = F(1)
        for site in z_sites:
            if image[site]:
                phase *= -1
        for site in x_sites:
            image[site] ^= 1
        out[tuple(image)] = out.get(tuple(image), F(0)) + phase * value
    return out


transition_expectation = inner(
    bell_plus, apply_paulis(bell_minus, z_sites=(1,))
)
diagonal_difference = inner(
    bell_plus, apply_paulis(bell_plus, x_sites=(0, 1))
) - inner(
    bell_minus, apply_paulis(bell_minus, x_sites=(0, 1))
)
bell_trace = inner(bell_plus, bell_plus)
assert bell_trace == inner(bell_minus, bell_minus) == F(2)
assert transition_expectation == F(2)
assert diagonal_difference / 2 == F(2)
assert (
    transition_expectation**2 + (diagonal_difference / 2) ** 2
    == 2 * bell_trace**2
)


# Exact factor-two obstruction to routing the logical skew through only
# the trace channel.  The Fierz coefficient metric on three real local
# matrix factors is W=2^-3 product_i(2I-T_i).
SparseMatrix = dict[tuple[tuple[int, ...], tuple[int, ...]], F]


def sparse_matrix_linear_combination(
    left: SparseMatrix,
    right: SparseMatrix,
    left_scale: F = F(1),
    right_scale: F = F(1),
) -> SparseMatrix:
    out: SparseMatrix = {}
    for entry in set(left) | set(right):
        coefficient = (
            left_scale * left.get(entry, F(0))
            + right_scale * right.get(entry, F(0))
        )
        if coefficient:
            out[entry] = coefficient
    return out


def local_matrix_transpose(matrix: SparseMatrix, site: int) -> SparseMatrix:
    out: SparseMatrix = {}
    for (row, column), coefficient in matrix.items():
        new_row = list(row)
        new_column = list(column)
        new_row[site], new_column[site] = (
            new_column[site],
            new_row[site],
        )
        entry = (tuple(new_row), tuple(new_column))
        out[entry] = out.get(entry, F(0)) + coefficient
    return out


def sparse_matrix_inner(left: SparseMatrix, right: SparseMatrix) -> F:
    return sum(
        coefficient * right.get(entry, F(0))
        for entry, coefficient in left.items()
    )


def fierz_weighted_norm_squared(matrix: SparseMatrix) -> F:
    image = matrix
    for site in range(3):
        image = sparse_matrix_linear_combination(
            image,
            local_matrix_transpose(image, site),
            F(2),
            F(-1),
        )
    return sparse_matrix_inner(matrix, image) / 8


trace_only_x: SparseMatrix = {
    ((0, 0, 0), (0, 0, 0)): F(1),
}
# For U=(|000>,(3|001>+4|010>)/5), the physical logical skew J obeys
# X J^T=-|000><v|.
trace_only_xj: SparseMatrix = {
    ((0, 0, 0), (0, 0, 1)): F(-3, 5),
    ((0, 0, 0), (0, 1, 0)): F(-4, 5),
}
assert fierz_weighted_norm_squared(trace_only_x) == F(1, 8)
assert fierz_weighted_norm_squared(trace_only_xj) == F(1, 4)


# Exact coefficient audit for the complex logical-quaternion reduction.
# Linearity reduces the Pauli twirl and qubit reduction/partial-transpose
# identity to the four rational 2-by-2 matrix units.
logical_identity = [[F(1), F(0)], [F(0), F(1)]]
logical_x = [[F(0), F(1)], [F(1), F(0)]]
logical_z = [[F(1), F(0)], [F(0), F(-1)]]
logical_epsilon = [[F(0), F(1)], [F(-1), F(0)]]
logical_frame = (
    logical_identity,
    logical_x,
    logical_z,
    logical_epsilon,
)

for row in range(2):
    for column in range(2):
        matrix_unit = zero_matrix(2)
        matrix_unit[row][column] = F(1)

        twirl = zero_matrix(2)
        for tau in logical_frame:
            twirl = matrix_add(
                twirl,
                matrix_multiply(
                    transpose(tau),
                    matrix_multiply(matrix_unit, tau),
                ),
            )
        expected_twirl = [
            [
                F(2) if row == column and i == j else F(0)
                for j in range(2)
            ]
            for i in range(2)
        ]
        assert twirl == expected_twirl

        reduction = [
            [
                (F(1) if row == column and i == j else F(0))
                - matrix_unit[i][j]
                for j in range(2)
            ]
            for i in range(2)
        ]
        epsilon_partial_transpose = matrix_multiply(
            logical_epsilon,
            matrix_multiply(
                transpose(matrix_unit),
                transpose(logical_epsilon),
            ),
        )
        assert reduction == epsilon_partial_transpose


print(
    "verified: Pauli/exterior and universal-inversion recouplings; "
    "spin-flip boundary (1-1=0); nilpotent boundary (all terms zero); "
    "weighted sharp relation; exact conditional-phase, odd-anchor, and "
    "noncommuting-Clifford obstructions; convex cube-translation no-go; "
    "full Q-anchor stays positive; trace-only logical-skew recoupling "
    "loses exact factor two; complex logical Pauli twirl reduces the "
    "frontier exactly to a two-by-two PPT Gram block"
)
