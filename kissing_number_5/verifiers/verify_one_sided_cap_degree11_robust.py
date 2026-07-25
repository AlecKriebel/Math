#!/usr/bin/env python3
"""Exact verifier for the degree-11 enlarged-cap robustness theorem.

Only Python's standard library and exact Fraction arithmetic are used.  The
Gram factors come from the separately certified degree-11 hemisphere kernel;
this verifier authenticates that source before rebuilding the enlarged-domain
polynomial and its Bernstein tree.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = ROOT / "verifiers" / "verify_one_sided_cap_degree10.py"
SOURCE_CERTIFICATE_PATH = (
    ROOT / "certificates" / "one_sided_cap_degree11_bound.json"
)
ROBUST_CERTIFICATE_PATH = (
    ROOT / "certificates" / "one_sided_cap_degree11_robust_1_over_300.json"
)
SPEC = importlib.util.spec_from_file_location("cap_exact_core_robust", CORE_PATH)
assert SPEC is not None and SPEC.loader is not None
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def affine_substitute(
    polynomial: CORE.Polynomial,
    shifts: tuple[Q, Q, Q],
    scales: tuple[Q, Q, Q],
) -> CORE.Polynomial:
    """Substitute old variable_i = shift_i + scale_i * new variable_i."""

    answer: CORE.Polynomial = {}
    for exponent, coefficient in polynomial.items():
        partial: CORE.Polynomial = {(0, 0, 0): coefficient}
        for axis, power in enumerate(exponent):
            factor: CORE.Polynomial = {}
            for new_power in range(power + 1):
                new_exponent = [0, 0, 0]
                new_exponent[axis] = new_power
                factor[tuple(new_exponent)] = (
                    Q(comb(power, new_power))
                    * shifts[axis] ** (power - new_power)
                    * scales[axis] ** new_power
                )
            partial = CORE.poly_multiply(partial, factor)
        answer = CORE.poly_add(answer, partial)
    return answer


def affine_substitute_univariate(
    polynomial: dict[int, Q], shift: Q, scale: Q
) -> dict[int, Q]:
    answer: dict[int, Q] = {}
    for power, coefficient in polynomial.items():
        for new_power in range(power + 1):
            value = (
                coefficient
                * comb(power, new_power)
                * shift ** (power - new_power)
                * scale**new_power
            )
            answer[new_power] = answer.get(new_power, Q(0)) + value
    return {
        power: coefficient
        for power, coefficient in answer.items()
        if coefficient
    }


def terminal_category_counts(counts: Counter) -> dict[str, int]:
    return {
        category: sum(
            number
            for (current_category, _), number in counts.items()
            if current_category == category
        )
        for category in ("infeasible", "proved")
    }


def verify() -> dict[str, object]:
    certificate = json.loads(ROBUST_CERTIFICATE_PATH.read_text())
    source = json.loads(SOURCE_CERTIFICATE_PATH.read_text())
    assert certificate["status"] == "COMPUTATIONALLY CERTIFIED"
    assert certificate["source_kernel_certificate"] == (
        "certificates/one_sided_cap_degree11_bound.json"
    )
    assert sha256_file(SOURCE_CERTIFICATE_PATH) == certificate[
        "source_kernel_certificate_sha256"
    ]
    assert certificate["source_kernel_certificate_sha256"] == (
        "182553399ad2f0cd932e82237943f6b9bd27d18a970bd94592294df8cc5abf5c"
    )
    assert CORE.factor_payload_digest(source) == certificate[
        "source_factor_payload_sha256"
    ]
    assert certificate["source_factor_payload_sha256"] == (
        "723d5521951ce45d236116016a69e7e8e510b8e7ba1f0338f7c1d6fffe507257"
    )
    assert source["harmonic_degree"] == certificate["harmonic_degree"] == 11

    minimum_height = Q(certificate["minimum_height"])
    epsilon = -minimum_height
    off_target = Q(certificate["off_diagonal_upper_target"])
    diag_target = Q(certificate["diagonal_upper_target"])
    assert minimum_height == -Q(1, 300)
    assert off_target == -Q(121, 125)
    assert diag_target == Q(3291, 100)

    blocks = CORE.load_blocks(str(SOURCE_CERTIFICATE_PATH))
    degree = len(blocks) - 1
    polynomial = CORE.cap_polynomial(blocks)
    assert degree == 11
    assert len(polynomial) == 650

    diagonal_margin: dict[int, Q] = {0: diag_target}
    for power, coefficient in CORE.diagonal_polynomial(polynomial).items():
        diagonal_margin[power] = (
            diagonal_margin.get(power, Q(0)) - coefficient
        )
    diagonal_margin = affine_substitute_univariate(
        diagonal_margin, minimum_height, 1 + epsilon
    )
    diagonal_degree = max(diagonal_margin)
    diagonal_bernstein = CORE.univariate_power_to_bernstein(
        diagonal_margin, diagonal_degree
    )
    diagonal_counts = CORE.audit_univariate(diagonal_bernstein, 48)
    diagonal_manifest = certificate["diagonal_bernstein_manifest"]
    assert diagonal_manifest["initial_interval"] == ["-1/300", "1"]
    assert diagonal_degree == diagonal_manifest["polynomial_degree"] == 22
    assert sum(diagonal_counts.values()) == diagonal_manifest["total_leaves"] == 5
    assert max(depth for _, depth in diagonal_counts) == (
        diagonal_manifest["maximum_leaf_depth"]
    ) == 3
    assert {
        str(depth): sum(
            number
            for (category, current_depth), number in diagonal_counts.items()
            if category == "proved" and current_depth == depth
        )
        for depth in sorted({depth for _, depth in diagonal_counts})
    } == diagonal_manifest["depth_counts"] == {"2": 3, "3": 2}

    h_polynomial = CORE.poly_scale(polynomial, Q(-1))
    h_polynomial[(0, 0, 0)] = (
        h_polynomial.get((0, 0, 0), Q(0)) + off_target
    )
    shifts = (minimum_height, minimum_height, Q(-1))
    scales = (1 + epsilon, 1 + epsilon, Q(3, 2))
    h_transformed = affine_substitute(h_polynomial, shifts, scales)
    h_bernstein = CORE.power_to_bernstein(h_transformed, degree)

    determinant = {
        (0, 0, 0): Q(1),
        (1, 1, 1): Q(2),
        (2, 0, 0): Q(-1),
        (0, 2, 0): Q(-1),
        (0, 0, 2): Q(-1),
    }
    determinant_transformed = affine_substitute(determinant, shifts, scales)
    determinant_bernstein = CORE.power_to_bernstein(
        determinant_transformed, degree
    )
    counts, digest = CORE.audit_domain(
        h_bernstein,
        determinant_bernstein,
        degree,
        48,
        5_000_000,
    )
    manifest = certificate["bernstein_tree_manifest"]
    assert manifest["initial_box"] == {
        "u": ["-1/300", "1"],
        "v": ["-1/300", "1"],
        "t": ["-1", "1/2"],
    }
    assert manifest["unit_cube_substitution"] == {
        "u": "-1/300+(301/300)a",
        "v": "-1/300+(301/300)b",
        "t": "-1+(3/2)s",
    }
    assert manifest["branch_rule"] == (
        "bisect a,b,s cyclically at exact midpoints"
    )
    total_leaves = sum(counts.values())
    maximum_depth = max(depth for _, depth in counts)
    category_counts = terminal_category_counts(counts)
    assert total_leaves == manifest["total_leaves"] == 6053
    assert maximum_depth == manifest["maximum_leaf_depth"] == 30
    assert category_counts == manifest["terminal_category_counts"] == {
        "infeasible": 2914,
        "proved": 3139,
    }
    assert digest == manifest["leaf_digest_sha256"]
    assert digest == (
        "8c61e175b7cd3b83e5140becb278c47a2c413bdf3e0cc034a0891f1e41b79eab"
    )

    scale = -Q(1) / off_target
    objective = Q(1) + scale * diag_target
    assert scale == Q(125, 121)
    assert objective == Q(certificate["resulting_real_objective"])
    assert objective == Q(16939, 484)
    assert objective == 35 - Q(1, 484)
    assert objective < 35
    assert certificate["resulting_integer_bound"] == 34

    return {
        "status": "PASS",
        "harmonic_degree": degree,
        "minimum_height": minimum_height,
        "power_terms": len(polynomial),
        "diagonal_bernstein_leaves": sum(diagonal_counts.values()),
        "domain_bernstein_leaves": total_leaves,
        "maximum_leaf_depth": maximum_depth,
        "terminal_category_counts": category_counts,
        "leaf_digest_sha256": digest,
        "dual_objective": objective,
        "enlarged_cap_upper_bound": 34,
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
