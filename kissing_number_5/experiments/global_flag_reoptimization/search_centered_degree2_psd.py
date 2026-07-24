#!/usr/bin/env python3
"""Numerical search for the centered full degree-two rooted-edge block.

Eleven exact centered root-sum identities are imposed as zero-square
equalities.  Minimum-eigenvector cuts then enforce the full 18 by 18 block,
while a seven-coordinate complement is given a positive margin.  This is a
discovery program only.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import csc_matrix, hstack, vstack

from experiments.global_flag_reoptimization.search_degree2_psd import (
    CATALOG,
    DIMENSION,
    FEATURE_NAMES,
    SOURCE,
    Search,
)


def vector(**entries):
    result = np.zeros(DIMENSION)
    for name, value in entries.items():
        result[FEATURE_NAMES.index(name)] = value
    return result


CENTERED_KERNELS = (
    vector(**{"1": 152, "q": 38, "a+c": 741}),
    vector(**{"1": 152, "q": 38, "b+d": 741}),
    vector(**{"1": 74, "q": -1, "e": 741}),
    vector(**{"q": 152, "q^2": 38, "q*(a+c)": 741}),
    vector(**{"q": 152, "q^2": 38, "q*(b+d)": 741}),
    vector(**{"q": 74, "q^2": -1, "q*e": 741}),
    vector(
        **{
            "1": -608,
            "q": -304,
            "q^2": -38,
            "a^2+c^2": 741,
            "a*c": 56316,
        }
    ),
    vector(
        **{
            "1": -608,
            "q": -304,
            "q^2": -38,
            "b^2+d^2": 741,
            "b*d": 56316,
        }
    ),
    vector(
        **{
            "1": -608,
            "q": -304,
            "q^2": -38,
            "a*b+c*d": 741,
            "a*d+b*c": 28158,
        }
    ),
    vector(
        **{
            "a+c": 4,
            "e*(a+c)": 38,
            "a^2+c^2": 1,
            "a*b+c*d": 1,
        }
    ),
    vector(
        **{
            "b+d": 4,
            "e*(b+d)": 38,
            "b^2+d^2": 1,
            "a*b+c*d": 1,
        }
    ),
)

# Root-summed quantities not eliminated by the centered identities.
QUOTIENT_INDICES = tuple(
    FEATURE_NAMES.index(name)
    for name in (
        "1",
        "q",
        "q^2",
        "e^2",
        "a^2+c^2",
        "b^2+d^2",
        "a*b+c*d",
    )
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--iterations", type=int, default=80)
    parser.add_argument("--batch-cuts", type=int, default=8)
    args = parser.parse_args()

    search = Search(args.catalog, args.source)
    coordinate_rows = []
    scales = []
    for index in range(DIMENSION):
        direction = np.zeros(DIMENSION)
        direction[index] = 1
        row = search.direction_row(direction)
        coordinate_rows.append(row)
        scales.append(np.sqrt(max(abs(row))))
        print("coordinate", index, FEATURE_NAMES[index], flush=True)
    scales = np.asarray(scales)

    kernel_rows = []
    for index, kernel in enumerate(CENTERED_KERNELS):
        row = search.direction_row(kernel / np.linalg.norm(kernel))
        kernel_rows.append(row / max(abs(row)))
        print("centered_kernel", index, flush=True)

    equality_matrix = vstack(
        [search.equalities, np.asarray(kernel_rows)], format="csc"
    )
    equality_target = np.concatenate(
        (search.target, np.zeros(len(kernel_rows)))
    )
    equality_matrix = hstack(
        [
            equality_matrix,
            csc_matrix((equality_matrix.shape[0], 1)),
        ],
        format="csc",
    )

    full_rows = [
        row / (scale * scale)
        for row, scale in zip(coordinate_rows, scales)
    ]
    quotient_rows = [
        coordinate_rows[index] / (scales[index] ** 2)
        for index in QUOTIENT_INDICES
    ]
    history = []
    solution = None
    for iteration in range(args.iterations):
        inequality_rows = [
            np.concatenate((-row, [0.0])) for row in full_rows
        ] + [
            np.concatenate((-row, [1.0])) for row in quotient_rows
        ]
        objective = np.concatenate(
            (np.zeros(search.column_count), [-1.0])
        )
        started = time.time()
        result = linprog(
            objective,
            A_ub=csc_matrix(np.asarray(inequality_rows)),
            b_ub=np.zeros(len(inequality_rows)),
            A_eq=equality_matrix,
            b_eq=equality_target,
            bounds=[(0, None)] * search.column_count + [(-10, 10)],
            method="highs",
        )
        if not result.success:
            raise RuntimeError(result.message)
        weights = result.x[:-1]
        support = np.flatnonzero(weights > 1e-10)
        matrix = search.aggregate_matrix(
            support, weights[support], scales
        )
        full_eigenvalues, full_eigenvectors = np.linalg.eigh(matrix)
        quotient = matrix[np.ix_(QUOTIENT_INDICES, QUOTIENT_INDICES)]
        quotient_eigenvalues, quotient_eigenvectors = np.linalg.eigh(quotient)
        record = {
            "iteration": iteration,
            "full_cuts": len(full_rows),
            "quotient_cuts": len(quotient_rows),
            "margin": float(result.x[-1]),
            "full_eigenvalues": full_eigenvalues.tolist(),
            "quotient_eigenvalues": quotient_eigenvalues.tolist(),
            "active_columns": len(support),
            "seconds": time.time() - started,
        }
        history.append(record)
        print(json.dumps(record), flush=True)
        solution = (result, support, matrix)

        bad_full = [
            index
            for index, value in enumerate(full_eigenvalues)
            if value < -1e-7
        ][: args.batch_cuts]
        bad_quotient = [
            index
            for index, value in enumerate(quotient_eigenvalues)
            if value < result.x[-1] - 1e-7
        ][: args.batch_cuts]
        if not bad_full and not bad_quotient:
            break
        for index in bad_full:
            direction = full_eigenvectors[:, index] / scales
            full_rows.append(search.direction_row(direction))
        for index in bad_quotient:
            normalized = np.zeros(DIMENSION)
            normalized[list(QUOTIENT_INDICES)] = quotient_eigenvectors[
                :, index
            ]
            direction = normalized / scales
            quotient_rows.append(search.direction_row(direction))

    assert solution is not None
    result, support, matrix = solution
    report = {
        "status": "NUMERICAL EVIDENCE ONLY",
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "solver": "scipy.optimize.linprog(method='highs')",
        "feature_names": FEATURE_NAMES,
        "centered_kernel_vectors": [
            vector.tolist() for vector in CENTERED_KERNELS
        ],
        "quotient_indices": QUOTIENT_INDICES,
        "history": history,
        "active_catalog_indices": search.catalog_indices[support].tolist(),
        "active_weights": result.x[support].tolist(),
        "final_normalized_matrix": matrix.tolist(),
        "warning": (
            "Floating feasibility is not a certificate. The finite atom "
            "catalog is incomplete."
        ),
    }
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
