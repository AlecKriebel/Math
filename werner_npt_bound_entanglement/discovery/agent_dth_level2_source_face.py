#!/usr/bin/env python3
"""Search for a site-invariant facial ray of the PSD-only DTH extension.

Let A be the complete degree-three-to-degree-two marginal map after the
holomorphic Omega quotient, restricted losslessly to site-invariant source
and target coordinates.  A nonzero target multiplier y satisfying

    A^* y >= 0,       <y,r> = 0

exposes a face containing every positive preimage of the fixed marginal r.
We fix ``trace(A^*y)=1`` and use Douglas--Rachford between the product PSD
cone and the resulting affine subspace of ``range(A^*)``.

Floating point is used only for discovery.  A ray found by this script is
not an exact facial certificate until reconstructed and audited exactly.
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

import agent_dth_level2_joint_extension as JOINT
import agent_dth_level2_joint_symmetry as TARGET_SYMMETRY
import agent_dth_level2_source_symmetry as SOURCE_SYMMETRY


DEFAULT_NORMAL = DISCOVERY / "dth_level2_full_symmetric_normal.npz"
DEFAULT_SAVE = DISCOVERY / "dth_level2_source_face_best.pkl"


def target_from_coordinates(target_data, directions, coefficients):
    output = JOINT.zero_targets(target_data)
    supports = TARGET_SYMMETRY.direction_supports(directions)
    for coefficient, support in zip(coefficients, supports):
        for target, matrix in support:
            output[target] += coefficient * matrix
    return output


def source_inner(left, right):
    return sum(np.sum(a * b) for a, b in zip(left, right))


def source_norm(values):
    return np.sqrt(source_inner(values, values))


def marginal(reduction, values):
    return JOINT.apply_marginal(
        reduction["blocks"], SOURCE_SYMMETRY.expand(reduction, values),
        reduction["target_data"],
    )


def adjoint(reduction, direction):
    full = JOINT.apply_adjoint(reduction["blocks"], direction)
    return SOURCE_SYMMETRY.reduce_adjoint(reduction, full)


def solve(iterations, report, save, normal_cache):
    data, reduction = SOURCE_SYMMETRY.load_default()
    target_data = data["target_data"]
    directions = TARGET_SYMMETRY.invariant_target_basis(target_data)
    assert len(directions) == 761
    target = TARGET_SYMMETRY.invariant_projection(target_data, directions)
    target_coordinates = TARGET_SYMMETRY.invariant_coordinates(
        target, directions
    )

    normal = np.load(normal_cache)["normal"]
    normal_inverse = la.inv(normal)
    identity = SOURCE_SYMMETRY.physical_floor_shift(reduction, 1.0)
    trace_coordinates = TARGET_SYMMETRY.invariant_coordinates(
        marginal(reduction, identity), directions
    )

    constraints = np.column_stack((target_coordinates, trace_coordinates))
    constraint_rhs = np.array((0.0, 1.0))
    normal_inverse_constraints = normal_inverse @ constraints
    constraint_gram = constraints.T @ normal_inverse_constraints
    assert la.eigvalsh(constraint_gram)[0] > 0.0

    def affine_projection(values):
        image_coordinates = TARGET_SYMMETRY.invariant_coordinates(
            marginal(reduction, values), directions
        )
        multiplier_coordinates = normal_inverse @ image_coordinates
        defect = constraint_rhs - constraints.T @ multiplier_coordinates
        multiplier_coordinates += normal_inverse_constraints @ la.solve(
            constraint_gram, defect, assume_a="sym"
        )
        multiplier = target_from_coordinates(
            target_data, directions, multiplier_coordinates
        )
        return adjoint(reduction, multiplier)

    z = affine_projection(SOURCE_SYMMETRY.zero_components(reduction))
    best = None
    for iteration in range(iterations + 1):
        positive = SOURCE_SYMMETRY.project_psd(z)
        reflected = [2.0 * value - old for value, old in zip(positive, z)]
        affine = affine_projection(reflected)
        z = [old + new - pos for old, new, pos in zip(z, affine, positive)]

        if iteration % 25 == 0 or iteration == iterations:
            candidate = affine_projection(positive)
            spectra = [la.eigvalsh((value + value.T) / 2.0)
                       for value in candidate]
            psd_defect = np.sqrt(sum(
                np.sum(np.minimum(spectrum, 0.0) ** 2)
                for spectrum in spectra
            ))
            minimum = min(spectrum[0] for spectrum in spectra)

            image_coordinates = TARGET_SYMMETRY.invariant_coordinates(
                marginal(reduction, candidate), directions
            )
            multiplier_coordinates = normal_inverse @ image_coordinates
            multiplier = target_from_coordinates(
                target_data, directions, multiplier_coordinates
            )
            reconstructed = adjoint(reduction, multiplier)
            range_residual = source_norm([
                value - recovered
                for value, recovered in zip(candidate, reconstructed)
            ])
            target_pairing = float(
                target_coordinates @ multiplier_coordinates
            )
            trace = float(source_inner(identity, candidate))
            score = max(
                psd_defect, range_residual, abs(target_pairing),
                abs(trace - 1.0),
            )
            if best is None or score < best[0]:
                best = (
                    score, psd_defect, minimum, range_residual,
                    target_pairing, trace, multiplier_coordinates, candidate,
                )
            if iteration % report == 0 or iteration == iterations:
                print(
                    f"face DR iter={iteration:5d} score={score:.3e} "
                    f"psd={psd_defect:.3e} min={minimum:.3e} "
                    f"range={range_residual:.3e} pair={target_pairing:.3e} "
                    f"trace={trace:.16g}"
                )

    payload = {
        "score": best[0],
        "psd_defect": best[1],
        "minimum_eigenvalue": best[2],
        "range_residual": best[3],
        "target_pairing": best[4],
        "trace": best[5],
        "multiplier_coordinates": best[6],
        "source_candidate": best[7],
    }
    with save.open("wb") as stream:
        pickle.dump(payload, stream, pickle.HIGHEST_PROTOCOL)
    print("best face metrics:", {key: value for key, value in payload.items()
                                  if key not in ("multiplier_coordinates",
                                                 "source_candidate")})
    print("saved:", save)


def main():
    parser = ArgumentParser()
    parser.add_argument("--iterations", type=int, default=5000)
    parser.add_argument("--report", type=int, default=250)
    parser.add_argument("--save", type=Path, default=DEFAULT_SAVE)
    parser.add_argument("--normal-cache", type=Path, default=DEFAULT_NORMAL)
    args = parser.parse_args()
    solve(args.iterations, args.report, args.save, args.normal_cache)


if __name__ == "__main__":
    main()
