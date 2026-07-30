#!/usr/bin/env python3
"""Exact rational checks for the square-zero code-output lemma.

Only Python's standard library is used.  The test constructs two
orthogonal erasure-decoupled qutrit codes from disjoint Latin
diagonals, forms the endpoint Gram by partial traces, and independently
reconstructs its positive pair-output decomposition.
"""

from fractions import Fraction as F
from itertools import combinations


Word = tuple[int, int, int]
SparseVector = dict[Word, F]
SparseMatrix = dict[tuple[tuple[int, ...], tuple[int, ...]], F]


def diagonal_state(a: int, b: int) -> SparseVector:
    """Unnormalized support of (1/sqrt(3)) sum_j |j,j+a,j+b>."""
    return {
        (j, (j + a) % 3, (j + b) % 3): F(1)
        for j in range(3)
    }


def transition(
    left: SparseVector, right: SparseVector, normalization: F = F(1, 3)
) -> SparseMatrix:
    """Normalized |left><right| for the Latin states used below."""
    return {
        (row, col): normalization * x * y
        for row, x in left.items()
        for col, y in right.items()
    }


def partial_trace(matrix: SparseMatrix, traced: tuple[int, ...]) -> SparseMatrix:
    traced = tuple(sorted(traced))
    kept = tuple(i for i in range(3) if i not in traced)
    out: SparseMatrix = {}
    for (row, col), value in matrix.items():
        if any(row[i] != col[i] for i in traced):
            continue
        key = (
            tuple(row[i] for i in kept),
            tuple(col[i] for i in kept),
        )
        out[key] = out.get(key, F(0)) + value
    return {key: value for key, value in out.items() if value}


def hs_inner(left: SparseMatrix, right: SparseMatrix) -> F:
    return sum(value * right.get(key, F(0)) for key, value in left.items())


def endpoint_bilinear(left: SparseMatrix, right: SparseMatrix) -> F:
    value = hs_inner(left, right)
    for site in range(3):
        value -= F(1, 2) * hs_inner(
            partial_trace(left, (site,)),
            partial_trace(right, (site,)),
        )
    for sites in combinations(range(3), 2):
        value += F(1, 4) * hs_inner(
            partial_trace(left, sites),
            partial_trace(right, sites),
        )
    value -= F(1, 8) * hs_inner(
        partial_trace(left, (0, 1, 2)),
        partial_trace(right, (0, 1, 2)),
    )
    return value


def determinant(matrix: list[list[F]]) -> F:
    work = [row[:] for row in matrix]
    answer = F(1)
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        p = work[column][column]
        answer *= p
        for row in range(column + 1, len(work)):
            factor = work[row][column] / p
            for j in range(column + 1, len(work)):
                work[row][j] -= factor * work[column][j]
    return answer


def one_site_reduction(
    left: SparseVector, right: SparseVector, site: int
) -> list[list[F]]:
    reduced = partial_trace(
        transition(left, right),
        tuple(i for i in range(3) if i != site),
    )
    return [
        [reduced.get(((a,), (b,)), F(0)) for b in range(3)]
        for a in range(3)
    ]


def pair_output_entry(
    u_left: SparseVector,
    u_right: SparseVector,
    w_left: SparseVector,
    w_right: SparseVector,
    retained: tuple[int, int],
) -> F:
    """<u_left|[(Tr_complement |w_left><w_right|) tensor I]|u_right>."""
    complement = next(i for i in range(3) if i not in retained)
    reduced = partial_trace(
        transition(w_left, w_right),
        (complement,),
    )
    answer = F(0)
    # Each normalized u amplitude contributes 1/sqrt(3), hence 1/3
    # for the bra-ket pair.
    for row, x in u_left.items():
        for col, y in u_right.items():
            if row[complement] != col[complement]:
                continue
            pair_row = tuple(row[i] for i in retained)
            pair_col = tuple(col[i] for i in retained)
            answer += (
                F(1, 3)
                * x
                * y
                * reduced.get((pair_row, pair_col), F(0))
            )
    return answer


# Four disjoint Latin diagonals.  Each displayed pair is an isometry,
# the two planes are orthogonal, and both codes erase every one-site
# subsystem exactly.
u = (diagonal_state(0, 1), diagonal_state(1, 0))
w = (diagonal_state(0, 0), diagonal_state(1, 2))

identity_over_three = [
    [F(1, 3) if a == b else F(0) for b in range(3)]
    for a in range(3)
]
zero_three = [[F(0)] * 3 for _ in range(3)]

for code in (u, w):
    for site in range(3):
        for a in range(2):
            for b in range(2):
                expected = identity_over_three if a == b else zero_three
                assert one_site_reduction(code[a], code[b], site) == expected


# Endpoint Gram on E_ab=|u_a><w_b|, ordered 00,01,10,11.
units = [
    transition(u[a], w[b])
    for a in range(2)
    for b in range(2)
]
gram = [
    [endpoint_bilinear(left, right) for right in units]
    for left in units
]
expected_gram = [
    [F(7, 12), 0, 0, F(1, 12)],
    [0, F(7, 12), 0, 0],
    [0, 0, F(7, 12), 0],
    [F(1, 12), 0, 0, F(7, 12)],
]
assert gram == expected_gram
assert determinant(gram) == F(49, 432)


# Independently reconstruct G=I/2+(1/4) sum_{i<j} T_ij from the
# positive pair-output compressions.
pair_outputs: list[list[list[F]]] = []
for retained in combinations(range(3), 2):
    block = [[F(0)] * 4 for _ in range(4)]
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    block[2 * a + b][2 * c + d] = pair_output_entry(
                        u[a], u[c], w[b], w[d], retained
                    )
    pair_outputs.append(block)

reconstructed = [
    [
        (F(1, 2) if row == col else F(0))
        + F(1, 4) * sum(block[row][col] for block in pair_outputs)
        for col in range(4)
    ]
    for row in range(4)
]
assert reconstructed == gram

# Exact positivity of G-I/2: all principal minors are nonnegative.
gap = [
    [
        gram[row][col] - (F(1, 2) if row == col else F(0))
        for col in range(4)
    ]
    for row in range(4)
]
for size in range(1, 5):
    for subset in combinations(range(4), size):
        principal = [[gap[i][j] for j in subset] for i in subset]
        assert determinant(principal) >= 0


# Both aggregate plane marginals are 2I/3 at all sites.
two_identity_over_three = [
    [F(2, 3) if a == b else F(0) for b in range(3)]
    for a in range(3)
]
marginal_determinants: list[F] = []
for code in (u, w):
    for site in range(3):
        marginal = [
            [
                sum(
                    one_site_reduction(code[r], code[r], site)[a][b]
                    for r in range(2)
                )
                for b in range(3)
            ]
            for a in range(3)
        ]
        assert marginal == two_identity_over_three
        marginal_determinants.append(determinant(marginal))

assert marginal_determinants == [F(8, 27)] * 6
product_bound = F(3**18, 2**22)
for value in marginal_determinants:
    product_bound *= value
assert product_bound == F(1, 16)
assert determinant(gram) - product_bound == F(11, 216) > 0

print("verified: exact one-site erasure decoupling")
print("verified: endpoint Gram and positive pair-output decomposition")
print("verified: uniform one-half spectral gap")
print("verified: product determinant bound on a full-rank rational code")
