#!/usr/bin/env python3
"""Dependency-free exact checks for the logical Bell-normal reduction."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations, product

G = tuple[F, F]
ZERO: G = (F(0), F(0))
ONE: G = (F(1), F(0))


def g(real: int | F = 0, imag: int | F = 0) -> G:
    return (F(real), F(imag))


def add(x: G, y: G) -> G:
    return (x[0] + y[0], x[1] + y[1])


def neg(x: G) -> G:
    return (-x[0], -x[1])


def mul(x: G, y: G) -> G:
    return (
        x[0] * y[0] - x[1] * y[1],
        x[0] * y[1] + x[1] * y[0],
    )


def conj(x: G) -> G:
    return (x[0], -x[1])


def sum_g(values) -> G:
    result = ZERO
    for value in values:
        result = add(result, value)
    return result


def product_g(values) -> G:
    result = ONE
    for value in values:
        result = mul(result, value)
    return result


def matrix_add(*matrices: list[list[G]]) -> list[list[G]]:
    return [
        [sum_g(matrix[i][j] for matrix in matrices)
         for j in range(len(matrices[0][0]))]
        for i in range(len(matrices[0]))
    ]


def matrix_scale(value: G, matrix: list[list[G]]) -> list[list[G]]:
    return [[mul(value, entry) for entry in row] for row in matrix]


def matrix_multiply(
    left: list[list[G]], right: list[list[G]]
) -> list[list[G]]:
    return [
        [
            sum_g(
                mul(left[i][k], right[k][j])
                for k in range(len(right))
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def dagger(matrix: list[list[G]]) -> list[list[G]]:
    return [
        [conj(matrix[j][i]) for j in range(len(matrix))]
        for i in range(len(matrix[0]))
    ]


def kronecker(
    left: list[list[G]], right: list[list[G]]
) -> list[list[G]]:
    return [
        [
            mul(
                left[i // len(right)][j // len(right[0])],
                right[i % len(right)][j % len(right[0])],
            )
            for j in range(len(left[0]) * len(right[0]))
        ]
        for i in range(len(left) * len(right))
    ]


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix: list[list[G]]) -> G:
    size = len(matrix)
    terms = []
    for permutation in permutations(range(size)):
        term = product_g(
            matrix[i][permutation[i]] for i in range(size)
        )
        terms.append(term if permutation_sign(permutation) == 1 else neg(term))
    return sum_g(terms)


def partial_transpose_second(matrix: list[list[G]]) -> list[list[G]]:
    """Partial transpose in the second factor of a 2 x 2 system."""
    result = [[ZERO for _ in range(4)] for _ in range(4)]
    for a, b, c, d in product(range(2), repeat=4):
        result[2 * a + d][2 * c + b] = matrix[2 * a + b][2 * c + d]
    return result


def partial_transpose_first(matrix: list[list[G]]) -> list[list[G]]:
    """Partial transpose in the first factor of a 2 x 2 system."""
    result = [[ZERO for _ in range(4)] for _ in range(4)]
    for a, b, c, d in product(range(2), repeat=4):
        result[2 * c + b][2 * a + d] = matrix[2 * a + b][2 * c + d]
    return result


def bell_operator(t1: F, t2: F, t3: F) -> list[list[G]]:
    identity = [[ONE, ZERO], [ZERO, ONE]]
    pauli_x = [[ZERO, ONE], [ONE, ZERO]]
    pauli_y = [[ZERO, g(0, -1)], [g(0, 1), ZERO]]
    pauli_z = [[ONE, ZERO], [ZERO, neg(ONE)]]
    return matrix_scale(
        g(F(1, 4)),
        matrix_add(
            kronecker(identity, identity),
            matrix_scale(g(t1), kronecker(pauli_x, pauli_x)),
            matrix_scale(g(t2), kronecker(pauli_y, pauli_y)),
            matrix_scale(g(t3), kronecker(pauli_z, pauli_z)),
        ),
    )


def transpose(matrix: list[list[G]]) -> list[list[G]]:
    return [
        [matrix[j][i] for j in range(len(matrix))]
        for i in range(len(matrix[0]))
    ]


def choi_from_scalar_spatial_transfer(
    scalar: F, spatial: list[list[F]]
) -> list[list[G]]:
    """Build J = sum T_{mu,nu} e_nu^T tensor e_mu."""
    paulis = [
        [[ONE, ZERO], [ZERO, ONE]],
        [[ZERO, ONE], [ONE, ZERO]],
        [[ZERO, g(0, -1)], [g(0, 1), ZERO]],
        [[ONE, ZERO], [ZERO, neg(ONE)]],
    ]
    result = matrix_scale(
        g(F(scalar, 2)), kronecker(paulis[0], paulis[0])
    )
    for row in range(3):
        for column in range(3):
            result = matrix_add(
                result,
                matrix_scale(
                    g(spatial[row][column] / 2),
                    kronecker(
                        transpose(paulis[column + 1]), paulis[row + 1]
                    ),
                ),
            )
    return result


def choi_from_transfer(transfer: list[list[F]]) -> list[list[G]]:
    """Build J = sum T_{mu,nu} e_nu^T tensor e_mu."""
    paulis = [
        [[ONE, ZERO], [ZERO, ONE]],
        [[ZERO, ONE], [ONE, ZERO]],
        [[ZERO, g(0, -1)], [g(0, 1), ZERO]],
        [[ONE, ZERO], [ZERO, neg(ONE)]],
    ]
    result = [[ZERO for _ in range(4)] for _ in range(4)]
    for row in range(4):
        for column in range(4):
            result = matrix_add(
                result,
                matrix_scale(
                    g(transfer[row][column] / 2),
                    kronecker(
                        transpose(paulis[column]), paulis[row]
                    ),
                ),
            )
    return result


def matrix_vector(
    matrix: list[list[G]], vector: list[G]
) -> list[G]:
    return [
        sum_g(mul(matrix[i][j], vector[j]) for j in range(len(vector)))
        for i in range(len(matrix))
    ]


def inverse2(matrix: list[list[G]]) -> list[list[G]]:
    determinant_value = add(
        mul(matrix[0][0], matrix[1][1]),
        neg(mul(matrix[0][1], matrix[1][0])),
    )
    denominator = (
        determinant_value[0] ** 2 + determinant_value[1] ** 2
    )
    reciprocal = (
        determinant_value[0] / denominator,
        -determinant_value[1] / denominator,
    )
    return [
        [mul(reciprocal, matrix[1][1]),
         mul(reciprocal, neg(matrix[0][1]))],
        [mul(reciprocal, neg(matrix[1][0])),
         mul(reciprocal, matrix[0][0])],
    ]


def singlet_expectation(matrix: list[list[G]]) -> G:
    """Expectation on (|01>-|10>)/sqrt(2), without square roots."""
    return mul(
        g(F(1, 2)),
        add(
            add(matrix[1][1], matrix[2][2]),
            neg(add(matrix[1][2], matrix[2][1])),
        ),
    )


def sign_values(t1: F, t2: F, t3: F, sign_product: int) -> list[F]:
    return [
        F(1) + e1 * t1 + e2 * t2 + e3 * t3
        for e1, e2, e3 in product((-1, 1), repeat=3)
        if e1 * e2 * e3 == sign_product
    ]


# A strict rational PPT point checks every determinant formula.
t1, t2, t3 = F(1, 5), F(-1, 4), F(1, 6)
k = bell_operator(t1, t2, t3)
k_partial_transpose = partial_transpose_second(k)
ordinary_factors = sign_values(t1, t2, t3, -1)
partial_transpose_factors = sign_values(t1, t2, t3, 1)
assert determinant(k) == mul(
    g(F(1, 4**4)), product_g(g(value) for value in ordinary_factors)
)
assert determinant(k_partial_transpose) == g(
    product_g(g(value) for value in partial_transpose_factors)[0] / 4**4
)
det_transfer = -t1 * t2 * t3 / 16
assert determinant(k_partial_transpose) == add(
    determinant(k), g(-det_transfer)
)

# The eight Bell inequalities are exactly the trace-norm octahedron.
all_factors = ordinary_factors + partial_transpose_factors
assert min(all_factors) == F(1) - abs(t1) - abs(t2) - abs(t3)
spatial_nuclear_norm = (abs(t1) + abs(t2) + abs(t3)) / 2
assert spatial_nuclear_norm <= F(1, 2)

# Positivity of K alone is strictly weaker: this Bell-diagonal point is NPT.
u1, u2, u3 = F(1, 2), F(-1, 2), F(1, 2)
assert min(sign_values(u1, u2, u3, -1)) > 0
assert min(sign_values(u1, u2, u3, 1)) < 0
assert (abs(u1) + abs(u2) + abs(u3)) / 2 > F(1, 2)

# Local determinant scaling is audited on non-unit diagonal filters.
r = [[g(2), ZERO], [ZERO, g(3)]]
s = [[g(5), ZERO], [ZERO, g(7)]]
local_filter = kronecker(r, s)
filtered = matrix_multiply(
    local_filter, matrix_multiply(k, dagger(local_filter))
)
filtered_partial_transpose = partial_transpose_second(filtered)
scale = F(2 * 3) ** 4 * F(5 * 7) ** 4
assert determinant(filtered) == g(scale * determinant(k)[0])
assert determinant(filtered_partial_transpose) == g(
    scale * determinant(k_partial_transpose)[0]
)

# The fixed Minkowski trace is exactly twice the partially transposed
# singlet expectation, including for a non-diagonal spatial block.
scalar = F(7, 5)
spatial = [
    [F(1, 3), F(1, 11), F(-1, 13)],
    [F(1, 7), F(-2, 9), F(1, 17)],
    [F(1, 19), F(-1, 23), F(3, 10)],
]
generic_choi = choi_from_scalar_spatial_transfer(scalar, spatial)
generic_partial_transpose = partial_transpose_first(generic_choi)
minkowski_trace = scalar - sum(spatial[j][j] for j in range(3))
assert mul(g(2), singlet_expectation(generic_partial_transpose)) == g(
    minkowski_trace
)

# A symmetric Pauli transfer matrix makes the singlet an exact
# eigenvector.  Determinant-one linked filters preserve that same
# singlet, rather than merely preserving the sign of its expectation.
symmetric_transfer = [
    [F(2), F(1, 10), F(-1, 12), F(1, 14)],
    [F(1, 10), F(1, 3), F(1, 20), F(-1, 18)],
    [F(-1, 12), F(1, 20), F(-1, 5), F(1, 16)],
    [F(1, 14), F(-1, 18), F(1, 16), F(1, 7)],
]
symmetric_choi = choi_from_transfer(symmetric_transfer)
symmetric_partial_transpose = partial_transpose_first(symmetric_choi)
singlet = [ZERO, ONE, neg(ONE), ZERO]
singlet_eigenvalue = (
    symmetric_transfer[0][0]
    - sum(symmetric_transfer[j][j] for j in range(1, 4))
) / 2
assert matrix_vector(symmetric_partial_transpose, singlet) == [
    mul(g(singlet_eigenvalue), value) for value in singlet
]

h = [[g(2), g(1)], [g(1), g(1)]]  # positive and determinant one
linked_filter = kronecker(h, h)
assert matrix_vector(linked_filter, singlet) == singlet
linked_choi = matrix_multiply(
    linked_filter, matrix_multiply(symmetric_choi, dagger(linked_filter))
)
linked_partial_transpose = partial_transpose_first(linked_choi)
assert linked_partial_transpose == matrix_multiply(
    linked_filter,
    matrix_multiply(symmetric_partial_transpose, dagger(linked_filter)),
)
assert matrix_vector(linked_partial_transpose, singlet) == [
    mul(g(singlet_eigenvalue), value) for value in singlet
]

# The determinant-critical core identity
# A^* (C^+)^* B = M^{- *} is checked in a nontrivial complex frame.
a_frame = [[g(2), g(1, 1)], [g(0, 1), g(3)]]
b_frame = [[g(1), g(1, -1)], [g(2, 1), g(2)]]
m_core = [[g(1, 1), g(2)], [g(-1), g(1, -1)]]
c_matrix = matrix_multiply(
    a_frame, matrix_multiply(m_core, dagger(b_frame))
)
n_matrix = dagger(inverse2(c_matrix))
assert matrix_multiply(
    dagger(a_frame), matrix_multiply(n_matrix, b_frame)
) == dagger(inverse2(m_core))

print(
    "verified exact Bell eigenvalues, partial-transpose determinant, "
    "octahedral trace-norm frontier, local-filter scaling, and fixed "
    "Minkowski/singlet, linked-filter, and determinant-critical core "
    "identities"
)
