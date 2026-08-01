#!/usr/bin/env python3
"""Numerically audit the exact D5 face against frozen Gamma5 data.

This is a convention checker, not an exact certificate.  It independently
builds the two final-slot delta contractions in the orthonormal target
highest-weight bases, restricts ``D5^* D5`` to the frozen pair/Pluecker
support, and compares its kernel with the rank-751 Gamma5 face exposed by an
objective-free feasible point.

It also crosses the exact computational product equality through the final
replica and checks that its blocks have zero D5 energy.  The exact rank and
kernel theorem is verified separately by
``verification/agent_dth_gamma5_face_exact.py`` and
``verification/agent_dth_exact_gamma5_face_coordinates.py``.
"""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
import sys

import numpy as np
import scipy.linalg as la


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


EXACT = import_file(
    "dth_gamma5_exact_coordinates_audit",
    ROOT / "verification" / "agent_dth_exact_gamma5_face_coordinates.py",
)
LAST_NUMERICAL = import_file(
    "dth_gamma5_last_numerical_audit",
    HERE / "agent_dth_last_invariant_crossing.py",
)


def dense_columns(basis):
    output = np.zeros((3**5, len(basis)), dtype=float)
    for column, vector in enumerate(basis):
        for row, value in vector.items():
            output[row, column] = float(value)
    return output


def normalized_local_deltas_raw_order():
    """Return d0,d2 in the QR-orthonormal raw-LAST target convention."""
    output = []
    for shape, basis in enumerate(EXACT.LOCAL_BASES):
        raw = dense_columns(basis)
        _, triangular = la.qr(raw, mode="economic")
        assert np.min(np.abs(np.diag(triangular))) > 1e-12
        inverse = la.solve_triangular(triangular, np.eye(triangular.shape[0]))
        output.append(tuple(
            np.asarray(EXACT.local_delta(shape, which), dtype=float) @ inverse
            for which in (0, 2)
        ))
    return output


def archive_state_changes(cache_local):
    """Recover the state-basis changes hidden in the frozen crossing cache.

    The final-slot cache was exported in reverse irrep order and with a
    different orthonormal basis in each multiplicity space.  On operator
    coordinates its relative block is exactly ``K tensor K``.  Reshuffling
    makes this a rank-one matrix and recovers the state-space matrix ``K``.
    """
    naive, _, _ = LAST_NUMERICAL.normalized_local_crossing(verbose=False)
    raw_ranges = coordinate_ranges(EXACT.LAST_MULTS)
    row_permutation = np.concatenate([
        item.reshape(-1) for item in reversed(raw_ranges)
    ])
    relative = cache_local @ naive[row_permutation].T
    archive_mults = tuple(reversed(EXACT.LAST_MULTS))
    archive_ranges = coordinate_ranges(archive_mults)
    block_mask = np.zeros_like(relative, dtype=bool)
    output = []
    for multiplicity, indices in zip(archive_mults, archive_ranges):
        flat = indices.reshape(-1)
        block_mask[np.ix_(flat, flat)] = True
        block = relative[np.ix_(flat, flat)]
        reshuffled = (
            block.reshape(multiplicity, multiplicity,
                          multiplicity, multiplicity)
            .transpose(0, 2, 1, 3)
            .reshape(multiplicity**2, multiplicity**2)
        )
        reshuffled = (reshuffled + reshuffled.T) / 2
        values, vectors = la.eigh(reshuffled)
        state = (vectors[:, -1].reshape(multiplicity, multiplicity)
                 * np.sqrt(values[-1]))
        if la.det(state) < 0 and multiplicity % 2:
            state = -state
        assert la.norm(state.T @ state - np.eye(multiplicity)) < 2e-12
        assert la.norm(block - np.kron(state, state)) < 2e-12
        output.append(state)
    assert la.norm(relative[~block_mask]) < 2e-12
    return output


def normalized_local_deltas(cache_local):
    """Return d0,d2 in frozen archive order and target-basis convention."""
    raw = normalized_local_deltas_raw_order()
    changes = archive_state_changes(cache_local)
    return [
        tuple(delta @ change.T for delta in raw[5 - archive_shape])
        for archive_shape, change in enumerate(changes)
    ]


def kron3(left, middle, right):
    return np.kron(np.kron(left, middle), right)


def delta_gram(shapes, deltas):
    local = [deltas[shape] for shape in shapes]
    output = None
    for choices in ((0, 0), (0, 1), (1, 0), (1, 1)):
        factors = [pair[choices[0]].T @ pair[choices[1]] for pair in local]
        term = kron3(*factors)
        output = term if output is None else output + term
    return (output + output.T) / 2


def coordinate_ranges(multiplicities):
    output = []
    offset = 0
    for multiplicity in multiplicities:
        output.append(
            np.arange(offset, offset + multiplicity**2)
            .reshape(multiplicity, multiplicity)
        )
        offset += multiplicity**2
    assert offset == 103
    return output


def block_indices(local_ranges, shapes):
    grids = [local_ranges[shape] for shape in shapes]
    return (grids[0][:, None, None, :, None, None],
            grids[1][None, :, None, None, :, None],
            grids[2][None, None, :, None, None, :])


def get_block(tensor, indices, dimensions):
    size = int(np.prod(dimensions))
    return tensor[indices].reshape(size, size)


def crossing_apply(local, tensor):
    output = np.tensordot(local, tensor, axes=(1, 0))
    output = np.tensordot(local, output, axes=(1, 1)).transpose(1, 0, 2)
    return np.tensordot(local, output, axes=(1, 2)).transpose(1, 2, 0)


