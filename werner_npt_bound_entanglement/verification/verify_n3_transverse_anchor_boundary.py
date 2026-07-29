"""Exact verifier for the transverse three-copy anchor boundary.

Only standard-library rational arithmetic is used.
"""

from fractions import Fraction as F
from itertools import combinations, product


DIMS = (2, 2, 2, 2)  # K, physical sites 1,2,3
WORDS4 = list(product(range(2), repeat=4))
INDEX4 = {word: index for index, word in enumerate(WORDS4)}
WORDS3 = list(product(range(2), repeat=3))
INDEX3 = {word: index for index, word in enumerate(WORDS3)}


def zero_matrix(rows: int, columns: int | None = None) -> list[list[F]]:
    if columns is None:
        columns = rows
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def inner(x: list[F], y: list[F]) -> F:
    return sum(a * b for a, b in zip(x, y))


def outer(x: list[F], y: list[F]) -> list[list[F]]:
    return [[a * b for b in y] for a in x]


def mat_add(
    left: list[list[F]], right: list[list[F]], scale: F = F(1)
) -> list[list[F]]:
    return [
        [left[i][j] + scale * right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def mat_vec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def mat_mul(
    left: list[list[F]], right: list[list[F]]
) -> list[list[F]]:
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def trace(matrix: list[list[F]]) -> F:
    return sum(matrix[i][i] for i in range(len(matrix)))


def identity(size: int) -> list[list[F]]:
    out = zero_matrix(size)
    for i in range(size):
        out[i][i] = F(1)
    return out


def reduced_density4(vector: list[F], kept: tuple[int, ...]) -> list[list[F]]:
    omitted = tuple(i for i in range(4) if i not in kept)
    kept_words = list(product(range(2), repeat=len(kept)))
    omitted_words = list(product(range(2), repeat=len(omitted)))
    out = zero_matrix(2 ** len(kept))
    for row_index, row_kept in enumerate(kept_words):
        for column_index, column_kept in enumerate(kept_words):
            value = F(0)
            for omitted_word in omitted_words:
                row = [0] * 4
                column = [0] * 4
                for site, digit in zip(kept, row_kept):
                    row[site] = digit
                for site, digit in zip(kept, column_kept):
                    column[site] = digit
                for site, digit in zip(omitted, omitted_word):
                    row[site] = digit
                    column[site] = digit
                value += (
                    vector[INDEX4[tuple(row)]]
                    * vector[INDEX4[tuple(column)]]
                )
            out[row_index][column_index] = value
    return out


def swap_moment(a: list[F], b: list[F], mask: int) -> F:
    kept = tuple(i for i in range(4) if mask >> i & 1)
    rho_a = reduced_density4(a, kept)
    rho_b = reduced_density4(b, kept)
    return trace(mat_mul(rho_a, rho_b))


def sector_weights(a: list[F], b: list[F]) -> dict[tuple[int, ...], F]:
    moments = [swap_moment(a, b, mask) for mask in range(16)]
    out: dict[tuple[int, ...], F] = {}
    for parity in product(range(2), repeat=4):
        value = F(0)
        for mask, moment in enumerate(moments):
            exponent = sum(
                parity[site] for site in range(4) if mask >> site & 1
            )
            value += (-1) ** exponent * moment
        out[parity] = value / 16
    return out


def aggregate(
    weights: dict[tuple[int, ...], F], k: int, r: int
) -> F:
    return sum(
        value
        for parity, value in weights.items()
        if parity[0] == k and sum(parity[1:]) == r
    )


def partial_trace3(
    matrix: list[list[F]], traced: tuple[int, ...]
) -> list[list[F]]:
    retained = tuple(i for i in range(3) if i not in traced)
    retained_words = list(product(range(2), repeat=len(retained)))
    traced_words = list(product(range(2), repeat=len(traced)))
    out = zero_matrix(2 ** len(retained))
    for row_index, row_retained in enumerate(retained_words):
        for column_index, column_retained in enumerate(retained_words):
            value = F(0)
            for traced_word in traced_words:
                row = [0] * 3
                column = [0] * 3
                for site, digit in zip(retained, row_retained):
                    row[site] = digit
                for site, digit in zip(retained, column_retained):
                    column[site] = digit
                for site, digit in zip(traced, traced_word):
                    row[site] = digit
                    column[site] = digit
                value += matrix[INDEX3[tuple(row)]][INDEX3[tuple(column)]]
            out[row_index][column_index] = value
    return out


def hs_inner(left: list[list[F]], right: list[list[F]]) -> F:
    return sum(
        left[i][j] * right[i][j]
        for i in range(len(left))
        for j in range(len(left[0]))
    )


def q3_bilinear(left: list[list[F]], right: list[list[F]]) -> F:
    value = F(0)
    for mask in range(8):
        traced = tuple(i for i in range(3) if mask >> i & 1)
        value += (
            F(-1, 2) ** len(traced)
            * hs_inner(
                partial_trace3(left, traced),
                partial_trace3(right, traced),
            )
        )
    return value


def lifted_reduction4(vector: list[F], kept: tuple[int, ...]) -> list[list[F]]:
    rho = reduced_density4(vector, kept)
    kept_words = list(product(range(2), repeat=len(kept)))
    kept_index = {word: index for index, word in enumerate(kept_words)}
    omitted = tuple(i for i in range(4) if i not in kept)
    out = zero_matrix(16)
    for row in WORDS4:
        for column in WORDS4:
            if any(row[i] != column[i] for i in omitted):
                continue
            row_kept = tuple(row[i] for i in kept)
            column_kept = tuple(column[i] for i in kept)
            out[INDEX4[row]][INDEX4[column]] = rho[
                kept_index[row_kept]
            ][kept_index[column_kept]]
    return out


def characteristic_coefficients(matrix: list[list[F]]) -> list[F]:
    """Faddeev--LeVerrier coefficients of det(t I - matrix)."""

    size = len(matrix)
    coefficients = [F(1)]
    current = identity(size)
    for k in range(1, size + 1):
        product_matrix = mat_mul(matrix, current)
        coefficient = -trace(product_matrix) / k
        coefficients.append(coefficient)
        current = mat_add(product_matrix, identity(size), coefficient)
    return coefficients


def polynomial_product(left: list[F], right: list[F]) -> list[F]:
    out = [F(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def root_polynomial(root: F, multiplicity: int) -> list[F]:
    out = [F(1)]
    for _ in range(multiplicity):
        out = polynomial_product(out, [F(1), -root])
    return out


# The four-party vectors in (9), with their square-root factors multiplied.
A = [F(0)] * 16
B = [F(0)] * 16
for word, value in (
    ((0, 0, 0, 0), 1),
    ((0, 0, 1, 1), 1),
    ((1, 1, 0, 0), 1),
    ((1, 1, 1, 1), -1),
):
    A[INDEX4[word]] = F(value, 2)
for word, value in (
    ((0, 0, 0, 0), -1),
    ((0, 0, 1, 1), 1),
    ((1, 1, 0, 0), 1),
    ((1, 1, 1, 1), 1),
):
    B[INDEX4[word]] = F(value, 2)

assert inner(A, A) == inner(B, B) == F(1)
assert inner(A, B) == F(0)
assert reduced_density4(A, (0,)) == [[F(1, 2), F(0)], [F(0), F(1, 2)]]
assert reduced_density4(B, (0,)) == [[F(1, 2), F(0)], [F(0), F(1, 2)]]

weights = sector_weights(A, B)
expected = {
    (0, 0): F(5, 16),
    (0, 1): F(3, 8),
    (0, 2): F(1, 16),
    (0, 3): F(0),
    (1, 0): F(1, 8),
    (1, 1): F(1, 16),
    (1, 2): F(0),
    (1, 3): F(1, 16),
}
actual = {
    (k, r): aggregate(weights, k, r)
    for k in range(2)
    for r in range(4)
}
assert actual == expected

d_odd = actual[1, 0] + actual[0, 1] + 13 * actual[0, 3] - 3 * actual[1, 2]
d_even = 4 * actual[0, 2] - 12 * actual[1, 3]
assert d_odd == F(1, 2)
assert d_even == F(-1, 2)
assert d_odd + d_even == 0
assert 3 * actual[1, 3] > actual[0, 2]

# Three-physical-qubit singular frames, stored without square roots:
# each actual vector is the displayed integer vector divided by sqrt(2).
u1_num = {(0, 0, 0): 1, (0, 1, 1): 1}
u2_num = {(1, 0, 0): 1, (1, 1, 1): -1}
v1_num = {(0, 0, 0): -1, (0, 1, 1): 1}
v2_num = {(1, 0, 0): 1, (1, 1, 1): 1}


def rank_one_from_numerators(
    left: dict[tuple[int, int, int], int],
    right: dict[tuple[int, int, int], int],
) -> list[list[F]]:
    out = zero_matrix(8)
    for row, row_value in left.items():
        for column, column_value in right.items():
            out[INDEX3[row]][INDEX3[column]] = F(
                row_value * column_value, 2
            )
    return out


u_nums = (u1_num, u2_num)
v_nums = (v1_num, v2_num)
matrix_units = [
    [rank_one_from_numerators(u_nums[a], v_nums[b]) for b in range(2)]
    for a in range(2)
]
two_plane = zero_matrix(4)
for a, b, c, d in product(range(2), repeat=4):
    two_plane[2 * a + b][2 * c + d] = q3_bilinear(
        matrix_units[a][b], matrix_units[c][d]
    )

assert two_plane == [
    [F(1, 4), F(0), F(0), F(-1, 4)],
    [F(0), F(3, 4), F(0), F(0)],
    [F(0), F(0), F(3, 4), F(0)],
    [F(-1, 4), F(0), F(0), F(1, 4)],
]
assert mat_vec(two_plane, [F(1), F(0), F(0), F(1)]) == [F(0)] * 4

# Build the anchor operator (5).
anchor = mat_add(identity(16), outer(A, A), F(-1))
anchor = [[entry / 2 for entry in row] for row in anchor]
anchor = mat_add(anchor, lifted_reduction4(A, (0,)), F(3))
for site in (1, 2, 3):
    anchor = mat_add(anchor, lifted_reduction4(A, (0, site)), F(-2))
for first, second in combinations((1, 2, 3), 2):
    anchor = mat_add(
        anchor, lifted_reduction4(A, (0, first, second)), F(1)
    )

assert mat_vec(anchor, B) == [F(0)] * 16
actual_characteristic = characteristic_coefficients(anchor)
expected_characteristic = [F(1)]
for root, multiplicity in (
    (F(0), 1),
    (F(1, 2), 5),
    (F(1), 8),
    (F(3, 2), 2),
):
    expected_characteristic = polynomial_product(
        expected_characteristic, root_polynomial(root, multiplicity)
    )
assert actual_characteristic == expected_characteristic

print(
    "verified: transverse rank-two boundary; "
    "Dodd=1/2, Deven=-1/2; "
    "spec(H)={0,1/2,(3/4)^2}; "
    "spec(M)={0,(1/2)^5,1^8,(3/2)^2}"
)
