#!/usr/bin/env python3
"""Integer/rational checker for the crossed-energy obstruction."""

from fractions import Fraction


Word = tuple[int, int, int]


def kernel(x: Word, y: Word, xp: Word, yp: Word) -> Fraction:
    """Three-copy matrix-unit endpoint Gram."""

    value = Fraction(1)
    for a, b, c, d in zip(x, y, xp, yp):
        value *= (
            int(a == c and b == d)
            - Fraction(1, 2) * int(a == b and c == d)
        )
    return value


def pairing(
    left_row: tuple[Word, Word],
    left_column: tuple[Word, Word],
    right_row: tuple[Word, Word],
    right_column: tuple[Word, Word],
) -> Fraction:
    """Pairing of normalized equal superpositions.

    Each dyad coefficient is 1/2, hence the four-coefficient product
    contributes the common factor 1/4.
    """

    return Fraction(1, 4) * sum(
        kernel(x, y, xp, yp)
        for x in left_row
        for y in left_column
        for xp in right_row
        for yp in right_column
    )


def main() -> None:
    u0 = ((0, 0, 0), (0, 1, 1))
    u1 = ((1, 0, 0), (1, 1, 2))
    v0 = ((0, 0, 0), (0, 1, 2))
    v1 = ((1, 0, 0), (1, 1, 1))

    assert set(u0).isdisjoint(u1)
    assert set(v0).isdisjoint(v1)

    e00 = pairing(u0, v0, u0, v0)
    e01 = pairing(u0, v1, u0, v1)
    e10 = pairing(u1, v0, u1, v0)
    e11 = pairing(u1, v1, u1, v1)
    cross = pairing(u0, v0, u1, v1)

    assert (e00, e01, e10, e11) == (
        Fraction(11, 32),
        Fraction(3, 4),
        Fraction(3, 4),
        Fraction(11, 32),
    )
    assert cross == Fraction(-1, 32)

    minimum = Fraction(1, 8)
    tradeoff_defect = (
        e00 * e11
        - (e01 - minimum) * (e10 - minimum)
    )
    assert tradeoff_defect == Fraction(-279, 1024)

    true_rank_two_energy = e00 + e11 + 2 * cross
    assert true_rank_two_energy == Fraction(5, 8)
    assert true_rank_two_energy > 0

    print(
        "verified: crossed-energy tradeoff defect = -279/1024, "
        "actual interference = -1/32, Q3(E0+E1) = 5/8"
    )


if __name__ == "__main__":
    main()
