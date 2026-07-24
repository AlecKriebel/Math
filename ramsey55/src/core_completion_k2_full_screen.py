#!/usr/bin/env python3
"""Resume-safe, storage-capped full delete-two/add-three catalog screen."""

from __future__ import annotations

import argparse
import concurrent.futures
import fcntl
import json
import os
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
from core_completion_k2_compact import (  # noqa: E402
    HEADER_BYTES,
    PAIRS_PER_LINE,
    RECORD_BYTES,
    validate_file,
)
from core_completion_sat import count_forbidden_sets  # noqa: E402
from graph_io import (  # noqa: E402
    encode_graph6,
    read_graph,
    write_canonical_artifact,
)


RUN_ID = "ramsey55_core_completion_catalog_k2_full_screen_v1"
OBSERVED_UNSAT = "OBSERVED_UNSAT_UNCHECKED"
LIMIT = "LIMIT_NO_CONCLUSION"
VERIFIED_SAT = "DUAL_VERIFIED_SAT_CONSTRUCTION"
FAILED_SAT = "SAT_MODEL_VERIFICATION_FAILED"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def output_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def shard_filename(shard: dict[str, object]) -> str:
    return (
        f"shard_{int(shard['shard']):02d}_lines_"
        f"{int(shard['line_start']):03d}_{int(shard['line_end']):03d}"
        ".k2scrn"
    )


def expected_shard_bytes(shard: dict[str, object]) -> int:
    lines = int(shard["line_end"]) - int(shard["line_start"]) + 1
    return HEADER_BYTES + lines * PAIRS_PER_LINE * RECORD_BYTES


def parse_shards(plan: dict[str, object]) -> list[dict[str, object]]:
    raw_shards = plan.get("shards")
    if not isinstance(raw_shards, list):
        raise ValueError("plan has no shard list")
    shards: list[dict[str, object]] = []
    expected_start = 1
    for expected_id, raw in enumerate(raw_shards):
        if not isinstance(raw, dict):
            raise ValueError("non-object shard plan")
        shard = dict(raw)
        start = int(shard.get("line_start", 0))
        end = int(shard.get("line_end", 0))
        shard_id = int(shard.get("shard", -1))
        pair_count = int(shard.get("pair_count", -1))
        record_bytes = int(shard.get("record_bytes", -1))
        if shard_id != expected_id or start != expected_start or end < start:
            raise ValueError("shards are not contiguous and ordered")
        expected_pairs = (end - start + 1) * PAIRS_PER_LINE
        if pair_count != expected_pairs:
            raise ValueError("shard pair count mismatch")
        if record_bytes != expected_shard_bytes(shard):
            raise ValueError("shard byte count mismatch")
        expected_start = end + 1
        shards.append(shard)
    if expected_start != 329:
        raise ValueError("shards do not exactly cover catalog lines 1..328")
    return shards


