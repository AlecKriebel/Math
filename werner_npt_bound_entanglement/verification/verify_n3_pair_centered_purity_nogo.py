#!/usr/bin/env python3
"""Dependency-free exact checks for the pair-centered purity obstruction.

The checker uses only rational arithmetic.  It constructs

    C = |Phi_3><Phi_3|_{13} tensor P_{01}^{(2)}

in the canonical site order, decomposes it into scalar/traceless
operator sectors, and checks the pair-centered data and criticality
claimed in ``notes/agent_n3_pair_centered_purity_nogo.md``.
"""

from fractions import Fraction as F
from itertools import product


D_LOCAL = 3
N_SITES = 3
DIMENSION = D_LOCAL**N_SITES


def basis_index(word: tuple[int, ...]) -> int:
    value = 0
    for digit in word:
        value = D_LOCAL * value + digit
    return value


def zero(rows: int = DIMENSION, columns: int = DIMENSION):
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def identity():
    result = zero()
    for i in range(DIMENSION):
        result[i][i] = F(1)
    return result


def add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def subtract(left, right):
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def scale(coefficient: F, matrix):
    return [[coefficient * value for value in row] for row in matrix]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    rows = len(left)
    middle = len(right)
    columns = len(right[0])
    assert len(left[0]) == middle
    result = zero(rows, columns)
    for i in range(rows):
        for k in range(middle):
            coefficient = left[i][k]
            if coefficient == 0:
                continue
            for j in range(columns):
                if right[k][j] != 0:
                    result[i][j] += coefficient * right[k][j]
    return result


def trace(matrix):
    return sum((matrix[i][i] for i in range(len(matrix))), F(0))


def hs_inner(left, right):
    # All matrices in this checker are real.  The first factor is thus
    # its own entrywise conjugate.
    return sum(
        (
            left[i][j] * right[i][j]
            for i in range(len(left))
            for j in range(len(left[0]))
        ),
        F(0),
    )


def scalar_projection(matrix, site: int):
    """Orthogonal projection onto the scalar local operator at ``site``."""

    result = zero()
    other_sites = tuple(i for i in range(N_SITES) if i != site)
    other_words = tuple(product(range(D_LOCAL), repeat=N_SITES - 1))
    for row_other in other_words:
        for column_other in other_words:
            contracted = F(0)
            for local in range(D_LOCAL):
                row_word = [0] * N_SITES
                column_word = [0] * N_SITES
                row_word[site] = local
                column_word[site] = local
                for position, physical_site in enumerate(other_sites):
                    row_word[physical_site] = row_other[position]
                    column_word[physical_site] = column_other[position]
                contracted += matrix[
                    basis_index(tuple(row_word))
                ][basis_index(tuple(column_word))]
            for local in range(D_LOCAL):
                row_word = [0] * N_SITES
                column_word = [0] * N_SITES
                row_word[site] = local
                column_word[site] = local
                for position, physical_site in enumerate(other_sites):
                    row_word[physical_site] = row_other[position]
                    column_word[physical_site] = column_other[position]
                result[
                    basis_index(tuple(row_word))
                ][basis_index(tuple(column_word))] = contracted / D_LOCAL
    return result


def sector_component(matrix, mask: int):
    result = matrix
    for site in range(N_SITES):
        scalar = scalar_projection(result, site)
        if mask & (1 << site):
            result = subtract(result, scalar)
        else:
            result = scalar
    return result


def local_endpoint(matrix, site: int):
    # L(A)=A-(Tr A)I/2=A-(3/2)Pi_scalar(A).
    return subtract(matrix, scale(F(3, 2), scalar_projection(matrix, site)))


def endpoint_operator(matrix):
    result = matrix
    for site in range(N_SITES):
        result = local_endpoint(result, site)
    return result


def partial_trace_to_site(matrix, site: int):
    result = zero(D_LOCAL, D_LOCAL)
    other_sites = tuple(i for i in range(N_SITES) if i != site)
    for row_local in range(D_LOCAL):
        for column_local in range(D_LOCAL):
            total = F(0)
            for traced_word in product(
                range(D_LOCAL), repeat=N_SITES - 1
            ):
                row_word = [0] * N_SITES
                column_word = [0] * N_SITES
                row_word[site] = row_local
                column_word[site] = column_local
                for position, physical_site in enumerate(other_sites):
                    row_word[physical_site] = traced_word[position]
                    column_word[physical_site] = traced_word[position]
                total += matrix[
                    basis_index(tuple(row_word))
                ][basis_index(tuple(column_word))]
            result[row_local][column_local] = total
    return result


def hermitian_part(matrix):
    return scale(F(1, 2), add(matrix, transpose(matrix)))


def flag_bell_projection():
    """Return |Phi_3><Phi_3| on sites 1,3 times P_{01} on site 2."""

    result = zero()
    for flag in (0, 1):
        for left_bell in range(D_LOCAL):
            row = basis_index((left_bell, flag, left_bell))
            for right_bell in range(D_LOCAL):
                column = basis_index((right_bell, flag, right_bell))
                result[row][column] = F(1, 3)
    return result


