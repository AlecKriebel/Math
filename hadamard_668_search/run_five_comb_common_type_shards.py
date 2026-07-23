#!/usr/bin/env python3
"""Resume-safe scheduler for the 48 x 8 common-type carrier CP shards."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from ortools.sat.python import cp_model

from search_five_comb_common_type_cp_sat import build_model


BASE = Path(__file__).resolve().parent
SEARCH = BASE / "search_five_comb_common_type_cp_sat.py"
FORMAT = "h668-five-comb-common-type-shard-v1"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def parse_key_values(output: str) -> dict[str, str]:
    result = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


def shard_path(directory: Path, quartet: int, projective: int) -> Path:
    return directory / f"q{quartet:02d}_p{projective}.json"


def completed(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return payload.get("format") == FORMAT and payload.get("status") in {
        "INFEASIBLE",
        "FEASIBLE",
        "OPTIMAL",
    }


def run_shard(
    quartet: int,
    projective: int,
    *,
    time_limit: float,
    workers: int,
    max_memory_mb: int,
    directory: Path,
) -> dict[str, Any]:
    command = [
        sys.executable,
        str(SEARCH),
        "--quartet",
        str(quartet),
        "--projective",
        str(projective),
        "--time-limit",
        str(time_limit),
        "--workers",
        str(workers),
        "--max-memory-mb",
        str(max_memory_mb),
    ]
    started = now()
    result = subprocess.run(
        command,
        cwd=BASE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    fields = parse_key_values(result.stdout)
    payload = {
        "format": FORMAT,
        "quartet": quartet,
        "projective": projective,
        "status": fields.get("status", "ERROR"),
        "wall_time_seconds": float(fields.get("wall_time", "nan")),
        "conflicts": int(fields.get("conflicts", "-1")),
        "branches": int(fields.get("branches", "-1")),
        "booleans": int(fields.get("booleans", "-1")),
        "returncode": result.returncode,
        "started_at": started,
        "finished_at": now(),
        "command": command,
        "stdout": result.stdout,
    }
    atomic_json(shard_path(directory, quartet, projective), payload)
    return payload


def run_shard_in_process(
    quartet: int,
    projective: int,
    *,
    time_limit: float,
    workers: int,
    max_memory_mb: int,
    directory: Path,
) -> dict[str, Any]:
    """Solve one shard without paying a fresh Python/OR-Tools import cost."""

    started = now()
    model, _types, _orientations, _holes = build_model(quartet, projective)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.max_memory_in_mb = max_memory_mb
    status_code = solver.solve(model)
    status = solver.status_name(status_code)
    if status in {"FEASIBLE", "OPTIMAL"}:
        raise RuntimeError(
            "an in-process shard found a candidate; rerun the standalone "
            "constructor immediately for independent full verification"
        )
    stdout = (
        f"status={status}\n"
        f"quartet={quartet}\n"
        f"projective={projective}\n"
        f"wall_time={solver.wall_time:.6f}\n"
        f"conflicts={solver.num_conflicts}\n"
        f"branches={solver.num_branches}\n"
        f"booleans={solver.num_booleans}\n"
    )
    payload = {
        "format": FORMAT,
        "quartet": quartet,
        "projective": projective,
        "status": status,
        "wall_time_seconds": solver.wall_time,
        "conflicts": solver.num_conflicts,
        "branches": solver.num_branches,
        "booleans": solver.num_booleans,
        "returncode": 1 if status == "INFEASIBLE" else 2,
        "started_at": started,
        "finished_at": now(),
        "command": ["in-process", f"q={quartet}", f"p={projective}"],
        "stdout": stdout,
    }
    atomic_json(shard_path(directory, quartet, projective), payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--workers-per-shard", type=int, default=1)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--max-memory-mb", type=int, default=2048)
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=BASE / "output" / "five_comb_common_type_cp",
    )
    parser.add_argument("--quartet-start", type=int, default=0)
    parser.add_argument("--quartet-end", type=int, default=47)
    parser.add_argument(
        "--in-process",
        action="store_true",
        help="reuse one imported runtime across all shards",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.jobs < 1 or args.workers_per_shard < 1:
        raise ValueError("worker counts must be positive")
    if not 0 <= args.quartet_start <= args.quartet_end < 48:
        raise ValueError("quartet range must lie in 0..47")
    shards = [
        (quartet, projective)
        for quartet in range(args.quartet_start, args.quartet_end + 1)
        for projective in range(8)
        if not completed(shard_path(args.output_directory, quartet, projective))
    ]
    print(f"pending={len(shards)}")
    counts: dict[str, int] = {}
    worker_function = run_shard_in_process if args.in_process else run_shard
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {
            executor.submit(
                worker_function,
                quartet,
                projective,
                time_limit=args.time_limit,
                workers=args.workers_per_shard,
                max_memory_mb=args.max_memory_mb,
                directory=args.output_directory,
            ): (quartet, projective)
            for quartet, projective in shards
        }
        for future in as_completed(futures):
            quartet, projective = futures[future]
            payload = future.result()
            status = payload["status"]
            counts[status] = counts.get(status, 0) + 1
            print(
                f"q={quartet:02d} p={projective} status={status} "
                f"wall={payload['wall_time_seconds']:.3f}"
            )
            if status in {"FEASIBLE", "OPTIMAL"}:
                print("verified candidate found; inspect the candidate output")
    print("run_counts=" + json.dumps(counts, sort_keys=True))
    remaining = sum(
        not completed(shard_path(args.output_directory, quartet, projective))
        for quartet in range(args.quartet_start, args.quartet_end + 1)
        for projective in range(8)
    )
    print(f"remaining={remaining}")
    return int(remaining != 0)


if __name__ == "__main__":
    raise SystemExit(main())
