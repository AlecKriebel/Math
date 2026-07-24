#!/usr/bin/env python3
"""Verify the exact H1 spectral-variance lattice on the quarter grid.

This is a deliberately small, standard-library verifier.  It checks only
the arithmetic consequence of quarter-grid pair counts and rank at most
five.  It does not certify that an arbitrary spherical code has quarter-grid
inner products.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE = (
    ROOT / "certificates" / "quarter_grid_h1_variance_lattice.json"
)


class VerificationError(ValueError):
    """Raised when an exact certificate check fails."""


def check(condition: bool, message: str) -> None:
    """Proof-critical check that remains active under ``python -O``."""

    if not condition:
        raise VerificationError(message)


def ceil_fraction(value: Q) -> int:
    """Return the exact ceiling of a rational number."""

    return -((-value.numerator) // value.denominator)


def verify(certificate_path: Path = DEFAULT_CERTIFICATE) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    check(
        certificate["schema"]
        == "kissing5.quarter_grid_h1_variance_lattice.v1",
        "unexpected certificate schema",
    )
    cardinality = int(certificate["cardinality"])
    denominator = int(certificate["grid_denominator"])
    rank_bound = int(certificate["rank_bound"])
    numerators = [int(value) for value in certificate["grid_numerators"]]
    check(cardinality == 41, "cardinality must be 41")
    check(denominator == 4, "grid denominator must be four")
    check(rank_bound == 5, "rank bound must be five")
    check(
        numerators == list(range(-4, 3)),
        "quarter-grid numerator set is incorrect",
    )

    # If n_m counts unordered pairs with inner product m/4, then the
    # ordered pair distribution is alpha_m=2*n_m/41.  Thus
    # E=sum alpha_m(m/4)^2=Q/328 for Q=sum n_m*m^2.
    energy_denominator = cardinality * denominator**2 // 2
    check(energy_denominator == 328, "energy denominator is not 328")
    check(
        certificate["energy_integer"] == "Q=sum_m n_m*m^2",
        "energy-integer definition changed",
    )
    check(
        certificate["energy_formula"] == "E=Q/328",
        "energy formula changed",
    )

    # tr(G^2)=41+2*Q/16=41+Q/8.  Padding the nonzero spectrum
    # with zeros to five entries gives
    # V=sum_{a=1}^5(lambda_a-41/5)^2=tr(G^2)-41^2/5.
    trace_q_coefficient = Q(2, denominator**2)
    trace_constant = Q(cardinality)
    variance_constant = trace_constant - Q(cardinality**2, rank_bound)
    variance_q_coefficient = trace_q_coefficient
    check(trace_q_coefficient == Q(1, 8), "trace Q coefficient is wrong")
    check(
        certificate["trace_square_formula"] == "tr(G^2)=41+Q/8",
        "trace-square formula changed",
    )
    check(
        variance_constant == Q(-11808, 40),
        "variance constant is wrong",
    )
    check(
        variance_q_coefficient == Q(5, 40),
        "variance Q coefficient is wrong",
    )
    check(
        certificate["spectral_variance_formula"] == "V=(5Q-11808)/40",
        "spectral-variance formula changed",
    )
    check(
        certificate["scaled_variance"] == "X=40V=5Q-11808",
        "scaled-variance formula changed",
    )
    residue = (-11808) % 5
    check(residue == 2, "internal residue computation failed")
    check(
        certificate["scaled_variance_residue_mod_5"] == residue,
        "recorded scaled-variance residue is wrong",
    )

    minimum_q = ceil_fraction(Q(11808, 5))
    expected_levels = []
    for q_value in range(minimum_q, minimum_q + 4):
        x_value = 5 * q_value - 11808
        variance = Q(x_value, 40)
        energy = Q(q_value, energy_denominator)
        expected_levels.append(
            {
                "Q": q_value,
                "X": x_value,
                "V": str(variance),
                "E": str(energy),
            }
        )
    check(
        certificate["first_nonnegative_levels"] == expected_levels,
        "first nonnegative variance levels are incorrect",
    )

    allowed = [
        level for level in expected_levels if Q(level["V"]) <= Q(3, 10)
    ]
    consequence = certificate["closed_low_variance_consequence"]
    check(
        consequence["hypothesis"] == "0<=V<=3/10",
        "low-variance hypothesis changed",
    )
    check(
        consequence["allowed_V"] == [level["V"] for level in allowed],
        "allowed low-variance values are incorrect",
    )
    check(
        consequence["allowed_Q"] == [level["Q"] for level in allowed],
        "allowed low-variance Q values are incorrect",
    )
    return {
        "energy_denominator": energy_denominator,
        "scaled_variance_residue_mod_5": residue,
        "minimum_Q_from_rank": minimum_q,
        "allowed_V_at_most_3_over_10": consequence["allowed_V"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate", nargs="?", type=Path, default=DEFAULT_CERTIFICATE
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
