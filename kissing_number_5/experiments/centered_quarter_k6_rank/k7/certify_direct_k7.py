#!/usr/bin/env python3
"""Exactly reconstruct the discovered direct rank-five K7 mixture."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import qr


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
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
    rows = []
    for line in lines[1:]:
        fields = tuple(map(int, line.split(",")))
        assert len(fields) == 56
        rows.append((fields[:21], fields[21:]))
    selected = [rows[index] for index in active]

    matrix_all: list[list[Q]] = [[Q(1)] * len(selected)]
    for triangle_index in range(51):
        matrix_all.append(
            [
                Q(feature.count(triangle_index))
                for _edges, feature in selected
            ]
        )
    target_all = [Q(1)] + [
        Q(7) * Q(value) / 312 for value in source["nu"]
    ]
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
    weights = solve_square(
        [matrix_all[index] for index in independent_rows],
        [target_all[index] for index in independent_rows],
    )
    assert all(weight > 0 for weight in weights)
    assert all(
        sum(
            coefficient * weight
            for coefficient, weight in zip(row, weights, strict=True)
        )
        == target
        for row, target in zip(matrix_all, target_all, strict=True)
    )

    k6_path = HERE.parent / "direct_k6_triangle_extension.json"
    atoms = [
        {
            "edge_color_indices_01_02_03_04_05_06_12_13_14_15_16_23_24_25_26_34_35_36_45_46_56": list(
                edges
            ),
            "triangle_orbit_indices": list(feature),
            "weight": qstr(weight),
        }
        for (edges, feature), weight in zip(selected, weights, strict=True)
    ]
    certificate = {
        "schema": "kissing5.centered_quarter_direct_k7_triangle_extension.v1",
        "status": (
            "exact symmetric local rank-five Gram-PSD K7 triangle-marginal "
            "extension; not a code and not a seven-point Lasserre certificate"
        ),
        "source_certificate": str(source_path.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "generation_k6_certificate": str(k6_path.relative_to(ROOT)),
        "generation_k6_sha256": hashlib.sha256(k6_path.read_bytes()).hexdigest(),
        "grid": source["grid"],
        "normalization": (
            "atom weights sum to 1; expected count of each triangle type "
            "among the thirty-five faces is 7*nu/312, so the uniform "
            "triangle-face marginal is nu/1560"
        ),
        "discovery_catalog": str(args.catalog.relative_to(ROOT)),
        "discovery_catalog_header": lines[0],
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
            "marginals on local K7 atoms. It does not realize a global "
            "41-point code or establish consistency between overlapping "
            "K7 atoms."
        ),
    }
    args.output.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    )
    print(args.output)
    print(hashlib.sha256(args.output.read_bytes()).hexdigest())
    print("minimum_weight", min(weights), "maximum_weight", max(weights))


if __name__ == "__main__":
    main()
