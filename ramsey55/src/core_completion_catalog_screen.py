#!/usr/bin/env python3
"""Fast constructive screen of every catalog delete-one/add-two fixed core.

UNSAT statuses from this workflow are intentionally *not* proof-checked and
therefore remain reproducible computational observations.  A SAT model is
atomically preserved, reconstructed as a 43-vertex graph, and checked by both
independent project graph verifiers before it is promoted.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_catalog_batch import (  # noqa: E402
    atomic_json,
    atomic_write,
    data_line_count,
    parse_last_json,
    sha256_file,
)
from core_completion_sat import (  # noqa: E402
    completed_adjacency,
    count_forbidden_sets,
    induced_core,
)
from graph_io import (  # noqa: E402
    encode_graph6,
    read_graph,
    write_canonical_artifact,
)


SCREEN_ID = "ramsey55_core_completion_catalog_k1_constructive_screen_v1"
OBSERVED_UNSAT = "OBSERVED_UNSAT_UNCHECKED"
VERIFIED_SAT = "DUAL_VERIFIED_SAT_CONSTRUCTION"
FAILED_SAT = "SAT_MODEL_VERIFICATION_FAILED"
LIMIT = "LIMIT_NO_CONCLUSION"
ERROR = "SCREEN_ERROR"


def record_path(output_dir: Path, line: int, deleted: int) -> Path:
    return (
        output_dir
        / "records"
        / f"line_{line:03d}"
        / f"line_{line:03d}_delete_{deleted:02d}.json"
    )


def validate_plan(
    plan_path: Path,
    *,
    catalog_sha256: str,
    catalog_lines: int,
    solver_sha256: str,
    seconds_limit: float,
    node_limit: int,
    jobs: int,
) -> dict[str, object]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    required = {
        "catalog_sha256": catalog_sha256,
        "catalog_data_line_count": catalog_lines,
        "full_pair_count": catalog_lines * 42,
        "solver_binary_sha256": solver_sha256,
        "seconds_limit_per_instance": seconds_limit,
        "node_limit_per_instance": node_limit,
        "jobs": jobs,
        "unsat_proof_replay": False,
    }
    mismatches = {
        key: {"plan": plan.get(key), "command": value}
        for key, value in required.items()
        if plan.get(key) != value
    }
    if mismatches:
        raise ValueError(f"screen plan mismatch: {mismatches}")
    return plan


def preserve_and_verify_sat(
    *,
    catalog: Path,
    catalog_sha256: str,
    line: int,
    deleted: int,
    solver_result: dict[str, object],
    output_dir: Path,
    python: Path,
    exhaustive_verifier: Path,
    bitset_verifier: Path,
) -> dict[str, object]:
    raw_true = solver_result.get("true_variables")
    if not isinstance(raw_true, list):
        raise ValueError("SAT result has no true-variable list")
    true_variables = sorted(int(value) for value in raw_true)
    stem = f"line_{line:03d}_delete_{deleted:02d}"
    candidate_dir = output_dir / "sat_candidates" / stem
    model_path = candidate_dir / f"{stem}.model.json"
    model_record = {
        "screen": SCREEN_ID,
        "preserved_utc": datetime.now(timezone.utc).isoformat(),
        "catalog_sha256": catalog_sha256,
        "catalog_line": line,
        "deleted_vertex": deleted,
        "variable_numbering": "zero-based, as emitted by C++ solver",
        "true_variables": true_variables,
        "solver_result": solver_result,
    }
    # This write happens before graph reconstruction or any verifier call.
    atomic_json(model_path, model_record)

    base = read_graph(catalog, line)
    core, original_vertices = induced_core(base, deleted)
    true_set = set(true_variables)
    assignment = [variable in true_set for variable in range(83)]
    completed = completed_adjacency(core, assignment)
    internal_counts = count_forbidden_sets(completed, 5)
    graph6_path = candidate_dir / f"{stem}.candidate.g6"
    canonical_path = candidate_dir / f"{stem}.candidate.canonical.json"
    atomic_write(graph6_path, (encode_graph6(completed) + "\n").encode("ascii"))
    canonical_sha256 = write_canonical_artifact(
        completed,
        canonical_path,
        provenance={
            "source": SCREEN_ID,
            "catalog_sha256": catalog_sha256,
            "catalog_line": line,
            "deleted_vertex": deleted,
            "retained_original_vertices": list(original_vertices),
            "model_sha256": sha256_file(model_path),
        },
    )

    exhaustive = subprocess.run(
        (str(python), str(exhaustive_verifier), str(graph6_path)),
        text=True,
        capture_output=True,
        check=False,
    )
    bitset = subprocess.run(
        (str(bitset_verifier), str(graph6_path)),
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
    verification_path = candidate_dir / f"{stem}.verification.json"
    atomic_json(
        verification_path,
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
        "model_path": str(model_path.resolve()),
        "model_sha256": sha256_file(model_path),
        "candidate_graph6_path": str(graph6_path.resolve()),
        "candidate_graph6_sha256": sha256_file(graph6_path),
        "candidate_canonical_path": str(canonical_path.resolve()),
        "candidate_canonical_sha256": canonical_sha256,
        "verification_path": str(verification_path.resolve()),
        "verification_sha256": sha256_file(verification_path),
    }


def screen_instance(
    pair: tuple[int, int],
    *,
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
) -> dict[str, object]:
    line, deleted = pair
    started = time.monotonic()
    solved = subprocess.run(
        (
            str(solver),
            "--graph",
            str(catalog),
            "--line",
            str(line),
            "--delete",
            str(deleted),
            "--node-limit",
            str(node_limit),
            "--seconds-limit",
            str(seconds_limit),
            "--progress",
            "0",
        ),
        text=True,
        capture_output=True,
        check=False,
    )
    solver_wall = time.monotonic() - started
    solver_result = parse_last_json(solved.stdout, "screen solver")
    expected_return = {"SAT": 10, "UNSAT": 20, "LIMIT": 2}.get(
        solver_result.get("status")
    )
    if solved.returncode != expected_return:
        raise RuntimeError(
            f"status/return mismatch for {(line, deleted)}: "
            f"status={solver_result.get('status')!r} "
            f"returncode={solved.returncode} stderr={solved.stderr!r}"
        )
    if (
        solver_result.get("catalog_line") != line
        or solver_result.get("deleted_vertex") != deleted
    ):
        raise RuntimeError(f"solver selected the wrong pair for {(line, deleted)}")

    record: dict[str, object] = {
        "screen": SCREEN_ID,
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "catalog": str(catalog.resolve()),
        "catalog_sha256": catalog_sha256,
        "catalog_line": line,
        "deleted_vertex": deleted,
        "solver_path": str(solver.resolve()),
        "solver_sha256": solver_sha256,
        "solver_returncode": solved.returncode,
        "solver_wall_seconds": solver_wall,
        "solver_stderr": solved.stderr,
        "solver_result": solver_result,
        "fixed_core_scope": (
            "only the induced 41-vertex core selected by this catalog line "
            "and deletion label"
        ),
    }
    if solver_result["status"] == "UNSAT":
        record.update(
            {
                "classification": OBSERVED_UNSAT,
                "evidence_category": (
                    "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
                ),
                "negative_certified": False,
                "proof_generated": False,
                "proof_checked": False,
            }
        )
    elif solver_result["status"] == "LIMIT":
        record.update(
            {
                "classification": LIMIT,
                "evidence_category": (
                    "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
                ),
                "negative_certified": False,
                "proof_generated": False,
                "proof_checked": False,
            }
        )
    else:
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
        record["evidence_category"] = (
            "CERTIFIED" if record["classification"] == VERIFIED_SAT else
            "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        )
        record["negative_certified"] = False
        record["proof_generated"] = False
        record["proof_checked"] = False

    path = record_path(output_dir, line, deleted)
    atomic_json(path, record)
    record["record_path"] = str(path.resolve())
    record["record_sha256"] = sha256_file(path)
    return record


def reusable_record(
    path: Path,
    *,
    line: int,
    deleted: int,
    catalog_sha256: str,
    solver_sha256: str,
) -> dict[str, object] | None:
    if not path.is_file():
        return None
    record = json.loads(path.read_text(encoding="utf-8"))
    if (
        record.get("catalog_line") != line
        or record.get("deleted_vertex") != deleted
        or record.get("catalog_sha256") != catalog_sha256
        or record.get("solver_sha256") != solver_sha256
        or record.get("classification")
        not in (OBSERVED_UNSAT, VERIFIED_SAT, LIMIT)
    ):
        return None
    if record.get("classification") == VERIFIED_SAT:
        for path_key, hash_key in (
            ("model_path", "model_sha256"),
            ("candidate_graph6_path", "candidate_graph6_sha256"),
            ("candidate_canonical_path", "candidate_canonical_sha256"),
            ("verification_path", "verification_sha256"),
        ):
            artifact = Path(str(record[path_key]))
            if (
                not artifact.is_file()
                or sha256_file(artifact) != record.get(hash_key)
            ):
                return None
    record["record_path"] = str(path.resolve())
    record["record_sha256"] = sha256_file(path)
    record["resumed"] = True
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seconds-limit-per-instance", type=float, required=True)
    parser.add_argument("--node-limit-per-instance", type=int, required=True)
    parser.add_argument("--jobs", type=int, required=True)
    parser.add_argument("--resume", action="store_true")
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
    if args.seconds_limit_per_instance <= 0:
        raise SystemExit("--seconds-limit-per-instance must be positive")
    if args.node_limit_per_instance <= 0:
        raise SystemExit("--node-limit-per-instance must be positive")
    if args.jobs <= 0:
        raise SystemExit("--jobs must be positive")
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
    validate_plan(
        args.plan,
        catalog_sha256=catalog_sha256,
        catalog_lines=catalog_lines,
        solver_sha256=solver_sha256,
        seconds_limit=args.seconds_limit_per_instance,
        node_limit=args.node_limit_per_instance,
        jobs=args.jobs,
    )
    if args.output_dir.exists() and any(args.output_dir.iterdir()) and not args.resume:
        raise SystemExit(
            "output directory is nonempty; use a fresh directory or --resume"
        )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pairs = [
        (line, deleted)
        for line in range(1, catalog_lines + 1)
        for deleted in range(42)
    ]
    results: list[dict[str, object]] = []
    pending: list[tuple[int, int]] = []
    for line, deleted in pairs:
        existing = (
            reusable_record(
                record_path(args.output_dir, line, deleted),
                line=line,
                deleted=deleted,
                catalog_sha256=catalog_sha256,
                solver_sha256=solver_sha256,
            )
            if args.resume
            else None
        )
        if existing is None:
            pending.append((line, deleted))
        else:
            results.append(existing)

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
    }
    completed = len(results)
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.jobs
    ) as executor:
        future_to_pair = {
            executor.submit(screen_instance, pair, **common): pair
            for pair in pending
        }
        for future in concurrent.futures.as_completed(future_to_pair):
            line, deleted = future_to_pair[future]
            try:
                result = future.result()
            except Exception as error:
                result = {
                    "screen": SCREEN_ID,
                    "recorded_utc": datetime.now(timezone.utc).isoformat(),
                    "catalog": str(args.catalog.resolve()),
                    "catalog_sha256": catalog_sha256,
                    "catalog_line": line,
                    "deleted_vertex": deleted,
                    "solver_path": str(args.solver.resolve()),
                    "solver_sha256": solver_sha256,
                    "classification": ERROR,
                    "evidence_category": (
                        "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
                    ),
                    "negative_certified": False,
                    "error": repr(error),
                }
                path = record_path(args.output_dir, line, deleted)
                atomic_json(path, result)
                result["record_path"] = str(path.resolve())
                result["record_sha256"] = sha256_file(path)
            results.append(result)
            completed += 1
            classification = result["classification"]
            if (
                completed % 250 == 0
                or classification not in (OBSERVED_UNSAT,)
            ):
                print(
                    json.dumps(
                        {
                            "completed": completed,
                            "total": len(pairs),
                            "catalog_line": line,
                            "deleted_vertex": deleted,
                            "classification": classification,
                            "elapsed_seconds": time.monotonic() - started,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )

    results.sort(
        key=lambda item: (
            int(item["catalog_line"]),
            int(item["deleted_vertex"]),
        )
    )
    classifications = (
        OBSERVED_UNSAT,
        VERIFIED_SAT,
        FAILED_SAT,
        LIMIT,
        ERROR,
    )
    counts = {
        classification: sum(
            result["classification"] == classification for result in results
        )
        for classification in classifications
    }
    summary = {
        "screen": SCREEN_ID,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "evidence_category": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        "negative_result_policy": (
            "UNSAT statuses were not proof-replayed and are not certified"
        ),
        "scope": (
            "Each negative status concerns only one fixed induced 41-vertex "
            "catalog core; neither individual nor aggregate negatives are "
            "global order-43 nonexistence."
        ),
        "catalog": str(args.catalog.resolve()),
        "catalog_sha256": catalog_sha256,
        "catalog_data_line_count": catalog_lines,
        "deletion_labels": list(range(42)),
        "expected_pair_count": catalog_lines * 42,
        "actual_record_count": len(results),
        "jobs": args.jobs,
        "seconds_limit_per_instance": args.seconds_limit_per_instance,
        "node_limit_per_instance": args.node_limit_per_instance,
        "unsat_proof_replay": False,
        "solver_path": str(args.solver.resolve()),
        "solver_sha256": solver_sha256,
        "plan": str(args.plan.resolve()),
        "plan_sha256": sha256_file(args.plan),
        "screen_source_sha256": sha256_file(Path(__file__)),
        "runtime_seconds": time.monotonic() - started,
        "resumed_record_count": sum(bool(item.get("resumed")) for item in results),
        "counts": counts,
        "instances": results,
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
            },
            sort_keys=True,
        ),
        flush=True,
    )
    if counts[ERROR] or counts[FAILED_SAT]:
        return 1
    if counts[VERIFIED_SAT]:
        return 10
    if counts[LIMIT]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
