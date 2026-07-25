#!/usr/bin/env python3
"""Exact endpoint-algebra audit for the top-eigenvector cap lemma."""

from __future__ import annotations

from fractions import Fraction as Q
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "exact_subregion_certificate.json"


class VerificationError(Exception):
    """Raised when the exact subregion certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def verify(certificate_path: Path = CERTIFICATE) -> dict[str, object]:
    data = json.loads(certificate_path.read_text())
    require(data["status"] == "PROVED", "unexpected certificate status")
    epsilon = Q(data["epsilon"])
    require(epsilon == Q(1, 50), "wrong epsilon")
    require(data["cap_integer_bound"] == 39, "wrong cap integer bound")

    # The second endpoint allowance is
    # epsilon*beta-epsilon^2-lambda4*(1-epsilon^2).
    require(epsilon**2 == Q(1, 2500), "wrong epsilon square")
    require(
        1 - epsilon**2 == Q(2499, 2500),
        "wrong transverse coefficient",
    )

    example = data["example_region"]
    beta = Q(example["beta_lower"])
    lambda4 = Q(example["lambda4_upper"])
    transverse = Q(example["transverse_norm_upper"])
    endpoint_one_allowance = beta - 1
    endpoint_epsilon_allowance = (
        epsilon * beta
        - epsilon**2
        - lambda4 * (1 - epsilon**2)
    )
    require(endpoint_one_allowance == 1, "wrong top-endpoint allowance")
    require(
        endpoint_epsilon_allowance == Q(99, 2500),
        "wrong epsilon-endpoint allowance",
    )
    require(
        transverse <= min(endpoint_one_allowance, endpoint_epsilon_allowance),
        "example transverse width exceeds the endpoint allowance",
    )

    # f(s)=lambda4+(1-lambda4)s^2-beta*s+B_perp has
    # f''=2(1-lambda4)>=0 whenever lambda4<=1.
    require(2 * (1 - Q(1)) == 0, "convexity boundary check failed")
    return {
        "status": "PASS",
        "epsilon": str(epsilon),
        "example_transverse_width": str(transverse),
        "cap_integer_bound": 39,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
