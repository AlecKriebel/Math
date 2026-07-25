#!/usr/bin/env python3
"""Numerically impose the candidate centered radical and search the quotient."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import sys

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import csc_matrix, hstack, vstack


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
CATALOG = (
    ROOT
    / "experiments"
    / "root_triangle_k7_overlap"
    / "expanded_k7_catalog.csv"
)
MOMENTS = (
    ROOT
    / "experiments"
    / "root_triangle_k7_overlap"
    / "expanded_degree3_moments.npz"
)
RADICAL = (
    ROOT
    / "experiments"
    / "root_triangle_k7_overlap"
    / "centered_degree3_radical.json"
)


def scaled_rows(matrix):
    scale = np.max(np.abs(matrix), axis=1)
    nonzero = scale != 0
    return matrix[nonzero] / scale[nonzero, None], scale[nonzero], int(
        np.count_nonzero(~nonzero)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--max-iterations", type=int, default=250)
    parser.add_argument("--cuts-per-iteration", type=int, default=12)
    parser.add_argument("--tolerance", type=float, default=2e-9)
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text())
    radical = json.loads(RADICAL.read_text())
    kernels = np.asarray(radical["radical_vectors"], dtype=float).T
    quotient_indices = tuple(radical["quotient_coordinate_indices"])
    if kernels.shape != (48, 26) or len(quotient_indices) != 22:
        raise RuntimeError("wrong radical dimensions")
    complement = np.eye(48)[:, quotient_indices]
    if np.linalg.matrix_rank(np.hstack((kernels, complement))) != 48:
        raise RuntimeError("radical and quotient coordinates do not span")

    lines = CATALOG.read_text().splitlines()
    triangle_counts = np.asarray(
        [
            np.bincount(
                tuple(map(int, line.split(",")))[21:],
                minlength=51,
            )
            for line in lines[1:]
        ],
        dtype=float,
    ).T
    moments_integer = np.load(MOMENTS)["moments"]
    if moments_integer.shape != (len(lines) - 1, 48, 48):
        raise RuntimeError("moment cache shape mismatch")
    moment_scale = float(np.max(np.abs(moments_integer)))
    moments = moments_integer.astype(float) / moment_scale

    source_nu = np.asarray([float(Q(value)) for value in source["nu"]])
    marginal_matrix = np.vstack(
        (np.ones(len(lines) - 1), triangle_counts)
    )
    marginal_target = np.concatenate(([1.0], 7.0 * source_nu / 312.0))

    kernel_quotient = np.einsum(
        "ir,aij,jq->arq", kernels, moments, complement
    ).reshape(len(lines) - 1, -1).T
    kernel_kernel_full = np.einsum(
        "ir,aij,js->ars", kernels, moments, kernels
    )
    upper = tuple(
        (row, column)
        for row in range(26)
        for column in range(row, 26)
    )
    kernel_kernel = np.asarray(
        [
            kernel_kernel_full[:, row, column]
            for row, column in upper
        ]
    )
    radical_rows = np.vstack((kernel_quotient, kernel_kernel))
    radical_rows, radical_scales, zero_radical_rows = scaled_rows(
        radical_rows
    )
    equality = csc_matrix(np.vstack((marginal_matrix, radical_rows)))
    target = np.concatenate(
        (
            marginal_target,
            np.zeros(radical_rows.shape[0]),
        )
    )

    feasibility = linprog(
        np.zeros(len(lines) - 1),
        A_eq=equality,
        b_eq=target,
        bounds=(0.0, None),
        method="highs",
        options={
            "dual_feasibility_tolerance": 1e-9,
            "primal_feasibility_tolerance": 1e-9,
        },
    )
    history = []
    if not feasibility.success:
        report = {
            "status": "NUMERICAL EVIDENCE ONLY",
            "success": False,
            "stage": "radical feasibility",
            "message": feasibility.message,
            "catalog_atoms": len(lines) - 1,
            "radical_rows": radical_rows.shape[0],
        }
        args.output.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))
        return

    quotient_moments = moments[:, quotient_indices][:, :, quotient_indices]
    dimension = len(quotient_indices)
    cut_vectors = [np.eye(dimension)[index] for index in range(dimension)]
    cut_keys = {tuple(vector) for vector in cut_vectors}
    solution = feasibility.x
    eigenvalues = None
    for iteration in range(args.max_iterations):
        cut_rows = np.asarray(
            [
                -np.einsum(
                    "i,aij,j->a",
                    vector,
                    quotient_moments,
                    vector,
                )
                for vector in cut_vectors
            ]
        )
        inequalities = hstack(
            (
                csc_matrix(cut_rows),
                csc_matrix(np.ones((len(cut_vectors), 1))),
            ),
            format="csc",
        )
        equality_with_margin = hstack(
            (
                equality,
                csc_matrix((equality.shape[0], 1)),
            ),
            format="csc",
        )
        objective = np.zeros(len(lines))
        objective[-1] = -1
        result = linprog(
            objective,
            A_ub=inequalities,
            b_ub=np.zeros(len(cut_vectors)),
            A_eq=equality_with_margin,
            b_eq=target,
            bounds=[(0.0, None)] * (len(lines) - 1) + [(None, None)],
            method="highs",
            options={
                "dual_feasibility_tolerance": 1e-9,
                "primal_feasibility_tolerance": 1e-9,
            },
        )
        if not result.success:
            history.append(
                {
                    "iteration": iteration,
                    "success": False,
                    "message": result.message,
                }
            )
            break
        solution = result.x[:-1]
        margin = result.x[-1]
        aggregate = np.einsum(
            "a,aij->ij", solution, quotient_moments
        )
        aggregate = (aggregate + aggregate.T) / 2
        eigenvalues, eigenvectors = np.linalg.eigh(aggregate)
        item = {
            "iteration": iteration,
            "cuts": len(cut_vectors),
            "claimed_margin": float(margin),
            "actual_minimum_eigenvalue": float(eigenvalues[0]),
            "active_atoms": int(np.count_nonzero(solution > 1e-10)),
            "equality_residual": float(
                np.max(np.abs(equality @ solution - target))
            ),
        }
        history.append(item)
        print(json.dumps(item), flush=True)
        if eigenvalues[0] >= margin - args.tolerance:
            break
        added = 0
        for index in np.argsort(eigenvalues):
            if eigenvalues[index] >= margin - args.tolerance:
                break
            vector = eigenvectors[:, index]
            sign_index = int(np.argmax(np.abs(vector)))
            if vector[sign_index] < 0:
                vector = -vector
            key = tuple(np.round(vector, 12))
            if key in cut_keys:
                continue
            cut_keys.add(key)
            cut_vectors.append(vector)
            added += 1
            if added == args.cuts_per_iteration:
                break
        if added == 0:
            break

    active = np.flatnonzero(solution > 1e-10).tolist()
    report = {
        "status": "NUMERICAL EVIDENCE ONLY",
        "scope_warning": (
            "The centered radical is not yet symbolically certified and "
            "the expanded K7 catalog remains incomplete."
        ),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "solver": "scipy.optimize.linprog(method='highs')",
        "catalog_atoms": len(lines) - 1,
        "feature_dimension": 48,
        "radical_dimension": 26,
        "quotient_dimension": 22,
        "radical_rows": radical_rows.shape[0],
        "identically_zero_radical_rows": zero_radical_rows,
        "radical_feasibility": "PASS",
        "history": history,
        "final_eigenvalues": (
            [float(value) for value in eigenvalues]
            if eigenvalues is not None
            else None
        ),
        "active_columns": active,
        "active_weights": [float(solution[index]) for index in active],
        "active_edges": [
            list(map(int, lines[1 + index].split(",")))[:21]
            for index in active
        ],
        "moment_scale": moment_scale,
        "radical_row_scales": [float(value) for value in radical_scales],
    }
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(
        json.dumps(
            {
                key: value
                for key, value in report.items()
                if key
                not in {
                    "history",
                    "active_weights",
                    "active_edges",
                    "radical_row_scales",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
