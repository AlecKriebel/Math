#!/usr/bin/env python3
"""Exact sparse check of the partial anchored-recursion counterexample."""

from collections import defaultdict
from fractions import Fraction


DIMS = (2, 3, 3, 3)  # K,H1,H2,H3
Index = tuple[int, int, int, int]
Entry = tuple[Index, Index]


def add_scaled(
    out: defaultdict[Entry, Fraction],
    x: dict[Entry, Fraction],
    scale: Fraction,
) -> None:
    for key, value in x.items():
        out[key] += scale * value


def trace_replace(
    x: dict[Entry, Fraction], site: int
) -> dict[Entry, Fraction]:
    """Return Tr_site(x) tensor I_site, preserving the tensor ordering."""
    out: defaultdict[Entry, Fraction] = defaultdict(Fraction)
    for (row, col), value in x.items():
        if row[site] != col[site]:
            continue
        for t in range(DIMS[site]):
            new_row = list(row)
            new_col = list(col)
            new_row[site] = t
            new_col[site] = t
            out[(tuple(new_row), tuple(new_col))] += value
    return dict(out)


def main() -> None:
    # sqrt(3)|U> has the six indicated unit-amplitude entries.  Therefore
    # P=|U><U| has coefficient 1/3 on every pair of these entries.
    u_support: list[Index] = []
    for j in range(3):
        u_support.append((0, j, j, 0))
        u_support.append((1, j, j, 2))
    p: dict[Entry, Fraction] = {
        (row, col): Fraction(1, 3)
        for row in u_support
        for col in u_support
    }

    e2 = trace_replace(p, 2)
    e3 = trace_replace(p, 3)
    e23 = trace_replace(e2, 3)
    n: defaultdict[Entry, Fraction] = defaultdict(Fraction)
    add_scaled(n, e23, Fraction(4))
    add_scaled(n, e2, Fraction(-2))
    add_scaled(n, e3, Fraction(-2))
    add_scaled(n, p, Fraction(1))

    # sqrt(3)|B> = sum_j |0,j,j,1>.  Divide the unnormalized quadratic
    # form by 3 to account for B's normalization.
    b_support: list[Index] = [(0, j, j, 1) for j in range(3)]
    rayleigh = sum(
        n[(row, col)] for row in b_support for col in b_support
    ) / 3
    assert rayleigh == Fraction(-2, 3)

    # Independent scalar check through D=(I/3) tensor |0><1|.
    d_norm_sq = Fraction(1, 3)
    tr_h2_norm_sq = Fraction(1)
    tr_h3_norm_sq = Fraction(0)
    tr_d_sq = Fraction(0)
    q2_d = (
        d_norm_sq
        - Fraction(1, 2) * (tr_h2_norm_sq + tr_h3_norm_sq)
        + Fraction(1, 4) * tr_d_sq
    )
    assert q2_d == Fraction(-1, 6)
    assert rayleigh == 4 * q2_d
    print("verified: partial anchored recursion has quotient -2/3")


if __name__ == "__main__":
    main()
