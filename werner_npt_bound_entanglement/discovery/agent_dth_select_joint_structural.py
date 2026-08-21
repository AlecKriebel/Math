#!/usr/bin/env python3
"""Well-conditioned structural selector for the joint 667 defect space.

This companion uses exact integer pair/Pluecker support charts and the raw
double-Hodge Gram to construct an orthonormal numerical basis of the D5
state-face quotient.  It selects the 333 new source columns before the
structural rows are translated to generic exact E5 interpolation rows.
All claims remain discovery-only until the final generic labels are replayed
modulo primes.
"""

from __future__ import annotations

import argparse
import gzip
import importlib.util
import json
import pickle
from pathlib import Path
import sys

import numpy as np
import scipy.linalg as la


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


JOINT = import_file(
    "dth_joint_structural_base", HERE / "agent_dth_select_joint_face_minor.py"
)


def read_support(path):
    with gzip.open(path, "rt", encoding="ascii") as handle:
        payload = json.load(handle)
    assert payload["format"] == "dth-gamma5-defect-support-integer-charts-v1"
    assert payload["support_rank_sum"] == 253
    assert payload["delta_rank_sum"] == 21
    assert payload["face_rank_sum"] == 232
    return payload


def raw_local_data():
    deltas = [
        tuple(np.asarray(JOINT.EXACT5.local_delta(shape, which), dtype=float)
              for which in (0, 2))
        for shape in range(6)
    ]
    grams = [
        np.asarray(JOINT.EXACT5.local_gram(shape), dtype=float)
        for shape in range(6)
    ]
    return deltas, grams


def block_structural_data(shapes, block, deltas, grams):
    pair = np.asarray(block["matrix"], dtype=float)
    support_rank = int(block["support_rank"])
    defect_rank = int(block["delta_rank"])
    assert pair.shape[1] == support_rank
    pair_orthonormal, _ = la.qr(pair, mode="economic")
    gram = np.kron(np.kron(grams[shapes[0]], grams[shapes[1]]),
                   grams[shapes[2]])
    delta_gram = JOINT.AUDIT.delta_gram(shapes, deltas)
    coefficient = la.solve(gram, pair_orthonormal, assume_a="pos")
    left_raw = coefficient.T @ delta_gram
    left_raw = la.solve(gram.T, left_raw.T, assume_a="pos").T
    _, singular, vh = la.svd(left_raw, full_matrices=False)
    recovered = int(np.sum(singular > singular[0] * 1e-9))
    assert recovered == defect_rank, (shapes, singular)
    left = vh[:defect_rank]
    assert la.norm(left @ pair_orthonormal) > 1e-8
    labels = [(shapes, i, j)
              for i in range(defect_rank) for j in range(support_rank)]
    return left, pair_orthonormal, labels, singular


