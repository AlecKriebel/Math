#!/usr/bin/env python3
"""Numerical local S7 crossing for the prolonged DTH support constraint.

Partial transpose of the anchored bivector changes one local seven-replica
module from ``3^tensor7`` to ``conj(3)^tensor2 tensor 3^tensor5``.  This
script constructs the complete local crossing on invariant multiplicity
coordinates.  The holomorphic side has eight S7 shapes and local commutant
dimension 2,761.  The mixed side has ten irreducible types and the same
commutant dimension.

The construction uses sparse partial-transposed permutation diagrams and
the finite-group Fourier formula for Young-orthogonal matrix units.  It never
forms a 2187 by 2187 permutation matrix.  Output is numerical discovery data;
an eventual theorem requires the exact polytabloid/diagram reconstruction.
"""

from argparse import ArgumentParser
from collections import defaultdict, deque
from itertools import product
from pathlib import Path
import math
import sys


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "discovery"
sys.path.insert(0, str(DISCOVERY))

import numpy as np
import scipy.linalg as la

import agent_dth_level2_444_extension as YOUNG
import agent_dth_level2_joint_extension as LEVEL2


D = 3
NREP = 7
TRANSPOSED = frozenset((0, 1))
WORDS = tuple(product(range(D), repeat=NREP))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}

HOL_SHAPES = tuple(YOUNG.S7)
HOL_MULTS = tuple(len(YOUNG.standard_tableaux(shape)) for shape in HOL_SHAPES)
HOL_CARRIER_DIMS = tuple(LEVEL2.S7_CARRIER_DIMS)

MIXED_WEIGHTS = (
    (5, 0, -2), (5, -1, -1), (4, 1, -2), (4, 0, -1),
    (3, 2, -2), (3, 1, -1), (3, 0, 0), (2, 2, -1),
    (2, 1, 0), (1, 1, 1),
)
MIXED_MULTS = (1, 1, 4, 10, 5, 24, 20, 15, 36, 11)
MIXED_CARRIER_DIMS = (81, 28, 64, 35, 35, 27, 10, 10, 8, 1)

DEFAULT_CACHE = DISCOVERY / "dth_level2_local_gammaA_crossing.npz"


def mixed_weight(word):
    counts = [0, 0, 0]
    for position in range(2, NREP):
        counts[word[position]] += 1
    for position in range(2):
        counts[word[position]] -= 1
    return tuple(counts)


WEIGHT_INDICES = defaultdict(list)
for _index, _word in enumerate(WORDS):
    WEIGHT_INDICES[mixed_weight(_word)].append(_index)


def raised_word(word, simple_root):
    low = simple_root + 1
    high = simple_root
    for position, value in enumerate(word):
        if position < 2:
            if value == high:
                new = list(word)
                new[position] = low
                yield tuple(new), -1.0
        elif value == low:
            new = list(word)
            new[position] = high
            yield tuple(new), 1.0


def raising_matrix(indices, simple_root):
    rows = {}
    terms = []
    for column, index in enumerate(indices):
        for word, coefficient in raised_word(WORDS[index], simple_root):
            if word not in rows:
                rows[word] = len(rows)
            terms.append((rows[word], column, coefficient))
    output = np.zeros((len(rows), len(indices)))
    for row, column, coefficient in terms:
        output[row, column] += coefficient
    return output


def mixed_highest_weight_bases():
    output = []
    for weight, expected in zip(MIXED_WEIGHTS, MIXED_MULTS):
        indices = np.asarray(WEIGHT_INDICES[weight], dtype=int)
        raising = np.vstack((
            raising_matrix(indices, 0), raising_matrix(indices, 1)
        ))
        kernel = la.null_space(raising, rcond=1e-12)
        assert kernel.shape == (len(indices), expected), (
            weight, kernel.shape, expected
        )
        assert la.norm(kernel.T @ kernel - np.eye(expected)) < 2e-12
        lookup = np.full(len(WORDS), -1, dtype=np.int32)
        lookup[indices] = np.arange(len(indices), dtype=np.int32)
        output.append((indices, lookup, kernel))
    return tuple(output)


