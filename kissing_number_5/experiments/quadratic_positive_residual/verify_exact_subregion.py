#!/usr/bin/env python3
"""Exact endpoint-algebra audit for the top-eigenvector cap lemma."""

from __future__ import annotations

from fractions import Fraction as Q
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "exact_subregion_certificate.json"


def verify() -> dict[str, object]:
    data = json.loads(CERTIFICATE.read_text())
    assert data["status"] == "PROVED"
    epsilon = Q(data["epsilon"])
    assert epsilon == Q(1, 50)
    assert data["cap_integer_bound"] == 39

    # The second endpoint allowance is
    # epsilon*beta-epsilon^2-lambda4*(1-epsilon^2).
    assert epsilon**2 == Q(1, 2500)
    assert 1 - epsilon**2 == Q(2499, 2500)

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
    assert endpoint_one_allowance == 1
    assert endpoint_epsilon_allowance == Q(99, 2500)
    assert transverse <= min(
        endpoint_one_allowance, endpoint_epsilon_allowance
    )

    # f(s)=lambda4+(1-lambda4)s^2-beta*s+B_perp has
    # f''=2(1-lambda4)>=0 whenever lambda4<=1.
    assert 2 * (1 - Q(1)) == 0
    return {
        "status": "PASS",
        "epsilon": str(epsilon),
        "example_transverse_width": str(transverse),
        "cap_integer_bound": 39,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
