#!/usr/bin/env python3
"""Rationalize the repaired noncentered pair/triple witness.

Only the orbit masses are rounded.  Their total is corrected exactly, and
the pair masses are then reconstructed from the exact marginal identities.
This avoids trusting a floating rank decision or a floating linear solve.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


N = 41
DENOMINATOR = 10**14


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=(
            root
            / "experiments"
            / "continuous_rank_bv_search"
            / "results"
            / "noncentered_integer_cut_d12_rich2.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("candidate_exact.json"),
    )
    args = parser.parse_args()
    args.source = args.source.resolve()
    args.output = args.output.resolve()
    source_bytes = args.source.read_bytes()
    source = json.loads(source_bytes)
    triples = [tuple(item) for item in source["triple_orbits"]]
    rounded = [
        Q(round(float(value) * DENOMINATOR), DENOMINATOR)
        for value in source["nu"]
    ]
    rounded[-1] += Q((N - 1) * (N - 2)) - sum(rounded)
    if not all(value > 0 for value in rounded):
        raise ValueError("rationalized orbit mass is not strictly positive")

    alpha = []
    for index in range(len(source["grid"])):
        marginal = sum(
            mass * triple.count(index) / 3
            for mass, triple in zip(rounded, triples, strict=True)
        )
        alpha.append(marginal / (N - 2))
    if sum(alpha) != N - 1 or not all(value > 0 for value in alpha):
        raise ValueError("reconstructed pair marginal is invalid")

    output = {
        "schema": "fixed41-bv-fullradial-k16-pseudodistribution-v1",
        "status": (
            "exact repaired noncentered pair/triple relaxation witness; "
            "not a code"
        ),
        "source_numerical_result": str(args.source.relative_to(root)),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "dimension": 5,
        "cardinality": N,
        "maximum_inner_product": "1/2",
        "grid": source["grid"],
        "triples": [list(triple) for triple in triples],
        "alpha": [qstr(value) for value in alpha],
        "nu": [qstr(value) for value in rounded],
        "bv_total_degree": None,
        "bv_full_radial_harmonic_degree": 16,
        "two_point_degree": 100,
        "rounding_denominator": DENOMINATOR,
        "exact_constraints": [
            "sum(alpha)=40",
            "sum(nu)=1560",
            "marginal_i=39*alpha_i for every grid node",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
