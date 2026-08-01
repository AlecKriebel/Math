#!/usr/bin/env python3
"""Generate a compact exact mixed-block positive-definiteness certificate.

The 85-prime CRT exporter reconstructs 216 exact rational product-face
coordinate matrices B.  Their absolute scale is tiny and block dependent,
so this generator first multiplies each nonzero block by an exact power of
two.  It then records

* a 100-bit dyadic symmetric reference matrix, and
* an 80-bit dyadic upper-triangular inverse-Cholesky transform.

The verifier proves the reference positive definite by exact diagonal
dominance after congruence and transfers positivity to the exact B via a
rigorous Frobenius perturbation bound.  No floating-point sign is trusted;
floating point is used only to propose the dyadic transform.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import gzip
import hashlib
import importlib.util
from itertools import product
import json
import math
from pathlib import Path

import numpy as np
import scipy.linalg as la


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MATRIX_PATH = ROOT / "verification" / "agent_dth_exact_matrix.py"
SPEC = importlib.util.spec_from_file_location("dth_mixed_pd_matrix", MATRIX_PATH)
MATRIX = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MATRIX)


FORMAT = "dth-mixed-face-pd-reference-v1"


def nearest_dyadic_numerator(value, bits):
    value = Fraction(value)
    scale = 1 << bits
    sign = -1 if value < 0 else 1
    numerator = abs(value.numerator) * scale
    quotient, remainder = divmod(numerator, value.denominator)
    # Deterministic half-away-from-zero rounding.  Exact halfway cases are
    # harmless; this rule is simpler to replay than host-language rounding.
    if 2 * remainder >= value.denominator:
        quotient += 1
    return sign * quotient


def parse_exact_blocks(path):
    data = json.loads(Path(path).read_text(encoding="ascii"))
    blocks = {}
    for shapes in product(range(6), repeat=3):
        tag = "".join(map(str, shapes))
        block = data["blocks"][tag]
        dimension = int(block["dimension"])
        values = [Fraction(int(numerator), int(denominator))
                  for numerator, denominator in block["upper"]]
        if len(values) != dimension * (dimension + 1) // 2:
            raise ValueError(f"wrong exact mixed entry count in {tag}")
        matrix = [[Fraction(0) for _ in range(dimension)]
                  for _ in range(dimension)]
        position = 0
        for i in range(dimension):
            matrix[i][i] = values[position]
            position += 1
        for i in range(dimension):
            for j in range(i + 1, dimension):
                matrix[i][j] = matrix[j][i] = values[position]
                position += 1
        blocks[shapes] = matrix
    return blocks


def canonical_json(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"


def write_gzip(path, payload):
    path = Path(path)
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb",
                           compresslevel=9, mtime=0) as handle:
            handle.write(canonical_json(payload).encode("ascii"))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", default="/tmp/dth_exact_mixed_coordinates.json"
    )
    parser.add_argument(
        "--source-certificate",
        default="/tmp/dth_exact_obstruction_v2.json.gz",
    )
    parser.add_argument(
        "--output",
        default=str(
            ROOT / "verification" / "certificates" /
            "dth_mixed_pd_reference.json.gz"
        ),
    )
    parser.add_argument("--reference-bits", type=int, default=100)
    parser.add_argument("--transform-bits", type=int, default=80)
    args = parser.parse_args()

    exact_blocks = parse_exact_blocks(args.input)
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
    nonzero = 0
    total_rank = 0
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
        nonzero += 1
        maximum = max(abs(float(value)) for row in matrix for value in row)
        if not maximum or not math.isfinite(maximum):
            raise AssertionError(f"invalid exact mixed block scale in {tag}")
        exponent = -math.floor(math.log2(maximum))
        scale = Fraction(2) ** exponent
        scaled = [[value * scale for value in row] for row in matrix]

        reference_denominator = 1 << args.reference_bits
        reference_numerators = [[
            nearest_dyadic_numerator(value, args.reference_bits)
            for value in row
        ] for row in scaled]
        reference = [[Fraction(value, reference_denominator)
                      for value in row] for row in reference_numerators]
        reference_float = np.asarray(reference, dtype=float)
        cholesky = la.cholesky(reference_float, lower=True)
        inverse_cholesky = la.solve_triangular(
            cholesky.T, np.eye(dimension), lower=False
        )
        transform_denominator = 1 << args.transform_bits
        transform_numerators = [[0] * dimension for _ in range(dimension)]
        for i in range(dimension):
            for j in range(i, dimension):
                transform_numerators[i][j] = int(round(
                    inverse_cholesky[i, j] * transform_denominator
                ))
        transform = [[Fraction(value, transform_denominator)
                      for value in row] for row in transform_numerators]

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
            print("exact mixed PD blocks", count, "/216", flush=True)

    assert nonzero == 198
    assert total_rank == 2266
    output = Path(args.output)
    certificate_hash = write_gzip(output, payload)
    print("exact mixed PD reference certificate passed")
    print("nonzero blocks:", nonzero, "total rank:", total_rank)
    print("worst perturbation ratio:", float(worst_ratio),
          "block", worst_shape)
    print("certificate bytes:", output.stat().st_size)
    print("certificate sha256:", certificate_hash)


if __name__ == "__main__":
    main()
