#!/usr/bin/env python3
"""Exact finite-field replay of the 334-dimensional DTH defect minor.

The certificate labels a literal set of source coordinates in the exact
holomorphic K charts and literal row-membership equations in the exact
2266-dimensional product-face charts.  This verifier rebuilds both charts,
the exact local crossing, and the resulting 334 by 334 matrix modulo two
good primes.  Nonsingularity proves that the rational defect map has rank at
least 334.  No floating-point arithmetic enters the replay.

This is a certificate for the first lifted pseudomoment problem only.  It is
not a physical DTH or Werner-state witness.
"""

from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
import argparse

import numpy as np


HERE = Path(__file__).resolve().parent


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


KCHART = import_file("dth_exact_k_minor", HERE / "agent_dth_exact_k_coordinates.py")
FCHART = import_file("dth_exact_face_minor", HERE / "agent_dth_exact_face_coordinates.py")
BRIDGE = KCHART.BRIDGE
FACE = FCHART.FACE


PRIMES = (1_000_003, 1_000_033)
EXPECTED_RANK = 334


def rational_mod(value, prime):
    numerator, denominator = value.as_numer_denom()
    return int(numerator) % prime * pow(int(denominator) % prime, -1, prime) % prime


def matrix_mod(matrix, prime):
    return np.asarray([
        [rational_mod(matrix[row, column], prime) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ], dtype=np.int64)


def block_ranges(multiplicities):
    out = []
    offset = 0
    for multiplicity in multiplicities:
        out.append(np.arange(offset, offset + multiplicity * multiplicity).reshape(
            multiplicity, multiplicity
        ))
        offset += multiplicity * multiplicity
    assert offset == 103
    return out


def local_crossing_mod(prime):
    hol, mixed, _, _ = BRIDGE.exact_restriction_bridge()
    hol_mod = [[BRIDGE.fraction_mod(value, prime) for value in row] for row in hol]
    mixed_mod = [[BRIDGE.fraction_mod(value, prime) for value in row] for row in mixed]
    inverse = FACE.modular_inverse(hol_mod, prime)
    return FACE.matmul_mod(mixed_mod, inverse, prime)


def mode3_apply(a, b, c, tensor, prime):
    out = np.tensordot(a, tensor, axes=(1, 0)) % prime
    out = np.tensordot(b, out, axes=(1, 1)).transpose(1, 0, 2) % prime
    out = np.tensordot(c, out, axes=(1, 2)).transpose(1, 2, 0) % prime
    return out


def matrix_to_local_tensor(matrix, dimensions):
    return matrix.reshape((*dimensions, *dimensions)).transpose(
        0, 3, 1, 4, 2, 5
    ).reshape(tuple(d * d for d in dimensions))


def local_tensor_to_matrix(tensor, dimensions):
    return tensor.reshape(
        dimensions[0], dimensions[0],
        dimensions[1], dimensions[1],
        dimensions[2], dimensions[2],
    ).transpose(0, 2, 4, 1, 3, 5).reshape(
        int(np.prod(dimensions)), int(np.prod(dimensions))
    )


def inverse_mod(matrix, prime):
    return np.asarray(FACE.modular_inverse(matrix.tolist(), prime), dtype=np.int64)


def rank_mod(matrix, prime):
    return FACE.rank_mod(matrix, prime)


def source_data(labels, prime):
    triples = list(product(range(5), repeat=3))
    cache = {}
    output = []
    for block_index, first, second in labels:
        shapes = triples[int(block_index)]
        if shapes not in cache:
            _, _, exact_range = KCHART.hol_k_coordinates(shapes)
            cache[shapes] = matrix_mod(exact_range, prime)
        basis = cache[shapes]
        first = int(first)
        second = int(second)
        matrix = np.outer(basis[:, first], basis[:, second]) % prime
        if first != second:
            matrix = (matrix + np.outer(basis[:, second], basis[:, first])) % prime
        dimensions = tuple(BRIDGE.HOL_MULTS[s] for s in shapes)
        output.append((shapes, dimensions, matrix))
    return output


def crossed_matrix(source, mixed_shapes, crossing, hol_ranges, mixed_ranges, prime):
    hol_shapes, hol_dimensions, matrix = source
    tensor = matrix_to_local_tensor(matrix, hol_dimensions)
    maps = [
        crossing[np.ix_(mixed_ranges[mu].reshape(-1),
                        hol_ranges[lam].reshape(-1))]
        for mu, lam in zip(mixed_shapes, hol_shapes)
    ]
    crossed = mode3_apply(*maps, tensor, prime)
    mixed_dimensions = tuple(BRIDGE.MIXED_MULTS[s] for s in mixed_shapes)
    return local_tensor_to_matrix(crossed, mixed_dimensions) % prime


def replay(certificate_path, prime):
    certificate = np.load(certificate_path)
    source_labels = certificate["source_labels"]
    row_shapes = certificate["row_shapes"]
    row_indices = certificate["row_indices"]
    column_indices = certificate["column_indices"]
    assert source_labels.shape == (EXPECTED_RANK, 3)
    assert row_shapes.shape == (EXPECTED_RANK, 3)

    crossing = local_crossing_mod(prime)
    hol_ranges = block_ranges(BRIDGE.HOL_MULTS)
    mixed_ranges = block_ranges(BRIDGE.MIXED_MULTS)
    sources = source_data(source_labels, prime)
    minor = np.zeros((EXPECTED_RANK, EXPECTED_RANK), dtype=np.int64)

    unique_shapes = sorted(set(tuple(map(int, row)) for row in row_shapes))
    for count, shapes in enumerate(unique_shapes, 1):
        selected_rows = np.flatnonzero(np.all(row_shapes == shapes, axis=1))
        exact_face, _ = FCHART.face_chart(shapes)
        face = matrix_mod(exact_face, prime)
        pivot_key = "face_rows_" + "".join(map(str, shapes))
        pivots = certificate[pivot_key].astype(int)
        principal = face[pivots, :]
        assert rank_mod(principal, prime) == face.shape[1]
        principal_inverse = inverse_mod(principal, prime)

        crossed = [
            crossed_matrix(source, shapes, crossing, hol_ranges, mixed_ranges, prime)
            for source in sources
        ]
        for row in selected_rows:
            q = int(row_indices[row])
            s = int(column_indices[row])
            alpha = face[q, :] @ principal_inverse % prime
            for column, matrix in enumerate(crossed):
                minor[row, column] = (
                    matrix[q, s] - alpha @ matrix[pivots, s]
                ) % prime
        print(" prime", prime, "block", count, "/", len(unique_shapes), shapes,
              flush=True)

    rank = rank_mod(minor, prime)
    assert rank == EXPECTED_RANK
    return rank, minor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        default="/tmp/dth_direct_defect_minor334.npz",
    )
    parser.add_argument("--prime", type=int, action="append")
    args = parser.parse_args()
    primes = tuple(args.prime) if args.prime else PRIMES
    for prime in primes:
        rank, _ = replay(args.certificate, prime)
        print("prime", prime, "direct DTH defect minor rank:", rank)
    print("exact modular 334-dimensional DTH defect minor passed")


if __name__ == "__main__":
    main()
