#!/usr/bin/env python3
"""Probe the exact structural face behind Gamma_5-PPT feasibility.

The pair antisymmetries, pair exchange, and first Pluecker equation commute
with final-slot partial transpose.  They define an exact target support of
dimension 772.  This script crosses the holomorphic Omega exposing operator
``C_Omega^* C_Omega`` through Gamma_5 and compresses it to that support.

The calculation is numerical discovery.  The representation projectors and
the crossing have independent exact implementations, making any clean rank
pattern a direct target for exact reconstruction.
"""

from __future__ import annotations

import itertools

import numpy as np
import scipy.linalg as la

import agent_dth_invariant_crossing as hol_data
import agent_dth_last_invariant_crossing as last_data


PERMUTATIONS4 = tuple(itertools.permutations(range(4)))
PERMUTATION_INDEX = {p: i for i, p in enumerate(PERMUTATIONS4)}


def parity(permutation):
    return -1 if sum(permutation[i] > permutation[j]
                     for i in range(len(permutation))
                     for j in range(i + 1, len(permutation))) % 2 else 1


def kron3(left, middle, right):
    return np.kron(np.kron(left, middle), right)


def epsilon(i, j, k):
    if len({i, j, k}) < 3:
        return 0
    return parity((i, j, k))


def omega_local(basis, first):
    retained = (2, 3) if first == 0 else (0, 1)
    raw = np.zeros((9, hol_data.LOCAL_DIM), dtype=float)
    for column, word in enumerate(hol_data.WORDS):
        coefficient = epsilon(word[4], word[first], word[first + 1])
        if coefficient:
            raw[3 * word[retained[0]] + word[retained[1]], column] = coefficient
    return raw @ basis


def block_indices(ranges, shapes):
    grids = [ranges[shape] for shape in shapes]
    return (grids[0][:, None, None, :, None, None],
            grids[1][None, :, None, None, :, None],
            grids[2][None, None, :, None, None, :])


def put_block(tensor, ranges, shapes, matrix, dimensions):
    tensor[block_indices(ranges, shapes)] = matrix.reshape(
        (*dimensions, *dimensions)
    )


def get_block(tensor, ranges, shapes, dimensions):
    size = int(np.prod(dimensions))
    return tensor[block_indices(ranges, shapes)].reshape(size, size)


def crossing_apply(local, tensor):
    output = np.tensordot(local, tensor, axes=(1, 0))
    output = np.tensordot(local, output, axes=(1, 1)).transpose(1, 0, 2)
    return np.tensordot(local, output, axes=(1, 2)).transpose(1, 2, 0)


def target_representations(target_bases):
    output = []
    for basis in target_bases:
        output.append([
            basis.T @ hol_data.permutation_matrix(tuple(p) + (4,)) @ basis
            for p in PERMUTATIONS4
        ])
    return output


def pair_pluecker_basis(representations, shapes, tolerance=1e-8):
    dimensions = tuple(last_data.LAST_MULTS[shape] for shape in shapes)
    size = int(np.prod(dimensions))
    identity = np.eye(size)

    def global_representation(index):
        return kron3(*(representations[shape][index] for shape in shapes))

    a = PERMUTATION_INDEX[(1, 0, 2, 3)]
    b = PERMUTATION_INDEX[(0, 1, 3, 2)]
    c = PERMUTATION_INDEX[(2, 3, 0, 1)]
    projector = ((identity - global_representation(a)) / 2
                 @ (identity - global_representation(b)) / 2
                 @ (identity + global_representation(c)) / 2)
    antisymmetrizer = sum(
        parity(permutation) * global_representation(index) / 24
        for index, permutation in enumerate(PERMUTATIONS4)
    )
    projector = projector @ (identity - antisymmetrizer)
    projector = (projector + projector.T) / 2
    values, vectors = la.eigh(projector)
    assert np.max(np.minimum(abs(values), abs(values - 1))) < 2e-10
    return vectors[:, values > 1 - tolerance]


def crossed_omega_exposer():
    local5, hol_ranges, target_ranges = last_data.normalized_local_crossing(
        verbose=False
    )
    holomorphic = hol_data.hol_highest_weight_bases()
    omega = tuple((omega_local(basis, 0), omega_local(basis, 2))
                  for basis in holomorphic)
    tensor = np.zeros((103, 103, 103), dtype=float)
    for shapes in itertools.product(range(len(hol_data.HOL_MULTS)), repeat=3):
        dimensions = tuple(hol_data.HOL_MULTS[shape] for shape in shapes)
        first = kron3(*(omega[shape][0] for shape in shapes))
        second = kron3(*(omega[shape][1] for shape in shapes))
        combined = first + second
        matrix = combined.T @ combined
        carrier = np.prod([
            hol_data.HOL_CARRIER_DIMS[shape] for shape in shapes
        ])
        put_block(tensor, hol_ranges, shapes,
                  np.sqrt(carrier) * matrix, dimensions)
    return crossing_apply(local5, tensor), target_ranges


def main():
    crossed, target_ranges = crossed_omega_exposer()
    target = last_data.orthonormal_target_bases()
    representations = target_representations(target)
    support_total = support_active = 0
    positive_total = positive_active = negative_total = 0
    nonzero = []
    for shapes in itertools.product(range(len(last_data.LAST_MULTS)), repeat=3):
        dimensions = tuple(last_data.LAST_MULTS[shape] for shape in shapes)
        basis = pair_pluecker_basis(representations, shapes)
        support_total += basis.shape[1]
        support_active += bool(basis.shape[1])
        if not basis.shape[1]:
            continue
        matrix = get_block(crossed, target_ranges, shapes, dimensions)
        compressed = basis.T @ ((matrix + matrix.T) / 2) @ basis
        values = la.eigvalsh(compressed)
        positive = int(np.sum(values > 1e-8))
        negative = int(np.sum(values < -1e-8))
        positive_total += positive
        positive_active += bool(positive)
        negative_total += negative
        if positive or negative:
            nonzero.append((shapes, basis.shape[1], positive, negative,
                            float(values[0]), float(values[-1])))

    print("Gamma5 pair/Pluecker support dimension/active:",
          support_total, support_active)
    print("crossed Omega compressed positive/negative ranks:",
          positive_total, negative_total,
          "positive blocks", positive_active)
    print("candidate kernel dimension:", support_total - positive_total)
    print("nonzero compressed blocks:")
    for shapes, size, positive, negative, low, high in nonzero:
        print(" ", "/".join(last_data.LAST_NAMES[s] for s in shapes),
              "support", size, "rank+/-", positive, negative,
              "range", low, high)


if __name__ == "__main__":
    main()
