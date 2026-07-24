#!/usr/bin/env python3
"""Attempt an exact full-domain audit of a rationalized cap kernel.

This is certificate construction, not a frozen verifier.  Success means the
specified rational Gram factors and targets pass an exact Bernstein audit;
the result should then be copied into an immutable certificate plus a small
independent verifier.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROBUST_PATH = ROOT / "verifiers" / "verify_one_sided_cap_degree11_robust.py"
SPEC = importlib.util.spec_from_file_location("qpl_robust_exact_core", ROBUST_PATH)
assert SPEC is not None and SPEC.loader is not None
ROBUST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ROBUST)
CORE = ROBUST.CORE


def category_counts(counts: Counter) -> dict[str, int]:
    return {
        category: sum(
            number
            for (current, _), number in counts.items()
            if current == category
        )
        for category in ("infeasible", "proved")
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate")
    parser.add_argument("--epsilon", default="1/50")
    parser.add_argument("--off-target", default="-9/10")
    parser.add_argument("--diag-target", default="35")
    parser.add_argument("--max-depth", type=int, default=54)
    parser.add_argument("--max-nodes", type=int, default=5_000_000)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    epsilon = Q(args.epsilon)
    off_target = Q(args.off_target)
    diag_target = Q(args.diag_target)
    blocks = CORE.load_blocks(args.candidate)
    degree = len(blocks) - 1
    polynomial = CORE.cap_polynomial(blocks)

    diagonal_margin: dict[int, Q] = {0: diag_target}
    for power, coefficient in CORE.diagonal_polynomial(polynomial).items():
        diagonal_margin[power] = diagonal_margin.get(power, Q(0)) - coefficient
    diagonal_margin = ROBUST.affine_substitute_univariate(
        diagonal_margin, -epsilon, 1 + epsilon
    )
    diagonal_degree = max(diagonal_margin)
    diagonal_bernstein = CORE.univariate_power_to_bernstein(
        diagonal_margin, diagonal_degree
    )
    diagonal_counts = CORE.audit_univariate(diagonal_bernstein, args.max_depth)

    margin = CORE.poly_scale(polynomial, Q(-1))
    margin[(0, 0, 0)] = margin.get((0, 0, 0), Q(0)) + off_target
    shifts = (-epsilon, -epsilon, Q(-1))
    scales = (1 + epsilon, 1 + epsilon, Q(3, 2))
    margin = ROBUST.affine_substitute(margin, shifts, scales)
    margin_bernstein = CORE.power_to_bernstein(margin, degree)

    determinant = {
        (0, 0, 0): Q(1),
        (1, 1, 1): Q(2),
        (2, 0, 0): Q(-1),
        (0, 2, 0): Q(-1),
        (0, 0, 2): Q(-1),
    }
    determinant = ROBUST.affine_substitute(determinant, shifts, scales)
    determinant_bernstein = CORE.power_to_bernstein(determinant, degree)
    counts, digest = CORE.audit_domain(
        margin_bernstein,
        determinant_bernstein,
        degree,
        args.max_depth,
        args.max_nodes,
    )

    objective = 1 - diag_target / off_target
    report = {
        "status": "EXACT AUDIT PASS",
        "candidate": str(Path(args.candidate)),
        "degree": degree,
        "minimum_height": str(-epsilon),
        "off_diagonal_upper_target": str(off_target),
        "diagonal_upper_target": str(diag_target),
        "objective": str(objective),
        "objective_decimal": float(objective),
        "integer_bound": (objective.numerator // objective.denominator),
        "diagonal": {
            "leaves": sum(diagonal_counts.values()),
            "maximum_depth": max(depth for _, depth in diagonal_counts),
        },
        "domain": {
            "leaves": sum(counts.values()),
            "maximum_depth": max(depth for _, depth in counts),
            "categories": category_counts(counts),
            "leaf_digest_sha256": digest,
        },
    }
    Path(args.report).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
