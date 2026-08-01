#!/usr/bin/env python3
"""Find an exact rational third-slot-PPT separator for the DTH moment.

Every physical Veronese--Segre density
``|(w tensor w) tensor z><...|`` is separable, hence PPT, across the final
``z`` slot.  The corrected first DTH lift only imposes partial transpose on
the first bivector slot.  This script reconstructs the final-slot partial
transpose in the one-contravariant local module and searches its smallest
64-dimensional block for a short integer negative Rayleigh vector.

Discovery code only.  The final vector and sign must be replayed by a small
exact verifier.
"""

from __future__ import annotations

import argparse
from functools import reduce
import importlib.util
import math
from pathlib import Path
import sys

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VERIFY = ROOT / "verification"
sys.path.insert(0, str(VERIFY))

import agent_dth_local_crossing_exact as BRIDGE
import agent_dth_full_face_crt as FULL


TARGET_WEIGHT = (3, 0, 0)
TARGET_MULTIPLICITY = 4
TARGET_BLOCK = (2, 2, 2)  # index in the complete numerical target census


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
                # rational_nullspace assumes a rational coefficient field;
                # bare Python integer division would silently create floats.
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
    out = {}
    for (row, column), value in operator.items():
        row_word = list(BRIDGE.WORDS[row])
        column_word = list(BRIDGE.WORDS[column])
        row_word[4], column_word[4] = column_word[4], row_word[4]
        key = (BRIDGE.WORD_INDEX[tuple(row_word)],
               BRIDGE.WORD_INDEX[tuple(column_word)])
        out[key] = out.get(key, 0) + value
    return out


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
    return integer, denominator


def matrix_to_tensor(matrix, dimensions):
    return matrix.reshape((*dimensions, *dimensions)).transpose(
        0, 3, 1, 4, 2, 5
    ).reshape(tuple(value * value for value in dimensions))


def tensor_to_target_matrix(tensor):
    return tensor.reshape((TARGET_MULTIPLICITY,) * 6).transpose(
        0, 2, 4, 1, 3, 5
    ).reshape(TARGET_MULTIPLICITY ** 3, TARGET_MULTIPLICITY ** 3)


def exact_target_block(certificate):
    coordinates, common_denominator = FULL.parse_certificate(certificate)
    charts, integer_coordinates, _ = FULL.integer_hol_charts(
        coordinates, common_denominator
    )
    crossing, crossing_denominator = target_crossing_numerator()
    hol_ranges = FULL.block_ranges(BRIDGE.HOL_MULTS)
    output = np.zeros((64, 64), dtype=object)
    for count, shapes in enumerate(__import__("itertools").product(
        range(5), repeat=3
    ), 1):
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
        if count % 25 == 0:
            print("exact target contributions", count, "/125", flush=True)
    return output, common_denominator, crossing_denominator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        default=str(
            VERIFY / "certificates" /
            "dth_constrained_pseudomoment.json.gz"
        ),
    )
    parser.add_argument("--output", default="/tmp/dth_third_slot_vector.txt")
    args = parser.parse_args()
    block, coordinate_denominator, crossing_denominator = exact_target_block(
        args.certificate
    )
    antisymmetry = max(abs(int(block[i, j] - block[j, i]))
                       for i in range(64) for j in range(64))
    maximum = max(abs(int(value)) for value in block.flat)
    print("exact transpose asymmetry/max:", antisymmetry, "/", maximum)
    assert antisymmetry == 0
    negative_diagonal = next(
        (i for i in range(64) if int(block[i, i]) < 0), None
    )
    negative_pair = None
    if negative_diagonal is None:
        for i in range(64):
            for j in range(i + 1, 64):
                determinant = (
                    int(block[i, i]) * int(block[j, j])
                    - int(block[i, j]) ** 2
                )
                if determinant < 0:
                    negative_pair = (i, j, determinant)
                    break
            if negative_pair is not None:
                break
    print("negative diagonal:", negative_diagonal)
    print("first negative two-by-two principal minor:", negative_pair)
    # The quadratic form depends only on the symmetric part.  Keep the
    # doubled symmetric numerator integral.
    symmetric = block + block.T
    scale = max(abs(int(value)) for value in symmetric.flat)
    numerical = np.asarray([
        [int(value) / scale for value in row] for row in symmetric
    ], dtype=float)
    eigenvalues, eigenvectors = np.linalg.eigh(numerical)
    print("smallest scaled eigenvalue:", eigenvalues[0])
    vector = eigenvectors[:, 0]
    for bits in range(8, 33, 2):
        integer_vector = np.rint(vector * (1 << bits)).astype(np.int64)
        value = sum(
            int(integer_vector[i]) * int(symmetric[i, j])
            * int(integer_vector[j])
            for i in range(64) for j in range(64)
        )
        if value < 0:
            path = Path(args.output)
            path.write_text(
                ",".join(map(str, map(int, integer_vector))) + "\n"
                + str(value) + "\n"
                + str(coordinate_denominator) + "\n"
                + str(crossing_denominator) + "\n",
                encoding="ascii",
            )
            print("negative integer vector bits:", bits)
            print("vector squared norm:",
                  sum(int(value) ** 2 for value in integer_vector))
            print("negative numerator digits:", len(str(abs(value))))
            print("wrote", path)
            break
    else:
        raise AssertionError("no short negative integer vector found")


if __name__ == "__main__":
    main()
