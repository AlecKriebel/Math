#!/usr/bin/env python3
"""Run checked delete-one/add-two completions across a graph6 catalog.

Each pair (catalog data line, deleted vertex) denotes one fixed 41-vertex
core.  UNSAT is accepted only after the independent exhaustive-tree checker
reconstructs that selected core and replays the proof.  SAT models are
persisted before candidate construction and then sent through both project
graph verifiers.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

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


BATCH_ID = "ramsey55_core_completion_catalog_k1_batch_v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def atomic_json(path: Path, value: object) -> None:
    atomic_write(
        path,
        (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8"),
    )


def parse_indices(specification: str, maximum: int) -> list[int]:
    if specification == "all":
        return list(range(1, maximum + 1))
    result: set[int] = set()
    for raw_part in specification.split(","):
        part = raw_part.strip()
        if not part:
            raise ValueError("empty index component")
        if "-" in part:
            left_text, right_text = part.split("-", 1)
            left, right = int(left_text), int(right_text)
            if left > right:
                raise ValueError(f"descending index range {part}")
            result.update(range(left, right + 1))
        else:
            result.add(int(part))
    if not result or min(result) < 1 or max(result) > maximum:
        raise ValueError(f"indices must lie in 1..{maximum}")
    return sorted(result)


def parse_deletions(specification: str) -> list[int]:
    # Reuse the one-based parser by shifting deletion labels.
    if specification == "all":
        return list(range(42))
    shifted = parse_indices(
        ",".join(
            (
                f"{int(part.split('-', 1)[0]) + 1}-"
                f"{int(part.split('-', 1)[1]) + 1}"
                if "-" in part
                else str(int(part) + 1)
            )
            for part in specification.split(",")
        ),
        42,
    )
    return [value - 1 for value in shifted]


def data_line_count(path: Path) -> int:
    return sum(
        bool(line.strip()) and not line.lstrip().startswith(b"#")
        for line in path.read_bytes().splitlines()
    )


def parse_last_json(output: str, label: str) -> dict[str, object]:
    lines = [line for line in output.splitlines() if line.strip()]
    if not lines:
        raise ValueError(f"{label} emitted no JSON")
    value = json.loads(lines[-1])
    if not isinstance(value, dict):
        raise ValueError(f"{label} JSON is not an object")
    return value


def planned_pairs(
    *,
    plan_path: Path | None,
    catalog_sha256: str,
    catalog_lines: int,
    line_specification: str,
    deletion_specification: str,
    seconds_limit: float,
    node_limit: int,
    jobs: int,
) -> tuple[list[tuple[int, int]], str | None]:
    if plan_path is None:
        lines = parse_indices(line_specification, catalog_lines)
        deletions = parse_deletions(deletion_specification)
        return [(line, deleted) for line in lines for deleted in deletions], None

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("catalog_sha256") != catalog_sha256:
        raise ValueError("pilot plan catalog hash mismatch")
    expected_options = {
        "seconds_limit_per_instance": seconds_limit,
        "node_limit_per_instance": node_limit,
        "jobs": jobs,
    }
    for key, value in expected_options.items():
        if plan.get(key) != value:
            raise ValueError(
                f"pilot plan {key}={plan.get(key)!r}, command requested "
                f"{value!r}"
            )
    raw_pairs = plan.get("pairs")
    if not isinstance(raw_pairs, list) or not raw_pairs:
        raise ValueError("pilot plan has no nonempty pairs list")
    pairs: list[tuple[int, int]] = []
    for raw in raw_pairs:
        if not isinstance(raw, dict):
            raise ValueError("pilot pair is not an object")
        line = int(raw["catalog_line"])
        deleted = int(raw["deleted_vertex"])
        if not 1 <= line <= catalog_lines or not 0 <= deleted < 42:
            raise ValueError(f"pilot pair outside catalog: {(line, deleted)}")
        pairs.append((line, deleted))
    if len(pairs) != len(set(pairs)):
        raise ValueError("pilot plan contains duplicate pairs")
    return pairs, sha256_file(plan_path)


def run_checked_instance(
    pair: tuple[int, int],
    *,
    catalog: Path,
    catalog_sha256: str,
    solver: Path,
    checker: Path,
    python: Path,
    exhaustive_verifier: Path,
    bitset_verifier: Path,
    output_dir: Path,
    seconds_limit: float,
    node_limit: int,
) -> dict[str, object]:
    line, deleted = pair
    stem = f"line_{line:03d}_delete_{deleted:02d}"
    instance_dir = output_dir / f"line_{line:03d}"
    instance_dir.mkdir(parents=True, exist_ok=True)
    proof_path = instance_dir / f"{stem}.proof.bin"
    result_path = instance_dir / f"{stem}.result.json"
    solver_started = time.monotonic()
    solved = subprocess.run(
        (
            str(solver),
            "--graph",
            str(catalog),
            "--line",
            str(line),
            "--delete",
            str(deleted),
            "--proof",
            str(proof_path),
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
    solver_wall = time.monotonic() - solver_started
    solver_result = parse_last_json(solved.stdout, "solver")
    expected_returncode = {"SAT": 10, "UNSAT": 20, "LIMIT": 2}.get(
        solver_result.get("status")
    )
    if solved.returncode != expected_returncode:
        raise RuntimeError(
            f"{stem}: solver status/return mismatch: "
            f"status={solver_result.get('status')} rc={solved.returncode} "
            f"stderr={solved.stderr!r}"
        )
    if (
        solver_result.get("catalog_line") != line
        or solver_result.get("deleted_vertex") != deleted
    ):
        raise RuntimeError(f"{stem}: solver selected the wrong fixed core")

    record: dict[str, object] = {
        "batch": BATCH_ID,
        "catalog": str(catalog),
        "catalog_sha256": catalog_sha256,
        "catalog_line": line,
        "deleted_vertex": deleted,
        "fixed_core_scope": (
            "only the induced 41-vertex core selected by this catalog line "
            "and deletion label"
        ),
        "solver_returncode": solved.returncode,
        "solver_wall_seconds": solver_wall,
        "solver_stderr": solved.stderr,
        "solver_result": solver_result,
    }

    if solver_result["status"] == "UNSAT":
        if not proof_path.is_file():
            raise RuntimeError(f"{stem}: UNSAT solver run produced no proof")
        checked_started = time.monotonic()
        checked = subprocess.run(
            (
                str(python),
                str(checker),
                "--graph",
                str(catalog),
                "--line",
                str(line),
                "--delete",
                str(deleted),
                "--proof",
                str(proof_path),
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        checker_wall = time.monotonic() - checked_started
        if checked.returncode != 0:
            raise RuntimeError(
                f"{stem}: proof checker rejected: {checked.stderr!r}"
            )
        checker_result = parse_last_json(checked.stdout, "proof checker")
        record.update(
            {
                "classification": "CHECKED_UNSAT_FIXED_CORE",
                "proof_path": str(proof_path),
                "proof_sha256": sha256_file(proof_path),
                "proof_bytes": proof_path.stat().st_size,
                "checker_wall_seconds": checker_wall,
                "checker_result": checker_result,
            }
        )
    elif solver_result["status"] == "SAT":
        raw_true = solver_result.get("true_variables")
        if not isinstance(raw_true, list):
            raise RuntimeError(f"{stem}: SAT result has no model")
        true_variables = sorted(int(value) for value in raw_true)
        model_path = instance_dir / f"{stem}.model.json"
        model_record = {
            "catalog_sha256": catalog_sha256,
            "catalog_line": line,
            "deleted_vertex": deleted,
            "variable_numbering": "zero-based, as emitted by C++ solver",
            "true_variables": true_variables,
            "solver_result": solver_result,
        }
        # Preserve the raw model before doing any reconstruction or checking.
        atomic_json(model_path, model_record)

        base = read_graph(catalog, line)
        core, original_vertices = induced_core(base, deleted)
        true_variable_set = set(true_variables)
        assignment = [
            variable in true_variable_set for variable in range(83)
        ]
        completed = completed_adjacency(core, assignment)
        internal_counts = count_forbidden_sets(completed, 5)
        candidate_path = instance_dir / f"{stem}.candidate.g6"
        canonical_path = instance_dir / f"{stem}.candidate.canonical.json"
        atomic_write(
            candidate_path, (encode_graph6(completed) + "\n").encode("ascii")
        )
        canonical_sha256 = write_canonical_artifact(
            completed,
            canonical_path,
            provenance={
                "source": BATCH_ID,
                "catalog_sha256": catalog_sha256,
                "catalog_line": line,
                "deleted_vertex": deleted,
                "retained_original_vertices": list(original_vertices),
                "model_sha256": sha256_file(model_path),
            },
        )
        exhaustive = subprocess.run(
            (str(python), str(exhaustive_verifier), str(candidate_path)),
            text=True,
            capture_output=True,
            check=False,
        )
        bitset = subprocess.run(
            (str(bitset_verifier), str(candidate_path)),
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
        atomic_json(
            instance_dir / f"{stem}.verification.json",
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
        record.update(
            {
                "classification": (
                    "DUAL_VERIFIED_SAT_CONSTRUCTION"
                    if verified
                    else "SAT_MODEL_VERIFICATION_FAILED"
                ),
                "model_path": str(model_path),
                "model_sha256": sha256_file(model_path),
                "candidate_graph6_path": str(candidate_path),
                "candidate_graph6_sha256": sha256_file(candidate_path),
                "candidate_canonical_path": str(canonical_path),
                "candidate_canonical_sha256": canonical_sha256,
                "dual_verified": verified,
            }
        )
    else:
        partial_path = Path(str(proof_path) + ".partial")
        record.update(
            {
                "classification": "LIMIT_NO_CONCLUSION",
                "partial_proof_path": (
                    str(partial_path) if partial_path.is_file() else None
                ),
                "partial_proof_sha256": (
                    sha256_file(partial_path)
                    if partial_path.is_file()
                    else None
                ),
            }
        )

    record["recorded_utc"] = datetime.now(timezone.utc).isoformat()
    atomic_json(result_path, record)
    record["result_path"] = str(result_path)
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument(
        "--checker",
        type=Path,
        default=ROOT / "verify" / "core_completion_proof_check.py",
    )
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
    parser.add_argument("--lines", default="all")
    parser.add_argument("--deletions", default="all")
    parser.add_argument("--pairs-plan", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seconds-limit-per-instance", type=float, default=60.0)
    parser.add_argument("--node-limit-per-instance", type=int, default=1_000_000)
    parser.add_argument("--jobs", type=int, default=1)
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
        args.checker,
        args.python,
        args.exhaustive_verifier,
        args.bitset_verifier,
    ):
        if not required.is_file():
            raise SystemExit(f"required file is absent: {required}")

    started = time.monotonic()
    catalog_sha256 = sha256_file(args.catalog)
    catalog_lines = data_line_count(args.catalog)
    pairs, plan_sha256 = planned_pairs(
        plan_path=args.pairs_plan,
        catalog_sha256=catalog_sha256,
        catalog_lines=catalog_lines,
        line_specification=args.lines,
        deletion_specification=args.deletions,
        seconds_limit=args.seconds_limit_per_instance,
        node_limit=args.node_limit_per_instance,
        jobs=args.jobs,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    common = {
        "catalog": args.catalog.resolve(),
        "catalog_sha256": catalog_sha256,
        "solver": args.solver.resolve(),
        "checker": args.checker.resolve(),
        "python": args.python.resolve(),
        "exhaustive_verifier": args.exhaustive_verifier.resolve(),
        "bitset_verifier": args.bitset_verifier.resolve(),
        "output_dir": args.output_dir.resolve(),
        "seconds_limit": args.seconds_limit_per_instance,
        "node_limit": args.node_limit_per_instance,
    }
    results: list[dict[str, object]] = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.jobs
    ) as executor:
        future_to_pair = {
            executor.submit(run_checked_instance, pair, **common): pair
            for pair in pairs
        }
        for future in concurrent.futures.as_completed(future_to_pair):
            pair = future_to_pair[future]
            result = future.result()
            results.append(result)
            print(
                json.dumps(
                    {
                        "catalog_line": pair[0],
                        "deleted_vertex": pair[1],
                        "classification": result["classification"],
                        "solver_elapsed_seconds": result["solver_result"][
                            "elapsed_seconds"
                        ],
                        "solver_wall_seconds": result["solver_wall_seconds"],
                        "checker_wall_seconds": result.get(
                            "checker_wall_seconds"
                        ),
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
    counts = {
        classification: sum(
            result["classification"] == classification for result in results
        )
        for classification in (
            "CHECKED_UNSAT_FIXED_CORE",
            "DUAL_VERIFIED_SAT_CONSTRUCTION",
            "SAT_MODEL_VERIFICATION_FAILED",
            "LIMIT_NO_CONCLUSION",
        )
    }
    summary = {
        "batch": BATCH_ID,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "evidence_category": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        "scope": (
            "Each checked UNSAT result concerns only one fixed induced "
            "41-vertex catalog core; it is not global order-43 UNSAT."
        ),
        "catalog": str(args.catalog.resolve()),
        "catalog_sha256": catalog_sha256,
        "catalog_data_line_count": catalog_lines,
        "full_catalog_pair_count": catalog_lines * 42,
        "selected_pair_count": len(pairs),
        "selected_pairs": [
            {"catalog_line": line, "deleted_vertex": deleted}
            for line, deleted in pairs
        ],
        "pairs_plan": (
            str(args.pairs_plan.resolve()) if args.pairs_plan else None
        ),
        "pairs_plan_sha256": plan_sha256,
        "seconds_limit_per_instance": args.seconds_limit_per_instance,
        "node_limit_per_instance": args.node_limit_per_instance,
        "jobs": args.jobs,
        "solver_path": str(args.solver.resolve()),
        "solver_sha256": sha256_file(args.solver),
        "checker_path": str(args.checker.resolve()),
        "checker_sha256": sha256_file(args.checker),
        "batch_source_sha256": sha256_file(Path(__file__)),
        "runtime_seconds": time.monotonic() - started,
        "counts": counts,
        "instances": results,
    }
    summary_path = args.output_dir / "catalog_k1_batch_summary.json"
    atomic_json(summary_path, summary)
    print(
        json.dumps(
            {
                "summary": str(summary_path),
                "runtime_seconds": summary["runtime_seconds"],
                "selected_pair_count": len(pairs),
                "counts": counts,
            },
            sort_keys=True,
        )
    )
    if counts["SAT_MODEL_VERIFICATION_FAILED"]:
        return 1
    if counts["DUAL_VERIFIED_SAT_CONSTRUCTION"]:
        return 10
    if counts["LIMIT_NO_CONCLUSION"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