def validate_plan(
    plan_path: Path,
    *,
    catalog: Path,
    solver: Path,
    runner: Path,
    parser_source: Path,
    python: Path,
    exhaustive_verifier: Path,
    bitset_verifier: Path,
    output_dir: Path,
    jobs: int,
    seconds_limit: float,
    node_limit: int,
    max_wall_seconds: float,
    output_byte_cap: int,
    reserve_bytes: int,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    required = {
        "catalog_sha256": sha256_file(catalog),
        "catalog_dual_verification_sha256": sha256_file(
            ROOT
            / "results"
            / "verification"
            / "r55_42some_catalog_dual_check.json"
        ),
        "producer_source_sha256": sha256_file(
            ROOT / "src" / "core_completion_k2_compact_screen_solver.cpp"
        ),
        "included_solver_source_sha256": sha256_file(
            ROOT / "src" / "core_completion_k2_persistent_solver.cpp"
        ),
        "producer_binary_sha256": sha256_file(solver),
        "runner_source_sha256": sha256_file(runner),
        "independent_parser_sha256": sha256_file(parser_source),
        "coverage_checker_sha256": sha256_file(
            ROOT / "verify" / "core_completion_k2_full_screen_coverage.py"
        ),
        "python_executable_sha256": sha256_file(python),
        "exhaustive_sat_verifier_sha256": sha256_file(exhaustive_verifier),
        "bitset_sat_verifier_sha256": sha256_file(bitset_verifier),
        "jobs": jobs,
        "seconds_limit_per_instance": seconds_limit,
        "node_limit_per_instance": node_limit,
        "max_wall_seconds": max_wall_seconds,
        "output_byte_cap": output_byte_cap,
        "free_disk_reserve_bytes": reserve_bytes,
        "output_directory": relative(output_dir),
    }
    mismatches = {
        key: {"plan": plan.get(key), "actual": value}
        for key, value in required.items()
        if plan.get(key) != value
    }
    if mismatches:
        raise ValueError(f"immutable full-screen plan mismatch: {mismatches}")
    shards = parse_shards(plan)
    expected_pairs = sum(int(shard["pair_count"]) for shard in shards)
    expected_bytes = sum(int(shard["record_bytes"]) for shard in shards)
    if expected_pairs != 282_408:
        raise ValueError("plan does not contain exactly 282,408 cores")
    if expected_bytes != int(plan.get("expected_binary_bytes", -1)):
        raise ValueError("plan binary-byte projection mismatch")
    if int(plan.get("worst_case_retained_output_bytes", output_byte_cap + 1)) > (
        output_byte_cap
    ):
        raise ValueError("plan worst-case retained output exceeds hard cap")
    return plan, shards


class RunControl:
    def __init__(
        self,
        *,
        output_dir: Path,
        deadline: float,
        output_byte_cap: int,
        reserve_bytes: int,
    ) -> None:
        self.output_dir = output_dir
        self.deadline = deadline
        self.output_byte_cap = output_byte_cap
        self.reserve_bytes = reserve_bytes
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.processes: dict[int, subprocess.Popen[str]] = {}
        self.reason: str | None = None
        self.stop_started: float | None = None
        self.sat_claimed = False

    def register(self, shard_id: int, process: subprocess.Popen[str]) -> None:
        with self.lock:
            self.processes[shard_id] = process
            stopped = self.stop_event.is_set()
        if stopped and process.poll() is None:
            process.terminate()

    def unregister(self, shard_id: int) -> None:
        with self.lock:
            self.processes.pop(shard_id, None)

    def claim_sat(self) -> bool:
        with self.lock:
            if self.sat_claimed:
                return False
            self.sat_claimed = True
            return True

    def request_stop(
        self, reason: str, *, exclude: subprocess.Popen[str] | None = None
    ) -> None:
        with self.lock:
            if self.reason is None:
                self.reason = reason
                self.stop_started = time.monotonic()
            self.stop_event.set()
            processes = list(self.processes.values())
        for process in processes:
            if process is exclude or process.poll() is not None:
                continue
            try:
                process.terminate()
            except ProcessLookupError:
                pass

    def watchdog(self) -> None:
        while True:
            with self.lock:
                processes = list(self.processes.values())
                stop_started = self.stop_started
            if not processes and self.stop_event.is_set():
                return
            if time.monotonic() >= self.deadline:
                self.request_stop("MAX_WALL_SECONDS_EXCEEDED")
            elif output_bytes(self.output_dir) > self.output_byte_cap:
                self.request_stop("OUTPUT_BYTE_CAP_EXCEEDED")
            elif shutil.disk_usage(self.output_dir).free < self.reserve_bytes:
                self.request_stop("FREE_DISK_RESERVE_BREACHED")
            if (
                self.stop_event.is_set()
                and stop_started is not None
                and time.monotonic() - stop_started >= 3.0
            ):
                for process in processes:
                    if process.poll() is None:
                        try:
                            process.kill()
                        except ProcessLookupError:
                            pass
            if not processes and not self.stop_event.is_set():
                time.sleep(0.25)
            else:
                time.sleep(1.0)


def archive_stale(path: Path, output_dir: Path, label: str) -> Path:
    diagnostics = output_dir / "diagnostics"
    diagnostics.mkdir(parents=True, exist_ok=True)
    destination = diagnostics / (
        f"{path.name}.{label}.{time.time_ns()}.preserved"
    )
    os.replace(path, destination)
    return destination


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
    if (
        len(true_variables) != len(set(true_variables))
        or any(value < 0 or value >= 123 for value in true_variables)
    ):
        raise ValueError("SAT result has invalid true-variable indices")

    stem = f"line_{line:03d}_delete_{left:02d}_{right:02d}"
    candidate_dir = output_dir / "sat_candidates" / stem
    model = candidate_dir / f"{stem}.model.json"
    atomic_json(
        model,
        {
            "run": RUN_ID,
            "preserved_utc": utc_now(),
            "catalog_sha256": catalog_sha256,
            "catalog_line": line,
            "deleted_left": left,
            "deleted_right": right,
            "variable_numbering": "zero-based, as emitted by C++ solver",
            "true_variables": true_variables,
            "raw_solver_result": solver_result,
        },
    )

    base = read_graph(catalog, line)
    core, retained = induced_core_two(base, left, right)
    true_set = set(true_variables)
    completed = completed_adjacency_k2(
        core, [variable in true_set for variable in range(123)]
    )
    internal_counts = count_forbidden_sets(completed, 5)
    graph6 = candidate_dir / f"{stem}.candidate.g6"
    canonical = candidate_dir / f"{stem}.candidate.canonical.json"
    atomic_write(graph6, (encode_graph6(completed) + "\n").encode("ascii"))
    canonical_sha256 = write_canonical_artifact(
        completed,
        canonical,
        provenance={
            "source": RUN_ID,
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
        exhaustive.stdout, "exhaustive SAT verifier"
    )
    bitset_result = parse_last_json(bitset.stdout, "bitset SAT verifier")
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
        "model_path": relative(model),
        "model_sha256": sha256_file(model),
        "candidate_graph6_path": relative(graph6),
        "candidate_graph6_sha256": sha256_file(graph6),
        "candidate_canonical_path": relative(canonical),
        "candidate_canonical_sha256": canonical_sha256,
        "verification_path": relative(verification),
        "verification_sha256": sha256_file(verification),
    }


def result_matches(
    result: dict[str, object],
    *,
    plan_sha256: str,
    records_sha256: str,
    audit: dict[str, int | str],
) -> bool:
    return (
        result.get("status") == "COMPLETE"
        and result.get("plan_sha256") == plan_sha256
        and result.get("records_sha256") == records_sha256
        and result.get("record_count") == audit["record_count"]
        and result.get("unsat_count") == audit["unsat_count"]
        and result.get("limit_count") == audit["limit_count"]
        and result.get("record_bytes") == audit["record_bytes"]
    )


def finalize_shard_result(
    *,
    shard: dict[str, object],
    records: Path,
    result_path: Path,
    plan_sha256: str,
    audit: dict[str, int | str],
    producer_result: dict[str, object] | None,
    runtime_seconds: float,
    reused: bool,
    output_dir: Path,
) -> dict[str, object]:
    records_sha256 = str(audit["sha256"])
    if result_path.exists():
        try:
            old = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            old = {}
        if result_matches(
            old,
            plan_sha256=plan_sha256,
            records_sha256=records_sha256,
            audit=audit,
        ):
            return old
        archive_stale(result_path, output_dir, "invalid-result")
    result = {
        "schema": "ramsey55.core_completion_catalog_k2_shard_result.v1",
        "completed_utc": utc_now(),
        "status": "COMPLETE",
        "shard": int(shard["shard"]),
        "line_start": int(shard["line_start"]),
        "line_end": int(shard["line_end"]),
        "record_count": int(audit["record_count"]),
        "unsat_count": int(audit["unsat_count"]),
        "limit_count": int(audit["limit_count"]),
        "total_nodes": int(audit["total_nodes"]),
        "max_nodes": int(audit["max_nodes"]),
        "max_elapsed_microseconds": int(
            audit["max_elapsed_microseconds"]
        ),
        "record_bytes": int(audit["record_bytes"]),
        "records": relative(records),
        "records_sha256": records_sha256,
        "plan_sha256": plan_sha256,
        "runtime_seconds": runtime_seconds,
        "reused_validated_shard": reused,
        "producer_result": producer_result,
        "negative_certified_count": 0,
        "proof_generated": False,
        "proof_checked": False,
    }
    atomic_json(result_path, result)
    return result


def run_shard(
    *,
    shard: dict[str, object],
    catalog: Path,
    catalog_sha256: str,
    solver: Path,
    output_dir: Path,
    plan_sha256: str,
    seconds_limit: float,
    node_limit: int,
    control: RunControl,
    python: Path,
    exhaustive_verifier: Path,
    bitset_verifier: Path,
) -> dict[str, object]:
    shard_id = int(shard["shard"])
    start = int(shard["line_start"])
    end = int(shard["line_end"])
    records = output_dir / "shards" / shard_filename(shard)
    result_path = output_dir / "shards" / (
        Path(shard_filename(shard)).stem + ".result.json"
    )
    records.parent.mkdir(parents=True, exist_ok=True)

    partial = Path(f"{records}.partial")
    if partial.exists():
        archived = archive_stale(partial, output_dir, "incomplete-partial")
        print(
            json.dumps(
                {
                    "record_type": "RESUME_DIAGNOSTIC",
                    "shard": shard_id,
                    "preserved_partial": relative(archived),
                },
                sort_keys=True,
            ),
            flush=True,
        )

    if records.exists():
        try:
            audit = validate_file(
                records,
                expected_range=(start, end),
                expected_catalog_sha256=catalog_sha256,
                node_limit=node_limit,
            )
        except Exception:
            archived = archive_stale(records, output_dir, "invalid-shard")
            if result_path.exists():
                archive_stale(result_path, output_dir, "orphaned-result")
            print(
                json.dumps(
                    {
                        "record_type": "RESUME_DIAGNOSTIC",
                        "shard": shard_id,
                        "preserved_invalid_shard": relative(archived),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        else:
            result = finalize_shard_result(
                shard=shard,
                records=records,
                result_path=result_path,
                plan_sha256=plan_sha256,
                audit=audit,
                producer_result=None,
                runtime_seconds=0.0,
                reused=True,
                output_dir=output_dir,
            )
            print(
                json.dumps(
                    {
                        "record_type": "SHARD_BOUNDARY",
                        "status": "REUSED_VALIDATED",
                        "shard": shard_id,
                        "line_start": start,
                        "line_end": end,
                        "record_count": audit["record_count"],
                        "unsat_count": audit["unsat_count"],
                        "limit_count": audit["limit_count"],
                        "record_bytes": audit["record_bytes"],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            return {"kind": "COMPLETE", "result": result}

    if control.stop_event.is_set():
        return {"kind": "STOPPED", "shard": shard_id}
    started = time.monotonic()
    process = subprocess.Popen(
        (
            str(solver),
            "--graph",
            str(catalog),
            "--records",
            str(records),
            "--line-start",
            str(start),
            "--line-end",
            str(end),
            "--catalog-sha256",
            catalog_sha256,
            "--node-limit",
            str(node_limit),
            "--seconds-limit",
            str(seconds_limit),
            "--record-byte-cap",
            str(int(shard["record_bytes"])),
        ),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
    )
    control.register(shard_id, process)
    if process.stdout is None or process.stderr is None:
        control.request_stop(f"SHARD_{shard_id}_PIPE_CREATION_FAILED")
        raise RuntimeError("worker pipes were not created")
    producer_result: dict[str, object] | None = None
    sat_result: dict[str, object] | None = None
    try:
        for raw in process.stdout:
            if not raw.strip():
                continue
            value = json.loads(raw)
            record_type = value.get("record_type")
            if record_type == "LINE":
                print(
                    json.dumps(
                        {
                            "record_type": "LINE_PROGRESS",
                            "shard": shard_id,
                            "catalog_line": value.get("catalog_line"),
                            "completed_records": value.get(
                                "completed_records"
                            ),
                            "unsat_count": value.get("unsat_count"),
                            "limit_count": value.get("limit_count"),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
            elif record_type == "SAT":
                if not control.claim_sat():
                    control.request_stop("MULTIPLE_SAT_RESULTS")
                    continue
                control.request_stop("SAT_FOUND", exclude=process)
                sat_result = {
                    "solver_result": value,
                    **preserve_and_verify_sat(
                        catalog=catalog,
                        catalog_sha256=catalog_sha256,
                        solver_result=value,
                        output_dir=output_dir,
                        python=python,
                        exhaustive_verifier=exhaustive_verifier,
                        bitset_verifier=bitset_verifier,
                    ),
                }
                print(
                    json.dumps(
                        {
                            "record_type": "SAT_PRESERVED",
                            "shard": shard_id,
                            "catalog_line": value.get("catalog_line"),
                            "deleted_left": value.get("deleted_left"),
                            "deleted_right": value.get("deleted_right"),
                            "classification": sat_result["classification"],
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
            elif record_type == "SHARD":
                producer_result = value
            else:
                raise RuntimeError(
                    f"shard {shard_id} emitted unknown record {record_type!r}"
                )
        returncode = process.wait()
        stderr = process.stderr.read()
    except Exception:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3.0)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        raise
    finally:
        process.stdout.close()
        process.stderr.close()
        control.unregister(shard_id)

    runtime = time.monotonic() - started
    if sat_result is not None:
        return {
            "kind": "SAT",
            "shard": shard_id,
            "runtime_seconds": runtime,
            "returncode": returncode,
            "stderr": stderr,
            "sat": sat_result,
            "producer_result": producer_result,
        }
    if control.stop_event.is_set():
        return {
            "kind": "STOPPED",
            "shard": shard_id,
            "runtime_seconds": runtime,
            "returncode": returncode,
            "stderr": stderr,
        }
    if returncode not in (0, 2):
        raise RuntimeError(
            f"shard {shard_id} failed with return code {returncode}:"
            f" {stderr.strip()}"
        )
    if (
        not isinstance(producer_result, dict)
        or producer_result.get("status") != "COMPLETE"
    ):
        raise RuntimeError(f"shard {shard_id} has no COMPLETE producer record")
    audit = validate_file(
        records,
        expected_range=(start, end),
        expected_catalog_sha256=catalog_sha256,
        node_limit=node_limit,
    )
    if (
        int(producer_result.get("record_count", -1))
        != audit["record_count"]
        or int(producer_result.get("unsat_count", -1))
        != audit["unsat_count"]
        or int(producer_result.get("limit_count", -1))
        != audit["limit_count"]
        or int(producer_result.get("record_bytes", -1))
        != audit["record_bytes"]
    ):
        raise RuntimeError(f"shard {shard_id} producer/parser mismatch")
    result = finalize_shard_result(
        shard=shard,
        records=records,
        result_path=result_path,
        plan_sha256=plan_sha256,
        audit=audit,
        producer_result=producer_result,
        runtime_seconds=runtime,
        reused=False,
        output_dir=output_dir,
    )
    print(
        json.dumps(
            {
                "record_type": "SHARD_BOUNDARY",
                "status": "COMPLETE",
                "shard": shard_id,
                "line_start": start,
                "line_end": end,
                "record_count": audit["record_count"],
                "unsat_count": audit["unsat_count"],
                "limit_count": audit["limit_count"],
                "record_bytes": audit["record_bytes"],
                "runtime_seconds": runtime,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return {"kind": "COMPLETE", "result": result}


def write_stop_record(
    output_dir: Path,
    *,
    plan_sha256: str,
    reason: str,
    started_utc: str,
    runtime_seconds: float,
    outcomes: list[dict[str, object]],
    sat_result: dict[str, object] | None,
    output_byte_cap: int,
    reserve_bytes: int,
) -> Path:
    path = output_dir / f"STOP_{time.time_ns()}.json"
    atomic_json(
        path,
        {
            "schema": "ramsey55.core_completion_catalog_k2_stop.v1",
            "created_utc": utc_now(),
            "status": "INCOMPLETE_STOPPED",
            "reason": reason,
            "started_utc": started_utc,
            "runtime_seconds": runtime_seconds,
            "plan_sha256": plan_sha256,
            "outcomes": outcomes,
            "sat_result": sat_result,
            "output_bytes": output_bytes(output_dir),
            "output_byte_cap": output_byte_cap,
            "free_disk_bytes": shutil.disk_usage(output_dir).free,
            "free_disk_reserve_bytes": reserve_bytes,
            "negative_certified_count": 0,
            "proof_generation": False,
            "proof_replay": False,
        },
    )
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--solver", required=True, type=Path)
    parser.add_argument("--parser-source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--jobs", required=True, type=int)
    parser.add_argument("--seconds-limit", required=True, type=float)
    parser.add_argument("--node-limit", required=True, type=int)
    parser.add_argument("--max-wall-seconds", required=True, type=float)
    parser.add_argument("--output-byte-cap", required=True, type=int)
    parser.add_argument("--reserve-bytes", required=True, type=int)
    parser.add_argument("--python", type=Path, default=Path(sys.executable))
    parser.add_argument("--exhaustive-verifier", required=True, type=Path)
    parser.add_argument("--bitset-verifier", required=True, type=Path)
    args = parser.parse_args()

    runner = Path(__file__)
    plan, shards = validate_plan(
        args.plan,
        catalog=args.catalog,
        solver=args.solver,
        runner=runner,
        parser_source=args.parser_source,
        python=args.python,
        exhaustive_verifier=args.exhaustive_verifier,
        bitset_verifier=args.bitset_verifier,
        output_dir=args.output,
        jobs=args.jobs,
        seconds_limit=args.seconds_limit,
        node_limit=args.node_limit,
        max_wall_seconds=args.max_wall_seconds,
        output_byte_cap=args.output_byte_cap,
        reserve_bytes=args.reserve_bytes,
    )
    plan_sha256 = sha256_file(args.plan)
    catalog_sha256 = sha256_file(args.catalog)
    output_existed = args.output.exists()
    if not output_existed:
        args.output.mkdir(parents=True)
    lock_path = args.output / ".run.lock"
    with lock_path.open("a+", encoding="utf-8") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise SystemExit("another full-screen runner holds the run lock") from error

        identity_path = args.output / "run_identity.json"
        identity = {
            "run": RUN_ID,
            "plan": relative(args.plan),
            "plan_sha256": plan_sha256,
            "catalog_sha256": catalog_sha256,
            "producer_binary_sha256": sha256_file(args.solver),
            "runner_source_sha256": sha256_file(runner),
            "independent_parser_sha256": sha256_file(args.parser_source),
        }
        if identity_path.exists():
            existing_identity = json.loads(
                identity_path.read_text(encoding="utf-8")
            )
            if existing_identity != identity:
                raise SystemExit("existing output has a different run identity")
        else:
            if output_existed and any(args.output.iterdir()):
                non_lock = [item for item in args.output.iterdir() if item != lock_path]
                if non_lock:
                    raise SystemExit("nonempty output has no matching run identity")
            atomic_json(identity_path, identity)

        existing_bytes = output_bytes(args.output)
        completed_ids: set[int] = set()
        for shard in shards:
            records = args.output / "shards" / shard_filename(shard)
            if not records.exists():
                continue
            try:
                validate_file(
                    records,
                    expected_range=(
                        int(shard["line_start"]),
                        int(shard["line_end"]),
                    ),
                    expected_catalog_sha256=catalog_sha256,
                    node_limit=args.node_limit,
                )
            except Exception:
                continue
            completed_ids.add(int(shard["shard"]))
        remaining_binary_bytes = sum(
            int(shard["record_bytes"])
            for shard in shards
            if int(shard["shard"]) not in completed_ids
        )
        metadata_allowance = int(plan["ordinary_metadata_allowance_bytes"])
        projected_bytes = (
            existing_bytes + remaining_binary_bytes + metadata_allowance
        )
        free_before = shutil.disk_usage(args.output).free
        required_free = args.reserve_bytes + max(
            0, args.output_byte_cap - existing_bytes
        )
        if projected_bytes > args.output_byte_cap:
            raise SystemExit(
                f"projected retained output {projected_bytes} exceeds cap"
            )
        if free_before < required_free:
            raise SystemExit(
                f"disk preflight failed: free {free_before} < {required_free}"
            )

        started_utc = utc_now()
        started = time.monotonic()
        control = RunControl(
            output_dir=args.output,
            deadline=started + args.max_wall_seconds,
            output_byte_cap=args.output_byte_cap,
            reserve_bytes=args.reserve_bytes,
        )
        watcher = threading.Thread(target=control.watchdog, daemon=True)
        watcher.start()
        outcomes: list[dict[str, object]] = []
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=args.jobs
        ) as executor:
            future_to_shard = {
                executor.submit(
                    run_shard,
                    shard=shard,
                    catalog=args.catalog,
                    catalog_sha256=catalog_sha256,
                    solver=args.solver,
                    output_dir=args.output,
                    plan_sha256=plan_sha256,
                    seconds_limit=args.seconds_limit,
                    node_limit=args.node_limit,
                    control=control,
                    python=args.python,
                    exhaustive_verifier=args.exhaustive_verifier,
                    bitset_verifier=args.bitset_verifier,
                ): shard
                for shard in shards
            }
            for future in concurrent.futures.as_completed(future_to_shard):
                shard = future_to_shard[future]
                try:
                    outcome = future.result()
                except Exception as error:
                    outcome = {
                        "kind": "ERROR",
                        "shard": int(shard["shard"]),
                        "error": f"{type(error).__name__}: {error}",
                    }
                    control.request_stop(
                        f"SHARD_{int(shard['shard'])}_ERROR"
                    )
                outcomes.append(outcome)
        if not control.stop_event.is_set():
            control.stop_event.set()
        watcher.join(timeout=5.0)
        runtime = time.monotonic() - started

        sat_outcomes = [
            outcome for outcome in outcomes if outcome.get("kind") == "SAT"
        ]
        if sat_outcomes or any(
            outcome.get("kind") != "COMPLETE" for outcome in outcomes
        ):
            reason = control.reason or "INCOMPLETE_SHARD_OUTCOME"
            sat_result = (
                sat_outcomes[0].get("sat") if sat_outcomes else None
            )
            stop_path = write_stop_record(
                args.output,
                plan_sha256=plan_sha256,
                reason=reason,
                started_utc=started_utc,
                runtime_seconds=runtime,
                outcomes=outcomes,
                sat_result=(
                    sat_result if isinstance(sat_result, dict) else None
                ),
                output_byte_cap=args.output_byte_cap,
                reserve_bytes=args.reserve_bytes,
            )
            print(
                json.dumps(
                    {
                        "record_type": "RUN",
                        "status": "INCOMPLETE_STOPPED",
                        "reason": reason,
                        "stop_record": relative(stop_path),
                    },
                    sort_keys=True,
                )
            )
            return 10 if sat_outcomes else 1

        results = sorted(
            (
                outcome["result"]
                for outcome in outcomes
                if isinstance(outcome.get("result"), dict)
            ),
            key=lambda result: int(result["shard"]),
        )
        total_records = sum(int(result["record_count"]) for result in results)
        unsat_count = sum(int(result["unsat_count"]) for result in results)
        limit_count = sum(int(result["limit_count"]) for result in results)
        total_record_bytes = sum(
            int(result["record_bytes"]) for result in results
        )
        summary = {
            "schema": "ramsey55.core_completion_catalog_k2_full_screen_result.v1",
            "run": RUN_ID,
            "completed_utc": utc_now(),
            "status": "COMPLETE",
            "evidence_category": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
            "plan": relative(args.plan),
            "plan_sha256": plan_sha256,
            "catalog": relative(args.catalog),
            "catalog_sha256": catalog_sha256,
            "producer_binary_sha256": sha256_file(args.solver),
            "runner_source_sha256": sha256_file(runner),
            "independent_parser_sha256": sha256_file(args.parser_source),
            "started_utc": started_utc,
            "runtime_seconds": runtime,
            "jobs": args.jobs,
            "seconds_limit_per_instance": args.seconds_limit,
            "node_limit_per_instance": args.node_limit,
            "max_wall_seconds": args.max_wall_seconds,
            "free_disk_before_bytes": free_before,
            "existing_bytes_at_launch": existing_bytes,
            "required_free_at_launch_bytes": required_free,
            "free_disk_reserve_bytes": args.reserve_bytes,
            "output_byte_cap": args.output_byte_cap,
            "projected_bytes_at_launch": projected_bytes,
            "expected_pair_count": 282_408,
            "actual_pair_count": total_records,
            "exact_pair_coverage": total_records == 282_408,
            "expected_binary_bytes": int(plan["expected_binary_bytes"]),
            "actual_binary_bytes": total_record_bytes,
            "counts": {
                OBSERVED_UNSAT: unsat_count,
                LIMIT: limit_count,
                VERIFIED_SAT: 0,
                FAILED_SAT: 0,
                "ERROR": 0,
            },
            "negative_certified_count": 0,
            "proof_generation": False,
            "proof_replay": False,
            "shards": results,
            "scope_warning": (
                "All negative statuses concern fixed induced 40-vertex "
                "catalog cores and are unchecked observations, not negative "
                "certificates or a global Ramsey-bound result."
            ),
        }
        summary_path = args.output / "summary.json"
        if summary_path.exists():
            old_summary = json.loads(summary_path.read_text(encoding="utf-8"))
            if old_summary != summary:
                archive_stale(summary_path, args.output, "old-summary")
        atomic_json(summary_path, summary)
        if output_bytes(args.output) > args.output_byte_cap:
            raise SystemExit("output cap exceeded while writing summary")
        print(
            json.dumps(
                {
                    "record_type": "RUN",
                    "status": "COMPLETE",
                    "summary": relative(summary_path),
                    "record_count": total_records,
                    "unsat_count": unsat_count,
                    "limit_count": limit_count,
                    "record_bytes": total_record_bytes,
                    "runtime_seconds": runtime,
                },
                sort_keys=True,
            )
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
