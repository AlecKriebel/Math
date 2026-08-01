#!/usr/bin/env python3
"""Full fixed-marginal solve on the losslessly reduced DTH source cone.

This combines the 761-dimensional invariant target from
``agent_dth_level2_full_symmetry.py`` with the 112-orbit, 171-PSD-component
source reduction from ``agent_dth_level2_source_symmetry.py``.  It is a
floating-point discovery solver; exactification uses the rational seed and
right-inverse architecture in the companion notes.
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

import agent_dth_level2_joint_extension as JOINT
import agent_dth_level2_joint_symmetry as TARGET_SYMMETRY
import agent_dth_level2_source_symmetry as SOURCE_SYMMETRY


DEFAULT_CACHE = DISCOVERY / "dth_level2_full_blocks.pkl"
DEFAULT_NORMAL = DISCOVERY / "dth_level2_source_reduced_normal.npz"
DEFAULT_CANDIDATE = DISCOVERY / "dth_level2_source_reduced_best.pkl"


def reduced_adjoint(reduction, direction):
    return SOURCE_SYMMETRY.reduce_adjoint(
        reduction,
        JOINT.apply_adjoint(reduction["blocks"], direction),
    )


def reduced_marginal(reduction, variables):
    return JOINT.apply_marginal(
        reduction["blocks"],
        SOURCE_SYMMETRY.expand(reduction, variables),
        reduction["target_data"],
    )


def invariant_coordinates(value, directions):
    return TARGET_SYMMETRY.invariant_coordinates(value, directions)


def build_normal(reduction, directions):
    dimension = len(directions)
    normal = np.empty((dimension, dimension))
    for column, direction in enumerate(directions):
        image = reduced_marginal(
            reduction, reduced_adjoint(reduction, direction)
        )
        normal[:, column] = invariant_coordinates(image, directions)
        if column % 20 == 0:
            print("source-reduced AA* column", column, "/", dimension)
    normal = (normal + normal.T) / 2.0
    spectrum = la.eigvalsh(normal)
    print(
        "source-reduced AA* spectrum/rank:",
        spectrum[0], spectrum[-1],
        np.sum(spectrum > 1e-11 * spectrum[-1]),
    )
    return normal


def coordinates_to_direction(reduction, directions, coordinates):
    output = JOINT.zero_targets(reduction["target_data"])
    for coefficient, support in zip(
        coordinates, TARGET_SYMMETRY.direction_supports(directions)
    ):
        for target, matrix in support:
            output[target] += coefficient * matrix
    return output


def affine_projection(reduction, directions, inverse, desired, variables):
    residual = invariant_coordinates(
        reduced_marginal(reduction, variables), directions
    ) - desired
    multiplier = coordinates_to_direction(
        reduction, directions, inverse @ residual
    )
    correction = reduced_adjoint(reduction, multiplier)
    return [value - delta for value, delta in zip(variables, correction)]


def spectra_metrics(variables):
    spectra = [la.eigvalsh((value + value.T) / 2.0) for value in variables]
    defect = np.sqrt(sum(
        np.sum(np.minimum(spectrum, 0.0) ** 2) for spectrum in spectra
    ))
    return defect, min(spectrum[0] for spectrum in spectra)


def solve(reduction, directions, target, normal, floor, iterations,
          tolerance):
    inverse = la.inv(normal)
    shift = SOURCE_SYMMETRY.physical_floor_shift(reduction, floor)
    desired = (
        invariant_coordinates(target, directions)
        - invariant_coordinates(reduced_marginal(reduction, shift), directions)
    )
    zero = SOURCE_SYMMETRY.zero_components(reduction)
    z = affine_projection(
        reduction, directions, inverse, desired, zero
    )
    best = None
    for iteration in range(iterations + 1):
        positive = SOURCE_SYMMETRY.project_psd(z)
        reflected = [
            2.0 * value - old for value, old in zip(positive, z)
        ]
        affine = affine_projection(
            reduction, directions, inverse, desired, reflected
        )
        z = [
            old + new - projected
            for old, new, projected in zip(z, affine, positive)
        ]
        if iteration % 25 == 0 or iteration == iterations:
            candidate = affine_projection(
                reduction, directions, inverse, desired, positive
            )
            residual = la.norm(
                invariant_coordinates(
                    reduced_marginal(reduction, candidate), directions
                ) - desired
            )
            defect, minimum = spectra_metrics(candidate)
            score = max(residual, defect)
            if best is None or score < best[0]:
                best = (score, residual, defect, minimum, candidate)
            if iteration % 250 == 0:
                print(
                    f"source-reduced DR floor={floor:.2e} "
                    f"iter={iteration:5d} residual={residual:.3e} "
                    f"defect={defect:.3e} min={minimum:.3e}"
                )
            if residual < tolerance and defect < tolerance:
                break
    print("source-reduced best floor/score/residual/defect/min:",
          floor, best[:4])
    return best


def main():
    parser = ArgumentParser()
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--normal-cache", type=Path, default=DEFAULT_NORMAL)
    parser.add_argument("--candidate-cache", type=Path,
                        default=DEFAULT_CANDIDATE)
    parser.add_argument("--iterations", type=int, default=10000)
    parser.add_argument("--floor", type=float, default=0.0)
    parser.add_argument("--tolerance", type=float, default=1e-18)
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()

    with args.cache.open("rb") as stream:
        data = pickle.load(stream)
    JOINT.TARGETS = tuple(data["targets"])
    reduction = SOURCE_SYMMETRY.build_reduction(
        data["blocks"], data["target_data"], audit=args.audit
    )
    directions = TARGET_SYMMETRY.invariant_target_basis(data["target_data"])
    target = TARGET_SYMMETRY.invariant_projection(
        data["target_data"], directions
    )
    if args.normal_cache.exists():
        normal = np.load(args.normal_cache)["normal"]
        assert normal.shape == (761, 761)
        print("loaded source-reduced AA*:", args.normal_cache)
    else:
        normal = build_normal(reduction, directions)
        np.savez_compressed(args.normal_cache, normal=normal)
        print("saved source-reduced AA*:", args.normal_cache)
    best = solve(
        reduction, directions, target, normal,
        floor=args.floor, iterations=args.iterations,
        tolerance=args.tolerance,
    )
    with args.candidate_cache.open("wb") as stream:
        pickle.dump({
            "floor": args.floor,
            "score": best[0],
            "residual": best[1],
            "psd_defect": best[2],
            "minimum_shifted_component_eigenvalue": best[3],
            "shifted_components": best[4],
        }, stream, pickle.HIGHEST_PROTOCOL)
    print("saved source-reduced candidate:", args.candidate_cache)


if __name__ == "__main__":
    main()
