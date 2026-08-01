#!/usr/bin/env python3
"""Exact arithmetic checks for notes/simplex_voronoi_lemma.md.

This intentionally does not sample points or invoke an optimizer.  It checks
the rational identities and reduces every radical comparison to an integer
comparison after verifying signs.
"""

from fractions import Fraction as Q


def verify_dimension_four() -> None:
    # h_max = (8 - 4 sqrt(3))/5.  To show h_max < 3/10, it is
    # enough (with positive sides) to check 13 < 8 sqrt(3).
    assert Q(13) > 0 and Q(8) > 0
    assert 13 * 13 < 8 * 8 * 3

    # Four times the cell-ball squared radius is
    # 4 * (h_max/2 + 1/10) = (18 - 8 sqrt(3))/5.
    rational_part = Q(4) * (Q(8, 5) / 2 + Q(1, 10))
    radical_coefficient = Q(4) * (Q(-4, 5) / 2)
    assert rational_part == Q(18, 5)
    assert radical_coefficient == Q(-8, 5)

    # (18 - 8 sqrt(3))/5 < 1 is again 13 < 8 sqrt(3).
    assert Q(18) - Q(5) == Q(13)
    assert 13 * 13 < 8 * 8 * 3

    # Reflection obstruction in the edge-length-one simplex model:
    # ||q_i||^2=2/5 and <q_i,q_j>=-1/10.  The reflected point is
    # -(3/2)q_i.  It remains one unit from the opposite facet vertices,
    # but its squared distance from q_i is 5/2.
    opposite_edge_sq = Q(9, 4) * Q(2, 5) + Q(2, 5) - 2 * Q(3, 20)
    omitted_edge_sq = Q(5, 2) ** 2 * Q(2, 5)
    assert opposite_edge_sq == 1
    assert omitted_edge_sq == Q(5, 2)
    assert omitted_edge_sq > opposite_edge_sq


if __name__ == "__main__":
    verify_dimension_four()
    print("simplex Voronoi bound: exact checks passed")
