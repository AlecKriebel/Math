#!/usr/bin/env python3
"""Numerical local crossings for Gamma_z and Gamma_AA at DTH degree three.

The seven local replicas are ``A1=(0,1)``, ``A2=(2,3)``, ``A3=(4,5)``
and ``z=6``.  This script constructs the normalized local commutant crossing
for either remaining grouped PPT representative:

* ``gamma_z``: transpose replica ``6``;
* ``gamma_aa``: transpose replicas ``0,1,2,3``.

It shares the audited S7 Fourier layer with the existing Gamma_A crossing,
but constructs the appropriate mixed highest-weight spaces and sparse
partial-transposed diagrams.  The output format is identical to
``dth_level2_local_gammaA_crossing.npz`` and can therefore be passed
directly to ``agent_dth_level2_cross_candidate_orbits.py``.

This is floating-point discovery infrastructure.  Exact diagram audits live
in ``verification/verify_dth_level2_other_local_crossings.py``.
"""

from argparse import ArgumentParser
from collections import defaultdict
from itertools import product
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "discovery"
sys.path.insert(0, str(DISCOVERY))

import numpy as np
import scipy.linalg as la

import agent_dth_level2_local_crossing as BASE


D = BASE.D
NREP = BASE.NREP
WORDS = BASE.WORDS
WORD_INDEX = BASE.WORD_INDEX

CUTS = {
    "gamma_z": frozenset((6,)),
    "gamma_aa": frozenset((0, 1, 2, 3)),
    # Complement representative for Gamma_AA.  On a pair-symmetric source,
    # full transpose identifies Gamma_AA with Gamma_(A3,z), and pair
    # exchange identifies A3 with the anchored A1 used here.
    "gamma_az": frozenset((0, 1, 6)),
}

# Exact order is pinned by the independent census verifier.
MIXED_DATA = {
    "gamma_z": (
        ((6, 0, -1), 1, 63),
        ((5, 1, -1), 5, 60),
        ((5, 0, 0), 6, 21),
        ((4, 2, -1), 9, 42),
        ((4, 1, 0), 24, 24),
        ((3, 3, -1), 5, 15),
        ((3, 2, 0), 30, 15),
        ((3, 1, 1), 26, 6),
        ((2, 2, 1), 21, 3),
    ),
    "gamma_aa": (
        ((3, 0, -4), 1, 90),
        ((3, -1, -3), 3, 60),
        ((3, -2, -2), 2, 21),
        ((2, 1, -4), 2, 48),
        ((2, 0, -3), 12, 42),
        ((2, -1, -2), 18, 24),
        ((1, 1, -3), 9, 15),
        ((1, 0, -2), 33, 15),
        ((1, -1, -1), 24, 6),
        ((0, 0, -1), 23, 3),
    ),
    "gamma_az": (
        ((4, 0, -3), 1, 90),
        ((4, -1, -2), 2, 48),
        ((3, 1, -3), 3, 60),
        ((3, 0, -2), 12, 42),
        ((3, -1, -1), 9, 15),
        ((2, 2, -3), 2, 21),
        ((2, 1, -2), 18, 24),
        ((2, 0, -1), 33, 15),
        ((1, 1, -1), 24, 6),
        ((1, 0, 0), 23, 3),
    ),
}


def mixed_weight(word, transposed):
    counts = [0, 0, 0]
    for position, value in enumerate(word):
        counts[value] += -1 if position in transposed else 1
    return tuple(counts)


def raised_word(word, simple_root, transposed):
    high = simple_root
    low = simple_root + 1
    for position, value in enumerate(word):
        if position in transposed:
            if value == high:
                changed = list(word)
                changed[position] = low
                yield tuple(changed), -1.0
        elif value == low:
            changed = list(word)
            changed[position] = high
            yield tuple(changed), 1.0


def raising_matrix(indices, simple_root, transposed):
    rows = {}
    terms = []
    for column, index in enumerate(indices):
        for word, coefficient in raised_word(
            WORDS[index], simple_root, transposed
        ):
            if word not in rows:
                rows[word] = len(rows)
            terms.append((rows[word], column, coefficient))
    output = np.zeros((len(rows), len(indices)))
    for row, column, coefficient in terms:
        output[row, column] += coefficient
    return output


def mixed_highest_weight_bases(cut):
    transposed = CUTS[cut]
    grouped = defaultdict(list)
    for index, word in enumerate(WORDS):
        grouped[mixed_weight(word, transposed)].append(index)
    output = []
    for weight, expected, _carrier in MIXED_DATA[cut]:
        indices = np.asarray(grouped[weight], dtype=int)
        raising = np.vstack((
            raising_matrix(indices, 0, transposed),
            raising_matrix(indices, 1, transposed),
        ))
        kernel = (
            np.eye(len(indices)) if raising.shape[0] == 0
            else la.null_space(raising, rcond=1e-12)
        )
        assert kernel.shape == (len(indices), expected), (
            cut, weight, kernel.shape, expected
        )
        assert la.norm(kernel.T @ kernel - np.eye(expected)) < 3e-12
        lookup = np.full(len(WORDS), -1, dtype=np.int32)
        lookup[indices] = np.arange(len(indices), dtype=np.int32)
        output.append((indices, lookup, kernel))
    return tuple(output)


