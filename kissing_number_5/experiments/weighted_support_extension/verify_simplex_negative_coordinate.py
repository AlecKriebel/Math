#!/usr/bin/env python3
"""Exact algebra audit for the regular-simplex extension threshold."""

from __future__ import annotations

from fractions import Fraction as Q
import json


class VerificationError(Exception):
    """Raised when an exact support-six check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def add(x: tuple[Q, Q], y: tuple[Q, Q]) -> tuple[Q, Q]:
    return (x[0] + y[0], x[1] + y[1])


def scale(c: Q, x: tuple[Q, Q]) -> tuple[Q, Q]:
    return (c * x[0], c * x[1])


def is_positive(x: tuple[Q, Q]) -> bool:
    """Return the exact sign test x[0]+x[1]*sqrt(15)>0."""
    a, b = x
    if b == 0:
        return a > 0
    if b < 0:
        return not is_positive((-a, -b))
    if a >= 0:
        return True
    return 15 * b * b > a * a


def verify(
    rho_constant: Q = Q(1, 4),
    rho_radical: Q = Q(1, 20),
) -> dict[str, object]:
    # rho=(5+sqrt(15))/20 is represented in Q(sqrt(15)) by the pair
    # constant + radical_coefficient*sqrt(15).
    constant = rho_constant
    radical = rho_radical
    require(
        (constant, radical) == (Q(1, 4), Q(1, 20)),
        "unexpected rho representation",
    )

    # Multiplication in Q(sqrt(15)).
    rho_squared_constant = constant**2 + 15 * radical**2
    rho_squared_radical = 2 * constant * radical
    require(
        (rho_squared_constant, rho_squared_radical)
        == (Q(1, 10), Q(1, 40)),
        "incorrect square of rho",
    )

    polynomial_constant = (
        12 * rho_squared_constant - 6 * constant + Q(3, 10)
    )
    polynomial_radical = 12 * rho_squared_radical - 6 * radical
    require(
        polynomial_constant == polynomial_radical == 0,
        "rho does not satisfy its defining quadratic",
    )

    # The unique feasible vertex regime at rho in (1/4,1/2) has two upper
    # endpoints, three lower endpoints, and one free coordinate 3rho-1.
    require(radical > 0, "rho must exceed 1/4")
    require(15 < 25, "sqrt(15) must be less than 5")
    # The free coordinate c=3rho-1 lies strictly between -rho and 1/2:
    # c+rho=4rho-1=sqrt(15)/5>0 and
    # 1/2-c=3(5-sqrt(15))/20>0.
    require(
        4 * constant - 1 == 0 and 4 * radical > 0,
        "free-coordinate lower-bound comparison failed",
    )
    require(15 < 25, "free-coordinate upper-bound comparison failed")

    rho = (constant, radical)
    lower = scale(Q(-1), rho)
    upper = (Q(1, 2), Q(0))
    vertex_cases: list[dict[str, object]] = []
    feasible_k: list[int] = []
    for k in range(6):
        free = add(scale(Q(5 - k), rho), (Q(-k, 2), Q(0)))
        above_lower = is_positive(add(free, scale(Q(-1), lower)))
        below_upper = is_positive(add(upper, scale(Q(-1), free)))
        feasible = above_lower and below_upper
        if feasible:
            feasible_k.append(k)
        vertex_cases.append(
            {
                "upper_endpoints": k,
                "free_coordinate": (
                    str(free[0])
                    if free[1] == 0
                    else f"{free[0]}+({free[1]})*sqrt(15)"
                ),
                "feasible": feasible,
            }
        )
    require(feasible_k == [2], "endpoint-case enumeration is not unique")

    # Its squared norm is 6/5 by the polynomial identity.
    vertex_norm_constant = (
        Q(1, 2)
        + 9 * rho_squared_constant
        - 6 * constant
        + 1
        + 3 * rho_squared_constant
    )
    vertex_norm_radical = (
        9 * rho_squared_radical - 6 * radical + 3 * rho_squared_radical
    )
    require(
        (vertex_norm_constant, vertex_norm_radical) == (Q(6, 5), Q(0)),
        "feasible vertex has wrong squared norm",
    )
    return {
        "status": "PASS",
        "rho": "(5+sqrt(15))/20",
        "minimal_polynomial": "12*rho^2-6*rho+3/10",
        "vertex_cases": vertex_cases,
        "unique_feasible_endpoint_count": 2,
        "vertex_squared_norm": "6/5",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
