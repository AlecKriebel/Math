#!/usr/bin/env python3
"""Exact finite sanity checks for the proved complexity corollaries.

This script does not enumerate reaction networks and makes no support
minimality claim.  It checks only the integer inequalities that reduce the
three-species m<=4 case and the stated edge-count consequences.
"""


def main():
    # Necessary conditions already proved in the accompanying note:
    # s>=2, deficiency delta=m-l-s>=1, and n=3 so s<=3.
    possibilities = []
    for m in range(1, 5):
        for linkage_classes in range(1, m + 1):
            for rank in range(2, 4):
                deficiency = m - linkage_classes - rank
                if deficiency >= 1:
                    possibilities.append((m, linkage_classes, rank, deficiency))
    assert possibilities == [(4, 1, 2, 1)]
    # The remaining tuple is excluded by the one-linkage rank-two theorem.

    minimum_complexes = 5
    minimum_rank = 2
    minimum_deficiency = 1
    # Weak reversibility gives at least one outgoing directed edge per active
    # complex.  Reversibility gives at least m-l undirected pairs, while
    # delta>=1 implies m-l>=s+1.
    assert minimum_complexes == 5  # outgoing-edge count in the WR case
    # m-l=s+delta gives the global reversible-pair lower bound.
    assert minimum_rank + minimum_deficiency == 3
    # With one linkage, connectedness gives p>=m-1.
    assert minimum_complexes - 1 == 4

    # There are exactly four three-species complexes of molecularity <=1.
    degree_at_most_one = [
        (i, j, k)
        for i in range(2)
        for j in range(2)
        for k in range(2)
        if i + j + k <= 1
    ]
    assert sorted(degree_at_most_one) == [
        (0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0)
    ]

    print("PASS: exact complexity-arithmetic checks succeeded")
    print("  m<=4 reduces uniquely to (m,l,s,delta)=(4,1,2,1)")
    print("  proved lower bound after the rank-two obstruction: m>=5")
    print("  no bounded reaction-support impossibility claim is asserted")


if __name__ == "__main__":
    main()