def adjacent_bfs():
    """All S7 permutations with one parent/adjacent-generator edge."""
    identity = tuple(range(NREP))
    permutations = [identity]
    parent = [-1]
    generator = [-1]
    index = {identity: 0}
    cursor = 0
    while cursor < len(permutations):
        permutation = permutations[cursor]
        for adjacent in range(NREP - 1):
            child = list(permutation)
            child[adjacent], child[adjacent + 1] = (
                child[adjacent + 1], child[adjacent]
            )
            child = tuple(child)
            if child not in index:
                index[child] = len(permutations)
                permutations.append(child)
                parent.append(cursor)
                generator.append(adjacent)
        cursor += 1
    assert len(permutations) == math.factorial(NREP)
    return tuple(permutations), tuple(parent), tuple(generator)


def holomorphic_fourier(permutations, parent, generator):
    dimension = sum(multiplicity ** 2 for multiplicity in HOL_MULTS)
    output = np.empty((len(permutations), dimension))
    offset = 0
    for shape, multiplicity, carrier in zip(
        HOL_SHAPES, HOL_MULTS, HOL_CARRIER_DIMS
    ):
        matrices = np.empty((len(permutations), multiplicity, multiplicity))
        matrices[0] = np.eye(multiplicity)
        adjacent = tuple(
            YOUNG.adjacent_matrix(shape, value)
            for value in range(NREP - 1)
        )
        for index in range(1, len(permutations)):
            matrices[index] = (
                matrices[parent[index]] @ adjacent[generator[index]]
            )
        scale = multiplicity / (math.factorial(NREP) * carrier)
        width = multiplicity ** 2
        output[:, offset:offset + width] = (
            scale * matrices.reshape(len(permutations), width)
        )
        offset += width
    assert offset == dimension
    return output


def partial_transpose_outputs(permutation, input_word):
    """Nonzero output words of Gamma_(0,1)(P_permutation)."""
    parent = list(range(NREP))

    def find(value):
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def union(left, right):
        left = find(left)
        right = find(right)
        if left != right:
            parent[right] = left

    assignments = []
    for old in range(NREP):
        position = permutation[old]
        left_is_input = position in TRANSPOSED
        right_is_output = old in TRANSPOSED
        if left_is_input and not right_is_output:
            if input_word[position] != input_word[old]:
                return ()
        elif not left_is_input and not right_is_output:
            assignments.append((position, input_word[old]))
        elif left_is_input and right_is_output:
            assignments.append((old, input_word[position]))
        else:
            union(position, old)

    values = {}
    for position, value in assignments:
        root = find(position)
        if root in values and values[root] != value:
            return ()
        values[root] = value
    roots = sorted({find(position) for position in range(NREP)})
    free = tuple(root for root in roots if root not in values)
    output = []
    for choices in product(range(D), repeat=len(free)):
        assigned = dict(values)
        assigned.update(zip(free, choices))
        output.append(tuple(assigned[find(position)]
                            for position in range(NREP)))
    return tuple(output)


def mixed_restrictions(permutations, bases, report=100):
    dimension = sum(multiplicity ** 2 for multiplicity in MIXED_MULTS)
    output = np.empty((dimension, len(permutations)))
    for column, permutation in enumerate(permutations):
        offset = 0
        for indices, lookup, basis in bases:
            acted = np.zeros_like(basis)
            for local_column, word_index in enumerate(indices):
                for output_word in partial_transpose_outputs(
                    permutation, WORDS[word_index]
                ):
                    row = lookup[WORD_INDEX[output_word]]
                    assert row >= 0
                    acted[row] += basis[local_column]
            block = basis.T @ acted
            width = block.size
            output[offset:offset + width, column] = block.reshape(-1)
            offset += width
        assert offset == dimension
        if report and column % report == 0:
            print("mixed crossed permutation", column, "/", len(permutations),
                  flush=True)
    return output