def projector(columns):
    if not columns.shape[1]:
        return np.zeros((columns.shape[0], columns.shape[0]))
    orthonormal, _ = la.qr(columns, mode="economic")
    return orthonormal @ orthonormal.T


def main():
    face = np.load("/tmp/dth_gamma5_feasible_face.npz")
    pair_data = np.load("/tmp/dth_gamma5_pairplucker_rank21.npz")
    archive_names = tuple(map(str, face["names"]))
    archive_mults = tuple(map(int, face["mults"]))
    assert archive_names == tuple(reversed(EXACT.LAST.LAST_NAMES))
    assert archive_mults == tuple(reversed(EXACT.LAST_MULTS))

    crossing = np.load("/tmp/dth_gamma5_local_crossing_root.npz")
    local = crossing["local"]
    assert tuple(map(int, crossing["mults"])) == archive_mults
    deltas = normalized_local_deltas(local)
    maximum_face_projector_error = 0.0
    maximum_internal_projector_error = 0.0
    maximum_face_d5_residual = 0.0
    support_total = face_total = internal_total = 0
    worst_face = worst_internal = worst_residual = None

    for archive_shapes in itertools.product(range(6), repeat=3):
        key = "".join(map(str, archive_shapes))
        pair = pair_data[f"pair_{key}"]
        frozen_internal = pair_data[f"internal_{key}"]
        frozen_face = face[f"range_{key}"]
        gram = delta_gram(archive_shapes, deltas)
        reduced = (pair.T @ gram @ pair)
        reduced = (reduced + reduced.T) / 2
        if reduced.shape[0]:
            values, vectors = la.eigh(reduced)
        else:
            values = np.empty(0)
            vectors = np.empty((0, 0))
        scale = max(1.0, float(np.max(np.abs(values), initial=0.0)))
        positive = values > 2e-9 * scale
        internal = pair @ vectors[:, positive]
        calculated_face = pair @ vectors[:, ~positive]

        face_error = la.norm(
            projector(calculated_face) - projector(frozen_face), ord=2
        )
        internal_error = la.norm(
            projector(internal) - projector(frozen_internal), ord=2
        )
        residual = (la.norm(gram @ calculated_face, ord=2)
                    if calculated_face.shape[1] else 0.0)
        if face_error > maximum_face_projector_error:
            maximum_face_projector_error, worst_face = face_error, key
        if internal_error > maximum_internal_projector_error:
            maximum_internal_projector_error, worst_internal = (
                internal_error, key
            )
        if residual > maximum_face_d5_residual:
            maximum_face_d5_residual, worst_residual = residual, key

        assert internal.shape[1] == frozen_internal.shape[1], key
        assert calculated_face.shape[1] == frozen_face.shape[1], key
        support_total += pair.shape[1]
        internal_total += internal.shape[1]
        face_total += calculated_face.shape[1]

    # Cross a physical product equality through Gamma5 in the same reversed
    # block ordering used by the frozen archives.
    equality = np.load("/tmp/dth_computational_equality.npz")
    z5 = crossing_apply(local, equality["x"])
    ranges = coordinate_ranges(archive_mults)
    maximum_equality_face_leakage = 0.0
    maximum_equality_d5_energy = 0.0
    total_equality_d5_energy = 0.0
    worst_equality_face = worst_equality_energy = None
    for archive_shapes in itertools.product(range(6), repeat=3):
        key = "".join(map(str, archive_shapes))
        dimensions = tuple(archive_mults[shape]
                           for shape in archive_shapes)
        matrix = get_block(z5, block_indices(ranges, archive_shapes),
                           dimensions)
        matrix = (matrix + matrix.T) / 2
        frozen_face = face[f"range_{key}"]
        projection = projector(frozen_face)
        leakage = la.norm(matrix - projection @ matrix @ projection, ord=2)
        energy = float(np.trace(delta_gram(archive_shapes, deltas) @ matrix))
        carrier = int(np.prod([
            int(face["carriers"][shape]) for shape in archive_shapes
        ]))
        total_equality_d5_energy += carrier * energy
        if leakage > maximum_equality_face_leakage:
            maximum_equality_face_leakage, worst_equality_face = leakage, key
        if abs(energy) > maximum_equality_d5_energy:
            maximum_equality_d5_energy, worst_equality_energy = abs(energy), key

    print("support/internal/face dimensions:",
          support_total, internal_total, face_total)
    print("max face projector error:", maximum_face_projector_error,
          "block", worst_face)
    print("max internal projector error:", maximum_internal_projector_error,
          "block", worst_internal)
    print("max D5 residual on calculated face:", maximum_face_d5_residual,
          "block", worst_residual)
    print("computational equality max face leakage:",
          maximum_equality_face_leakage, "block", worst_equality_face)
    print("computational equality max block D5 energy:",
          maximum_equality_d5_energy, "block", worst_equality_energy)
    print("computational equality carrier-weighted D5 energy:",
          total_equality_d5_energy)
    assert support_total == 772
    assert internal_total == 21
    assert face_total == 751
    # The frozen feasible point has residuals around 1e-11 and its smallest
    # positive Gamma5 eigenvalue is only 1.8e-8, so its numerical eigenspace
    # is expected to be accurate only at the several-parts-in-1e6 level.
    assert maximum_face_projector_error < 1e-5
    assert maximum_internal_projector_error < 1e-5
    assert maximum_face_d5_residual < 2e-8
    assert maximum_equality_face_leakage < 2e-7
    assert maximum_equality_d5_energy < 2e-7
    print("Gamma5 exact-formula convention audit passed")


if __name__ == "__main__":
    main()
