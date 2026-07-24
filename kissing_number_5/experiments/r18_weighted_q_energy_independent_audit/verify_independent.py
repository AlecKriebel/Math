#!/usr/bin/env python3
"""Independent exact audit of the r=18 weighted q-energy calculation."""

from __future__ import annotations

from fractions import Fraction as Q
import json


class AuditError(Exception):
    """An always-on independent audit check failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def verify() -> dict[str, object]:
    c0 = Q(64, 315)
    c2 = Q(256, 135)
    c4 = Q(2048, 945)

    # Re-expand q from the dimension-five normalized Gegenbauer basis.
    t4 = c4 * Q(21, 8)
    t2 = c2 * Q(5, 4) - c4 * Q(14, 8)
    t0 = c0 - c2 * Q(1, 4) + c4 * Q(1, 8)
    require(
        (t4, t2, t0) == (Q(256, 45), Q(-64, 45), Q(0)),
        "incorrect monomial expansion",
    )
    require(c2 > 0 and c4 > 0, "nonconstant harmonic coefficients")
    q_one = t4 + t2 + t0
    require(q_one == Q(64, 15), "incorrect q(1)")

    # Closed-interval sign certificate:
    # q=(64/45)u(4u-1), 0<=u<=1/4.
    require(Q(64, 45) > 0, "wrong leading factor")
    require(4 * Q(1, 4) - 1 == 0, "wrong interval endpoint")
    boundary_values = {
        "-1/2": t4 * Q(1, 16) + t2 * Q(1, 4) + t0,
        "0": t0,
        "1/2": t4 * Q(1, 16) + t2 * Q(1, 4) + t0,
    }
    require(
        set(boundary_values.values()) == {Q(0)},
        "q must vanish at all sign-boundary test points",
    )
    require(
        t4 * Q(1, 256) + t2 * Q(1, 16) + t0 < 0,
        "q must be negative at t=1/4",
    )

    # Full-code ordered/unordered calculation.
    n = 41
    antipodal_pairs = 18
    residual_edges = 5
    ordered_total_lower = c0 * n * (n - 1) - n * (c2 + c4)
    antipodal_ordered_count = 2 * antipodal_pairs
    antipodal_ordered_contribution = antipodal_ordered_count * q_one
    residual_unordered_lower = (
        ordered_total_lower - antipodal_ordered_contribution
    ) / 2
    require(ordered_total_lower == Q(10496, 63), "equation (9)")
    require(
        antipodal_ordered_count == 36
        and antipodal_ordered_contribution == Q(768, 5),
        "equation (10) ordered antipodal factor",
    )
    require(residual_edges * 2 == 10, "ordered cycle-edge factor")
    require(residual_unordered_lower == Q(2048, 315), "equation (11)")

    # General residual weights: A=sum a_i and S2=sum a_i^2.
    # R(lambda)=r2 lambda^2+r1*A lambda+rA*A^2+rS*S2.
    r2 = c0 * 18**2 - 18 * q_one
    r1 = c0 * 2 * 18
    rA = c0
    rS = -q_one
    require(
        (r2, r1, rA, rS)
        == (Q(-384, 35), Q(256, 35), Q(64, 315), Q(-64, 15)),
        "wrong arbitrary-weight quadratic",
    )
    require(r2 < 0, "representative-weight quadratic must be concave")

    # Vertex lambda=(-r1*A)/(2*r2)=A/3.  It is nonnegative whenever
    # residual weights are nonnegative (A>=0), including A=0.
    lambda_per_A = -r1 / (2 * r2)
    require(lambda_per_A == Q(1, 3), "wrong optimizing weight")
    optimized_A2 = (
        r2 * lambda_per_A**2 + r1 * lambda_per_A + rA
    )
    require(
        (optimized_A2, rS) == (Q(64, 45), Q(-64, 15)),
        "wrong optimized arbitrary-weight coefficients",
    )
    copositive_constant = optimized_A2 / 2
    require(copositive_constant == Q(32, 45), "equation (15)")

    # Unit residual weights: A=S2=5.
    unit_residual_lower = (
        optimized_A2 * 5**2 + rS * 5
    ) / 2
    require(unit_residual_lower == Q(64, 9), "equation (14)")

    # Edge-depth corollary.  Let U=(1+sqrt(17))/8.  In Q(sqrt(17)),
    # check 4U^2-U-1=0 coefficientwise and U>1/4.
    u_const = Q(1, 8)
    u_radical = Q(1, 8)
    u2_const = u_const**2 + 17 * u_radical**2
    u2_radical = 2 * u_const * u_radical
    threshold_poly = (
        4 * u2_const - u_const - 1,
        4 * u2_radical - u_radical,
    )
    require(threshold_poly == (Q(0), Q(0)), "wrong edge threshold")
    require(
        u_const == Q(1, 8)
        and u_radical > 0
        and 17 > 1,
        "U must exceed 1/4",
    )
    average_q = unit_residual_lower / residual_edges
    require(average_q == Q(64, 45), "wrong five-edge average")

    return {
        "status": "PASS",
        "ordered_antipodal_count": antipodal_ordered_count,
        "ordered_cycle_count": 2 * residual_edges,
        "closed_interval_boundary_values": {
            key: str(value) for key, value in boundary_values.items()
        },
        "representative_weight": "A/3",
        "copositive_constant": str(copositive_constant),
        "unit_weight_cycle_lower_bound": str(unit_residual_lower),
        "forced_edge_threshold": "-sqrt((1+sqrt(17))/8)",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
