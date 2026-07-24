#!/usr/bin/env python3
"""Numerically test a discovered rank-five K7 catalog against exact nu."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text())
    lines = args.catalog.read_text().splitlines()
    assert lines and lines[0].startswith("# ")
    edges = []
    features = []
    for line in lines[1:]:
        fields = tuple(map(int, line.split(",")))
        assert len(fields) == 56
        edges.append(fields[:21])
        features.append(fields[21:])

    row_indices = [0] * len(features)
    column_indices = list(range(len(features)))
    values = [1.0] * len(features)
    for column, feature in enumerate(features):
        counts = np.bincount(feature, minlength=51)
        for index in np.flatnonzero(counts):
            row_indices.append(1 + int(index))
            column_indices.append(column)
            values.append(float(counts[index]))
    matrix = csc_matrix(
        (values, (row_indices, column_indices)),
        shape=(52, len(features)),
    )
    nu = np.array(
        [float(__import__("fractions").Fraction(value)) for value in source["nu"]]
    )
    target = np.concatenate(([1.0], 7.0 * nu / 312.0))
    result = linprog(
        np.zeros(len(features)),
        A_eq=matrix,
        b_eq=target,
        bounds=(0.0, None),
        method="highs",
    )
    active = (
        np.flatnonzero(result.x > 1e-10).tolist()
        if result.success
        else []
    )
    report = {
        "status": "NUMERICAL EVIDENCE ONLY",
        "catalog_header": lines[0],
        "catalog_columns": len(features),
        "solver": "scipy.optimize.linprog(method='highs')",
        "success": bool(result.success),
        "message": result.message,
        "maximum_equality_residual": (
            float(np.max(np.abs(matrix @ result.x - target)))
            if result.success
            else None
        ),
        "active_columns": active,
        "active_weights": (
            [float(result.x[index]) for index in active]
            if result.success
            else []
        ),
        "active_edges": [edges[index] for index in active],
        "warning": (
            "Feasible floating weights require exact reconstruction; "
            "infeasibility applies only to this discovered subcatalog."
        ),
    }
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
