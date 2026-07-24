#!/usr/bin/env python3
"""Independent standard-library checker for rigidity-search JSON.

The checker deliberately does not import the search program, NumPy, SciPy,
or any solver.  It parses every stored coordinate, normalizes every row with
``math.fsum``/``math.sqrt``, enumerates every unordered pair, and checks the
reported hashes and maxima.  This verifies the numerical artifact; it does
not turn binary64 coordinates into an exact spherical-code certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import struct
from pathlib import Path


STATUS = "INDEPENDENT BINARY64 CHECK — NOT AN EXACT CERTIFICATE"


def coordinate_hash(rows: list[list[float]]) -> str:
    payload = bytearray()
    for row in rows:
        for value in row:
            payload.extend(struct.pack("<d", float(value)))
    return hashlib.sha256(payload).hexdigest()


def recompute(coordinates: object, expected_n: int) -> dict:
    if not isinstance(coordinates, list) or len(coordinates) != expected_n:
        raise AssertionError(f"expected {expected_n} coordinate rows")
    literal_rows: list[list[float]] = []
    normalized_rows: list[list[float]] = []
    norm_errors = []
    for row in coordinates:
        if not isinstance(row, list) or len(row) != 5:
            raise AssertionError("every coordinate row must have length five")
        values = [float(value) for value in row]
        if not all(math.isfinite(value) for value in values):
            raise AssertionError("non-finite coordinate")
        squared_norm = math.fsum(value * value for value in values)
        if squared_norm <= 0.0:
            raise AssertionError("zero coordinate row")
        norm_errors.append(abs(squared_norm - 1.0))
        norm = math.sqrt(squared_norm)
        literal_rows.append(values)
        normalized_rows.append([value / norm for value in values])

    maximum = -math.inf
    literal_maximum = -math.inf
    maximizing_pair = None
    pairs_above_half = 0
    for first in range(expected_n):
        for second in range(first + 1, expected_n):
            literal = math.fsum(
                literal_rows[first][coordinate]
                * literal_rows[second][coordinate]
                for coordinate in range(5)
            )
            value = math.fsum(
                normalized_rows[first][coordinate]
                * normalized_rows[second][coordinate]
                for coordinate in range(5)
            )
            if literal > literal_maximum:
                literal_maximum = literal
            if value > maximum:
                maximum = value
                maximizing_pair = [first, second]
            if value > 0.5:
                pairs_above_half += 1
    return {
        "n": expected_n,
        "coordinate_little_endian_float64_sha256": coordinate_hash(
            literal_rows
        ),
        "maximum_row_squared_norm_error": max(norm_errors),
        "literal_maximum_inner_product": literal_maximum,
        "normalized_maximum_inner_product": maximum,
        "normalized_maximizing_pair": maximizing_pair,
        "normalized_pairs_above_one_half": pairs_above_half,
    }


def check_coordinate_record(
    record: dict, n: int, label: str, tolerance: float
) -> dict:
    coordinates = record["coordinates_float64"]
    diagnostics = record["diagnostics"]
    actual = recompute(coordinates, n)
    expected_hash = diagnostics[
        "coordinate_little_endian_float64_sha256"
    ]
    if actual["coordinate_little_endian_float64_sha256"] != expected_hash:
        raise AssertionError(f"{label}: coordinate hash mismatch")
    expected_maximum = float(diagnostics["maximum_inner_product"])
    if (
        abs(actual["normalized_maximum_inner_product"] - expected_maximum)
        > tolerance
    ):
        raise AssertionError(
            f"{label}: maximum mismatch: "
            f"{actual['normalized_maximum_inner_product']} versus "
            f"{expected_maximum}"
        )
    if actual["maximum_row_squared_norm_error"] > 2e-14:
        raise AssertionError(f"{label}: excessive row-norm error")
    return actual


def check(path: Path, tolerance: float = 8e-13) -> dict:
    payload = json.loads(path.read_text())
    if payload.get("status") != (
        "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
    ):
        raise AssertionError("missing numerical-evidence status")
    runs = payload.get("runs")
    if not isinstance(runs, list) or [run.get("n") for run in runs] != [
        41,
        42,
        43,
        44,
    ]:
        raise AssertionError("expected exactly one ordered run for N=41..44")

    summaries = []
    for run in runs:
        n = int(run["n"])
        trials = run["trials"]
        if int(run["trial_count"]) != len(trials):
            raise AssertionError(f"N={n}: trial-count mismatch")
        baseline_maximum = float(run["baseline"]["maximum_inner_product"])

        trial_checks = []
        for index, trial in enumerate(trials):
            trial_checks.append(
                check_coordinate_record(
                    trial, n, f"N={n} trial={index}", tolerance
                )
            )
        best_check = check_coordinate_record(
            run["best"], n, f"N={n} best", tolerance
        )
        best_maximum = best_check["normalized_maximum_inner_product"]
        enumerated_minimum = min(
            [baseline_maximum]
            + [
                checked["normalized_maximum_inner_product"]
                for checked in trial_checks
            ]
        )
        if best_maximum > enumerated_minimum + tolerance:
            raise AssertionError(f"N={n}: stored best is not a run minimum")
        expected_reached_half = best_maximum <= 0.5
        if bool(run["reached_half"]) != expected_reached_half:
            raise AssertionError(f"N={n}: threshold flag mismatch")
        expected_beat = best_maximum < baseline_maximum - 1e-13
        if bool(run["beat_baseline"]) != expected_beat:
            raise AssertionError(f"N={n}: baseline-improvement flag mismatch")
        summaries.append(
            {
                "n": n,
                "trial_count": len(trials),
                "baseline_maximum": baseline_maximum,
                "best": best_check,
                "beat_baseline": expected_beat,
                "reached_half": expected_reached_half,
            }
        )
    return {
        "status": STATUS,
        "source": str(path),
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "runs": summaries,
        "all_checks_passed": True,
    }


def parse_args() -> argparse.Namespace:
    directory = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=directory / "rigidity_softmode_results.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=directory / "rigidity_verification.json",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    result = check(arguments.input)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    for run in result["runs"]:
        print(
            f"N={run['n']} trials={run['trial_count']} "
            f"baseline={run['baseline_maximum']:.17g} "
            f"best={run['best']['normalized_maximum_inner_product']:.17g} "
            f"pairs>1/2="
            f"{run['best']['normalized_pairs_above_one_half']}"
        )
    print("all independent binary64 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
