#!/usr/bin/env python3
"""Exact rational S7 -> S5 branch embeddings for the DTH marginal.

This verifier constructs integral polytabloid models for all eight local S7
modules, obtains their exact adjacent-transposition matrices, and builds every
two-box restriction intertwiner by a Reynolds projection.  The multiplicity
space is then split by the swap of the deleted pair into horizontal and
vertical channels.  No algebraic orthonormalization is used.

SymPy is used for small exact Gram calculations; all representation and
Reynolds matrices are integral NumPy arrays.
"""

from functools import lru_cache
from itertools import permutations, product
from math import gcd
from pathlib import Path
import importlib.util
import sys

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_dth_level2_s7_census as census

K_PATH = HERE / "agent_dth_exact_k_coordinates.py"
SPEC = importlib.util.spec_from_file_location("dth_exact_k_branch", K_PATH)
K5 = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(K5)


S7 = tuple(census.partitions(7, max_parts=3))
S5 = ((5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1))


def removable_cells(shape):
    return tuple(
        (row, shape[row] - 1) for row in range(len(shape))
        if row + 1 == len(shape) or shape[row] > shape[row + 1]
    )


@lru_cache(None)
def standard_tableaux(shape):
    shape = tuple(shape)
    if not shape:
        return ((),)
    output = []
    for cell in removable_cells(shape):
        row, _ = cell
        smaller = list(shape)
        smaller[row] -= 1
        if not smaller[row]:
            smaller.pop(row)
        for tableau in standard_tableaux(tuple(smaller)):
            output.append(tuple(tableau) + (cell,))
    return tuple(sorted(output))


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def polytabloid(shape, tableau):
    columns = []
    for column in range(max(shape)):
        columns.append(tuple(
            label for label, (row, selected_column) in enumerate(tableau)
            if selected_column == column
        ))
    base_word = tuple(row for row, _ in tableau)
    output = {}
    for images in product(*(tuple(permutations(column)) for column in columns)):
        permutation = list(range(sum(shape)))
        sign = 1
        for column, image in zip(columns, images):
            sign *= permutation_sign(tuple(column.index(value) for value in image))
            for old, new in zip(column, image):
                permutation[old] = new
        # The permutation-operator convention is row[i] = column[p[i]].
        inverse = [0] * len(permutation)
        for source, target in enumerate(permutation):
            inverse[target] = source
        word = tuple(base_word[inverse[index]] for index in range(len(inverse)))
        output[word] = output.get(word, 0) + sign
    return {key: value for key, value in output.items() if value}


@lru_cache(None)
def local_basis(shape_index):
    shape = S7[shape_index]
    return tuple(
        polytabloid(shape, tableau)
        for tableau in standard_tableaux(shape)
    )


def inner(left, right):
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(key, 0) for key, value in left.items())


def apply_adjacent(vector, generator):
    output = {}
    for word, value in vector.items():
        changed = list(word)
        changed[generator], changed[generator + 1] = (
            changed[generator + 1], changed[generator]
        )
        changed = tuple(changed)
        output[changed] = output.get(changed, 0) + value
    return output


@lru_cache(None)
def local_gram(shape_index):
    basis = local_basis(shape_index)
    return sp.Matrix([
        [inner(left, right) for right in basis] for left in basis
    ])


@lru_cache(None)
def adjacent_representation(shape_index, generator):
    basis = local_basis(shape_index)
    restriction = sp.Matrix([
        [inner(left, apply_adjacent(right, generator)) for right in basis]
        for left in basis
    ])
    representation = local_gram(shape_index).inv() * restriction
    assert all(value.q == 1 for value in representation)
    return np.asarray(representation.tolist(), dtype=np.int64)


def representation_from_adjacent(adjacent, permutation):
    current = list(range(len(permutation)))
    output = np.eye(adjacent[0].shape[0], dtype=np.int64)
    for position in range(len(permutation)):
        location = current.index(permutation[position])
        while location > position:
            generator = location - 1
            current[generator], current[generator + 1] = (
                current[generator + 1], current[generator]
            )
            output = output @ adjacent[generator]
            location -= 1
    assert tuple(current) == tuple(permutation)
    return output


@lru_cache(None)
def s7_representation(shape_index, permutation):
    adjacent = tuple(
        adjacent_representation(shape_index, generator)
        for generator in range(6)
    )
    return representation_from_adjacent(adjacent, tuple(permutation))


