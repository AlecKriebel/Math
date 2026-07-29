"""Exact checker for the inertia-(2,2) obstruction and rank-two completion.

Only Python's standard-library rational arithmetic is used.
"""

from fractions import Fraction as F
from itertools import product


D = 3
N = 3
WORDS = list(product(range(D), repeat=N))
INDEX = {word: index for index, word in enumerate(WORDS)}


def zero_matrix(size: int) -> list[list[F]]:
    return [[F(0) for _ in range(size)] for _ in range(size)]


def partial_trace(
    matrix: list[list[F]], traced: tuple[int, ...]
) -> list[list[F]]:
    retained = tuple(site for site in range(N) if site not in traced)
    retained_words = list(product(range(D), repeat=len(retained)))
    traced_words = list(product(range(D), repeat=len(traced)))
    out = zero_matrix(D ** len(retained))
    for row_index, row_retained in enumerate(retained_words):
        for column_index, column_retained in enumerate(retained_words):
            value = F(0)
            for common in traced_words:
                row = [0] * N
                column = [0] * N
                for position, site in enumerate(retained):
                    row[site] = row_retained[position]
                    column[site] = column_retained[position]
                for position, site in enumerate(traced):
                    row[site] = common[position]
                    column[site] = common[position]
                value += matrix[INDEX[tuple(row)]][INDEX[tuple(column)]]
            out[row_index][column_index] = value
    return out


def norm_squared(matrix: list[list[F]]) -> F:
    return sum(entry * entry for row in matrix for entry in row)


def q3(matrix: list[list[F]]) -> F:
    value = F(0)
    for mask in range(8):
        traced = tuple(site for site in range(3) if mask >> site & 1)
        value += F(-1, 2) ** len(traced) * norm_squared(
            partial_trace(matrix, traced)
        )
    return value


def projector_diagonal(
    positive: tuple[tuple[int, int, int], ...],
    negative: tuple[tuple[int, int, int], ...],
) -> list[list[F]]:
    out = zero_matrix(27)
    for word in positive:
        out[INDEX[word]][INDEX[word]] = F(1, 2)
    for word in negative:
        out[INDEX[word]][INDEX[word]] = F(-1, 2)
    return out


def completion_b(
    positive: tuple[tuple[int, int, int], ...],
    negative: tuple[tuple[int, int, int], ...],
) -> list[list[F]]:
    """The U=I member of equation (56)."""

    out = zero_matrix(27)
    for p, n in zip(positive, negative):
        out[INDEX[p]][INDEX[n]] = F(1, 2)
        out[INDEX[n]][INDEX[p]] = F(1, 2)
    return out


POSITIVE = ((0, 2, 2), (1, 0, 1))
NEGATIVE = ((1, 2, 0), (2, 0, 2))
H = projector_diagonal(POSITIVE, NEGATIVE)
B = completion_b(POSITIVE, NEGATIVE)

expected_h_norms = (
    F(1),
    F(1),
    F(1),
    F(1, 2),
    F(1),
    F(0),
    F(1, 2),
    F(0),
)
actual_h_norms = tuple(
    norm_squared(
        partial_trace(H, tuple(site for site in range(3) if mask >> site & 1))
    )
    for mask in range(8)
)
assert actual_h_norms == expected_h_norms
assert q3(H) == F(-1, 4)
assert q3(B) == F(1, 2)

# On span(p_1,p_2,n_1,n_2), C=H+iB has block matrix
# (1/2)[[I,iI],[iI,-I]].  Its square is exactly zero, so rank(C)<=2.
# Its upper-left 2-by-2 minor is (1/2)I, so rank(C)>=2.
# Finally Q(A+iB)=Q(A)+Q(B) for Hermitian A,B.
assert q3(H) + q3(B) == F(1, 4)

print("verified: Q3(H)=-1/4, rank(H+iB)=2, Q3(H+iB)=1/4")
