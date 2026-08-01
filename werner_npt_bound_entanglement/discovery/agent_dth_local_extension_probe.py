#!/usr/bin/env python3
"""Cheapest one-site symmetric-extension probe for the DTH pseudomoment.

This discovery script first reconstructs the exact five-replica certificate
in the selected local permutation-diagram coordinates.  It then traces out
two physical qutrit sites, producing the one-site five-replica marginal.

The next stage (added below) tests whether this marginal admits a third
exchangeable copy of the bivector pair.  Floating point is used only for
discovery; every reconstruction is independently audited in the dense local
243-dimensional Hilbert space.
"""

from __future__ import annotations

import importlib.util
from itertools import permutations, product
from math import sqrt
from pathlib import Path

import numpy as np
import scipy.linalg as la


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VERIFY = ROOT / "verification"


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


REALIGN = import_file(
    "dth_local_ext_realign", HERE / "agent_dth_realignment_probe.py"
)
CODEC = REALIGN.CODEC
BRIDGE = REALIGN.BRIDGE


def permutation_cycles(permutation):
    seen = set()
    count = 0
    for start in range(len(permutation)):
        if start in seen:
            continue
        count += 1
        current = start
        while current not in seen:
            seen.add(current)
            current = permutation[current]
    return count


def compose(left, right):
    """Image-form composition left o right."""
    return tuple(left[right[index]] for index in range(len(left)))


def inverse(permutation):
    out = [None] * len(permutation)
    for source, target in enumerate(permutation):
        out[target] = source
    return tuple(out)


def standard_tableaux(shape):
    """Return tableaux as tuples giving the cell of each entry."""
    shape = tuple(shape)

    def recurse(current_shape):
        size = sum(current_shape)
        if size == 0:
            yield ()
            return
        for row in range(len(current_shape)):
            if row + 1 < len(current_shape) and (
                    current_shape[row] == current_shape[row + 1]):
                continue
            column = current_shape[row] - 1
            smaller = list(current_shape)
            smaller[row] -= 1
            if smaller[row] == 0:
                smaller.pop(row)
            for positions in recurse(tuple(smaller)):
                yield positions + ((row, column),)

    return tuple(recurse(shape))


def adjacent_specht_matrices(shape):
    """Young orthogonal matrices for adjacent transpositions."""
    tableaux = standard_tableaux(shape)
    index = {tableau: position for position, tableau in enumerate(tableaux)}
    dimension = len(tableaux)
    matrices = []
    for adjacent in range(sum(shape) - 1):
        matrix = np.zeros((dimension, dimension))
        for column, tableau in enumerate(tableaux):
            first = tableau[adjacent]
            second = tableau[adjacent + 1]
            axial = ((second[1] - second[0])
                     - (first[1] - first[0]))
            diagonal = 1.0 / axial
            matrix[column, column] = diagonal
            if abs(axial) != 1:
                swapped = list(tableau)
                swapped[adjacent], swapped[adjacent + 1] = (
                    swapped[adjacent + 1], swapped[adjacent]
                )
                row = index[tuple(swapped)]
                matrix[row, column] = sqrt(1.0 - diagonal * diagonal)
        assert la.norm(matrix @ matrix - np.eye(dimension)) < 1e-12
        matrices.append(matrix)
    return tableaux, matrices


def adjacent_word(permutation):
    """Express an image-form permutation as right adjacent swaps."""
    current = list(range(len(permutation)))
    word = []
    for position, wanted in enumerate(permutation):
        location = current.index(wanted, position)
        while location > position:
            current[location - 1], current[location] = (
                current[location], current[location - 1]
            )
            word.append(location - 1)
            location -= 1
    assert tuple(current) == tuple(permutation)
    return word


def specht_representation(adjacent, permutation):
    matrix = np.eye(adjacent[0].shape[0])
    for generator in adjacent_word(permutation):
        matrix = matrix @ adjacent[generator]
    return matrix


def gl3_dimension(shape):
    padded = tuple(shape) + (0,) * (3 - len(shape))
    numerator = 1
    denominator = 1
    for first in range(3):
        for second in range(first + 1, 3):
            numerator *= padded[first] - padded[second] + second - first
            denominator *= second - first
    assert numerator % denominator == 0
    return numerator // denominator


def svec(matrix):
    """Orthonormal vectorization of a real symmetric matrix."""
    matrix = (matrix + matrix.T) / 2
    values = [matrix[index, index] for index in range(matrix.shape[0])]
    values.extend(
        sqrt(2.0) * matrix[row, column]
        for row in range(matrix.shape[0])
        for column in range(row + 1, matrix.shape[0])
    )
    return np.asarray(values)


