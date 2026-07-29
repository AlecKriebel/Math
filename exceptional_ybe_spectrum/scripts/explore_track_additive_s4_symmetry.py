#!/usr/bin/env python3
"""Reproducible numerical probe of an S4-equivariant (2,3,2) ansatz.

This is a falsifier/discovery experiment, not a proof.  The local factors
are the two- and three-dimensional irreducible real representations of S4.
The rank-six equivariant involutions have a central branch and a
four-parameter branch.  The latter is sampled with deterministic BFGS
starts.
"""

from __future__ import annotations

import itertools
import platform
from datetime import datetime, timezone

import numpy as np
import scipy
from scipy.optimize import minimize


SEED = 7
STARTS = 20


def permutation_parity(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inversions % 2 else 1


def sum_zero_basis(dimension):
    spanning = np.zeros((dimension, dimension - 1))
    for column in range(dimension - 1):
        spanning[column, column] = 1
        spanning[-1, column] = -1
    return np.linalg.qr(spanning)[0]


def build_representations():
    permutations = list(itertools.permutations(range(4)))
    basis_four = sum_zero_basis(4)
    basis_three = sum_zero_basis(3)
    matchings = [
        frozenset((frozenset((0, 1)), frozenset((2, 3)))),
        frozenset((frozenset((0, 2)), frozenset((1, 3)))),
        frozenset((frozenset((0, 3)), frozenset((1, 2)))),
    ]

    representations = []
    standard_projector = np.zeros((12, 12))
    twisted_projector = np.zeros((12, 12))

    for permutation in permutations:
        permutation_four = np.zeros((4, 4))
        for index in range(4):
            permutation_four[permutation[index], index] = 1
        representation_three = (
            basis_four.T @ permutation_four @ basis_four
        )

        permutation_three = np.zeros((3, 3))
        for index, matching in enumerate(matchings):
            image = frozenset(
                frozenset(permutation[element] for element in pair)
                for pair in matching
            )
            permutation_three[matchings.index(image), index] = 1
        representation_two = (
            basis_three.T @ permutation_three @ basis_three
        )

        representation = np.kron(
            np.kron(representation_two, representation_three),
            representation_two,
        )
        representations.append(representation)

        character = sum(
            permutation[index] == index for index in range(4)
        ) - 1
        standard_projector += character * representation / 8
        twisted_projector += (
            permutation_parity(permutation)
            * character
            * representation
            / 8
        )

    return representations, standard_projector, twisted_projector


def commutant_average(representations, matrix):
    return sum(
        representation @ matrix @ representation.T
        for representation in representations
    ) / len(representations)


def multiplicity_paulis(representations, projector, rng):
    real_random = rng.normal(size=(12, 12))
    real_random = (real_random + real_random.T) / 2
    splitter = (
        projector
        @ commutant_average(representations, real_random)
        @ projector
    )
    _, eigenvectors = np.linalg.eigh(splitter)
    lower = eigenvectors[:, :3] @ eigenvectors[:, :3].T
    upper = eigenvectors[:, 3:6] @ eigenvectors[:, 3:6].T
    pauli_z = upper - lower

    complex_random = (
        rng.normal(size=(12, 12))
        + 1j * rng.normal(size=(12, 12))
    )
    complex_random = (complex_random + complex_random.conj().T) / 2
    averaged = (
        projector
        @ commutant_average(representations, complex_random)
        @ projector
    )
    intertwiner = upper @ averaged @ lower
    scale = np.real(np.trace(intertwiner @ intertwiner.conj().T) / 3)
    intertwiner /= np.sqrt(scale)
    pauli_x = intertwiner + intertwiner.conj().T
    pauli_y = -1j * (intertwiner - intertwiner.conj().T)

    errors = (
        np.linalg.norm(pauli_x @ pauli_x - projector),
        np.linalg.norm(pauli_y @ pauli_y - projector),
        np.linalg.norm(pauli_z @ pauli_z - projector),
        np.linalg.norm(pauli_x @ pauli_y + pauli_y @ pauli_x),
    )
    return (pauli_x, pauli_y, pauli_z), errors


def cubic_residual(involution):
    first = np.kron(involution, np.eye(6))
    second = np.kron(np.eye(6), involution)
    return (
        first @ second @ first
        - second @ first @ second
        - (first - second) / 3
    )


def main():
    print("started_utc:", datetime.now(timezone.utc).isoformat())
    print("python:", platform.python_version())
    print("platform:", platform.platform())
    print("numpy:", np.__version__)
    print("scipy:", scipy.__version__)
    print("seed:", SEED)
    print("starts:", STARTS)

    representations, standard, twisted = build_representations()
    print(
        "central_projector_errors:",
        np.linalg.norm(standard @ standard - standard),
        np.linalg.norm(twisted @ twisted - twisted),
        np.linalg.norm(standard @ twisted),
    )
    print("central_projector_traces:", np.trace(standard), np.trace(twisted))
    for label, projector in (("standard", standard), ("twisted", twisted)):
        involution = np.eye(12) - 2 * projector
        residual = cubic_residual(involution)
        print(
            f"central_{label}_residual:",
            np.linalg.norm(residual),
            np.max(np.abs(residual)),
        )

    rng = np.random.default_rng(SEED)
    standard_paulis, standard_errors = multiplicity_paulis(
        representations, standard, rng
    )
    twisted_paulis, twisted_errors = multiplicity_paulis(
        representations, twisted, rng
    )
    print("standard_pauli_errors:", *standard_errors)
    print("twisted_pauli_errors:", *twisted_errors)

    def involution(parameters):
        first_vector = parameters[:3] / np.linalg.norm(parameters[:3])
        second_vector = parameters[3:] / np.linalg.norm(parameters[3:])
        return sum(
            first_vector[index] * standard_paulis[index]
            + second_vector[index] * twisted_paulis[index]
            for index in range(3)
        )

    def objective(parameters):
        residual = cubic_residual(involution(parameters))
        return np.linalg.norm(residual) ** 2

    best = None
    for start in range(STARTS):
        initial = rng.normal(size=6)
        result = minimize(
            objective,
            initial,
            method="BFGS",
            options={"maxiter": 500, "gtol": 1e-10},
        )
        if best is None or result.fun < best.fun:
            best = result
        print(
            "start_result:",
            start,
            repr(float(result.fun)),
            result.success,
            result.nit,
        )

    assert best is not None
    first_vector = best.x[:3] / np.linalg.norm(best.x[:3])
    second_vector = best.x[3:] / np.linalg.norm(best.x[3:])
    print("best_objective:", repr(float(best.fun)))
    print("best_first_vector:", repr(first_vector.tolist()))
    print("best_second_vector:", repr(second_vector.tolist()))
    print(
        "interpretation: no zero was found; this is numerical evidence only."
    )
    print("finished_utc:", datetime.now(timezone.utc).isoformat())


if __name__ == "__main__":
    main()
