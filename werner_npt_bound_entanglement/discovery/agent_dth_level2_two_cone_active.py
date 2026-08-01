#!/usr/bin/env python3
"""Active-cut solver for the degree-three DTH PSD/Gamma_A cones.

The expensive Gamma_A cone is sampled by eigenvector cuts obtained from an
orbit-streamed crossing cache.  This driver resumes an earlier cut set,
pulls any newly negative eigenvectors back in one pass through the 112 source
orbits, and applies Douglas--Rachford to

    fixed five-replica marginal  intersect  source PSD  intersect  cuts.

After each run the candidate must be crossed again.  Repeating this driver
with that new spectrum is a cutting-plane approximation to the full second
cone.  This is floating-point discovery infrastructure; it is not an exact
PPT certificate or obstruction.
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

import agent_dth_level2_cross_candidate as BASE
import agent_dth_level2_cross_candidate_orbits as CROSS
import agent_dth_level2_joint_extension as JOINT
import agent_dth_level2_joint_symmetry as TARGET_SYMMETRY
import agent_dth_level2_reconstruct_union as RECONSTRUCT
import agent_dth_level2_source_reduced_full as REDUCED
import agent_dth_level2_source_symmetry as SOURCE_SYMMETRY
import agent_dth_level2_active_cut as ACTIVE


DEFAULT_RESUME = DISCOVERY / "dth_level2_source_active_cut.pkl"
DEFAULT_OUTPUT = DISCOVERY / "dth_level2_source_two_cone_active.pkl"


def spectrum_cuts(path, threshold, maximum_per_block, maximum_total):
    """Return all materially negative eigendirections in a crossing cache."""
    with Path(path).open("rb") as stream:
        spectrum = pickle.load(stream)
    output = []
    for label, matrix in sorted(spectrum["blocks"].items()):
        matrix = (matrix + matrix.T) / 2.0
        values, vectors = la.eigh(matrix)
        selected = np.flatnonzero(values < threshold)[:maximum_per_block]
        for index in selected:
            output.append((tuple(label), float(values[index]), vectors[:, index]))
    output.sort(key=lambda item: item[1])
    if maximum_total is not None:
        output = output[:maximum_total]
    return output


def pullback_cuts(reduction, data, factors, mixed_multiplicities, cuts):
    """Pull back several mixed eigenvector cuts with one union reconstruction."""
    tensors = [
        vector.reshape(*(mixed_multiplicities[index] for index in label))
        for label, _, vector in cuts
    ]
    output = [[] for _ in cuts]
    block_by_source = {
        tuple(block["source"]): block for block in data["blocks"]
    }
    orbit_count = len(reduction["orbits"])
    for orbit_index, orbit in enumerate(reduction["orbits"], 1):
        representative = tuple(orbit["representative"])
        block = block_by_source[representative]
        union, _, _ = RECONSTRUCT.reconstruct_union(
            block, data["target_data"], audit=False
        )
        gradients = [
            np.zeros((union.shape[1], union.shape[1])) for _ in cuts
        ]
        orbit_scale = 1.0 / np.sqrt(len(orbit["members"]))
        for member in orbit["members"]:
            member = tuple(member)
            permutation = CROSS.member_permutation(representative, member)
            inverse_permutation = tuple(np.argsort(permutation))
            for cut_index, ((label, _, _), vector_tensor) in enumerate(
                zip(cuts, tensors)
            ):
                if not all(
                    (label[site], member[site]) in factors
                    for site in range(3)
                ):
                    continue
                local = [
                    factors[(label[site], member[site])]
                    for site in range(3)
                ]
                for indices in product(
                    *(range(len(item[0])) for item in local)
                ):
                    transforms = [
                        local[site][1][indices[site]] for site in range(3)
                    ]
                    raw_member = np.einsum(
                        "pa,rb,tc,prt->abc",
                        transforms[0], transforms[1], transforms[2],
                        vector_tensor, optimize="optimal",
                    )
                    raw_representative = np.transpose(
                        raw_member, inverse_permutation
                    ).reshape(-1)
                    compressed = union.T @ raw_representative
                    coefficient = np.prod([
                        local[site][0][indices[site]]
                        for site in range(3)
                    ])
                    gradients[cut_index] += (
                        orbit_scale * coefficient
                        * np.outer(compressed, compressed)
                    )
        for cut_index, gradient in enumerate(gradients):
            for descriptor in orbit["components"]:
                output[cut_index].append(
                    SOURCE_SYMMETRY.adjoint_component(gradient, descriptor)
                )
        if orbit_index % 10 == 0 or orbit_index == orbit_count:
            print(
                "batch pullback orbit", orbit_index, "/", orbit_count,
                "source", representative, "cuts", len(cuts), flush=True,
            )
    assert all(
        len(items) == len(reduction["component_descriptors"])
        for items in output
    )
    return output


def load_physical_source(reduction, path):
    with Path(path).open("rb") as stream:
        candidate = pickle.load(stream)
    shift = SOURCE_SYMMETRY.physical_floor_shift(
        reduction, candidate.get("floor", 0.0)
    )
    return candidate, [
        value + delta for value, delta in zip(
            candidate["shifted_components"], shift
        )
    ]


def main():
    parser = ArgumentParser()
    parser.add_argument("--blocks", type=Path, default=BASE.DEFAULT_BLOCKS)
    parser.add_argument("--crossing", type=Path, default=BASE.DEFAULT_CROSSING)
    parser.add_argument("--fixed-candidate", type=Path,
                        default=BASE.DEFAULT_CANDIDATE)
    parser.add_argument("--resume", type=Path, default=DEFAULT_RESUME)
    parser.add_argument("--spectrum", type=Path, action="append", default=[])
    parser.add_argument("--normal", type=Path, default=REDUCED.DEFAULT_NORMAL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--negative-threshold", type=float, default=-1e-15)
    parser.add_argument("--maximum-per-block", type=int, default=3)
    parser.add_argument(
        "--maximum-new-cuts", type=int, default=15,
        help="retain only the globally most negative new eigenvector cuts",
    )
    parser.add_argument("--iterations", type=int, default=3000)
    parser.add_argument("--cone-cycles", type=int, default=8)
    args = parser.parse_args()

    with args.blocks.open("rb") as stream:
        data = pickle.load(stream)
    JOINT.TARGETS = tuple(data["targets"])
    RECONSTRUCT.ENGINE.TARGETS = tuple(data["targets"])
    reduction = SOURCE_SYMMETRY.build_reduction(
        data["blocks"], data["target_data"], audit=False, compile_maps=True
    )
    directions = TARGET_SYMMETRY.invariant_target_basis(data["target_data"])
    normal = np.load(args.normal)["normal"]
    inverse_normal = la.inv(normal)

    _, fixed_source = load_physical_source(reduction, args.fixed_candidate)
    desired = REDUCED.invariant_coordinates(
        REDUCED.reduced_marginal(reduction, fixed_source), directions
    )
    with args.resume.open("rb") as stream:
        resume = pickle.load(stream)
    _, initial = load_physical_source(reduction, args.resume)
    gradients = list(resume.get("active_gradients", ()))
    labels = list(resume.get("active_labels", ()))
    print("resumed cuts/source components:", len(gradients), len(initial))

    new_cuts = []
    for path in args.spectrum:
        found = spectrum_cuts(
            path, args.negative_threshold, args.maximum_per_block,
            args.maximum_new_cuts,
        )
        print("new spectrum cuts", path, len(found), [
            (item[0], item[1]) for item in found
        ])
        new_cuts.extend(found)

    replays = []
    projection_residuals = []
    if new_cuts:
        crossing = np.load(args.crossing)
        local, _, mixed_multiplicities = BASE.local_blocks(crossing)
        factors, maximum_rank, error = CROSS.local_choi_factors(local)
        print("local Choi rank/error", maximum_rank, error)
        new_gradients = pullback_cuts(
            reduction, data, factors, mixed_multiplicities, new_cuts
        )
        for cut, gradient in zip(new_cuts, new_gradients):
            replay = ACTIVE.inner(gradient, initial)
            kernel, residual = ACTIVE.affine_kernel_projection(
                reduction, directions, inverse_normal, gradient
            )
            # A cut may be constant on the affine space.  Keep the original
            # gradient for evaluation/projection, but expose this diagnostic.
            replays.append((cut[0], cut[1], replay, replay - cut[1]))
            projection_residuals.append((
                cut[0], residual, np.sqrt(ACTIVE.inner(kernel, kernel))
            ))
            gradients.append(gradient)
            labels.append(cut[0])
        print("new cut replays:", replays)
        print("new cut kernel projections:", projection_residuals)

    best = ACTIVE.finite_cut_dr(
        reduction, directions, inverse_normal, desired, initial, gradients,
        args.iterations, args.cone_cycles,
    )
    print("two-cone active best score/residual/defect/min/cuts", best[:5])
    with args.output.open("wb") as stream:
        pickle.dump({
            "floor": 0.0,
            "iteration": args.iterations,
            "score": best[0],
            "residual": best[1],
            "psd_defect": best[2],
            "minimum_shifted_component_eigenvalue": best[3],
            "active_labels": tuple(labels),
            "active_gradients": gradients,
            "finite_cut_values": best[4],
            "shifted_components": best[5],
            "new_cut_replays": replays,
            "new_cut_kernel_projections": projection_residuals,
        }, stream, pickle.HIGHEST_PROTOCOL)
    print("saved", args.output)


if __name__ == "__main__":
    main()
