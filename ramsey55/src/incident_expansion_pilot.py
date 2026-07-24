#!/usr/bin/env python3
"""Exact moving-boundary pilot around a near Ramsey(5,5;43) graph.

For each selected set of extra vertices, every edge incident to either the
recorded conflict union or an extra vertex is free.  All other edges remain
equal to the base graph.  The resulting exact CNF is solved independently for
each boundary.  SAT models are reconstructed as full graphs and checked by
direct five-set enumeration; UNSAT results from this pilot are observations,
not proof-carrying claims.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import itertools
import json
import os
import time
from pathlib import Path
from typing import Sequence

import pysat
from pysat import solvers

from graph_io import encode_graph6, read_graph, validate_simple
from residual_lns_sat import (
    apply_assignment,
    build_residual_lns_instance,
    count_forbidden_sets,
    formula_is_satisfied,
    neighborhood_edges,
)


PILOT_ID = "ramsey55_incident_conflict_expansion_pilot_v1"
SOLVERS = {
    name: getattr(solvers, name)
    for name in ("Glucose3", "Glucose4", "MapleChrono", "MapleCM", "Maplesat")
}


def parse_vertices(text: str) -> tuple[int, ...]:
    try:
        vertices = tuple(sorted({int(field) for field in text.split(",")}))
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "vertices must be comma-separated integers"
        ) from error
    if not vertices:
        raise argparse.ArgumentTypeError("at least one vertex is required")
    return vertices


def solve_boundary(
    base_path: str,
    conflict_vertices: tuple[int, ...],
    extra_vertices: tuple[int, ...],
    solver_name: str,
    conflict_budget: int | None,
) -> dict[str, object]:
    started = time.monotonic()
    adjacency = read_graph(Path(base_path))
    free_vertices = tuple(sorted(set(conflict_vertices) | set(extra_vertices)))
    free_edges = neighborhood_edges(
        len(adjacency),
        (),
        (),
        incident_vertices=free_vertices,
    )
    build_started = time.monotonic()
    instance = build_residual_lns_instance(adjacency, free_edges)
    build_seconds = time.monotonic() - build_started

    solver_class = SOLVERS[solver_name]
    solve_started = time.monotonic()
    with solver_class(
        bootstrap_with=instance.clauses,
        use_timer=True,
    ) as solver:
        if conflict_budget is None:
            outcome = solver.solve()
        else:
            solver.conf_budget(conflict_budget)
            outcome = solver.solve_limited()
        stats = solver.accum_stats()
        solver_cpu_seconds = solver.time_accum()
        model = solver.get_model() if outcome is True else None
    solve_seconds = time.monotonic() - solve_started

    status = (
        "SAT"
        if outcome is True
        else "UNSAT"
        if outcome is False
        else "BUDGET_EXHAUSTED"
    )
    record: dict[str, object] = {
        "extra_vertices": list(extra_vertices),
        "free_incident_vertices": list(free_vertices),
        "free_edge_count": len(free_edges),
        "clique_clause_count": len(instance.clique_clauses),
        "independent_clause_count": len(instance.independent_clauses),
        "clause_count": len(instance.clauses),
        "status": status,
        "build_seconds": build_seconds,
        "solve_seconds": solve_seconds,
        "solver_cpu_seconds": solver_cpu_seconds,
        "wall_seconds": time.monotonic() - started,
        **stats,
    }
    if outcome is True:
        assert model is not None
        values = {abs(literal): literal > 0 for literal in model}
        assignment = tuple(
            values.get(variable, False)
            for variable in range(1, len(free_edges) + 1)
        )
        if not formula_is_satisfied(instance.clauses, assignment):
            raise AssertionError("SAT model does not satisfy its boundary CNF")
        completed = apply_assignment(adjacency, free_edges, assignment)
        forbidden = count_forbidden_sets(completed)
        if forbidden != (0, 0):
            raise AssertionError(
                f"SAT boundary model is not a Ramsey graph: {forbidden}"
            )
        record["graph6"] = encode_graph6(completed)
        record["true_variables"] = [
            variable
            for variable, value in enumerate(assignment, start=1)
            if value
        ]
        record["forbidden_counts"] = list(forbidden)
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_graph", type=Path)
    parser.add_argument("--conflict-vertices", type=parse_vertices, required=True)
    parser.add_argument("--extra-count", type=int, default=1)
    parser.add_argument("--solver", choices=sorted(SOLVERS), default="Glucose3")
    parser.add_argument("--conflict-budget", type=int)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--candidate-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.extra_count < 1:
        parser.error("--extra-count must be positive")
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    if args.conflict_budget is not None and args.conflict_budget < 1:
        parser.error("--conflict-budget must be positive")

    adjacency = read_graph(args.base_graph)
    validate_simple(adjacency)
    order = len(adjacency)
    if any(not 0 <= vertex < order for vertex in args.conflict_vertices):
        parser.error("a conflict vertex is outside the base graph")
    remaining = tuple(
        vertex
        for vertex in range(order)
        if vertex not in set(args.conflict_vertices)
    )
    selections = tuple(itertools.combinations(remaining, args.extra_count))
    if not selections:
        parser.error("no extra-vertex selections exist")

    started = time.monotonic()
    records: list[dict[str, object] | None] = [None] * len(selections)
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=args.jobs
    ) as executor:
        futures = {
            executor.submit(
                solve_boundary,
                str(args.base_graph.resolve()),
                args.conflict_vertices,
                extra_vertices,
                args.solver,
                args.conflict_budget,
            ): index
            for index, extra_vertices in enumerate(selections)
        }
        for future in concurrent.futures.as_completed(futures):
            index = futures[future]
            records[index] = future.result()

    complete = [record for record in records if record is not None]
    args.candidate_dir.mkdir(parents=True, exist_ok=True)
    candidates: list[dict[str, object]] = []
    for index, record in enumerate(complete, start=1):
        if record["status"] != "SAT":
            continue
        graph6 = str(record["graph6"])
        path = args.candidate_dir / f"boundary_{index:03d}.g6"
        if path.exists():
            raise SystemExit(f"refusing to overwrite candidate {path}")
        path.write_text(graph6 + "\n", encoding="ascii", newline="\n")
        candidates.append(
            {
                "selection_index_one_based": index,
                "extra_vertices": record["extra_vertices"],
                "path": str(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "graph6": graph6,
            }
        )

    statuses = [str(record["status"]) for record in complete]
    result = {
        "pilot": PILOT_ID,
        "base_graph_path": str(args.base_graph),
        "base_graph_sha256": hashlib.sha256(
            args.base_graph.read_bytes()
        ).hexdigest(),
        "base_graph6": encode_graph6(adjacency),
        "order": order,
        "conflict_vertices": list(args.conflict_vertices),
        "extra_count": args.extra_count,
        "selection_count": len(selections),
        "selection_coverage_exact": [
            tuple(record["extra_vertices"]) for record in complete
        ]
        == list(selections),
        "solver": args.solver,
        "pysat_version": pysat.__version__,
        "conflict_budget_per_instance": args.conflict_budget,
        "jobs": args.jobs,
        "sat_count": statuses.count("SAT"),
        "unsat_count": statuses.count("UNSAT"),
        "budget_exhausted_count": statuses.count("BUDGET_EXHAUSTED"),
        "wall_seconds": time.monotonic() - started,
        "candidate_records": candidates,
        "records": complete,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise SystemExit(f"refusing to overwrite result {args.output}")
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "pilot": PILOT_ID,
                "sat_count": result["sat_count"],
                "unsat_count": result["unsat_count"],
                "budget_exhausted_count": result["budget_exhausted_count"],
                "wall_seconds": result["wall_seconds"],
                "result": str(args.output),
            },
            sort_keys=True,
        )
    )
    return 10 if candidates else 0


if __name__ == "__main__":
    raise SystemExit(main())
