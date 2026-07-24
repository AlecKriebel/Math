#!/usr/bin/env python3
"""Test weighted two-design feasibility on unrestricted 41-point near codes.

The inputs are existing construction artifacts from several independent
search mechanisms.  Linear programming asks whether zero lies in the convex
hull of the degree-one/traceless-degree-two feature vectors.  Results are
floating-point diagnostics, not exact proofs about the approximate inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Iterator

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSON_GLOBS = (
    "experiments/four_point_depth_projection/construction_homotopy_deflation/*.json",
    "experiments/four_point_depth_projection/construction_active_search/*.json",
    "experiments/construction_round10/results/*.json",
    "experiments/construction_round8_tight_frames/results/*.json",
    "experiments/centered_tight_frame_endpoint/results/*.json",
)


def coordinate_arrays(value: object, path: str = "") -> Iterator[tuple[str, np.ndarray]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield from coordinate_arrays(child, f"{path}/{key}")
    elif isinstance(value, list):
        try:
            array = np.asarray(value, dtype=float)
        except (TypeError, ValueError):
            array = np.empty((0,))
        if array.shape == (41, 5):
            yield path, array
        else:
            for index, child in enumerate(value):
                if isinstance(child, (dict, list)):
                    yield from coordinate_arrays(child, f"{path}[{index}]")


def feature_matrix(x: np.ndarray) -> np.ndarray:
    """Rows span R^5 plus traceless Sym(5), a 19-dimensional feature space."""

    rows = [x[:, coordinate] for coordinate in range(5)]
    rows.extend(x[:, i] ** 2 - x[:, 4] ** 2 for i in range(4))
    rows.extend(
        x[:, i] * x[:, j]
        for i in range(5)
        for j in range(i + 1, 5)
    )
    matrix = np.asarray(rows)
    assert matrix.shape == (19, 41)
    return matrix


def analyze(x: np.ndarray) -> dict[str, object]:
    norms = np.linalg.norm(x, axis=1)
    normalized = x / norms[:, None]
    gram = normalized @ normalized.T
    np.fill_diagonal(gram, -math.inf)
    features = feature_matrix(normalized)
    equalities = np.vstack((np.ones(41), features))
    target = np.zeros(20)
    target[0] = 1.0

    feasible = linprog(
        np.zeros(41),
        A_eq=equalities,
        b_eq=target,
        bounds=(0.0, None),
        method="highs",
    )
    report: dict[str, object] = {
        "maximum_inner_product": float(np.max(gram)),
        "maximum_input_norm_error": float(np.max(np.abs(norms - 1.0))),
        "weighted_design_feasible": bool(feasible.success),
        "linprog_status": feasible.message,
    }
    if not feasible.success:
        return report

    weights = feasible.x
    residual = equalities @ weights - target
    report.update(
        {
            "one_feasible_support_size": int(np.count_nonzero(weights > 1e-9)),
            "one_feasible_minimum_positive_weight": float(
                np.min(weights[weights > 1e-9])
            ),
            "one_feasible_maximum_weight": float(np.max(weights)),
            "one_feasible_residual_inf": float(np.max(np.abs(residual))),
        }
    )

    # Maximize the minimum weight.  A positive optimum puts the target in the
    # relative interior of the convex hull and is more robust than a sparse
    # basic feasible solution.
    objective = np.zeros(42)
    objective[-1] = -1.0
    full_equalities = np.hstack((equalities, np.zeros((20, 1))))
    inequalities = np.zeros((41, 42))
    inequalities[np.arange(41), np.arange(41)] = -1.0
    inequalities[:, -1] = 1.0
    interior = linprog(
        objective,
        A_ub=inequalities,
        b_ub=np.zeros(41),
        A_eq=full_equalities,
        b_eq=target,
        bounds=[(0.0, None)] * 42,
        method="highs",
    )
    report["full_support_optimization_success"] = bool(interior.success)
    if interior.success:
        report["maximum_common_weight_floor"] = float(interior.x[-1])
        report["full_support_residual_inf"] = float(
            np.max(np.abs(equalities @ interior.x[:-1] - target))
        )
    return report


def canonical_digest(x: np.ndarray) -> str:
    normalized = x / np.linalg.norm(x, axis=1)[:, None]
    return hashlib.sha256(np.round(normalized, 12).tobytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    candidates: list[tuple[str, np.ndarray]] = []
    input_path = ROOT / "experiments" / "input" / "spherical_codes_5_41.txt"
    candidates.append(
        (
            str(input_path.relative_to(ROOT)),
            np.loadtxt(input_path, delimiter=","),
        )
    )
    for pattern in DEFAULT_JSON_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            try:
                value = json.loads(path.read_text())
            except (json.JSONDecodeError, OSError):
                continue
            for json_path, array in coordinate_arrays(value):
                candidates.append(
                    (f"{path.relative_to(ROOT)}:{json_path}", array)
                )

    seen: set[str] = set()
    records = []
    for source, x in candidates:
        digest = canonical_digest(x)
        if digest in seen:
            continue
        seen.add(digest)
        report = analyze(x)
        report["source"] = source
        report["coordinate_digest_rounded_12_sha256"] = digest
        records.append(report)
        print(
            f"{report['maximum_inner_product']:.12f}",
            report["weighted_design_feasible"],
            report.get("maximum_common_weight_floor"),
            source,
            flush=True,
        )

    records.sort(key=lambda record: record["maximum_inner_product"])
    payload = {
        "status": "NUMERICAL EVIDENCE ONLY",
        "warning": (
            "The coordinates and LP calculations are floating point; this "
            "tests the conjecture but proves neither existence nor nonexistence."
        ),
        "numpy_version": np.__version__,
        "scipy_version": __import__("scipy").__version__,
        "records": records,
    }
    Path(args.output).write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
