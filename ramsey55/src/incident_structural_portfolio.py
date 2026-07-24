#!/usr/bin/env python3
"""Preregister and run exact 9--12-vertex incident-boundary completions.

The two inputs are fixed representatives of the two complement-isomorphism
classes in the retained 22-graph E=2 corpus.  Every boundary contains the
six-vertex union of the representative's two forbidden five-sets.  Two
deterministic nested expansion sequences add three through six vertices:

* ``near_pressure`` greedily covers one-edge-away homogeneous five-sets that
  are disjoint from the conflict union; and
* ``row_diversity`` starts at the largest near-conflict load and then greedily
  maximizes adjacency-row distance from the already selected extra vertices.

All other edges are pinned to the representative.  SAT therefore supplies a
full Ramsey(5,5;43) graph.  Negative solver returns carry no proof and are
reported only as fixed-boundary observations.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable, Sequence

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


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PLAN = "ramsey55.incident_structural_portfolio_plan.v1"
SCHEMA_RESULT = "ramsey55.incident_structural_portfolio_result.v1"
SCHEMA_SHARD = "ramsey55.incident_structural_portfolio_shard.v1"
BOUNDARY_SIZES = (9, 10, 11, 12)
BUDGET_BY_SIZE = {9: 400_000, 10: 300_000, 11: 200_000, 12: 150_000}
REPRESENTATIVES = (
    {
        "class_id": "class01",
        "catalog_line": 1,
        "path": "results/constructive/catalog_seed_search_stratified_v1/line_001.g6",
        "sha256": "c168d89376f939653c4a7d1f9da4c5800fb9379bf2c4a5cd7db226fce8789a85",
        "expected_colour": "independent",
    },
    {
        "class_id": "class02",
        "catalog_line": 2,
        "path": "results/constructive/catalog_seed_search_stratified_v1/line_002.g6",
        "sha256": "4e18e027c3211898569ae8a2113ff6e62c1bffd6bb9d2f413930225109547da4",
        "expected_colour": "clique",
    },
)
SOLVER_CLASSES = {
    name: getattr(solvers, name)
    for name in ("Glucose3", "MapleChrono")
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def write_new_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    path.write_text(
        json.dumps(value, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def homogeneous_and_near_sets(
    adjacency: Sequence[int],
) -> tuple[
    tuple[tuple[tuple[int, ...], int], ...],
    tuple[tuple[int, ...], ...],
]:
    homogeneous: list[tuple[tuple[int, ...], int]] = []
    near: list[tuple[int, ...]] = []
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        if edge_count in (0, 10):
            homogeneous.append((vertices, edge_count))
        if edge_count in (1, 9):
            near.append(vertices)
    return tuple(homogeneous), tuple(near)


def conflict_geometry(
    adjacency: Sequence[int], expected_colour: str
) -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...]]:
    homogeneous, _ = homogeneous_and_near_sets(adjacency)
    if len(homogeneous) != 2:
        raise ValueError("representative is not exactly E=2")
    edge_counts = {edge_count for _, edge_count in homogeneous}
    expected_count = 0 if expected_colour == "independent" else 10
    if edge_counts != {expected_count}:
        raise ValueError("representative has the wrong conflict colour")
    sets = tuple(vertices for vertices, _ in homogeneous)
    if len(set(sets[0]) & set(sets[1])) != 4:
        raise ValueError("the two conflicts do not overlap in four vertices")
    union = tuple(sorted(set(sets[0]) | set(sets[1])))
    if len(union) != 6:
        raise AssertionError("four-overlap conflict union is not six vertices")
    return sets, union


def near_loads(
    near: Sequence[tuple[int, ...]], vertices: Iterable[int]
) -> dict[int, int]:
    return {
        vertex: sum(vertex in subset for subset in near)
        for vertex in vertices
    }


def pressure_sequence(
    near: Sequence[tuple[int, ...]],
    conflict_union: Sequence[int],
    order: int,
    count: int = 6,
) -> tuple[tuple[int, ...], tuple[dict[str, int], ...]]:
    conflict = frozenset(conflict_union)
    candidates = tuple(vertex for vertex in range(order) if vertex not in conflict)
    loads = near_loads(near, candidates)
    uncovered = [frozenset(subset) for subset in near if conflict.isdisjoint(subset)]
    selected: list[int] = []
    trace: list[dict[str, int]] = []
    while len(selected) < count:
        scores = {
            vertex: sum(vertex in subset for subset in uncovered)
            for vertex in candidates
            if vertex not in selected
        }
        vertex = max(
            scores,
            key=lambda candidate: (
                scores[candidate],
                loads[candidate],
                -candidate,
            ),
        )
        trace.append(
            {
                "vertex": vertex,
                "new_near_sets_covered": scores[vertex],
                "total_near_load": loads[vertex],
                "uncovered_before": len(uncovered),
            }
        )
        selected.append(vertex)
        uncovered = [subset for subset in uncovered if vertex not in subset]
    return tuple(selected), tuple(trace)


def row_distance(
    adjacency: Sequence[int], left: int, right: int
) -> int:
    return (adjacency[left] ^ adjacency[right]).bit_count()


def row_diversity_sequence(
    adjacency: Sequence[int],
    near: Sequence[tuple[int, ...]],
    conflict_union: Sequence[int],
    count: int = 6,
) -> tuple[tuple[int, ...], tuple[dict[str, int], ...]]:
    conflict = frozenset(conflict_union)
    candidates = tuple(
        vertex for vertex in range(len(adjacency)) if vertex not in conflict
    )
    loads = near_loads(near, candidates)
    selected: list[int] = []
    trace: list[dict[str, int]] = []
    while len(selected) < count:
        available = tuple(vertex for vertex in candidates if vertex not in selected)
        if not selected:
            vertex = max(
                available,
                key=lambda candidate: (
                    loads[candidate],
                    -abs(adjacency[candidate].bit_count() - 21),
                    -candidate,
                ),
            )
            minimum_distance = 0
        else:
            minimum_by_vertex = {
                candidate: min(
                    row_distance(adjacency, candidate, prior)
                    for prior in selected
                )
                for candidate in available
            }
            signatures = {
                candidate: tuple(
                    (adjacency[candidate] >> core_vertex) & 1
                    for core_vertex in conflict_union
                )
                for candidate in candidates
            }
            old_signatures = {signatures[prior] for prior in selected}
            vertex = max(
                available,
                key=lambda candidate: (
                    minimum_by_vertex[candidate],
                    int(signatures[candidate] not in old_signatures),
                    loads[candidate],
                    -candidate,
                ),
            )
            minimum_distance = minimum_by_vertex[vertex]
        trace.append(
            {
                "vertex": vertex,
                "minimum_row_distance": minimum_distance,
                "total_near_load": loads[vertex],
                "degree": adjacency[vertex].bit_count(),
            }
        )
        selected.append(vertex)
    return tuple(selected), tuple(trace)


def free_edge_count(order: int, boundary_size: int) -> int:
    return boundary_size * order - boundary_size * (boundary_size + 1) // 2


def solver_for(class_id: str, policy: str) -> str:
    if (class_id, policy) in (
        ("class01", "near_pressure"),
        ("class02", "row_diversity"),
    ):
        return "MapleChrono"
    return "Glucose3"


def dependency_records() -> list[dict[str, object]]:
    paths = [
        Path(__file__).resolve(),
        ROOT / "src" / "residual_lns_sat.py",
        ROOT / "src" / "graph_io.py",
        ROOT / "verify" / "exhaustive_verify.py",
        ROOT / "build" / "bitset_verify",
        Path(pysat.__file__).resolve(),
    ]
    try:
        import pysolvers

        paths.append(Path(pysolvers.__file__).resolve())
    except ImportError:
        pass
    return [
        {
            "path": (
                str(path.relative_to(ROOT))
                if path.is_relative_to(ROOT)
                else str(path)
            ),
            "sha256": sha256_file(path),
        }
        for path in paths
    ]


def build_plan() -> dict[str, object]:
    representatives: list[dict[str, object]] = []
    instances: list[dict[str, object]] = []
    for representative in REPRESENTATIVES:
        path = ROOT / str(representative["path"])
        if sha256_file(path) != representative["sha256"]:
            raise ValueError(f"representative hash mismatch: {path}")
        adjacency = read_graph(path)
        validate_simple(adjacency)
        homogeneous, near = homogeneous_and_near_sets(adjacency)
        conflict_sets, conflict_union = conflict_geometry(
            adjacency, str(representative["expected_colour"])
        )
        pressure, pressure_trace = pressure_sequence(
            near, conflict_union, len(adjacency)
        )
        diversity, diversity_trace = row_diversity_sequence(
            adjacency, near, conflict_union
        )
        sequences = {
            "near_pressure": {
                "vertices": list(pressure),
                "trace": list(pressure_trace),
            },
            "row_diversity": {
                "vertices": list(diversity),
                "trace": list(diversity_trace),
            },
        }
        representatives.append(
            {
                **representative,
                "order": len(adjacency),
                "edge_count": sum(row.bit_count() for row in adjacency) // 2,
                "conflict_sets": [list(vertices) for vertices in conflict_sets],
                "conflict_union": list(conflict_union),
                "near_homogeneous_five_set_count": len(near),
                "selection_sequences": sequences,
            }
        )
        for policy, sequence in (
            ("near_pressure", pressure),
            ("row_diversity", diversity),
        ):
            for boundary_size in BOUNDARY_SIZES:
                extra_count = boundary_size - len(conflict_union)
                boundary = tuple(sorted(conflict_union + sequence[:extra_count]))
                instances.append(
                    {
                        "instance_id": (
                            f"{representative['class_id']}_{policy}_"
                            f"k{boundary_size:02d}"
                        ),
                        "class_id": representative["class_id"],
                        "base_graph": representative["path"],
                        "base_graph_sha256": representative["sha256"],
                        "policy": policy,
                        "boundary_size": boundary_size,
                        "conflict_union": list(conflict_union),
                        "extra_vertices": list(sequence[:extra_count]),
                        "incident_vertices": list(boundary),
                        "free_edge_count": free_edge_count(
                            len(adjacency), boundary_size
                        ),
                        "solver": solver_for(
                            str(representative["class_id"]), policy
                        ),
                        "conflict_budget": BUDGET_BY_SIZE[boundary_size],
                    }
                )
    return {
        "schema": SCHEMA_PLAN,
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "PREREGISTERED_BEFORE_PRODUCTION_RUN",
        "question": (
            "Does any of sixteen deterministic exact incident-boundary "
            "completions around the two retained E=2 complement-class "
            "representatives contain a Ramsey(5,5;43) graph?"
        ),
        "scope": {
            "representative_count": 2,
            "policies": ["near_pressure", "row_diversity"],
            "boundary_sizes": list(BOUNDARY_SIZES),
            "instance_count": len(instances),
            "fixed_edge_rule": (
                "Every edge with neither endpoint in incident_vertices equals "
                "the named representative."
            ),
            "free_edge_rule": (
                "Every edge with at least one endpoint in incident_vertices "
                "is a Boolean completion variable."
            ),
            "selection_rule": (
                "Sequences are computed exactly by the pinned generator: "
                "near_pressure greedily covers near-homogeneous five-sets "
                "disjoint from the six-vertex conflict union; row_diversity "
                "greedily maximizes full adjacency-row Hamming distance."
            ),
        },
        "resources": {
            "jobs": 1,
            "conflict_budget_by_boundary_size": {
                str(key): value for key, value in BUDGET_BY_SIZE.items()
            },
            "proof_logging": False,
            "resume_shards": True,
        },
        "solver_environment": {
            "pysat_version": pysat.__version__,
            "python_executable": sys.executable,
        },
        "representatives": representatives,
        "instances": instances,
        "pinned_files": dependency_records(),
        "outcome_policy": {
            "SAT": (
                "Export graph6 immediately and require embedded exhaustive "
                "five-set enumeration plus standalone Python exhaustive and "
                "C++ recursive-bitset verifiers all to accept."
            ),
            "UNSAT": (
                "Record only a reproducible non-proof-carrying observation "
                "about this exact fixed boundary."
            ),
            "BUDGET_EXHAUSTED": (
                "Record unresolved; this is neither SAT nor UNSAT."
            ),
            "all_negative": (
                "No finite fixed-boundary portfolio proves global "
                "nonexistence or changes an R(5,5) bound."
            ),
        },
    }


def formula_sha256(
    free_edges: Sequence[tuple[int, int]],
    clauses: Sequence[Sequence[int]],
) -> str:
    digest = hashlib.sha256()
    digest.update(f"p cnf {len(free_edges)} {len(clauses)}\n".encode("ascii"))
    for left, right in free_edges:
        digest.update(f"e {left} {right}\n".encode("ascii"))
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return digest.hexdigest()


def run_external_verifier(command: Sequence[str]) -> dict[str, object]:
    started = time.monotonic()
    completed = subprocess.run(
        list(command),
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    parsed: object | None = None
    if completed.stdout.strip():
        try:
            parsed = json.loads(completed.stdout.strip().splitlines()[-1])
        except json.JSONDecodeError:
            parsed = None
    return {
        "command": list(command),
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "wall_seconds": time.monotonic() - started,
        "json": parsed,
    }


def solve_instance(
    plan_sha256: str,
    instance: dict[str, object],
    candidate_dir: Path,
) -> dict[str, object]:
    started = time.monotonic()
    base_path = ROOT / str(instance["base_graph"])
    adjacency = read_graph(base_path)
    incident = tuple(int(vertex) for vertex in instance["incident_vertices"])
    free_edges = neighborhood_edges(
        len(adjacency), (), (), incident_vertices=incident
    )
    if len(free_edges) != instance["free_edge_count"]:
        raise AssertionError("plan free-edge count mismatch")
    build_started = time.monotonic()
    formula = build_residual_lns_instance(adjacency, free_edges)
    build_seconds = time.monotonic() - build_started
    clauses = formula.clauses
    solver_name = str(instance["solver"])
    solver_class = SOLVER_CLASSES[solver_name]
    solve_started = time.monotonic()
    with solver_class(bootstrap_with=clauses, use_timer=True) as solver:
        solver.conf_budget(int(instance["conflict_budget"]))
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
        "schema": SCHEMA_SHARD,
        "plan_sha256": plan_sha256,
        "instance": instance,
        "status": status,
        "evidence_label": (
            "CERTIFIED_CONSTRUCTION"
            if status == "SAT"
            else "REPRODUCIBLE_COMPUTATIONAL_OBSERVATION"
            if status == "UNSAT"
            else "UNRESOLVED"
        ),
        "variable_count": formula.variable_count,
        "clique_clause_count": len(formula.clique_clauses),
        "independent_clause_count": len(formula.independent_clauses),
        "clause_count": len(clauses),
        "formula_stream_sha256": formula_sha256(free_edges, clauses),
        "build_seconds": build_seconds,
        "solve_seconds": solve_seconds,
        "solver_cpu_seconds": solver_cpu_seconds,
        "wall_seconds": time.monotonic() - started,
        "solver_stats": stats,
        "candidate": None,
    }
    if status == "SAT":
        if model is None:
            raise AssertionError("SAT solver returned no model")
        values = {abs(literal): literal > 0 for literal in model}
        assignment = tuple(
            values.get(variable, False)
            for variable in range(1, formula.variable_count + 1)
        )
        if not formula_is_satisfied(clauses, assignment):
            raise AssertionError("solver model does not satisfy boundary formula")
        completed = apply_assignment(adjacency, free_edges, assignment)
        direct_counts = count_forbidden_sets(completed)
        if direct_counts != (0, 0):
            raise AssertionError("solver model is not a Ramsey graph")
        candidate_dir.mkdir(parents=True, exist_ok=True)
        candidate_path = candidate_dir / f"{instance['instance_id']}.g6"
        graph6 = encode_graph6(completed)
        payload = (graph6 + "\n").encode("ascii")
        if candidate_path.exists():
            if candidate_path.read_bytes() != payload:
                raise FileExistsError(
                    f"refusing to overwrite different candidate {candidate_path}"
                )
        else:
            candidate_path.write_bytes(payload)
        python_check = run_external_verifier(
            [
                sys.executable,
                str(ROOT / "verify" / "exhaustive_verify.py"),
                str(candidate_path),
                "--k",
                "5",
            ]
        )
        bitset_check = run_external_verifier(
            [
                str(ROOT / "build" / "bitset_verify"),
                str(candidate_path),
                "--k",
                "5",
            ]
        )
        if (
            python_check["returncode"] != 0
            or not isinstance(python_check["json"], dict)
            or not python_check["json"].get("valid")
            or bitset_check["returncode"] != 0
            or not isinstance(bitset_check["json"], dict)
            or not bitset_check["json"].get("valid")
        ):
            raise AssertionError("standalone candidate verification failed")
        record["candidate"] = {
            "path": str(candidate_path.relative_to(ROOT)),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "graph6": graph6,
            "true_variables": [
                variable
                for variable, value in enumerate(assignment, 1)
                if value
            ],
            "embedded_exhaustive_counts": list(direct_counts),
            "python_exhaustive_verifier": python_check,
            "cpp_recursive_bitset_verifier": bitset_check,
            "independently_verified": True,
        }
    return record


def pinned_files_match(plan: dict[str, object]) -> bool:
    for record in plan["pinned_files"]:
        raw_path = Path(str(record["path"]))
        path = raw_path if raw_path.is_absolute() else ROOT / raw_path
        if not path.is_file() or sha256_file(path) != record["sha256"]:
            return False
    return True


def run_plan(
    plan_path: Path,
    result_path: Path,
    work_dir: Path,
    candidate_dir: Path,
) -> dict[str, object]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("schema") != SCHEMA_PLAN:
        raise ValueError("unexpected plan schema")
    if plan.get("status") != "PREREGISTERED_BEFORE_PRODUCTION_RUN":
        raise ValueError("plan was not preregistered")
    if not pinned_files_match(plan):
        raise ValueError("a pinned production file changed after preregistration")
    if result_path.exists():
        raise FileExistsError(f"refusing to overwrite {result_path}")
    plan_digest = sha256_file(plan_path)
    work_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    started = time.monotonic()
    for instance in plan["instances"]:
        shard_path = work_dir / f"{instance['instance_id']}.json"
        if shard_path.exists():
            record = json.loads(shard_path.read_text(encoding="utf-8"))
            if (
                record.get("schema") != SCHEMA_SHARD
                or record.get("plan_sha256") != plan_digest
                or record.get("instance") != instance
            ):
                raise ValueError(f"stale or mismatched shard {shard_path}")
        else:
            record = solve_instance(plan_digest, instance, candidate_dir)
            write_new_json(shard_path, record)
        records.append(record)
        print(
            json.dumps(
                {
                    "instance_id": instance["instance_id"],
                    "status": record["status"],
                    "conflicts": record["solver_stats"].get("conflicts"),
                    "solve_seconds": record["solve_seconds"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if record["status"] == "SAT":
            break
    statuses = [str(record["status"]) for record in records]
    certified = any(
        record["status"] == "SAT"
        and isinstance(record.get("candidate"), dict)
        and record["candidate"].get("independently_verified")
        for record in records
    )
    result = {
        "schema": SCHEMA_RESULT,
        "plan": str(plan_path.relative_to(ROOT)),
        "plan_sha256": plan_digest,
        "production_started_after_plan_mtime": (
            min(
                (work_dir / f"{record['instance']['instance_id']}.json").stat().st_mtime
                for record in records
            )
            >= plan_path.stat().st_mtime
        ),
        "planned_instance_count": len(plan["instances"]),
        "completed_instance_count": len(records),
        "complete": len(records) == len(plan["instances"]) or certified,
        "sat_count": statuses.count("SAT"),
        "unsat_observation_count": statuses.count("UNSAT"),
        "budget_exhausted_count": statuses.count("BUDGET_EXHAUSTED"),
        "certified_construction": certified,
        "wall_seconds": time.monotonic() - started,
        "records": records,
        "claim_boundary": (
            "Only a SAT record accepted by all three graph checks is a "
            "certified construction. UNSAT records have no proof and are only "
            "fixed-boundary observations; budget exhaustion is unresolved. "
            "An all-negative finite portfolio is not global nonexistence."
        ),
    }
    write_new_json(result_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--make-plan", type=Path)
    actions.add_argument("--run", type=Path, metavar="PLAN")
    parser.add_argument("--result", type=Path)
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--candidate-dir", type=Path)
    args = parser.parse_args()
    if args.make_plan is not None:
        plan = build_plan()
        write_new_json(args.make_plan, plan)
        print(
            json.dumps(
                {
                    "schema": plan["schema"],
                    "instance_count": len(plan["instances"]),
                    "output": str(args.make_plan),
                    "sha256": sha256_file(args.make_plan),
                },
                sort_keys=True,
            )
        )
        return 0
    if args.result is None or args.work_dir is None or args.candidate_dir is None:
        parser.error("--run requires --result, --work-dir, and --candidate-dir")
    result = run_plan(
        args.run.resolve(),
        args.result.resolve(),
        args.work_dir.resolve(),
        args.candidate_dir.resolve(),
    )
    print(
        json.dumps(
            {
                "schema": result["schema"],
                "complete": result["complete"],
                "sat_count": result["sat_count"],
                "unsat_observation_count": result["unsat_observation_count"],
                "budget_exhausted_count": result["budget_exhausted_count"],
                "result": str(args.result),
            },
            sort_keys=True,
        )
    )
    return 10 if result["certified_construction"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