def partial_transpose_outputs(permutation, input_word, transposed):
    """Nonzero outputs of Gamma_transposed(P_permutation)."""
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
        left_is_input = position in transposed
        right_is_output = old in transposed
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
        output.append(tuple(
            assigned[find(position)] for position in range(NREP)
        ))
    return tuple(output)


def mixed_restrictions(permutations, bases, transposed, report=100):
    multiplicities = tuple(basis.shape[1] for _, _, basis in bases)
    dimension = sum(value * value for value in multiplicities)
    output = np.empty((dimension, len(permutations)))
    for column, permutation in enumerate(permutations):
        offset = 0
        for indices, lookup, basis in bases:
            acted = np.zeros_like(basis)
            for local_column, word_index in enumerate(indices):
                for output_word in partial_transpose_outputs(
                    permutation, WORDS[word_index], transposed
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
            print("mixed crossed permutation", column, "/",
                  len(permutations), flush=True)
    return output


def audit_crossing(crossing, mixed_multiplicities, mixed_carriers):
    mixed_metric = np.concatenate([
        np.full(multiplicity ** 2, carrier)
        for multiplicity, carrier in zip(
            mixed_multiplicities, mixed_carriers
        )
    ])
    holomorphic_metric = np.concatenate([
        np.full(multiplicity ** 2, 1.0 / carrier)
        for multiplicity, carrier in zip(
            BASE.HOL_MULTS, BASE.HOL_CARRIER_DIMS
        )
    ])
    gram = crossing.T @ (mixed_metric[:, None] * crossing)
    expected = np.diag(holomorphic_metric)
    metric_error = la.norm(gram - expected)
    metric_max = np.max(np.abs(gram - expected))

    mixed_trace = np.zeros(crossing.shape[0])
    offset = 0
    for multiplicity, carrier in zip(
        mixed_multiplicities, mixed_carriers
    ):
        for index in range(multiplicity):
            mixed_trace[offset + index * multiplicity + index] = carrier
        offset += multiplicity ** 2
    expected_trace = []
    for multiplicity in BASE.HOL_MULTS:
        for row in range(multiplicity):
            for column in range(multiplicity):
                expected_trace.append(float(row == column))
    trace_error = np.max(np.abs(
        mixed_trace @ crossing - np.asarray(expected_trace)
    ))
    print("crossing weighted-isometry Frobenius/max error:",
          metric_error, metric_max)
    print("crossing trace error:", trace_error)
    assert metric_error < 3e-9
    assert trace_error < 3e-9
    return metric_error, metric_max, trace_error


def main():
    parser = ArgumentParser()
    parser.add_argument("--cut", choices=tuple(CUTS), required=True)
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--census-only", action="store_true")
    parser.add_argument("--report", type=int, default=100)
    args = parser.parse_args()

    cut = args.cut
    transposed = CUTS[cut]
    data = MIXED_DATA[cut]
    weights = tuple(row[0] for row in data)
    multiplicities = tuple(row[1] for row in data)
    carriers = tuple(row[2] for row in data)
    assert sum(a * b for a, b in zip(multiplicities, carriers)) == D ** NREP
    assert sum(value * value for value in multiplicities) == 2761
    print("cut/transposed:", cut, tuple(sorted(transposed)))
    print("mixed weights/multiplicities/carriers:", data)
    bases = mixed_highest_weight_bases(cut)
    if args.census_only:
        return

    cache = args.cache
    if cache is None:
        cache = DISCOVERY / f"dth_level2_local_{cut}_crossing.npz"
    permutations, parent, generator = BASE.adjacent_bfs()
    print("building holomorphic Fourier table", flush=True)
    fourier = BASE.holomorphic_fourier(permutations, parent, generator)
    print("building sparse mixed restriction table", flush=True)
    mixed = mixed_restrictions(
        permutations, bases, transposed, report=args.report
    )
    print("contracting local crossing", flush=True)
    crossing = mixed @ fourier
    diagnostics = audit_crossing(crossing, multiplicities, carriers)
    np.savez_compressed(
        cache,
        crossing=crossing,
        cut=np.asarray(cut),
        transposed=np.asarray(sorted(transposed), dtype=np.int16),
        hol_shapes=np.asarray([
            tuple(shape) + (0,) * (3 - len(shape))
            for shape in BASE.HOL_SHAPES
        ], dtype=np.int16),
        hol_multiplicities=np.asarray(BASE.HOL_MULTS, dtype=np.int16),
        hol_carrier_dimensions=np.asarray(
            BASE.HOL_CARRIER_DIMS, dtype=np.int16
        ),
        mixed_weights=np.asarray(weights, dtype=np.int16),
        mixed_multiplicities=np.asarray(multiplicities, dtype=np.int16),
        mixed_carrier_dimensions=np.asarray(carriers, dtype=np.int16),
        diagnostics=np.asarray(diagnostics),
    )
    print("saved local crossing:", cache)


if __name__ == "__main__":
    main()
