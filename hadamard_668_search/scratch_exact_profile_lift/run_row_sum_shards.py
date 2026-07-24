#!/usr/bin/env python3
"""Resumable bounded row-margin shards for the first exact h=2 profile."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from threading import Lock
import time

HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
if str(SEARCH) not in sys.path:
    sys.path.insert(0, str(SEARCH))

from verify_lp333_order3_labeled_jet import (  # noqa: E402
    CANONICAL_ZERO_EXPONENTS,
    ROOTS,
    ROW_SUM_CATALOG_PATH,
    ROW_SUM_CATALOG_SHA256,
)
from verify_lp333_order3_profile_zero_gate import (  # noqa: E402
    aggregate_shard_target,
)


TARGET = (2, -2, -2, 2)
WORKER = HERE / "search_exact_profile_lift_xor.py"


def compatible_indices() -> tuple[int, ...]:
    payload = ROW_SUM_CATALOG_PATH.read_bytes()
    if sha256(payload).hexdigest() != ROW_SUM_CATALOG_SHA256:
        raise AssertionError("the pinned row-sum catalog changed")
    rows = list(csv.reader(payload.decode("ascii").splitlines()))
    zero = tuple(ROOTS[exponent] for exponent in CANONICAL_ZERO_EXPONENTS)
    result = []
    for index, raw in enumerate(rows[1:]):
        if len(raw) != 18:
            raise AssertionError("a row-sum entry has the wrong width")
        values = tuple(int(value) for value in raw)
        aggregate = []
        for row, core in enumerate(zero):
            difference = (
                values[2 * row] - core[0],
                values[2 * row + 1] - core[1],
            )
            if difference[0] % 3 or difference[1] % 3:
                raise AssertionError("a row-sum entry has a nonintegral lift")
            aggregate.extend((difference[0] // 3, difference[1] // 3))
        if aggregate_shard_target(aggregate) == TARGET:
            result.append(index)
    if len(result) != 72:
        raise AssertionError("the exact profile should have 72 row-margin shards")
    return tuple(result)


def atomic_json(path: Path, payload: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def parse_status(output: str, returncode: int) -> str:
    for line in output.splitlines():
        if line.startswith("status="):
            return line.split("=", 1)[1].strip()
    if returncode == 0 and "PASS: exact LP(333)" in output:
        return "FEASIBLE"
    return "ERROR"


def run_one(
    index: int,
    attempt: int,
    seconds: float,
    memory_mb: int,
    solver_python: Path,
    output_directory: Path,
) -> dict[str, object]:
    seed = 668 + 1009 * attempt + index
    started = time.time()
    command = (
        str(solver_python),
        str(WORKER),
        "--row-sum-index",
        str(index),
        "--time-limit",
        str(seconds),
        "--workers",
        "1",
        "--max-memory-mb",
        str(memory_mb),
        "--seed",
        str(seed),
    )
    completed = subprocess.run(
        command,
        cwd=SEARCH.parent,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=seconds + 120,
        check=False,
    )
    status = parse_status(completed.stdout, completed.returncode)
    log_path = output_directory / f"row_{index:04d}_attempt_{attempt:02d}.log"
    log_path.write_text(completed.stdout, encoding="utf-8")
    return {
        "row_sum_index": index,
        "attempt": attempt,
        "seed": seed,
        "time_limit_seconds": seconds,
        "elapsed_seconds": time.time() - started,
        "returncode": completed.returncode,
        "status": status,
        "log": log_path.name,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds-per-shard", type=float, default=10.0)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--memory-per-shard-mb", type=int, default=2500)
    parser.add_argument(
        "--solver-python",
        type=Path,
        default=Path(sys.executable),
        help="Python interpreter whose environment contains OR-Tools",
    )
    parser.add_argument("--attempt", type=int, default=0)
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=HERE / "output" / "row_sum_shards",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.seconds_per_shard <= 0 or args.jobs <= 0:
        raise SystemExit("time and job counts must be positive")
    if args.jobs * args.memory_per_shard_mb > 12_000:
        raise SystemExit("aggregate shard memory cap must not exceed 12 GB")
    if not args.solver_python.is_file():
        raise SystemExit(
            f"solver environment is missing: {args.solver_python}"
        )
    args.output_directory.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.output_directory / "checkpoint.json"
    if checkpoint_path.is_file():
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    else:
        checkpoint = {
            "schema": "lp333-exact-profile-row-shards-v1",
            "target": TARGET,
            "compatible_row_sum_indices": compatible_indices(),
            "runs": [],
        }
    indices = compatible_indices()
    if tuple(checkpoint["compatible_row_sum_indices"]) != indices:
        raise AssertionError("the checkpoint row-margin shard list changed")
    completed_keys = {
        (int(run["row_sum_index"]), int(run["attempt"]))
        for run in checkpoint["runs"]
    }
    pending = [
        index for index in indices if (index, args.attempt) not in completed_keys
    ]
    lock = Lock()
    print(f"compatible_shards={len(indices)}", flush=True)
    print(f"pending_shards={len(pending)}", flush=True)
    print(f"parallel_jobs={args.jobs}", flush=True)

    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {
            executor.submit(
                run_one,
                index,
                args.attempt,
                args.seconds_per_shard,
                args.memory_per_shard_mb,
                args.solver_python,
                args.output_directory,
            ): index
            for index in pending
        }
        for future in as_completed(futures):
            record = future.result()
            with lock:
                checkpoint["runs"].append(record)
                checkpoint["runs"].sort(
                    key=lambda run: (
                        int(run["attempt"]),
                        int(run["row_sum_index"]),
                    )
                )
                atomic_json(checkpoint_path, checkpoint)
            print(
                f"row={record['row_sum_index']} status={record['status']} "
                f"elapsed={record['elapsed_seconds']:.3f}",
                flush=True,
            )
            if record["status"] in ("FEASIBLE", "OPTIMAL"):
                print("VERIFIED CANDIDATE FOUND; inspect the shard log", flush=True)

    statuses: dict[str, int] = {}
    for run in checkpoint["runs"]:
        if int(run["attempt"]) == args.attempt:
            status = str(run["status"])
            statuses[status] = statuses.get(status, 0) + 1
    print("status_census=" + json.dumps(statuses, sort_keys=True))
    print(f"checkpoint={checkpoint_path}")


if __name__ == "__main__":
    main()
