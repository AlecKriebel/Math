#!/usr/bin/env python3
"""Storage-light deterministic search sweep over an order-42 graph catalog."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import math
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLAN_SCHEMA = "ramsey55.catalog_seed_search_plan.v1"
PLAN_STATUS = "PREREGISTERED_BEFORE_EXECUTION"
SEARCH_ALGORITHM = "violated_set_min_conflicts_tabu_v1"
INTEGER_SEARCH_FIELDS = (
    "C5",
    "I5",
    "E",
    "edge_count",
    "steps_executed",
    "delta_evaluations",
    "improvements",
    "penalty_updates",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_json_object(stdout: str, label: str) -> dict[str, Any]:
    def reject_constant(token: str) -> None:
        raise ValueError(f"non-finite JSON number {token}")

    try:
        value = json.loads(stdout, parse_constant=reject_constant)
    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"{label} did not emit exactly one finite JSON object") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} JSON root is not an object")
    return value


def parse_search_json(stdout: str) -> tuple[dict[str, Any], str]:
    graph_marker = ',"graph6":"'
    output_marker = '","output":'
    if stdout.count(graph_marker) != 1:
        raise ValueError("search output does not contain exactly one graph6 field")
    graph_start = stdout.index(graph_marker) + len(graph_marker)
    graph_end = stdout.find(output_marker, graph_start)
    if graph_end < 0 or stdout.find(output_marker, graph_end + 1) >= 0:
        raise ValueError("search output does not contain one graph6/output boundary")
    raw_graph6 = stdout[graph_start:graph_end]
    if (
        not raw_graph6
        or '"' in raw_graph6
        or any(not 63 <= ord(character) <= 126 for character in raw_graph6)
    ):
        raise ValueError("search output graph6 has bytes outside the graph6 alphabet")
    normalized = (
        stdout[:graph_start]
        + json.dumps(raw_graph6, ensure_ascii=True)[1:-1]
        + stdout[graph_end:]
    )
    value = parse_json_object(normalized, "search")
    if value.get("graph6") != raw_graph6:
        raise ValueError("normalized search graph6 changed unexpectedly")
    return value, raw_graph6


def _require_nonnegative_int(value: Any, field: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"search output {field} is not a nonnegative integer")
    return value


def parse_search_output(
    stdout: str,
    *,
    expected: dict[str, Any],
) -> dict[str, Any]:
    value, raw_graph6 = parse_search_json(stdout)
    exact_bindings = {
        "mode": "search",
        "algorithm": SEARCH_ALGORITHM,
        "n": 43,
        "seed": expected["seed"],
        "steps_requested": expected["steps"],
        "restarts": expected["restarts"],
        "tabu_tenure": expected["tabu"],
        "breakout_interval": expected["breakout_interval"],
        "initial_perturbation": expected["initial_perturbation"],
        "seed_graph": expected["catalog"],
        "seed_line": expected["line_number"],
        "output": expected["output"],
    }
    for field, wanted in exact_bindings.items():
        if value.get(field) != wanted:
            raise ValueError(
                f"search output binding mismatch for {field}: "
                f"{value.get(field)!r} != {wanted!r}"
            )
    random_walk = value.get("random_walk")
    if (
        isinstance(random_walk, bool)
        or not isinstance(random_walk, (int, float))
        or not math.isfinite(float(random_walk))
        or not math.isclose(
            float(random_walk),
            expected["random_walk"],
            rel_tol=0.0,
            abs_tol=0.5e-6,
        )
    ):
        raise ValueError("search output random_walk binding mismatch")

    for field in INTEGER_SEARCH_FIELDS:
        _require_nonnegative_int(value.get(field), field)
    for field in ("runtime_seconds", "precompute_seconds"):
        number = value.get(field)
        if (
            isinstance(number, bool)
            or not isinstance(number, (int, float))
            or not math.isfinite(float(number))
            or number < 0
        ):
            raise ValueError(f"search output {field} is not finite and nonnegative")
    if value["E"] != value["C5"] + value["I5"]:
        raise ValueError("search output E does not equal C5 + I5")
    if value["edge_count"] > 903:
        raise ValueError("search output edge_count exceeds K_43")
    if value["steps_executed"] > expected["steps"] * expected["restarts"]:
        raise ValueError("search output steps_executed exceeds the requested budget")

    degrees = value.get("degree_sequence")
    if (
        not isinstance(degrees, list)
        or len(degrees) != 43
        or any(type(degree) is not int or not 0 <= degree <= 42 for degree in degrees)
        or degrees != sorted(degrees)
        or sum(degrees) != 2 * value["edge_count"]
    ):
        raise ValueError("search output degree sequence is malformed or inconsistent")
    if value.get("graph6") != raw_graph6:
        raise ValueError("search output graph6 extraction mismatch")
    return value


def timeout_text(value: str | bytes | None) -> str | None:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def repo_plan_path(value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise SystemExit(f"plan {label} path must be a nonempty repo-relative string")
    root = ROOT.resolve()
    resolved = (ROOT / value).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise SystemExit(f"plan {label} path escapes the repository") from error
    return resolved


def plan_output_path(value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise SystemExit(f"plan {label} must be a nonempty path string")
    path = Path(value)
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def load_and_validate_plan(
    plan_path: Path,
    *,
    args: argparse.Namespace,
) -> dict[str, Any]:
    try:
        plan = parse_json_object(plan_path.read_text(encoding="utf-8"), "plan")
    except (OSError, UnicodeError, ValueError) as error:
        raise SystemExit(f"invalid plan: {error}") from error
    if plan.get("schema") != PLAN_SCHEMA or plan.get("status") != PLAN_STATUS:
        raise SystemExit(
            f"plan must have schema {PLAN_SCHEMA} and status {PLAN_STATUS}"
        )

    supplied_paths = {
        "catalog": args.catalog,
        "search": args.search,
        "exhaustive_verifier": args.exhaustive_verifier,
        "bitset_verifier": args.bitset_verifier,
    }
    for label, supplied in supplied_paths.items():
        record = plan.get(label)
        if not isinstance(record, dict):
            raise SystemExit(f"plan {label} record is missing")
        expected_path = repo_plan_path(record.get("path"), label)
        if supplied.resolve() != expected_path:
            raise SystemExit(f"plan path mismatch for {label}")
        if not expected_path.is_file():
            raise SystemExit(f"missing pinned {label}: {expected_path}")
        expected_sha256 = record.get("sha256")
        if (
            not isinstance(expected_sha256, str)
            or sha256_file(expected_path) != expected_sha256
        ):
            raise SystemExit(f"plan SHA-256 mismatch for {label}")

    runner = plan.get("runner")
    if not isinstance(runner, dict):
        raise SystemExit("plan runner record is missing")
    expected_runner = repo_plan_path(runner.get("path"), "runner")
    if expected_runner != Path(__file__).resolve():
        raise SystemExit("plan runner path does not name this runner")
    runner_sha256 = runner.get("sha256")
    if not isinstance(runner_sha256, str) or sha256_file(expected_runner) != runner_sha256:
        raise SystemExit("plan SHA-256 mismatch for runner")

    selected = plan.get("selected_lines")
    if not isinstance(selected, dict):
        raise SystemExit("plan selected_lines record is missing")
    if args.lines_file is None or args.last_line is not None:
        raise SystemExit("this plan schema requires --lines-file, not --last-line")
    expected_lines_path = repo_plan_path(selected.get("path"), "selected_lines")
    if args.lines_file.resolve() != expected_lines_path:
        raise SystemExit("plan path mismatch for selected_lines")
    expected_lines_sha256 = selected.get("sha256")
    if (
        not expected_lines_path.is_file()
        or not isinstance(expected_lines_sha256, str)
        or sha256_file(expected_lines_path) != expected_lines_sha256
    ):
        raise SystemExit("plan SHA-256 mismatch for selected_lines")
    if type(selected.get("count")) is not int or selected["count"] < 1:
        raise SystemExit("plan selected_lines count must be a positive integer")

    configuration = plan.get("configuration")
    if not isinstance(configuration, dict):
        raise SystemExit("plan configuration is missing")
    actual_configuration = {
        "seed_base": args.seed_base,
        "steps": args.steps,
        "restarts": args.restarts,
        "tabu": args.tabu,
        "random_walk": args.random_walk,
        "breakout_interval": args.breakout_interval,
        "initial_perturbation": args.initial_perturbation,
        "workers": args.workers,
        "instance_time_limit": args.instance_time_limit,
        "verifier_time_limit": args.verifier_time_limit,
    }
    for field, actual in actual_configuration.items():
        registered = configuration.get(field)
        if field in {
            "seed_base",
            "steps",
            "restarts",
            "tabu",
            "breakout_interval",
            "initial_perturbation",
            "workers",
        }:
            matches = type(registered) is int and registered == actual
        else:
            matches = (
                not isinstance(registered, bool)
                and isinstance(registered, (int, float))
                and math.isfinite(float(registered))
                and float(registered) == actual
            )
        if not matches:
            raise SystemExit(
                f"plan configuration mismatch for {field}: "
                f"{registered!r} != {actual!r}"
            )

    outputs = plan.get("outputs")
    if not isinstance(outputs, dict):
        raise SystemExit("plan outputs record is missing")
    if args.output_dir.resolve() != plan_output_path(
        outputs.get("directory"), "outputs.directory"
    ):
        raise SystemExit("plan output directory mismatch")
    if args.summary.resolve() != plan_output_path(
        outputs.get("summary"), "outputs.summary"
    ):
        raise SystemExit("plan summary path mismatch")
    return plan


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def run_verifier(command: list[str], timeout: float) -> dict[str, Any]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "status": "TIMEOUT",
            "wall_seconds": time.monotonic() - started,
            "stdout": timeout_text(error.stdout),
            "stderr": timeout_text(error.stderr),
        }
    except OSError as error:
        return {
            "status": "ERROR",
            "wall_seconds": time.monotonic() - started,
            "error": str(error),
        }
    return {
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "returncode": completed.returncode,
        "wall_seconds": time.monotonic() - started,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--search", type=Path, required=True)
    parser.add_argument("--exhaustive-verifier", type=Path, required=True)
    parser.add_argument("--bitset-verifier", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--first-line", type=int, default=1)
    parser.add_argument("--last-line", type=int)
    parser.add_argument("--lines-file", type=Path)
    parser.add_argument("--seed-base", type=int, required=True)
    parser.add_argument("--steps", type=int, required=True)
    parser.add_argument("--restarts", type=int, required=True)
    parser.add_argument("--tabu", type=int, required=True)
    parser.add_argument("--random-walk", type=float, required=True)
    parser.add_argument("--breakout-interval", type=int, required=True)
    parser.add_argument("--initial-perturbation", type=int, required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--instance-time-limit", type=float, required=True)
    parser.add_argument("--verifier-time-limit", type=float, default=60.0)
    args = parser.parse_args()

    if (args.last_line is None) == (args.lines_file is None):
        raise SystemExit("provide exactly one of --last-line or --lines-file")
    if (
        args.first_line < 1
        or (args.last_line is not None and args.last_line < args.first_line)
        or args.steps < 1
        or args.restarts < 1
        or args.tabu < 0
        or not 0.0 <= args.random_walk <= 1.0
        or args.breakout_interval < 0
        or args.initial_perturbation < 0
        or args.workers < 1
        or args.instance_time_limit <= 0
        or args.verifier_time_limit <= 0
    ):
        raise SystemExit("invalid search, positive, or range argument")
    if not math.isfinite(args.random_walk):
        raise SystemExit("--random-walk must be finite")
    if not math.isfinite(args.instance_time_limit) or not math.isfinite(
        args.verifier_time_limit
    ):
        raise SystemExit("time limits must be finite")
    plan = load_and_validate_plan(args.plan, args=args)
    if not os.access(args.search, os.X_OK):
        raise SystemExit(f"search is not executable: {args.search}")
    if not os.access(args.bitset_verifier, os.X_OK):
        raise SystemExit(f"bitset verifier is not executable: {args.bitset_verifier}")
    try:
        catalog_lines = args.catalog.read_text(encoding="ascii").splitlines()
    except (OSError, UnicodeError) as error:
        raise SystemExit(f"cannot read catalog: {error}") from error
    if not catalog_lines or any(not line.strip() for line in catalog_lines):
        raise SystemExit(
            "catalog must contain exactly one nonblank graph6 record per physical line"
        )
    if args.lines_file is not None:
        try:
            requested = [
                int(line)
                for line in args.lines_file.read_text(encoding="ascii").splitlines()
                if line.strip()
            ]
        except (OSError, UnicodeError, ValueError) as error:
            raise SystemExit(f"invalid lines file: {error}") from error
        if (
            not requested
            or len(requested) != len(set(requested))
            or requested != sorted(requested)
        ):
            raise SystemExit("lines file must contain distinct increasing line numbers")
    else:
        assert args.last_line is not None
        requested = list(range(args.first_line, args.last_line + 1))
    if min(requested) < 1 or max(requested) > len(catalog_lines):
        raise SystemExit("requested line is beyond the catalog")
    if len(requested) != plan["selected_lines"]["count"]:
        raise SystemExit("selected line count does not match the plan")
    if args.seed_base + min(requested) < 0 or args.seed_base + max(requested) >= 2**64:
        raise SystemExit("derived seeds must be inside the uint64 range")

    graph_paths = [
        args.output_dir / f"line_{line_number:03d}.g6"
        for line_number in requested
    ]
    record_paths = [
        args.output_dir / f"line_{line_number:03d}.result.json"
        for line_number in requested
    ]
    outputs = [*graph_paths, *record_paths, args.summary]
    raw_json_echoes = [str(args.catalog), *(str(path) for path in graph_paths)]
    if any(
        any(character in {'"', "\\"} or ord(character) < 32 for character in text)
        for text in raw_json_echoes
    ):
        raise SystemExit(
            "catalog and graph output paths cannot contain quotes, backslashes, "
            "or control characters because the pinned search binary echoes them raw"
        )
    resolved_outputs = [path.resolve() for path in outputs]
    if len(resolved_outputs) != len(set(resolved_outputs)):
        raise SystemExit("output paths are not pairwise distinct")
    protected = {
        args.catalog.resolve(),
        args.search.resolve(),
        args.exhaustive_verifier.resolve(),
        args.bitset_verifier.resolve(),
        args.plan.resolve(),
        args.lines_file.resolve(),
    }
    if any(path in protected for path in resolved_outputs):
        raise SystemExit("an output path aliases a pinned input")
    existing = [str(path) for path in outputs if path.exists()]
    if existing:
        raise SystemExit(f"refusing to overwrite existing outputs: {existing[:3]}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stop = threading.Event()
    started_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    started = time.monotonic()

    def execute(line_number: int) -> dict[str, Any]:
        if stop.is_set():
            return {"catalog_line": line_number, "status": "SKIPPED_AFTER_CONSTRUCTION"}
        seed = args.seed_base + line_number
        prefix = args.output_dir / f"line_{line_number:03d}"
        graph_path = prefix.with_suffix(".g6")
        command = [
            str(args.search),
            "--n",
            "43",
            "--seed",
            str(seed),
            "--steps",
            str(args.steps),
            "--restarts",
            str(args.restarts),
            "--tabu",
            str(args.tabu),
            "--random-walk",
            str(args.random_walk),
            "--breakout-interval",
            str(args.breakout_interval),
            "--initial-perturbation",
            str(args.initial_perturbation),
            "--seed-graph",
            str(args.catalog),
            "--seed-line",
            str(line_number),
            "--output",
            str(graph_path),
        ]
        instance_started = time.monotonic()
        try:
            completed = subprocess.run(
                command,
                text=True,
                capture_output=True,
                check=False,
                timeout=args.instance_time_limit,
            )
        except subprocess.TimeoutExpired as error:
            return {
                "catalog_line": line_number,
                "seed": seed,
                "status": "TIMEOUT_NO_CONCLUSION",
                "wall_seconds": time.monotonic() - instance_started,
                "stdout": timeout_text(error.stdout),
                "stderr": timeout_text(error.stderr),
            }
        except OSError as error:
            return {
                "catalog_line": line_number,
                "seed": seed,
                "status": "SEARCH_ERROR",
                "wall_seconds": time.monotonic() - instance_started,
                "error": str(error),
            }
        record: dict[str, Any] = {
            "catalog_line": line_number,
            "seed": seed,
            "command": command,
            "returncode": completed.returncode,
            "wall_seconds": time.monotonic() - instance_started,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        if completed.returncode != 0 or not graph_path.is_file():
            record["status"] = "SEARCH_ERROR"
            return record
        try:
            search_output = parse_search_output(
                completed.stdout,
                expected={
                    "seed": seed,
                    "steps": args.steps,
                    "restarts": args.restarts,
                    "tabu": args.tabu,
                    "random_walk": args.random_walk,
                    "breakout_interval": args.breakout_interval,
                    "initial_perturbation": args.initial_perturbation,
                    "catalog": str(args.catalog),
                    "line_number": line_number,
                    "output": str(graph_path),
                },
            )
            expected_graph_bytes = (search_output["graph6"] + "\n").encode("ascii")
            graph_bytes = graph_path.read_bytes()
            if graph_bytes != expected_graph_bytes:
                raise ValueError("graph artifact does not exactly match search JSON")
        except (OSError, UnicodeError, ValueError) as error:
            record.update({"status": "OUTPUT_PARSE_ERROR", "error": str(error)})
            return record
        graph6 = search_output["graph6"]
        record.update(
            {field: search_output[field] for field in INTEGER_SEARCH_FIELDS}
        )
        record["runtime_seconds"] = search_output["runtime_seconds"]
        record.update(
            {
                "graph_path": str(graph_path.resolve()),
                "graph_sha256": sha256_file(graph_path),
                "graph6_length": len(graph6),
                "status": "SEARCHED_INVALID_CANDIDATE",
            }
        )
        if search_output["E"] == 0:
            exhaustive = run_verifier(
                [sys.executable, str(args.exhaustive_verifier), str(graph_path)],
                args.verifier_time_limit,
            )
            bitset = run_verifier(
                [str(args.bitset_verifier), str(graph_path)],
                args.verifier_time_limit,
            )
            record["exhaustive_verifier"] = exhaustive
            record["bitset_verifier"] = bitset
            verifiers_agree = False
            if exhaustive["status"] == "PASS" and bitset["status"] == "PASS":
                try:
                    exhaustive_json = parse_json_object(
                        exhaustive["stdout"], "exhaustive verifier"
                    )
                    bitset_json = parse_json_object(
                        bitset["stdout"], "bitset verifier"
                    )
                    record["exhaustive_verifier"]["json"] = exhaustive_json
                    record["bitset_verifier"]["json"] = bitset_json
                    verifiers_agree = (
                        exhaustive_json.get("verifier")
                        == "python_exhaustive_k_subset_pairs_v1"
                        and exhaustive_json.get("input") == str(graph_path)
                        and exhaustive_json.get("input_sha256")
                        == record["graph_sha256"]
                        and exhaustive_json.get("line") == 1
                        and exhaustive_json.get("n") == 43
                        and exhaustive_json.get("k") == 5
                        and exhaustive_json.get("clique_count") == 0
                        and exhaustive_json.get("independent_count") == 0
                        and exhaustive_json.get("objective") == 0
                        and exhaustive_json.get("valid") is True
                        and bitset_json.get("verifier")
                        == "cpp_recursive_bitset_clique_v1"
                        and bitset_json.get("n") == 43
                        and bitset_json.get("k") == 5
                        and bitset_json.get("clique_k_found") is False
                        and bitset_json.get("independent_k_found") is False
                        and bitset_json.get("valid") is True
                        and exhaustive_json.get("edge_count")
                        == bitset_json.get("edge_count")
                        == search_output["edge_count"]
                        and exhaustive_json.get("degree_sequence")
                        == bitset_json.get("degree_sequence")
                        == search_output["degree_sequence"]
                    )
                except (TypeError, ValueError) as error:
                    record["verifier_output_error"] = str(error)
            if verifiers_agree:
                record["status"] = "DUAL_VERIFIED_SAT_CONSTRUCTION"
                stop.set()
            else:
                record["status"] = "E0_VERIFICATION_FAILED"
        return record

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        records = list(pool.map(execute, requested))
    records.sort(key=lambda record: record["catalog_line"])
    for record in records:
        write_json(
            args.output_dir / f"line_{record['catalog_line']:03d}.result.json",
            record,
        )

    status_counts: dict[str, int] = {}
    best_e: int | None = None
    best_lines: list[int] = []
    for record in records:
        status = str(record["status"])
        status_counts[status] = status_counts.get(status, 0) + 1
        if isinstance(record.get("E"), int):
            objective = int(record["E"])
            if best_e is None or objective < best_e:
                best_e = objective
                best_lines = [int(record["catalog_line"])]
            elif objective == best_e:
                best_lines.append(int(record["catalog_line"]))
    certified_count = status_counts.get("DUAL_VERIFIED_SAT_CONSTRUCTION", 0)
    record_coverage = [record["catalog_line"] for record in records] == requested
    skipped_count = status_counts.get("SKIPPED_AFTER_CONSTRUCTION", 0)
    incomplete_statuses = {
        "TIMEOUT_NO_CONCLUSION",
        "SEARCH_ERROR",
        "OUTPUT_PARSE_ERROR",
        "E0_VERIFICATION_FAILED",
    }
    incomplete_count = sum(status_counts.get(status, 0) for status in incomplete_statuses)
    batch_status = (
        "CONSTRUCTION_CERTIFIED"
        if certified_count
        else "INCOMPLETE_NO_CONCLUSION"
        if incomplete_count or skipped_count
        else "COMPLETE_NO_CONSTRUCTION"
    )
    summary = {
        "schema": "ramsey55.catalog_seed_search_batch.v1",
        "evidence_category": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        "status": batch_status,
        "started_utc": started_utc,
        "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "runtime_seconds": time.monotonic() - started,
        "catalog": str(args.catalog.resolve()),
        "catalog_sha256": sha256_file(args.catalog),
        "search": str(args.search.resolve()),
        "search_sha256": sha256_file(args.search),
        "exhaustive_verifier_sha256": sha256_file(args.exhaustive_verifier),
        "bitset_verifier_sha256": sha256_file(args.bitset_verifier),
        "plan": str(args.plan.resolve()),
        "plan_sha256": sha256_file(args.plan),
        "plan_schema": plan["schema"],
        "plan_status": plan["status"],
        "configuration": {
            "first_line": args.first_line if args.lines_file is None else None,
            "last_line": args.last_line,
            "lines_file": (
                str(args.lines_file.resolve()) if args.lines_file is not None else None
            ),
            "lines_file_sha256": (
                sha256_file(args.lines_file) if args.lines_file is not None else None
            ),
            "seed_base": args.seed_base,
            "steps": args.steps,
            "restarts": args.restarts,
            "tabu": args.tabu,
            "random_walk": args.random_walk,
            "breakout_interval": args.breakout_interval,
            "initial_perturbation": args.initial_perturbation,
            "workers": args.workers,
            "instance_time_limit": args.instance_time_limit,
            "verifier_time_limit": args.verifier_time_limit,
        },
        "requested_count": len(requested),
        "record_count": len(records),
        "exact_record_coverage": record_coverage,
        "exact_line_coverage": record_coverage and skipped_count == 0,
        "searched_lines": [
            record["catalog_line"]
            for record in records
            if record["status"] != "SKIPPED_AFTER_CONSTRUCTION"
        ],
        "status_counts": status_counts,
        "best_E": best_e,
        "best_lines": best_lines,
        "certified_construction_count": certified_count,
        "scope_warning": (
            "Failure to find E=0 is not nonexistence evidence; only a dual-verified "
            "E=0 output is a Ramsey construction."
        ),
    }
    write_json(args.summary, summary)
    print(json.dumps(summary, sort_keys=True))
    if certified_count:
        return 10
    return 0 if batch_status == "COMPLETE_NO_CONSTRUCTION" else 2


if __name__ == "__main__":
    raise SystemExit(main())
