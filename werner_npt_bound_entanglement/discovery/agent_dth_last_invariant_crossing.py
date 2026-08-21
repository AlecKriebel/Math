#!/usr/bin/env python3
"""Numerical normalized local crossing for final-slot DTH partial transpose.

This is the discovery-precision companion to the exact bridge in
``verification/agent_dth_last_crossing_exact.py``.  It exposes a 103 by 103
Hilbert--Schmidt orthogonal matrix compatible with
``agent_dth_primal_admm.crossing_apply``.  The full three-site crossing is
its tensor cube.

Numerical conclusions made with this module require later exact
reconstruction.  The representation census and algebraic crossing itself
are independently exact-certified.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import scipy.linalg as la

import agent_dth_invariant_crossing as first


HERE = Path(__file__).resolve().parent
EXACT_PATH = HERE.parent / "verification" / "agent_dth_last_crossing_exact.py"
SPEC = importlib.util.spec_from_file_location("dth_last_exact", EXACT_PATH)
EXACT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(EXACT)


D = 3
LOCAL_DIM = D**5
HOL_NAMES = first.HOL_NAMES
HOL_SHAPES = first.HOL_SHAPES
HOL_CARRIER_DIMS = first.HOL_CARRIER_DIMS
HOL_MULTS = first.HOL_MULTS

LAST_DYNKIN_WEIGHTS = EXACT.LAST_DYNKIN_WEIGHTS
LAST_NAMES = EXACT.LAST_NAMES
LAST_CARRIER_DIMS = EXACT.LAST_IRREP_DIMS
LAST_MULTS = EXACT.LAST_MULTS


def dense_columns(basis):
    output = np.zeros((LOCAL_DIM, len(basis)), dtype=float)
    for column, vector in enumerate(basis):
        for row, value in vector.items():
            output[row, column] = float(value)
    return output


def orthonormal_target_bases():
    output = []
    for basis, expected in zip(EXACT.last_highest_weight_bases(), LAST_MULTS):
        raw = dense_columns(basis)
        q, r = la.qr(raw, mode="economic")
        assert np.min(np.abs(np.diag(r))) > 1e-12
        assert q.shape[1] == expected
        output.append(q)
    return output


def dense_sparse_operator(operator):
    output = np.zeros((LOCAL_DIM, LOCAL_DIM), dtype=float)
    for (row, column), value in operator.items():
        output[row, column] = float(value)
    return output


def flatten_restrictions(operator, bases):
    return np.concatenate([
        (basis.T @ operator @ basis).reshape(-1)
        for basis in bases
    ])


def block_ranges(multiplicities):
    output = []
    offset = 0
    for multiplicity in multiplicities:
        output.append(
            np.arange(offset, offset + multiplicity * multiplicity)
            .reshape(multiplicity, multiplicity)
        )
        offset += multiplicity * multiplicity
    assert offset == 103
    return output


def normalized_local_crossing(verbose=True):
    """Return ``(C5, hol_ranges, last_ranges)`` in HS-normalized coordinates."""
    holomorphic = first.hol_highest_weight_bases()
    target = orthonormal_target_bases()
    hol_columns = []
    target_columns = []
    for permutation in EXACT.bridge.SELECTED_PERMUTATIONS:
        covariant_sparse = EXACT.bridge.permutation_operator(permutation)
        target_sparse = EXACT.partial_transpose_last(covariant_sparse)
        covariant = dense_sparse_operator(covariant_sparse)
        crossed = dense_sparse_operator(target_sparse)
        hol_columns.append(flatten_restrictions(covariant, holomorphic))
        target_columns.append(flatten_restrictions(crossed, target))
    hol_restriction = np.column_stack(hol_columns)
    target_restriction = np.column_stack(target_columns)
    raw = la.solve(hol_restriction.T, target_restriction.T).T

    input_scale = np.concatenate([
        np.full(multiplicity * multiplicity, 1 / np.sqrt(carrier))
        for multiplicity, carrier in zip(HOL_MULTS, HOL_CARRIER_DIMS)
    ])
    output_scale = np.concatenate([
        np.full(multiplicity * multiplicity, np.sqrt(carrier))
        for multiplicity, carrier in zip(LAST_MULTS, LAST_CARRIER_DIMS)
    ])
    normalized = output_scale[:, None] * raw * input_scale[None, :]
    error = la.norm(normalized.T @ normalized - np.eye(103), ord=2)
    if verbose:
        print("normalized final-slot local crossing orthogonality error:", error)
        print("target names / multiplicities:",
              list(zip(LAST_NAMES, LAST_MULTS)))
    assert error < 2e-8
    return (normalized,
            block_ranges(HOL_MULTS),
            block_ranges(LAST_MULTS))


if __name__ == "__main__":
    matrix, source_ranges, target_ranges = normalized_local_crossing()
    print("shape:", matrix.shape)
    print("source blocks:", [item.shape for item in source_ranges])
    print("target blocks:", [item.shape for item in target_ranges])
