#!/usr/bin/env python3
"""Exact checks for notes/route_c_explicit_high_radius_band.md.

Only rational integer arithmetic is used.  The sole radical comparison is
verified by checking positivity and then comparing its square.
"""

from fractions import Fraction as Q


def verify_defect_to_distortion() -> None:
    epsilon = Q(1, 100000)

    # The weight term gives |lambda_i - 1/5|^2 < 2 epsilon < (1/10)^2.
    assert 2 * epsilon == Q(1, 50000)
    assert 2 * epsilon < Q(1, 10) ** 2

    # Hence lambda_i lambda_j > 1/100, and each squared-edge defect is
    # below epsilon/(1/100) = 1/1000.
    eta_endpoint = epsilon / Q(1, 100)
    assert eta_endpoint == Q(1, 1000)

    # Lemma 1 converts this to squared-norm distortion tau < 8 eta.
    tau_endpoint = 8 * eta_endpoint
    assert tau_endpoint == Q(1, 125)


def verify_cell_endpoint() -> None:
    tau = Q(1, 125)
    a = tau / (1 - tau)
    b = 3 + 5 * a
    assert a == Q(1, 124)
    assert b == Q(377, 124)

    # At tau=1/125, equation (23) is
    # rho^2 = rational_part - (4/5) sqrt(377/620).
    rational_part = b / 5 + Q(4, 25) + Q(4, 5) * a + Q(8, 125)
    radical_coefficient = Q(4, 5)
    radicand = Q(377, 620)
    assert rational_part == Q(12997, 15500)

    # The needed comparison is rho^2 < 125/504.  After moving the radical,
    # L < (4/5) sqrt(377/620), both sides are positive.
    target = Q(125, 504)
    left = rational_part - target
    assert left == Q(1153247, 1953000)
    assert left > 0 and radical_coefficient > 0 and radicand > 0

    square_margin = radical_coefficient**2 * radicand - left**2
    assert square_margin == Q(154363852991, 3814209000000)
    assert square_margin > 0

    # Four times the forward metric factor at the endpoint takes the target
    # exactly to one, so the strict radical margin proves Gamma^2 < 1.
    assert 4 * (1 + tau) * target == 1


def verify_gram_constants() -> None:
    # In the four-edge basis, an entrywise Gram error <= eta implies
    # |c^T E c| <= eta ||c||_1^2 <= 4 eta ||c||_2^2.
    dimension = 4
    l1_to_l2_sq = Q(dimension)

    # The regular edge Gram matrix is (I+J)/2 and has minimum eigenvalue 1/2.
    regular_min_eigenvalue = Q(1, 2)
    distortion_multiplier = l1_to_l2_sq / regular_min_eigenvalue
    assert distortion_multiplier == 8


if __name__ == "__main__":
    verify_defect_to_distortion()
    verify_gram_constants()
    verify_cell_endpoint()
    print("explicit high-radius band: exact checks passed")
