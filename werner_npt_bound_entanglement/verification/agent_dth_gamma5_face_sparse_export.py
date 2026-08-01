#!/usr/bin/env python3
"""Export exact integer charts for the 751-rank reduced Gamma5 face.

This is an independent sparse-ambient construction of the same charts used
by the final-slot CRT verifier.  It avoids dense representation matrices.
For each of the 56 unordered local-type triples it:

1. constructs the raw tensor-product highest-weight basis;
2. applies the pair/Pluecker projector coefficientwise;
3. extracts an exact support basis by rational sparse elimination;
4. applies ``D5=d0^tensor3+d2^tensor3``;
5. lifts exact kernel relations back to face vectors; and
6. records ``E5[i,k]=<raw_i,face_k>``.

Thus ``E5=G5*K5`` is directly in the raw LAST highest-weight restriction
coordinates.  Each column is independently scaled to a primitive integer
column.  Ordered blocks are obtained by exact physical-site permutation;
the output contains all 216 blocks and nonsingular pivot rows.

The gzip JSON artifact contains integers only and is deterministic.  No
floating-point arithmetic or external package is used.
"""

from fractions import Fraction as F
from functools import reduce
from itertools import permutations, product
from math import gcd
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, "verification")
import agent_dth_block_census as census
import agent_dth_gamma5_000_chart as dense_000
import agent_dth_gamma5_face_exact as face
import agent_dth_last_crossing_exact as last


EXPECTED_REDUCED_SUPPORT = 772
EXPECTED_REDUCED_DELTA = 21
EXPECTED_REDUCED_FACE = 751
EXPECTED_ACTIVE = 188
EXPECTED_FULL_SUPPORT = 1_194_102
EXPECTED_FULL_DELTA = 6_552
EXPECTED_FULL_FACE = 1_187_550
D5_DEFECT_TYPES = {
    (1, 1, 3), (1, 3, 3), (1, 3, 5),
    (3, 3, 3), (3, 3, 5), (3, 5, 5),
}


def add_scaled(vectors, coefficients):
    output = {}
    for index, coefficient in coefficients.items():
        output = census.add(output, census.scale(coefficient, vectors[index]))
    return output


