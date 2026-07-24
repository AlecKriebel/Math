#!/usr/bin/env python3
"""Independently reconstruct and check the targeted Cadical retry ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_catalog_batch import atomic_json, sha256_file  # noqa: E402
from core_completion_k2 import build_k2_completion_instance  # noqa: E402
from e2_triple_replacement_compact import (  # noqa: E402
    STATUS_LIMIT,
    TRIPLES,
    iter_records,
)
from graph_io import read_graph, validate_simple  # noqa: E402


CHECKER_ID = "ramsey55_e2_triple_replacement_limit_retry_checker_v2"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def extract_base_limits(
    base_plan: dict[str, object], shard_dir: Path
) -> list[dict[str, object]]:
    limits: list[dict[str, object]] = []
    corpus_sha256 = str(base_plan["corpus_sha256"])
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
                limits.append(
                    {
                        "target": len(limits),
                        "input_index": input_index,
                        "triple_ordinal": record.triple_ordinal,
                        "deleted_vertices": list(record.deleted_vertices),
                        "base_shard": str(path.resolve().relative_to(ROOT)),
                        "base_shard_sha256": shard_sha256,
                        "base_nodes": record.nodes,
                        "base_elapsed_microseconds": (
                            record.elapsed_microseconds
                        ),
                    }
                )
    return limits


def run_check(plan_path: Path, record_dir: Path) -> dict[str, object]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan_sha256 = sha256_file(plan_path)
    if (
        plan.get("schema")
        != "ramsey55.e2_triple_replacement_limit_retry_plan.v2"
    ):
        raise ValueError("unexpected retry-plan schema")
    base_plan_path = ROOT / str(plan["base_plan"])
    base_coverage_path = ROOT / str(plan["base_coverage"])
    if sha256_file(base_plan_path) != plan.get("base_plan_sha256"):
        raise ValueError("base plan hash mismatch")
    if sha256_file(base_coverage_path) != plan.get("base_coverage_sha256"):
        raise ValueError("base coverage hash mismatch")
    base_plan = json.loads(base_plan_path.read_text(encoding="utf-8"))
    base_coverage = json.loads(
        base_coverage_path.read_text(encoding="utf-8")
    )
    if (
        base_coverage.get("valid") is not True
        or base_coverage.get("plan_sha256") != sha256_file(base_plan_path)
    ):
        raise ValueError("base coverage is not valid")
    base_limits = extract_base_limits(
        base_plan, ROOT / str(plan["base_shard_directory"])
    )
    if base_limits != plan.get("targets"):
        raise ValueError("plan targets do not exactly equal base limits")
    if len(base_limits) != int(plan["target_count"]):
        raise ValueError("retry target count mismatch")

    expected_names = {
        f"target_{index:03d}.json" for index in range(len(base_limits))
    }
    actual_names = {path.name for path in record_dir.glob("target_*.json")}
    if actual_names != expected_names:
        raise ValueError(
            "retry record filenames are not the exact target set: "
            f"missing={sorted(expected_names - actual_names)}, "
            f"extra={sorted(actual_names - expected_names)}"
        )

    corpus = ROOT / str(plan["corpus"])
    if sha256_file(corpus) != plan.get("corpus_sha256"):
        raise ValueError("retry corpus hash mismatch")
    graphs = {index: read_graph(corpus, index) for index in (1, 2)}
    counts = {"UNSAT": 0, "LIMIT": 0}
    total_generation_seconds = 0.0
    total_solver_seconds = 0.0
    total_conflicts = 0
    records: list[dict[str, object]] = []
    bundle_digest = hashlib.sha256()
    for target in base_limits:
        target_index = int(target["target"])
        path = record_dir / f"target_{target_index:03d}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        status = data.get("status")
        if status not in counts:
            raise ValueError(f"invalid retry status at target {target_index}")
        if data.get("plan_sha256") != plan_sha256:
            raise ValueError(f"plan hash mismatch at target {target_index}")
        for field in ("target", "input_index", "triple_ordinal"):
            if int(data.get(field, -1)) != int(target[field]):
                raise ValueError(
                    f"target identity mismatch for {field} at {target_index}"
                )
        deleted = tuple(int(value) for value in data["deleted_vertices"])
        if (
            list(deleted) != target["deleted_vertices"]
            or deleted != TRIPLES[int(target["triple_ordinal"])]
        ):
            raise ValueError(
                f"deletion triple mismatch at target {target_index}"
            )
        input_index = int(target["input_index"])
        core = induced_core_three(graphs[input_index], deleted)
        instance = build_k2_completion_instance(core)
        reconstructed_digest = formula_sha256(instance.clauses)
        if data.get("formula_sha256") != reconstructed_digest:
            raise ValueError(
                f"formula digest mismatch at target {target_index}"
            )
        if int(data.get("variables", -1)) != instance.variable_count:
            raise ValueError(
                f"variable count mismatch at target {target_index}"
            )
        if int(data.get("clauses", -1)) != len(instance.clauses):
            raise ValueError(
                f"clause count mismatch at target {target_index}"
            )
        if int(data.get("conflict_budget", -1)) != int(
            plan["conflict_budget_per_target"]
        ):
            raise ValueError(
                f"conflict budget mismatch at target {target_index}"
            )
        if data.get("proof_generated") is not False:
            raise ValueError("unexpected proof-generation claim")
        if data.get("proof_checked") is not False:
            raise ValueError("unexpected proof-check claim")
        statistics = data.get("solver_statistics")
        if not isinstance(statistics, dict):
            raise ValueError("missing solver statistics")
        conflicts = int(statistics.get("conflicts", -1))
        if conflicts < 0:
            raise ValueError("invalid Cadical conflict count")
        if status == "LIMIT" and conflicts > int(
            plan["conflict_budget_per_target"]
        ):
            raise ValueError("limit record exceeds conflict budget")
        record_sha256 = sha256_file(path)
        bundle_digest.update(
            f"{target_index} {record_sha256}\n".encode("ascii")
        )
        counts[status] += 1
        total_generation_seconds += float(data["generation_seconds"])
        total_solver_seconds += float(data["solver_seconds"])
        total_conflicts += conflicts
        records.append(
            {
                "target": target_index,
                "input_index": input_index,
                "triple_ordinal": int(target["triple_ordinal"]),
                "deleted_vertices": list(deleted),
                "status": status,
                "formula_sha256": reconstructed_digest,
                "record": str(path.resolve().relative_to(ROOT)),
                "record_sha256": record_sha256,
                "conflicts": conflicts,
            }
        )
    if sum(counts.values()) != len(base_limits):
        raise ValueError("retry status partition is incomplete")
    base_totals = base_coverage["totals"]
    combined = {
        "total_labeled_triples": int(base_totals["record_count"]),
        "structural_obstruction_count": int(
            base_totals["structural_obstruction_count"]
        ),
        "solver_observed_unsat_count": (
            int(base_totals["observed_unsat_count"]) + counts["UNSAT"]
        ),
        "unresolved_limit_count": counts["LIMIT"],
        "construction_found": False,
    }
    if (
        combined["structural_obstruction_count"]
        + combined["solver_observed_unsat_count"]
        + combined["unresolved_limit_count"]
        != combined["total_labeled_triples"]
    ):
        raise ValueError("combined exact coverage partition fails")
    return {
        "schema": "ramsey55.e2_triple_replacement_limit_retry_check.v2",
        "checker": CHECKER_ID,
        "checked_utc": utc_now(),
        "valid": True,
        "plan": str(plan_path.resolve().relative_to(ROOT)),
        "plan_sha256": plan_sha256,
        "record_directory": str(record_dir.resolve().relative_to(ROOT)),
        "target_count": len(base_limits),
        "exact_base_limit_coverage": True,
        "counts": counts,
        "combined_coverage": combined,
        "total_generation_seconds": total_generation_seconds,
        "total_solver_seconds": total_solver_seconds,
        "total_conflicts": total_conflicts,
        "record_bundle_sha256": bundle_digest.hexdigest(),
        "records": records,
        "negative_certified_count": 0,
        "proof_checked_negative_count": 0,
        "claim_boundary": (
            "The Cadical UNSAT results are exact-formula, reproducible "
            "observations without proof certificates. The combined ledger "
            "covers only the two frozen E=2 representatives."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--record-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = run_check(args.plan, args.record_dir)
    except Exception as error:
        failure = {
            "schema": "ramsey55.e2_triple_replacement_limit_retry_check.v2",
            "checker": CHECKER_ID,
            "checked_utc": utc_now(),
            "valid": False,
            "error": str(error),
        }
        if args.output:
            atomic_json(args.output, failure)
        print(json.dumps(failure, sort_keys=True))
        return 1
    if args.output:
        atomic_json(args.output, result)
        result["output_sha256"] = sha256_file(args.output)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
