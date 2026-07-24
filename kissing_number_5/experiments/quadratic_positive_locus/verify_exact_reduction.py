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


class VerificationError(Exception):
    """Raised when the exact positive-locus reduction audit fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


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


def verify(certificate_path: Path = CERTIFICATE) -> dict[str, object]:
    data = json.loads(certificate_path.read_text())
    require(
        data["status"].startswith("PROVED REDUCTION"),
        "unexpected certificate status",
    )
    require(data["dimension"] == 5, "wrong dimension")
    require(data["hypothetical_code_size"] == 41, "wrong code size")

    cap = data["robust_cap"]
    require(Q(cap["minimum_height"]) == -Q(1, 50), "wrong cap height")
    require(
        cap["maximum_occupancy"] == 39 and 39 < 41,
        "wrong cap occupancy",
    )
    require(
        cap["source_certificate"]
        == (
            "experiments/quadratic_positive_locus/"
            "enlarged_cap_minus_1_over_50_certificate.json"
        ),
        "unexpected source certificate",
    )
    source = ROOT / cap["source_certificate"]
    require(source.is_file(), "source certificate is missing")
    require(
        sha256(source) == cap["source_certificate_sha256"],
        "source certificate hash mismatch",
    )
    require(
        cap["source_certificate_sha256"]
        == "c39b937146c515988f408662b388a6b1d4d9f116798dafadd58dcc8509d841df",
        "unexpected source certificate hash",
    )
    source_data = json.loads(source.read_text())
    require(
        source_data["status"] == "COMPUTATIONALLY CERTIFIED",
        "unexpected source status",
    )
    require(
        Q(source_data["minimum_height"]) == -Q(1, 50),
        "source cap height mismatch",
    )
    require(
        Q(source_data["resulting_real_objective"]) < 40,
        "source objective is not below 40",
    )
    require(
        source_data["resulting_integer_bound"] == 39,
        "source integer bound mismatch",
    )

    canonical = data["canonical_normalization"]
    require(
        Q(canonical["largest_eigenvalue"]) == 1,
        "wrong largest-eigenvalue normalization",
    )
    require(
        [Q(value) for value in canonical["ordered_eigenvalue_interval"]]
        == [-4, 1],
        "wrong eigenvalue interval",
    )
    require(
        [Q(value) for value in canonical["linear_norm_residual_interval"]]
        == [0, 50],
        "wrong residual linear-norm interval",
    )

    # At ||b||=50, q(x)>0 and x^T A x<=1 force
    # <b/||b||,x> > -1/50.  The inequality is strict even at the endpoint.
    b_norm = Q(50)
    cap_floor = -Q(1, 50)
    require(1 + b_norm * cap_floor == 0, "linear cap endpoint mismatch")

    # The lowest possible eigenvalue after lambda_max=1 and trace(A)=0 is
    # -4: four other eigenvalues can contribute at most four.
    dimension = data["dimension"]
    require(-(dimension - 1) == -4, "lowest eigenvalue bound mismatch")

    families = data["axisymmetric_families"]
    beta_transition = Q(4)
    # Both root transitions occur at an endpoint t=+/-1.
    require(
        q_minus(Q(1), beta_transition) == 0,
        "q-minus transition is wrong",
    )
    require(
        q_plus(Q(-1), beta_transition) == 0,
        "q-plus transition is wrong",
    )

    # q_-(t) has its lower root at -1/50 precisely at beta=499/10.
    beta_robust = Q(499, 10)
    require(
        q_minus(-Q(1, 50), beta_robust) == 0,
        "q-minus robust threshold is wrong",
    )
    require(beta_robust < 50, "q-minus threshold must be below 50")
    require(
        families["belt_to_cap"]["certified_occupancy_39_range"]
        == "beta >= 499/10",
        "wrong q-minus certified range",
    )

    # q_+(t), beta>=4, is positive only above its positive root, hence in
    # the open northern hemisphere and therefore in the robust cap.
    require(
        families["two_caps_to_cap"]["certified_occupancy_39_range"]
        == "beta >= 4",
        "wrong q-plus certified range",
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
