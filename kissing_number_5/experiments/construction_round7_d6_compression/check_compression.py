#!/usr/bin/env python3
"""Independent binary64 checker for round-7 compression artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def measurements(coordinates):
    x = np.asarray(coordinates, dtype=float)
    norms2 = np.sum(x * x, axis=1)
    ii, jj = np.triu_indices(len(x), 1)
    pairs = np.sum(x[ii] * x[jj], axis=1)
    covariance = np.linalg.eigvalsh(x.T @ x)
    gram = np.linalg.eigvalsh(x @ x.T)
    return x, norms2, pairs, covariance, gram


def assert_close(first, second, tolerance, message):
    if abs(float(first) - float(second)) > tolerance:
        raise AssertionError(message)


def check_active(x, pairs, stored, tolerance):
    top = float(np.max(pairs))
    ii, jj = np.triu_indices(len(x), 1)
    selected = pairs >= top - tolerance
    edges = np.column_stack([ii[selected], jj[selected]]).tolist()
    if edges != stored["edges"]:
        raise AssertionError("active edge mismatch")
    degree = np.bincount(np.asarray(edges, dtype=int).ravel(), minlength=len(x))
    unique, counts = np.unique(degree, return_counts=True)
    histogram = {
        str(int(key)): int(value) for key, value in zip(unique, counts)
    }
    if histogram != stored["degree_histogram"]:
        raise AssertionError("active degree histogram mismatch")


def check_diagnostics(stored, expected_dimension):
    x, norms2, pairs, covariance, gram = measurements(
        stored["coordinates_float64"]
    )
    if x.shape != (stored["n"], expected_dimension):
        raise AssertionError("coordinate shape mismatch")
    norm_error = float(np.max(np.abs(norms2 - 1.0)))
    if norm_error > 8e-15:
        raise AssertionError("coordinate row is not unit length")
    assert_close(
        norm_error, stored["row_norm_max_error"], 3e-16, "norm error mismatch"
    )
    assert_close(
        np.max(pairs), stored["maximum"], 6e-15, "maximum mismatch"
    )
    assert_close(
        np.min(pairs), stored["minimum"], 6e-15, "minimum mismatch"
    )
    if float(np.max(np.abs(covariance - stored["covariance_eigenvalues"]))) > 3e-13:
        raise AssertionError("covariance spectrum mismatch")
    if float(np.max(np.abs(gram - stored["gram_eigenvalues"]))) > 3e-13:
        raise AssertionError("Gram spectrum mismatch")
    for tolerance in (1e-4, 1e-6, 1e-8):
        check_active(x, pairs, stored[f"active_{tolerance:.0e}"], tolerance)
    return x


def label_vector(label):
    answer = np.zeros(6)
    answer[label[0]] = label[2] / np.sqrt(2.0)
    answer[label[1]] = label[3] / np.sqrt(2.0)
    return answer


def exact_pair_numerator(first, second):
    row = [0] * 6
    other = [0] * 6
    row[first[0]], row[first[1]] = first[2], first[3]
    other[second[0]], other[second[1]] = second[2], second[3]
    return sum(a * b for a, b in zip(row, other))


def check_run(run):
    initial = check_diagnostics(run["initial"], 6)
    labels = run["exact_d6_root_labels"]
    if labels is not None:
        if len(labels) != run["n"] or len({tuple(label) for label in labels}) != run["n"]:
            raise AssertionError("bad exact D6 labels")
        reconstructed = np.asarray([label_vector(label) for label in labels])
        if float(np.max(np.abs(reconstructed - initial))) > 3e-16:
            raise AssertionError("D6 labels do not reconstruct initial coordinates")
        for first in range(run["n"]):
            for second in range(first + 1, run["n"]):
                if exact_pair_numerator(labels[first], labels[second]) > 1:
                    raise AssertionError("exact D6 initial pair exceeds 1/2")
    elif run["initial"]["maximum"] > 0.5:
        raise AssertionError("random S5 start is not feasible")

    previous_fraction = None
    for index, stage in enumerate(run["homotopy_history"]):
        x, norms2, pairs, spectrum, _ = measurements(
            stage["coordinates_float64"]
        )
        if x.shape != (run["n"], 6):
            raise AssertionError("stage coordinate shape mismatch")
        if float(np.max(np.abs(norms2 - 1.0))) > 8e-15:
            raise AssertionError("stage norm mismatch")
        assert_close(np.max(pairs), stage["maximum"], 6e-15, "stage maximum mismatch")
        if float(np.max(np.abs(spectrum - stage["covariance_eigenvalues"]))) > 3e-13:
            raise AssertionError("stage covariance spectrum mismatch")
        assert_close(
            max(0.0, spectrum[0]) / run["n"],
            stage["sixth_fraction"],
            2e-15,
            "sixth fraction mismatch",
        )
        if stage["stage"] != index:
            raise AssertionError("stage order mismatch")
        previous_fraction = stage["sixth_fraction"]

    collapsed = check_diagnostics(run["collapsed_six_dimensional"], 6)
    final = check_diagnostics(run["final_five_dimensional"], 5)
    projection = run["projection"]
    direction = np.asarray(projection["discarded_direction"], dtype=float)
    if abs(float(direction @ direction) - 1.0) > 3e-14:
        raise AssertionError("discarded direction is not unit")
    spectrum = np.linalg.eigvalsh(collapsed.T @ collapsed)
    residual = np.linalg.norm(
        collapsed.T @ collapsed @ direction - spectrum[0] * direction
    )
    if residual > 2e-9:
        raise AssertionError("discarded direction is not a bottom eigenvector")
    projected = collapsed - (collapsed @ direction)[:, None] * direction
    norms = np.linalg.norm(projected, axis=1)
    projected /= norms[:, None]
    assert_close(
        np.max(np.linalg.eigvalsh(collapsed.T @ collapsed) - spectrum),
        0.0,
        1e-14,
        "internal spectrum error",
    )
    assert_close(
        np.max(
            np.sum(
                projected[np.triu_indices(len(projected), 1)[0]]
                * projected[np.triu_indices(len(projected), 1)[1]],
                axis=1,
            )
        ),
        projection["maximum_immediately_after_projection"],
        8e-14,
        "projection maximum mismatch",
    )
    if final.shape != (run["n"], 5):
        raise AssertionError("final shape mismatch")
    return run["final_five_dimensional"]["maximum"]


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    arguments = parser.parse_args(argv)
    with arguments.artifact.open() as stream:
        payload = json.load(stream)
    if not payload["status"].startswith("NUMERICAL EVIDENCE ONLY"):
        raise AssertionError("missing numerical-only warning")
    best = {}
    for run in payload["runs"]:
        value = check_run(run)
        best[run["n"]] = min(best.get(run["n"], float("inf")), value)
    if sorted(best) != [41, 42, 43, 44]:
        raise AssertionError("artifact does not cover N=41 through N=44")
    for n in sorted(best):
        stored = payload["barrier_summary"][str(n)]["best_final_maximum"]
        assert_close(best[n], stored, 6e-15, "barrier summary mismatch")
        print(f"N={n} best verified final maximum={best[n]:.16f}")
    print("PASS (binary64 integrity and exact D6-label checks only; not a proof)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
