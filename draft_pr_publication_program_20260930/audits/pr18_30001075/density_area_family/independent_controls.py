#!/usr/bin/env python3
"""Exact audit controls, not a finite substitute for the analytic proof."""
import json
from fractions import Fraction as Q


def det(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def add_at(a, b, z):
    return [[a[i][j] + z * b[i][j] for j in range(2)] for i in range(2)]


def run():
    receipts = []
    # Exact two-contact rectangle family: q=(s,t), u=(0,s), v=(t,-s).
    a = [[0, 0], [1, 0]]
    b = [[0, 1], [-1, 0]]
    for z in [Q(-2), Q(0), Q(1, 2), Q(1), Q(3)]:
        assert det(add_at(a, b, z)) == z * (z - 1)
    assert det(add_at(a, b, 0)) == det(add_at(a, b, 1)) == 0
    assert det(add_at(a, b, Q(1, 2))) == Q(-1, 4)
    receipts.append({"name": "two_contact_polynomial_control", "passed": True,
                     "roots": [0, 1], "midpoint_determinant": "-1/4"})

    # This volume is for an injective explicit countercontrol only. The proof
    # being audited uses the noninjective area formula and does not need this.
    volume = 4 * (Q(1, 2) - Q(1, 3))
    assert volume == Q(2, 3)
    receipts.append({"name": "two_rectangle_sweep_volume", "passed": True,
                     "volume": str(volume)})

    # Three distinct roots force every degree <=2 coefficient to vanish:
    # det of the three evaluation rows is the nonzero Vandermonde product.
    z = [Q(-7, 5), Q(2, 3), Q(11, 2)]
    rows = [[Q(1), x, x*x] for x in z]
    vandermonde = ((rows[0][0] * (rows[1][1] * rows[2][2] - rows[1][2] * rows[2][1]))
                  - (rows[0][1] * (rows[1][0] * rows[2][2] - rows[1][2] * rows[2][0]))
                  + (rows[0][2] * (rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0])))
    assert vandermonde == (z[1]-z[0])*(z[2]-z[0])*(z[2]-z[1]) != 0
    receipts.append({"name": "three_distinct_heights_vandermonde_control", "passed": True,
                     "determinant": str(vandermonde)})

    # Dropping tangency: the vertical-intersection family has A=I, B=0.
    identity = [[1, 0], [0, 1]]
    zero = [[0, 0], [0, 0]]
    assert all(det(add_at(identity, zero, x)) == 1 for x in [-9, 0, 3, 6, 9])
    assert Q(1, 2) + Q(1, 2) < 3  # three balls really are pairwise disjoint
    receipts.append({"name": "intersection_instead_of_tangency_control", "passed": True,
                     "swept_jacobian": 1})

    # Dropping disjointness: all point contacts can have one repeated root.
    assert det(add_at(zero, identity, 0)) == 0
    assert det(add_at(zero, identity, 1)) == 1
    receipts.append({"name": "repeated_height_control", "passed": True,
                     "polynomial": "z^2"})

    # Rank-one identity does not mean stationary lines; one common image
    # direction permits nonzero A and B with determinant identically zero.
    rankone_a = [[1, 2], [3, 6]]
    rankone_b = [[2, -1], [6, -3]]
    assert all(det(add_at(rankone_a, rankone_b, x)) == 0
               for x in [Q(-4), Q(0), Q(1, 7), Q(10)])
    receipts.append({"name": "nonstationary_rank_one_control", "passed": True})

    return {"scope": "exact finite controls for reconstructed analytic audit",
            "analytic_proof_certified_by_code": False,
            "checks": receipts, "check_count": len(receipts),
            "all_passed": all(x["passed"] for x in receipts)}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
