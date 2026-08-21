#!/usr/bin/env python3
"""Cross a saved degree-three DTH source through Gamma_A block by block.

The fixed-marginal cache intentionally discarded the large post-Omega source
bases.  This script reconstructs each basis, aligns it to the cached source
coordinates through the collectively full-rank marginal Kraus frames, and
then applies the tensor product of the audited local S7 crossing maps.

The first pass materializes only mixed blocks below a requested multiplicity
dimension.  This ranks active negative sectors before a matrix-free two-cone
solver is built.  All output is floating-point discovery evidence.
"""

from argparse import ArgumentParser
from itertools import product
from pathlib import Path
import pickle
import sys


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "discovery"
sys.path.insert(0, str(DISCOVERY))

import numpy as np
import scipy.linalg as la

import agent_dth_level2_444_extension as YOUNG
import agent_dth_level2_joint_extension as JOINT
import agent_dth_level2_reconstruct_union as RECONSTRUCT
import agent_dth_level2_source_symmetry as SOURCE_SYMMETRY


DEFAULT_BLOCKS = DISCOVERY / "dth_level2_full_blocks.pkl"
DEFAULT_CANDIDATE = (
    DISCOVERY / "dth_level2_source_reduced_floor1e12_warm.pkl"
)
DEFAULT_CROSSING = DISCOVERY / "dth_level2_local_gammaA_crossing.npz"
DEFAULT_OUTPUT = DISCOVERY / "dth_level2_crossed_small_blocks.pkl"


def reconstruct_source_basis(source, target_data):
    """Rebuild one post-Omega source basis and its marginal Kraus frames."""
    raw_by_target = {}
    raw_dimension = None
    for target in JOINT.TARGETS:
        embeddings = JOINT.target_embeddings(
            source, target, target_data[target][0]
        )
        if embeddings:
            raw_by_target[target] = embeddings
            raw_dimension = embeddings[0].shape[0]
    assert raw_by_target and raw_dimension is not None

    qomega = JOINT.omega_range(
        source, raw_dimension, JOINT.omega_output_rank(source)
    )
    layout = []
    raw_columns = []
    cursor = 0
    for target, embeddings in raw_by_target.items():
        for embedding in embeddings:
            width = embedding.shape[1]
            layout.append((target, cursor, cursor + width))
            raw_columns.append(embedding)
            cursor += width
    all_vectors = YOUNG.source_project(np.hstack(raw_columns), source)
    all_vectors -= qomega @ (qomega.T @ all_vectors)
    projected = {target: [] for target in raw_by_target}
    for target, start, stop in layout:
        projected[target].append(all_vectors[:, start:stop])
    union, values = YOUNG.orthonormal_columns(all_vectors, tolerance=3e-9)
    maps = {
        target: [union.T @ vector for vector in vectors]
        for target, vectors in projected.items()
    }
    return union, maps, values


def align_cached_basis(cached_maps, rebuilt_maps):
    """Return O with rebuilt_map = O cached_map for every Kraus frame."""
    cached = []
    rebuilt = []
    for target in sorted(cached_maps):
        assert len(cached_maps[target]) == len(rebuilt_maps[target])
        cached.extend(cached_maps[target])
        rebuilt.extend(rebuilt_maps[target])
    cached = np.hstack(cached)
    rebuilt = np.hstack(rebuilt)
    gram = cached @ cached.T
    transform = la.solve(
        gram, cached @ rebuilt.T, assume_a="sym"
    ).T
    left, _, right = la.svd(transform)
    transform = left @ right
    relative = la.norm(transform @ cached - rebuilt) / max(
        1.0, la.norm(rebuilt)
    )
    orthogonal = la.norm(
        transform.T @ transform - np.eye(transform.shape[0])
    )
    assert relative < 5e-7, relative
    assert orthogonal < 5e-10, orthogonal
    return transform, relative


def local_blocks(crossing):
    matrix = crossing["crossing"]
    holomorphic = tuple(map(int, crossing["hol_multiplicities"]))
    mixed = tuple(map(int, crossing["mixed_multiplicities"]))
    carriers = tuple(map(int, crossing["hol_carrier_dimensions"]))
    row_offsets = np.cumsum((0,) + tuple(value * value for value in mixed))
    column_offsets = np.cumsum(
        (0,) + tuple(value * value for value in holomorphic)
    )
    output = {}
    for mu, multiplicity in enumerate(mixed):
        for lam, source_multiplicity in enumerate(holomorphic):
            raw = matrix[
                row_offsets[mu]:row_offsets[mu + 1],
                column_offsets[lam]:column_offsets[lam + 1],
            ]
            if la.norm(raw) < 1e-12:
                continue
            # The cached source density is the raw multiplicity block
            # I_carrier tensor X, whereas the crossing columns are normalized
            # trace-one units I_carrier tensor E_ab / carrier.
            output[(mu, lam)] = (
                carriers[lam] * raw
            ).reshape(
                multiplicity, multiplicity,
                source_multiplicity, source_multiplicity,
            )
    return output, holomorphic, mixed


