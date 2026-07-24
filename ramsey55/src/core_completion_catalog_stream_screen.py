#!/usr/bin/env python3
"""Eight-persistent-worker constructive screen of all catalog fixed cores."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_catalog_batch import atomic_json, data_line_count, sha256_file  # noqa: E402
from core_completion_catalog_screen import (  # noqa: E402
    ERROR,
    FAILED_SAT,
    LIMIT,
    OBSERVED_UNSAT,
    SCREEN_ID,
    VERIFIED_SAT,
    preserve_and_verify_sat,
    record_path,
)


STREAM_SCREEN_ID = (
    "ramsey55_core_completion_catalog_k1_persistent_screen_v1"
)


class Progress:
    def __init__(self, total: int) -> None:
        self.total = total
        self.completed = 0
        self.lock = threading.Lock()
        self.started = time.monotonic()

    def add(
        self, worker: int, line: int, deleted: int, classification: str
    ) -> None:
        with self.lock:
            self.completed += 1
            if (
                self.completed % 250 == 0
                or classification != OBSERVED_UNSAT
            ):
                print(
                    json.dumps(
                        {
                            "completed": self.completed,
                            "total": self.total,
                            "worker": worker,
                            "catalog_line": line,
                            "deleted_vertex": deleted,
                            "classification": classification,
                            "elapsed_seconds": time.monotonic() - self.started,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )


def validate_plan(
    plan_path: Path,
    *,
    catalog_sha256: str,
    catalog_lines: int,
    solver_sha256: str,
    persistent_solver_source_sha256: str,
    included_solver_source_sha256: str,
    stream_runner_sha256: str,
    coverage_checker_sha256: str,
    jobs: int,
    seconds_limit: float,
    node_limit: int,
) -> dict[str, object]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    required = {
        "catalog_sha256": catalog_sha256,
        "catalog_data_line_count": catalog_lines,
        "full_pair_count": catalog_lines * 42,
        "persistent_solver_binary_sha256": solver_sha256,
        "persistent_solver_source_sha256": persistent_solver_source_sha256,
        "included_solver_source_sha256": included_solver_source_sha256,
        "stream_runner_sha256": stream_runner_sha256,
        "coverage_checker_sha256": coverage_checker_sha256,
        "jobs": jobs,
        "seconds_limit_per_instance": seconds_limit,
        "node_limit_per_instance": node_limit,
        "unsat_proof_replay": False,
        "worker_mode": "persistent_contiguous_line_ranges",
    }
    mismatches = {
        key: {"plan": plan.get(key), "command": value}
        for key, value in required.items()
        if plan.get(key) != value
    }
    if mismatches:
        raise ValueError(f"persistent screen plan mismatch: {mismatches}")
    return plan


def classify_result(
    solver_result: dict[str, object],
    *,
    worker: int,
    worker_started: float,
    catalog: Path,
    catalog_sha256: str,
    solver: Path,
    solver_sha256: str,
    output_dir: Path,
    python: Path,
    exhaustive_verifier: Path,
    bitset_verifier: Path,
) -> dict[str, object]:
    line = int(solver_result["catalog_line"])
    deleted = int(solver_result["deleted_vertex"])
    status = solver_result.get("status")
    record: dict[str, object] = {
        "screen": STREAM_SCREEN_ID,
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "catalog": str(catalog.resolve()),
        "catalog_sha256": catalog_sha256,
        "catalog_line": line,
        "deleted_vertex": deleted,
        "solver_path": str(solver.resolve()),
        "solver_sha256": solver_sha256,
        "worker": worker,
        "worker_elapsed_at_receipt_seconds": (
            time.monotonic() - worker_started
        ),
        "solver_result": solver_result,
        "fixed_core_scope": (
            "only the induced 41-vertex core selected by this catalog line "
            "and deletion label"
        ),
        "negative_certified": False,
        "proof_generated": False,
        "proof_checked": False,
    }
    if status == "UNSAT":
        record.update(
            {
                "solver_returncode_semantics": 20,
                "classification": OBSERVED_UNSAT,
                "evidence_category": (
                    "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
                ),
            }
        )
    elif status == "LIMIT":
        record.update(
            {
                "solver_returncode_semantics": 2,
                "classification": LIMIT,
                "evidence_category": (
                    "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
                ),
            }
        )
    elif status == "SAT":
        record.update(
            preserve_and_verify_sat(
                catalog=catalog,
                catalog_sha256=catalog_sha256,
                line=line,
                deleted=deleted,
                solver_result=solver_result,
                output_dir=output_dir,
                python=python,
                exhaustive_verifier=exhaustive_verifier,
                bitset_verifier=bitset_verifier,
            )
        )
        record["solver_returncode_semantics"] = 10
        record["evidence_category"] = (
            "CERTIFIED"
            if record["classification"] == VERIFIED_SAT
            else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        )
    else:
        raise ValueError(f"unrecognized solver status {status!r}")
    path = record_path(output_dir, line, deleted)
    atomic_json(path, record)
    record["record_path"] = str(path.resolve())
    record["record_sha256"] = sha256_file(path)
    return record


def run_worker(
    *,
    worker: int,
    line_start: int,
    line_end: int,
    catalog: Path,
    catalog_sha256: str,
    solver: Path,
    solver_sha256: str,
    output_dir: Path,
    seconds_limit: float,
    node_limit: int,
    python: Path,
    exhaustive_verifier: Path,
    bitset_verifier: Path,
    progress: Progress,
) -> dict[str, object]:
    started = time.monotonic()
    process = subprocess.Popen(
        (
            str(solver),
            "--graph",
            str(catalog),
            "--line-start",
            str(line_start),
            "--line-end",
            str(line_end),
            "--node-limit",
            str(node_limit),
            "--seconds-limit",
            str(seconds_limit),
        ),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.stdout is None or process.stderr is None:
        raise RuntimeError("persistent solver pipes were not created")
    results: list[dict[str, object]] = []
    seen: set[tuple[int, int]] = set()
    for raw in process.stdout:
        if not raw.strip():
            continue
        solver_result = json.loads(raw)
        line = int(solver_result["catalog_line"])
        deleted = int(solver_result["deleted_vertex"])
        selected = (line, deleted)
        if not (
            line_start <= line <= line_end
            and 0 <= deleted < 42
            and selected not in seen
        ):
            raise RuntimeError(
                f"worker {worker} emitted invalid or duplicate pair {selected}"
            )
        seen.add(selected)
        record = classify_result(
            solver_result,
            worker=worker,
            worker_started=started,
            catalog=catalog,
            catalog_sha256=catalog_sha256,
            solver=solver,
            solver_sha256=solver_sha256,
            output_dir=output_dir,
            python=python,
            exhaustive_verifier=exhaustive_verifier,
            bitset_verifier=bitset_verifier,
        )
        results.append(record)
        progress.add(worker, line, deleted, str(record["classification"]))
    stderr = process.stderr.read()
    returncode = process.wait()
    expected_count = (line_end - line_start + 1) * 42
    counts = {
        classification: sum(
            result["classification"] == classification for result in results
        )
        for classification in (
            OBSERVED_UNSAT,
            VERIFIED_SAT,
            FAILED_SAT,
            LIMIT,
        )
    }
    expected_returncode = (
        10
        if counts[VERIFIED_SAT] or counts[FAILED_SAT]
        else 2
        if counts[LIMIT]
        else 0
    )
    if returncode != expected_returncode or len(results) != expected_count:
        raise RuntimeError(
            f"worker {worker} failed: returncode={returncode}, "
            f"expected_returncode={expected_returncode}, "
            f"records={len(results)}, expected_records={expected_count}, "
            f"stderr={stderr!r}"
        )
    return {
        "worker": worker,
        "line_start": line_start,
        "line_end": line_end,
        "expected_pair_count": expected_count,
        "actual_pair_count": len(results),
        "returncode": returncode,
        "stderr": stderr,
        "runtime_seconds": time.monotonic() - started,
        "counts": counts,
        "instances": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seconds-limit-per-instance", type=float, required=True)
    parser.add_argument("--node-limit-per-instance", type=int, required=True)
    parser.add_argument("--jobs", type=int, required=True)
    parser.add_argument(
        "--python", type=Path, default=Path(sys.executable)
    )
    parser.add_argument(
        "--exhaustive-verifier",
        type=Path,
        default=ROOT / "verify" / "exhaustive_verify.py",
    )
    parser.add_argument(
        "--bitset-verifier",
        type=Path,
        default=ROOT / "build" / "bitset_verify",
    )
    args = parser.parse_args()
    if args.jobs != 8:
        raise SystemExit("this preregistered screen requires exactly 8 jobs")
    if args.seconds_limit_per_instance <= 0:
        raise SystemExit("--seconds-limit-per-instance must be positive")
    if args.node_limit_per_instance <= 0:
        raise SystemExit("--node-limit-per-instance must be positive")
    for required in (
        args.catalog,
        args.solver,
        args.plan,
        args.python,
        args.exhaustive_verifier,
        args.bitset_verifier,
    ):
        if not required.is_file():
            raise SystemExit(f"required file is absent: {required}")

    started = time.monotonic()
    catalog_sha256 = sha256_file(args.catalog)
    catalog_lines = data_line_count(args.catalog)
    solver_sha256 = sha256_file(args.solver)
    persistent_solver_source_sha256 = sha256_file(
        ROOT / "src" / "core_completion_catalog_screen_solver.cpp"
    )
    included_solver_source_sha256 = sha256_file(
        ROOT / "src" / "core_completion_proof_solver.cpp"
    )
    stream_runner_sha256 = sha256_file(Path(__file__))
    coverage_checker_sha256 = sha256_file(
        ROOT / "verify" / "core_completion_catalog_screen_coverage.py"
    )
    validate_plan(
        args.plan,
        catalog_sha256=catalog_sha256,
        catalog_lines=catalog_lines,
        solver_sha256=solver_sha256,
        persistent_solver_source_sha256=persistent_solver_source_sha256,
        included_solver_source_sha256=included_solver_source_sha256,
        stream_runner_sha256=stream_runner_sha256,
        coverage_checker_sha256=coverage_checker_sha256,
        jobs=args.jobs,
        seconds_limit=args.seconds_limit_per_instance,
        node_limit=args.node_limit_per_instance,
    )
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise SystemExit("output directory must be absent or empty")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # 328 catalog lines divide exactly into eight contiguous ranges of 41.
    if catalog_lines % args.jobs:
        raise SystemExit("catalog line count is not divisible by job count")
    block = catalog_lines // args.jobs
    ranges = [
        (worker, worker * block + 1, (worker + 1) * block)
        for worker in range(args.jobs)
    ]
    progress = Progress(catalog_lines * 42)
    common = {
        "catalog": args.catalog.resolve(),
        "catalog_sha256": catalog_sha256,
        "solver": args.solver.resolve(),
        "solver_sha256": solver_sha256,
        "output_dir": args.output_dir.resolve(),
        "seconds_limit": args.seconds_limit_per_instance,
        "node_limit": args.node_limit_per_instance,
        "python": args.python.resolve(),
        "exhaustive_verifier": args.exhaustive_verifier.resolve(),
        "bitset_verifier": args.bitset_verifier.resolve(),
        "progress": progress,
    }
    workers: list[dict[str, object]] = []
    worker_errors: list[dict[str, object]] = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.jobs
    ) as executor:
        future_to_range = {
            executor.submit(
                run_worker,
                worker=worker,
                line_start=line_start,
                line_end=line_end,
                **common,
            ): (worker, line_start, line_end)
            for worker, line_start, line_end in ranges
        }
        for future in concurrent.futures.as_completed(future_to_range):
            worker, line_start, line_end = future_to_range[future]
            try:
                workers.append(future.result())
            except Exception as error:
                worker_errors.append(
                    {
                        "worker": worker,
                        "line_start": line_start,
                        "line_end": line_end,
                        "error": repr(error),
                    }
                )
    workers.sort(key=lambda item: int(item["worker"]))
    instances = [
        instance
        for worker in workers
        for instance in worker["instances"]
    ]
    instances.sort(
        key=lambda item: (
            int(item["catalog_line"]),
            int(item["deleted_vertex"]),
        )
    )
    counts = {
        classification: sum(
            item["classification"] == classification for item in instances
        )
        for classification in (
            OBSERVED_UNSAT,
            VERIFIED_SAT,
            FAILED_SAT,
            LIMIT,
            ERROR,
        )
    }
    summary = {
        "screen": STREAM_SCREEN_ID,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "evidence_category": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        "negative_result_policy": (
            "UNSAT statuses were not proof-replayed and are not certified"
        ),
        "scope": (
            "fixed induced 41-vertex catalog cores only; aggregate negatives "
            "are not global order-43 nonexistence"
        ),
        "catalog": str(args.catalog.resolve()),
        "catalog_sha256": catalog_sha256,
        "catalog_data_line_count": catalog_lines,
        "deletion_labels": list(range(42)),
        "expected_pair_count": catalog_lines * 42,
        "actual_record_count": len(instances),
        "jobs": args.jobs,
        "worker_mode": "persistent_contiguous_line_ranges",
        "worker_ranges": [
            {"worker": worker, "line_start": start, "line_end": end}
            for worker, start, end in ranges
        ],
        "seconds_limit_per_instance": args.seconds_limit_per_instance,
        "node_limit_per_instance": args.node_limit_per_instance,
        "unsat_proof_replay": False,
        "solver_path": str(args.solver.resolve()),
        "solver_sha256": solver_sha256,
        "persistent_solver_source_sha256": persistent_solver_source_sha256,
        "included_solver_source_sha256": included_solver_source_sha256,
        "plan": str(args.plan.resolve()),
        "plan_sha256": sha256_file(args.plan),
        "screen_source_sha256": stream_runner_sha256,
        "coverage_checker_sha256": coverage_checker_sha256,
        "runtime_seconds": time.monotonic() - started,
        "counts": counts,
        "worker_errors": worker_errors,
        "workers": [
            {key: value for key, value in worker.items() if key != "instances"}
            for worker in workers
        ],
        "instances": instances,
    }
    summary_path = args.output_dir / "catalog_k1_screen_summary.json"
    atomic_json(summary_path, summary)
    print(
        json.dumps(
            {
                "summary": str(summary_path),
                "summary_sha256": sha256_file(summary_path),
                "runtime_seconds": summary["runtime_seconds"],
                "expected_pair_count": summary["expected_pair_count"],
                "actual_record_count": summary["actual_record_count"],
                "counts": counts,
                "worker_errors": worker_errors,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    if worker_errors or counts[ERROR] or counts[FAILED_SAT]:
        return 1
    if counts[VERIFIED_SAT]:
        return 10
    if counts[LIMIT]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
