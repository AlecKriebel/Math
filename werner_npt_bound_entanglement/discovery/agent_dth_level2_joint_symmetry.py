#!/usr/bin/env python3
"""Site-symmetry reduction of the joint DTH level-two extension test.

This is floating-point discovery code.  It consumes the temporary block cache
written by ``agent_dth_level2_joint_extension.py`` and exactly averages the
recorded moment over permutations of the three physical qutrit sites.  Since
the degree-three extension cone is site-permutation invariant, feasibility of
the averaged moment can be tested using only invariant target equations.

The invariant target has 13 coordinates in 444, 27 in 333, and 66 in the
orbit of 433, for 106 coordinates total instead of 551.
"""

from __future__ import annotations

from itertools import permutations
from pathlib import Path
import pickle
import sys

import numpy as np
import scipy.linalg as la


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "discovery"
sys.path.insert(0, str(DISCOVERY))

import agent_dth_level2_joint_extension as JOINT


CACHE = DISCOVERY / "dth_level2_joint_blocks.pkl"


def load_or_build_data():
    """Use the optional cache, otherwise replay the committed joint builder."""
    if CACHE.exists():
        with CACHE.open("rb") as handle:
            return pickle.load(handle)
    target_data = {
        target: JOINT.load_target(target) for target in JOINT.TARGETS
    }
    sources = JOINT.candidate_sources(target_data)
    blocks = [
        JOINT.construct_source_block(source, target_data)
        for source in sources
    ]
    return {
        "target_data": target_data,
        "sources": sources,
        "blocks": blocks,
    }


def svec(matrix):
    return np.asarray([
        np.sum(element * matrix)
        for element in JOINT.BASE.symmetric_basis(matrix.shape[0])
    ])


def smat(vector, dimension):
    return sum(
        coefficient * element
        for coefficient, element in zip(
            vector, JOINT.BASE.symmetric_basis(dimension)
        )
    )


def axis_intertwiner(target_data, target, permutation):
    """Orthogonal map from target K space to its permuted target K space."""
    qout = target_data[target][0]
    local_dimensions = [
        len(JOINT.BASE.standard_tableaux(JOINT.S5_SHAPES[index]))
        for index in target
    ]
    permuted_target = tuple(target[index] for index in permutation)
    permuted_qout = target_data[permuted_target][0]
    raw = qout.reshape(*local_dimensions, qout.shape[1])
    raw = raw.transpose(*permutation, 3).reshape(-1, qout.shape[1])
    intertwiner = permuted_qout.T @ raw
    assert la.norm(permuted_qout @ intertwiner - raw) < 4e-10
    assert la.norm(intertwiner.T @ intertwiner - np.eye(qout.shape[1])) < 4e-10
    return permuted_target, intertwiner


def projected_symmetric_basis(dimension, projector, expected_dimension=None):
    columns = []
    for element in JOINT.BASE.symmetric_basis(dimension):
        columns.append(svec(projector(element)))
    columns = np.asarray(columns).T
    u, singular, _ = la.svd(columns, full_matrices=False)
    rank = int(np.sum(singular > 1e-9 * singular[0]))
    if expected_dimension is not None:
        assert rank == expected_dimension, (rank, expected_dimension, singular)
    return [smat(u[:, index], dimension) for index in range(rank)]


def invariant_target_basis(target_data):
    directions = []
    representatives = sorted({tuple(sorted(target)) for target in target_data})
    all_permutations = tuple(permutations(range(3)))
    orbit_census = []
    for representative in representatives:
        orbit_targets = tuple(
            target for target in target_data
            if tuple(sorted(target)) == representative
        )
        stabilizer = [
            axis_intertwiner(target_data, representative, permutation)[1]
            for permutation in all_permutations
            if tuple(representative[index] for index in permutation)
            == representative
        ]

        def stabilizer_projector(matrix):
            return sum(
                value @ matrix @ value.T for value in stabilizer
            ) / len(stabilizer)

        dimension = target_data[representative][1].shape[0]
        representative_basis = projected_symmetric_basis(
            dimension, stabilizer_projector
        )
        orbit_census.append(
            (representative, len(orbit_targets), dimension,
             len(representative_basis))
        )
        for matrix in representative_basis:
            direction = JOINT.zero_targets(target_data)
            for target in orbit_targets:
                selected = None
                for permutation in all_permutations:
                    permuted, intertwiner = axis_intertwiner(
                        target_data, representative, permutation
                    )
                    if permuted == target:
                        selected = intertwiner
                        break
                assert selected is not None
                direction[target] = (
                    selected @ matrix @ selected.T
                    / np.sqrt(len(orbit_targets))
                )
            directions.append(direction)

    expected_totals = {5: 106, 17: 222, 125: 761}
    if len(target_data) in expected_totals:
        assert len(directions) == expected_totals[len(target_data)]
    print("invariant target orbit census:")
    for row in orbit_census:
        print(" ", row)
    gram = np.asarray([
        [JOINT.target_inner(left, right) for right in directions]
        for left in directions
    ])
    assert la.norm(gram - np.eye(len(directions))) < 5e-8
    return directions


def invariant_projection(target_data, directions):
    original = {target: moment for target, (_, moment) in target_data.items()}
    output = JOINT.zero_targets(target_data)
    for direction in directions:
        coefficient = JOINT.target_inner(direction, original)
        for target in JOINT.TARGETS:
            output[target] += coefficient * direction[target]
    return output


