#!/usr/bin/env python3
"""Exact checker for the compensated inertia-(2,2) obstruction.

Only Python's standard library is used.  Matrices are represented by
lists of Fractions.  The checker constructs

    H = |0><0| tensor (|0><0| tensor I - I tensor |0><0|)

and verifies its rank/signature, Q_3(H)=-1, vanishing 011 sector, and
therefore 2 Q_3(H)+3 w_011(H)=-2.
"""

from fractions import Fraction as F
from itertools import combinations, product


D = 3
N = 3


def index(digits):
    out = 0
    for digit in digits:
        out = D * out + digit
    return out


def diagonal_h():
    values = [F(0) for _ in range(D**N)]
    for i, j, k in product(range(D), repeat=N):
        value = 0
        if i == 0:
            if j == 0:
                value += 1
            if k == 0:
                value -= 1
        values[index((i, j, k))] = F(value)
    return values


def partial_trace_diagonal(values, traced):
    traced = tuple(sorted(traced))
    remaining = tuple(i for i in range(N) if i not in traced)
    out = {}
    for rem_digits in product(range(D), repeat=len(remaining)):
        total = F(0)
        for tr_digits in product(range(D), repeat=len(traced)):
            digits = [0] * N
            for pos, site in enumerate(remaining):
                digits[site] = rem_digits[pos]
            for pos, site in enumerate(traced):
                digits[site] = tr_digits[pos]
            total += values[index(tuple(digits))]
        out[rem_digits] = total
    return out


def norm_squared_diagonal(values):
    return sum((value * value for value in values), F(0))


def endpoint_q3(values):
    out = F(0)
    sites = tuple(range(N))
    for size in range(N + 1):
        for traced in combinations(sites, size):
            reduced = partial_trace_diagonal(values, traced)
            out += F(-1, 2) ** size * norm_squared_diagonal(
                reduced.values()
            )
    return out


def scalar_projection_site(values, site):
    """Apply P_0(A)=Tr(A) I/3 at one local operator factor."""
    out = [F(0) for _ in values]
    other = tuple(i for i in range(N) if i != site)
    for row_other in product(range(D), repeat=len(other)):
        trace = F(0)
        for local in range(D):
            digits = [0] * N
            digits[site] = local
            for pos, other_site in enumerate(other):
                digits[other_site] = row_other[pos]
            trace += values[index(tuple(digits))]
        scalar = trace / D
        for local in range(D):
            digits = [0] * N
            digits[site] = local
            for pos, other_site in enumerate(other):
                digits[other_site] = row_other[pos]
            out[index(tuple(digits))] = scalar
    return out


def traceless_projection_site(values, site):
    scalar = scalar_projection_site(values, site)
    return [value - scalar_value for value, scalar_value in zip(values, scalar)]


def main():
    h = diagonal_h()

    positive = sum(value > 0 for value in h)
    negative = sum(value < 0 for value in h)
    rank = sum(value != 0 for value in h)
    assert (positive, negative, rank) == (2, 2, 4)
    assert norm_squared_diagonal(h) == 4

    q3 = endpoint_q3(h)
    assert q3 == -1

    sector_011 = scalar_projection_site(h, 0)
    sector_011 = traceless_projection_site(sector_011, 1)
    sector_011 = traceless_projection_site(sector_011, 2)
    w011 = norm_squared_diagonal(sector_011)
    assert w011 == 0

    compensated = 2 * q3 + 3 * w011
    assert compensated == -2

    print("rank(H) =", rank)
    print("inertia(H) =", (positive, negative))
    print("Q3(H) =", q3)
    print("w_011(H) =", w011)
    print("2 Q3(H) + 3 w_011(H) =", compensated)


if __name__ == "__main__":
    main()
