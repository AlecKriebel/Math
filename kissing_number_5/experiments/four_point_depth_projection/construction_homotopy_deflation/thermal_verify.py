#!/usr/bin/env python3
"""Independent standard-library verifier for thermal construction results."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from pathlib import Path


STATUS = "INDEPENDENT BINARY64 CHECK — NOT AN EXACT CERTIFICATE"


def hash_rows(rows: list[list[float]]) -> str:
    payload = bytearray()
    for row in rows:
        for value in row:
            payload.extend(struct.pack("<d", float(value)))
    return hashlib.sha256(payload).hexdigest()


def recompute(coordinates: object, n: int) -> dict:
    if not isinstance(coordinates, list) or len(coordinates) != n:
        raise AssertionError(f"expected {n} rows")
    literal = []
    normalized = []
    norm_errors = []
    for row in coordinates:
        if not isinstance(row, list) or len(row) != 5:
            raise AssertionError("coordinate row is not length five")
        values = [float(value) for value in row]
        if not all(math.isfinite(value) for value in values):
            raise AssertionError("non-finite coordinate")
        squared_norm = math.fsum(value * value for value in values)
        if squared_norm <= 0.0:
            raise AssertionError("zero coordinate row")
        norm_errors.append(abs(squared_norm - 1.0))
        norm = math.sqrt(squared_norm)
        literal.append(values)
        normalized.append([value / norm for value in values])
    top = -math.inf
    top_pair = None
    energy = 0.0
    violating = 0
    for first in range(n):
        for second in range(first + 1, n):
            product = math.fsum(
                normalized[first][coordinate]
                * normalized[second][coordinate]
                for coordinate in range(5)
            )
            if product > top:
                top = product
                top_pair = [first, second]
            if product > 0.5:
                violating += 1
                energy += (product - 0.5) ** 2
    return {
        "coordinate_little_endian_float64_sha256": hash_rows(literal),
        "maximum_inner_product": top,
        "maximizing_pair": top_pair,
        "threshold_energy": energy,
        "pairs_above_one_half": violating,
        "maximum_row_squared_norm_error": max(norm_errors),
    }


def check_record(
    record: dict, n: int, label: str, tolerance: float
) -> dict:
    actual = recompute(record["coordinates_float64"], n)
    expected = record["diagnostics"]
    if (
        actual["coordinate_little_endian_float64_sha256"]
        != expected["coordinate_little_endian_float64_sha256"]
    ):
        raise AssertionError(f"{label}: coordinate hash mismatch")
    for key in ("maximum_inner_product", "threshold_energy"):
        if abs(actual[key] - float(expected[key])) > tolerance:
            raise AssertionError(f"{label}: {key} mismatch")
    if actual["pairs_above_one_half"] != int(
        expected["pairs_above_one_half"]
    ):
        raise AssertionError(f"{label}: violating-pair count mismatch")
    if actual["maximum_row_squared_norm_error"] > 2e-14:
        raise AssertionError(f"{label}: excessive row-norm error")
    return actual


def source_path(repository: Path, locator: str) -> Path:
    relative = locator.split("#", 1)[0]
    path = repository / relative
    if not path.is_file():
        raise AssertionError(f"missing origin source {relative}")
    return path


def verify(input_path: Path, tolerance: float = 8e-13) -> dict:
    payload = json.loads(input_path.read_text())
    if payload.get("status") != (
        "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
    ):
        raise AssertionError("wrong numerical-only status")
    runs = payload.get("runs")
    if not isinstance(runs, list) or not runs:
        raise AssertionError("missing runs")
    repository = Path(__file__).resolve().parents[3]
    expected_pairs = [
        (n, regime)
        for n in payload["parameters"]["n"]
        for regime in payload["parameters"]["regimes"]
    ]
    if [(run["n"], run["regime"]) for run in runs] != expected_pairs:
        raise AssertionError("run order/cardinality/regime mismatch")

    summaries = []
    threshold_hit = False
    checked_by_n: dict[int, list[tuple[float, dict]]] = {}
    for run_index, run in enumerate(runs):
        n = int(run["n"])
        regime_index = payload["parameters"]["regimes"].index(run["regime"])
        expected_seed = (
            int(payload["parameters"]["seed_base"])
            + 100 * (n - 41)
            + regime_index
        )
        if int(run["seed"]) != expected_seed:
            raise AssertionError(f"run {run_index}: seed mismatch")
        origin = source_path(repository, run["origin"])
        if hashlib.sha256(origin.read_bytes()).hexdigest() != run[
            "origin_sha256"
        ]:
            raise AssertionError(f"run {run_index}: origin hash mismatch")

        baseline = check_record(
            run["baseline"], n, f"run {run_index} baseline", tolerance
        )
        candidates = []
        for candidate_index, candidate in enumerate(
            run["polished_candidates"]
        ):
            candidates.append(
                check_record(
                    candidate,
                    n,
                    f"run {run_index} candidate {candidate_index}",
                    tolerance,
                )
            )
        best = check_record(
            run["best"], n, f"run {run_index} best", tolerance
        )
        enumerated = [baseline] + candidates
        minimum = min(row["maximum_inner_product"] for row in enumerated)
        if best["maximum_inner_product"] > minimum + tolerance:
            raise AssertionError(f"run {run_index}: best is not a minimum")
        hashes = {
            row["coordinate_little_endian_float64_sha256"]
            for row in enumerated
        }
        if best["coordinate_little_endian_float64_sha256"] not in hashes:
            raise AssertionError(f"run {run_index}: unknown best coordinates")
        expected_beat = (
            best["maximum_inner_product"]
            < baseline["maximum_inner_product"] - 1e-13
        )
        expected_half = best["maximum_inner_product"] <= 0.5
        if bool(run["beat_baseline"]) != expected_beat:
            raise AssertionError(f"run {run_index}: beat flag mismatch")
        if bool(run["reached_half"]) != expected_half:
            raise AssertionError(f"run {run_index}: threshold flag mismatch")
        threshold_hit = threshold_hit or expected_half
        checked_by_n.setdefault(n, []).append(
            (best["maximum_inner_product"], best)
        )
        summaries.append(
            {
                "n": n,
                "regime": run["regime"],
                "seed": int(run["seed"]),
                "candidate_count": len(candidates),
                "baseline_maximum": baseline["maximum_inner_product"],
                "best": best,
                "beat_baseline": expected_beat,
                "reached_half": expected_half,
            }
        )

    for n, entries in checked_by_n.items():
        selected = payload["best_by_n"][str(n)]
        selected_check = recompute(selected["coordinates_float64"], n)
        stored_hash = selected["diagnostics"][
            "coordinate_little_endian_float64_sha256"
        ]
        if (
            selected_check[
                "coordinate_little_endian_float64_sha256"
            ]
            != stored_hash
        ):
            raise AssertionError(f"N={n}: consolidated hash mismatch")
        minimum = min(value for value, _ in entries)
        if selected_check["maximum_inner_product"] > minimum + tolerance:
            raise AssertionError(f"N={n}: wrong consolidated minimum")
    if bool(payload["binary64_threshold_hit"]) != threshold_hit:
        raise AssertionError("global threshold flag mismatch")

    return {
        "status": STATUS,
        "source": str(input_path),
        "source_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "runs": summaries,
        "binary64_threshold_hit": threshold_hit,
        "all_coordinate_checks_passed": True,
        "scope_warning": (
            "Coordinate integrity only; stochastic trajectory histories "
            "and solver optimality are not certified."
        ),
    }


def parse_args() -> argparse.Namespace:
    directory = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=directory / "thermal_portfolio.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=directory / "thermal_verification.json",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    result = verify(arguments.input)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    for run in result["runs"]:
        print(
            f"N={run['n']} {run['regime']} seed={run['seed']} "
            f"best={run['best']['maximum_inner_product']:.17g}"
        )
    print("all independent coordinate checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
