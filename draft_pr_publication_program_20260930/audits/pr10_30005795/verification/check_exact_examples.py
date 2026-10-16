#!/usr/bin/env python3
"""Exact arithmetic checks of independently derived audit examples.

The geometric derivations in EXACT_EXAMPLES.md and lct_family/LCT_AUDIT.md
are the certificates of resolution data; these computations check their
arithmetic and a nonzero Fano-family integral, not the general theorem.
"""
from fractions import Fraction as Q
import json


def integrate_polynomial(coefficients, left, right):
    return sum((Q(c, i + 1) * (right ** (i + 1) - left ** (i + 1))
                for i, c in enumerate(coefficients)), Q(0))


def threshold(data):
    ratios = [Q(a, m) for a, m in data if m > 0]
    c = min(ratios)
    assert all(Q(a) - c * m >= 0 for a, m in data)
    assert any(Q(a) - c * m == 0 for a, m in data if m > 0)
    return c


def main():
    # For Bl_line P^3 with S a plane fiber: w*f=(4-u)^2*(u-1)/18
    # on [1,4], and zero on [0,1].
    integral = integrate_polynomial([Q(-16, 18), Q(24, 18),
                                     Q(-9, 18), Q(1, 18)], Q(1), Q(4))
    assert integral == Q(3, 8)
    # The two nef pieces agree at u=1; the endpoint weight is zero.
    assert Q((4-1)**2, 18) == Q(1, 2)
    assert Q((4-4)**2, 18) == 0
    assert 4**3 + 12*(-1) - (-2) == 54
    # The surface boundary is (3/8)*a smooth line, threshold 8/3.
    surface_threshold = threshold([(1, integral), (2, integral)])
    assert surface_threshold == Q(8, 3)
    assert 1/surface_threshold == integral

    transverse = threshold([(1, Q(1, 2)), (1, Q(1, 2)), (2, 1)])
    tangent = threshold([(1, 1), (1, 1), (2, 2), (3, 4)])
    du_val = threshold([(1, 1), (1, 2)])
    assert (transverse, tangent, du_val) == (Q(2), Q(3, 4), Q(1, 2))
    print(json.dumps({
        "status": "PASS",
        "fano_example": {"anticanonical_volume": 54, "tau": 4,
                         "integral_and_optimal_constant": str(integral),
                         "boundary_threshold": str(surface_threshold)},
        "resolution_thresholds": {"transverse": str(transverse),
                                  "tangent": str(tangent),
                                  "du_val_nonreduced": str(du_val)},
        "limitation": "Arithmetic checks depend on the separately derived geometry."
    }, indent=2))


if __name__ == "__main__":
    main()