def primitive_integer_columns(matrix):
    """Scale each rational column to a primitive integral column."""
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    output = [[0 for _ in range(columns)] for _ in range(rows)]
    for column in range(columns):
        denominators = [matrix[row][column].denominator
                        for row in range(rows)]
        common = 1
        for denominator in denominators:
            common = common * denominator // gcd(common, denominator)
        integers = [matrix[row][column].numerator
                    * (common // matrix[row][column].denominator)
                    for row in range(rows)]
        divisor = reduce(gcd, (abs(value) for value in integers if value), 0)
        assert divisor
        integers = [value // divisor for value in integers]
        first = next(value for value in integers if value)
        if first < 0:
            integers = [-value for value in integers]
        for row, value in enumerate(integers):
            output[row][column] = value
    return output


def pivot_rows(matrix):
    if not matrix or not matrix[0]:
        return []
    rows_as_columns = [
        {column: F(value) for column, value in enumerate(row) if value}
        for row in matrix
    ]
    independent, _ = census.exact_column_echelon(rows_as_columns)
    rank = len(matrix[0])
    assert len(independent) == rank
    return independent


def canonical_chart(shapes, bases, include_support=False):
    if shapes == (5, 5, 5):
        matrix = [list(row) for row in dense_000.PRIMITIVE_CHART]
        result = {
            "raw_rank": dense_000.RAW_RANK,
            "support_rank": dense_000.SUPPORT_RANK,
            "delta_rank": dense_000.DELTA_RANK,
            "face_rank": dense_000.FACE_RANK,
            "matrix": matrix,
            "pivot_rows": list(dense_000.PIVOT_ROWS),
        }
        if include_support:
            result["support_matrix"] = matrix
            result["support_pivot_rows"] = list(dense_000.PIVOT_ROWS)
        return result
    raw = [census.tensor3(left, middle, right)
           for left in bases[shapes[0]]
           for middle in bases[shapes[1]]
           for right in bases[shapes[2]]]
    projected = [census.source_project(vector) for vector in raw]
    independent, _ = census.exact_column_echelon(projected)
    support = [projected[index] for index in independent]
    plus = [face.combined_delta(vector, 1) for vector in support]
    minus = [face.combined_delta(vector, -1) for vector in support]
    assert all(not vector for vector in minus)
    delta_independent, relations = census.exact_column_echelon(plus)
    face_vectors = [add_scaled(support, relation) for relation in relations]
    restriction = [
        [census.inner(raw_vector, face_vector)
         for face_vector in face_vectors]
        for raw_vector in raw
    ]
    integral = primitive_integer_columns(restriction) if face_vectors else [
        [] for _ in raw
    ]
    pivots = pivot_rows(integral)
    assert len(independent) == len(delta_independent) + len(relations)
    result = {
        "raw_rank": len(raw),
        "support_rank": len(independent),
        "delta_rank": len(delta_independent),
        "face_rank": len(relations),
        "matrix": integral,
        "pivot_rows": pivots,
    }
    if include_support:
        support_restriction = [
            [census.inner(raw_vector, support_vector)
             for support_vector in support]
            for raw_vector in raw
        ]
        support_integral = primitive_integer_columns(support_restriction)
        result["support_matrix"] = support_integral
        result["support_pivot_rows"] = pivot_rows(support_integral)
    return result


def unflatten(index, dimensions):
    output = [0] * len(dimensions)
    for position in range(len(dimensions) - 1, -1, -1):
        output[position] = index % dimensions[position]
        index //= dimensions[position]
    assert index == 0
    return tuple(output)


def flatten(indices, dimensions):
    output = 0
    for index, dimension in zip(indices, dimensions):
        output = output * dimension + index
    return output


def first_axis_permutation(canonical, ordered):
    """Return ``p`` with ``ordered[i]=canonical[p[i]]``."""
    return next(
        permutation for permutation in permutations(range(3))
        if tuple(canonical[index] for index in permutation) == ordered
    )


def permuted_chart(canonical_shapes, ordered_shapes, block):
    permutation = first_axis_permutation(canonical_shapes, ordered_shapes)
    canonical_dimensions = tuple(last.LAST_MULTS[s]
                                 for s in canonical_shapes)
    ordered_dimensions = tuple(last.LAST_MULTS[s] for s in ordered_shapes)
    row_map = []
    for ordered_row in range(block["raw_rank"]):
        ordered_indices = unflatten(ordered_row, ordered_dimensions)
        canonical_indices = [None, None, None]
        for ordered_axis, canonical_axis in enumerate(permutation):
            canonical_indices[canonical_axis] = ordered_indices[ordered_axis]
        row_map.append(flatten(tuple(canonical_indices), canonical_dimensions))

    matrix = [block["matrix"][canonical_row] for canonical_row in row_map]
    inverse_row_map = [None] * len(row_map)
    for ordered_row, canonical_row in enumerate(row_map):
        inverse_row_map[canonical_row] = ordered_row
    pivots = [inverse_row_map[row] for row in block["pivot_rows"]]
    assert len(set(row_map)) == block["raw_rank"]
    selected_rows = [
        {column: F(matrix[row][column])
         for column in range(block["face_rank"])
         if matrix[row][column]}
        for row in pivots
    ]
    independent, _ = census.exact_column_echelon(selected_rows)
    assert len(independent) == block["face_rank"]
    return {
        "raw_rank": block["raw_rank"],
        "support_rank": block["support_rank"],
        "delta_rank": block["delta_rank"],
        "face_rank": block["face_rank"],
        "matrix": matrix,
        "pivot_rows": pivots,
    }


def block_key(shapes):
    return ",".join(map(str, shapes))


def checkpoint_path(directory, shapes):
    return directory / ("block_" + "_".join(map(str, shapes)) + ".json.gz")


def save_checkpoint(directory, shapes, block):
    directory.mkdir(parents=True, exist_ok=True)
    payload = {
        "format": "dth-gamma5-canonical-chart-v1",
        "shapes": list(shapes),
        "block": block,
    }
    body = json.dumps(payload, sort_keys=True,
                      separators=(",", ":")).encode("ascii")
    wrapper = json.dumps({
        "sha256": hashlib.sha256(body).hexdigest(),
        "payload": payload,
    }, sort_keys=True, separators=(",", ":")).encode("ascii")
    path = checkpoint_path(directory, shapes)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with open(temporary, "wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb",
                           compresslevel=9, mtime=0) as handle:
            handle.write(wrapper)
    os.replace(temporary, path)


def load_checkpoint(directory, shapes, require_support=False):
    path = checkpoint_path(directory, shapes)
    if not path.exists():
        return None
    try:
        with gzip.open(path, "rb") as handle:
            wrapper = json.loads(handle.read().decode("ascii"))
        payload = wrapper["payload"]
        body = json.dumps(payload, sort_keys=True,
                          separators=(",", ":")).encode("ascii")
        assert wrapper["sha256"] == hashlib.sha256(body).hexdigest()
        assert payload["format"] == "dth-gamma5-canonical-chart-v1"
        assert tuple(payload["shapes"]) == tuple(shapes)
        block = payload["block"]
        assert block["raw_rank"] == len(block["matrix"])
        assert block["face_rank"] == (
            len(block["matrix"][0]) if block["matrix"] else 0
        )
        assert len(block["pivot_rows"]) == block["face_rank"]
        if require_support:
            assert len(block["support_matrix"]) == block["raw_rank"]
            assert len(block["support_pivot_rows"]) == block["support_rank"]
        return block
    except (AssertionError, EOFError, OSError, ValueError, KeyError,
            json.JSONDecodeError, gzip.BadGzipFile):
        return None


def matrix_columns(matrix):
    if not matrix or not matrix[0]:
        return []
    return [
        {row: F(matrix[row][column])
         for row in range(len(matrix)) if matrix[row][column]}
        for column in range(len(matrix[0]))
    ]


def audit_permuted_column_space(canonical_shapes, ordered_shapes,
                                canonical_block, bases):
    """Compare the induced site permutation with a direct exact rebuild."""
    induced = permuted_chart(canonical_shapes, ordered_shapes, canonical_block)
    direct = canonical_chart(ordered_shapes, bases)
    assert induced["face_rank"] == direct["face_rank"]
    left = matrix_columns(induced["matrix"])
    right = matrix_columns(direct["matrix"])
    independent_left, _ = census.exact_column_echelon(left)
    independent_right, _ = census.exact_column_echelon(right)
    independent_joined, _ = census.exact_column_echelon(left + right)
    rank = induced["face_rank"]
    assert len(independent_left) == len(independent_right) == rank
    assert len(independent_joined) == rank


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--checkpoint-dir")
    args = parser.parse_args()
    checkpoint_directory = Path(
        args.checkpoint_dir or (args.output + ".parts")
    )

    bases = face.target_word_bases()
    canonical = {}
    for number, shapes in enumerate(face.unordered_triples(6), 1):
        include_support = shapes in D5_DEFECT_TYPES
        block = load_checkpoint(checkpoint_directory, shapes,
                                require_support=include_support)
        cached = block is not None
        if block is None:
            block = canonical_chart(shapes, bases,
                                    include_support=include_support)
            save_checkpoint(checkpoint_directory, shapes, block)
        canonical[shapes] = block
        print("canonical chart", number, "/56",
              "/".join(last.LAST_NAMES[index] for index in shapes),
              "support/delta/face",
              block["support_rank"], block["delta_rank"],
              block["face_rank"], "cached" if cached else "computed",
              flush=True)

    # Exact nontrivial site-permutation audits.  The second block is one of
    # the six crossed-support correction types, so this checks both a plain
    # Pluecker face and a genuine D5-kernel face.
    audit_permuted_column_space((0, 3, 4), (4, 0, 3),
                                canonical[(0, 3, 4)], bases)
    audit_permuted_column_space((1, 3, 5), (5, 1, 3),
                                canonical[(1, 3, 5)], bases)
    print("exact site-permutation chart audits passed", flush=True)

    blocks = {}
    reduced_support = reduced_delta = reduced_face = active = 0
    full_support = full_delta = full_face = 0
    for shapes in product(range(6), repeat=3):
        canonical_shapes = tuple(sorted(shapes))
        block = permuted_chart(canonical_shapes, shapes,
                               canonical[canonical_shapes])
        blocks[block_key(shapes)] = block
        reduced_support += block["support_rank"]
        reduced_delta += block["delta_rank"]
        reduced_face += block["face_rank"]
        active += int(block["face_rank"] > 0)
        carrier = reduce(
            lambda left, right: left * right,
            (last.LAST_IRREP_DIMS[shape] for shape in shapes),
            1,
        )
        full_support += carrier * block["support_rank"]
        full_delta += carrier * block["delta_rank"]
        full_face += carrier * block["face_rank"]

    assert reduced_support == EXPECTED_REDUCED_SUPPORT
    assert reduced_delta == EXPECTED_REDUCED_DELTA
    assert reduced_face == EXPECTED_REDUCED_FACE
    assert active == EXPECTED_ACTIVE
    assert full_support == EXPECTED_FULL_SUPPORT
    assert full_delta == EXPECTED_FULL_DELTA
    assert full_face == EXPECTED_FULL_FACE

    payload = {
        "format": "dth-gamma5-face-integer-charts-v1",
        "last_names": list(last.LAST_NAMES),
        "last_multiplicities": list(last.LAST_MULTS),
        "reduced_support_rank": reduced_support,
        "reduced_delta_rank": reduced_delta,
        "reduced_face_rank": reduced_face,
        "active_blocks": active,
        "full_support_dimension": full_support,
        "full_delta_rank": full_delta,
        "full_face_dimension": full_face,
        "blocks": blocks,
    }
    encoded = json.dumps(payload, sort_keys=True,
                         separators=(",", ":")).encode("ascii")
    digest = hashlib.sha256(encoded).hexdigest()
    with open(args.output, "wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb",
                           compresslevel=9, mtime=0) as handle:
            handle.write(encoded)

    print("exact sparse Gamma5 chart export passed")
    print("reduced support/delta/face:",
          reduced_support, reduced_delta, reduced_face)
    print("active blocks:", active)
    print("full support/delta/face:",
          full_support, full_delta, full_face)
    print("uncompressed bytes:", len(encoded))
    print("payload sha256:", digest)
    print("saved:", args.output)


if __name__ == "__main__":
    main()
