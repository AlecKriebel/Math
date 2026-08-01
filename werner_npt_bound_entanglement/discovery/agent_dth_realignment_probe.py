#!/usr/bin/env python3
"""Invariant CCNR/realignment probe for the exact DTH pseudomoment.

This is discovery code.  It reconstructs the exact certificate numerically
in the selected 103-diagram local permutation basis and computes the trace
norm of two realignments without ever forming the global ambient operator:

* A:BC, where A is one bivector (replicas 1,2); and
* C:AB, where C is the final vector (replica 5).

Local realigned permutation diagrams are reduced to SU(3) highest-weight
multiplicity maps.  The three physical qutrit sites then give only small
Kronecker multiplicity blocks.  A ratio greater than one is a convex-hull-
valid CCNR separation of the normalized moment from the corresponding
separable cone.  Floating point is used only for discovery.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import importlib.util
from pathlib import Path

import numpy as np
import scipy.linalg as la


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VERIFY = ROOT / "verification"
DEFAULT_CERTIFICATE = (
    VERIFY / "certificates" / "dth_complete_ppt_pseudomoment.json.gz"
)


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CODEC = import_file("dth_realign_codec", VERIFY / "agent_dth_certificate_io.py")
KCHART = import_file(
    "dth_realign_kchart", VERIFY / "agent_dth_exact_k_coordinates.py"
)
BRIDGE = import_file(
    "dth_realign_bridge", VERIFY / "agent_dth_local_crossing_exact.py"
)
BLOCKS = import_file(
    "dth_realign_blocks", VERIFY / "agent_dth_full_face_crt.py"
)


def flatten(indices):
    value = 0
    for index in indices:
        value = 3 * value + int(index)
    return value


def mode_apply(matrix, tensor, axis):
    output = np.tensordot(matrix, tensor, axes=(1, axis))
    if axis:
        order = list(range(1, output.ndim))
        order.insert(axis, 0)
        output = output.transpose(order)
    return output


def highest_weight_bases(signs, tolerance=1e-11):
    """Return orthonormal highest-weight multiplicity bases.

    A sign ``+1`` denotes a covariant qutrit slot and ``-1`` a
    contravariant slot.  The keys are SU(3) labels ``(p,q)``.
    """
    words = list(product(range(3), repeat=len(signs)))

    def weight(word):
        output = [0, 0, 0]
        for sign, value in zip(signs, word):
            output[value] += sign
        return tuple(output)

    spaces = {}
    for index, word in enumerate(words):
        spaces.setdefault(weight(word), []).append(index)

    result = {}
    total_dimension = 0
    for dominant, indices in sorted(spaces.items(), reverse=True):
        if not dominant[0] >= dominant[1] >= dominant[2]:
            continue
        row_labels = {}
        entries = []
        for root in (0, 1):
            for column, index in enumerate(indices):
                word = words[index]
                for position, (sign, value) in enumerate(zip(signs, word)):
                    if sign == 1 and value == root + 1:
                        target = list(word)
                        target[position] = root
                        key = (root, tuple(target))
                        row_labels.setdefault(key, len(row_labels))
                        entries.append((row_labels[key], column, 1.0))
                    elif sign == -1 and value == root:
                        target = list(word)
                        target[position] = root + 1
                        key = (root, tuple(target))
                        row_labels.setdefault(key, len(row_labels))
                        entries.append((row_labels[key], column, -1.0))
        raising = np.zeros((len(row_labels), len(indices)))
        for row, column, value in entries:
            raising[row, column] += value
        if raising.shape[0]:
            kernel = la.null_space(raising, rcond=tolerance)
        else:
            kernel = np.eye(len(indices))
        if not kernel.shape[1]:
            continue
        label = (dominant[0] - dominant[1], dominant[1] - dominant[2])
        basis = np.zeros((len(words), kernel.shape[1]))
        basis[np.asarray(indices), :] = kernel
        p, q = label
        carrier = (p + 1) * (q + 1) * (p + q + 2) // 2
        result[label] = {
            "basis": basis,
            "multiplicity": kernel.shape[1],
            "carrier": carrier,
            "weight": dominant,
        }
        total_dimension += carrier * kernel.shape[1]
    assert total_dimension == 3 ** len(signs)
    return result


def raw_restriction_tensor(coordinates):
    tensor = np.zeros((103, 103, 103))
    ranges = BLOCKS.block_ranges(BRIDGE.HOL_MULTS)
    for shapes in product(range(5), repeat=3):
        _, _, exact_range = KCHART.hol_k_coordinates(shapes)
        chart = np.asarray(exact_range, dtype=float)
        coordinate = np.asarray(coordinates[shapes], dtype=float)
        if coordinate.size:
            block = chart @ coordinate @ chart.T
        else:
            block = np.zeros((chart.shape[0], chart.shape[0]))
        dimensions = tuple(BRIDGE.HOL_MULTS[shape] for shape in shapes)
        BLOCKS.put_block(tensor, ranges, shapes, dimensions, block)
    return tensor


def diagram_core(coordinates):
    tensor = raw_restriction_tensor(coordinates)
    holomorphic, _, _, _ = BRIDGE.exact_restriction_bridge()
    restriction = np.asarray(holomorphic, dtype=float)
    print("local restriction condition number:", np.linalg.cond(restriction))
    core = tensor
    for axis in range(3):
        moved = np.moveaxis(core, axis, 0)
        solved = la.solve(
            restriction, moved.reshape(103, -1), assume_a="gen"
        ).reshape(moved.shape)
        core = np.moveaxis(solved, 0, axis)
    reconstructed = core
    for axis in range(3):
        reconstructed = mode_apply(restriction, reconstructed, axis)
    relative = la.norm((reconstructed - tensor).ravel()) / la.norm(tensor.ravel())
    print("diagram-core reconstruction relative residual:", relative)
    return core


def source_trace_and_purity(coordinates):
    trace = 0.0
    purity = 0.0
    for shapes in product(range(5), repeat=3):
        physical, gram, _ = KCHART.hol_k_coordinates(shapes)
        k = np.asarray(physical, dtype=float)
        g = np.asarray(gram, dtype=float)
        a = np.asarray(coordinates[shapes], dtype=float)
        if not a.size:
            continue
        compressed = a @ (k.T @ g @ k)
        carrier = np.prod([BRIDGE.HOL_IRREP_DIMS[s] for s in shapes])
        trace += carrier * np.trace(compressed)
        purity += carrier * np.trace(compressed @ compressed)
    return trace, purity


def local_ab_realignments():
    row = highest_weight_bases((1, 1, -1, -1))
    column = highest_weight_bases((-1, -1, -1, 1, 1, 1))
    shared = sorted(set(row) & set(column))
    maps = {
        label: np.zeros((103, row[label]["multiplicity"],
                         column[label]["multiplicity"]))
        for label in shared
    }
    words = BRIDGE.WORDS
    for diagram, permutation in enumerate(BRIDGE.SELECTED_PERMUTATIONS):
        operator = BRIDGE.permutation_operator(permutation)
        row_indices = []
        column_indices = []
        values = []
        for (target, source), coefficient in operator.items():
            target_word = words[target]
            source_word = words[source]
            row_indices.append(flatten(
                target_word[:2] + source_word[:2]
            ))
            column_indices.append(flatten(
                target_word[2:] + source_word[2:]
            ))
            values.append(float(coefficient))
        row_indices = np.asarray(row_indices)
        column_indices = np.asarray(column_indices)
        values = np.asarray(values)
        for label in shared:
            left = row[label]["basis"][row_indices, :]
            right = column[label]["basis"][column_indices, :]
            maps[label][diagram] = left.T @ (values[:, None] * right)

    maximum_error = 0.0
    for diagram in range(103):
        norm = sum(
            row[label]["carrier"]
            * np.sum(maps[label][diagram] ** 2)
            for label in shared
        )
        maximum_error = max(maximum_error, abs(norm - 243.0))
    print("A:BC local realignment Frobenius audit:", maximum_error)
    print("A:BC shared labels:", {
        label: (row[label]["carrier"], row[label]["multiplicity"],
                column[label]["multiplicity"])
        for label in shared
    })
    return row, column, maps


def global_ab_trace_norm(core, row, maps):
    labels = sorted(maps)
    total = 0.0
    frobenius_squared = 0.0
    rows = []
    for labels3 in product(labels, repeat=3):
        tensor = core
        local_dimensions = []
        carrier = 1
        for axis, label in enumerate(labels3):
            local = maps[label]
            mr, mc = local.shape[1:]
            tensor = mode_apply(local.reshape(103, mr * mc).T, tensor, axis)
            local_dimensions.append((mr, mc))
            carrier *= row[label]["carrier"]
        shape = tuple(value for pair in local_dimensions for value in pair)
        tensor = tensor.reshape(shape)
        tensor = tensor.transpose(0, 2, 4, 1, 3, 5)
        matrix = tensor.reshape(
            np.prod([pair[0] for pair in local_dimensions]),
            np.prod([pair[1] for pair in local_dimensions]),
        )
        singular = la.svdvals(matrix)
        contribution = carrier * np.sum(singular)
        total += contribution
        frobenius_squared += carrier * np.sum(singular ** 2)
        rows.append((labels3, matrix.shape, carrier, contribution,
                     singular[0] if singular.size else 0.0,
                     np.sum(singular > 1e-10)))
    rows.sort(key=lambda item: item[3], reverse=True)
    print("A:BC ten largest nuclear contributions")
    for row_entry in rows[:10]:
        print(" ", row_entry)
    return total, frobenius_squared, rows


def local_c_gram():
    words = BRIDGE.WORDS
    matrices = np.zeros((103, 9, 3 ** 8))
    for diagram, permutation in enumerate(BRIDGE.SELECTED_PERMUTATIONS):
        operator = BRIDGE.permutation_operator(permutation)
        for (target, source), coefficient in operator.items():
            target_word = words[target]
            source_word = words[source]
            row = flatten((target_word[4], source_word[4]))
            column = flatten(target_word[:4] + source_word[:4])
            matrices[diagram, row, column] += float(coefficient)
    identity = np.zeros(9)
    for index in range(3):
        identity[3 * index + index] = 1 / np.sqrt(3)
    trivial_vectors = np.einsum("a,pac->pc", identity, matrices)
    trivial = trivial_vectors @ trivial_vectors.T
    full = matrices.reshape(103, -1) @ matrices.reshape(103, -1).T
    adjoint = (full - trivial) / 8.0
    error = max(
        np.max(np.abs(np.diag(trivial + 8 * adjoint) - 243)),
        np.max(np.abs(full - (trivial + 8 * adjoint))),
    )
    print("C:AB local realignment Frobenius audit:", error)
    return {(0, 0): (1, trivial), (1, 1): (8, adjoint)}


def gram_norm_squared(core, grams):
    transformed = core
    for axis, gram in enumerate(grams):
        transformed = mode_apply(gram, transformed, axis)
    value = np.vdot(core, transformed).real
    return max(value, 0.0)


def global_c_trace_norm(core, local):
    total = 0.0
    frobenius_squared = 0.0
    rows = []
    labels = sorted(local)
    for labels3 in product(labels, repeat=3):
        carrier = np.prod([local[label][0] for label in labels3])
        norm_squared = gram_norm_squared(
            core, [local[label][1] for label in labels3]
        )
        contribution = carrier * np.sqrt(norm_squared)
        total += contribution
        frobenius_squared += carrier * norm_squared
        rows.append((labels3, carrier, contribution, norm_squared))
    rows.sort(key=lambda item: item[2], reverse=True)
    print("C:AB nuclear contributions")
    for row_entry in rows:
        print(" ", row_entry)
    return total, frobenius_squared, rows


def main():
    coordinates, metadata = CODEC.read_certificate(DEFAULT_CERTIFICATE)
    print("certificate metadata:", metadata)
    trace, purity = source_trace_and_purity(coordinates)
    print("source trace/purity:", trace, purity)
    core = diagram_core(coordinates)

    row, _, ab_maps = local_ab_realignments()
    ab_norm, ab_frobenius, _ = global_ab_trace_norm(core, row, ab_maps)
    print("A:BC realignment norm/frobenius^2/ratio:",
          ab_norm, ab_frobenius, ab_norm / trace)
    print("A:BC purity audit relative error:",
          abs(ab_frobenius - purity) / purity)

    c_local = local_c_gram()
    c_norm, c_frobenius, _ = global_c_trace_norm(core, c_local)
    print("C:AB realignment norm/frobenius^2/ratio:",
          c_norm, c_frobenius, c_norm / trace)
    print("C:AB purity audit relative error:",
          abs(c_frobenius - purity) / purity)


if __name__ == "__main__":
    main()
