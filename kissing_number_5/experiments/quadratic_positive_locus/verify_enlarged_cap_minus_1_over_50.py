#!/usr/bin/env python3
"""Exact verifier for the enlarged-cap u>=-1/50 bound.

The verifier uses only the Python standard library and Fraction arithmetic.
It reconstructs the positive-semidefinite kernel from integer Gram factors,
expands the polynomial exactly, and rebuilds both Bernstein subdivision
trees.  Floating-point discovery metadata is ignored.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CERTIFICATE_PATH = HERE / "enlarged_cap_minus_1_over_50_certificate.json"
CORE_PATH = ROOT / "verifiers" / "verify_one_sided_cap_degree10.py"
ROBUST_PATH = ROOT / "verifiers" / "verify_one_sided_cap_degree11_robust.py"


class VerificationError(Exception):
    """Raised when an exact enlarged-cap certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


CORE_SPEC = importlib.util.spec_from_file_location("qpl_cap_exact_core", CORE_PATH)
require(
    CORE_SPEC is not None and CORE_SPEC.loader is not None,
    "cannot load exact cap core",
)
CORE = importlib.util.module_from_spec(CORE_SPEC)
CORE_SPEC.loader.exec_module(CORE)
ROBUST_SPEC = importlib.util.spec_from_file_location(
    "qpl_cap_affine_exact_core", ROBUST_PATH
)
require(
    ROBUST_SPEC is not None and ROBUST_SPEC.loader is not None,
    "cannot load exact affine core",
)
ROBUST = importlib.util.module_from_spec(ROBUST_SPEC)
ROBUST_SPEC.loader.exec_module(ROBUST)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def terminal_counts(counts: Counter) -> dict[str, int]:
    return {
        category: sum(
            number
            for (current, _), number in counts.items()
            if current == category
        )
        for category in ("infeasible", "proved")
    }


def validate_factor_structure(factor_data: dict[str, object]) -> None:
    blocks = factor_data.get("blocks")
    require(isinstance(blocks, list), "factor blocks must be a list")
    require(len(blocks) == 9, "factor file must contain nine blocks")
    for expected_k, entry in enumerate(blocks):
        require(isinstance(entry, dict), f"block {expected_k} is not an object")
        require(entry.get("k") == expected_k, f"wrong index for block {expected_k}")
        size = entry.get("size")
        require(isinstance(size, int) and size == 9 - expected_k, "wrong block size")
        denominator = entry.get("factor_denominator")
        require(
            isinstance(denominator, int) and denominator != 0,
            f"invalid denominator in block {expected_k}",
        )
        factor = entry.get("factor_integer_columns")
        require(isinstance(factor, list), f"missing factor in block {expected_k}")
        require(len(factor) == size, f"wrong factor height in block {expected_k}")
        rank = len(factor[0]) if size else 0
        require(
            all(
                isinstance(row, list)
                and len(row) == rank
                and all(isinstance(value, int) for value in row)
                for row in factor
            ),
            f"ragged or nonintegral factor in block {expected_k}",
        )


