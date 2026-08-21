#!/usr/bin/env python3
"""Test a finite S4 group-algebra certificate for the shadow inequality.

The square of a decomposable bivector has global Young symmetry [2,2].
This script decomposes each local four-replica permutation action into
the four S4 irreducibles allowed in qutrit dimension and checks the
compression of

    9 sum_i (12)(34)_i
      - 2 ((12)(34)_0(12)(34)_1
           + (12)(34)_0(12)(34)_2
           + (12)(34)_1(12)(34)_2)

to the fixed [2,2] tableau line.  Positivity would prove the candidate
quadratic Pluecker-shadow inequality by a pure group-algebra argument.
Negative blocks diagnose the extra realizability information required.
"""

from __future__ import annotations

import itertools

import numpy as np


Permutation = tuple[int, int, int, int]


def compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(4))


def inverse(permutation: Permutation) -> Permutation:
    out = [0] * 4
    for index, image in enumerate(permutation):
        out[image] = index
    return tuple(out)  # type: ignore[return-value]


def parity(permutation: Permutation) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inversions & 1 else 1


PERMUTATIONS = tuple(itertools.permutations(range(4)))
IDENTITY = (0, 1, 2, 3)


def transposition(i: int, j: int) -> Permutation:
    out = list(IDENTITY)
    out[i], out[j] = out[j], out[i]
    return tuple(out)  # type: ignore[return-value]


def permutation_matrix(permutation: Permutation) -> np.ndarray:
    matrix = np.zeros((4, 4))
    for index, image in enumerate(permutation):
        matrix[image, index] = 1
    return matrix


def standard_basis() -> np.ndarray:
    vectors = np.array(
        [
            [1, -1, 0, 0],
            [0, 1, -1, 0],
            [0, 0, 1, -1],
        ],
        dtype=float,
    ).T
    return np.linalg.qr(vectors)[0]


PAIRINGS = (
    frozenset((frozenset((0, 1)), frozenset((2, 3)))),
    frozenset((frozenset((0, 2)), frozenset((1, 3)))),
    frozenset((frozenset((0, 3)), frozenset((1, 2)))),
)


def act_pairing(
    permutation: Permutation,
    pairing: frozenset[frozenset[int]],
) -> frozenset[frozenset[int]]:
    return frozenset(
        frozenset(permutation[index] for index in pair)
        for pair in pairing
    )


def pairing_matrix(permutation: Permutation) -> np.ndarray:
    matrix = np.zeros((3, 3))
    for index, pairing in enumerate(PAIRINGS):
        image = act_pairing(permutation, pairing)
        matrix[PAIRINGS.index(image), index] = 1
    return matrix


STANDARD_BASIS = standard_basis()
PAIRING_BASIS = np.linalg.qr(
    np.array([[1, -1, 0], [0, 1, -1]], dtype=float).T
)[0]


def representation(name: str, permutation: Permutation) -> np.ndarray:
    if name == "4":
        return np.ones((1, 1))
    if name == "31":
        full = permutation_matrix(permutation)
        return STANDARD_BASIS.T @ full @ STANDARD_BASIS
    if name == "211":
        full = permutation_matrix(permutation)
        return parity(permutation) * (
            STANDARD_BASIS.T @ full @ STANDARD_BASIS
        )
    if name == "22":
        full = pairing_matrix(permutation)
        return PAIRING_BASIS.T @ full @ PAIRING_BASIS
    raise ValueError(name)


IRREPS = ("4", "31", "22", "211")


def tensor_representation(
    names: tuple[str, str, str, str],
    permutation: Permutation,
) -> np.ndarray:
    result = np.ones((1, 1))
    for name in names:
        result = np.kron(result, representation(name, permutation))
    return result


def local_action(
    names: tuple[str, str, str, str],
    site: int,
    permutation: Permutation,
) -> np.ndarray:
    result = np.ones((1, 1))
    for index, name in enumerate(names):
        factor = (
            representation(name, permutation)
            if index == site
            else np.eye(representation(name, IDENTITY).shape[0])
        )
        result = np.kron(result, factor)
    return result


def analyze(names: tuple[str, str, str, str]) -> tuple[int, float]:
    dimension = tensor_representation(names, IDENTITY).shape[0]
    identity = np.eye(dimension)
    swap12 = transposition(0, 1)
    swap34 = transposition(2, 3)
    pair_swap = compose(transposition(0, 2), transposition(1, 3))
    p_pair = (
        (identity - tensor_representation(names, swap12))
        @ (identity - tensor_representation(names, swap34))
        @ (identity + tensor_representation(names, pair_swap))
        / 8
    )
    p_sign = sum(
        parity(permutation)
        * tensor_representation(names, permutation)
        for permutation in PERMUTATIONS
    ) / 24
    projector = (p_pair - p_sign + (p_pair - p_sign).T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(projector)
    basis = eigenvectors[:, eigenvalues > 0.5]
    if basis.shape[1] == 0:
        return 0, float("inf")

    double_swap = compose(swap12, swap34)
    local = [
        local_action(names, site, double_swap) for site in range(4)
    ]
    operator = 9 * sum(local)
    operator -= 2 * (
        local[0] @ local[1]
        + local[0] @ local[2]
        + local[1] @ local[2]
    )
    compressed = basis.T @ operator @ basis
    compressed = (compressed + compressed.T) / 2
    return basis.shape[1], float(np.linalg.eigvalsh(compressed)[0])


def main() -> None:
    worst = (float("inf"), None, None)
    for names in itertools.product(IRREPS, repeat=4):
        rank, least = analyze(names)
        if rank and least < worst[0]:
            worst = (least, names, rank)
        if rank and least < -1e-9:
            print("negative", names, "rank", rank, "least", least)
    print("worst", worst)


if __name__ == "__main__":
    main()
