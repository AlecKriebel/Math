#!/usr/bin/env python3
"""Resume-safe sequential runner for the 298 exact LP333 signature shards.

Each shard invokes ``search_lp333_sextic_cp_sat.py`` in a separate process and
writes one atomic JSON record containing its exact command, solver status,
statistics, and captured output.  Existing records are skipped by default;
``--rerun-unknown`` repeats only records whose previous solver status was
UNKNOWN.  A candidate path can exist only if the searcher's strict LP333 and
H(668) replay gate completed successfully.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

from search_lp333_sextic_cp_sat import SIGNATURE_SHARD_VECTORS


SCHEMA = "lp333-sextic-signature-shard-run-v1"


def parse_key_values(output: str) -> dict[str, str]:
    """Extract the searcher's simple ``key=value`` report lines."""

    result: dict[str, str] = {}
    for line in output.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key and all(character.isalnum() or character == "_" for character in key):
            result[key] = value
    return result


def load_record(path: Path) -> dict[str, Any] | None:
    """Return a valid prior record, or ``None`` for a missing/corrupt file."""

    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if (
        not isinstance(payload, dict)
        or payload.get("schema") != SCHEMA
        or not isinstance(payload.get("shard"), int)
    ):
        return None
    return payload


def write_record_atomic(path: Path, payload: dict[str, Any]) -> None:
    """Atomically publish one completed shard record."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument(
        "--end", type=int, default=len(SIGNATURE_SHARD_VECTORS) - 1
    )
    parser.add_argument("--time-limit", type=float, default=3600.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--max-memory-mb", type=int, default=4096)
    parser.add_argument("--random-seed", type=int, default=668)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output/lp333_sextic_signature_shards"),
    )
    parser.add_argument(
        "--rerun-unknown",
        action="store_true",
        help="repeat shards whose existing record has solver status UNKNOWN",
    )
    parser.add_argument("--log-search-progress", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    shard_count = len(SIGNATURE_SHARD_VECTORS)
    if not 0 <= args.start <= args.end < shard_count:
        print(
            f"error: require 0 <= start <= end < {shard_count}",
            file=sys.stderr,
        )
        return 2
    if args.time_limit <= 0 or args.workers <= 0 or args.max_memory_mb <= 0:
        print(
            "error: time limit, workers, and memory cap must be positive",
            file=sys.stderr,
        )
        return 2

    searcher = Path(__file__).with_name("search_lp333_sextic_cp_sat.py")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for shard in range(args.start, args.end + 1):
        record_path = args.output_dir / f"shard_{shard:03d}.json"
        prior = load_record(record_path)
        if prior is not None and not (
            args.rerun_unknown and prior.get("status") == "UNKNOWN"
        ):
            print(f"shard={shard} action=skip status={prior.get('status')}")
            continue

        candidate_path = args.output_dir / f"candidate_shard_{shard:03d}.json"
        command = [
            sys.executable,
            str(searcher),
            "--signature-shard",
            str(shard),
            "--time-limit",
            str(args.time_limit),
            "--workers",
            str(args.workers),
            "--max-memory-mb",
            str(args.max_memory_mb),
            "--random-seed",
            str(args.random_seed + shard),
            "--output",
            str(candidate_path),
        ]
        if args.log_search_progress:
            command.append("--log-search-progress")
        print(f"shard={shard} action=run aggregate={SIGNATURE_SHARD_VECTORS[shard]}")
        started = time.time()
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
        fields = parse_key_values(completed.stdout)
        status = fields.get("status", "PROCESS_ERROR")
        candidate_verified = (
            status in {"FEASIBLE", "OPTIMAL"}
            and completed.returncode == 0
            and candidate_path.is_file()
            and fields.get("hadamard_verified") == "true"
        )
        payload: dict[str, Any] = {
            "schema": SCHEMA,
            "shard": shard,
            "aggregate": list(SIGNATURE_SHARD_VECTORS[shard]),
            "status": status,
            "returncode": completed.returncode,
            "candidate_verified": candidate_verified,
            "candidate": str(candidate_path) if candidate_verified else None,
            "started_unix": started,
            "elapsed_seconds": time.time() - started,
            "parameters": {
                "time_limit": args.time_limit,
                "workers": args.workers,
                "max_memory_mb": args.max_memory_mb,
                "random_seed": args.random_seed + shard,
            },
            "report": fields,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        if status in {"FEASIBLE", "OPTIMAL"} and not candidate_verified:
            payload["status"] = "CANDIDATE_GATE_FAILED"
        write_record_atomic(record_path, payload)
        print(
            f"shard={shard} status={payload['status']} "
            f"elapsed={payload['elapsed_seconds']:.3f}"
        )
        if candidate_verified:
            print(f"verified_candidate={candidate_path}")
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
