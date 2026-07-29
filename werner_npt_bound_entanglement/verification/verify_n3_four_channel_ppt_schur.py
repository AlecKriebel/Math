"""Exact checks for the three-copy four-channel Gram reduction.

Only standard-library rational arithmetic is used.  The script verifies:

* the weighted local Fierz channel;
* the four-channel Pauli collapse to twice a partial transpose;
* equality with the direct partial-trace definition of Q_3;
* the ordinary and reversed Schur-complement factorizations; and
* negativity of an individual rank-two Fierz atom after logical
  partial transpose.
"""

from fractions import Fraction as F
from itertools import combinations, product


def zeros(rows: int, columns: int) -> list[list[F]]:
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def identity(size: int) -> list[list[F]]:
    out = zeros(size, size)
    for index in range(size):
        out[index][index] = F(1)
    return out


def transpose(matrix: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*matrix)]


def add(*matrices: list[list[F]]) -> list[list[F]]:
    return [
        [sum(matrix[row][column] for matrix in matrices)
         for column in range(len(matrices[0][0]))]
        for row in range(len(matrices[0]))
    ]


def scale(value: F, matrix: list[list[F]]) -> list[list[F]]:
    return [[value * entry for entry in row] for row in matrix]


def multiply(
    left: list[list[F]], right: list[list[F]]
) -> list[list[F]]:
    return [
        [
            sum(left[row][middle] * right[middle][column]
                for middle in range(len(right)))
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def kronecker(
    left: list[list[F]], right: list[list[F]]
) -> list[list[F]]:
    return [
        [
            left[row_left][column_left] * right[row_right][column_right]
            for column_left in range(len(left[0]))
            for column_right in range(len(right[0]))
        ]
        for row_left in range(len(left))
        for row_right in range(len(right))
    ]


def outer(left: list[F], right: list[F]) -> list[list[F]]:
    return [[x * y for y in right] for x in left]


def flatten_columns(matrix: list[list[F]]) -> list[F]:
    """Identify an H-by-2 matrix with H tensor K."""

    return [
        matrix[physical][logical]
        for physical in range(len(matrix))
        for logical in range(len(matrix[0]))
    ]


def inverse(matrix: list[list[F]]) -> list[list[F]]:
    size = len(matrix)
    augmented = [
        matrix[row][:] + identity(size)[row]
        for row in range(size)
    ]
    for pivot_column in range(size):
        pivot_row = next(
            row
            for row in range(pivot_column, size)
            if augmented[row][pivot_column]
        )
        augmented[pivot_column], augmented[pivot_row] = (
            augmented[pivot_row],
            augmented[pivot_column],
        )
        pivot = augmented[pivot_column][pivot_column]
        augmented[pivot_column] = [
            entry / pivot for entry in augmented[pivot_column]
        ]
        for row in range(size):
            if row == pivot_column:
                continue
            coefficient = augmented[row][pivot_column]
            if coefficient:
                augmented[row] = [
                    augmented[row][column]
                    - coefficient * augmented[pivot_column][column]
                    for column in range(2 * size)
                ]
    return [row[size:] for row in augmented]


def words(number_of_sites: int) -> list[tuple[int, ...]]:
    return list(product(range(2), repeat=number_of_sites))


def word_index(word: tuple[int, ...]) -> int:
    value = 0
    for digit in word:
        value = 2 * value + digit
    return value


def partial_trace_matrix(
    matrix: list[list[F]], traced: tuple[int, ...]
) -> list[list[F]]:
    number_of_sites = 3
    remaining = tuple(
        site for site in range(number_of_sites) if site not in traced
    )
    remaining_words = words(len(remaining))
    traced_words = words(len(traced))
    out = zeros(2 ** len(remaining), 2 ** len(remaining))
    for row_remaining in remaining_words:
        for column_remaining in remaining_words:
            value = F(0)
            for traced_word in traced_words:
                row = [0] * number_of_sites
                column = [0] * number_of_sites
                for site, digit in zip(remaining, row_remaining):
                    row[site] = digit
                for site, digit in zip(remaining, column_remaining):
                    column[site] = digit
                for site, digit in zip(traced, traced_word):
                    row[site] = digit
                    column[site] = digit
                value += matrix[word_index(tuple(row))][
                    word_index(tuple(column))
                ]
            out[word_index(row_remaining)][word_index(column_remaining)] = (
                value
            )
    return out


def hs_norm_squared(matrix: list[list[F]]) -> F:
    return sum(entry * entry for row in matrix for entry in row)


def q3(matrix: list[list[F]]) -> F:
    value = F(0)
    for size in range(4):
        for traced in combinations(range(3), size):
            value += (
                F(-1, 2) ** size
                * hs_norm_squared(partial_trace_matrix(matrix, traced))
            )
    return value


def transpose_site(
    matrix: list[list[F]], site: int, number_of_sites: int
) -> list[list[F]]:
    out = zeros(len(matrix), len(matrix))
    all_words = words(number_of_sites)
    for row_word in all_words:
        for column_word in all_words:
            source_row = list(row_word)
            source_column = list(column_word)
            source_row[site], source_column[site] = (
                source_column[site],
                source_row[site],
            )
            out[word_index(row_word)][word_index(column_word)] = matrix[
                word_index(tuple(source_row))
            ][word_index(tuple(source_column))]
    return out


def trace_replace_site(
    matrix: list[list[F]], site: int, number_of_sites: int
) -> list[list[F]]:
    out = zeros(len(matrix), len(matrix))
    all_words = words(number_of_sites)
    for row_word in all_words:
        for column_word in all_words:
            if row_word[site] != column_word[site]:
                continue
            value = F(0)
            for digit in range(2):
                source_row = list(row_word)
                source_column = list(column_word)
                source_row[site] = digit
                source_column[site] = digit
                value += matrix[word_index(tuple(source_row))][
                    word_index(tuple(source_column))
                ]
            out[word_index(row_word)][word_index(column_word)] = value
    return out


def tilde_phi_tensor(matrix: list[list[F]]) -> list[list[F]]:
    out = matrix
    for site in range(3):
        out = add(
            trace_replace_site(out, site, 3),
            scale(F(-1, 2), transpose_site(out, site, 3)),
        )
    return out


def logical_partial_transpose(matrix: list[list[F]]) -> list[list[F]]:
    """Partial transpose on K in the H tensor K ordering."""

    physical_size = len(matrix) // 2
    out = zeros(len(matrix), len(matrix))
    for row_physical in range(physical_size):
        for column_physical in range(physical_size):
            for row_logical in range(2):
                for column_logical in range(2):
                    out[2 * row_physical + row_logical][
                        2 * column_physical + column_logical
                    ] = matrix[
                        2 * row_physical + column_logical
                    ][2 * column_physical + row_logical]
    return out


I2 = [[F(1), F(0)], [F(0), F(1)]]
X = [[F(0), F(1)], [F(1), F(0)]]
Z = [[F(1), F(0)], [F(0), F(-1)]]
EPSILON = [[F(0), F(1)], [F(-1), F(0)]]


# The local weighted frame is represented by an unscaled rational matrix
# and the square of its scalar weight.
local_frame = (
    (I2, F(1, 4)),
    (X, F(1, 4)),
    (Z, F(1, 4)),
    (EPSILON, F(3, 4)),
)


# Direct local-channel audit on a generic rational matrix.
generic = [[F(2), F(3)], [F(5), F(7)]]
frame_image = zeros(2, 2)
for raw, weight_squared in local_frame:
    frame_image = add(
        frame_image,
        scale(
            weight_squared,
            multiply(transpose(raw), multiply(generic, raw)),
        ),
    )
expected_image = add(
    scale(generic[0][0] + generic[1][1], I2),
    scale(F(-1, 2), transpose(generic)),
)
assert frame_image == expected_image


# A rational isometry U:C^2 -> (C^2)^3.
physical_size = 8
u0 = [F(0)] * physical_size
u1 = [F(0)] * physical_size
u0[0] = F(1)
u1[1] = F(3, 5)
u1[2] = F(4, 5)
assert sum(x * x for x in u0) == F(1)
assert sum(x * x for x in u1) == F(1)
assert sum(x * y for x, y in zip(u0, u1)) == F(0)
U = [[u0[row], u1[row]] for row in range(physical_size)]


# Build the positive Fierz Gram operator G_U exactly.
G = zeros(2 * physical_size, 2 * physical_size)
identity_atom = None
identity_atom_weight = None
for choices in product(range(4), repeat=3):
    raw = [[F(1)]]
    weight_squared = F(1)
    for choice in choices:
        raw = kronecker(raw, local_frame[choice][0])
        weight_squared *= local_frame[choice][1]
    analysis_matrix = multiply(transpose(raw), U)
    analysis_vector = flatten_columns(analysis_matrix)
    G = add(G, scale(weight_squared, outer(
        analysis_vector, analysis_vector
    )))
    if choices == (0, 0, 0):
        identity_atom = outer(analysis_vector, analysis_vector)
        identity_atom_weight = weight_squared


# The block formula G_ab=tildePhi(|u_a><u_b|).
for row_logical in range(2):
    for column_logical in range(2):
        source = outer(
            [U[row][row_logical] for row in range(physical_size)],
            [U[row][column_logical] for row in range(physical_size)],
        )
        expected_block = tilde_phi_tensor(source)
        actual_block = [
            [
                G[2 * row + row_logical][
                    2 * column + column_logical
                ]
                for column in range(physical_size)
            ]
            for row in range(physical_size)
        ]
        assert actual_block == expected_block


# Exact Pauli collapse:
# Gamma_I+Gamma_X+Gamma_Z-Gamma_epsilon=2 G^{Gamma_K}.
logical_operators = [
    kronecker(identity(physical_size), logical)
    for logical in (I2, X, Z, EPSILON)
]
gammas = [
    multiply(transpose(operator), multiply(G, operator))
    for operator in logical_operators
]
signed_channels = add(
    gammas[0], gammas[1], gammas[2], scale(F(-1), gammas[3])
)
G_partial_transpose = logical_partial_transpose(G)
assert signed_channels == scale(F(2), G_partial_transpose)


# Compare the Gram quadratic form with the direct partial-trace formula.
v0 = [F(index - 2, 7) for index in range(physical_size)]
v1 = [F((-1) ** index * (index + 1), 11) for index in range(physical_size)]
V = [[v0[row], v1[row]] for row in range(physical_size)]
C = multiply(U, transpose(V))
vector_V = flatten_columns(V)
gram_q3 = sum(
    vector_V[row] * G_partial_transpose[row][column] * vector_V[column]
    for row in range(2 * physical_size)
    for column in range(2 * physical_size)
)
assert gram_q3 == q3(C)


# Extract the 2-by-2 logical blocks.
def block(
    matrix: list[list[F]], row_logical: int, column_logical: int
) -> list[list[F]]:
    return [
        [
            matrix[2 * row + row_logical][
                2 * column + column_logical
            ]
            for column in range(physical_size)
        ]
        for row in range(physical_size)
    ]


A = block(G, 0, 0)
B = block(G, 0, 1)
D = block(G, 1, 1)
A_inverse = inverse(A)
ordinary_schur = add(
    D,
    scale(F(-1), multiply(transpose(B), multiply(A_inverse, B))),
)
reversed_schur = add(
    D,
    scale(F(-1), multiply(B, multiply(A_inverse, transpose(B)))),
)


# Exact block Gaussian eliminations.  The two Schur complements differ
# for this nontrivial anchor; positivity of the reversed one is the
# unresolved theorem, not asserted here.
zero_block = zeros(physical_size, physical_size)
block_identity = identity(physical_size)


def assemble_blocks(
    top_left: list[list[F]],
    top_right: list[list[F]],
    bottom_left: list[list[F]],
    bottom_right: list[list[F]],
) -> list[list[F]]:
    out = zeros(2 * physical_size, 2 * physical_size)
    for row in range(physical_size):
        for column in range(physical_size):
            out[row][column] = top_left[row][column]
            out[row][physical_size + column] = top_right[row][column]
            out[physical_size + row][column] = bottom_left[row][column]
            out[physical_size + row][physical_size + column] = (
                bottom_right[row][column]
            )
    return out


# Switch from H tensor K ordering to K tensor H for conventional blocks.
permutation = zeros(2 * physical_size, 2 * physical_size)
for physical in range(physical_size):
    for logical in range(2):
        permutation[logical * physical_size + physical][
            2 * physical + logical
        ] = F(1)
G_block_order = multiply(permutation, multiply(G, transpose(permutation)))
Gpt_block_order = multiply(
    permutation, multiply(G_partial_transpose, transpose(permutation))
)

ordinary_eliminator = assemble_blocks(
    block_identity,
    scale(F(-1), multiply(A_inverse, B)),
    zero_block,
    block_identity,
)
ordinary_diagonalized = multiply(
    transpose(ordinary_eliminator),
    multiply(G_block_order, ordinary_eliminator),
)
assert ordinary_diagonalized == assemble_blocks(
    A, zero_block, zero_block, ordinary_schur
)

reversed_eliminator = assemble_blocks(
    block_identity,
    scale(F(-1), multiply(A_inverse, transpose(B))),
    zero_block,
    block_identity,
)
reversed_diagonalized = multiply(
    transpose(reversed_eliminator),
    multiply(Gpt_block_order, reversed_eliminator),
)
assert reversed_diagonalized == assemble_blocks(
    A, zero_block, zero_block, reversed_schur
)
assert ordinary_schur != reversed_schur


# A single invertible frame atom cannot be PPT.  The I tensor I tensor I
# atom is weight 1/64 times |U>><<U|.  Its logical partial transpose has
# eigenvalue -1 on the normalized antisymmetric code vector.  With the
# unnormalized vector below, the exact quadratic value is -2/64=-1/32.
assert identity_atom is not None
assert identity_atom_weight == F(1, 64)
identity_atom_pt = logical_partial_transpose(identity_atom)
antisymmetric = [F(0)] * (2 * physical_size)
for physical in range(physical_size):
    antisymmetric[2 * physical + 1] += u0[physical]
    antisymmetric[2 * physical + 0] -= u1[physical]
atom_value = identity_atom_weight * sum(
    antisymmetric[row]
    * identity_atom_pt[row][column]
    * antisymmetric[column]
    for row in range(2 * physical_size)
    for column in range(2 * physical_size)
)
assert atom_value == F(-1, 32)


print(
    "verified: weighted Fierz channel; four-channel partial-transpose "
    "collapse; direct Q3 identity; ordinary/reversed Schur reductions; "
    "single-atom NPT obstruction"
)
