#!/usr/bin/env python3
"""Select the 667-dimensional joint Gamma1/Gamma5 defect minor.

This is discovery code.  It keeps the previously certified 334 Gamma1
rows and source columns first, constructs the 339 canonical Gamma5
state-face equations in raw LAST highest-weight coordinates, and selects
333 rows and 333 new source columns in the quotient by the Gamma1 row
space.  The exact verifier reconstructs every selected row over a finite
field; no floating rank printed here is a theorem.

The 339 Gamma5 candidates are obtained blockwise as follows.  If E_pair and
E_face are the pair/Pluecker and D5-face restriction charts, choose a
generic face interpolation basis ell_q and pair pivot rows s.  In eighteen
codimension-one blocks this gives one times dim(pair) equations.  In the
(11,11,11) block it gives three times 43 equations.  Their intrinsic rank
is 336: the three skew internal/internal combinations vanish because the
source matrices are symmetric.  Three further directions lie in the
Gamma1 row space, leaving the expected incremental rank 333.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import pickle
from pathlib import Path
import sys

import numpy as np
import scipy.linalg as la


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import agent_dth_rational_reconstruction as rr


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = import_file(
    "dth_joint_gamma5_conventions",
    HERE / "agent_dth_gamma5_face_convention_audit.py",
)
EXACT5 = AUDIT.EXACT


EXPECTED_GAMMA1_RANK = 334
EXPECTED_GAMMA5_CANDIDATES = 339
EXPECTED_GAMMA5_RANK = 336
EXPECTED_OVERLAP = 3
EXPECTED_INCREMENT = 333
EXPECTED_JOINT_RANK = 667


def source_labels(codec):
    labels = []
    for block_index, (block, section) in enumerate(codec.blocks):
        rank = block["range"].shape[1]
        labels.extend((block_index, i, i) for i in range(rank))
        labels.extend((block_index, i, j)
                      for i in range(rank) for j in range(i + 1, rank))
        assert len(labels) == section.stop
    return labels


def normalize_rows(matrix):
    norms = la.norm(matrix, axis=1)
    assert np.min(norms) > 1e-13
    return matrix / norms[:, None]


def numerical_rank(matrix, relative=2e-9):
    singular = la.svdvals(matrix)
    rank = int(np.sum(singular > singular[0] * relative))
    return rank, singular


def block_diagonal(matrices):
    rows = sum(matrix.shape[0] for matrix in matrices)
    columns = sum(matrix.shape[1] for matrix in matrices)
    output = np.zeros((rows, columns))
    row = column = 0
    for matrix in matrices:
        r, c = matrix.shape
        output[row:row + r, column:column + c] = matrix
        row += r
        column += c
    return output


def raw_gamma5_crossing(cache_path, metadata_path):
    """Return raw-hol to raw-LAST crossing and local state transforms."""
    raw_hol_exact, raw_last_exact, _, _ = (
        EXACT5.LAST.exact_last_restriction_bridge()
    )
    raw_hol = np.asarray(raw_hol_exact, dtype=float)
    raw_last = np.asarray(raw_last_exact, dtype=float)
    raw_crossing = la.solve(raw_hol.T, raw_last.T).T
    metadata = np.load(metadata_path)
    normalized_hol = metadata["normalized_hol_restriction"]
    source_operator_change = la.solve(raw_hol.T, normalized_hol.T).T

    cache = np.load(cache_path)
    cache_local = cache["local"]
    cache_multiplicities = tuple(map(int, cache["mults"]))
    assert cache_multiplicities == tuple(reversed(EXACT5.LAST_MULTS))
    cache_ranges = AUDIT.coordinate_ranges(cache_multiplicities)
    archive_row_permutation = np.concatenate([
        item.reshape(-1) for item in reversed(cache_ranges)
    ])
    cache_last = cache_local[archive_row_permutation]
    # Derive the target coordinate change from the two independently built
    # crossings, then factor each local operator block as T tensor T.  This
    # avoids any ambiguity about QR transposes in the frozen cache.
    target_operator_change = la.solve(
        raw_crossing.T, (cache_last @ source_operator_change).T
    ).T
    raw_to_cache_last = []
    target_ranges = AUDIT.coordinate_ranges(EXACT5.LAST_MULTS)
    mask = np.zeros_like(target_operator_change, dtype=bool)
    for multiplicity, indices in zip(EXACT5.LAST_MULTS, target_ranges):
        flat = indices.reshape(-1)
        mask[np.ix_(flat, flat)] = True
        block = target_operator_change[np.ix_(flat, flat)]
        assert np.linalg.cond(block) < 1e5
        raw_to_cache_last.append(block)
    off_block = la.norm(target_operator_change[~mask])
    residual = la.norm(
        target_operator_change @ raw_crossing
        - cache_last @ source_operator_change,
        ord=2,
    )
    assert residual < 2e-10
    assert off_block < 2e-10
    transpose_source = np.concatenate([
        item.T.reshape(-1) for item in rr.block_ranges(rr.BRIDGE.HOL_MULTS)
    ])
    transpose_target = np.concatenate([
        item.T.reshape(-1) for item in target_ranges
    ])
    assert la.norm(
        raw_crossing[:, transpose_source]
        - raw_crossing[transpose_target, :]
    ) < 2e-9
    return raw_crossing, raw_to_cache_last, max(residual, off_block)


def raw_face_data(raw_to_cache_last, face_path, pair_path):
    """Build provisional raw charts and the 339 generic Gamma5 equations."""
    face = np.load(face_path)
    pair = np.load(pair_path)
    blocks = {}
    labels = []
    for archive_shapes in itertools.product(range(6), repeat=3):
        key = "".join(map(str, archive_shapes))
        internal_rank = pair[f"internal_{key}"].shape[1]
        if not internal_rank:
            continue
        exact_shapes = tuple(5 - shape for shape in archive_shapes)
        transforms_inverse = [la.inv(raw_to_cache_last[exact_shape])
                              for exact_shape in exact_shapes]
        dimensions = tuple(EXACT5.LAST_MULTS[s] for s in exact_shapes)

        def pull_range(normalized_range):
            positive = normalized_range @ normalized_range.T
            tensor = positive.reshape(
                dimensions[0], dimensions[1], dimensions[2],
                dimensions[0], dimensions[1], dimensions[2],
            ).transpose(0, 3, 1, 4, 2, 5).reshape(
                dimensions[0] ** 2, dimensions[1] ** 2,
                dimensions[2] ** 2,
            )
            raw_tensor = rr.mode3_apply(*transforms_inverse, tensor)
            raw_positive = raw_tensor.reshape(
                dimensions[0], dimensions[0],
                dimensions[1], dimensions[1],
                dimensions[2], dimensions[2],
            ).transpose(0, 2, 4, 1, 3, 5).reshape(positive.shape)
            raw_positive = (raw_positive + raw_positive.T) / 2
            values, vectors = la.eigh(raw_positive)
            rank = normalized_range.shape[1]
            if not rank:
                return np.zeros((positive.shape[0], 0))
            assert values[-rank] > 1e-10 * values[-1]
            return vectors[:, -rank:]

        pair_range = pull_range(pair[f"pair_{key}"])
        face_range = pull_range(face[f"range_{key}"])
        n, face_rank = face_range.shape
        support_rank = pair_range.shape[1]

        _, _, face_permutation = la.qr(
            face_range.T, mode="economic", pivoting=True
        )
        face_pivots = tuple(sorted(map(int, face_permutation[:face_rank])))
        principal = face_range[list(face_pivots), :]
        interpolation = face_range @ la.inv(principal)
        outside = tuple(row for row in range(n) if row not in face_pivots)
        left = np.eye(n)[list(outside)]
        left[:, list(face_pivots)] -= interpolation[list(outside), :]

        coupling = left @ pair_range
        _, triangular, q_permutation = la.qr(
            coupling.T, mode="economic", pivoting=True
        )
        diagonal = np.abs(np.diag(triangular))
        recovered_rank = int(np.sum(
            diagonal > (diagonal[0] if len(diagonal) else 1) * 2e-8
        ))
        assert recovered_rank == internal_rank, (
            exact_shapes, recovered_rank, internal_rank, diagonal
        )
        selected_q = tuple(outside[int(index)]
                           for index in q_permutation[:internal_rank])

        _, _, pair_permutation = la.qr(
            pair_range.T, mode="economic", pivoting=True
        )
        pair_pivots = tuple(sorted(map(
            int, pair_permutation[:support_rank]
        )))
        for q in selected_q:
            for s in pair_pivots:
                labels.append((exact_shapes, q, s))
        blocks[exact_shapes] = {
            "face_range": face_range,
            "face_pivots": face_pivots,
            "selected_q": selected_q,
            "pair_pivots": pair_pivots,
            "support_rank": support_rank,
            "internal_rank": internal_rank,
        }
    assert len(blocks) == 19
    assert len(labels) == EXPECTED_GAMMA5_CANDIDATES
    return blocks, labels


def functionals_for_block(block, labels):
    face_range = block["face_range"]
    pivots = block["face_pivots"]
    principal = face_range[list(pivots), :]
    interpolation = face_range @ la.inv(principal)
    n = face_range.shape[0]
    output = np.zeros((len(labels), n, n))
    for index, (_, q, s) in enumerate(labels):
        left = np.zeros(n)
        left[q] = 1
        left[list(pivots)] -= interpolation[q, :]
        output[index, :, s] = left
    return output


def matrix_batch_to_local_tensor(matrices, dimensions):
    count = matrices.shape[0]
    return matrices.reshape(
        count, dimensions[0], dimensions[1], dimensions[2],
        dimensions[0], dimensions[1], dimensions[2],
    ).transpose(1, 4, 2, 5, 3, 6, 0).reshape(
        dimensions[0] ** 2, dimensions[1] ** 2,
        dimensions[2] ** 2, count,
    )


def local_tensor_to_matrix_batch(tensor, dimensions):
    count = tensor.shape[-1]
    size = int(np.prod(dimensions))
    return tensor.reshape(
        dimensions[0], dimensions[0],
        dimensions[1], dimensions[1],
        dimensions[2], dimensions[2], count,
    ).transpose(6, 0, 2, 4, 1, 3, 5).reshape(count, size, size)


def mode3_apply_batch(first, second, third, tensor):
    output = np.tensordot(first, tensor, axes=(1, 0))
    output = np.tensordot(second, output, axes=(1, 1)).transpose(1, 0, 2, 3)
    return np.tensordot(third, output, axes=(1, 2)).transpose(1, 2, 0, 3)


def pullback_batch(target_shapes, functionals, crossing, blocks, codec,
                   hol_ranges, target_ranges):
    target_dimensions = tuple(EXACT5.LAST_MULTS[s] for s in target_shapes)
    target_tensor = matrix_batch_to_local_tensor(
        functionals, target_dimensions
    )
    rows = np.zeros((functionals.shape[0], codec.size))
    for source_block, section in codec.blocks:
        rank = source_block["range"].shape[1]
        if not rank:
            continue
        maps = [
            crossing[np.ix_(target_ranges[mu].reshape(-1),
                            hol_ranges[lam].reshape(-1))]
            for mu, lam in zip(target_shapes, source_block["shapes"])
        ]
        if any(la.norm(matrix) < 1e-13 for matrix in maps):
            continue
        pulled = mode3_apply_batch(
            maps[0].T, maps[1].T, maps[2].T, target_tensor
        )
        matrices = local_tensor_to_matrix_batch(
            pulled, source_block["dimensions"]
        )
        source_range = source_block["range"]
        compressed = np.einsum(
            "ia,qij,jb->qab", source_range, matrices, source_range,
            optimize=True,
        )
        values = [compressed[:, i, i] for i in range(rank)]
        values.extend(
            compressed[:, i, j] + compressed[:, j, i]
            for i in range(rank) for j in range(i + 1, rank)
        )
        rows[:, section] = np.stack(values, axis=1)
    return rows


def gamma5_rows(labels, face_blocks, crossing, blocks, codec):
    hol_ranges = rr.block_ranges(rr.BRIDGE.HOL_MULTS)
    target_ranges = rr.block_ranges(EXACT5.LAST_MULTS)
    output = np.zeros((len(labels), codec.size))
    offset = 0
    grouped = []
    for shapes in sorted(face_blocks):
        local_labels = [label for label in labels if label[0] == shapes]
        pieces = []
        # The (11)^3 block has 129 functionals on a 512-dimensional raw
        # space.  Materializing every 512-square functional and all of its
        # pullbacks at once creates a needless multi-hundred-MB peak.
        for start in range(0, len(local_labels), 12):
            batch_labels = local_labels[start:start + 12]
            functionals = functionals_for_block(
                face_blocks[shapes], batch_labels
            )
            pieces.append(pullback_batch(
                shapes, functionals, crossing, blocks, codec,
                hol_ranges, target_ranges,
            ))
        pulled = np.vstack(pieces)
        count = len(local_labels)
        output[offset:offset + count] = pulled
        grouped.extend(local_labels)
        offset += count
        print("Gamma5 pullback", "/".join(EXACT5.LAST.LAST_NAMES[s]
              for s in shapes), count, "rows", flush=True)
    assert offset == len(labels)
    return output, grouped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="/tmp/dth_exactK_source_float.pkl")
    parser.add_argument("--gamma1-rows",
                        default="/tmp/dth_defect_rows600_exactK.npz")
    parser.add_argument("--gamma1-pivots",
                        default="/tmp/dth_defect_pivots_exactK.npz")
    parser.add_argument("--gamma1-direct",
                        default="/tmp/dth_direct_defect_minor334.npz")
    parser.add_argument("--gamma5-cache",
                        default="/tmp/dth_gamma5_local_crossing_root.npz")
    parser.add_argument("--metadata",
                        default="/tmp/dth_obstruction_diagram_metadata.npz")
    parser.add_argument("--gamma5-face",
                        default="/tmp/dth_gamma5_feasible_face.npz")
    parser.add_argument("--gamma5-pair",
                        default="/tmp/dth_gamma5_pairplucker_rank21.npz")
    parser.add_argument("--rows-cache",
                        default="/tmp/dth_gamma5_generic_rows339.npz")
    parser.add_argument("--output",
                        default="/tmp/dth_joint_face_selection667.npz")
    args = parser.parse_args()

    with open(args.source, "rb") as handle:
        blocks, codec = pickle.load(handle)
    labels_all = source_labels(codec)
    assert codec.size == 4139

    crossing, transforms, crossing_residual = raw_gamma5_crossing(
        args.gamma5_cache, args.metadata
    )
    face_blocks, candidate_labels = raw_face_data(
        transforms, args.gamma5_face, args.gamma5_pair
    )
    candidate_labels = [
        label for shapes in sorted(face_blocks)
        for label in candidate_labels if label[0] == shapes
    ]
    if Path(args.rows_cache).exists():
        cached = np.load(args.rows_cache)
        gamma_rows = cached["rows"]
        grouped_labels = [
            (tuple(map(int, shapes)), int(q), int(s))
            for shapes, q, s in zip(cached["row_shapes"],
                                    cached["row_indices"],
                                    cached["column_indices"])
        ]
        assert grouped_labels == candidate_labels
        print("loaded Gamma5 pullback cache", args.rows_cache, flush=True)
    else:
        gamma_rows, grouped_labels = gamma5_rows(
            candidate_labels, face_blocks, crossing, blocks, codec
        )
        np.savez(
            args.rows_cache,
            rows=gamma_rows,
            row_shapes=np.asarray([label[0] for label in grouped_labels]),
            row_indices=np.asarray([label[1] for label in grouped_labels]),
            column_indices=np.asarray([label[2] for label in grouped_labels]),
            crossing_residual=np.array(crossing_residual),
        )
        print("saved Gamma5 pullback cache", args.rows_cache, flush=True)

    gamma_normalized = normalize_rows(gamma_rows)
    # Two exact directions are poorly scaled in the provisional raw chart
    # pulled back from the 1e-11-accurate frozen face (singular values around
    # 1e-9, followed by a clean drop to 1e-15).  Exact chart replay, not this
    # floating threshold, certifies them later.
    gamma_rank, gamma_singular = numerical_rank(
        gamma_normalized, relative=1e-11
    )
    assert gamma_rank == EXPECTED_GAMMA5_RANK, gamma_singular[330:340]

    g1_random = np.load(args.gamma1_rows)["rows"]
    g1_pivots = np.load(args.gamma1_pivots)
    g1_basis = normalize_rows(g1_random[g1_pivots["sketch_rows"]])
    old_columns = tuple(map(int, g1_pivots["source_columns"]))
    old_minor = g1_basis[:, old_columns]
    assert numerical_rank(g1_basis)[0] == EXPECTED_GAMMA1_RANK
    assert numerical_rank(old_minor, relative=2e-10)[0] == EXPECTED_GAMMA1_RANK

    coefficient = la.solve(old_minor.T,
                           gamma_normalized[:, old_columns].T).T
    quotient = gamma_normalized - coefficient @ g1_basis
    increment, quotient_singular = numerical_rank(quotient, relative=1e-11)
    assert increment == EXPECTED_INCREMENT, quotient_singular[328:338]
    overlap = gamma_rank - increment
    assert overlap == EXPECTED_OVERLAP

    _, _, row_permutation = la.qr(
        quotient.T, mode="economic", pivoting=True
    )
    selected_gamma = tuple(map(int, row_permutation[:increment]))
    selected_quotient = quotient[list(selected_gamma)]
    remaining = np.asarray([
        index for index in range(codec.size) if index not in set(old_columns)
    ], dtype=int)
    _, _, column_permutation = la.qr(
        selected_quotient[:, remaining], mode="economic", pivoting=True
    )
    new_columns = tuple(map(int, remaining[column_permutation[:increment]]))
    joint_columns = old_columns + new_columns
    selection_minor = np.vstack([
        g1_basis[:, joint_columns],
        gamma_normalized[list(selected_gamma)][:, joint_columns],
    ])
    joint_rank, joint_singular = numerical_rank(
        selection_minor, relative=2e-10
    )
    assert joint_rank == EXPECTED_JOINT_RANK, joint_singular[-10:]

    old = np.load(args.gamma1_direct)
    selected_labels = [grouped_labels[index] for index in selected_gamma]
    payload = {
        "cut": np.concatenate([
            np.zeros(EXPECTED_GAMMA1_RANK, dtype=int),
            np.ones(EXPECTED_INCREMENT, dtype=int),
        ]),
        "source_columns": np.asarray(joint_columns, dtype=int),
        "source_labels": np.asarray([labels_all[index]
                                     for index in joint_columns], dtype=int),
        "row_shapes": np.vstack([
            old["row_shapes"],
            np.asarray([label[0] for label in selected_labels], dtype=int),
        ]),
        "row_indices": np.concatenate([
            old["row_indices"],
            np.asarray([label[1] for label in selected_labels], dtype=int),
        ]),
        "column_indices": np.concatenate([
            old["column_indices"],
            np.asarray([label[2] for label in selected_labels], dtype=int),
        ]),
        "minor": selection_minor,
        "rank": np.array(joint_rank),
        "gamma5_candidate_count": np.array(len(grouped_labels)),
        "gamma5_candidate_rank": np.array(gamma_rank),
        "gamma5_incremental_rank": np.array(increment),
        "gamma1_gamma5_overlap": np.array(overlap),
        "crossing_residual": np.array(crossing_residual),
        "condition_number": np.array(np.linalg.cond(selection_minor)),
        "smallest_singular_value": np.array(joint_singular[-1]),
    }
    for key in old.files:
        if key.startswith("face_rows_"):
            payload["g1_" + key] = old[key]
    for shapes in sorted(set(label[0] for label in selected_labels)):
        tag = "".join(map(str, shapes))
        payload["g5_face_rows_" + tag] = np.asarray(
            face_blocks[shapes]["face_pivots"], dtype=int
        )
    np.savez(args.output, **payload)

    print("joint Gamma1/Gamma5 face selection passed", flush=True)
    print("Gamma5 candidates/rank/overlap/increment:",
          len(grouped_labels), gamma_rank, overlap, increment, flush=True)
    print("joint rank/condition/min singular:", joint_rank,
          np.linalg.cond(selection_minor), joint_singular[-1], flush=True)
    print("raw crossing reconstruction residual:", crossing_residual,
          flush=True)
    print("saved:", args.output, flush=True)


if __name__ == "__main__":
    main()