def pull_structural_rows(shapes, left, right, labels, crossing,
                         blocks, codec, batch_size):
    rows = []
    for start in range(0, len(labels), batch_size):
        batch = labels[start:start + batch_size]
        matrices = np.asarray([
            np.outer(left[i], right[:, j]) for _, i, j in batch
        ])
        pulled = JOINT.pullback_batch(
            shapes, matrices, crossing, blocks, codec,
            JOINT.rr.block_ranges(JOINT.rr.BRIDGE.HOL_MULTS),
            JOINT.rr.block_ranges(JOINT.EXACT5.LAST_MULTS),
        )
        rows.append(pulled)
    return np.vstack(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--support", required=True)
    parser.add_argument("--source", default="/tmp/dth_exactK_source_float.pkl")
    parser.add_argument("--gamma1-rows",
                        default="/tmp/dth_defect_rows600_exactK.npz")
    parser.add_argument("--gamma1-pivots",
                        default="/tmp/dth_defect_pivots_exactK.npz")
    parser.add_argument("--gamma5-cache",
                        default="/tmp/dth_gamma5_local_crossing_root.npz")
    parser.add_argument("--metadata",
                        default="/tmp/dth_obstruction_diagram_metadata.npz")
    parser.add_argument("--rows-cache",
                        default="/tmp/dth_gamma5_structural_rows339.npz")
    parser.add_argument("--output",
                        default="/tmp/dth_joint_structural_selection667.npz")
    parser.add_argument("--batch-size", type=int, default=12)
    args = parser.parse_args()

    support = read_support(args.support)
    with open(args.source, "rb") as handle:
        blocks, codec = pickle.load(handle)
    all_source_labels = JOINT.source_labels(codec)
    crossing, _, crossing_residual = JOINT.raw_gamma5_crossing(
        args.gamma5_cache, args.metadata
    )
    deltas, grams = raw_local_data()

    structural_labels = []
    structural_rows = []
    singular_audit = []
    if Path(args.rows_cache).exists():
        cache = np.load(args.rows_cache)
        structural_rows = cache["rows"]
        structural_labels = [
            (tuple(map(int, shapes)), int(i), int(j))
            for shapes, i, j in zip(cache["row_shapes"],
                                    cache["left_indices"],
                                    cache["right_indices"])
        ]
        print("loaded structural row cache", args.rows_cache, flush=True)
    else:
        for key in sorted(support["blocks"]):
            shapes = tuple(map(int, key.split(",")))
            block = support["blocks"][key]
            left, right, labels, singular = block_structural_data(
                shapes, block, deltas, grams
            )
            pulled = pull_structural_rows(
                shapes, left, right, labels, crossing, blocks, codec,
                args.batch_size,
            )
            structural_rows.append(pulled)
            structural_labels.extend(labels)
            singular_audit.append((shapes, singular[-1]))
            print("structural pullback", key, len(labels), "rows", flush=True)
        structural_rows = np.vstack(structural_rows)
        np.savez(
            args.rows_cache,
            rows=structural_rows,
            row_shapes=np.asarray([label[0] for label in structural_labels]),
            left_indices=np.asarray([label[1] for label in structural_labels]),
            right_indices=np.asarray([label[2] for label in structural_labels]),
            crossing_residual=np.array(crossing_residual),
        )
        print("saved structural row cache", args.rows_cache, flush=True)

    assert structural_rows.shape == (339, 4139)
    normalized = JOINT.normalize_rows(structural_rows)
    structural_rank, structural_singular = JOINT.numerical_rank(
        normalized, relative=1e-10
    )
    # The abstract symmetric pair-support operator loss is 336, but two of
    # those functionals vanish already on the exact holomorphic source
    # support.  The pulled-back Gamma5 defect therefore has rank 334; the
    # gap is clean (about 1e-2 to 1e-15) and is replayed exactly later.
    assert structural_rank == 334, structural_singular[328:]

    gamma1_rows = np.load(args.gamma1_rows)["rows"]
    gamma1_pivots = np.load(args.gamma1_pivots)
    gamma1 = JOINT.normalize_rows(
        gamma1_rows[gamma1_pivots["sketch_rows"]]
    )
    old_columns = tuple(map(int, gamma1_pivots["source_columns"]))
    old_minor = gamma1[:, old_columns]
    coefficients = la.solve(
        old_minor.T, normalized[:, old_columns].T
    ).T
    quotient = normalized - coefficients @ gamma1
    increment, quotient_singular = JOINT.numerical_rank(
        quotient, relative=1e-9
    )
    assert increment == 333, quotient_singular[328:]

    _, _, row_permutation = la.qr(
        quotient.T, mode="economic", pivoting=True
    )
    selected_rows = tuple(map(int, row_permutation[:increment]))
    selected_quotient = quotient[list(selected_rows)]
    old_set = set(old_columns)
    remaining = np.asarray([i for i in range(codec.size) if i not in old_set])
    _, _, column_permutation = la.qr(
        selected_quotient[:, remaining], mode="economic", pivoting=True
    )
    new_columns = tuple(map(int, remaining[column_permutation[:increment]]))
    joint_columns = old_columns + new_columns
    selection_minor = np.vstack([
        gamma1[:, joint_columns],
        normalized[list(selected_rows)][:, joint_columns],
    ])
    joint_rank, joint_singular = JOINT.numerical_rank(
        selection_minor, relative=1e-10
    )
    assert joint_rank == 667, joint_singular[-10:]

    chosen = [structural_labels[index] for index in selected_rows]
    np.savez(
        args.output,
        source_columns=np.asarray(joint_columns),
        source_labels=np.asarray([all_source_labels[index]
                                  for index in joint_columns]),
        structural_row_shapes=np.asarray([label[0] for label in chosen]),
        structural_left_indices=np.asarray([label[1] for label in chosen]),
        structural_right_indices=np.asarray([label[2] for label in chosen]),
        selected_structural_rows=np.asarray(selected_rows),
        minor=selection_minor,
        structural_candidate_count=np.array(339),
        structural_rank=np.array(structural_rank),
        incremental_rank=np.array(increment),
        overlap=np.array(structural_rank - increment),
        joint_rank=np.array(joint_rank),
        condition_number=np.array(np.linalg.cond(selection_minor)),
        minimum_singular=np.array(joint_singular[-1]),
        crossing_residual=np.array(crossing_residual),
    )
    print("joint structural selector passed", flush=True)
    print("candidate/rank/overlap/increment:",
          339, structural_rank, structural_rank - increment, increment,
          flush=True)
    print("joint rank/condition/min singular:", joint_rank,
          np.linalg.cond(selection_minor), joint_singular[-1], flush=True)
    print("saved:", args.output, flush=True)


if __name__ == "__main__":
    main()