def smat(vector, dimension):
    matrix = np.zeros((dimension, dimension))
    position = 0
    for index in range(dimension):
        matrix[index, index] = vector[position]
        position += 1
    for row in range(dimension):
        for column in range(row + 1, dimension):
            matrix[row, column] = matrix[column, row] = (
                vector[position] / sqrt(2.0)
            )
            position += 1
    assert position == len(vector)
    return matrix


def target_moments(rho):
    moments = []
    permutations5 = tuple(permutations(range(5)))
    for permutation in permutations5:
        operator = BRIDGE.permutation_operator(permutation)
        moments.append(sum(
            float(value) * rho[row, column]
            for (row, column), value in operator.items()
        ))
    return permutations5, np.asarray(moments)


def embed_five(permutation, retained_pairs):
    """Embed target pair-pair-z slots into three-pair-pair-pair-z slots."""
    retained = (
        2 * retained_pairs[0], 2 * retained_pairs[0] + 1,
        2 * retained_pairs[1], 2 * retained_pairs[1] + 1,
        6,
    )
    output = list(range(7))
    for source, target in enumerate(permutation):
        output[retained[source]] = retained[target]
    return tuple(output)


def extension_affine_system(target):
    """Three equal two-pair marginals in the U(3)-invariant S7 blocks."""
    shapes = (
        (7,), (6, 1), (5, 2), (5, 1, 1),
        (4, 3), (4, 2, 1), (3, 3, 1), (3, 2, 2),
    )
    local_data = []
    offsets = [0]
    for shape in shapes:
        tableaux, adjacent = adjacent_specht_matrices(shape)
        dimension = len(tableaux)
        local_data.append({
            "shape": shape,
            "dimension": dimension,
            "carrier": gl3_dimension(shape),
            "adjacent": adjacent,
        })
        offsets.append(offsets[-1] + dimension * (dimension + 1) // 2)
    print("S7 symmetric block variables:", offsets[-1])

    permutations5 = tuple(permutations(range(5)))
    pair_choices = ((0, 1), (0, 2), (1, 2))
    system = np.zeros((len(pair_choices) * len(permutations5), offsets[-1]))
    for pair_row, pair_choice in enumerate(pair_choices):
        for permutation_row, permutation in enumerate(permutations5):
            row = pair_row * len(permutations5) + permutation_row
            embedded = embed_five(permutation, pair_choice)
            # Our dense P_pi convention is the inverse of the standard
            # left group action.  Symmetrization makes inversion immaterial,
            # but retaining it here fixes the convention explicitly.
            embedded = inverse(embedded)
            for block, data in enumerate(local_data):
                representation = specht_representation(
                    data["adjacent"], embedded
                )
                system[row, offsets[block]:offsets[block + 1]] = (
                    data["carrier"] * svec(representation)
                )
    right = np.tile(target, len(pair_choices))
    return system, right, local_data, offsets


def inspect_affine_extension(system, right, local_data, offsets):
    solution, residuals, rank, singular = la.lstsq(
        system, right, lapack_driver="gelsd"
    )
    relative = la.norm(system @ solution - right) / la.norm(right)
    print("extension affine rank/residual/min singular:",
          rank, relative, singular[-1])
    minimum = float("inf")
    block_spectra = []
    for block, data in enumerate(local_data):
        matrix = smat(solution[offsets[block]:offsets[block + 1]],
                      data["dimension"])
        eigenvalues = la.eigvalsh(matrix)
        minimum = min(minimum, eigenvalues[0])
        block_spectra.append((data["shape"], eigenvalues[0],
                              eigenvalues[-1], np.trace(matrix)))
    print("minimum-norm affine extension minimum eigenvalue:", minimum)
    print("minimum-norm affine block spectra:")
    for row in block_spectra:
        print(" ", row)
    return solution


def project_psd(vector, local_data, offsets):
    output = np.empty_like(vector)
    minimum = float("inf")
    negative_squared = 0.0
    for block, data in enumerate(local_data):
        sl = slice(offsets[block], offsets[block + 1])
        matrix = smat(vector[sl], data["dimension"])
        eigenvalues, eigenvectors = la.eigh(matrix)
        minimum = min(minimum, eigenvalues[0])
        negative_squared += np.sum(np.minimum(eigenvalues, 0.0) ** 2)
        positive = np.maximum(eigenvalues, 0.0)
        output[sl] = svec((eigenvectors * positive) @ eigenvectors.T)
    return output, minimum, sqrt(negative_squared)


def dykstra_psd_affine(system, right, local_data, offsets,
                       iterations=20000, tolerance=2e-10, floor=0.0):
    """Project onto affine marginals intersected with block PSD cone."""
    shift = np.zeros(system.shape[1])
    if floor:
        for block, data in enumerate(local_data):
            shift[offsets[block]:offsets[block + 1]] = svec(
                floor * np.eye(data["dimension"])
            )
    shifted_right = right - system @ shift
    u, singular, vh = la.svd(system, full_matrices=False)
    threshold = 1e-11 * singular[0]
    rank = int(np.sum(singular > threshold))
    u = u[:, :rank]
    singular = singular[:rank]
    vh = vh[:rank, :]
    particular = vh.T @ ((u.T @ shifted_right) / singular)
    affine_right_residual = (
        la.norm(shifted_right - u @ (u.T @ shifted_right))
        / la.norm(right)
    )
    print("affine SVD rank/right-space residual/condition:",
          rank, affine_right_residual, singular[0] / singular[-1])

    def project_affine(vector):
        residual = shifted_right - system @ vector
        return vector + vh.T @ ((u.T @ residual) / singular)

    vector = particular.copy()
    affine_correction = np.zeros_like(vector)
    psd_correction = np.zeros_like(vector)
    best = None
    for iteration in range(1, iterations + 1):
        previous = vector
        temporary = vector + affine_correction
        affine = project_affine(temporary)
        affine_correction = temporary - affine
        temporary = affine + psd_correction
        vector, _, _ = project_psd(temporary, local_data, offsets)
        psd_correction = temporary - vector

        if iteration <= 10 or iteration % 100 == 0:
            affine_residual = (
                la.norm(system @ vector - shifted_right) / la.norm(right)
            )
            _, minimum, negative = project_psd(vector, local_data, offsets)
            step = la.norm(vector - previous) / max(la.norm(vector), 1e-30)
            score = max(affine_residual, negative)
            if best is None or score < best[0]:
                best = (score, iteration, affine_residual, minimum, step)
            if iteration <= 10 or iteration % 1000 == 0:
                print("Dykstra", iteration, "affine/min/negative/step:",
                      affine_residual, minimum, negative, step)
            if affine_residual < tolerance and negative < tolerance:
                print("Dykstra feasible at", iteration)
                return vector + shift, best
    print("Dykstra best:", best)
    return vector + shift, best


def one_site_marginal(core):
    """Return dense rho_1 and its selected-diagram coefficients."""
    traces = np.asarray([
        3.0 ** permutation_cycles(permutation)
        for permutation in BRIDGE.SELECTED_PERMUTATIONS
    ])
    coefficients = np.einsum("abc,b,c->a", core, traces, traces)
    rho = np.zeros((3 ** 5, 3 ** 5))
    for coefficient, permutation in zip(
            coefficients, BRIDGE.SELECTED_PERMUTATIONS):
        operator = BRIDGE.permutation_operator(permutation)
        for (row, column), value in operator.items():
            rho[row, column] += coefficient * float(value)
    rho = (rho + rho.T) / 2
    return rho, coefficients


def main():
    coordinates, _ = CODEC.read_certificate(REALIGN.DEFAULT_CERTIFICATE)
    source_trace, _ = REALIGN.source_trace_and_purity(coordinates)
    core = REALIGN.diagram_core(coordinates)
    rho, coefficients = one_site_marginal(core)
    eigenvalues = la.eigvalsh(rho)
    print("source/local trace:", source_trace, np.trace(rho))
    print("local Hermiticity residual:", la.norm(rho - rho.T))
    print("local spectrum min/max/rank/purity:",
          eigenvalues[0], eigenvalues[-1],
          int(np.sum(eigenvalues > 1e-11)), np.trace(rho @ rho))
    print("local diagram coefficient norm/max:",
          la.norm(coefficients), np.max(np.abs(coefficients)))
    print("twenty largest local eigenvalues:", eigenvalues[-20:][::-1])

    permutations5, moments = target_moments(rho)
    assert len(permutations5) == len(moments) == 120
    print("target moment norm/range:", la.norm(moments),
          np.min(moments), np.max(moments))
    system, right, local_data, offsets = extension_affine_system(moments)
    inspect_affine_extension(system, right, local_data, offsets)
    extension, best = dykstra_psd_affine(
        system, right, local_data, offsets, floor=5e-5
    )
    affine_residual = la.norm(system @ extension - right) / la.norm(right)
    _, minimum, negative = project_psd(extension, local_data, offsets)
    print("final local extension affine/min/negative:",
          affine_residual, minimum, negative)


if __name__ == "__main__":
    main()
