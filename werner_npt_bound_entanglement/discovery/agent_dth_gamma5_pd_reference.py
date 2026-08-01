#!/usr/bin/env python3
"""Generate an exact positive-definiteness reference for Gamma5 blocks.

The exact Gamma5 CRT replay exports 216 rational coordinate matrices on the
canonical final-slot face whose reduced multiplicity-rank sum is 751.  This
discovery utility records dyadic
reference matrices and inverse-Cholesky proposals.  The independent verifier
replays all inequalities over QQ; floating point is used here only to propose
the transforms.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
from itertools import product
import math
from pathlib import Path

import numpy as np
import scipy.linalg as la


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


GENERIC = import_file(
    "dth_gamma5_pd_generic", HERE / "agent_dth_mixed_pd_reference.py"
)
MATRIX = GENERIC.MATRIX
FORMAT = "dth-gamma5-face-pd-reference-v1"
EXPECTED_ACTIVE = 188
EXPECTED_REDUCED_RANK = 751


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--source-certificate", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--reference-bits", type=int, default=100)
    parser.add_argument("--transform-bits", type=int, default=80)
    args = parser.parse_args()

    exact_blocks = GENERIC.parse_exact_blocks(args.input)
    source_hash = hashlib.sha256(
        Path(args.source_certificate).read_bytes()
    ).hexdigest()
    payload = {
        "format": FORMAT,
        "source_certificate_sha256": source_hash,
        "reference_bits": args.reference_bits,
        "transform_bits": args.transform_bits,
        "blocks": [],
    }
    worst_ratio = Fraction(0)
    worst_shape = None
    active = total_rank = 0
    for count, shapes in enumerate(product(range(6), repeat=3), 1):
        matrix = exact_blocks[shapes]
        dimension = len(matrix)
        total_rank += dimension
        tag = "".join(map(str, shapes))
        if not dimension:
            payload["blocks"].append({
                "shape": tag, "dimension": 0, "scale_exponent": 0,
                "reference_upper": [], "transform_upper": [],
            })
            continue
        active += 1
        maximum = max(abs(float(value)) for row in matrix for value in row)
        if not maximum or not math.isfinite(maximum):
            raise AssertionError(f"invalid Gamma5 block scale in {tag}")
        exponent = -math.floor(math.log2(maximum))
        scaled = [[value * Fraction(2) ** exponent for value in row]
                  for row in matrix]

        reference_denominator = 1 << args.reference_bits
        reference_numerators = [[
            GENERIC.nearest_dyadic_numerator(value, args.reference_bits)
            for value in row
        ] for row in scaled]
        reference = [[Fraction(value, reference_denominator) for value in row]
                     for row in reference_numerators]
        cholesky = la.cholesky(np.asarray(reference, dtype=float), lower=True)
        inverse_cholesky = la.solve_triangular(
            cholesky.T, np.eye(dimension), lower=False
        )
        transform_denominator = 1 << args.transform_bits
        transform_numerators = [[0] * dimension for _ in range(dimension)]
        for row in range(dimension):
            for column in range(row, dimension):
                transform_numerators[row][column] = int(round(
                    inverse_cholesky[row, column] * transform_denominator
                ))
        transform = [[Fraction(value, transform_denominator) for value in row]
                     for row in transform_numerators]
        result = MATRIX.assert_pd_near_reference(
            scaled, reference, transform, triangular=True
        )
        ratio = (result["difference_frobenius_squared"]
                 / result["matrix_lower_bound"] ** 2)
        if ratio > worst_ratio:
            worst_ratio, worst_shape = ratio, shapes

        reference_upper = [reference_numerators[i][i]
                           for i in range(dimension)]
        reference_upper.extend(
            reference_numerators[i][j]
            for i in range(dimension) for j in range(i + 1, dimension)
        )
        transform_upper = [
            transform_numerators[i][j]
            for i in range(dimension) for j in range(i, dimension)
        ]
        payload["blocks"].append({
            "shape": tag,
            "dimension": dimension,
            "scale_exponent": exponent,
            "reference_upper": [str(value) for value in reference_upper],
            "transform_upper": [str(value) for value in transform_upper],
        })
        if count % 24 == 0:
            print("Gamma5 PD blocks", count, "/216", flush=True)

    assert active == EXPECTED_ACTIVE
    assert total_rank == EXPECTED_REDUCED_RANK
    output = Path(args.output)
    digest = GENERIC.write_gzip(output, payload)
    print("Gamma5 PD reference generation passed")
    print("active/rank:", active, total_rank)
    print("worst perturbation ratio:", float(worst_ratio),
          "block", worst_shape)
    print("certificate bytes:", output.stat().st_size)
    print("certificate sha256:", digest)


if __name__ == "__main__":
    main()
