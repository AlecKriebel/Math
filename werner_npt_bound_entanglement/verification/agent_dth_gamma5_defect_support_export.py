#!/usr/bin/env python3
"""Export exact pair/Pluecker support charts in the 19 D5-defect blocks.

The exact Gamma5 face differs from pair/Pluecker support in only nineteen
ordered local Schur blocks, arising from six unordered type multisets.  This
small companion to ``agent_dth_gamma5_face_sparse_export.py`` exports a
primitive integer restriction chart ``E_pair`` and nonsingular pivot rows in
exactly those blocks.  It is used when an exact correction must move inside
the larger pair/Pluecker support before imposing ``ker D5``.
"""

from itertools import permutations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, "verification")
import agent_dth_gamma5_face_sparse_export as export
import agent_dth_last_crossing_exact as last


DEFECT_TYPES = (
    (1, 1, 3),  # 30,30,11
    (1, 3, 3),  # 30,11,11
    (1, 3, 5),  # 30,11,00
    (3, 3, 3),  # 11,11,11
    (3, 3, 5),  # 11,11,00
    (3, 5, 5),  # 11,00,00
)


def ordered_orbit(shapes):
    return sorted(set(permutations(shapes)))


def permute_support(canonical_shapes, ordered_shapes, block):
    permutation = export.first_axis_permutation(canonical_shapes,
                                                ordered_shapes)
    canonical_dimensions = tuple(last.LAST_MULTS[s]
                                 for s in canonical_shapes)
    ordered_dimensions = tuple(last.LAST_MULTS[s] for s in ordered_shapes)
    row_map = []
    for ordered_row in range(block["raw_rank"]):
        ordered_indices = export.unflatten(ordered_row, ordered_dimensions)
        canonical_indices = [None, None, None]
        for ordered_axis, canonical_axis in enumerate(permutation):
            canonical_indices[canonical_axis] = ordered_indices[ordered_axis]
        row_map.append(export.flatten(tuple(canonical_indices),
                                      canonical_dimensions))
    matrix = [block["support_matrix"][row] for row in row_map]
    inverse = [None] * len(row_map)
    for ordered_row, canonical_row in enumerate(row_map):
        inverse[canonical_row] = ordered_row
    pivots = [inverse[row] for row in block["support_pivot_rows"]]
    selected = [
        {column: export.F(matrix[row][column])
         for column in range(block["support_rank"])
         if matrix[row][column]}
        for row in pivots
    ]
    independent, _ = export.census.exact_column_echelon(selected)
    assert len(independent) == block["support_rank"]
    return {
        "raw_rank": block["raw_rank"],
        "support_rank": block["support_rank"],
        "delta_rank": block["delta_rank"],
        "face_rank": block["face_rank"],
        "matrix": matrix,
        "pivot_rows": pivots,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--checkpoint-dir")
    args = parser.parse_args()
    checkpoint_directory = Path(
        args.checkpoint_dir or (args.output + ".parts")
    )

    bases = export.face.target_word_bases()
    blocks = {}
    ordered_count = support_sum = delta_sum = face_sum = 0
    for number, shapes in enumerate(DEFECT_TYPES, 1):
        canonical = export.load_checkpoint(checkpoint_directory, shapes,
                                           require_support=True)
        cached = canonical is not None
        if canonical is None:
            canonical = export.canonical_chart(shapes, bases,
                                               include_support=True)
            export.save_checkpoint(checkpoint_directory, shapes, canonical)
        assert canonical["delta_rank"] > 0
        for ordered in ordered_orbit(shapes):
            block = permute_support(shapes, ordered, canonical)
            blocks[export.block_key(ordered)] = block
            ordered_count += 1
            support_sum += block["support_rank"]
            delta_sum += block["delta_rank"]
            face_sum += block["face_rank"]
        print("defect support chart", number, "/6",
              "/".join(last.LAST_NAMES[index] for index in shapes),
              canonical["support_rank"], canonical["delta_rank"],
              canonical["face_rank"], "cached" if cached else "computed",
              flush=True)

    assert ordered_count == 19
    # These are unweighted sums over only the exceptional ordered blocks.
    assert support_sum == 253
    assert delta_sum == 21
    assert face_sum == 232
    assert support_sum - face_sum == delta_sum
    payload = {
        "format": "dth-gamma5-defect-support-integer-charts-v1",
        "last_names": list(last.LAST_NAMES),
        "ordered_blocks": ordered_count,
        "support_rank_sum": support_sum,
        "delta_rank_sum": delta_sum,
        "face_rank_sum": face_sum,
        "blocks": blocks,
    }
    encoded = json.dumps(payload, sort_keys=True,
                         separators=(",", ":")).encode("ascii")
    digest = hashlib.sha256(encoded).hexdigest()
    with open(args.output, "wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb",
                           compresslevel=9, mtime=0) as handle:
            handle.write(encoded)
    print("exact Gamma5 defect-support chart export passed")
    print("ordered support/delta/face sums:",
          support_sum, delta_sum, face_sum)
    print("uncompressed bytes:", len(encoded))
    print("payload sha256:", digest)
    print("saved:", args.output)


if __name__ == "__main__":
    main()
