#!/usr/bin/env python3
"""Independent binary64 integrity checker for round-5 search artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def unit_rows(x: np.ndarray) -> np.ndarray:
    norms = np.sqrt(np.sum(x * x, axis=1))
    if float(np.min(norms)) <= 1e-13:
        raise AssertionError("zero coordinate row")
    return x / norms[:, None]


def recompute(run: dict):
    stored = run["best"]
    x = unit_rows(np.asarray(stored["coordinates_float64"], dtype=float))
    if x.shape != (run["n"], 5):
        raise AssertionError("wrong coordinate shape")
    gram = x @ x.T
    mask = ~np.eye(len(x), dtype=bool)
    maximum = float(np.max(gram[mask]))
    minimum = float(np.min(gram[mask]))
    if abs(maximum - stored["maximum"]) > 5e-15:
        raise AssertionError("stored maximum mismatch")
    if abs(minimum - stored["minimum"]) > 5e-15:
        raise AssertionError("stored minimum mismatch")
    if abs(maximum - 0.5 - stored["gap_above_one_half"]) > 5e-15:
        raise AssertionError("stored gap mismatch")
    eigenvalues = np.linalg.eigvalsh(gram)
    if float(np.max(np.abs(eigenvalues - stored["gram_eigenvalues"]))) > 2e-13:
        raise AssertionError("stored Gram spectrum mismatch")

    ii, jj = np.triu_indices(len(x), 1)
    values = gram[ii, jj]
    if int(np.sum(values < -0.5)) != stored[
        "deep_negative_pairs_below_minus_half"
    ]:
        raise AssertionError("stored negative-pair count mismatch")
    for tolerance in (1e-4, 1e-6, 1e-8):
        active = stored[f"active_{tolerance:.0e}"]
        selected = values >= maximum - tolerance
        edges = np.column_stack([ii[selected], jj[selected]])
        if edges.tolist() != active["edges"]:
            raise AssertionError("stored active edges mismatch")
        degrees = np.bincount(edges.ravel(), minlength=len(x))
        unique, counts = np.unique(degrees, return_counts=True)
        histogram = {
            str(int(key)): int(value) for key, value in zip(unique, counts)
        }
        if histogram != active["degree_histogram"]:
            raise AssertionError("stored degree histogram mismatch")
    return maximum


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    arguments = parser.parse_args(argv)
    with arguments.artifact.open() as stream:
        payload = json.load(stream)
    if not payload["status"].startswith("NUMERICAL EVIDENCE ONLY"):
        raise AssertionError("artifact has no numerical-only warning")
    for run in payload["runs"]:
        maximum = recompute(run)
        print(f"N={run['n']} seed={run['seed']} maximum={maximum:.16f}")
    print("PASS (binary64 integrity only; not a proof)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
