#!/usr/bin/env python3
"""Exact verifier for the rational degree-11 one-sided cap-SDP bound.

Only Python's standard library and exact Fraction arithmetic are used.
The common polynomial/Bernstein primitives are imported from the independently
tested degree-10 verifier; no degree-10 certificate data or conclusion is used.
"""

from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = ROOT / "verifiers" / "verify_one_sided_cap_degree10.py"
CERTIFICATE_PATH = ROOT / "certificates" / "one_sided_cap_degree11_bound.json"
SPEC = importlib.util.spec_from_file_location("cap_exact_core", CORE_PATH)
assert SPEC is not None and SPEC.loader is not None
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)


def verify() -> dict[str, object]:
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    assert certificate["status"] == "COMPUTATIONALLY CERTIFIED"
    assert certificate["harmonic_degree"] == 11
    assert certificate["source_matrix_scale"] == "997/1000"
    assert CORE.factor_payload_digest(certificate) == certificate[
        "factor_payload_sha256"
    ]
    assert certificate["factor_payload_sha256"] == (
        "723d5521951ce45d236116016a69e7e8e510b8e7ba1f0338f7c1d6fffe507257"
    )

    manifest = certificate["bernstein_tree_manifest"]
    assert manifest["leaf_digest_sha256"] == (
        "3ffd08afa66bcd12e52399e392c09fda237f8bab18fc1af9a8090e76f1f81f65"
    )
    assert manifest["total_leaves"] == 5995
    assert manifest["maximum_leaf_depth"] == 31
    assert manifest["terminal_category_counts"] == {
        "infeasible": 2848,
        "proved": 3147,
    }

    off_target = Q(certificate["off_diagonal_upper_target"])
    diag_target = Q(certificate["diagonal_upper_target"])
    assert off_target == Q(-969, 1000)
    assert diag_target == Q(1647, 50)

    blocks = CORE.load_blocks(str(CERTIFICATE_PATH))
    degree = len(blocks) - 1
    polynomial = CORE.cap_polynomial(blocks)
    max_multidegree = tuple(
        max(exponent[index] for exponent in polynomial)
        for index in range(3)
    )
    assert degree == 11
    assert len(polynomial) == 650
    assert max_multidegree == (11, 11, 11)

    diagonal_margin = {0: diag_target}
    for power, coefficient in CORE.diagonal_polynomial(polynomial).items():
        diagonal_margin[power] = (
            diagonal_margin.get(power, Q(0)) - coefficient
        )
    diagonal_degree = max(diagonal_margin)
    diagonal_bernstein = CORE.univariate_power_to_bernstein(
        diagonal_margin, diagonal_degree
    )
    diagonal_counts = CORE.audit_univariate(diagonal_bernstein, 48)
    assert sum(diagonal_counts.values()) == 3
    assert max(depth for (_, depth) in diagonal_counts) == 2

    # H = off_target-F.  Proving H>=0 is the required off-diagonal bound.
    h_polynomial = CORE.poly_scale(polynomial, Q(-1))
    h_polynomial[(0, 0, 0)] = (
        h_polynomial.get((0, 0, 0), Q(0)) + off_target
    )
    h_bernstein = CORE.power_to_bernstein(
        CORE.substitute_t_to_unit(h_polynomial), degree
    )

    determinant = {
        (0, 0, 0): Q(1),
        (1, 1, 1): Q(2),
        (2, 0, 0): Q(-1),
        (0, 2, 0): Q(-1),
        (0, 0, 2): Q(-1),
    }
    determinant_bernstein = CORE.power_to_bernstein(
        CORE.substitute_t_to_unit(determinant), degree
    )
    counts, digest = CORE.audit_domain(
        h_bernstein,
        determinant_bernstein,
        degree,
        48,
        5_000_000,
    )
    total_leaves = sum(counts.values())
    maximum_leaf_depth = max(depth for (_, depth) in counts)
    category_counts = {
        category: sum(
            number
            for (current_category, _), number in counts.items()
            if current_category == category
        )
        for category in ("infeasible", "proved")
    }
    assert total_leaves == manifest["total_leaves"] == 5995
    assert maximum_leaf_depth == manifest["maximum_leaf_depth"] == 31
    assert category_counts == manifest["terminal_category_counts"]
    assert digest == manifest["leaf_digest_sha256"]

    scale = -Q(1) / off_target
    objective = Q(1) + scale * diag_target
    assert scale == Q(1000, 969)
    assert objective == Q(certificate["resulting_real_objective"])
    assert objective == Q(11303, 323)
    assert objective < 35
    assert certificate["resulting_integer_bound"] == 34

    return {
        "status": "PASS",
        "harmonic_degree": degree,
        "power_terms": len(polynomial),
        "max_multidegree": max_multidegree,
        "diagonal_bernstein_leaves": sum(diagonal_counts.values()),
        "domain_bernstein_leaves": total_leaves,
        "maximum_leaf_depth": maximum_leaf_depth,
        "terminal_category_counts": category_counts,
        "leaf_digest_sha256": digest,
        "dual_objective": objective,
        "one_sided_kissing_upper_bound": 34,
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
