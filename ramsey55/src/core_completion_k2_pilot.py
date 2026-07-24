#!/usr/bin/env python3
"""Storage-capped persistent-worker pilot for delete-two/add-three cores."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_catalog_batch import (  # noqa: E402
    atomic_json,
    atomic_write,
    parse_last_json,
    sha256_file,
)
from core_completion_k2 import (  # noqa: E402
    completed_adjacency_k2,
    induced_core_two,
)
from core_completion_sat import count_forbidden_sets  # noqa: E402
from graph_io import (  # noqa: E402
    encode_graph6,
    read_graph,
    write_canonical_artifact,
)


PILOT_ID = "ramsey55_core_completion_k2_persistent_pilot_v1"
OBSERVED_UNSAT = "OBSERVED_UNSAT_UNCHECKED"
VERIFIED_SAT = "DUAL_VERIFIED_SAT_CONSTRUCTION"
FAILED_SAT = "SAT_MODEL_VERIFICATION_FAILED"
LIMIT = "LIMIT_NO_CONCLUSION"
ERROR = "PILOT_ERROR"


def parse_pairs(path: Path) -> list[tuple[int, int, int]]:
    pairs: list[tuple[int, int, int]] = []
    for physical_line, raw in enumerate(
        path.read_text(encoding="ascii").splitlines(), start=1
    ):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        fields = stripped.split()
        if len(fields) != 3:
            raise ValueError(
                f"invalid pair record at physical line {physical_line}"
            )
        selected = tuple(map(int, fields))
        line, left, right = selected
        if line < 1 or not 0 <= left < right < 42:
            raise ValueError(f"invalid pair selection {selected}")
        pairs.append(selected)
    if not pairs or len(pairs) != len(set(pairs)):
        raise ValueError("pair list is empty or contains duplicates")
    return pairs


def preserve_and_verify_sat(
    *,
    catalog: Path,
    catalog_sha256: str,
    solver_result: dict[str, object],
    output_dir: Path,
    python: Path,
    exhaustive_verifier: Path,
    bitset_verifier: Path,
) -> dict[str, object]:
    line = int(solver_result["catalog_line"])
    left = int(solver_result["deleted_left"])
    right = int(solver_result["deleted_right"])
    raw_true = solver_result.get("true_variables")
    if not isinstance(raw_true, list):
        raise ValueError("SAT result has no true-variable list")
    true_variables = sorted(int(value) for value in raw_true)
    stem = f"line_{line:03d}_delete_{left:02d}_{right:02d}"
    candidate_dir = output_dir / "sat_candidates" / stem
    model = candidate_dir / f"{stem}.model.json"
    atomic_json(
        model,
        {
            "pilot": PILOT_ID,
            "preserved_utc": datetime.now(timezone.utc).isoformat(),
            "catalog_sha256": catalog_sha256,
            "catalog_line": line,
            "deleted_left": left,
            "deleted_right": right,
            "variable_numbering": "zero-based, as emitted by C++ solver",
            "true_variables": true_variables,
            "solver_result": solver_result,
        },
    )

    base = read_graph(catalog, line)
    core, retained = induced_core_two(base, left, right)
    true_set = set(true_variables)
    assignment = [variable in true_set for variable in range(123)]
    completed = completed_adjacency_k2(core, assignment)
    internal_counts = count_forbidden_sets(completed, 5)
    graph6 = candidate_dir / f"{stem}.candidate.g6"
    canonical = candidate_dir / f"{stem}.candidate.canonical.json"
    atomic_write(graph6, (encode_graph6(completed) + "\n").encode("ascii"))
    canonical_sha256 = write_canonical_artifact(
        completed,
        canonical,
        provenance={
            "source": PILOT_ID,
            "catalog_sha256": catalog_sha256,
            "catalog_line": line,
            "deleted_original_vertices": [left, right],
            "retained_original_vertices": list(retained),
            "model_sha256": sha256_file(model),
        },
    )
    exhaustive = subprocess.run(
        (str(python), str(exhaustive_verifier), str(graph6)),
        text=True,
        capture_output=True,
        check=False,
    )
    bitset = subprocess.run(
        (str(bitset_verifier), str(graph6)),
        text=True,
        capture_output=True,
        check=False,
    )
    exhaustive_result = parse_last_json(
        exhaustive.stdout, "exhaustive verifier"
    )
    bitset_result = parse_last_json(bitset.stdout, "bitset verifier")
    verified = (
        internal_counts == (0, 0)
        and exhaustive.returncode == 0
        and exhaustive_result.get("valid") is True
        and bitset.returncode == 0
        and bitset_result.get("valid") is True
    )
    verification = candidate_dir / f"{stem}.verification.json"
    atomic_json(
        verification,
        {
            "verified": verified,
            "internal_forbidden_counts": list(internal_counts),
            "exhaustive_returncode": exhaustive.returncode,
            "exhaustive_stderr": exhaustive.stderr,
            "exhaustive_result": exhaustive_result,
            "bitset_returncode": bitset.returncode,
            "bitset_stderr": bitset.stderr,
            "bitset_result": bitset_result,
        },
    )
    return {
        "classification": VERIFIED_SAT if verified else FAILED_SAT,
        "dual_verified": verified,
        "model_path": str(model.resolve()),
        "model_sha256": sha256_file(model),
        "candidate_graph6_path": str(graph6.resolve()),
        "candidate_graph6_sha256": sha256_file(graph6),
        "candidate_canonical_path": str(canonical.resolve()),
        "candidate_canonical_sha256": canonical_sha256,
        "verification_path": str(verification.resolve()),
        "verification_sha256": sha256_file(verification),
    }


def validate_plan(
    plan_path: Path,
    *,
    catalog_sha256: str,
    solver_sha256: str,
    runner_sha256: str,
    pair_files: list[Path],
    jobs: int,
    seconds_limit: float,
    node_limit: int,
    output_byte_cap: int,
    reserve_bytes: int,
    max_wall_seconds: float,
) -> dict[str, object]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    planned_shards = plan.get("shards")
    actual_shards = [
        {
            "pairs_sha256": sha256_file(path),
            "pair_count": len(parse_pairs(path)),
        }
        for path in pair_files
    ]
    required = {
        "catalog_sha256": catalog_sha256,
        "solver_binary_sha256": solver_sha256,
        "runner_source_sha256": runner_sha256,
        "jobs": jobs,
        "seconds_limit_per_instance": seconds_limit,
        "node_limit_per_instance": node_limit,
        "output_byte_cap": output_byte_cap,
        "free_disk_reserve_bytes": reserve_bytes,
        "max_wall_seconds": max_wall_seconds,
    }
    mismatches = {
        key: {"plan": plan.get(key), "command": value}
        for key, value in required.items()
        if plan.get(key) != value
    }
    planned_compact = (
        [
            {
                "pairs_sha256": shard.get("pairs_sha256"),
                "pair_count": shard.get("pair_count"),
            }
            for shard in planned_shards
        ]
        if isinstance(planned_shards, list)
        else None
    )
    if planned_compact != actual_shards:
        mismatches["shards"] = {
            "plan": planned_compact,
            "command": actual_shards,
        }
    if mismatches:
        raise ValueError(f"k2 pilot plan mismatch: {mismatches}")
    return plan


def classify(
    solver_result: dict[str, object],
    *,
    catalog: Path,
    catalog_sha256: str,
    output_dir: Path,
    python: Path,
    exhaustive_verifier: Path,
    bitset_verifier: Path,
) -> dict[str, object]:
    record: dict[str, object] = {
        "pilot": PILOT_ID,
        "catalog_line": int(solver_result["catalog_line"]),
        "deleted_left": int(solver_result["deleted_left"]),
        "deleted_right": int(solver_result["deleted_right"]),
        "solver_result": solver_result,
        "negative_certified": False,
        "proof_generated": False,
        "proof_checked": False,
        "fixed_core_scope": (
            "only this induced 40-vertex catalog core completed by three "
            "new vertices"
        ),
    }
    status = solver_result.get("status")
    if status == "UNSAT":
        record.update(
            {
                "classification": OBSERVED_UNSAT,
                "evidence_category": (
                    "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
                ),
            }
        )
    elif status == "LIMIT":
        record.update(
            {
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
                solver_result=solver_result,
                output_dir=output_dir,
                python=python,
                exhaustive_verifier=exhaustive_verifier,
                bitset_verifier=bitset_verifier,
            )
        )
        record["evidence_category"] = (
            "CERTIFIED"
            if record["classification"] == VERIFIED_SAT
            else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        )
    else:
        raise ValueError(f"unrecognized solver status {status!r}")
    return record


def run_worker(
    *,
    worker: int,
    pairs_path: Path,
    expected_pairs: list[tuple[int, int, int]],
    catalog: Path,
    catalog_sha256: str,
    solver: Path,
    output_dir: Path,
    seconds_limit: float,
    node_limit: int,
    deadline: float,
    stop_event: threading.Event,
    python: Path,
    exhaustive_verifier: Path,
    bitset_verifier: Path,
) -> dict[str, object]:
    started = time.monotonic()
    process = subprocess.Popen(
        (
            str(solver),
            "--graph",
            str(catalog),
            "--pairs",
            str(pairs_path),
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
        raise RuntimeError("worker pipes were not created")
    records: list[dict[str, object]] = []
    run_record: dict[str, object] | None = None
    terminated_early = False
    for raw in process.stdout:
        if not raw.strip():
            continue
        value = json.loads(raw)
        if value.get("record_type") == "RUN":
            run_record = value
            continue
        if value.get("record_type") != "PAIR":
            raise RuntimeError(f"worker {worker} emitted unknown record")
        selected = (
            int(value["catalog_line"]),
            int(value["deleted_left"]),
            int(value["deleted_right"]),
        )
        if selected != expected_pairs[len(records)]:
            raise RuntimeError(
                f"worker {worker} emitted wrong pair {selected}"
            )
        record = classify(
            value,
            catalog=catalog,
            catalog_sha256=catalog_sha256,
            output_dir=output_dir,
            python=python,
            exhaustive_verifier=exhaustive_verifier,
            bitset_verifier=bitset_verifier,
        )
        record["worker"] = worker
        records.append(record)
        if record["classification"] in (VERIFIED_SAT, FAILED_SAT):
            stop_event.set()
        if (
            stop_event.is_set()
            and record["classification"]
            not in (VERIFIED_SAT, FAILED_SAT)
        ) or time.monotonic() >= deadline:
            process.terminate()
            terminated_early = True
            break
    stderr = process.stderr.read()
    returncode = process.wait()
    expected_returncode = (
        {
            "COMPLETE": 0,
            "COMPLETE_WITH_LIMITS": 2,
            "SAT_STOP": 10,
        }.get(str(run_record.get("status")))
        if run_record is not None
        else None
    )
    if not terminated_early and (
        expected_returncode is None
        or returncode != expected_returncode
        or (
            run_record.get("status") in ("COMPLETE", "COMPLETE_WITH_LIMITS")
            and len(records) != len(expected_pairs)
        )
    ):
        raise RuntimeError(
            f"worker {worker} status/return mismatch: "
            f"returncode={returncode}, run_record={run_record!r}, "
            f"records={len(records)}, expected={len(expected_pairs)}, "
            f"stderr={stderr!r}"
        )
    return {
        "worker": worker,
        "pairs": str(pairs_path.resolve()),
        "pairs_sha256": sha256_file(pairs_path),
        "expected_pair_count": len(expected_pairs),
        "actual_pair_count": len(records),
        "returncode": returncode,
        "terminated_early": terminated_early,
        "stderr": stderr,
        "runtime_seconds": time.monotonic() - started,
        "run_record": run_record,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--solver", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--pairs", required=True, type=Path, nargs="+")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--seconds-limit-per-instance", required=True, type=float)
    parser.add_argument("--node-limit-per-instance", required=True, type=int)
    parser.add_argument("--jobs", required=True, type=int)
    parser.add_argument("--output-byte-cap", required=True, type=int)
    parser.add_argument("--free-disk-reserve-bytes", required=True, type=int)
    parser.add_argument("--max-wall-seconds", required=True, type=float)
    parser.add_argument("--python", type=Path, default=Path(sys.executable))
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
    if args.jobs != len(args.pairs) or args.jobs <= 0:
        raise SystemExit("--jobs must equal the number of pair shards")
    for required in (
        args.catalog,
        args.solver,
        args.plan,
        args.python,
        args.exhaustive_verifier,
        args.bitset_verifier,
        *args.pairs,
    ):
        if not required.is_file():
            raise SystemExit(f"required file is absent: {required}")
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise SystemExit("output directory must be absent or empty")
    free_before = shutil.disk_usage(args.output_dir.parent).free
    required_free = (
        args.free_disk_reserve_bytes + args.output_byte_cap
    )
    if free_before < required_free:
        raise SystemExit(
            f"disk preflight failed: free={free_before}, "
            f"required={required_free}"
        )

    catalog_sha256 = sha256_file(args.catalog)
    solver_sha256 = sha256_file(args.solver)
    runner_sha256 = sha256_file(Path(__file__))
    validate_plan(
        args.plan,
        catalog_sha256=catalog_sha256,
        solver_sha256=solver_sha256,
        runner_sha256=runner_sha256,
        pair_files=args.pairs,
        jobs=args.jobs,
        seconds_limit=args.seconds_limit_per_instance,
        node_limit=args.node_limit_per_instance,
        output_byte_cap=args.output_byte_cap,
        reserve_bytes=args.free_disk_reserve_bytes,
        max_wall_seconds=args.max_wall_seconds,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    deadline = started + args.max_wall_seconds
    stop_event = threading.Event()
    shard_pairs = [parse_pairs(path) for path in args.pairs]
    workers: list[dict[str, object]] = []
    worker_errors: list[dict[str, object]] = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.jobs
    ) as executor:
        futures = {
            executor.submit(
                run_worker,
                worker=worker,
                pairs_path=path.resolve(),
                expected_pairs=shard_pairs[worker],
                catalog=args.catalog.resolve(),
                catalog_sha256=catalog_sha256,
                solver=args.solver.resolve(),
                output_dir=args.output_dir.resolve(),
                seconds_limit=args.seconds_limit_per_instance,
                node_limit=args.node_limit_per_instance,
                deadline=deadline,
                stop_event=stop_event,
                python=args.python.resolve(),
                exhaustive_verifier=args.exhaustive_verifier.resolve(),
                bitset_verifier=args.bitset_verifier.resolve(),
            ): worker
            for worker, path in enumerate(args.pairs)
        }
        for future in concurrent.futures.as_completed(futures):
            worker = futures[future]
            try:
                workers.append(future.result())
            except Exception as error:
                stop_event.set()
                worker_errors.append(
                    {"worker": worker, "error": repr(error)}
                )
    workers.sort(key=lambda item: int(item["worker"]))
    records = [
        record
        for worker in workers
        for record in worker["records"]
    ]
    counts = {
        classification: sum(
            record["classification"] == classification
            for record in records
        )
        for classification in (
            OBSERVED_UNSAT,
            VERIFIED_SAT,
            FAILED_SAT,
            LIMIT,
            ERROR,
        )
    }
    expected_pairs = [
        selected for shard in shard_pairs for selected in shard
    ]
    actual_pairs = [
        (
            int(record["catalog_line"]),
            int(record["deleted_left"]),
            int(record["deleted_right"]),
        )
        for record in records
    ]
    exact_coverage = actual_pairs == expected_pairs
    summary = {
        "pilot": PILOT_ID,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": (
            "SAT_FOUND"
            if counts[VERIFIED_SAT]
            else "SAT_VERIFICATION_FAILED"
            if counts[FAILED_SAT]
            else "PILOT_COMPLETE"
            if exact_coverage and not worker_errors
            else "PILOT_INCOMPLETE"
        ),
        "scope": (
            "selected fixed induced 40-vertex catalog cores only; negative "
            "statuses are unchecked observations and are not global"
        ),
        "catalog": str(args.catalog.resolve()),
        "catalog_sha256": catalog_sha256,
        "expected_pair_count": len(expected_pairs),
        "actual_pair_count": len(actual_pairs),
        "exact_coverage": exact_coverage,
        "counts": counts,
        "negative_certified_count": 0,
        "proof_generation": False,
        "proof_replay": False,
        "jobs": args.jobs,
        "seconds_limit_per_instance": args.seconds_limit_per_instance,
        "node_limit_per_instance": args.node_limit_per_instance,
        "max_wall_seconds": args.max_wall_seconds,
        "output_byte_cap": args.output_byte_cap,
        "free_disk_reserve_bytes": args.free_disk_reserve_bytes,
        "free_disk_before_bytes": free_before,
        "solver": str(args.solver.resolve()),
        "solver_sha256": solver_sha256,
        "runner_source_sha256": runner_sha256,
        "plan": str(args.plan.resolve()),
        "plan_sha256": sha256_file(args.plan),
        "worker_errors": worker_errors,
        "workers": [
            {key: value for key, value in worker.items() if key != "records"}
            for worker in workers
        ],
        "records": records,
        "runtime_seconds": time.monotonic() - started,
    }
    raw = (
        json.dumps(summary, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
    existing_bytes = sum(
        path.stat().st_size
        for path in args.output_dir.rglob("*")
        if path.is_file()
    )
    if existing_bytes + len(raw) > args.output_byte_cap:
        raise SystemExit("output byte cap would be exceeded")
    summary_path = args.output_dir / "summary.json"
    atomic_write(summary_path, raw)
    free_after = shutil.disk_usage(args.output_dir).free
    if free_after < args.free_disk_reserve_bytes:
        raise SystemExit("free disk reserve breached")
    print(
        json.dumps(
            {
                "status": summary["status"],
                "expected_pair_count": summary["expected_pair_count"],
                "actual_pair_count": summary["actual_pair_count"],
                "exact_coverage": summary["exact_coverage"],
                "counts": counts,
                "runtime_seconds": summary["runtime_seconds"],
                "summary": str(summary_path),
                "summary_sha256": sha256_file(summary_path),
                "output_bytes": existing_bytes + len(raw),
                "free_disk_after_bytes": free_after,
            },
            sort_keys=True,
        )
    )
    if counts[FAILED_SAT] or worker_errors:
        return 1
    if counts[VERIFIED_SAT]:
        return 10
    if counts[LIMIT]:
        return 2
    return 0 if exact_coverage else 1


if __name__ == "__main__":
    raise SystemExit(main())
