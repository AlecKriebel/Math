#!/usr/bin/env python3
"""Try an exact Bernstein audit of an enlarged-cap degree-11 kernel.

This is a certificate-construction experiment.  It imports exact polynomial
and Bernstein primitives from the existing degree-10 verifier, but loads the
already-certified degree-11 Gram factors.  Successful output must still be
frozen in an independent certificate/verifier pair before it is cited.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import importlib.util
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE_PATH = ROOT / "verifiers" / "verify_one_sided_cap_degree10.py"
CERTIFICATE_PATH = ROOT / "certificates" / "one_sided_cap_degree11_bound.json"
SPEC = importlib.util.spec_from_file_location("cap_exact_core_robust_try", CORE_PATH)
assert SPEC is not None and SPEC.loader is not None
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)


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
    return {power: coefficient for power, coefficient in answer.items() if coefficient}


def category_counts(counts: Counter) -> dict[str, int]:
    return {
        category: sum(
            number
            for (current_category, _), number in counts.items()
            if current_category == category
        )
        for category in ("infeasible", "proved")
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epsilon", default="1/300")
    parser.add_argument("--off-target", default="-121/125")
    parser.add_argument("--diag-target", default="3291/100")
    parser.add_argument("--max-depth", type=int, default=60)
    parser.add_argument("--max-nodes", type=int, default=10_000_000)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    epsilon = Q(args.epsilon)
    off_target = Q(args.off_target)
    diag_target = Q(args.diag_target)
    blocks = CORE.load_blocks(str(CERTIFICATE_PATH))
    degree = len(blocks) - 1
    polynomial = CORE.cap_polynomial(blocks)

    diagonal_margin: dict[int, Q] = {0: diag_target}
    for power, coefficient in CORE.diagonal_polynomial(polynomial).items():
        diagonal_margin[power] = (
            diagonal_margin.get(power, Q(0)) - coefficient
        )
    diagonal_margin = affine_substitute_univariate(
        diagonal_margin, -epsilon, 1 + epsilon
    )
    diagonal_degree = max(diagonal_margin)
    diagonal_bernstein = CORE.univariate_power_to_bernstein(
        diagonal_margin, diagonal_degree
    )
    diagonal_counts = CORE.audit_univariate(
        diagonal_bernstein, args.max_depth
    )
    print(
        "diagonal",
        {
            "leaves": sum(diagonal_counts.values()),
            "maximum_depth": max(depth for _, depth in diagonal_counts),
        },
        flush=True,
    )

    h_polynomial = CORE.poly_scale(polynomial, Q(-1))
    h_polynomial[(0, 0, 0)] = (
        h_polynomial.get((0, 0, 0), Q(0)) + off_target
    )
    shifts = (-epsilon, -epsilon, Q(-1))
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
        args.max_depth,
        args.max_nodes,
        args.verbose,
    )
    total_leaves = sum(counts.values())
    maximum_depth = max(depth for _, depth in counts)
    scale = -Q(1) / off_target
    objective = Q(1) + scale * diag_target
    print(
        "domain",
        {
            "leaves": total_leaves,
            "maximum_depth": maximum_depth,
            "categories": category_counts(counts),
            "digest": digest,
        },
        flush=True,
    )
    print(
        "objective",
        {
            "exact": str(objective),
            "decimal": float(objective),
            "below_35": objective < 35,
        },
        flush=True,
    )


if __name__ == "__main__":
    main()
