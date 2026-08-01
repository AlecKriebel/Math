#!/usr/bin/env python3
"""Select a well-conditioned direct 334 by 334 DTH defect minor.

The input source columns come from the randomized rank audit, but every row
selected here is a literal pivot-row face-membership equation

    (e_i^T - E_i E_J^{-1} e_J^T) M e_j = 0.

Consequently the saved row labels can be replayed over a finite field or QQ
using the exact K and product-face charts.  This remains discovery code: the
floating minor is used only to select exact row/column labels.
"""

from __future__ import annotations

import argparse
import itertools
import pickle
import sys

import numpy as np
import scipy.linalg as la

sys.path.insert(0, "discovery")
import agent_dth_rational_reconstruction as rr


def source_labels(codec):
    labels = []
    for block_index, (block, section) in enumerate(codec.blocks):
        k = block["range"].shape[1]
        labels.extend((block_index, i, i) for i in range(k))
        labels.extend(
            (block_index, i, j)
            for i in range(k) for j in range(i + 1, k)
        )
        assert len(labels) == section.stop
    return labels


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


def crossed_source_matrix(source_label, mixed_shapes, blocks, crossing,
                          hol_ranges, mixed_ranges):
    block_index, i, j = source_label
    block = blocks[block_index]
    e = block["range"]
    matrix = np.outer(e[:, i], e[:, j])
    if i != j:
        matrix += np.outer(e[:, j], e[:, i])
    tensor = matrix_to_local_tensor(matrix, block["dimensions"])
    maps = [
        crossing[np.ix_(mixed_ranges[mu].reshape(-1),
                        hol_ranges[lam].reshape(-1))]
        for mu, lam in zip(mixed_shapes, block["shapes"])
    ]
    crossed = rr.mode3_apply(*maps, tensor)
    dimensions = tuple(rr.BRIDGE.MIXED_MULTS[s] for s in mixed_shapes)
    return local_tensor_to_matrix(crossed, dimensions)


def face_residual_map(face):
    n, rank = face.shape
    if not rank:
        rows = tuple()
        return np.zeros((n, 0)), rows, tuple(range(n))
    _, _, pivots = la.qr(face.T, mode="economic", pivoting=True)
    rows = tuple(sorted(int(x) for x in pivots[:rank]))
    principal = face[list(rows), :]
    interpolation = face @ la.inv(principal)
    outside = tuple(i for i in range(n) if i not in rows)
    assert la.norm(interpolation[list(rows), :] - np.eye(rank)) < 2e-7
    return interpolation, rows, outside


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="/tmp/dth_exactK_source_float.pkl")
    parser.add_argument("--random-rows", default="/tmp/dth_defect_rows600_exactK.npz")
    parser.add_argument("--pivots", default="/tmp/dth_defect_pivots_exactK.npz")
    parser.add_argument("--face", default="/tmp/dth_product_face_bases.npz")
    parser.add_argument("--output", default="/tmp/dth_direct_defect_minor334.npz")
    args = parser.parse_args()

    with open(args.source, "rb") as handle:
        blocks, codec = pickle.load(handle)
    labels = source_labels(codec)
    pivot_data = np.load(args.pivots)
    source_columns = pivot_data["source_columns"].astype(int)
    chosen_source_labels = [labels[index] for index in source_columns]

    random_data = np.load(args.random_rows)
    sketch_shapes = random_data["labels"][pivot_data["sketch_rows"]]
    relevant_shapes = sorted(set(tuple(map(int, row)) for row in sketch_shapes))
    print("relevant mixed blocks:", len(relevant_shapes), flush=True)

    crossing, hol_ranges, mixed_ranges, _, raw_mixed, _, _ = rr.raw_crossing_data()
    face_blocks = rr.raw_mixed_face_bases(raw_mixed, args.face)

    candidate_rows = []
    candidate_labels = []
    face_pivot_rows = {}
    for count, shapes in enumerate(relevant_shapes, 1):
        face = face_blocks[shapes]
        interpolation, pivots, outside = face_residual_map(face)
        face_pivot_rows[shapes] = pivots
        n = face.shape[0]
        images = np.empty((n, n, len(source_columns)))
        for column, label in enumerate(chosen_source_labels):
            images[:, :, column] = crossed_source_matrix(
                label, shapes, blocks, crossing, hol_ranges, mixed_ranges
            )
        residual = images[list(outside), :, :] - np.einsum(
            "ir,rjc->ijc", interpolation[list(outside), :],
            images[list(pivots), :, :], optimize=True
        )
        residual = residual.reshape(-1, len(source_columns))
        # Keep at most 334 independent representatives from this block.
        _, r, row_pivots = la.qr(residual.T, mode="economic", pivoting=True)
        diagonal = np.abs(np.diag(r))
        local_rank = int(np.sum(diagonal > (diagonal[0] if len(diagonal) else 1)
                                           * 1e-10))
        for flat in row_pivots[:local_rank]:
            oi, column = divmod(int(flat), n)
            candidate_rows.append(residual[flat])
            candidate_labels.append((shapes, outside[oi], column))
        print(count, "/", len(relevant_shapes), shapes,
              "candidate rank", local_rank, flush=True)

    candidate_rows = np.asarray(candidate_rows)
    _, r, pivots = la.qr(candidate_rows.T, mode="economic", pivoting=True)
    diagonal = np.abs(np.diag(r))
    rank = int(np.sum(diagonal > diagonal[0] * 1e-9))
    assert rank == 334, (rank, diagonal[333:336])
    selected = np.asarray(pivots[:rank], dtype=int)
    minor = candidate_rows[selected]
    print("direct minor condition number:", np.linalg.cond(minor), flush=True)

    selected_labels = [candidate_labels[index] for index in selected]
    np.savez(
        args.output,
        source_columns=source_columns,
        source_labels=np.asarray(chosen_source_labels, dtype=int),
        row_shapes=np.asarray([label[0] for label in selected_labels], dtype=int),
        row_indices=np.asarray([label[1] for label in selected_labels], dtype=int),
        column_indices=np.asarray([label[2] for label in selected_labels], dtype=int),
        minor=minor,
        relevant_shapes=np.asarray(relevant_shapes, dtype=int),
        **{
            "face_rows_" + "".join(map(str, shapes)): np.asarray(rows, dtype=int)
            for shapes, rows in face_pivot_rows.items()
        },
    )
    print("wrote", args.output)


if __name__ == "__main__":
    main()
