#!/usr/bin/env python3
"""Resume-safe scheduler for the exact BS(84,83) CP-SAT shard representatives."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
import time

from variable_q_base import MARGIN_SHARDS, MARGIN_SHARD_REPRESENTATIVES


STATUS_PATTERN = re.compile(r"^status=(\w+)$", re.MULTILINE)


def parse_shards(specification: str) -> tuple[int, ...]:
    if specification == "all":
        # Global alternation pairs 264 of the 288 normalized margin shards
        # and fixes 24, leaving 156 exhaustive representatives.
        return MARGIN_SHARD_REPRESENTATIVES
    result: set[int] = set()
    for part in specification.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            start, end = int(start_text), int(end_text)
            if end < start:
                raise ValueError(f"descending shard range: {part}")
            result.update(range(start, end + 1))
        else:
            result.add(int(part))
    if not result or min(result) < 0 or max(result) >= len(MARGIN_SHARDS):
        raise ValueError(f"shards must lie in 0..{len(MARGIN_SHARDS) - 1}")
    return tuple(sorted(result))


def completed_attempts(path: Path) -> set[tuple[int, int]]:
    result: set[tuple[int, int]] = set()
    if not path.exists():
        return result
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            result.add((int(record["shard"]), int(record["seed_index"])))
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
            raise ValueError(f"invalid JSONL record at {path}:{line_number}") from error
    return result


def append_record(path: Path, record: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")
        stream.flush()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--shards",
        default="all",
        help="all (156 alternation representatives), 0-287, or comma list",
    )
    parser.add_argument("--time-limit", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--max-memory-mb",
        type=int,
        default=2048,
        help="memory cap forwarded to each sequential CP-SAT attempt",
    )
    parser.add_argument("--seed", type=int, default=668)
    parser.add_argument("--seed-count", type=int, default=1)
    parser.add_argument(
        "--log",
        type=Path,
        default=Path("../tmp/hadamard_668_runs/variable_q_shards.jsonl"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("../tmp/hadamard_668_runs/variable_q_candidates"),
    )
    parser.add_argument("--rerun", action="store_true", help="ignore prior JSONL keys")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = Path(__file__).resolve().parent
    log_path = args.log if args.log.is_absolute() else project / args.log
    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else project / args.output_dir
    )
    if (
        args.time_limit <= 0
        or args.workers <= 0
        or args.max_memory_mb <= 0
        or args.seed_count <= 0
    ):
        print(
            "error=time limit, workers, memory cap, and seed count must be positive",
            file=sys.stderr,
        )
        return 2
    try:
        shards = parse_shards(args.shards)
        completed = set() if args.rerun else completed_attempts(log_path)
    except ValueError as error:
        print(f"error={error}", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    scheduled = [
        (shard, seed_index)
        for shard in shards
        for seed_index in range(args.seed_count)
        if (shard, seed_index) not in completed
    ]
    print(f"scheduled_attempts={len(scheduled)}")
    print(f"resume_log={log_path}")

    for ordinal, (shard, seed_index) in enumerate(scheduled, 1):
        random_seed = args.seed + 1009 * seed_index + shard
        candidate = output_dir / f"shard_{shard:03d}_seed_{seed_index:03d}.json"
        command = [
            sys.executable,
            str(project / "search_variable_q_cp_sat.py"),
            "--shard",
            str(shard),
            "--time-limit",
            str(args.time_limit),
            "--workers",
            str(args.workers),
            "--max-memory-mb",
            str(args.max_memory_mb),
            "--random-seed",
            str(random_seed),
            "--output",
            str(candidate),
        ]
        print(
            f"attempt={ordinal}/{len(scheduled)} shard={shard} "
            f"seed_index={seed_index} random_seed={random_seed}",
            flush=True,
        )
        started = time.monotonic()
        process = subprocess.run(
            command,
            cwd=project,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        elapsed = time.monotonic() - started
        match = STATUS_PATTERN.search(process.stdout)
        status = match.group(1) if match else "MISSING"
        record: dict[str, object] = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "shard": shard,
            "ordinary": MARGIN_SHARDS[shard][0],
            "alternating": MARGIN_SHARDS[shard][1],
            "seed_index": seed_index,
            "random_seed": random_seed,
            "time_limit": args.time_limit,
            "workers": args.workers,
            "max_memory_mb": args.max_memory_mb,
            "status": status,
            "returncode": process.returncode,
            "elapsed": elapsed,
            "candidate": str(candidate) if candidate.exists() else None,
            "output": process.stdout.strip().splitlines(),
        }
        append_record(log_path, record)
        print(f"status={status} elapsed={elapsed:.3f}", flush=True)

        if candidate.exists():
            verification = subprocess.run(
                [sys.executable, str(project / "verify_variable_q.py"), str(candidate)],
                cwd=project,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            print(verification.stdout, end="")
            if verification.returncode == 0:
                print(f"exact_candidate={candidate}")
                return 0
            print("error=solver wrote a candidate rejected by the independent verifier")
            return 3

    return 1 if scheduled else 0


if __name__ == "__main__":
    raise SystemExit(main())
