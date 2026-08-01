#!/usr/bin/env python3
"""Joint active-cut solver for all three grouped DTH PPT representatives.

This resumes a Gamma_A-corrected degree-three source, selects the strongest
negative eigenvector in each crossed Gamma_z/Gamma_Az block, pulls a bounded
number of those cuts back to the 171 site-symmetric source components, and
solves

    fixed marginal + source PSD + all retained PPT half-space cuts.

Cut metadata retains the crossing type.  Gamma_Az is spectrally equivalent
to Gamma_AA by full transpose and bivector-pair symmetry.  This is
floating-point cutting-plane infrastructure, not an exact cone certificate.
"""

from argparse import ArgumentParser
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
import agent_dth_level2_two_cone_active as TWO_CONE
import agent_dth_level2_active_cut as ACTIVE


DEFAULT_RESUME = DISCOVERY / "dth_level2_source_two_cone_round5_refined.pkl"
DEFAULT_GAMMA_Z_CROSSING = (
    DISCOVERY / "dth_level2_local_gamma_z_crossing.npz"
)
DEFAULT_GAMMA_Z_SPECTRUM = (
    DISCOVERY / "dth_level2_cross_gamma_z_round5_max500.pkl"
)
DEFAULT_GAMMA_AZ_CROSSING = (
    DISCOVERY / "dth_level2_local_gamma_az_crossing.npz"
)
DEFAULT_GAMMA_AZ_SPECTRUM = (
    DISCOVERY / "dth_level2_cross_gamma_az_round5_max100.pkl"
)
DEFAULT_OUTPUT = DISCOVERY / "dth_level2_source_all_ppt_round1.pkl"


def tagged_existing_labels(resume):
    metadata = resume.get("active_cut_metadata")
    if metadata is not None:
        return list(metadata)
    return [
        ("gamma_a", tuple(label))
        for label in resume.get("active_labels", ())
    ]


def main():
    parser = ArgumentParser()
    parser.add_argument("--blocks", type=Path, default=BASE.DEFAULT_BLOCKS)
    parser.add_argument("--fixed-candidate", type=Path,
                        default=BASE.DEFAULT_CANDIDATE)
    parser.add_argument("--resume", type=Path, default=DEFAULT_RESUME)
    parser.add_argument("--gamma-z-crossing", type=Path,
                        default=DEFAULT_GAMMA_Z_CROSSING)
    parser.add_argument("--gamma-z-spectrum", type=Path,
                        default=DEFAULT_GAMMA_Z_SPECTRUM)
    parser.add_argument("--gamma-az-crossing", type=Path,
                        default=DEFAULT_GAMMA_AZ_CROSSING)
    parser.add_argument("--gamma-az-spectrum", type=Path,
                        default=DEFAULT_GAMMA_AZ_SPECTRUM)
    parser.add_argument("--normal", type=Path, default=REDUCED.DEFAULT_NORMAL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--negative-threshold", type=float, default=-1e-15)
    parser.add_argument("--maximum-per-block", type=int, default=1)
    parser.add_argument("--maximum-new-per-type", type=int, default=10)
    parser.add_argument("--iterations", type=int, default=300)
    parser.add_argument("--cone-cycles", type=int, default=4)
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

    _, fixed_source = TWO_CONE.load_physical_source(
        reduction, args.fixed_candidate
    )
    desired = REDUCED.invariant_coordinates(
        REDUCED.reduced_marginal(reduction, fixed_source), directions
    )
    with args.resume.open("rb") as stream:
        resume = pickle.load(stream)
    _, initial = TWO_CONE.load_physical_source(reduction, args.resume)
    gradients = list(resume.get("active_gradients", ()))
    metadata = tagged_existing_labels(resume)
    assert len(metadata) == len(gradients)
    print("resumed source components/cuts:", len(initial), len(gradients))

    new_diagnostics = []
    cut_specs = (
        ("gamma_z", args.gamma_z_crossing, args.gamma_z_spectrum),
        ("gamma_az", args.gamma_az_crossing, args.gamma_az_spectrum),
    )
    for cut_type, crossing_path, spectrum_path in cut_specs:
        cuts = TWO_CONE.spectrum_cuts(
            spectrum_path,
            args.negative_threshold,
            args.maximum_per_block,
            args.maximum_new_per_type,
        )
        print("selected", cut_type, "cuts:", [
            (label, eigenvalue) for label, eigenvalue, _ in cuts
        ], flush=True)
        crossing = np.load(crossing_path)
        local, _, mixed_multiplicities = BASE.local_blocks(crossing)
        factors, maximum_rank, factor_error = CROSS.local_choi_factors(local)
        print(cut_type, "local Choi rank/error:",
              maximum_rank, factor_error, flush=True)
        pulled = TWO_CONE.pullback_cuts(
            reduction, data, factors, mixed_multiplicities, cuts
        )
        for (label, crossed_value, _), gradient in zip(cuts, pulled):
            replay = ACTIVE.inner(gradient, initial)
            kernel, residual = ACTIVE.affine_kernel_projection(
                reduction, directions, inverse_normal, gradient
            )
            kernel_norm = np.sqrt(ACTIVE.inner(kernel, kernel))
            diagnostic = {
                "cut_type": cut_type,
                "label": tuple(label),
                "crossed_value": crossed_value,
                "replay": replay,
                "replay_error": replay - crossed_value,
                "affine_kernel_residual": residual,
                "affine_kernel_norm": kernel_norm,
            }
            print("new cut replay/kernel:", diagnostic, flush=True)
            new_diagnostics.append(diagnostic)
            gradients.append(gradient)
            metadata.append((cut_type, tuple(label)))

    best = ACTIVE.finite_cut_dr(
        reduction, directions, inverse_normal, desired, initial, gradients,
        args.iterations, args.cone_cycles,
    )
    print("all-PPT active best score/residual/defect/min/cuts:", best[:5])
    with args.output.open("wb") as stream:
        pickle.dump({
            "floor": 0.0,
            "iteration": args.iterations,
            "score": best[0],
            "residual": best[1],
            "psd_defect": best[2],
            "minimum_shifted_component_eigenvalue": best[3],
            "active_cut_metadata": tuple(metadata),
            # Retain the legacy field for compatibility with the Gamma_A
            # solver; entries are now tagged pairs.
            "active_labels": tuple(metadata),
            "active_gradients": gradients,
            "finite_cut_values": best[4],
            "shifted_components": best[5],
            "new_cut_diagnostics": tuple(new_diagnostics),
        }, stream, pickle.HIGHEST_PROTOCOL)
    print("saved:", args.output)


if __name__ == "__main__":
    main()
