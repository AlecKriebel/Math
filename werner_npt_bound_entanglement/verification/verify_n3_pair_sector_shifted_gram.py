#!/usr/bin/env python3
"""Exact checks for the qutrit pair-sector shifted Gram note."""

from fractions import Fraction as F
from itertools import combinations, product


def zeros(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def index(word):
    value = 0
    for digit in word:
        value = 3 * value + digit
    return value


def partial_trace(a, traced):
    n = 3
    traced = tuple(sorted(traced))
    remaining = tuple(i for i in range(n) if i not in traced)
    rem_words = list(product(range(3), repeat=len(remaining)))
    tr_words = list(product(range(3), repeat=len(traced)))
    out = zeros(3 ** len(remaining), 3 ** len(remaining))
    for row_index, row_remaining in enumerate(rem_words):
        for col_index, col_remaining in enumerate(rem_words):
            value = F(0)
            for trace_word in tr_words:
                row = [0] * n
                col = [0] * n
                for position, site in enumerate(remaining):
                    row[site] = row_remaining[position]
                    col[site] = col_remaining[position]
                for position, site in enumerate(traced):
                    row[site] = trace_word[position]
                    col[site] = trace_word[position]
                value += a[index(row)][index(col)]
            out[row_index][col_index] = value
    return out


def hs_inner(a, b):
    return sum(
        a[i][j] * b[i][j]
        for i in range(len(a))
        for j in range(len(a[0]))
    )


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def pair_sector_inner(a, b):
    value = F(0)
    for site in range(3):
        value += F(1, 3) * hs_inner(
            partial_trace(a, (site,)),
            partial_trace(b, (site,)),
        )
        complement = tuple(i for i in range(3) if i != site)
        value -= F(2, 9) * hs_inner(
            partial_trace(a, complement),
            partial_trace(b, complement),
        )
    value += F(1, 9) * trace(a) * trace(b)
    return value


def kron(a, b):
    out = zeros(len(a) * len(b), len(a[0]) * len(b[0]))
    for i, j, k, ell in product(
        range(len(a)),
        range(len(a[0])),
        range(len(b)),
        range(len(b[0])),
    ):
        out[i * len(b) + k][j * len(b[0]) + ell] = a[i][j] * b[k][ell]
    return out


def matrix_unit(row, col):
    out = zeros(3, 3)
    out[row][col] = F(1)
    return out


def add_group_algebra(left, right):
    out = dict(left)
    for mask, coefficient in right.items():
        out[mask] = out.get(mask, F(0)) + coefficient
    return {mask: coefficient for mask, coefficient in out.items() if coefficient}


def multiply_group_algebra(left, right):
    out = {}
    for mask1, coefficient1 in left.items():
        for mask2, coefficient2 in right.items():
            mask = mask1 ^ mask2
            out[mask] = out.get(mask, F(0)) + coefficient1 * coefficient2
    return {mask: coefficient for mask, coefficient in out.items() if coefficient}


def main():
    # Verify the universal SOS identity in the commuting local-swap
    # group algebra.
    identity = {0: F(1)}
    one_minus = [
        {0: F(1), 1 << site: F(-1)}
        for site in range(3)
    ]
    rhs = {}
    for i, j in combinations(range(3), 2):
        rhs = add_group_algebra(
            rhs,
            multiply_group_algebra(one_minus[i], one_minus[j]),
        )
    triple = identity
    for factor in one_minus:
        triple = multiply_group_algebra(triple, factor)
    rhs = add_group_algebra(rhs, triple)

    expected = {
        0: F(4),
        1: F(-3),
        2: F(-3),
        4: F(-3),
        3: F(2),
        5: F(2),
        6: F(2),
        7: F(-1),
    }
    assert rhs == expected

    # Verify the partial-transpose parity spectra.
    pi2_eigenvalues = []
    shifted_eigenvalues = []
    slack_eigenvalues = []
    for q in range(4):
        signs = [-1] * q + [1] * (3 - q)
        pi2_value = F(0)
        for identity_site in range(3):
            term = F(signs[identity_site], 3)
            for site in range(3):
                if site != identity_site:
                    term *= 1 - F(signs[site], 3)
            pi2_value += term
        pi2_eigenvalues.append(pi2_value)
        shifted_eigenvalues.append(F(2, 3) - pi2_value)
        slack_eigenvalues.append(F(4, 9) - pi2_value)
    assert pi2_eigenvalues == [
        F(4, 9), F(4, 9), F(0), F(-16, 9)
    ]
    assert shifted_eigenvalues == [
        F(2, 9), F(2, 9), F(2, 3), F(22, 9)
    ]
    assert slack_eigenvalues == [
        F(0), F(0), F(4, 9), F(20, 9)
    ]

    p0 = matrix_unit(0, 0)
    p1 = matrix_unit(1, 1)
    e01 = matrix_unit(0, 1)

    # Sharp rank-one example.
    rank_one = kron(kron(p0, p0), p0)
    assert hs_inner(rank_one, rank_one) == 1
    assert pair_sector_inner(rank_one, rank_one) == F(4, 9)

    # Sharp rank-two shifted Gram.
    c1 = kron(kron(e01, e01), p0)
    c2 = kron(kron(e01, e01), p1)
    assert hs_inner(c1, c1) == 1
    assert hs_inner(c2, c2) == 1
    assert hs_inner(c1, c2) == 0
    gram = [
        [pair_sector_inner(c1, c1), pair_sector_inner(c1, c2)],
        [pair_sector_inner(c2, c1), pair_sector_inner(c2, c2)],
    ]
    assert gram == [
        [F(1, 3), F(1, 3)],
        [F(1, 3), F(1, 3)],
    ]
    shifted_determinant = (
        (F(2, 3) - gram[0][0]) * (F(2, 3) - gram[1][1])
        - gram[0][1] * gram[1][0]
    )
    assert shifted_determinant == 0

    print(
        "verified: rank-one pair-sector SOS, parity spectrum, and "
        "sharp shifted-Gram equality"
    )


if __name__ == "__main__":
    main()