def verify(certificate_path: Path = CERTIFICATE_PATH) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    require(
        certificate["status"] == "COMPUTATIONALLY CERTIFIED",
        "unexpected certificate status",
    )
    require(certificate["harmonic_degree"] == 8, "wrong harmonic degree")
    require(
        certificate["factor_file"]
        == (
            "experiments/quadratic_positive_locus/"
            "enlarged_cap_minus_1_over_50_exact_factors.json"
        ),
        "unexpected factor file",
    )
    factor_path = ROOT / certificate["factor_file"]
    require(
        sha256(factor_path) == certificate["factor_file_sha256"],
        "factor-file hash mismatch",
    )
    require(
        certificate["factor_file_sha256"]
        == "cde299fcc3d532ce1fca713f5e44fceb74e105a58be6df91ac9c706788a56ca4",
        "unexpected factor-file hash",
    )
    factor_data = json.loads(factor_path.read_text())
    require(
        factor_data["status"] == "COMPUTATIONALLY CERTIFIED EXACT GRAM FACTORS",
        "unexpected factor status",
    )
    validate_factor_structure(factor_data)
    require(
        CORE.factor_payload_digest(factor_data)
        == certificate["factor_payload_sha256"],
        "factor-payload hash mismatch",
    )
    require(
        certificate["factor_payload_sha256"]
        == "9f10faa6fac82dca03617c0de5db2b61974edf449b8c592d8fbefa0b1e08bf41",
        "unexpected factor-payload hash",
    )

    epsilon = -Q(certificate["minimum_height"])
    off_target = Q(certificate["off_diagonal_upper_target"])
    diag_target = Q(certificate["diagonal_upper_target"])
    require(epsilon == Q(1, 50), "wrong cap height")
    require(off_target == -Q(9, 10), "wrong off-diagonal target")
    require(diag_target == 35, "wrong diagonal target")

    # load_blocks explicitly forms L L^T from the integer columns, so every
    # block is PSD over the rationals without an eigenvalue tolerance.
    blocks = CORE.load_blocks(str(factor_path))
    require(len(blocks) == 9, "wrong reconstructed block count")
    polynomial = CORE.cap_polynomial(blocks)
    require(
        all(
            0 <= exponent[0] <= 8
            and 0 <= exponent[1] <= 8
            and 0 <= exponent[2] <= 8
            for exponent in polynomial
        ),
        "kernel polynomial exceeds degree eight",
    )

    diagonal_margin: dict[int, Q] = {0: diag_target}
    for power, coefficient in CORE.diagonal_polynomial(polynomial).items():
        diagonal_margin[power] = diagonal_margin.get(power, Q(0)) - coefficient
    diagonal_margin = ROBUST.affine_substitute_univariate(
        diagonal_margin, -epsilon, 1 + epsilon
    )
    diagonal_degree = max(diagonal_margin)
    require(diagonal_degree == 16, "wrong diagonal polynomial degree")
    diagonal_bernstein = CORE.univariate_power_to_bernstein(
        diagonal_margin, diagonal_degree
    )
    diagonal_counts = CORE.audit_univariate(diagonal_bernstein, 48)
    diagonal_manifest = certificate["diagonal_bernstein_manifest"]
    require(
        diagonal_manifest["initial_interval"] == ["-1/50", "1"],
        "wrong diagonal interval",
    )
    require(
        diagonal_manifest["polynomial_degree"] == 16,
        "wrong recorded diagonal degree",
    )
    require(
        sum(diagonal_counts.values())
        == diagonal_manifest["total_leaves"]
        == 3,
        "wrong diagonal leaf count",
    )
    require(
        max(depth for _, depth in diagonal_counts)
        == diagonal_manifest["maximum_leaf_depth"]
        == 2,
        "wrong diagonal maximum depth",
    )

    off_margin = CORE.poly_scale(polynomial, Q(-1))
    off_margin[(0, 0, 0)] = (
        off_margin.get((0, 0, 0), Q(0)) + off_target
    )
    shifts = (-epsilon, -epsilon, Q(-1))
    scales = (1 + epsilon, 1 + epsilon, Q(3, 2))
    off_margin = ROBUST.affine_substitute(off_margin, shifts, scales)
    off_bernstein = CORE.power_to_bernstein(off_margin, 8)

    determinant = {
        (0, 0, 0): Q(1),
        (1, 1, 1): Q(2),
        (2, 0, 0): Q(-1),
        (0, 2, 0): Q(-1),
        (0, 0, 2): Q(-1),
    }
    determinant = ROBUST.affine_substitute(determinant, shifts, scales)
    determinant_bernstein = CORE.power_to_bernstein(determinant, 8)
    counts, digest = CORE.audit_domain(
        off_bernstein,
        determinant_bernstein,
        8,
        48,
        100_000,
    )
    manifest = certificate["bernstein_tree_manifest"]
    require(
        sum(counts.values()) == manifest["total_leaves"] == 1344,
        "wrong domain leaf count",
    )
    require(
        max(depth for _, depth in counts)
        == manifest["maximum_leaf_depth"]
        == 21,
        "wrong domain maximum depth",
    )
    require(
        terminal_counts(counts)
        == manifest["terminal_category_counts"]
        == {"infeasible": 630, "proved": 714},
        "wrong terminal category counts",
    )
    require(digest == manifest["leaf_digest_sha256"], "leaf digest mismatch")
    require(
        digest
        == "1bf44242737474073736f8ce772e6433bab6fe4ea5d869fb10a660f413069ef1",
        "unexpected leaf digest",
    )

    objective = 1 - diag_target / off_target
    require(
        objective
        == Q(certificate["resulting_real_objective"])
        == Q(359, 9),
        "wrong real objective",
    )
    require(objective < 40, "objective does not prove an integer bound below 40")
    require(
        objective.numerator // objective.denominator
        == certificate["resulting_integer_bound"]
        == 39,
        "wrong resulting integer bound",
    )
    return {
        "status": "PASS",
        "factor_file_sha256": sha256(factor_path),
        "factor_payload_sha256": CORE.factor_payload_digest(factor_data),
        "domain_leaf_digest_sha256": digest,
        "objective": str(objective),
        "integer_bound": 39,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
