#!/usr/bin/env python3
"""Hash-bound Cadical retry of exactly the v1 replacement-screen limits."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_catalog_batch import (  # noqa: E402
    atomic_json,
    parse_last_json,
    sha256_file,
)
from core_completion_k2 import build_k2_completion_instance  # noqa: E402
from e2_triple_replacement_compact import (  # noqa: E402
    STATUS_LIMIT,
    TRIPLES,
    iter_records,
)
from e2_triple_replacement_screen import preserve_sat  # noqa: E402
from graph_io import read_graph, validate_simple  # noqa: E402


RUN_ID = "ramsey55_e2_triple_replacement_limit_retry_v2"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def formula_sha256(clauses: tuple[tuple[int, ...], ...]) -> str:
    digest = hashlib.sha256()
    for clause in clauses:
        digest.update(" ".join(str(literal) for literal in clause).encode())
        digest.update(b" 0\n")
    return digest.hexdigest()


def induced_core_three(
    adjacency: list[int], deleted: tuple[int, int, int]
) -> list[int]:
    retained = tuple(vertex for vertex in range(43) if vertex not in deleted)
    if len(retained) != 40:
        raise ValueError("delete-three core does not have order 40")
    core = [0] * 40
    for new_left, old_left in enumerate(retained):
        for new_right in range(new_left + 1, 40):
            old_right = retained[new_right]
            if (adjacency[old_left] >> old_right) & 1:
                core[new_left] |= 1 << new_right
                core[new_right] |= 1 << new_left
    validate_simple(core)
    return core


def extract_limit_targets(
    base_plan: dict[str, object], shard_dir: Path
) -> list[dict[str, object]]:
    corpus_sha256 = str(base_plan["corpus_sha256"])
    targets: list[dict[str, object]] = []
    for shard in base_plan["shards"]:
        input_index = int(shard["input_index"])
        start = int(shard["triple_start"])
        end = int(shard["triple_end"])
        path = shard_dir / str(shard["filename"])
        shard_sha256 = sha256_file(path)
        for record in iter_records(
            path,
            expected_input_index=input_index,
            expected_range=(start, end),
            expected_corpus_sha256=corpus_sha256,
        ):
            if record.status == STATUS_LIMIT:
                targets.append(
                    {
                        "target": len(targets),
                        "input_index": input_index,
                        "triple_ordinal": record.triple_ordinal,
                        "deleted_vertices": list(record.deleted_vertices),
                        "base_shard": relative(path),
                        "base_shard_sha256": shard_sha256,
                        "base_nodes": record.nodes,
                        "base_elapsed_microseconds": (
                            record.elapsed_microseconds
                        ),
                    }
                )
    return targets


def immutable_files(
    *,
    base_plan_path: Path,
    base_coverage_path: Path,
    corpus: Path,
    python_executable: Path,
    pysat_root: Path,
    tests: Path,
    checker: Path,
    exhaustive: Path,
    bitset: Path,
) -> list[dict[str, str]]:
    paths = [
        Path(__file__).resolve(),
        checker,
        tests,
        base_plan_path,
        base_coverage_path,
        corpus,
        python_executable,
        pysat_root / "pysat" / "__init__.py",
        pysat_root / "pysat" / "solvers.py",
        pysat_root / "pysolvers.cpython-311-darwin.so",
        ROOT / "src" / "core_completion_k2.py",
        ROOT / "src" / "e2_triple_replacement_compact.py",
        ROOT / "src" / "e2_triple_replacement_screen.py",
        ROOT / "src" / "graph_io.py",
        exhaustive,
        bitset,
    ]
    return [
        {"path": str(path.resolve()), "sha256": sha256_file(path)}
        for path in paths
    ]


def make_plan(
    *,
    plan_path: Path,
    base_plan_path: Path,
    base_coverage_path: Path,
    base_shard_dir: Path,
    output_dir: Path,
    python_executable: Path,
    pysat_root: Path,
    checker: Path,
    tests: Path,
    exhaustive: Path,
    bitset: Path,
    conflict_budget: int,
    worker_timeout: float,
    output_byte_cap: int,
    reserve_bytes: int,
) -> dict[str, object]:
    if plan_path.exists():
        raise FileExistsError(f"refusing to overwrite frozen plan {plan_path}")
    base_plan = json.loads(base_plan_path.read_text(encoding="utf-8"))
    base_coverage = json.loads(
        base_coverage_path.read_text(encoding="utf-8")
    )
    if base_plan.get("schema") != "ramsey55.e2_triple_replacement_plan.v1":
        raise ValueError("unexpected base-plan schema")
    if (
        base_coverage.get("valid") is not True
        or base_coverage.get("plan_sha256") != sha256_file(base_plan_path)
    ):
        raise ValueError("base coverage is not valid for base plan")
    corpus = ROOT / str(base_plan["corpus"])
    targets = extract_limit_targets(base_plan, base_shard_dir)
    expected_limits = int(base_coverage["totals"]["limit_count"])
    if len(targets) != expected_limits or expected_limits == 0:
        raise ValueError("target list does not equal nonempty base limit set")
    if conflict_budget <= 0 or worker_timeout <= 0:
        raise ValueError("retry bounds must be positive")
    plan = {
        "schema": "ramsey55.e2_triple_replacement_limit_retry_plan.v2",
        "experiment": RUN_ID,
        "frozen_utc": utc_now(),
        "question": (
            "Do any of the exact v1 time-limit cores admit a SAT "
            "delete-three/add-three completion under Cadical195?"
        ),
        "base_plan": relative(base_plan_path),
        "base_plan_sha256": sha256_file(base_plan_path),
        "base_coverage": relative(base_coverage_path),
        "base_coverage_sha256": sha256_file(base_coverage_path),
        "base_shard_directory": relative(base_shard_dir),
        "corpus": relative(corpus),
        "corpus_sha256": sha256_file(corpus),
        "target_count": len(targets),
        "targets": targets,
        "solver": "PySAT Cadical195",
        "solver_version": "1.9.dev7",
        "python_executable": str(python_executable.resolve()),
        "pysat_root": str(pysat_root.resolve()),
        "conflict_budget_per_target": conflict_budget,
        "worker_timeout_seconds": worker_timeout,
        "output_directory": relative(output_dir),
        "output_byte_cap": output_byte_cap,
        "free_disk_reserve_bytes": reserve_bytes,
        "checker": relative(checker),
        "tests": relative(tests),
        "exhaustive_sat_verifier": relative(exhaustive),
        "bitset_sat_verifier": relative(bitset),
        "immutable_files": immutable_files(
            base_plan_path=base_plan_path,
            base_coverage_path=base_coverage_path,
            corpus=corpus,
            python_executable=python_executable,
            pysat_root=pysat_root,
            tests=tests,
            checker=checker,
            exhaustive=exhaustive,
            bitset=bitset,
        ),
        "sat_policy": (
            "Stop immediately and use the v1 dual-verification artifact "
            "pipeline for any SAT model."
        ),
        "negative_policy": (
            "Cadical UNSAT outputs remain proof-free observations. No proof "
            "artifact is requested or retained."
        ),
        "claim_boundary": (
            "This retries exactly the 117 bounded v1 limits for two fixed "
            "E=2 representatives; it is not global nonexistence evidence."
        ),
    }
    atomic_json(plan_path, plan)
    return plan


def validate_plan(plan_path: Path) -> dict[str, object]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if (
        plan.get("schema")
        != "ramsey55.e2_triple_replacement_limit_retry_plan.v2"
    ):
        raise ValueError("unexpected retry-plan schema")
    for record in plan.get("immutable_files", []):
        path = Path(str(record["path"]))
        if sha256_file(path) != record.get("sha256"):
            raise ValueError(f"immutable file changed: {path}")
    base_plan_path = ROOT / str(plan["base_plan"])
    base_coverage_path = ROOT / str(plan["base_coverage"])
    if sha256_file(base_plan_path) != plan.get("base_plan_sha256"):
        raise ValueError("base plan hash mismatch")
    if sha256_file(base_coverage_path) != plan.get("base_coverage_sha256"):
        raise ValueError("base coverage hash mismatch")
    base_plan = json.loads(base_plan_path.read_text(encoding="utf-8"))
    actual_targets = extract_limit_targets(
        base_plan, ROOT / str(plan["base_shard_directory"])
    )
    if actual_targets != plan.get("targets"):
        raise ValueError("frozen targets do not equal current base limits")
    if len(actual_targets) != int(plan["target_count"]):
        raise ValueError("retry target-count mismatch")
    return plan


def run_worker(plan_path: Path, target_index: int) -> int:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    targets = plan.get("targets")
    if not isinstance(targets, list) or not 0 <= target_index < len(targets):
        raise ValueError("worker target index is outside plan")
    target = targets[target_index]
    if int(target["target"]) != target_index:
        raise ValueError("worker target index mismatch")
    input_index = int(target["input_index"])
    ordinal = int(target["triple_ordinal"])
    deleted = tuple(int(value) for value in target["deleted_vertices"])
    if deleted != TRIPLES[ordinal]:
        raise ValueError("worker deletion triple/ordinal mismatch")
    corpus = ROOT / str(plan["corpus"])
    adjacency = read_graph(corpus, input_index)
    generation_started = time.monotonic()
    core = induced_core_three(adjacency, deleted)
    instance = build_k2_completion_instance(core)
    generation_seconds = time.monotonic() - generation_started
    digest = formula_sha256(instance.clauses)

    from pysat.solvers import Cadical195

    solver_started = time.monotonic()
    with Cadical195(bootstrap_with=instance.clauses) as solver:
        solver.conf_budget(int(plan["conflict_budget_per_target"]))
        answer = solver.solve_limited(expect_interrupt=True)
        statistics = solver.accum_stats()
        model = solver.get_model() if answer is True else None
    solver_seconds = time.monotonic() - solver_started
    status = "SAT" if answer is True else ("UNSAT" if answer is False else "LIMIT")
    result: dict[str, object] = {
        "schema": "ramsey55.e2_triple_replacement_limit_retry_worker.v2",
        "record_type": "TARGET",
        "status": status,
        "target": target_index,
        "input_index": input_index,
        "triple_ordinal": ordinal,
        "deleted_vertices": list(deleted),
        "variables": instance.variable_count,
        "clauses": len(instance.clauses),
        "formula_sha256": digest,
        "generation_seconds": generation_seconds,
        "solver_seconds": solver_seconds,
        "solver_statistics": statistics,
        "conflict_budget": int(plan["conflict_budget_per_target"]),
        "proof_generated": False,
        "proof_checked": False,
    }
    if model is not None:
        true_variables = sorted(
            literal - 1
            for literal in model
            if 1 <= literal <= instance.variable_count
        )
        result["true_variables"] = true_variables
    print(json.dumps(result, sort_keys=True), flush=True)
    return 10 if answer is True else (0 if answer is False else 2)


def run_retry(plan_path: Path) -> int:
    plan = validate_plan(plan_path)
    plan_sha256 = sha256_file(plan_path)
    output_dir = ROOT / str(plan["output_directory"])
    record_dir = output_dir / "records"
    record_dir.mkdir(parents=True, exist_ok=True)
    lock_path = output_dir / ".run.lock"
    started = time.monotonic()
    executed = reused = 0
    with lock_path.open("a+b") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError("another limit retry holds the run lock") from error
        for target in plan["targets"]:
            target_index = int(target["target"])
            record_path = record_dir / f"target_{target_index:03d}.json"
            if record_path.exists():
                record = json.loads(record_path.read_text(encoding="utf-8"))
                if (
                    record.get("plan_sha256") != plan_sha256
                    or record.get("target") != target_index
                    or record.get("status") not in ("UNSAT", "LIMIT")
                ):
                    raise ValueError(f"stale retry record {record_path}")
                reused += 1
                continue
            output_bytes = sum(
                item.stat().st_size
                for item in output_dir.rglob("*")
                if item.is_file()
            )
            if output_bytes > int(plan["output_byte_cap"]):
                raise RuntimeError("retry output byte cap exceeded")
            if os.statvfs(output_dir).f_bavail * os.statvfs(
                output_dir
            ).f_frsize < int(plan["free_disk_reserve_bytes"]):
                raise RuntimeError("retry free-disk reserve breached")
            environment = os.environ.copy()
            environment["PYTHONPATH"] = str(plan["pysat_root"])
            worker_started = time.monotonic()
            worker = subprocess.run(
                (
                    str(plan["python_executable"]),
                    str(Path(__file__).resolve()),
                    "--worker",
                    "--plan",
                    str(plan_path),
                    "--target-index",
                    str(target_index),
                ),
                text=True,
                capture_output=True,
                check=False,
                timeout=float(plan["worker_timeout_seconds"]),
                env=environment,
            )
            worker_seconds = time.monotonic() - worker_started
            result = parse_last_json(worker.stdout, "Cadical retry worker")
            status = result.get("status")
            expected_returncode = {"UNSAT": 0, "LIMIT": 2, "SAT": 10}.get(
                status
            )
            if worker.returncode != expected_returncode:
                raise RuntimeError(
                    f"worker {target_index} malformed rc={worker.returncode}: "
                    f"{worker.stdout}\n{worker.stderr}"
                )
            if status == "SAT":
                preserved = preserve_sat(
                    solver_record=result,
                    plan_path=plan_path,
                    plan_sha256=plan_sha256,
                    corpus=ROOT / str(plan["corpus"]),
                    output_dir=output_dir,
                    exhaustive=ROOT / str(plan["exhaustive_sat_verifier"]),
                    bitset=ROOT / str(plan["bitset_sat_verifier"]),
                )
                found = {
                    "schema": (
                        "ramsey55.e2_triple_replacement_limit_retry_found.v2"
                    ),
                    "created_utc": utc_now(),
                    "plan": relative(plan_path),
                    "plan_sha256": plan_sha256,
                    "target": target_index,
                    "worker_stdout": worker.stdout,
                    "worker_stderr": worker.stderr,
                    **preserved,
                }
                atomic_json(output_dir / "FOUND.json", found)
                print(json.dumps(found, sort_keys=True))
                return 0 if preserved["verified"] else 1
            retained = {
                **result,
                "plan_sha256": plan_sha256,
                "completed_utc": utc_now(),
                "worker_wall_seconds": worker_seconds,
                "worker_returncode": worker.returncode,
                "worker_stderr": worker.stderr,
                "evidence_category": (
                    "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
                    if status == "UNSAT"
                    else "LIMIT_NO_CONCLUSION"
                ),
            }
            atomic_json(record_path, retained)
            executed += 1

        checker = ROOT / str(plan["checker"])
        check_path = output_dir / "check.json"
        check_run = subprocess.run(
            (
                sys.executable,
                str(checker),
                "--plan",
                str(plan_path),
                "--record-dir",
                str(record_dir),
                "--output",
                str(check_path),
            ),
            text=True,
            capture_output=True,
            check=False,
            timeout=600,
        )
        if check_run.returncode != 0:
            raise RuntimeError(
                f"retry checker failed: {check_run.stdout}\n{check_run.stderr}"
            )
        check = parse_last_json(check_run.stdout, "retry checker")
        if check.get("valid") is not True:
            raise RuntimeError("retry checker did not return valid")
        result = {
            "schema": "ramsey55.e2_triple_replacement_limit_retry_result.v2",
            "completed_utc": utc_now(),
            "status": (
                "COMPLETE_OBSERVATIONAL_NEGATIVE"
                if int(check["counts"]["LIMIT"]) == 0
                else "COMPLETE_WITH_LIMITS_NO_CONCLUSION"
            ),
            "plan": relative(plan_path),
            "plan_sha256": plan_sha256,
            "runtime_seconds_this_invocation": time.monotonic() - started,
            "executed_target_count": executed,
            "reused_target_count": reused,
            "check": relative(check_path),
            "check_sha256": sha256_file(check_path),
            "counts": check["counts"],
            "combined_coverage": check["combined_coverage"],
            "construction_found": False,
            "proof_generation": False,
            "proof_checked_negative_count": 0,
            "claim_boundary": plan["claim_boundary"],
        }
        result_path = output_dir / "result.json"
        atomic_json(result_path, result)
        result["result_sha256"] = sha256_file(result_path)
        print(json.dumps(result, sort_keys=True))
        return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--make-plan", action="store_true")
    mode.add_argument("--run", action="store_true")
    mode.add_argument("--worker", action="store_true")
    parser.add_argument(
        "--plan",
        type=Path,
        default=(
            ROOT
            / "results"
            / "benchmark_plans"
            / "e2_triple_replacement_limit_retry_v2.json"
        ),
    )
    parser.add_argument(
        "--base-plan",
        type=Path,
        default=(
            ROOT
            / "results"
            / "benchmark_plans"
            / "e2_triple_replacement_screen_v1.json"
        ),
    )
    parser.add_argument(
        "--base-coverage",
        type=Path,
        default=(
            ROOT
            / "results"
            / "constructive"
            / "e2_triple_replacement_screen_v1"
            / "coverage.json"
        ),
    )
    parser.add_argument(
        "--base-shard-dir",
        type=Path,
        default=(
            ROOT
            / "results"
            / "constructive"
            / "e2_triple_replacement_screen_v1"
            / "shards"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=(
            ROOT
            / "results"
            / "constructive"
            / "e2_triple_replacement_limit_retry_v2"
        ),
    )
    parser.add_argument(
        "--python-executable",
        type=Path,
        default=Path("/opt/homebrew/opt/python@3.11/bin/python3.11"),
    )
    parser.add_argument(
        "--pysat-root",
        type=Path,
        default=Path("/tmp/ramsey55-pysat.4YSXId"),
    )
    parser.add_argument(
        "--checker",
        type=Path,
        default=(
            ROOT
            / "verify"
            / "e2_triple_replacement_limit_retry_check.py"
        ),
    )
    parser.add_argument(
        "--tests",
        type=Path,
        default=(
            ROOT / "tests" / "e2_triple_replacement_limit_retry_tests.py"
        ),
    )
    parser.add_argument(
        "--exhaustive",
        type=Path,
        default=ROOT / "verify" / "exhaustive_verify.py",
    )
    parser.add_argument(
        "--bitset",
        type=Path,
        default=ROOT / "build" / "bitset_verify",
    )
    parser.add_argument("--conflict-budget", type=int, default=10_000_000)
    parser.add_argument("--worker-timeout", type=float, default=60.0)
    parser.add_argument("--output-byte-cap", type=int, default=10_000_000)
    parser.add_argument(
        "--free-disk-reserve-bytes", type=int, default=4_000_000_000
    )
    parser.add_argument("--target-index", type=int)
    args = parser.parse_args()
    if args.worker:
        if args.target_index is None:
            parser.error("--worker requires --target-index")
        return run_worker(args.plan, args.target_index)
    if args.make_plan:
        plan = make_plan(
            plan_path=args.plan,
            base_plan_path=args.base_plan,
            base_coverage_path=args.base_coverage,
            base_shard_dir=args.base_shard_dir,
            output_dir=args.output_dir,
            python_executable=args.python_executable,
            pysat_root=args.pysat_root,
            checker=args.checker,
            tests=args.tests,
            exhaustive=args.exhaustive,
            bitset=args.bitset,
            conflict_budget=args.conflict_budget,
            worker_timeout=args.worker_timeout,
            output_byte_cap=args.output_byte_cap,
            reserve_bytes=args.free_disk_reserve_bytes,
        )
        print(
            json.dumps(
                {
                    "status": "PLAN_FROZEN",
                    "plan": relative(args.plan),
                    "plan_sha256": sha256_file(args.plan),
                    "target_count": plan["target_count"],
                },
                sort_keys=True,
            )
        )
        return 0
    return run_retry(args.plan)


if __name__ == "__main__":
    raise SystemExit(main())
