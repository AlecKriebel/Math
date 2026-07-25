#!/usr/bin/env python3
"""Consistency checker for the cross-cardinality challenge artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from .check_results import check_diagnostics, independently_enumerate_shell, recompute


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_portfolio", type=Path)
    parser.add_argument("challenge", type=Path)
    arguments = parser.parse_args()
    payload = json.loads(arguments.challenge.read_text())
    source_digest = hashlib.sha256(arguments.source_portfolio.read_bytes()).hexdigest()
    if payload["source_portfolio_sha256"] != source_digest:
        raise AssertionError("source portfolio hash mismatch")
    best: dict[str, tuple[float, int, str]] = {}
    for index, run in enumerate(payload["runs"]):
        roots, labels = independently_enumerate_shell(run["source_family"])
        indices = np.asarray(run["child_root_indices"], dtype=int)
        if len(indices) != run["target_n"] or len(set(indices.tolist())) != len(indices):
            raise AssertionError("bad child subset")
        if [labels[int(root)] for root in indices] != run["child_root_labels"]:
            raise AssertionError("child labels mismatch")
        matrix = np.asarray(run["reoptimized_map_float64"], dtype=float)
        raw = roots[indices] @ matrix
        regenerated = raw / np.linalg.norm(raw, axis=1)[:, None]
        structured = np.asarray(run["structured_coordinates_float64"], dtype=float)
        if not np.allclose(regenerated, structured, atol=3e-14, rtol=3e-14):
            raise AssertionError("structured coordinates do not match map")
        check_diagnostics(structured, run["structured_diagnostics"])
        final = np.asarray(run["coordinates_float64"], dtype=float)
        check_diagnostics(final, run["final_diagnostics"])
        actual = recompute(final)
        key = str(run["target_n"])
        prior = best.get(key)
        candidate = (
            actual["maximum_inner_product"],
            index,
            actual["coordinate_little_endian_float64_sha256"],
        )
        if prior is None or candidate[0] < prior[0]:
            best[key] = candidate
    for n, stored in payload["best_by_n"].items():
        value, index, digest = best[n]
        if abs(value - stored["maximum_inner_product"]) > 5e-12:
            raise AssertionError("best maximum mismatch")
        if index != stored["run_index"] or digest != stored[
            "coordinate_little_endian_float64_sha256"
        ]:
            raise AssertionError("best endpoint mismatch")
    print(
        json.dumps(
            {
                "runs_checked": len(payload["runs"]),
                "best_maxima": {n: item[0] for n, item in sorted(best.items())},
                "interpretation": "binary64 numerical consistency only",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
