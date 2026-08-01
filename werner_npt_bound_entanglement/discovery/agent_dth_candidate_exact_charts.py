#!/usr/bin/env python3
"""Convert a numerical DTH tensor to the exact rational support charts.

This is discovery/conversion code.  It does not round or certify the output.
For the holomorphic side it writes the small matrices ``A_ijk`` for which

    h_ijk = E_ijk A_ijk E_ijk.T,

where ``E_ijk`` is returned by
``verification/agent_dth_exact_k_coordinates.py``.  The input solver tensor
uses Hilbert--Schmidt normalized orthonormal highest-weight coordinates; the
conversion removes the square-root carrier weight and applies the exact-
Specht-to-orthonormal change of basis before solving for ``A``.

Shape triples are ordered by physical sites (0,1,2), and tensor-product
multiplicity indices use lexicographic order ``(a0,a1,a2)``.  This is also
the order used by the exact crossing bridge.
"""

from __future__ import annotations

import argparse
import importlib.util
from itertools import product
from pathlib import Path
import sys

import numpy as np
import scipy.linalg as la


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import agent_dth_invariant_crossing as CROSS


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


EXACT_K = import_file(
    "dth_exact_k_coordinates",
    ROOT / "verification" / "agent_dth_exact_k_coordinates.py",
)
BRIDGE = EXACT_K.BRIDGE


def block_ranges(multiplicities):
    result = []
    offset = 0
    for multiplicity in multiplicities:
        result.append(
            np.arange(offset, offset + multiplicity * multiplicity).reshape(
                multiplicity, multiplicity
            )
        )
        offset += multiplicity * multiplicity
    assert offset == 103
    return result


def block_indices(ranges, shapes):
    grids = [ranges[shape] for shape in shapes]
    return (
        grids[0][:, None, None, :, None, None],
        grids[1][None, :, None, None, :, None],
        grids[2][None, None, :, None, None, :],
    )


def get_block(tensor, ranges, shapes, multiplicities):
    dimensions = tuple(multiplicities[shape] for shape in shapes)
    size = int(np.prod(dimensions))
    return tensor[block_indices(ranges, shapes)].reshape(size, size)


def exact_to_orthonormal_changes():
    exact = BRIDGE.holomorphic_highest_weight_bases()
    orthonormal = CROSS.hol_highest_weight_bases()
    changes = []
    for exact_basis, numerical_basis in zip(exact, orthonormal):
        raw = np.zeros_like(numerical_basis)
        for column, vector in enumerate(exact_basis):
            for row, value in vector.items():
                raw[row, column] = float(value)
        change = numerical_basis.T @ raw
        error = la.norm(numerical_basis @ change - raw)
        assert error < 1e-11
        changes.append(change)
    return changes


def convert_holomorphic(tensor):
    ranges = block_ranges(CROSS.HOL_MULTS)
    changes = exact_to_orthonormal_changes()
    output = {}
    maximum_range_residual = 0.0
    minimum_coordinate_eigenvalue = np.inf
    for shapes in product(range(5), repeat=3):
        solver_block = get_block(
            tensor, ranges, shapes, CROSS.HOL_MULTS
        )
        solver_block = (solver_block + solver_block.T) / 2
        carrier = np.prod([
            CROSS.HOL_CARRIER_DIMS[shape] for shape in shapes
        ])
        orthonormal_restriction = solver_block / np.sqrt(carrier)
        change = np.kron(
            np.kron(changes[shapes[0]], changes[shapes[1]]),
            changes[shapes[2]],
        )
        exact_restriction = (
            change.T @ orthonormal_restriction @ change
        )

        _, _, exact_range = EXACT_K.hol_k_coordinates(shapes)
        range_float = np.asarray(exact_range, dtype=float)
        if not range_float.shape[1]:
            assert la.norm(exact_restriction) < 2e-13
            coordinate = np.zeros((0, 0))
            residual = la.norm(exact_restriction)
        else:
            left_inverse = la.pinv(range_float)
            coordinate = left_inverse @ exact_restriction @ left_inverse.T
            coordinate = (coordinate + coordinate.T) / 2
            residual = la.norm(
                range_float @ coordinate @ range_float.T
                - exact_restriction
            )
            minimum_coordinate_eigenvalue = min(
                minimum_coordinate_eigenvalue,
                float(la.eigvalsh(coordinate)[0]),
            )
        maximum_range_residual = max(maximum_range_residual, residual)
        tag = "".join(map(str, shapes))
        output["A_" + tag] = coordinate
        output["range_residual_" + tag] = np.array(residual)

    output["maximum_range_residual"] = np.array(maximum_range_residual)
    output["minimum_coordinate_eigenvalue"] = np.array(
        minimum_coordinate_eigenvalue
    )
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--field", default="x")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    data = np.load(args.input)
    converted = convert_holomorphic(data[args.field])
    np.savez(args.output, **converted)
    print("wrote", args.output)
    print("maximum exact-K range residual:",
          float(converted["maximum_range_residual"]))
    print("minimum coordinate eigenvalue:",
          float(converted["minimum_coordinate_eigenvalue"]))


if __name__ == "__main__":
    main()
