#!/usr/bin/env python3
"""Resume-safe scheduler for the 32 projective-core exact CP shards."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from ortools.sat.python import cp_model

from search_five_comb_unrestricted_projective_cp_sat import (
    build_model,
    reconstruct,
)


BASE = Path(__file__).resolve().parent
SEARCH = BASE / "search_five_comb_unrestricted_projective_cp_sat.py"
FORMAT = "h668-five-comb-unrestricted-core-shard-v1"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def parse_key_values(output: str) -> dict[str, str]:
    result = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


def shard_path(directory: Path, quartet: int, core: int) -> Path:
    return directory / f"q{quartet:02d}_core{core:02d}.json"


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quartet", type=int, choices=range(48))
    parser.add_argument("--quartet-start", type=int, default=0, choices=range(48))
    parser.add_argument("--quartet-end", type=int, default=47, choices=range(48))
    parser.add_argument("--core-start", type=int, default=0, choices=range(32))
    parser.add_argument("--core-end", type=int, default=31, choices=range(32))
    parser.add_argument("--time-limit", type=float, default=90.0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--max-memory-mb", type=int, default=3072)
    parser.add_argument(
        "--in-process",
        action="store_true",
        help="reuse one imported Python/OR-Tools runtime across all cores",
    )
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=BASE / "output" / "five_comb_unrestricted_core_cp",
    )
    parser.add_argument(
        "--candidate-directory",
        type=Path,
        default=BASE / "output" / "five_comb_unrestricted_core_candidates",
    )
    return parser.parse_args()


def run_in_process(
    args: argparse.Namespace,
    quartet: int,
    core: int,
    candidate: Path,
) -> dict[str, Any]:
    started = now()
    model, label_vars, type_vars, orientation_vars, hole_vars = build_model(
        quartet, core
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    status_code = solver.solve(model)
    status = solver.status_name(status_code)
    if status in {"FEASIBLE", "OPTIMAL"}:
        labels = tuple(solver.value(variable) for variable in label_vars)
        types = tuple(solver.value(variable) for variable in type_vars)
        orientations = tuple(
            solver.value(variable) for variable in orientation_vars
        )
        holes = tuple(solver.value(variable) for variable in hole_vars)
        sequences = reconstruct(
            quartet, labels, types, orientations, holes
        )
        from construction import goethals_seidel, verify_hadamard
        from seed import special_quadruple
        from variable_q_base import base_correlations, base_to_special

        if base_correlations(*sequences) != (334,) + (0,) * 83:
            raise AssertionError("in-process solver emitted a false candidate")
        s, q = base_to_special(*sequences)
        verify_hadamard(goethals_seidel(special_quadruple(s, q)))
        atomic_json(
            candidate,
            {
                "format": "h668-five-comb-unrestricted-projective-v1",
                "quartet_index": quartet,
                "projective_core": core,
                "labels": list(labels),
                "types": list(types),
                "orientations": list(orientations),
                "holes": list(holes),
                "a": list(sequences[0]),
                "b": list(sequences[1]),
                "c": list(sequences[2]),
                "d": list(sequences[3]),
                "s": list(s),
                "q": list(q),
            },
        )
    stdout = (
        f"status={status}\n"
        f"quartet={quartet}\n"
        f"projective_core={core}\n"
        f"wall_time={solver.wall_time:.6f}\n"
        f"conflicts={solver.num_conflicts}\n"
        f"branches={solver.num_branches}\n"
        f"booleans={solver.num_booleans}\n"
    )
    return {
        "format": FORMAT,
        "quartet": quartet,
        "projective_core": core,
        "status": status,
        "wall_time_seconds": solver.wall_time,
        "conflicts": solver.num_conflicts,
        "branches": solver.num_branches,
        "booleans": solver.num_booleans,
        "returncode": (
            0 if status in {"FEASIBLE", "OPTIMAL"}
            else 1 if status == "INFEASIBLE"
            else 2
        ),
        "started_at": started,
        "finished_at": now(),
        "command": ["in-process", f"q={quartet}", f"core={core}"],
        "stdout": stdout,
    }


def main() -> int:
    args = parse_args()
    if args.core_start > args.core_end:
        raise ValueError("core-start must not exceed core-end")
    if args.quartet_start > args.quartet_end:
        raise ValueError("quartet-start must not exceed quartet-end")
    if args.time_limit <= 0 or args.workers < 1 or args.max_memory_mb < 1:
        raise ValueError("solver limits must be positive")
    quartets = (
        (args.quartet,)
        if args.quartet is not None
        else tuple(range(args.quartet_start, args.quartet_end + 1))
    )
    pending = tuple(
        (quartet, core)
        for quartet in quartets
        for core in range(args.core_start, args.core_end + 1)
        if not completed(shard_path(args.output_directory, quartet, core))
    )
    print(f"pending={len(pending)}", flush=True)
    counts: Counter[str] = Counter()
    for quartet, core in pending:
        candidate = (
            args.candidate_directory
            / f"q{quartet:02d}_core{core:02d}_candidate.json"
        )
        if args.in_process:
            payload = run_in_process(args, quartet, core, candidate)
        else:
            command = [
                sys.executable,
                str(SEARCH),
                "--quartet",
                str(quartet),
                "--projective-core",
                str(core),
                "--time-limit",
                str(args.time_limit),
                "--workers",
                str(args.workers),
                "--max-memory-mb",
                str(args.max_memory_mb),
                "--output",
                str(candidate),
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
            status = fields.get("status", "ERROR")
            payload = {
                "format": FORMAT,
                "quartet": quartet,
                "projective_core": core,
                "status": status,
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
        atomic_json(
            shard_path(args.output_directory, quartet, core),
            payload,
        )
        status = payload["status"]
        counts[status] += 1
        print(
            f"q={quartet:02d} core={core:02d} status={status} "
            f"wall={payload['wall_time_seconds']:.3f}",
            flush=True,
        )
        if status in {"FEASIBLE", "OPTIMAL"}:
            print(f"candidate={candidate}", flush=True)
            return 0
    remaining = sum(
        not completed(shard_path(args.output_directory, quartet, core))
        for quartet in quartets
        for core in range(args.core_start, args.core_end + 1)
    )
    print("run_counts=" + json.dumps(counts, sort_keys=True), flush=True)
    print(f"remaining={remaining}", flush=True)
    return int(remaining != 0)


if __name__ == "__main__":
    raise SystemExit(main())