def diagonal(values):
    result = zero(len(values), len(values))
    for i, value in enumerate(values):
        result[i][i] = F(value)
    return result


def check_exact_obstruction() -> None:
    C = flag_bell_projection()
    assert transpose(C) == C
    assert multiply(C, C) == C
    assert trace(C) == 2

    sectors = [sector_component(C, mask) for mask in range(8)]
    reconstructed = zero()
    for component in sectors:
        reconstructed = add(reconstructed, component)
    assert reconstructed == C

    # Bits in the mask mark traceless local factors.
    masses = tuple(hs_inner(component, component) for component in sectors)
    assert masses == (
        F(4, 27),
        F(0),
        F(2, 27),
        F(0),
        F(0),
        F(32, 27),
        F(0),
        F(16, 27),
    )

    degree_masses = tuple(
        sum(
            (masses[mask] for mask in range(8) if mask.bit_count() == degree),
            F(0),
        )
        for degree in range(4)
    )
    x, a, c, d = degree_masses
    q = -x / 8 + a / 4 - c / 2 + d
    G = a / 4 - c + 3 * d
    Xi = -5 * x + 4 * a - c / 2 + 7 * d / 4
    assert degree_masses == (F(4, 27), F(2, 27), F(32, 27), F(16, 27))
    assert q == 0
    assert c == F(32, 27)
    assert G == F(11, 18)
    assert a == F(2, 27)
    assert Xi == 0

    D = zero()
    for mask, component in enumerate(sectors):
        if mask.bit_count() == 2:
            D = add(D, component)
    assert hs_inner(C, D) == c
    assert hs_inner(D, D) == c

    # Pi_2 is an orthogonal projection on the operator Hilbert space.
    # Its image D is not itself an idempotent operator; multiplication
    # on the support of C gives the following exact scalar action.
    CD = multiply(C, transpose(D))
    DC = multiply(transpose(D), C)
    assert CD == scale(F(16, 27), C)
    assert DC == scale(F(16, 27), C)

    expected_H = (
        diagonal((F(1, 3), F(1, 3), F(1, 3))),
        diagonal((F(1, 2), F(1, 2), F(0))),
        diagonal((F(1, 3), F(1, 3), F(1, 3))),
    )

    raw_purity_sum = F(0)
    normalized_purity_sum = F(0)
    for product_matrix in (CD, DC):
        for site in range(N_SITES):
            X = hermitian_part(partial_trace_to_site(product_matrix, site))
            H = scale(1 / c, X)
            assert H == expected_H[site]
            raw_purity_sum += hs_inner(X, X)
            normalized_purity_sum += hs_inner(H, H)
    assert raw_purity_sum == F(7168, 2187)
    assert normalized_purity_sum == F(7, 3)

    # The original proposed certificate and its doubled polynomial form fail.
    original_gap = raw_purity_sum - 3 * c * c + q * c / 2
    doubled_polynomial = q * c - 6 * c * c + 2 * raw_purity_sum
    assert original_gap == F(-2048, 2187)
    assert doubled_polynomial == F(-4096, 2187)

    # The zero-compatible replacement proposed after finding this
    # obstruction is saturated here.  It is recorded as a candidate,
    # not asserted universally by this checker.
    repaired_gap = raw_purity_sum - F(7, 3) * c * c + q * c / 2
    assert repaired_gap == 0

    # Quotient criticality at lambda=0: A(C) lies in the rank-two normal
    # space, equivalently C A(C)=A(C) C=0 for this projection C.
    AC = endpoint_operator(C)
    assert hs_inner(C, AC) == q
    assert multiply(C, AC) == zero()
    assert multiply(AC, C) == zero()


def check_envelope_transition_arithmetic() -> None:
    # At P=3, the two envelope parametrizations meet at
    # alpha=1/2 and t=3/2 with rho=11/32.
    alpha = F(1, 2)
    t = F(3, 2)
    P_alpha = F(1, 2) + 2 * alpha + 6 * alpha * alpha
    rho_alpha = (
        2 * alpha * alpha * (3 + 16 * alpha)
        / (1 + 6 * alpha) ** 2
    )
    rho_t = (3 * t * t - 3 * t + F(1, 2)) / (6 * t - 1)
    assert P_alpha == 3
    assert rho_alpha == F(11, 32)
    assert rho_t == F(11, 32)

    # The critical Haar coefficient and its fusion consequence.
    assert F(51, 160) * F(16, 15) == F(17, 50)
    # r(1+17 R/50) <= 27/160 is equivalent to
    # r <= 135/(800+272 R).
    for R in (F(0), F(1, 7), F(9, 4)):
        left_form = F(27, 160) / (1 + F(17, 50) * R)
        right_form = F(135) / (800 + 272 * R)
        assert left_form == right_form


if __name__ == "__main__":
    check_exact_obstruction()
    check_envelope_transition_arithmetic()
    print("verified: exact pair-centered purity obstruction and envelope constants")
