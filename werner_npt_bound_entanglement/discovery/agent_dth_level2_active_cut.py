#!/usr/bin/env python3
"""Active-cut affine correction core for the degree-three DTH Gamma_A cone.

This is floating-point discovery code.  It pulls selected negative mixed
eigenvectors back through the low-Choi-rank crossing, projects their source
gradients into the fixed-marginal affine kernel, and applies the minimum
Euclidean correction satisfying the selected linear cuts.  Exact claims
require rational reconstruction after a robust feasible point is found.
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


DEFAULT_SPECTRUM = DISCOVERY / "dth_level2_crossed_orbits_max100.pkl"
DEFAULT_OUTPUT = DISCOVERY / "dth_level2_source_active_cut.pkl"


def inner(left, right):
    return float(sum(
        np.vdot(a, b).real for a, b in zip(left, right)
    ))


def scaled_add(base, directions, coefficients):
    return [
        value + sum(
            coefficient * direction[index]
            for coefficient, direction in zip(coefficients, directions)
        )
        for index, value in enumerate(base)
    ]


def subtract(left, right):
    return [a - b for a, b in zip(left, right)]


def add(left, right):
    return [a + b for a, b in zip(left, right)]


def zeros_like(value):
    return [np.zeros_like(item) for item in value]


def project_halfspace(value, gradient, norm_squared):
    pairing = inner(value, gradient)
    if pairing >= 0.0:
        return value
    return scaled_add(value, (gradient,), (-pairing / norm_squared,))


def project_cut_cone(value, gradients, cycles):
    """Dykstra projection onto block-PSD and finitely many halfspaces."""
    current = [item.copy() for item in value]
    corrections = [zeros_like(value) for _ in range(len(gradients) + 1)]
    norms = [inner(item, item) for item in gradients]
    for _ in range(cycles):
        shifted = add(current, corrections[0])
        projected = SOURCE_SYMMETRY.project_psd(shifted)
        corrections[0] = subtract(shifted, projected)
        current = projected
        for index, (gradient, norm_squared) in enumerate(
            zip(gradients, norms), 1
        ):
            shifted = add(current, corrections[index])
            projected = project_halfspace(
                shifted, gradient, norm_squared
            )
            corrections[index] = subtract(shifted, projected)
            current = projected
    return current


def selected_eigenvectors(spectrum, labels):
    output = []
    for label in labels:
        matrix = spectrum["blocks"][label]
        values, vectors = la.eigh((matrix + matrix.T) / 2.0)
        output.append((label, float(values[0]), vectors[:, 0]))
    return output


def pullback_cut(reduction, data, factors, mixed_multiplicities,
                 label, vector):
    """Return reduced source gradient for v^T Gamma_A(T)[label] v."""
    vector_tensor = vector.reshape(
        *(mixed_multiplicities[index] for index in label)
    )
    block_by_source = {
        tuple(block["source"]): block for block in data["blocks"]
    }
    output = []
    for orbit_index, orbit in enumerate(reduction["orbits"], 1):
        representative = tuple(orbit["representative"])
        block = block_by_source[representative]
        union, _, metrics = RECONSTRUCT.reconstruct_union(
            block, data["target_data"], audit=True
        )
        gradient = np.zeros((union.shape[1], union.shape[1]))
        orbit_scale = 1.0 / np.sqrt(len(orbit["members"]))
        for member in orbit["members"]:
            member = tuple(member)
            if not all(
                (label[site], member[site]) in factors
                for site in range(3)
            ):
                continue
            permutation = CROSS.member_permutation(representative, member)
            inverse_permutation = tuple(np.argsort(permutation))
            local = [
                factors[(label[site], member[site])]
                for site in range(3)
            ]
            for indices in product(*(range(len(item[0])) for item in local)):
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
                    local[site][0][indices[site]] for site in range(3)
                ])
                gradient += (
                    orbit_scale * coefficient
                    * np.outer(compressed, compressed)
                )
        for descriptor in orbit["components"]:
            output.append(SOURCE_SYMMETRY.adjoint_component(
                gradient, descriptor
            ))
        if orbit_index % 20 == 0:
            print("pullback", label, "orbit", orbit_index, "/",
                  len(reduction["orbits"]), flush=True)
    assert len(output) == len(reduction["component_descriptors"])
    return output


def affine_kernel_projection(reduction, directions, inverse_normal, value):
    image = REDUCED.reduced_marginal(reduction, value)
    coordinates = REDUCED.invariant_coordinates(image, directions)
    multiplier = REDUCED.coordinates_to_direction(
        reduction, directions, inverse_normal @ coordinates
    )
    adjoint = REDUCED.reduced_adjoint(reduction, multiplier)
    projected = [a - b for a, b in zip(value, adjoint)]
    residual = la.norm(REDUCED.invariant_coordinates(
        REDUCED.reduced_marginal(reduction, projected), directions
    ))
    return projected, residual


def affine_projection(reduction, directions, inverse_normal, desired, value):
    image = REDUCED.reduced_marginal(reduction, value)
    coordinates = REDUCED.invariant_coordinates(image, directions)
    multiplier = REDUCED.coordinates_to_direction(
        reduction, directions, inverse_normal @ (coordinates - desired)
    )
    adjoint = REDUCED.reduced_adjoint(reduction, multiplier)
    return subtract(value, adjoint)


def finite_cut_dr(reduction, directions, inverse_normal, desired, initial,
                  gradients, iterations, cone_cycles):
    iterate = [item.copy() for item in initial]
    best = None
    for iteration in range(iterations + 1):
        cone = project_cut_cone(iterate, gradients, cone_cycles)
        reflected = [2.0 * a - b for a, b in zip(cone, iterate)]
        affine = affine_projection(
            reduction, directions, inverse_normal, desired, reflected
        )
        iterate = [old + new - projected for old, new, projected in zip(
            iterate, affine, cone
        )]
        if iteration % 10 == 0 or iteration == iterations:
            candidate = affine_projection(
                reduction, directions, inverse_normal, desired, cone
            )
            residual = la.norm(REDUCED.invariant_coordinates(
                REDUCED.reduced_marginal(reduction, candidate), directions
            ) - desired)
            defect, minimum = REDUCED.spectra_metrics(candidate)
            cuts = np.array([inner(item, candidate) for item in gradients])
            cut_defect = la.norm(np.minimum(cuts, 0.0))
            score = max(residual, defect, cut_defect)
            if best is None or score < best[0]:
                best = (score, residual, defect, minimum, cuts, candidate)
            if iteration % 100 == 0:
                print("finite-cut DR", iteration, "score/res/psd/min/cuts",
                      score, residual, defect, minimum, cuts, flush=True)
    return best


def main():
    parser = ArgumentParser()
    parser.add_argument("--blocks", type=Path, default=BASE.DEFAULT_BLOCKS)
    parser.add_argument("--candidate", type=Path, default=BASE.DEFAULT_CANDIDATE)
    parser.add_argument("--crossing", type=Path, default=BASE.DEFAULT_CROSSING)
    parser.add_argument("--spectrum", type=Path, default=DEFAULT_SPECTRUM)
    parser.add_argument("--normal", type=Path,
                        default=REDUCED.DEFAULT_NORMAL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--margin", type=float, default=1.05)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--cone-cycles", type=int, default=4)
    args = parser.parse_args()

    with args.blocks.open("rb") as stream:
        data = pickle.load(stream)
    JOINT.TARGETS = tuple(data["targets"])
    RECONSTRUCT.ENGINE.TARGETS = tuple(data["targets"])
    reduction = SOURCE_SYMMETRY.build_reduction(
        data["blocks"], data["target_data"], audit=False,
        compile_maps=True,
    )
    directions = TARGET_SYMMETRY.invariant_target_basis(data["target_data"])
    normal = np.load(args.normal)["normal"]
    inverse_normal = la.inv(normal)

    with args.candidate.open("rb") as stream:
        candidate = pickle.load(stream)
    shift = SOURCE_SYMMETRY.physical_floor_shift(
        reduction, candidate["floor"]
    )
    source = [
        value + delta for value, delta in zip(
            candidate["shifted_components"], shift
        )
    ]
    with args.spectrum.open("rb") as stream:
        spectrum = pickle.load(stream)
    labels = ((1, 2, 9), (1, 4, 9), (0, 2, 5), (1, 4, 6))
    eigenvectors = selected_eigenvectors(spectrum, labels)

    crossing = np.load(args.crossing)
    local, _, mixed_multiplicities = BASE.local_blocks(crossing)
    factors, maximum_rank, error = CROSS.local_choi_factors(local)
    print("local Choi rank/error", maximum_rank, error)

    gradients = []
    projected = []
    for label, eigenvalue, vector in eigenvectors:
        gradient = pullback_cut(
            reduction, data, factors, mixed_multiplicities, label, vector
        )
        replay = inner(gradient, source)
        print("cut replay", label, "crossed/direct", replay, eigenvalue,
              "error", replay - eigenvalue)
        kernel, residual = affine_kernel_projection(
            reduction, directions, inverse_normal, gradient
        )
        print("kernel projection", label, "residual/norm",
              residual, np.sqrt(inner(kernel, kernel)))
        gradients.append(gradient)
        projected.append(kernel)

    gram = np.array([
        [inner(left, right) for right in projected]
        for left in gradients
    ])
    gram = (gram + gram.T) / 2.0
    right = -args.margin * np.array([item[1] for item in eigenvectors])
    coefficients = la.solve(gram, right, assume_a="sym")
    corrected = scaled_add(source, projected, coefficients)
    values = [la.eigvalsh((value + value.T) / 2.0) for value in corrected]
    marginal_residual = la.norm(REDUCED.invariant_coordinates(
        REDUCED.reduced_marginal(reduction, corrected), directions
    ) - REDUCED.invariant_coordinates(
        REDUCED.reduced_marginal(reduction, source), directions
    ))
    print("cut Gram eigenvalues", la.eigvalsh(gram))
    print("coefficients", coefficients)
    print("corrected cut predictions", np.array([
        value + sum(
            coefficient * gram[row, column]
            for column, coefficient in enumerate(coefficients)
        ) for row, (_, value, _) in enumerate(eigenvectors)
    ]))
    print("source minimum/marginal residual",
          min(value[0] for value in values), marginal_residual)

    desired = REDUCED.invariant_coordinates(
        REDUCED.reduced_marginal(reduction, source), directions
    )
    best = finite_cut_dr(
        reduction, directions, inverse_normal, desired, source, gradients,
        args.iterations, args.cone_cycles,
    )
    print("finite-cut best score/residual/defect/min/cuts", best[:5])

    with args.output.open("wb") as stream:
        pickle.dump({
            "floor": 0.0,
            "iteration": args.iterations,
            "score": best[0],
            "residual": best[1],
            "psd_defect": best[2],
            "minimum_shifted_component_eigenvalue": best[3],
            "active_labels": labels,
            "active_gram": gram,
            "active_coefficients": coefficients,
            "active_gradients": gradients,
            "finite_cut_score": best[0],
            "finite_cut_residual": best[1],
            "finite_cut_psd_defect": best[2],
            "finite_cut_minimum": best[3],
            "finite_cut_values": best[4],
            "shifted_components": best[5],
        }, stream, pickle.HIGHEST_PROTOCOL)
    print("saved", args.output)


if __name__ == "__main__":
    main()
