#!/usr/bin/env python3
"""Exact two-by-two third-slot-PPT separator for the DTH pseudomoment.

Every physical Veronese--Segre density

    |(w tensor w) tensor z><(w tensor w) tensor z|

is separable, hence PPT, across the final ``z`` replica.  The corrected
first-level DTH relaxation imposes PPT only across the first bivector slot.
This verifier proves that the exact negative pseudomoment is NPT across the
omitted final-slot cut: its ``(3,0,0)^3`` local Schur block has no negative
diagonal entry but has a negative 2 by 2 principal determinant at indices
``(2,8)``.  This is the smallest possible principal-minor obstruction.

All crossing and determinant arithmetic is exact.  The floating discovery
eigenvector is not used.
"""

from __future__ import annotations

from functools import reduce
from itertools import product
import hashlib
import importlib.util
import math
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "certificates" / "dth_constrained_pseudomoment.json.gz"
EXPECTED_CERTIFICATE_SHA256 = (
    "707e183995f1963aebe9eef732530396b2baa53421aaa9fcbf9f5cb31c36e9da"
)
TARGET_WEIGHT = (3, 0, 0)
TARGET_MULTIPLICITY = 4
MINOR_INDICES = (2, 8)


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BRIDGE = import_file(
    "dth_ptz_exact_bridge", HERE / "agent_dth_local_crossing_exact.py"
)
FULL = import_file(
    "dth_ptz_full_face", HERE / "agent_dth_full_face_crt.py"
)


def mixed_weight(word):
    counts = [0, 0, 0]
    for position, value in enumerate(word):
        counts[value] += -1 if position == 4 else 1
    return tuple(counts)


def raised_words(word, simple_root):
    high = simple_root
    low = simple_root + 1
    for position, value in enumerate(word):
        if position == 4:
            if value == high:
                out = list(word)
                out[position] = low
                yield tuple(out), -1
        elif value == low:
            out = list(word)
            out[position] = high
            yield tuple(out), 1


def target_basis():
    words = [word for word in BRIDGE.WORDS
             if mixed_weight(word) == TARGET_WEIGHT]
    word_index = {word: index for index, word in enumerate(words)}
    rows = {}
    for root in (0, 1):
        for word in words:
            column = word_index[word]
            for target, coefficient in raised_words(word, root):
                row = rows.setdefault((root, target), {})
                row[column] = (
                    row.get(column, BRIDGE.F(0)) + BRIDGE.F(coefficient)
                )
    kernel = BRIDGE.rational_nullspace(rows, len(words))
    assert len(kernel) == TARGET_MULTIPLICITY
    return [
        {
            BRIDGE.WORD_INDEX[words[column]]: coefficient
            for column, coefficient in vector.items()
        }
        for vector in kernel
    ]


def partial_transpose_last(operator):
    output = {}
    for (row, column), value in operator.items():
        row_word = list(BRIDGE.WORDS[row])
        column_word = list(BRIDGE.WORDS[column])
        row_word[4], column_word[4] = column_word[4], row_word[4]
        key = (BRIDGE.WORD_INDEX[tuple(row_word)],
               BRIDGE.WORD_INDEX[tuple(column_word)])
        output[key] = output.get(key, BRIDGE.F(0)) + value
    return output


def target_crossing_numerator():
    holomorphic, _, _, _ = BRIDGE.exact_restriction_bridge()
    basis = target_basis()
    columns = []
    for permutation in BRIDGE.SELECTED_PERMUTATIONS:
        crossed = partial_transpose_last(
            BRIDGE.permutation_operator(permutation)
        )
        columns.append(BRIDGE.flatten_blocks([
            BRIDGE.restriction_block(crossed, basis)
        ]))
    target = [list(row) for row in zip(*columns)]
    hol_domain = sp.polys.matrices.DomainMatrix.from_list_sympy(
        103, 103, holomorphic
    )
    target_domain = sp.polys.matrices.DomainMatrix.from_list_sympy(
        16, 103, target
    )
    inverse_numerator, denominator = hol_domain.inv_den()
    numerator = (target_domain * inverse_numerator).to_Matrix()
    common = reduce(math.gcd, [abs(int(value)) for value in numerator if value]
                    + [int(denominator)])
    denominator = int(denominator) // common
    integer = np.asarray([
        [int(numerator[row, column]) // common for column in range(103)]
        for row in range(16)
    ], dtype=object)
    assert denominator == 300
    return integer, denominator


def matrix_to_tensor(matrix, dimensions):
    return matrix.reshape((*dimensions, *dimensions)).transpose(
        0, 3, 1, 4, 2, 5
    ).reshape(tuple(value * value for value in dimensions))


def tensor_to_target_matrix(tensor):
    return tensor.reshape((TARGET_MULTIPLICITY,) * 6).transpose(
        0, 2, 4, 1, 3, 5
    ).reshape(TARGET_MULTIPLICITY ** 3, TARGET_MULTIPLICITY ** 3)


def exact_target_block():
    coordinates, common_denominator = FULL.parse_certificate(CERTIFICATE)
    charts, integer_coordinates, _ = FULL.integer_hol_charts(
        coordinates, common_denominator
    )
    crossing, crossing_denominator = target_crossing_numerator()
    hol_ranges = FULL.block_ranges(BRIDGE.HOL_MULTS)
    output = np.zeros((64, 64), dtype=object)
    for shapes in product(range(5), repeat=3):
        chart = charts[shapes]
        coordinate = integer_coordinates[shapes]
        if chart.shape[1]:
            matrix = chart @ coordinate @ chart.T
        else:
            matrix = np.zeros((chart.shape[0], chart.shape[0]), dtype=object)
        dimensions = tuple(BRIDGE.HOL_MULTS[shape] for shape in shapes)
        tensor = matrix_to_tensor(matrix, dimensions)
        maps = [crossing[:, hol_ranges[shape].reshape(-1)]
                for shape in shapes]
        tensor = np.tensordot(maps[0], tensor, axes=(1, 0))
        tensor = np.tensordot(maps[1], tensor, axes=(1, 1)).transpose(1, 0, 2)
        tensor = np.tensordot(maps[2], tensor, axes=(1, 2)).transpose(1, 2, 0)
        output += tensor_to_target_matrix(tensor)
    assert all(output[i, j] == output[j, i]
               for i in range(64) for j in range(64))
    positive_denominator = (
        common_denominator * FULL.HOL_SCALE ** 2
        * crossing_denominator ** 3
    )
    assert positive_denominator > 0
    return output, positive_denominator


def main():
    certificate_hash = hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest()
    assert certificate_hash == EXPECTED_CERTIFICATE_SHA256
    block, denominator = exact_target_block()
    # There is no one-dimensional principal obstruction.
    assert all(int(block[index, index]) >= 0 for index in range(64))
    first, second = MINOR_INDICES
    determinant_numerator = (
        int(block[first, first]) * int(block[second, second])
        - int(block[first, second]) ** 2
    )
    assert determinant_numerator < 0
    determinant_text = (
        f"{determinant_numerator}/{denominator ** 2}".encode("ascii")
    )
    print("exact final-slot partial-transpose obstruction passed")
    print("source certificate sha256:", certificate_hash)
    print("local target weight:", TARGET_WEIGHT,
          "global block dimension: 64")
    print("negative principal minor indices:", MINOR_INDICES)
    print("determinant numerator digits:",
          len(str(abs(determinant_numerator))))
    print("determinant rational sha256:",
          hashlib.sha256(determinant_text).hexdigest())


if __name__ == "__main__":
    main()
