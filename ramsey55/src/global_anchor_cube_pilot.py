#!/usr/bin/env python3
"""Proof-free selector-cube pilot for the exact degree-18/19/20 covers.

Each checked union formula has 143 anchor-matrix selector variables.  This
worker solves the formula once under each positive selector assumption.  A
solver instance is persistent within one degree branch, so learned clauses
are shared between that branch's 143 calls; per-call conflict deltas are
reported, but they are not independent timing samples.

Negative outcomes are deliberately labelled as unproved observations.  A SAT
outcome is replayed against every DIMACS clause, decoded to all 903 graph-edge
variables, and accepted only after both independent Ramsey verifiers agree.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import inspect
import json
import os
import resource
import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Iterable

import pysat
from pysat.formula import CNF
from pysat import solvers as pysat_solvers

from graph_io import encode_graph6


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "verify"
ORDER = 43
PRIMARY_VARIABLE_COUNT = 903
SELECTOR_VARIABLE_FIRST = 65_404
SELECTOR_COUNT = 143
WORKER_ID = "ramsey55_global_anchor_selector_cube_pilot_v1"
ALLOWED_SOLVERS = ("MapleChrono", "Cadical195")
ALLOWED_STATUSES = (
    "SAT",
    "OBSERVED_UNSAT_UNCHECKED",
    "BUDGET_EXHAUSTED",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def sha256_json_object(value: object) -> str:
    return hashlib.sha256(
        (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode(
            "utf-8"
        )
    ).hexdigest()


def selector_assumption_sha256(selector: int) -> str:
    return hashlib.sha256(f"{selector} 0\n".encode("ascii")).hexdigest()


def edge_variable(left: int, right: int) -> int:
    if left > right:
        left, right = right, left
    if not 0 <= left < right < ORDER:
        raise ValueError("invalid edge")
    return 1 + left * (2 * ORDER - left - 1) // 2 + right - left - 1


def decode_primary_model(model: Iterable[int]) -> list[int]:
    truth = {abs(literal): literal > 0 for literal in model}
    missing = [
        variable
        for variable in range(1, PRIMARY_VARIABLE_COUNT + 1)
        if variable not in truth
    ]
    if missing:
        raise ValueError(f"model omits primary variable {missing[0]}")
    adjacency = [0] * ORDER
    for left in range(ORDER):
        for right in range(left + 1, ORDER):
            if truth[edge_variable(left, right)]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
    return adjacency


def replay_dimacs_model(
    cnf_path: Path, model: Iterable[int], required_assumptions: Iterable[int]
) -> tuple[int, int]:
    """Stream-check a total model against the exact CNF and assumptions."""

    truth: dict[int, bool] = {}
    for literal in model:
        variable = abs(literal)
        if variable == 0:
            raise ValueError("model contains literal zero")
        value = literal > 0
        if variable in truth and truth[variable] != value:
            raise ValueError(f"model assigns variable {variable} twice")
        truth[variable] = value

    for literal in required_assumptions:
        value = truth.get(abs(literal))
        if value is None or value != (literal > 0):
            raise ValueError(f"model violates assumption {literal}")

    header_variables: int | None = None
    header_clauses: int | None = None
    clauses_seen = 0
    pending: list[int] = []
    pending_satisfied = False
    with cnf_path.open("r", encoding="ascii") as source:
        for line_number, raw_line in enumerate(source, start=1):
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("c"):
                continue
            if stripped.startswith("p"):
                fields = stripped.split()
                if (
                    len(fields) != 4
                    or fields[0] != "p"
                    or fields[1] != "cnf"
                    or header_variables is not None
                ):
                    raise ValueError(f"malformed DIMACS header on line {line_number}")
                header_variables = int(fields[2])
                header_clauses = int(fields[3])
                continue
            if header_variables is None:
                raise ValueError("DIMACS clause precedes header")
            for token in stripped.split():
                literal = int(token)
                if literal == 0:
                    if not pending:
                        raise ValueError(f"empty clause on line {line_number}")
                    clauses_seen += 1
                    if not pending_satisfied:
                        raise ValueError(
                            f"model falsifies DIMACS clause {clauses_seen}"
                        )
                    pending.clear()
                    pending_satisfied = False
                    continue
                if abs(literal) > header_variables:
                    raise ValueError(
                        f"literal outside DIMACS header on line {line_number}"
                    )
                pending.append(literal)
                value = truth.get(abs(literal))
                if value is None:
                    raise ValueError(f"model omits CNF variable {abs(literal)}")
                if value == (literal > 0):
                    pending_satisfied = True
    if pending:
        raise ValueError("unterminated final DIMACS clause")
    if header_variables is None or header_clauses is None:
        raise ValueError("missing DIMACS header")
    if clauses_seen != header_clauses:
        raise ValueError(
            f"DIMACS clause count mismatch: {clauses_seen} != {header_clauses}"
        )
    return header_variables, clauses_seen


def forbidden_counts(adjacency: list[int]) -> tuple[int, int]:
    sys.path.insert(0, str(VERIFY))
    from exhaustive_verify import count_forbidden

    return count_forbidden(adjacency, 5)


def atomic_write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} does not contain a JSON object")
    return value


def branch_from_plan(plan: dict[str, object], degree: int) -> dict[str, object]:
    if degree == 18:
        if plan.get("degree") != 18:
            raise ValueError("degree-18 plan has the wrong branch")
        return plan
    branches = plan.get("branches")
    if not isinstance(branches, list):
        raise ValueError("degree-19/20 plan omits branches")
    matches = [
        branch
        for branch in branches
        if isinstance(branch, dict) and branch.get("degree") == degree
    ]
    if len(matches) != 1:
        raise ValueError(f"plan does not have one degree-{degree} branch")
    return matches[0]


def cube_schedule(branch: dict[str, object], degree: int) -> list[dict[str, object]]:
    cubes = branch.get("cubes")
    if not isinstance(cubes, list) or len(cubes) != SELECTOR_COUNT:
        raise ValueError(f"degree-{degree} branch does not have 143 cubes")
    result: list[dict[str, object]] = []
    for index, cube in enumerate(cubes):
        if not isinstance(cube, dict):
            raise ValueError("cube record is not an object")
        expected_id = f"d{degree}_m{index:03d}"
        if cube.get("cube_index") != index or cube.get("cube_id") != expected_id:
            raise ValueError(f"malformed cube ordering at {expected_id}")
        selector = SELECTOR_VARIABLE_FIRST + index
        result.append(
            {
                "degree": degree,
                "cube_index": index,
                "cube_id": expected_id,
                "matrix_integer": cube.get("matrix_integer"),
                "matrix_hex": cube.get("matrix_hex"),
                "matrix_edge_count": cube.get("matrix_edge_count"),
                "matrix_orbit_size": cube.get("matrix_orbit_size"),
                "full_cube_assumption_count": cube.get("assumption_count"),
                "full_cube_assumptions_sha256": cube.get("assumptions_sha256"),
                "selector": selector,
                "selector_assumption_sha256": selector_assumption_sha256(selector),
            }
        )
    return result


def current_rss_bytes() -> int:
    # ru_maxrss is bytes on macOS (and KiB on Linux).
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value * 1024 if sys.platform.startswith("linux") else value)


def process_table() -> str:
    completed = subprocess.run(
        ["ps", "-axo", "pid=,command="],
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    return completed.stdout


def validate_launch_gates(plan: dict[str, object]) -> dict[str, object]:
    gates = plan.get("resource_gates")
    if not isinstance(gates, dict):
        raise ValueError("plan omits resource_gates")
    disk_path = Path(str(gates["disk_path"]))
    minimum_free = int(gates["minimum_free_disk_bytes"])
    free = shutil.disk_usage(disk_path).free
    if free < minimum_free:
        raise RuntimeError(
            f"free-disk gate failed: {free} < {minimum_free} bytes"
        )
    prohibited = gates.get("prohibited_process_substrings", [])
    if not isinstance(prohibited, list):
        raise ValueError("prohibited_process_substrings is not a list")
    table = process_table()
    found = [text for text in prohibited if str(text) in table]
    if found:
        raise RuntimeError(
            "process-pressure gate failed; active substring(s): "
            + ", ".join(map(str, found))
        )
    return {
        "disk_path": str(disk_path.resolve()),
        "free_disk_bytes": free,
        "minimum_free_disk_bytes": minimum_free,
        "prohibited_process_substrings": prohibited,
        "prohibited_processes_found": [],
        "launch_valid": True,
    }


def verify_input_hashes(plan: dict[str, object]) -> None:
    inputs = plan.get("inputs")
    if not isinstance(inputs, list):
        raise ValueError("plan omits inputs")
    for record in inputs:
        if not isinstance(record, dict):
            raise ValueError("input record is not an object")
        path = Path(str(record["path"]))
        actual = sha256_file(path)
        if actual != record.get("sha256"):
            raise ValueError(f"input SHA-256 mismatch: {path}")


def verify_worker_binding(plan: dict[str, object]) -> None:
    expected = plan.get("worker_source_sha256")
    actual = sha256_file(Path(__file__))
    if expected != actual:
        raise ValueError("worker source SHA-256 does not match frozen plan")


def construction_record(
    *,
    degree: int,
    cube: dict[str, object],
    model: list[int],
    cnf_path: Path,
    candidate_path: Path,
    cpp_verifier: Path,
) -> dict[str, object]:
    variables, clauses = replay_dimacs_model(
        cnf_path, model, [int(cube["selector"])]
    )
    adjacency = decode_primary_model(model)
    counts = forbidden_counts(adjacency)
    if counts != (0, 0):
        raise AssertionError(f"SAT graph has forbidden counts {counts}")
    graph6 = encode_graph6(adjacency) + "\n"
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(graph6, encoding="ascii")
    cpp = subprocess.run(
        [str(cpp_verifier), str(candidate_path)],
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    if cpp.returncode != 0:
        raise AssertionError(
            "independent C++ verifier rejected SAT graph: "
            + cpp.stdout
            + cpp.stderr
        )
    return {
        "degree": degree,
        "cube_id": cube["cube_id"],
        "cube_index": cube["cube_index"],
        "selector": cube["selector"],
        "union_cnf_model_replay": True,
        "replayed_variable_count": variables,
        "replayed_clause_count": clauses,
        "python_forbidden_clique5_count": counts[0],
        "python_forbidden_independent5_count": counts[1],
        "cpp_verifier_returncode": cpp.returncode,
        "cpp_verifier_stdout": cpp.stdout.strip(),
        "candidate_path": str(candidate_path.resolve()),
        "graph6": graph6.strip(),
        "graph6_sha256": hashlib.sha256(graph6.encode("ascii")).hexdigest(),
        "model_literal_count": len(model),
        "model_true_variables": sorted(
            literal for literal in model if literal > 0
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()

    frozen = load_json(args.plan)
    if frozen.get("schema") != "ramsey55.global_anchor_selector_cube_pilot.v1":
        raise SystemExit("unexpected frozen plan schema")
    if frozen.get("status") != "FROZEN_BEFORE_RUN":
        raise SystemExit("pilot plan is not frozen")
    verify_worker_binding(frozen)
    verify_input_hashes(frozen)
    launch_gates = validate_launch_gates(frozen)

    solver_name = str(frozen["solver"])
    if solver_name not in ALLOWED_SOLVERS:
        raise SystemExit("unsupported solver in plan")
    conflict_budget = int(frozen["conflict_budget_per_cube"])
    if conflict_budget <= 0:
        raise SystemExit("nonpositive conflict budget")
    maximum_rss = int(frozen["resource_gates"]["maximum_worker_rss_bytes"])
    solver_class = getattr(pysat_solvers, solver_name)
    branch_records = frozen.get("branches")
    if not isinstance(branch_records, list) or len(branch_records) != 3:
        raise SystemExit("plan must specify three branches")

    started = time.monotonic()
    records: list[dict[str, object]] = []
    status_counts: Counter[str] = Counter()
    total_conflicts = 0
    total_decisions = 0
    total_propagations = 0
    construction: dict[str, object] | None = None
    result: dict[str, object] = {
        "schema": "ramsey55.global_anchor_selector_cube_pilot_result.v1",
        "worker": WORKER_ID,
        "evidence_label": "PROOF-FREE CONSTRUCTION SEARCH",
        "claim_boundary": (
            "A SAT result is accepted only after exact union-CNF replay and "
            "two independent full-graph Ramsey verifiers. False and budget "
            "outcomes have no proof and exclude no cube or degree branch."
        ),
        "plan_path": str(args.plan.resolve()),
        "plan_sha256": sha256_file(args.plan),
        "worker_source_sha256": sha256_file(Path(__file__)),
        "solver": solver_name,
        "solver_class_source": inspect.getfile(solver_class),
        "pysat_version": pysat.__version__,
        "proof_logging": False,
        "conflict_budget_per_cube": conflict_budget,
        "persistent_solver_within_branch": True,
        "cross_branch_learned_clause_reuse": False,
        "measurement_caveat": (
            "Learned clauses are shared by the 143 selector calls within "
            "each branch. Conflict deltas are exact, but later records are "
            "not fresh-solver timing samples."
        ),
        "launch_gates": launch_gates,
        "maximum_worker_rss_bytes": maximum_rss,
        "maximum_resident_set_bytes": current_rss_bytes(),
        "records": records,
        "status_counts": {},
        "completed_cube_count": 0,
        "scheduled_cube_count": 3 * SELECTOR_COUNT,
        "total_conflicts": 0,
        "total_decisions": 0,
        "total_propagations": 0,
        "elapsed_seconds": 0.0,
        "construction": None,
        "scheduled_complete": False,
        "full_cover_screened": False,
        "negative_certified": False,
    }
    atomic_write_json(args.result, result)

    for branch_position, branch_spec in enumerate(branch_records):
        if not isinstance(branch_spec, dict):
            raise SystemExit("branch specification is not an object")
        degree = int(branch_spec["degree"])
        union_cnf = Path(str(branch_spec["union_cnf"]))
        cover_plan_path = Path(str(branch_spec["cover_plan"]))
        cover_plan = load_json(cover_plan_path)
        cover_branch = branch_from_plan(cover_plan, degree)
        schedule = cube_schedule(cover_branch, degree)
        if sha256_json_object(schedule) != branch_spec.get("schedule_sha256"):
            raise SystemExit(f"degree-{degree} schedule hash mismatch")

        setup_started = time.monotonic()
        formula = CNF(from_file=str(union_cnf))
        expected_variables = int(branch_spec["variable_count"])
        expected_clauses = int(branch_spec["clause_count"])
        if formula.nv != expected_variables or len(formula.clauses) != expected_clauses:
            raise AssertionError(f"degree-{degree} union formula count mismatch")
        solver = solver_class(bootstrap_with=formula.clauses, use_timer=True)
        del formula
        gc.collect()
        setup_seconds = time.monotonic() - setup_started

        rss = current_rss_bytes()
        if rss > maximum_rss:
            solver.delete()
            raise RuntimeError(f"worker RSS gate failed: {rss} > {maximum_rss}")

        for cube_position, cube in enumerate(schedule):
            selector = int(cube["selector"])
            before = solver.accum_stats()
            cube_started = time.monotonic()
            solver.conf_budget(conflict_budget)
            outcome = solver.solve_limited(assumptions=[selector])
            after = solver.accum_stats()
            elapsed = time.monotonic() - cube_started
            conflicts = after.get("conflicts", 0) - before.get("conflicts", 0)
            decisions = after.get("decisions", 0) - before.get("decisions", 0)
            propagations = (
                after.get("propagations", 0) - before.get("propagations", 0)
            )
            status = (
                "SAT"
                if outcome is True
                else "OBSERVED_UNSAT_UNCHECKED"
                if outcome is False
                else "BUDGET_EXHAUSTED"
            )
            if status not in ALLOWED_STATUSES:
                raise AssertionError("unexpected solve status")
            record = {
                **cube,
                "branch_schedule_position": branch_position,
                "cube_schedule_position": cube_position,
                "branch_solver_setup_seconds": (
                    setup_seconds if cube_position == 0 else None
                ),
                "status": status,
                "negative_certified": False,
                "conflict_budget": conflict_budget,
                "conflicts": conflicts,
                "decisions": decisions,
                "propagations": propagations,
                "wall_seconds": elapsed,
                "solver_cpu_seconds_accumulated": solver.time_accum(),
            }
            records.append(record)
            status_counts[status] += 1
            total_conflicts += conflicts
            total_decisions += decisions
            total_propagations += propagations

            if outcome is True:
                model = solver.get_model()
                if model is None:
                    raise AssertionError("SAT outcome has no model")
                candidate = Path(str(frozen["candidate_path"]))
                construction = construction_record(
                    degree=degree,
                    cube=cube,
                    model=model,
                    cnf_path=union_cnf,
                    candidate_path=candidate,
                    cpp_verifier=Path(str(frozen["cpp_verifier"])),
                )

            rss = current_rss_bytes()
            result.update(
                {
                    "maximum_resident_set_bytes": rss,
                    "status_counts": dict(sorted(status_counts.items())),
                    "completed_cube_count": len(records),
                    "total_conflicts": total_conflicts,
                    "total_decisions": total_decisions,
                    "total_propagations": total_propagations,
                    "elapsed_seconds": time.monotonic() - started,
                    "construction": construction,
                }
            )
            atomic_write_json(args.result, result)
            if rss > maximum_rss:
                solver.delete()
                raise RuntimeError(
                    f"worker RSS gate failed after cube: {rss} > {maximum_rss}"
                )
            if construction is not None:
                solver.delete()
                result["termination_reason"] = "VERIFIED_SAT_CONSTRUCTION"
                atomic_write_json(args.result, result)
                print(json.dumps(result, sort_keys=True))
                return 10

        solver.delete()
        gc.collect()

    result.update(
        {
            "scheduled_complete": True,
            "full_cover_screened": len(records) == 3 * SELECTOR_COUNT,
            "termination_reason": "SCHEDULE_COMPLETE_NO_SAT",
            "elapsed_seconds": time.monotonic() - started,
            "maximum_resident_set_bytes": current_rss_bytes(),
        }
    )
    atomic_write_json(args.result, result)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