@lru_cache(None)
def s5_representation(shape_index, permutation):
    # The pre-existing physical-word module records right actions, hence its
    # coordinate matrices are an antihomomorphism in image-form permutation
    # notation.  Inverting the argument gives the homomorphic convention used
    # by ``representation_from_adjacent`` above.  Adjacent generators are
    # unchanged by this conversion.
    return np.asarray(
        K5.local_representation(
            shape_index, inverse(tuple(permutation))
        ).tolist(),
        dtype=np.int64,
    )


def inverse(permutation):
    output = [0] * len(permutation)
    for source, target in enumerate(permutation):
        output[target] = source
    return tuple(output)


def primitive_columns(matrix, expected):
    basis = []
    rank = 0
    for column in matrix.T:
        if not np.any(column):
            continue
        trial = np.asarray(basis + [column.tolist()], dtype=np.float64).T
        new_rank = np.linalg.matrix_rank(trial, tol=1e-8)
        if new_rank > rank:
            values = [int(value) for value in column]
            divisor = 0
            for value in values:
                divisor = gcd(divisor, abs(value))
            basis.append([value // max(1, divisor) for value in values])
            rank = new_rank
            if rank == expected:
                break
    assert len(basis) == expected
    return tuple(np.asarray(value, dtype=np.int64) for value in basis)


@lru_cache(None)
def branch_intertwiners(source_index, target_index):
    expected_types = census.two_box_strip_types(
        S7[source_index], S5[target_index]
    )
    if not expected_types:
        return {}
    source_dimension = census.specht_dimension(S7[source_index])
    target_dimension = census.specht_dimension(S5[target_index])
    reynolds = np.zeros(
        (source_dimension * target_dimension,) * 2, dtype=np.int64
    )
    for permutation in permutations(range(5)):
        lifted = tuple(permutation) + (5, 6)
        source = s7_representation(source_index, lifted)
        target_inverse = s5_representation(target_index, inverse(permutation))
        reynolds += np.kron(target_inverse.T, source)
    basis = primitive_columns(reynolds, len(expected_types))
    swap = adjacent_representation(source_index, 5)
    output = {}
    for label, sign in (("H", 1), ("V", -1)):
        if label not in expected_types:
            continue
        selected = None
        for vector in basis:
            matrix = vector.reshape(
                source_dimension, target_dimension, order="F"
            )
            projected = matrix + sign * swap @ matrix
            if np.any(projected):
                values = [int(value) for value in projected.ravel()]
                divisor = 0
                for value in values:
                    divisor = gcd(divisor, abs(value))
                selected = projected // max(1, divisor)
                break
        assert selected is not None
        output[label] = selected
    assert set(output) == set(expected_types)
    return output


def normalization(source_index, target_index, branch):
    source_gram = local_gram(source_index)
    target_gram = K5.local_gram(target_index)
    matrix = sp.Matrix(branch.tolist())
    pulled = matrix.T * source_gram * matrix
    scalar_matrix = target_gram.inv() * pulled
    scalar = sp.trace(scalar_matrix) / scalar_matrix.rows
    assert pulled == scalar * target_gram
    assert scalar > 0
    return scalar


def main():
    rows = []
    for source_index in range(8):
        for target_index in range(5):
            branches = branch_intertwiners(source_index, target_index)
            if not branches:
                continue
            for label, branch in sorted(branches.items()):
                scalar = normalization(
                    source_index, target_index, branch
                )
                # Exact covariance and deleted-pair parity.
                for generator in range(4):
                    assert np.array_equal(
                        adjacent_representation(source_index, generator) @ branch,
                        branch @ s5_representation(
                            target_index,
                            tuple(
                                (generator + 1 if value == generator else
                                 generator if value == generator + 1 else value)
                                for value in range(5)
                            ),
                        ),
                    )
                sign = 1 if label == "H" else -1
                assert np.array_equal(
                    adjacent_representation(source_index, 5) @ branch,
                    sign * branch,
                )
                rows.append((source_index, target_index, label,
                             int(scalar.p), int(scalar.q)))

    assert len(rows) == 30
    assert sum(label == "H" for _, _, label, _, _ in rows) == 18
    assert sum(label == "V" for _, _, label, _, _ in rows) == 12
    print("exact rational S7-to-S5 branch audit passed")
    print("channels / horizontal / vertical:", len(rows), 18, 12)
    print("normalization rows:")
    for row in rows:
        print(" ", row)


if __name__ == "__main__":
    main()