def reduced_superoperator(blocks, target_data, directions):
    dimension = len(directions)
    superoperator = np.empty((dimension, dimension))
    for column, direction in enumerate(directions):
        image = JOINT.apply_marginal(
            blocks, JOINT.apply_adjoint(blocks, direction), target_data
        )
        for row, test in enumerate(directions):
            superoperator[row, column] = JOINT.target_inner(test, image)
        if column % 20 == 0:
            print("reduced AA* column", column, "/", dimension)
    superoperator = (superoperator + superoperator.T) / 2.0
    eigenvalues = la.eigvalsh(superoperator)
    print("reduced AA* spectrum/rank:", eigenvalues[0], eigenvalues[-1],
          np.sum(eigenvalues > 1e-11 * eigenvalues[-1]))
    return superoperator


def minimum_norm_preimage(blocks, target_data, directions, target,
                          superoperator):
    coordinates = np.asarray([
        JOINT.target_inner(direction, target) for direction in directions
    ])
    multiplier_coordinates = la.solve(
        superoperator, coordinates, assume_a="sym"
    )
    multiplier = JOINT.zero_targets(target_data)
    for coefficient, direction in zip(multiplier_coordinates, directions):
        for key in JOINT.TARGETS:
            multiplier[key] += coefficient * direction[key]
    variables = JOINT.apply_adjoint(blocks, multiplier)
    image = JOINT.apply_marginal(blocks, variables, target_data)
    residual = np.sqrt(sum(
        la.norm(image[key] - target[key]) ** 2 for key in JOINT.TARGETS
    ))
    rows = []
    for block, variable in zip(blocks, variables):
        values = la.eigvalsh((variable + variable.T) / 2.0)
        rows.append((block["source"], block["dimension"], values[0],
                     values[-1], np.sum(np.minimum(values, 0.0) ** 2)))
    rows.sort(key=lambda row: row[2])
    print("minimum-norm residual/PSD defect/min:", residual,
          np.sqrt(sum(row[4] for row in rows)), rows[0][2])
    print("twenty least source blocks:")
    for row in rows[:20]:
        print(" ", row)
    return multiplier, variables, rows


def project_psd(variables):
    output = []
    for variable in variables:
        eigenvalues, eigenvectors = la.eigh((variable + variable.T) / 2.0)
        output.append(
            (eigenvectors * np.maximum(eigenvalues, 0.0)) @ eigenvectors.T
        )
    return output


def invariant_coordinates(value, directions):
    return np.asarray([
        JOINT.target_inner(direction, value) for direction in directions
    ])


def reduced_dr(blocks, target_data, directions, target, superoperator,
               floor=0.0, iterations=20000, tolerance=2e-13):
    inverse = la.inv(superoperator)
    shift = [floor * np.eye(block["dimension"]) for block in blocks]
    shift_image = JOINT.apply_marginal(blocks, shift, target_data)
    desired = invariant_coordinates(target, directions) - invariant_coordinates(
        shift_image, directions
    )

    def affine_projection(variables):
        image = JOINT.apply_marginal(blocks, variables, target_data)
        residual = invariant_coordinates(image, directions) - desired
        correction_coordinates = inverse @ residual
        correction = JOINT.zero_targets(target_data)
        for coefficient, direction in zip(correction_coordinates, directions):
            for key in JOINT.TARGETS:
                correction[key] += coefficient * direction[key]
        adjoint = JOINT.apply_adjoint(blocks, correction)
        return [value - delta for value, delta in zip(variables, adjoint)]

    zero = [np.zeros((block["dimension"],) * 2) for block in blocks]
    z = affine_projection(zero)
    best = None
    for iteration in range(iterations + 1):
        positive = project_psd(z)
        reflected = [2.0 * value - old for value, old in zip(positive, z)]
        affine = affine_projection(reflected)
        z = [old + new - pos for old, new, pos in zip(z, affine, positive)]
        if iteration % 25 == 0 or iteration == iterations:
            candidate = affine_projection(positive)
            image = JOINT.apply_marginal(blocks, candidate, target_data)
            residual = la.norm(
                invariant_coordinates(image, directions) - desired
            )
            spectra = [la.eigvalsh((value + value.T) / 2.0)
                       for value in candidate]
            psd_defect = np.sqrt(sum(
                np.sum(np.minimum(spectrum, 0.0) ** 2)
                for spectrum in spectra
            ))
            minimum = min(spectrum[0] for spectrum in spectra)
            score = max(residual, psd_defect)
            if best is None or score < best[0]:
                best = (score, residual, psd_defect, minimum, candidate)
            if iteration % 250 == 0:
                print(
                    f"sym DR floor={floor:.2e} iter={iteration:5d} "
                    f"res={residual:.3e} psd={psd_defect:.3e} "
                    f"min={minimum:.3e}"
                )
            if residual < tolerance and psd_defect < tolerance:
                break
    print("sym DR best floor/score/residual/defect/min:",
          floor, best[:4])
    return best


def main():
    data = load_or_build_data()
    target_data = data["target_data"]
    blocks = data["blocks"]
    directions = invariant_target_basis(target_data)
    target = invariant_projection(target_data, directions)
    projection_residual = np.sqrt(sum(
        la.norm(target[key] - target_data[key][1]) ** 2
        for key in JOINT.TARGETS
    ))
    original_norm = np.sqrt(sum(
        la.norm(target_data[key][1]) ** 2 for key in JOINT.TARGETS
    ))
    print("site-average change relative norm:",
          projection_residual / original_norm)
    superoperator = reduced_superoperator(blocks, target_data, directions)
    minimum_norm_preimage(
        blocks, target_data, directions, target, superoperator
    )
    reduced_dr(
        blocks, target_data, directions, target, superoperator,
        floor=0.0, iterations=5000, tolerance=1e-18,
    )
    reduced_dr(
        blocks, target_data, directions, target, superoperator,
        floor=1e-12, iterations=5000, tolerance=1e-18,
    )


if __name__ == "__main__":
    main()
