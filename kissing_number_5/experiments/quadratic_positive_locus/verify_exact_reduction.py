#!/usr/bin/env python3
"""Exact arithmetic audit of the quadratic-positive-locus reduction.

This verifier checks constants, hashes, endpoint algebra, and the summation
that imports the existing robust-cap theorem.  The spectral theorem and
strict-separation theorem used in the accompanying proof are ordinary human
mathematics, not finite computations masquerading as verification.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "exact_reduction_certificate.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def q_minus(t: Q, beta: Q) -> Q:
    return 1 - 5 * t * t + beta * t


def q_plus(t: Q, beta: Q) -> Q:
    return 5 * t * t - 1 + beta * t


def verify() -> dict[str, object]:
    data = json.loads(CERTIFICATE.read_text())
    assert data["status"].startswith("PROVED REDUCTION")
    assert data["dimension"] == 5
    assert data["hypothetical_code_size"] == 41

    cap = data["robust_cap"]
    assert Q(cap["minimum_height"]) == -Q(1, 50)
    assert cap["maximum_occupancy"] == 39 < 41
    source = ROOT / cap["source_certificate"]
    assert source.is_file()
    assert sha256(source) == cap["source_certificate_sha256"]
    source_data = json.loads(source.read_text())
    assert source_data["status"] == "COMPUTATIONALLY CERTIFIED"
    assert Q(source_data["minimum_height"]) == -Q(1, 50)
    assert Q(source_data["resulting_real_objective"]) < 40
    assert source_data["resulting_integer_bound"] == 39

    canonical = data["canonical_normalization"]
    assert Q(canonical["largest_eigenvalue"]) == 1
    assert [Q(value) for value in canonical["ordered_eigenvalue_interval"]] == [
        -4,
        1,
    ]
    assert [
        Q(value) for value in canonical["linear_norm_residual_interval"]
    ] == [0, 50]

    # At ||b||=50, q(x)>0 and x^T A x<=1 force
    # <b/||b||,x> > -1/50.  The inequality is strict even at the endpoint.
    b_norm = Q(50)
    cap_floor = -Q(1, 50)
    assert 1 + b_norm * cap_floor == 0

    # The lowest possible eigenvalue after lambda_max=1 and trace(A)=0 is
    # -4: four other eigenvalues can contribute at most four.
    dimension = data["dimension"]
    assert -(dimension - 1) == -4

    families = data["axisymmetric_families"]
    beta_transition = Q(4)
    # Both root transitions occur at an endpoint t=+/-1.
    assert q_minus(Q(1), beta_transition) == 0
    assert q_plus(Q(-1), beta_transition) == 0

    # q_-(t) has its lower root at -1/50 precisely at beta=499/10.
    beta_robust = Q(499, 10)
    assert q_minus(-Q(1, 50), beta_robust) == 0
    assert beta_robust < 50
    assert (
        families["belt_to_cap"]["certified_occupancy_39_range"]
        == "beta >= 499/10"
    )

    # q_+(t), beta>=4, is positive only above its positive root, hence in
    # the open northern hemisphere and therefore in the robust cap.
    assert families["two_caps_to_cap"]["certified_occupancy_39_range"] == (
        "beta >= 4"
    )

    return {
        "status": "PASS",
        "source_cap_certificate_sha256": sha256(source),
        "general_linear_dominance_threshold": "50",
        "axisymmetric_q_minus_threshold": "499/10",
        "axisymmetric_q_plus_threshold": "4",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
