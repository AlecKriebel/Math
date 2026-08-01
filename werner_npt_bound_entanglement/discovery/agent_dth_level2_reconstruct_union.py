#!/usr/bin/env python3
"""Reconstruct the discarded degree-three source union bases.

The complete fixed-marginal cache retains, for every post-Omega S7 block,
all source-to-target matrices ``M_j = U.T @ V_j`` but discards the raw
orthonormal union basis ``U``.  Here ``V_j`` are the projected branch images.
Because the concatenated ``M`` has full row rank and every ``V_j`` lies in
the union, the original oriented basis is recovered losslessly (up to the
floating-point data already in the discovery cache) by

    U = V M.T (M M.T)^(-1).

This module rebuilds one block at a time and therefore does not retain the
roughly 1.17 GB collection of all raw bases.  It is intended as the source
side of the matrix-free Gamma_A crossing/Lanczos test.

This is numerical discovery infrastructure.  Exact reconstruction uses the
rational seed-Gram architecture in the verification notes.
"""

from argparse import ArgumentParser
from pathlib import Path
import pickle
import sys

import numpy as np
import scipy.linalg as la


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "discovery"
sys.path.insert(0, str(DISCOVERY))

import agent_dth_level2_joint_extension as ENGINE


DEFAULT_CACHE = DISCOVERY / "dth_level2_full_blocks.pkl"


def deterministic_omega_range(source, raw_dimension, expected_rank):
    """An orientation-independent basis of im(P Q P), with local RNG."""
    if expected_rank == 0:
        return np.zeros((raw_dimension, 0))
    seed = sum((index + 11) * (site + 17) ** 3
               for site, index in enumerate(source))
    generator = np.random.default_rng(seed)
    trial = generator.standard_normal((raw_dimension, expected_rank + 7))
    trial = ENGINE.BASE.source_project(trial, source)
    trial = ENGINE.BASE.omega_gram_action(trial, source)
    trial = ENGINE.BASE.source_project(trial, source)
    basis, values = ENGINE.BASE.orthonormal_columns(trial, tolerance=2e-10)
    assert basis.shape[1] == expected_rank, (
        source, basis.shape, expected_rank, values
    )
    return basis


def raw_projected_columns(block, target_data):
    """Rebuild the concatenated raw branch matrix V in cache order."""
    source = tuple(block["source"])
    raw_columns = []
    cached_columns = []
    layout = []
    for target in ENGINE.TARGETS:
        if target not in block["maps"]:
            continue
        embeddings = ENGINE.target_embeddings(
            source, target, target_data[target][0]
        )
        cached = block["maps"][target]
        assert len(embeddings) == len(cached), (
            source, target, len(embeddings), len(cached)
        )
        for channel, (embedding, matrix) in enumerate(zip(embeddings, cached)):
            assert embedding.shape[1] == matrix.shape[1]
            layout.append((target, channel, embedding.shape[1]))
            raw_columns.append(embedding)
            cached_columns.append(matrix)
    assert raw_columns
    raw = np.hstack(raw_columns)
    cached = np.hstack(cached_columns)
    projected = ENGINE.BASE.source_project(raw, source)
    omega = deterministic_omega_range(
        source, projected.shape[0], block["omega_rank"]
    )
    projected -= omega @ (omega.T @ projected)
    return projected, cached, tuple(layout)


def reconstruct_union(block, target_data, audit=True):
    """Recover the original oriented raw union basis for one cache block."""
    projected, cached, layout = raw_projected_columns(block, target_data)
    dimension = block["dimension"]
    assert cached.shape[0] == dimension
    gram = cached @ cached.T
    spectrum = la.eigvalsh((gram + gram.T) / 2.0)
    assert spectrum[0] > 2e-12 * spectrum[-1], (
        block["source"], spectrum[0], spectrum[-1]
    )
    numerator = projected @ cached.T
    union = la.solve(gram, numerator.T, assume_a="pos").T
    if audit:
        scale = max(1.0, la.norm(projected), la.norm(cached))
        column_error = la.norm(union @ cached - projected) / scale
        coordinate_error = la.norm(union.T @ projected - cached) / scale
        isometry_error = la.norm(
            union.T @ union - np.eye(dimension)
        )
        source_error = la.norm(
            ENGINE.BASE.source_project(union, tuple(block["source"])) - union
        ) / max(1.0, la.norm(union))
        omega_error = la.norm(
            ENGINE.BASE.omega_gram_action(union, tuple(block["source"]))
        ) / max(1.0, la.norm(union))
        assert column_error < 3e-7, (block["source"], column_error)
        assert coordinate_error < 3e-7, (block["source"], coordinate_error)
        assert isometry_error < 4e-6, (block["source"], isometry_error)
        assert source_error < 3e-7, (block["source"], source_error)
        assert omega_error < 3e-7, (block["source"], omega_error)
        metrics = {
            "column_error": column_error,
            "coordinate_error": coordinate_error,
            "isometry_error": isometry_error,
            "source_error": source_error,
            "omega_error": omega_error,
            "gram_min": spectrum[0],
            "gram_max": spectrum[-1],
        }
    else:
        metrics = None
    return union, layout, metrics


def load_cache(path=DEFAULT_CACHE):
    with Path(path).open("rb") as stream:
        data = pickle.load(stream)
    ENGINE.TARGETS = tuple(data["targets"])
    return data


def find_block(data, source):
    source = tuple(source)
    return next(
        block for block in data["blocks"]
        if tuple(block["source"]) == source
    )


def main():
    parser = ArgumentParser()
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument(
        "--source", type=int, nargs=3, default=(0, 0, 4),
        metavar=("L1", "L2", "L3"),
    )
    args = parser.parse_args()
    data = load_cache(args.cache)
    block = find_block(data, args.source)
    union, layout, metrics = reconstruct_union(
        block, data["target_data"], audit=True
    )
    print("reconstructed source:", tuple(block["source"]))
    print("raw/reduced dimensions:", union.shape)
    print("branch groups/columns:", len(layout), sum(item[2] for item in layout))
    print("audit:", metrics)


if __name__ == "__main__":
    main()
