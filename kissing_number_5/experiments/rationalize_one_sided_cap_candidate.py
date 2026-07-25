#!/usr/bin/env python3
"""Rationalize a sampled one-sided cap-SDP matrix candidate.

Discovery only.  The output consists of exact rational Gram factors, so its
matrix blocks are automatically positive semidefinite.  It is not a
certificate until the accompanying three-variable inequalities have been
proved on their full domains by an exact verifier.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--denominator", type=int, default=100_000_000)
    parser.add_argument("--eigenvalue-floor", type=float, default=0.0)
    parser.add_argument("--scale-numerator", type=int, default=1)
    parser.add_argument("--scale-denominator", type=int, default=1)
    args = parser.parse_args()
    assert args.scale_numerator > 0
    assert args.scale_denominator > 0
    matrix_scale = args.scale_numerator / args.scale_denominator

    source = np.load(args.input)
    blocks = []
    for k in range(len(source.files)):
        matrix = matrix_scale * source[f"F{k}"]
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        retained = eigenvalues > args.eigenvalue_floor
        factor = eigenvectors[:, retained] * np.sqrt(eigenvalues[retained])
        integers = np.rint(args.denominator * factor).astype(np.int64)
        rationalized = (
            integers.astype(float) @ integers.astype(float).T
            / args.denominator**2
        )
        blocks.append(
            {
                "k": k,
                "size": int(matrix.shape[0]),
                "factor_denominator": args.denominator,
                "factor_integer_columns": integers.tolist(),
                "source_minimum_eigenvalue": float(eigenvalues[0]),
                "source_maximum_eigenvalue": float(eigenvalues[-1]),
                "maximum_entry_change": float(
                    np.max(np.abs(rationalized - matrix))
                ),
            }
        )

    certificate = {
        "status": "NUMERICAL CANDIDATE REQUIRING EXACT DOMAIN AUDIT",
        "source_npz": str(Path(args.input).resolve()),
        "harmonic_degree": len(blocks) - 1,
        "source_matrix_scale": (
            f"{args.scale_numerator}/{args.scale_denominator}"
        ),
        "modified_zonal_normalization": (
            "lambda_ij omitted by positive diagonal congruence"
        ),
        "blocks": blocks,
    }
    Path(args.output).write_text(json.dumps(certificate, indent=2) + "\n")
    print(f"wrote {args.output}")
    print(
        "maximum rationalization change:",
        max(block["maximum_entry_change"] for block in blocks),
    )


if __name__ == "__main__":
    main()
