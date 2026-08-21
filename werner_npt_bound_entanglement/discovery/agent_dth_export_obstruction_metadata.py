#!/usr/bin/env python3
"""Export diagram-coordinate metadata for exact obstruction reconstruction.

The exact local bridge uses 103 selected permutation diagrams.  This utility
converts the S3-symmetric theta=9/500 numerical obstruction from normalized
Schur coordinates to the matched diagram coefficient tensor and exports the
local normalized restriction matrices.  The diagram tensor is the natural
target for rational correction because partial transpose leaves its
coefficients unchanged and only replaces each local diagram by its matched
walled diagram.

All exported coefficients remain floating discovery data.  Exact checking
must rebuild the restriction matrices from
``verification/agent_dth_local_crossing_exact.py`` and use a rationally
corrected diagram tensor.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

import numpy as np
import scipy.linalg as la

import agent_dth_invariant_crossing as cross
import agent_dth_primal_admm as primal


EXACT_BRIDGE = (Path(__file__).resolve().parent.parent / "verification"
                / "agent_dth_local_crossing_exact.py")
sys.path.insert(0, str(EXACT_BRIDGE.parent))
SPEC = importlib.util.spec_from_file_location("dth_exact_bridge", EXACT_BRIDGE)
BRIDGE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BRIDGE)


def normalized_restriction(selected, hol, mixed):
    hol_columns = []
    mixed_columns = []
    for permutation in selected:
        operator = cross.permutation_matrix(permutation)
        crossed = cross.partial_transpose_first_pair(operator)
        hol_columns.append(np.concatenate([
            (basis.T @ operator @ basis).reshape(-1)
            for basis in hol]))
        mixed_columns.append(np.concatenate([
            (basis.T @ crossed @ basis).reshape(-1)
            for basis in mixed]))
    hol_matrix = np.column_stack(hol_columns)
    mixed_matrix = np.column_stack(mixed_columns)

    def scale_rows(matrix, multiplicities, carrier_dimensions):
        scale = np.empty(103)
        offset = 0
        for multiplicity, carrier in zip(multiplicities,
                                         carrier_dimensions):
            scale[offset:offset + multiplicity * multiplicity] = np.sqrt(carrier)
            offset += multiplicity * multiplicity
        assert offset == 103
        return scale[:, None] * matrix

    return (scale_rows(hol_matrix, cross.HOL_MULTS,
                       cross.HOL_CARRIER_DIMS),
            scale_rows(mixed_matrix, cross.MIXED_MULTS,
                       cross.MIXED_CARRIER_DIMS))


def mode_cube(matrix, tensor):
    return primal.crossing_apply(matrix, tensor)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate",
                        default="/tmp/dth_constrained_obstruction_theta018_sym.npz")
    parser.add_argument("--output",
                        default="/tmp/dth_obstruction_diagram_metadata.npz")
    args = parser.parse_args()

    crossing_data, hol, mixed = cross.local_crossing(verbose=False)
    local, _, _ = primal.normalized_local_crossing(crossing_data)
    selected = BRIDGE.SELECTED_PERMUTATIONS
    hol_restriction, mixed_restriction = normalized_restriction(
        selected, hol, mixed)
    bridge_error = la.norm(mixed_restriction - local @ hol_restriction, ord=2)
    condition = np.linalg.cond(hol_restriction)

    data = np.load(args.candidate)
    x = data["x"]
    z = data["z"]
    inverse = la.inv(hol_restriction)
    diagram = mode_cube(inverse, x)
    reconstructed_x = mode_cube(hol_restriction, diagram)
    reconstructed_z = mode_cube(mixed_restriction, diagram)

    permutations_array = np.asarray(selected, dtype=np.int64)
    print("normalized exact-bridge error:", bridge_error)
    print("normalized hol restriction condition number:", condition)
    print("diagram tensor norm/max:", la.norm(diagram),
          np.max(np.abs(diagram)))
    print("hol reconstruction error:", la.norm(reconstructed_x - x))
    print("mixed reconstruction error:", la.norm(reconstructed_z - z))
    print("diagram S3 symmetry errors:",
          la.norm(diagram - diagram.transpose(1, 0, 2)),
          la.norm(diagram - diagram.transpose(0, 2, 1)))

    np.savez(args.output,
             diagram_coefficients=diagram,
             selected_permutations=permutations_array,
             normalized_hol_restriction=hol_restriction,
             normalized_mixed_restriction=mixed_restriction,
             normalized_local_crossing=local,
             x=x, z=z,
             theta=data["theta"], objective=data["objective"],
             hol_reconstruction_error=np.array(la.norm(reconstructed_x - x)),
             mixed_reconstruction_error=np.array(la.norm(reconstructed_z - z)),
             bridge_error=np.array(bridge_error),
             hol_condition=np.array(condition))


if __name__ == "__main__":
    main()
