#!/usr/bin/env python3
"""Numerical cutting-plane search for the full degree-two rooted-edge block.

Discovery only.  The search alternates a linear program over rank-five K6
atoms with the minimum eigenvector of the resulting 18 by 18 moment matrix.
Any positive output must be rationalized and checked by a separate exact
verifier.
"""

from __future__ import annotations

from fractions import Fraction as Q
import argparse
import itertools
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import csc_matrix, hstack


ROOT = Path(__file__).resolve().parents[2]
CATALOG = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "results"
    / "direct_k6_5000.csv"
)
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"

FEATURE_NAMES = (
    "1",
    "q",
    "e",
    "a+c",
    "b+d",
    "q^2",
    "q*e",
    "e^2",
    "q*(a+c)",
    "q*(b+d)",
    "e*(a+c)",
    "e*(b+d)",
    "a^2+c^2",
    "b^2+d^2",
    "a*b+c*d",
    "a*c",
    "b*d",
    "a*d+b*c",
)
DIMENSION = len(FEATURE_NAMES)
PAIRS6 = tuple(itertools.combinations(range(6), 2))
PAIR_INDEX6 = {pair: index for index, pair in enumerate(PAIRS6)}
LOCAL_PAIRS = tuple(itertools.combinations(range(4), 2))
KERNEL = np.array(
    [
        [
            {2: 494, 3: 9139, 4: 329004}[
                len(set(first) | set(second))
            ]
            for second in LOCAL_PAIRS
        ]
        for first in LOCAL_PAIRS
    ],
    dtype=np.int64,
)


def basis(q, a, b, c, d, e):
    """Return arrays in a full swap-(p,q)-invariant degree-two basis."""

    return (
        np.ones_like(q),
        q,
        e,
        a + c,
        b + d,
        q * q,
        q * e,
        e * e,
        q * (a + c),
        q * (b + d),
        e * (a + c),
        e * (b + d),
        a * a + c * c,
        b * b + d * d,
        a * b + c * d,
        a * c,
        b * d,
        a * d + b * c,
    )


