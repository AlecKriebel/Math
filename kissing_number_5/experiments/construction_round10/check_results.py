#!/usr/bin/env python3
"""Independent binary64 consistency checker for construction round 10.

This checker establishes only that the JSON faithfully records the numerical
arrays and diagnostics claimed by the discovery program.  It does not turn a
floating-point near miss into a rigorous spherical-code certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


def normalized(array: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(array, axis=1)
    if array.ndim != 2 or array.shape[1] != 5 or float(np.min(norms)) <= 1e-13:
        raise AssertionError("invalid coordinate matrix")
    return array / norms[:, None]


def independently_enumerate_shell(name: str) -> tuple[np.ndarray, list[dict]]:
    def enumerate_d(dimension: int) -> tuple[np.ndarray, list[dict]]:
        rows = []
        labels = []
        for first in range(dimension):
            for second in range(first + 1, dimension):
                for sign_first in (-1, 1):
                    for sign_second in (-1, 1):
                        row = np.zeros(dimension)
                        row[first] = sign_first / np.sqrt(2.0)
                        row[second] = sign_second / np.sqrt(2.0)
                        rows.append(row)
                        labels.append(
                            {
                                "kind": f"D{dimension}",
                                "support": [first, second],
                                "signs": [sign_first, sign_second],
                            }
                        )
        return np.asarray(rows), labels

    if name in ("D6", "D7"):
        return enumerate_d(int(name[1:]))
    if name != "E6":
        raise AssertionError("unrecognized shell")
    d5, d5_labels = enumerate_d(5)
    rows = [np.r_[row, 0.0] for row in d5]
    labels = [
        {"kind": "E6_D5", **{k: v for k, v in label.items() if k != "kind"}}
        for label in d5_labels
    ]
    for mask in range(32):
        signs = np.asarray(
            [1 if (mask >> coordinate) & 1 else -1 for coordinate in range(5)]
        )
        sixth = int(np.prod(signs))
        rows.append(
            np.r_[signs / 2.0, sixth * np.sqrt(3.0) / 2.0] / np.sqrt(2.0)
        )
        labels.append(
            {
                "kind": "E6_half",
                "signs_first5": signs.astype(int).tolist(),
                "sign6": sixth,
            }
        )
    return np.asarray(rows), labels


def recompute(array: np.ndarray) -> dict:
    x = normalized(array)
    n = len(x)
    gram = x @ x.T
    values = gram[np.triu_indices(n, 1)]
    eigenvalues = np.linalg.eigvalsh(gram)
    return {
        "n": n,
        "maximum_inner_product": float(np.max(values)),
        "gap_above_one_half": float(np.max(values)) - 0.5,
        "minimum_inner_product": float(np.min(values)),
        "unit_norm_residual": float(
            np.max(np.abs(np.sum(x * x, axis=1) - 1.0))
        ),
        "gram_top_five_eigenvalues": eigenvalues[-5:],
        "gram_null_spectrum_maximum_absolute": float(
            np.max(np.abs(eigenvalues[:-5]))
        ),
        "coordinate_little_endian_float64_sha256": hashlib.sha256(
            np.asarray(x, dtype="<f8").tobytes()
        ).hexdigest(),
    }


def close(first: float, second: float, tolerance: float = 5e-12) -> None:
    if not np.isfinite(first) or not np.isfinite(second):
        raise AssertionError("nonfinite diagnostic")
    if abs(first - second) > tolerance * max(1.0, abs(first), abs(second)):
        raise AssertionError(f"diagnostic mismatch: {first} versus {second}")


def check_diagnostics(array: np.ndarray, stored: dict) -> None:
    actual = recompute(array)
    if actual["n"] != stored["n"]:
        raise AssertionError("wrong point count")
    for key in (
        "maximum_inner_product",
        "gap_above_one_half",
        "minimum_inner_product",
        "unit_norm_residual",
        "gram_null_spectrum_maximum_absolute",
    ):
        close(actual[key], stored[key])
    if not np.allclose(
        actual["gram_top_five_eigenvalues"],
        stored["gram_top_five_eigenvalues"],
        atol=5e-12,
        rtol=5e-12,
    ):
        raise AssertionError("Gram spectrum mismatch")
    if (
        actual["coordinate_little_endian_float64_sha256"]
        != stored["coordinate_little_endian_float64_sha256"]
    ):
        raise AssertionError("coordinate hash mismatch")


def check_payload(payload: dict) -> dict:
    if payload.get("evidence_status") != (
        "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
    ):
        raise AssertionError("missing numerical-only status")
    if not payload.get("completed"):
        raise AssertionError("portfolio is not marked complete")
    structured_count = 0
    for run in payload["structured_runs"]:
        n = int(run["n"])
        roots, labels = independently_enumerate_shell(run["family"])
        indices = np.asarray(run["selected_root_indices"], dtype=int)
        if len(indices) != n or len(set(indices.tolist())) != n:
            raise AssertionError("structured subset is not exact cardinality")
        if int(np.min(indices)) < 0 or int(np.max(indices)) >= len(roots):
            raise AssertionError("root index outside shell")
        if [labels[int(index)] for index in indices] != run[
            "selected_root_labels"
        ]:
            raise AssertionError("root labels do not match indices")
        matrix = np.asarray(run["map_float64"], dtype=float)
        if matrix.shape != (roots.shape[1], 5):
            raise AssertionError("bad map shape")
        singular = np.linalg.svd(matrix, compute_uv=False)
        if int(np.linalg.matrix_rank(matrix, tol=1e-11)) != run[
            "map_rank_binary64"
        ]:
            raise AssertionError("map rank mismatch")
        if not np.allclose(
            singular, run["map_singular_values"], atol=5e-12, rtol=5e-12
        ):
            raise AssertionError("map singular values mismatch")
        raw = roots[indices] @ matrix
        regenerated = normalized(raw)
        stored_coordinates = np.asarray(
            run["structured_coordinates_float64"], dtype=float
        )
        if not np.allclose(
            regenerated, stored_coordinates, atol=3e-14, rtol=3e-14
        ):
            raise AssertionError("structured coordinates do not match map")
        check_diagnostics(stored_coordinates, run["structured_diagnostics"])
        structured_count += 1
    polished_count = 0
    best_actual: dict[str, tuple[float, int, str]] = {}
    for index, run in enumerate(payload["polished_runs"]):
        coordinates = np.asarray(run["coordinates_float64"], dtype=float)
        check_diagnostics(coordinates, run["final_diagnostics"])
        n = str(int(run["n"]))
        value = recompute(coordinates)["maximum_inner_product"]
        prior = best_actual.get(n)
        if prior is None or value < prior[0]:
            best_actual[n] = (
                value,
                index,
                recompute(coordinates)[
                    "coordinate_little_endian_float64_sha256"
                ],
            )
        polished_count += 1
    for n, stored in payload["best_by_n"].items():
        value, index, digest = best_actual[n]
        close(value, stored["maximum_inner_product"])
        if index != stored["polished_run_index"]:
            raise AssertionError("best run index mismatch")
        if digest != stored["coordinate_little_endian_float64_sha256"]:
            raise AssertionError("best coordinate hash mismatch")
        if value <= 0.5:
            # This would be exciting, but would still require exact or
            # directed-interval verification rather than this checker.
            raise AssertionError(
                "candidate at threshold requires a rigorous certificate audit"
            )
    return {
        "structured_runs_checked": structured_count,
        "polished_runs_checked": polished_count,
        "best_maxima": {
            n: value[0] for n, value in sorted(best_actual.items())
        },
        "interpretation": (
            "binary64 numerical consistency only; no exact construction "
            "or upper-bound conclusion"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    arguments = parser.parse_args()
    payload = json.loads(arguments.portfolio.read_text())
    print(json.dumps(check_payload(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
