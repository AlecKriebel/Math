#!/usr/bin/env python3
"""Build exact dense checkpoints for two slow 00-containing Gamma5 blocks.

The sparse raw-word route is inefficient for ``(11,11,00)`` and
``(11,00,00)`` because each local ``00`` highest-weight vector has eighteen
terms.  Their multiplicity blocks have sizes only 192 and 72.  This helper
uses the independent exact dense representation construction to write the
same checkpoint schema consumed by the sparse face exporter.
"""

from fractions import Fraction
from pathlib import Path
import argparse
import sys

sys.path.insert(0, "verification")
import agent_dth_exact_gamma5_face_coordinates as dense
import agent_dth_gamma5_face_sparse_export as sparse


SHAPES = ((3, 3, 5), (3, 5, 5))


def fraction_matrix(matrix):
    return [
        [Fraction(int(value.p), int(value.q)) for value in matrix.row(row)]
        for row in range(matrix.rows)
    ]


def dense_block(shapes):
    support = dense.pair_pluecker_coordinates(shapes)
    physical, gram, restriction = dense.gamma5_face_coordinates(shapes)
    support_restriction = gram * support
    assert support.rank() == support.cols
    assert physical.rank() == physical.cols
    assert dense.delta_gram(shapes) * physical == dense.sp.zeros(
        physical.rows, physical.cols
    )
    d0 = dense.kron3(tuple(dense.local_delta(shape, 0)
                           for shape in shapes))
    d2 = dense.kron3(tuple(dense.local_delta(shape, 2)
                           for shape in shapes))
    assert (d0 - d2) * support == dense.sp.zeros(d0.rows, support.cols)
    assert (d0 + d2) * physical == dense.sp.zeros(d0.rows, physical.cols)
    assert restriction == gram * physical

    face_matrix = sparse.primitive_integer_columns(
        fraction_matrix(restriction)
    )
    support_matrix = sparse.primitive_integer_columns(
        fraction_matrix(support_restriction)
    )
    return {
        "raw_rank": support.rows,
        "support_rank": support.cols,
        "delta_rank": support.cols - physical.cols,
        "face_rank": physical.cols,
        "matrix": face_matrix,
        "pivot_rows": sparse.pivot_rows(face_matrix),
        "support_matrix": support_matrix,
        "support_pivot_rows": sparse.pivot_rows(support_matrix),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-dir", required=True)
    args = parser.parse_args()
    directory = Path(args.checkpoint_dir)
    for shapes in SHAPES:
        block = dense_block(shapes)
        assert block["delta_rank"] == 1
        sparse.save_checkpoint(directory, shapes, block)
        replay = sparse.load_checkpoint(directory, shapes,
                                        require_support=True)
        assert replay == block
        print("exact dense Gamma5 tail checkpoint", shapes,
              "raw/support/delta/face",
              block["raw_rank"], block["support_rank"],
              block["delta_rank"], block["face_rank"])


if __name__ == "__main__":
    main()
