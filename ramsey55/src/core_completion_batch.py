#!/usr/bin/env python3
"""Generate and exactly solve a deterministic batch of k=1 core completions."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_sat import (  # noqa: E402
    GENERATOR_ID,
    build_core_completion_instance,
    completed_adjacency,
    count_forbidden_sets,
    induced_core,
    render_dimacs,
)
from extension_sat_solver import (  # noqa: E402
    SOLVER_ID,
    DpllSolver,
    SearchTimeout,
    model_satisfies,
    write_proof,
)
from graph_io import (  # noqa: E402
    encode_graph6,
    read_graph,
    validate_simple,
    write_canonical_artifact,
)


BATCH_ID = "core_completion_k1_batch_v1"


def parse_deletions(specification: str, order: int) -> list[int]:
    if specification == "all":
        return list(range(order))
    result: set[int] = set()
    for part in specification.split(","):
        if "-" in part:
            left, right = part.split("-", 1)
            result.update(range(int(left), int(right) + 1))
        else:
            result.add(int(part))
    if not result or min(result) < 0 or max(result) >= order:
        raise ValueError(f"deletions must lie in 0..{order - 1}")
    return sorted(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_graph", type=Path)
    parser.add_argument("--line", type=int, default=1)
    parser.add_argument("--deletions", default="all")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--time-limit-per-instance", type=float, default=60.0)
    args = parser.parse_args()
    if args.time_limit_per_instance <= 0:
        raise SystemExit("--time-limit-per-instance must be positive")

    batch_started = time.monotonic()
    base_bytes = args.base_graph.read_bytes()
    base_sha256 = hashlib.sha256(base_bytes).hexdigest()
    base = read_graph(args.base_graph, args.line)
    validate_simple(base)
    base_conflicts = count_forbidden_sets(base, 5)
    if base_conflicts != (0, 0):
        raise SystemExit(f"invalid base graph: conflicts={base_conflicts}")
    deletions = parse_deletions(args.deletions, len(base))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, object]] = []
    exit_status = 0
    for deleted_vertex in deletions:
        instance_started = time.monotonic()
        core, original_vertices = induced_core(base, deleted_vertex)
        instance = build_core_completion_instance(core, 5)
        stem = f"core_completion_delete_{deleted_vertex:02d}"
        cnf_path = args.output_dir / f"{stem}.cnf"
        proof_path = args.output_dir / f"{stem}.tree"
        metadata_path = args.output_dir / f"{stem}.json"
        dimacs = render_dimacs(
            instance,
            base_graph6=encode_graph6(base),
            base_file_sha256=base_sha256,
            deleted_original_vertex=deleted_vertex,
            core_original_vertices=original_vertices,
        )
        cnf_path.write_text(dimacs, encoding="ascii")
        cnf_sha256 = hashlib.sha256(dimacs.encode("ascii")).hexdigest()

        solver_started = time.monotonic()
        solver = DpllSolver(
            instance.variable_count,
            list(instance.clauses),
            deadline=solver_started + args.time_limit_per_instance,
        )
        try:
            model = solver.solve()
            status = "SAT" if model is not None else "UNSAT"
        except SearchTimeout:
            model = None
            status = "TIMEOUT"
            exit_status = 2
        solver_runtime = time.monotonic() - solver_started

        proof_sha256: str | None = None
        candidate_graph6_sha256: str | None = None
        candidate_canonical_sha256: str | None = None
        true_variables: list[int] | None = None
        if status == "UNSAT":
            with proof_path.open("w", encoding="ascii", newline="\n") as stream:
                write_proof(
                    stream,
                    instance.variable_count,
                    cnf_sha256,
                    solver.proof_records,
                )
            proof_sha256 = hashlib.sha256(proof_path.read_bytes()).hexdigest()
        elif status == "SAT":
            assert model is not None
            if not model_satisfies(model, list(instance.clauses)):
                raise AssertionError("solver returned a false model")
            assignment = [bool(value) for value in model[1:]]
            completed = completed_adjacency(core, assignment)
            if count_forbidden_sets(completed, 5) != (0, 0):
                raise AssertionError("SAT model failed direct graph validation")
            candidate_g6_path = args.output_dir / f"{stem}.candidate.g6"
            candidate_json_path = (
                args.output_dir / f"{stem}.candidate.canonical.json"
            )
            candidate_g6_path.write_text(
                encode_graph6(completed) + "\n", encoding="ascii"
            )
            candidate_graph6_sha256 = hashlib.sha256(
                candidate_g6_path.read_bytes()
            ).hexdigest()
            true_variables = [
                variable
                for variable in range(1, instance.variable_count + 1)
                if model[variable]
            ]
            candidate_canonical_sha256 = write_canonical_artifact(
                completed,
                candidate_json_path,
                provenance={
                    "source": BATCH_ID,
                    "base_file_sha256": base_sha256,
                    "deleted_original_vertex": deleted_vertex,
                    "true_variables": true_variables,
                },
            )
            # A SAT result requires external independent verifier invocations.
            exit_status = max(exit_status, 10)

        result: dict[str, object] = {
            "batch": BATCH_ID,
            "generator": GENERATOR_ID,
            "solver": SOLVER_ID,
            "base_file_sha256": base_sha256,
            "deleted_original_vertex": deleted_vertex,
            "core_graph6": encode_graph6(core),
            "core_vertex_count": len(core),
            "variable_count": instance.variable_count,
            "one_new_clique_clause_count": instance.one_new_clique_count,
            "two_new_clique_clause_count": instance.two_new_clique_count,
            "one_new_independent_clause_count": (
                instance.one_new_independent_count
            ),
            "two_new_independent_clause_count": (
                instance.two_new_independent_count
            ),
            "clause_count": len(instance.clauses),
            "cnf_sha256": cnf_sha256,
            "status": status,
            "solver_runtime_seconds": solver_runtime,
            "instance_runtime_seconds": time.monotonic() - instance_started,
            "proof_sha256": proof_sha256,
            "proof_record_count": len(solver.proof_records),
            "candidate_graph6_sha256": candidate_graph6_sha256,
            "candidate_canonical_sha256": candidate_canonical_sha256,
            "true_variables": true_variables,
            **vars(solver.stats),
        }
        metadata_path.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        results.append(result)
        print(json.dumps(result, sort_keys=True), flush=True)

    summary = {
        "batch": BATCH_ID,
        "base_file_sha256": base_sha256,
        "deletions": deletions,
        "instance_count": len(results),
        "sat_count": sum(item["status"] == "SAT" for item in results),
        "unsat_count": sum(item["status"] == "UNSAT" for item in results),
        "timeout_count": sum(item["status"] == "TIMEOUT" for item in results),
        "batch_runtime_seconds": time.monotonic() - batch_started,
        "instances": results,
    }
    summary_path = args.output_dir / "core_completion_summary.json"
    summary_path.write_text(
        json.dumps(summary, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in summary.items() if key != "instances"}, sort_keys=True))
    return exit_status


if __name__ == "__main__":
    raise SystemExit(main())