def crossed_contribution(local, source_factor, mu, source):
    first = local[(mu[0], source[0])]
    second = local[(mu[1], source[1])]
    third = local[(mu[2], source[2])]
    tensor = np.einsum(
        "pqad,rsbe,tucf,abck,defk->prtqsu",
        first, second, third, source_factor, source_factor,
        optimize="greedy",
    )
    dimension = first.shape[0] * second.shape[0] * third.shape[0]
    return tensor.reshape(dimension, dimension)


def main():
    parser = ArgumentParser()
    parser.add_argument("--blocks", type=Path, default=DEFAULT_BLOCKS)
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--crossing", type=Path, default=DEFAULT_CROSSING)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-mixed-dimension", type=int, default=25)
    parser.add_argument("--limit-sources", type=int, default=None)
    parser.add_argument("--report", type=int, default=10)
    args = parser.parse_args()

    with args.blocks.open("rb") as stream:
        data = pickle.load(stream)
    JOINT.TARGETS = tuple(data["targets"])
    reduction = SOURCE_SYMMETRY.build_reduction(
        data["blocks"], data["target_data"], audit=False, compile_maps=False
    )
    with args.candidate.open("rb") as stream:
        candidate = pickle.load(stream)
    shift = SOURCE_SYMMETRY.physical_floor_shift(
        reduction, candidate["floor"]
    )
    physical_components = [
        value + delta for value, delta in zip(
            candidate["shifted_components"], shift
        )
    ]
    ordered = SOURCE_SYMMETRY.expand(reduction, physical_components)

    crossing = np.load(args.crossing)
    local, holomorphic_multiplicities, mixed_multiplicities = local_blocks(
        crossing
    )
    selected = tuple(
        triple for triple in product(range(len(mixed_multiplicities)), repeat=3)
        if np.prod([mixed_multiplicities[index] for index in triple])
        <= args.max_mixed_dimension
    )
    output = {
        triple: np.zeros((
            int(np.prod([mixed_multiplicities[index] for index in triple])),
        ) * 2)
        for triple in selected
    }
    print("selected mixed blocks:", len(selected))

    maximum_alignment_error = 0.0
    source_count = len(data["blocks"])
    if args.limit_sources is not None:
        source_count = min(source_count, args.limit_sources)
    for block_index, (block, source_matrix) in enumerate(
        zip(data["blocks"][:source_count], ordered[:source_count]), 1
    ):
        source = tuple(block["source"])
        compatible = [
            mu for mu in selected
            if all((mu[site], source[site]) in local for site in range(3))
        ]
        if not compatible:
            if block_index % args.report == 0 or block_index == source_count:
                print(
                    "skipped sources", block_index, "/", source_count,
                    "source", source, "compatible", 0, flush=True,
                )
            continue
        union, _, reconstruction_metrics = RECONSTRUCT.reconstruct_union(
            block, data["target_data"], audit=False
        )
        alignment_error = (
            0.0 if reconstruction_metrics is None
            else reconstruction_metrics["coordinate_error"]
        )
        maximum_alignment_error = max(
            maximum_alignment_error, alignment_error
        )
        eigenvalues, eigenvectors = la.eigh(
            (source_matrix + source_matrix.T) / 2.0
        )
        assert eigenvalues[0] > -2e-16
        coefficient_factor = (
            eigenvectors * np.sqrt(np.maximum(eigenvalues, 0.0))
        )
        raw_factor = union @ coefficient_factor
        shapes = tuple(
            holomorphic_multiplicities[index] for index in source
        )
        raw_factor = raw_factor.reshape(*shapes, raw_factor.shape[1])

        for mu in compatible:
            output[mu] += crossed_contribution(
                local, raw_factor, mu, source
            )
        if block_index % args.report == 0 or block_index == source_count:
            print(
                "crossed sources", block_index, "/", source_count,
                "source", source, "raw/rank", union.shape,
                "compatible", len(compatible),
                "alignment", alignment_error,
                flush=True,
            )

    rows = []
    for triple, matrix in output.items():
        matrix = (matrix + matrix.T) / 2.0
        values = la.eigvalsh(matrix)
        trace = float(np.trace(matrix))
        negative = float(np.sqrt(np.sum(np.minimum(values, 0.0) ** 2)))
        quotient = float(values[0] / max(abs(trace), 1e-300))
        rows.append((
            quotient, triple, matrix.shape[0], values[0], values[-1],
            trace, negative,
        ))
        output[triple] = matrix
    rows.sort()
    print("maximum alignment error:", maximum_alignment_error)
    print("thirty least crossed blocks:")
    for row in rows[:30]:
        print(" ", row)
    with args.output.open("wb") as stream:
        pickle.dump({
            "max_mixed_dimension": args.max_mixed_dimension,
            "source_count": source_count,
            "maximum_alignment_error": maximum_alignment_error,
            "spectral_rows": rows,
            "blocks": output,
        }, stream, pickle.HIGHEST_PROTOCOL)
    print("saved:", args.output)


if __name__ == "__main__":
    main()
