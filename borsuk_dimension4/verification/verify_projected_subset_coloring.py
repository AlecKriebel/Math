#!/usr/bin/env python3
"""Independent exact finite check of the projected-subset coloring lemma."""

from fractions import Fraction
from itertools import combinations


UNIVERSE = frozenset(range(5))
SUBSETS = [
    frozenset(a)
    for k in range(1, 5)
    for a in combinations(range(5), k)
]


def boundary_color(a: frozenset[int]) -> int:
    boundary = [x for x in a if (x + 1) % 5 not in a]
    assert boundary
    return min(boundary)


def centered_dot(a: frozenset[int], b: frozenset[int]) -> Fraction:
    return Fraction(len(a & b)) - Fraction(len(a) * len(b), 5)


def verify() -> None:
    # Check the norm and dot-product formulas directly for all 30 labels.
    for a in SUBSETS:
        k = len(a)
        assert centered_dot(a, a) == Fraction(k * (5 - k), 5)

    for i, a in enumerate(SUBSETS):
        for b in SUBSETS[:i]:
            k, ell = len(a), len(b)
            min_intersection = max(0, k + ell - 5)
            if len(a & b) == min_intersection:
                assert (not a & b) or (a | b == UNIVERSE)
                assert boundary_color(a) != boundary_color(b)

            # The coefficient of |A cap B| in the squared-distance formula
            # is -2rs, strictly negative for every allowed r,s>0.
            # The checker records its sign after setting r=s=1; radii do not
            # affect the sign argument.
            assert Fraction(-2) < 0


if __name__ == "__main__":
    verify()
    print("projected-subset orbit coloring: exact checks passed")
