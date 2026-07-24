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

CORE_SPEC = importlib.util.spec_from_file_location("qpl_cap_exact_core", CORE_PATH)
assert CORE_SPEC is not None and CORE_SPEC.loader is not None
CORE = importlib.util.module_from_spec(CORE_SPEC)
CORE_SPEC.loader.exec_module(CORE)
ROBUST_SPEC = importlib.util.spec_from_file_location(
    "qpl_cap_affine_exact_core", ROBUST_PATH
)
assert ROBUST_SPEC is not None and ROBUST_SPEC.loader is not None
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


def verify() -> dict[str, object]:
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    assert certificate["status"] == "COMPUTATIONALLY CERTIFIED"
    assert certificate["harmonic_degree"] == 8
    factor_path = ROOT / certificate["factor_file"]
    assert sha256(factor_path) == certificate["factor_file_sha256"]
    factor_data = json.loads(factor_path.read_text())
    assert factor_data["status"] == "COMPUTATIONALLY CERTIFIED EXACT GRAM FACTORS"
    assert CORE.factor_payload_digest(factor_data) == certificate[
        "factor_payload_sha256"
    ]

    epsilon = -Q(certificate["minimum_height"])
    off_target = Q(certificate["off_diagonal_upper_target"])
    diag_target = Q(certificate["diagonal_upper_target"])
    assert epsilon == Q(1, 50)
    assert off_target == -Q(9, 10)
    assert diag_target == 35

    # load_blocks explicitly forms L L^T from the integer columns, so every
    # block is PSD over the rationals without an eigenvalue tolerance.
    blocks = CORE.load_blocks(str(factor_path))
    assert len(blocks) == 9
    polynomial = CORE.cap_polynomial(blocks)

    diagonal_margin: dict[int, Q] = {0: diag_target}
    for power, coefficient in CORE.diagonal_polynomial(polynomial).items():
        diagonal_margin[power] = diagonal_margin.get(power, Q(0)) - coefficient
    diagonal_margin = ROBUST.affine_substitute_univariate(
        diagonal_margin, -epsilon, 1 + epsilon
    )
    diagonal_degree = max(diagonal_margin)
    assert diagonal_degree == 16
    diagonal_bernstein = CORE.univariate_power_to_bernstein(
        diagonal_margin, diagonal_degree
    )
    diagonal_counts = CORE.audit_univariate(diagonal_bernstein, 48)
    diagonal_manifest = certificate["diagonal_bernstein_manifest"]
    assert sum(diagonal_counts.values()) == diagonal_manifest["total_leaves"] == 3
    assert max(depth for _, depth in diagonal_counts) == (
        diagonal_manifest["maximum_leaf_depth"]
    ) == 2

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
    assert sum(counts.values()) == manifest["total_leaves"] == 1344
    assert max(depth for _, depth in counts) == manifest["maximum_leaf_depth"] == 21
    assert terminal_counts(counts) == manifest["terminal_category_counts"] == {
        "infeasible": 630,
        "proved": 714,
    }
    assert digest == manifest["leaf_digest_sha256"]
    assert digest == "1bf44242737474073736f8ce772e6433bab6fe4ea5d869fb10a660f413069ef1"

    objective = 1 - diag_target / off_target
    assert objective == Q(certificate["resulting_real_objective"]) == Q(359, 9)
    assert objective < 40
    assert objective.numerator // objective.denominator == (
        certificate["resulting_integer_bound"]
    ) == 39
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
