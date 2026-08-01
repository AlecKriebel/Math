#!/usr/bin/env python3
"""Exact finite-field equality of the Gamma1 and Gamma5 defect spaces.

The constrained five-replica DTH source is stored in the 4,139 symmetric
coordinates of the exact holomorphic K charts.  This verifier constructs
two literal systems of range-membership equations on that same source:

* the previously certified 334 Gamma1 product-face equations; and
* the 339 canonical Gamma5 pair-support/``D5``-face equations.

All highest-weight charts, crossings, and face interpolation rows are
rebuilt from exact rational or integer data.  For each requested prime the
program proves that the two pulled-back row spaces both have rank 334 and
are equal.  Floating-point arithmetic is not used.

This is a finite-field structural certificate.  It is auxiliary to the
bounded-CRT replay of the rational pseudomoment itself; by itself it does
not assert equality of the two row spaces over QQ.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import argparse
import gzip
import hashlib
import importlib.util
import json
import math

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


OLD = import_file(
    "dth_defect_equality_old",
    ROOT / "discovery" / "agent_dth_exact_obstruction_generator.py",
)
DIRECT = import_file(
    "dth_defect_equality_direct", HERE / "agent_dth_defect_minor_modular.py"
)
G5 = import_file(
    "dth_defect_equality_gamma5", HERE / "agent_dth_gamma5_face_crt.py"
)


PRIMES = (1_000_003, 1_000_033)
HOL_SCALE = 360
SOURCE_DIMENSION = 4_139
GAMMA1_RANK = 334
GAMMA5_CANDIDATES = 339
CERTIFICATE_DIRECTORY = HERE / "certificates"
EXPECTED_HASHES = {
    "labels": "5ac03d9bd7b942d8e928921614d7b612f320063e869ff0d3c63d4323eaf5368f",
    "face": "6caf453f0043a2e7296b31e2f14bc90b01f38163b1d89ece39276ac625ded9aa",
    "support": "05ead1ec64ccb0e6858e2b65c7d6cbda08e3aee452783fcfcc88705ce23fa3a8",
}
EXPECTED_GAMMA5_LABEL_SHA256 = (
    "e7b6fd688c9f0033dae3852fd4bbdeb741c63da796bc4cb79648a3d54941e61b"
)


def rational_mod(value, prime):
    numerator, denominator = value.as_numer_denom()
    return (
        int(numerator) % prime
        * pow(int(denominator) % prime, -1, prime)
        % prime
    )


def sympy_matrix_mod(matrix, prime):
    return np.asarray(
        [
            [rational_mod(matrix[row, column], prime)
             for column in range(matrix.cols)]
            for row in range(matrix.rows)
        ],
        dtype=np.int64,
    )


def inverse_mod(matrix, prime):
    return np.asarray(
        DIRECT.FACE.modular_inverse(
            np.asarray(matrix, dtype=np.int64).tolist(), prime
        ),
        dtype=np.int64,
    )


def rank_mod(matrix, prime):
    return DIRECT.FACE.rank_mod(np.asarray(matrix, dtype=np.int64), prime)


def block_ranges(multiplicities):
    output = []
    offset = 0
    for multiplicity in multiplicities:
        block = np.arange(
            offset, offset + multiplicity * multiplicity
        ).reshape(multiplicity, multiplicity)
        output.append(block)
        offset += multiplicity * multiplicity
    assert offset == 103
    return output


def matrix_batch_to_local_tensor(matrices, dimensions):
    count = matrices.shape[0]
    return matrices.reshape(
        count,
        dimensions[0], dimensions[1], dimensions[2],
        dimensions[0], dimensions[1], dimensions[2],
    ).transpose(1, 4, 2, 5, 3, 6, 0).reshape(
        dimensions[0] ** 2,
        dimensions[1] ** 2,
        dimensions[2] ** 2,
        count,
    )


def local_tensor_to_matrix_batch(tensor, dimensions):
    count = tensor.shape[-1]
    size = math.prod(dimensions)
    return tensor.reshape(
        dimensions[0], dimensions[0],
        dimensions[1], dimensions[1],
        dimensions[2], dimensions[2], count,
    ).transpose(6, 0, 2, 4, 1, 3, 5).reshape(count, size, size)


def mode3_apply_batch(first, second, third, tensor, prime):
    output = np.tensordot(first, tensor, axes=(1, 0)) % prime
    output = (
        np.tensordot(second, output, axes=(1, 1)).transpose(1, 0, 2, 3)
        % prime
    )
    return (
        np.tensordot(third, output, axes=(1, 2)).transpose(1, 2, 0, 3)
        % prime
    )


def exact_integer_hol_ranges():
    """Return ``360 E_lambda`` and the common 4,139-coordinate sections."""
    ranges = {}
    sections = {}
    offset = 0
    for count, shapes in enumerate(product(range(5), repeat=3), 1):
        exact = OLD.KMOD.hol_k_coordinates(shapes)[2]
        integer = np.asarray(
            [
                [int(HOL_SCALE * exact[row, column])
                 for column in range(exact.cols)]
                for row in range(exact.rows)
            ],
            dtype=np.int64,
        )
        ranges[shapes] = integer
        rank = integer.shape[1]
        length = rank * (rank + 1) // 2
        sections[shapes] = slice(offset, offset + length)
        offset += length
        if count % 25 == 0:
            print("integer hol ranges", count, "/125", flush=True)
    assert offset == SOURCE_DIMENSION
    return ranges, sections


def crossing_mod(cut, prime):
    if cut == 1:
        numerator = OLD.exact_crossing_numerator()
        multiplicities = tuple(OLD.BRIDGE.MIXED_MULTS)
    elif cut == 5:
        numerator, denominator = G5.exact_crossing_numerator()
        inverse = pow(int(denominator) % prime, -1, prime)
        numerator = np.asarray(numerator, dtype=object)
        numerator = np.asarray(
            [[int(value) % prime * inverse % prime for value in row]
             for row in numerator],
            dtype=np.int64,
        )
        multiplicities = tuple(G5.LAST.LAST_MULTS)
        return numerator, multiplicities
    else:
        raise ValueError(cut)
    # The common crossing denominator is irrelevant to a row space, but
    # retaining it makes this literally the exact partial transpose map.
    denominator = OLD.CROSS_SCALE
    inverse = pow(denominator % prime, -1, prime)
    matrix = np.asarray(
        [[int(value) % prime * inverse % prime for value in row]
         for row in numerator],
        dtype=np.int64,
    )
    return matrix, multiplicities


def primitive_left_mod(face, pivots, q, prime):
    principal = face[list(pivots), :]
    inverse = inverse_mod(principal, prime)
    alpha = face[q, :] @ inverse % prime
    left = np.zeros(face.shape[0], dtype=np.int64)
    left[q] = 1
    left[list(pivots)] = -alpha % prime
    assert not np.any(left @ face % prime)
    return left


def read_integer_artifact(path, expected_format):
    with gzip.open(path, "rt", encoding="ascii") as handle:
        payload = json.load(handle)
    assert payload["format"] == expected_format
    return payload


def read_gamma1_certificate(path):
    path = Path(path)
    with gzip.open(path, "rt", encoding="ascii") as handle:
        payload = json.load(handle)
    assert payload["format"] == "dth-defect-labels334-v1"
    certificate = {
        "source_columns": np.asarray(payload["source_columns"], dtype=int),
        "row_shapes": np.asarray(payload["row_shapes"], dtype=int),
        "row_indices": np.asarray(payload["row_indices"], dtype=int),
        "column_indices": np.asarray(payload["column_indices"], dtype=int),
    }
    for tag, rows in payload["face_rows"].items():
        certificate["face_rows_" + tag] = np.asarray(rows, dtype=int)
    assert certificate["source_columns"].shape == (GAMMA1_RANK,)
    assert certificate["row_shapes"].shape == (GAMMA1_RANK, 3)
    return certificate


def verify_hash(path, expected):
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    assert actual == expected, (path, actual, expected)


def gamma1_functionals(certificate, prime):
    grouped = {}
    cache = {}
    for shapes_array, q, column in zip(
        certificate["row_shapes"],
        certificate["row_indices"],
        certificate["column_indices"],
    ):
        shapes = tuple(map(int, shapes_array))
        q, column = int(q), int(column)
        if shapes not in cache:
            face, _ = OLD.FMOD.face_chart(shapes)
            face_mod = sympy_matrix_mod(face, prime)
            pivots = tuple(map(
                int,
                certificate["face_rows_" + "".join(map(str, shapes))],
            ))
            cache[shapes] = face_mod, pivots
        face_mod, pivots = cache[shapes]
        left = primitive_left_mod(face_mod, pivots, q, prime)
        matrix = np.zeros(
            (face_mod.shape[0], face_mod.shape[0]), dtype=np.int64
        )
        matrix[:, column] = left
        grouped.setdefault(shapes, []).append(matrix)
    assert sum(map(len, grouped.values())) == GAMMA1_RANK
    return {
        shapes: np.asarray(matrices, dtype=np.int64)
        for shapes, matrices in grouped.items()
    }


def select_gamma5_labels(face_payload, support_payload, prime):
    """Choose exact quotient rows once, using deterministic modular pivots."""
    labels = []
    for key in sorted(support_payload["blocks"]):
        shapes = tuple(map(int, key.split(",")))
        support_block = support_payload["blocks"][key]
        face_block = face_payload["blocks"][key]
        support = np.asarray(support_block["matrix"], dtype=np.int64) % prime
        face = np.asarray(face_block["matrix"], dtype=np.int64) % prime
        face_pivots = tuple(map(int, face_block["pivot_rows"]))
        support_pivots = tuple(map(int, support_block["pivot_rows"]))
        delta_rank = int(support_block["delta_rank"])
        outside = [row for row in range(face.shape[0])
                   if row not in set(face_pivots)]
        chosen = []
        coupling_rows = []
        current_rank = 0
        for q in outside:
            left = primitive_left_mod(face, face_pivots, q, prime)
            coupling = left @ support % prime
            trial = coupling_rows + [coupling]
            rank = rank_mod(np.asarray(trial, dtype=np.int64), prime)
            if rank > current_rank:
                chosen.append(q)
                coupling_rows.append(coupling)
                current_rank = rank
                if current_rank == delta_rank:
                    break
        assert current_rank == delta_rank, (shapes, current_rank, delta_rank)
        for q in chosen:
            for column in support_pivots:
                labels.append((shapes, q, int(column)))
    assert len(labels) == GAMMA5_CANDIDATES
    return tuple(labels)


def gamma5_functionals(labels, face_payload, prime):
    grouped = {}
    cache = {}
    for shapes, q, column in labels:
        if shapes not in cache:
            block = face_payload["blocks"][",".join(map(str, shapes))]
            face = np.asarray(block["matrix"], dtype=np.int64) % prime
            pivots = tuple(map(int, block["pivot_rows"]))
            cache[shapes] = face, pivots
        face, pivots = cache[shapes]
        left = primitive_left_mod(face, pivots, q, prime)
        matrix = np.zeros((face.shape[0], face.shape[0]), dtype=np.int64)
        matrix[:, column] = left
        grouped.setdefault(shapes, []).append(matrix)
    assert sum(map(len, grouped.values())) == GAMMA5_CANDIDATES
    return {
        shapes: np.asarray(matrices, dtype=np.int64)
        for shapes, matrices in grouped.items()
    }


def pullback_rows(functionals, crossing, target_multiplicities,
                  hol_ranges, sections, prime, batch_size=12):
    """Pull literal target functionals to all 4,139 source coordinates."""
    hol_block_ranges = block_ranges(OLD.BRIDGE.HOL_MULTS)
    target_block_ranges = block_ranges(target_multiplicities)
    total = sum(matrices.shape[0] for matrices in functionals.values())
    rows = np.zeros((total, SOURCE_DIMENSION), dtype=np.int64)
    offset = 0
    for shapes in sorted(functionals):
        matrices = functionals[shapes]
        target_dimensions = tuple(target_multiplicities[s] for s in shapes)
        for start in range(0, len(matrices), batch_size):
            batch = matrices[start:start + batch_size]
            target_tensor = matrix_batch_to_local_tensor(
                batch, target_dimensions
            )
            destination = rows[offset + start:offset + start + len(batch)]
            for hol_shapes in product(range(5), repeat=3):
                source_range = hol_ranges[hol_shapes] % prime
                rank = source_range.shape[1]
                if not rank:
                    continue
                maps = [
                    crossing[np.ix_(
                        target_block_ranges[target_shape].reshape(-1),
                        hol_block_ranges[hol_shape].reshape(-1),
                    )]
                    for target_shape, hol_shape in zip(shapes, hol_shapes)
                ]
                if any(not np.any(matrix) for matrix in maps):
                    continue
                pulled = mode3_apply_batch(
                    maps[0].T, maps[1].T, maps[2].T,
                    target_tensor, prime,
                )
                source_dimensions = tuple(
                    OLD.BRIDGE.HOL_MULTS[s] for s in hol_shapes
                )
                source_matrices = local_tensor_to_matrix_batch(
                    pulled, source_dimensions
                )
                left = np.einsum(
                    "ia,qij->qaj", source_range, source_matrices,
                    optimize=True,
                ) % prime
                compressed = np.einsum(
                    "qaj,jb->qab", left, source_range, optimize=True
                ) % prime
                values = [compressed[:, i, i] for i in range(rank)]
                values.extend(
                    (compressed[:, i, j] + compressed[:, j, i]) % prime
                    for i in range(rank) for j in range(i + 1, rank)
                )
                if values:
                    destination[:, sections[hol_shapes]] = (
                        np.stack(values, axis=1) % prime
                    )
        offset += len(matrices)
        print("pulled", shapes, len(matrices), "rows", flush=True)
    assert offset == total
    return rows


def replay(prime, certificate, face_payload, support_payload,
           hol_ranges, sections, labels):
    crossing1, multiplicities1 = crossing_mod(1, prime)
    crossing5, multiplicities5 = crossing_mod(5, prime)
    functions1 = gamma1_functionals(certificate, prime)
    functions5 = gamma5_functionals(labels, face_payload, prime)
    rows1 = pullback_rows(
        functions1, crossing1, multiplicities1,
        hol_ranges, sections, prime,
    )
    rows5 = pullback_rows(
        functions5, crossing5, multiplicities5,
        hol_ranges, sections, prime,
    )

    source_columns = certificate["source_columns"].astype(int)
    minor1 = rows1[:, source_columns]
    rank1 = rank_mod(minor1, prime)
    assert rank1 == GAMMA1_RANK
    inverse1 = inverse_mod(minor1, prime)
    coefficients = rows5[:, source_columns] @ inverse1 % prime
    residual = (rows5 - coefficients @ rows1) % prime
    assert not np.any(residual), tuple(map(int, np.argwhere(residual)[0]))
    rank5 = rank_mod(rows5[:, source_columns], prime)
    assert rank5 == GAMMA1_RANK
    union_rank = rank1
    print(
        "prime", prime,
        "Gamma1/Gamma5/union ranks:", rank1, rank5, union_rank,
        flush=True,
    )
    return rank1, rank5, union_rank


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gamma1-certificate",
        default=CERTIFICATE_DIRECTORY / "dth_defect_labels334.json.gz",
    )
    parser.add_argument(
        "--gamma5-face",
        default=CERTIFICATE_DIRECTORY / "dth_gamma5_face_integer_charts.json.gz",
    )
    parser.add_argument(
        "--gamma5-support",
        default=(
            CERTIFICATE_DIRECTORY / "dth_gamma5_defect_support_charts.json.gz"
        ),
    )
    parser.add_argument("--prime", type=int, action="append")
    args = parser.parse_args()

    verify_hash(args.gamma1_certificate, EXPECTED_HASHES["labels"])
    verify_hash(args.gamma5_face, EXPECTED_HASHES["face"])
    verify_hash(args.gamma5_support, EXPECTED_HASHES["support"])
    certificate = read_gamma1_certificate(args.gamma1_certificate)
    face_payload = read_integer_artifact(
        args.gamma5_face, "dth-gamma5-face-integer-charts-v1"
    )
    support_payload = read_integer_artifact(
        args.gamma5_support,
        "dth-gamma5-defect-support-integer-charts-v1",
    )
    hol_ranges, sections = exact_integer_hol_ranges()
    labels = select_gamma5_labels(face_payload, support_payload, PRIMES[0])
    serialized_labels = np.asarray(
        [(*shapes, q, column) for shapes, q, column in labels], dtype="<i8"
    ).tobytes()
    label_digest = hashlib.sha256(serialized_labels).hexdigest()
    assert label_digest == EXPECTED_GAMMA5_LABEL_SHA256
    print("Gamma5 equation-label sha256:", label_digest, flush=True)
    primes = tuple(args.prime) if args.prime else PRIMES
    for prime in primes:
        replay(
            prime, certificate, face_payload, support_payload,
            hol_ranges, sections, labels,
        )
    print("exact finite-field Gamma1/Gamma5 defect equality passed")


if __name__ == "__main__":
    main()
