#!/usr/bin/env python3
"""Exactly reconstruct a discovered direct rank-five K6 triangle extension."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import qr


ROOT = Path(__file__).resolve().parents[2]
RATIONALIZE_DIR = ROOT / "experiments" / "centered_atomic_bv_barrier"
sys.path.insert(0, str(RATIONALIZE_DIR))
from rationalize import qstr, solve_square  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path)
    parser.add_argument("numerical_report", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.catalog = args.catalog.resolve()
    args.numerical_report = args.numerical_report.resolve()
    args.output = args.output.resolve()

    source_path = (
        ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
    )
    source = json.loads(source_path.read_text())
    report = json.loads(args.numerical_report.read_text())
    assert report["success"]
    active = report["active_columns"]
    assert len(active) == 51

    lines = args.catalog.read_text().splitlines()
    header = lines[0]
    rows = []
    for line in lines[1:]:
        fields = tuple(map(int, line.split(",")))
        assert len(fields) == 35
        rows.append((fields[:15], fields[15:]))
    selected = [rows[index] for index in active]

    # A has normalization followed by the 51 triangle-count rows.
    matrix_all: list[list[Q]] = [[Q(1)] * len(selected)]
    for triangle_index in range(51):
        matrix_all.append(
            [
                Q(feature.count(triangle_index))
                for _edges, feature in selected
            ]
        )
    target_all = [Q(1)] + [Q(value) / 78 for value in source["nu"]]
    floating = np.array(
        [[float(value) for value in row] for row in matrix_all]
    )
    assert np.linalg.matrix_rank(floating) == len(selected)
    _q, _r, row_permutation = qr(
        floating.T, mode="economic", pivoting=True
    )
    independent_rows = tuple(
        int(index) for index in row_permutation[: len(selected)]
    )
    matrix = [matrix_all[index] for index in independent_rows]
    target = [target_all[index] for index in independent_rows]
    weights = solve_square(matrix, target)
    assert all(weight > 0 for weight in weights)
    assert all(
        sum(
            coefficient * weight
            for coefficient, weight in zip(row, weights, strict=True)
        )
        == target_value
        for row, target_value in zip(matrix_all, target_all, strict=True)
    )

    atoms = [
        {
            "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45": list(
                edges
            ),
            "triangle_orbit_indices": list(feature),
            "weight": qstr(weight),
        }
        for (edges, feature), weight in zip(selected, weights, strict=True)
    ]
    certificate = {
        "schema": "kissing5.centered_quarter_direct_k6_triangle_extension.v1",
        "status": (
            "exact symmetric local rank-five Gram-PSD K6 triangle-marginal "
            "extension; not a code and not a six-point Lasserre certificate"
        ),
        "source_certificate": str(source_path.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "grid": source["grid"],
        "normalization": (
            "atom weights sum to 1; expected count of each triangle type "
            "among the twenty faces is nu/78, so the uniform triangle-face "
            "marginal is nu/1560"
        ),
        "discovery_catalog": str(args.catalog.relative_to(ROOT)),
        "discovery_catalog_header": header,
        "discovery_catalog_sha256": hashlib.sha256(
            args.catalog.read_bytes()
        ).hexdigest(),
        "discovery_numerical_report": str(
            args.numerical_report.relative_to(ROOT)
        ),
        "discovery_numerical_report_sha256": hashlib.sha256(
            args.numerical_report.read_bytes()
        ).hexdigest(),
        "independent_equation_rows": list(independent_rows),
        "positive_atom_count": len(atoms),
        "atoms": atoms,
        "scope_warning": (
            "This proves feasibility only for symmetrized pair/triangle "
            "marginals on local K6 atoms. It does not realize a global "
            "41-point code or establish higher-order consistency."
        ),
    }
    args.output.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    )
    print(args.output)
    print(hashlib.sha256(args.output.read_bytes()).hexdigest())
    print(
        "minimum_weight",
        min(weights),
        "maximum_weight",
        max(weights),
    )


if __name__ == "__main__":
    main()
