#!/usr/bin/env python3
"""Exact arithmetic verifier for the r=18 residual C5 q-energy bound."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE = ROOT / "certificates" / "r18_residual_q_energy.json"


class VerificationError(Exception):
    """Raised when an exact certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def rational(text: object, field: str) -> Fraction:
    require(isinstance(text, str), f"{field} must be a rational string")
    try:
        return Fraction(text)
    except (ValueError, ZeroDivisionError) as error:
        raise VerificationError(f"invalid rational in {field}") from error


def verify(path: Path = DEFAULT_CERTIFICATE) -> dict[str, object]:
    data = json.loads(path.read_text())
    require(
        data.get("schema") == "kissing5.r18_residual_q_energy.v1",
        "unexpected schema",
    )
    require(data.get("code_size") == 41, "unexpected code size")
    require(data.get("antipodal_pairs") == 18, "unexpected branch")
    require(data.get("residual_cycle_edges") == 5, "unexpected cycle size")

    coefficients = data.get("gegenbauer_coefficients")
    require(isinstance(coefficients, dict), "missing Gegenbauer coefficients")
    c0 = rational(coefficients.get("P0"), "P0")
    c2 = rational(coefficients.get("P2"), "P2")
    c4 = rational(coefficients.get("P4"), "P4")
    require(c2 > 0 and c4 > 0, "harmonic coefficients must be positive")

    # In dimension five:
    # P2(t)=(5t^2-1)/4 and P4(t)=(21t^4-14t^2+1)/8.
    t4 = c4 * Fraction(21, 8)
    t2 = c2 * Fraction(5, 4) - c4 * Fraction(14, 8)
    constant = c0 - c2 * Fraction(1, 4) + c4 * Fraction(1, 8)
    monomials = data.get("monomial_coefficients")
    require(isinstance(monomials, dict), "missing monomial coefficients")
    require(t4 == rational(monomials.get("t4"), "t4"), "wrong t^4 term")
    require(t2 == rational(monomials.get("t2"), "t2"), "wrong t^2 term")
    require(
        constant == rational(monomials.get("t0"), "t0"),
        "wrong constant term",
    )
    require(
        (t4, t2, constant)
        == (Fraction(256, 45), Fraction(-64, 45), Fraction(0)),
        "q(t) is not (64/45)t^2(4t^2-1)",
    )

    code_size = data["code_size"]
    ordered_pairs = code_size * (code_size - 1)
    total_lower = (
        c0 * ordered_pairs - code_size * (c2 + c4)
    )
    antipodal_ordered = 2 * data["antipodal_pairs"]
    q_minus_one = t4 + t2 + constant
    antipodal_contribution = antipodal_ordered * q_minus_one
    full_code_residual_lower = (total_lower - antipodal_contribution) / 2

    require(
        total_lower
        == rational(
            data.get("ordered_total_lower_bound"),
            "ordered_total_lower_bound",
        ),
        "wrong total lower bound",
    )
    require(
        antipodal_contribution
        == rational(
            data.get("ordered_antipodal_contribution"),
            "ordered_antipodal_contribution",
        ),
        "wrong antipodal contribution",
    )
    require(
        full_code_residual_lower
        == rational(
            data.get("full_code_unordered_residual_cycle_lower_bound"),
            "full_code_unordered_residual_cycle_lower_bound",
        ),
        "wrong full-code residual-cycle lower bound",
    )

    # Collapse each antipodal pair to one representative.  Giving each of
    # the 18 representatives weight lambda and each residual vertex weight
    # one gives
    #
    # 2 sum_cycle q(s_i) >=
    # c0(18 lambda+5)^2 - 18 q(1)lambda^2 - 5q(1).
    # The concave quadratic is maximized at lambda=5/3.
    representative_weight = rational(
        data.get("optimized_representative_weight"),
        "optimized_representative_weight",
    )
    require(
        representative_weight == Fraction(5, 3),
        "wrong optimized representative weight",
    )
    q_one = q_minus_one
    weighted_twice_residual = (
        c0 * (18 * representative_weight + 5) ** 2
        - 18 * q_one * representative_weight**2
        - 5 * q_one
    )
    weighted_residual_lower = weighted_twice_residual / 2
    require(
        weighted_residual_lower
        == rational(
            data.get("weighted_unordered_residual_cycle_lower_bound"),
            "weighted_unordered_residual_cycle_lower_bound",
        ),
        "wrong optimized weighted residual-cycle lower bound",
    )
    require(
        rational(data.get("copositive_constant"), "copositive_constant")
        == Fraction(32, 45),
        "wrong copositive constant",
    )
    require(
        weighted_residual_lower > full_code_residual_lower > 0,
        "optimized weighted bound must strictly improve the full-code bound",
    )

    return {
        "status": "PASS",
        "polynomial": "(64/45)*t^2*(4*t^2-1)",
        "ordered_total_lower_bound": str(total_lower),
        "full_code_unordered_residual_cycle_lower_bound": str(
            full_code_residual_lower
        ),
        "weighted_unordered_residual_cycle_lower_bound": str(
            weighted_residual_lower
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