def audit_crossing(crossing):
    mixed_metric = np.concatenate([
        np.full(multiplicity ** 2, carrier)
        for multiplicity, carrier in zip(MIXED_MULTS, MIXED_CARRIER_DIMS)
    ])
    holomorphic_metric = np.concatenate([
        np.full(multiplicity ** 2, 1.0 / carrier)
        for multiplicity, carrier in zip(HOL_MULTS, HOL_CARRIER_DIMS)
    ])
    gram = crossing.T @ (mixed_metric[:, None] * crossing)
    metric_error = la.norm(gram - np.diag(holomorphic_metric))
    metric_max = np.max(np.abs(gram - np.diag(holomorphic_metric)))

    mixed_trace = np.zeros(crossing.shape[0])
    offset = 0
    for multiplicity, carrier in zip(MIXED_MULTS, MIXED_CARRIER_DIMS):
        for index in range(multiplicity):
            mixed_trace[offset + index * multiplicity + index] = carrier
        offset += multiplicity ** 2
    expected_trace = []
    for multiplicity in HOL_MULTS:
        for row in range(multiplicity):
            for column in range(multiplicity):
                expected_trace.append(float(row == column))
    trace_error = np.max(np.abs(
        mixed_trace @ crossing - np.asarray(expected_trace)
    ))
    print("crossing weighted-isometry Frobenius/max error:",
          metric_error, metric_max)
    print("crossing trace error:", trace_error)
    assert metric_error < 2e-9
    assert trace_error < 2e-9
    return metric_error, metric_max, trace_error


def census():
    assert sum(value ** 2 for value in HOL_MULTS) == 2761
    assert sum(value ** 2 for value in MIXED_MULTS) == 2761
    assert sum(a * b for a, b in zip(HOL_MULTS, HOL_CARRIER_DIMS)) == D ** NREP
    assert sum(a * b for a, b in zip(MIXED_MULTS, MIXED_CARRIER_DIMS)) == D ** NREP
    print("holomorphic shapes/multiplicities/carriers:")
    print(tuple(zip(HOL_SHAPES, HOL_MULTS, HOL_CARRIER_DIMS)))
    print("mixed weights/multiplicities/carriers:")
    print(tuple(zip(MIXED_WEIGHTS, MIXED_MULTS, MIXED_CARRIER_DIMS)))
    print("local dimensions/commutants:", D ** NREP, 2761)


def main():
    parser = ArgumentParser()
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--census-only", action="store_true")
    parser.add_argument("--report", type=int, default=100)
    args = parser.parse_args()
    census()
    bases = mixed_highest_weight_bases()
    if args.census_only:
        return
    permutations, parent, generator = adjacent_bfs()
    print("building holomorphic Fourier table", flush=True)
    fourier = holomorphic_fourier(permutations, parent, generator)
    print("building sparse mixed restriction table", flush=True)
    mixed = mixed_restrictions(permutations, bases, report=args.report)
    print("contracting local crossing", flush=True)
    crossing = mixed @ fourier
    diagnostics = audit_crossing(crossing)
    np.savez_compressed(
        args.cache,
        crossing=crossing,
        hol_shapes=np.asarray([
            tuple(shape) + (0,) * (3 - len(shape)) for shape in HOL_SHAPES
        ], dtype=np.int16),
        hol_multiplicities=np.asarray(HOL_MULTS, dtype=np.int16),
        hol_carrier_dimensions=np.asarray(HOL_CARRIER_DIMS, dtype=np.int16),
        mixed_weights=np.asarray(MIXED_WEIGHTS, dtype=np.int16),
        mixed_multiplicities=np.asarray(MIXED_MULTS, dtype=np.int16),
        mixed_carrier_dimensions=np.asarray(
            MIXED_CARRIER_DIMS, dtype=np.int16
        ),
        diagnostics=np.asarray(diagnostics),
    )
    print("saved local crossing:", args.cache)


if __name__ == "__main__":
    main()
