#!/usr/bin/env python3
"""Independent standard-library checker for deflate_results.json.

This checker does not import NumPy, SciPy, or the discovery implementation.
It verifies the stored final coordinates and the combinatorial integrity of
the edge-state and deflation manifests.  It remains a binary64 numerical
check, not an exact spherical-code certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import struct
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DEFAULT_INPUT = HERE / "deflate_results.json"
DEFAULT_OUTPUT = HERE / "deflate_verification.json"
STATUS = "INDEPENDENT BINARY64 CHECK — NOT AN EXACT CERTIFICATE"
TOLERANCE = 8e-13


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coordinate_hash(rows: list[list[float]]) -> str:
    payload = bytearray()
    for row in rows:
        for value in row:
            payload.extend(struct.pack("<d", float(value)))
    return hashlib.sha256(payload).hexdigest()


def recompute(coordinates: Any, n: int) -> dict[str, Any]:
    if not isinstance(coordinates, list) or len(coordinates) != n:
        raise AssertionError(f"expected {n} coordinate rows")
    literal: list[list[float]] = []
    normalized: list[list[float]] = []
    norm_errors = []
    for row in coordinates:
        if not isinstance(row, list) or len(row) != 5:
            raise AssertionError("coordinate row must have length five")
        values = [float(value) for value in row]
        if not all(math.isfinite(value) for value in values):
            raise AssertionError("nonfinite coordinate")
        norm_squared = math.fsum(value * value for value in values)
        if norm_squared <= 0:
            raise AssertionError("zero coordinate row")
        norm_errors.append(abs(norm_squared - 1.0))
        norm = math.sqrt(norm_squared)
        literal.append(values)
        normalized.append([value / norm for value in values])

    maximum = -math.inf
    minimum = math.inf
    maximizing_pair = None
    violations = 0
    for first in range(n):
        for second in range(first + 1, n):
            value = math.fsum(
                normalized[first][coordinate]
                * normalized[second][coordinate]
                for coordinate in range(5)
            )
            if value > maximum:
                maximum = value
                maximizing_pair = [first, second]
            minimum = min(minimum, value)
            if value > 0.5:
                violations += 1
    return {
        "n": n,
        "coordinate_little_endian_float64_sha256": coordinate_hash(literal),
        "maximum_inner_product": maximum,
        "minimum_inner_product": minimum,
        "maximizing_pair": maximizing_pair,
        "pairs_above_one_half": violations,
        "maximum_row_norm_squared_error": max(norm_errors),
    }


def close(actual: float, expected: float, label: str) -> None:
    if not math.isfinite(actual) or not math.isfinite(expected):
        raise AssertionError(f"{label}: nonfinite value")
    if abs(actual - expected) > TOLERANCE:
        raise AssertionError(f"{label}: {actual!r} != {expected!r}")


def check_coordinate_record(
    coordinates: Any,
    reported: dict[str, Any],
    n: int,
    label: str,
) -> dict[str, Any]:
    actual = recompute(coordinates, n)
    if (
        actual["coordinate_little_endian_float64_sha256"]
        != reported["coordinate_little_endian_float64_sha256"]
    ):
        raise AssertionError(f"{label}: coordinate hash mismatch")
    close(
        actual["maximum_inner_product"],
        float(reported["maximum_inner_product"]),
        f"{label}: maximum",
    )
    close(
        actual["minimum_inner_product"],
        float(reported["minimum_inner_product"]),
        f"{label}: minimum",
    )
    if actual["pairs_above_one_half"] != int(
        reported["pairs_above_one_half"]
    ):
        raise AssertionError(f"{label}: violating-pair count mismatch")
    if actual["maximum_row_norm_squared_error"] > 2e-14:
        raise AssertionError(f"{label}: excessive row-norm error")
    if int(reported["n"]) != n or int(reported["dimension"]) != 5:
        raise AssertionError(f"{label}: dimension metadata mismatch")
    if int(reported["numerical_rank_at_1e-10"]) > 5:
        raise AssertionError(f"{label}: reported rank exceeds five")
    return actual


def check_finite_array(
    values: Any, length: int, label: str, nonnegative: bool = False
) -> list[float]:
    if not isinstance(values, list) or len(values) != length:
        raise AssertionError(f"{label}: expected array length {length}")
    answer = [float(value) for value in values]
    if not all(math.isfinite(value) for value in answer):
        raise AssertionError(f"{label}: nonfinite entry")
    if nonnegative and min(answer) < -1e-15:
        raise AssertionError(f"{label}: negative entry")
    return answer


def check_homotopy(record: dict[str, Any], n: int, label: str) -> None:
    edge_count = n * (n - 1) // 2
    homotopy = record["homotopy"]
    completed = int(homotopy["epochs_completed"])
    requested = int(homotopy["epochs_requested"])
    if not 1 <= completed <= requested:
        raise AssertionError(f"{label}: bad epoch count")
    state = homotopy["final_edge_state"]
    slack = check_finite_array(
        state["slack_at_one_half"],
        edge_count,
        f"{label}: threshold slack",
        nonnegative=True,
    )
    residual = check_finite_array(
        state["residual_at_one_half"],
        edge_count,
        f"{label}: threshold residual",
        nonnegative=True,
    )
    check_finite_array(
        state["dual_penalty"],
        edge_count,
        f"{label}: dual penalty",
        nonnegative=True,
    )
    check_finite_array(
        state["last_homotopy_slack"],
        edge_count,
        f"{label}: last slack",
        nonnegative=True,
    )
    check_finite_array(
        state["last_homotopy_residual"],
        edge_count,
        f"{label}: last residual",
        nonnegative=True,
    )
    check_finite_array(
        state["last_effective_weight"],
        edge_count,
        f"{label}: last weight",
        nonnegative=True,
    )
    if max((left * right for left, right in zip(slack, residual)), default=0) > 1e-12:
        raise AssertionError(f"{label}: slack/residual complementarity failure")

    events = homotopy["deflation_events"]
    if not isinstance(events, list) or len(events) != 3:
        raise AssertionError(f"{label}: expected three deflation events")
    seen_event_numbers = set()
    for event in events:
        event_number = int(event["event"])
        if event_number in seen_event_numbers:
            raise AssertionError(f"{label}: duplicate deflation event")
        seen_event_numbers.add(event_number)
        delete_epoch = int(event["delete_epoch"])
        reentry_epoch = int(event["reentry_epoch"])
        if not 0 <= delete_epoch < reentry_epoch < requested:
            raise AssertionError(f"{label}: invalid deflation interval")
        edges = event["deleted_edges"]
        if int(event["deleted_edge_count"]) != len(edges):
            raise AssertionError(f"{label}: deleted-edge count mismatch")
        normalized_edges = []
        for edge in edges:
            if (
                not isinstance(edge, list)
                or len(edge) != 2
                or not 0 <= int(edge[0]) < int(edge[1]) < n
            ):
                raise AssertionError(f"{label}: invalid deleted edge")
            normalized_edges.append((int(edge[0]), int(edge[1])))
        if len(set(normalized_edges)) != len(normalized_edges):
            raise AssertionError(f"{label}: repeated deleted edge")

    prior_epoch = 0
    for checkpoint in homotopy["checkpoints"]:
        epoch = int(checkpoint["epoch"])
        if epoch <= prior_epoch or epoch > completed:
            raise AssertionError(f"{label}: invalid checkpoint ordering")
        prior_epoch = epoch
        for aggregate_name in (
            "slack",
            "residual",
            "dual",
            "effective_weight",
        ):
            aggregate = checkpoint[aggregate_name]
            for key in ("minimum", "maximum", "mean", "l2"):
                if not math.isfinite(float(aggregate[key])):
                    raise AssertionError(
                        f"{label}: nonfinite checkpoint aggregate"
                    )


def check(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text())
    if payload.get("schema") != "kissing5-factor-slack-deflation-v1":
        raise AssertionError("unexpected schema")
    if payload.get("status") != (
        "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
    ):
        raise AssertionError("missing numerical-only status")
    parameters = payload["parameters"]
    ns = [int(value) for value in parameters["n"]]
    restarts = int(parameters["restarts"])
    warm_restarts = int(parameters["warm_restarts"])
    runs = payload["runs"]
    if len(runs) != len(ns) * restarts:
        raise AssertionError("run count mismatch")

    run_checks: dict[int, list[dict[str, Any]]] = {n: [] for n in ns}
    seen = set()
    for run in runs:
        n = int(run["n"])
        restart = int(run["restart"])
        label = f"N={n} restart={restart}"
        if n not in run_checks or not 0 <= restart < restarts:
            raise AssertionError(f"{label}: unexpected run")
        if (n, restart) in seen:
            raise AssertionError(f"{label}: duplicate run")
        seen.add((n, restart))
        expected_seed = (
            int(parameters["seed_base"]) + 100 * (n - 41) + restart
        )
        if int(run["seed"]) != expected_seed:
            raise AssertionError(f"{label}: seed mismatch")
        expected_origin = (
            "warm_perturbed"
            if restart < warm_restarts
            else "fresh_asymmetric_gaussian"
        )
        if run["origin"] != expected_origin:
            raise AssertionError(f"{label}: origin mismatch")
        source = run["warm_source"]
        source_path = REPO / source["source_file"]
        if file_hash(source_path) != source["source_file_sha256"]:
            raise AssertionError(f"{label}: source hash mismatch")

        actual = check_coordinate_record(
            run["best_coordinates_float64"],
            run["best_diagnostics"],
            n,
            label,
        )
        expected_beat = (
            actual["maximum_inner_product"]
            < float(source["maximum_inner_product"]) - 1e-13
        )
        if bool(run["beats_warm_record"]) != expected_beat:
            raise AssertionError(f"{label}: record flag mismatch")
        expected_threshold = actual["maximum_inner_product"] <= 0.5
        if bool(run["reaches_one_half_binary64"]) != expected_threshold:
            raise AssertionError(f"{label}: threshold flag mismatch")
        check_homotopy(run, n, label)

        polished = run["polished_candidates"]
        if not isinstance(polished, list) or len(polished) != 2:
            raise AssertionError(f"{label}: expected two polish records")
        for polish in polished:
            solver = polish["solver"]
            close(
                float(solver["recomputed_maximum"]),
                float(polish["diagnostics"]["maximum_inner_product"]),
                f"{label}: polish recomputation",
            )
        run_checks[n].append(actual)

    best_checks = []
    any_threshold = False
    for n in ns:
        record = payload["best_by_n"][str(n)]
        actual = check_coordinate_record(
            record["coordinates_float64"],
            record["diagnostics"],
            n,
            f"N={n} global best",
        )
        source_maximum = float(record["warm_source"]["maximum_inner_product"])
        enumerated_minimum = min(
            [source_maximum]
            + [
                run["maximum_inner_product"] for run in run_checks[n]
            ]
        )
        if actual["maximum_inner_product"] > enumerated_minimum + TOLERANCE:
            raise AssertionError(f"N={n}: global best is not minimal")
        expected_beat = (
            actual["maximum_inner_product"] < source_maximum - 1e-13
        )
        if bool(record["strictly_beats_warm_record"]) != expected_beat:
            raise AssertionError(f"N={n}: global record flag mismatch")
        threshold = actual["maximum_inner_product"] <= 0.5
        if bool(record["reaches_one_half_binary64"]) != threshold:
            raise AssertionError(f"N={n}: global threshold mismatch")
        any_threshold = any_threshold or threshold
        best_checks.append(actual)
    if bool(payload["any_threshold_candidate_found"]) != any_threshold:
        raise AssertionError("top-level threshold flag mismatch")

    return {
        "schema": "kissing5-factor-slack-deflation-verification-v1",
        "status": STATUS,
        "all_checks_passed": True,
        "source": str(path),
        "source_sha256": file_hash(path),
        "python": platform.python_version(),
        "absolute_maximum_tolerance": TOLERANCE,
        "run_count": len(runs),
        "best_by_n": best_checks,
        "any_threshold_candidate_found": any_threshold,
        "scope": (
            "binary64 coordinate and manifest integrity only; no failed "
            "construction search proves an upper bound"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, nargs="?", default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()
    result = check(arguments.input)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    for best in result["best_by_n"]:
        print(
            f"N={best['n']} "
            f"max={best['maximum_inner_product']:.17g} "
            f"pairs>1/2={best['pairs_above_one_half']}"
        )
    print("all independent binary64 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