class Search:
    def __init__(self, catalog: Path, source: Path):
        self.table = np.loadtxt(
            catalog, delimiter=",", dtype=np.int16, comments="#"
        )
        assert self.table.shape[1] == 35
        self.edges = self.table[:, :15]
        self.faces = self.table[:, 15:]
        self.column_count = len(self.table)
        self.catalog_indices = np.arange(self.column_count)
        self.equalities = self.build_equalities()
        source_data = json.loads(source.read_text())
        self.target = np.array(
            [1.0] + [float(Q(value) / 78) for value in source_data["nu"]]
        )

    def restrict(self, indices):
        indices = np.asarray(indices, dtype=int)
        self.table = self.table[indices]
        self.edges = self.table[:, :15]
        self.faces = self.table[:, 15:]
        self.catalog_indices = self.catalog_indices[indices]
        self.column_count = len(self.table)
        self.equalities = self.build_equalities()

    def edge_array(self, first, second, rows=None):
        values = (
            self.edges
            if rows is None
            else self.edges[np.asarray(rows, dtype=int)]
        )
        return (
            values[:, PAIR_INDEX6[tuple(sorted((first, second)))]].astype(
                np.int64
            )
            - 4
        )

    def build_equalities(self):
        rows = [0] * self.column_count
        columns = list(range(self.column_count))
        values = [1.0] * self.column_count
        for column, faces in enumerate(self.faces):
            counts = np.bincount(faces, minlength=51)
            for row in np.flatnonzero(counts):
                rows.append(1 + int(row))
                columns.append(column)
                values.append(float(counts[row]))
        return csc_matrix(
            (values, (rows, columns)), shape=(52, self.column_count)
        )

    def direction_row(self, coefficients):
        """Evaluate v^T M_atom v for every catalog atom."""

        coefficients = np.asarray(coefficients, dtype=float)
        assert coefficients.shape == (DIMENSION,)
        result = np.zeros(self.column_count)
        for first_root, second_root in itertools.permutations(range(6), 2):
            residual = [
                vertex
                for vertex in range(6)
                if vertex not in (first_root, second_root)
            ]
            q = self.edge_array(first_root, second_root)
            values = np.empty((self.column_count, 6))
            for position, (local_first, local_second) in enumerate(
                LOCAL_PAIRS
            ):
                first = residual[local_first]
                second = residual[local_second]
                a = self.edge_array(first_root, first)
                b = self.edge_array(second_root, first)
                c = self.edge_array(first_root, second)
                d = self.edge_array(second_root, second)
                e = self.edge_array(first, second)
                entries = basis(q, a, b, c, d, e)
                values[:, position] = sum(
                    coefficient * entry
                    for coefficient, entry in zip(coefficients, entries)
                )
            result += np.einsum(
                "ni,ij,nj->n", values, KERNEL, values, optimize=True
            )
        return result

    def bilinear_row(self, left_coefficients, right_coefficients):
        """Evaluate left^T M_atom right for every catalog atom."""

        left_coefficients = np.asarray(left_coefficients, dtype=float)
        right_coefficients = np.asarray(right_coefficients, dtype=float)
        result = np.zeros(self.column_count)
        for first_root, second_root in itertools.permutations(range(6), 2):
            residual = [
                vertex
                for vertex in range(6)
                if vertex not in (first_root, second_root)
            ]
            q = self.edge_array(first_root, second_root)
            left_values = np.empty((self.column_count, 6))
            right_values = np.empty((self.column_count, 6))
            for position, (local_first, local_second) in enumerate(
                LOCAL_PAIRS
            ):
                first = residual[local_first]
                second = residual[local_second]
                a = self.edge_array(first_root, first)
                b = self.edge_array(second_root, first)
                c = self.edge_array(first_root, second)
                d = self.edge_array(second_root, second)
                e = self.edge_array(first, second)
                entries = basis(q, a, b, c, d, e)
                left_values[:, position] = sum(
                    coefficient * entry
                    for coefficient, entry in zip(
                        left_coefficients, entries
                    )
                )
                right_values[:, position] = sum(
                    coefficient * entry
                    for coefficient, entry in zip(
                        right_coefficients, entries
                    )
                )
            result += np.einsum(
                "ni,ij,nj->n",
                left_values,
                KERNEL,
                right_values,
                optimize=True,
            )
        return result

    def aggregate_matrix(self, support, weights, scales):
        """Evaluate the normalized matrix only on the sparse active set."""

        support = np.asarray(support, dtype=int)
        weights = np.asarray(weights, dtype=float)
        result = np.zeros((DIMENSION, DIMENSION))
        for first_root, second_root in itertools.permutations(range(6), 2):
            residual = [
                vertex
                for vertex in range(6)
                if vertex not in (first_root, second_root)
            ]
            q = self.edge_array(first_root, second_root, support)
            values = np.empty((len(support), 6, DIMENSION))
            for position, (local_first, local_second) in enumerate(
                LOCAL_PAIRS
            ):
                first = residual[local_first]
                second = residual[local_second]
                a = self.edge_array(first_root, first, support)
                b = self.edge_array(second_root, first, support)
                c = self.edge_array(first_root, second, support)
                d = self.edge_array(second_root, second, support)
                e = self.edge_array(first, second, support)
                values[:, position, :] = np.stack(
                    basis(q, a, b, c, d, e), axis=1
                ) / scales
            kernel_values = np.einsum(
                "ij,njk->nik", KERNEL, values, optimize=True
            )
            result += np.einsum(
                "n,nki,nkj->ij",
                weights,
                values,
                kernel_values,
                optimize=True,
            )
        return (result + result.T) / 2


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
    for index in range(DIMENSION):
        direction = np.zeros(DIMENSION)
        direction[index] = 1
        coordinate_rows.append(search.direction_row(direction))
        print("coordinate", index, FEATURE_NAMES[index], flush=True)
    scales = np.sqrt(
        np.array([max(abs(row)) for row in coordinate_rows], dtype=float)
    )
    normalized_rows = [row / (scale * scale) for row, scale in zip(coordinate_rows, scales)]
    directions = [np.eye(DIMENSION)[index] for index in range(DIMENSION)]

    equality_matrix = hstack(
        [
            search.equalities,
            csc_matrix((search.equalities.shape[0], 1)),
        ],
        format="csc",
    )
    history = []
    solution = None
    for iteration in range(args.iterations):
        inequalities = csc_matrix(
            np.array(
                [
                    np.concatenate((-row, [1.0]))
                    for row in normalized_rows
                ]
            )
        )
        objective = np.concatenate(
            (np.zeros(search.column_count), [-1.0])
        )
        started = time.time()
        result = linprog(
            objective,
            A_ub=inequalities,
            b_ub=np.zeros(len(normalized_rows)),
            A_eq=equality_matrix,
            b_eq=search.target,
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
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        record = {
            "iteration": iteration,
            "cuts": len(normalized_rows),
            "margin": float(result.x[-1]),
            "eigenvalues": eigenvalues.tolist(),
            "active_columns": len(support),
            "seconds": time.time() - started,
        }
        history.append(record)
        print(json.dumps(record), flush=True)
        solution = (result, support, matrix)
        if eigenvalues[0] >= result.x[-1] - 1e-7:
            break
        violating = [
            index
            for index, value in enumerate(eigenvalues)
            if value < result.x[-1] - 1e-7
        ][: args.batch_cuts]
        for index in violating:
            direction = eigenvectors[:, index]
            raw_direction = direction / scales
            new_row = search.direction_row(raw_direction)
            normalized_rows.append(new_row)
            directions.append(direction)

    assert solution is not None
    result, support, matrix = solution
    report = {
        "status": "NUMERICAL EVIDENCE ONLY",
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "solver": "scipy.optimize.linprog(method='highs')",
        "feature_names": FEATURE_NAMES,
        "catalog_columns": search.column_count,
        "history": history,
        "active_catalog_indices": search.catalog_indices[support].tolist(),
        "active_weights": result.x[support].tolist(),
        "final_normalized_matrix": matrix.tolist(),
        "warning": (
            "Floating feasibility is not a certificate. Rationalize and "
            "verify independently."
        ),
    }
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
