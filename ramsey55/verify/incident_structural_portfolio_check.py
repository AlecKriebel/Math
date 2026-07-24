#!/usr/bin/env python3
"""Independent audit of the 9--12-vertex incident completion portfolio."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
PLAN_SCHEMA = "ramsey55.incident_structural_portfolio_plan.v1"
RESULT_SCHEMA = "ramsey55.incident_structural_portfolio_result.v1"
SHARD_SCHEMA = "ramsey55.incident_structural_portfolio_shard.v1"
SIZES = (9, 10, 11, 12)
BUDGETS = {9: 400_000, 10: 300_000, 11: 200_000, 12: 150_000}
EXPECTED_REPRESENTATIVES = (
    (
        "class01",
        1,
        "results/constructive/catalog_seed_search_stratified_v1/line_001.g6",
        "c168d89376f939653c4a7d1f9da4c5800fb9379bf2c4a5cd7db226fce8789a85",
        0,
    ),
    (
        "class02",
        2,
        "results/constructive/catalog_seed_search_stratified_v1/line_002.g6",
        "4e18e027c3211898569ae8a2113ff6e62c1bffd6bb9d2f413930225109547da4",
        10,
    ),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def decode_graph6_file(path: Path) -> tuple[int, ...]:
    lines = [
        line.strip()
        for line in path.read_text(encoding="ascii").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if len(lines) != 1:
        raise ValueError(f"expected one graph6 record in {path}")
    line = lines[0]
    if line.startswith(">>graph6<<"):
        line = line[10:]
    if not line:
        raise ValueError("empty graph6")
    order = ord(line[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("only short graph6 is supported")
    needed = order * (order - 1) // 2
    if len(line) != 1 + (needed + 5) // 6:
        raise ValueError("noncanonical graph6 length")
    adjacency = [0] * order
    bit_index = 0
    for right in range(1, order):
        for left in range(right):
            value = ord(line[1 + bit_index // 6]) - 63
            if not 0 <= value < 64:
                raise ValueError("invalid graph6 byte")
            if (value >> (5 - bit_index % 6)) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit_index += 1
    return tuple(adjacency)


def five_set_data(
    adjacency: Sequence[int],
) -> tuple[
    tuple[tuple[tuple[int, ...], int], ...],
    tuple[tuple[int, ...], ...],
]:
    homogeneous: list[tuple[tuple[int, ...], int]] = []
    near: list[tuple[int, ...]] = []
    for subset in itertools.combinations(range(len(adjacency)), 5):
        edge_count = 0
        for left, right in itertools.combinations(subset, 2):
            edge_count += (adjacency[left] >> right) & 1
        if edge_count == 0 or edge_count == 10:
            homogeneous.append((subset, edge_count))
        elif edge_count == 1 or edge_count == 9:
            near.append(subset)
    return tuple(homogeneous), tuple(near)


def pressure_sequence(
    near: Sequence[tuple[int, ...]],
    conflict_union: Sequence[int],
    order: int,
) -> tuple[tuple[int, ...], tuple[dict[str, int], ...]]:
    conflict = set(conflict_union)
    candidates = [vertex for vertex in range(order) if vertex not in conflict]
    total_load = {
        vertex: sum(1 for subset in near if vertex in subset)
        for vertex in candidates
    }
    remaining = [set(subset) for subset in near if not conflict.intersection(subset)]
    selected: list[int] = []
    trace: list[dict[str, int]] = []
    for _ in range(6):
        values = [
            (
                sum(1 for subset in remaining if vertex in subset),
                total_load[vertex],
                -vertex,
                vertex,
            )
            for vertex in candidates
            if vertex not in selected
        ]
        covered, load, _, chosen = max(values)
        trace.append(
            {
                "vertex": chosen,
                "new_near_sets_covered": covered,
                "total_near_load": load,
                "uncovered_before": len(remaining),
            }
        )
        selected.append(chosen)
        remaining = [subset for subset in remaining if chosen not in subset]
    return tuple(selected), tuple(trace)


def row_diversity_sequence(
    adjacency: Sequence[int],
    near: Sequence[tuple[int, ...]],
    conflict_union: Sequence[int],
) -> tuple[tuple[int, ...], tuple[dict[str, int], ...]]:
    conflict = set(conflict_union)
    candidates = [vertex for vertex in range(len(adjacency)) if vertex not in conflict]
    loads = {
        vertex: sum(1 for subset in near if vertex in subset)
        for vertex in candidates
    }
    signatures = {
        vertex: tuple(
            (adjacency[vertex] >> core_vertex) & 1
            for core_vertex in conflict_union
        )
        for vertex in candidates
    }
    selected: list[int] = []
    trace: list[dict[str, int]] = []
    for _ in range(6):
        available = [vertex for vertex in candidates if vertex not in selected]
        if not selected:
            chosen = max(
                available,
                key=lambda vertex: (
                    loads[vertex],
                    -abs(adjacency[vertex].bit_count() - 21),
                    -vertex,
                ),
            )
            minimum = 0
        else:
            old_signatures = {signatures[vertex] for vertex in selected}

            def key(vertex: int) -> tuple[int, int, int, int]:
                minimum_distance = min(
                    (adjacency[vertex] ^ adjacency[old]).bit_count()
                    for old in selected
                )
                return (
                    minimum_distance,
                    int(signatures[vertex] not in old_signatures),
                    loads[vertex],
                    -vertex,
                )

            chosen = max(available, key=key)
            minimum = key(chosen)[0]
        trace.append(
            {
                "vertex": chosen,
                "minimum_row_distance": minimum,
                "total_near_load": loads[chosen],
                "degree": adjacency[chosen].bit_count(),
            }
        )
        selected.append(chosen)
    return tuple(selected), tuple(trace)


def expected_solver(class_id: str, policy: str) -> str:
    if (class_id, policy) in (
        ("class01", "near_pressure"),
        ("class02", "row_diversity"),
    ):
        return "MapleChrono"
    return "Glucose3"


def expected_instance(
    class_id: str,
    base_path: str,
    base_sha256: str,
    conflict_union: Sequence[int],
    policy: str,
    sequence: Sequence[int],
    boundary_size: int,
) -> dict[str, object]:
    extra_count = boundary_size - 6
    incident = sorted(tuple(conflict_union) + tuple(sequence[:extra_count]))
    return {
        "instance_id": f"{class_id}_{policy}_k{boundary_size:02d}",
        "class_id": class_id,
        "base_graph": base_path,
        "base_graph_sha256": base_sha256,
        "policy": policy,
        "boundary_size": boundary_size,
        "conflict_union": list(conflict_union),
        "extra_vertices": list(sequence[:extra_count]),
        "incident_vertices": incident,
        "free_edge_count": boundary_size * 43 - boundary_size * (boundary_size + 1) // 2,
        "solver": expected_solver(class_id, policy),
        "conflict_budget": BUDGETS[boundary_size],
    }


def audit_plan(plan_path: Path) -> dict[str, object]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {
        "schema": plan.get("schema") == PLAN_SCHEMA,
        "status": plan.get("status") == "PREREGISTERED_BEFORE_PRODUCTION_RUN",
        "instance_count": len(plan.get("instances", [])) == 16,
        "representative_count": len(plan.get("representatives", [])) == 2,
        "resource_jobs_one": plan.get("resources", {}).get("jobs") == 1,
        "proof_logging_disabled": (
            plan.get("resources", {}).get("proof_logging") is False
        ),
    }
    pinned_ok = True
    for record in plan.get("pinned_files", []):
        raw = Path(str(record.get("path")))
        path = raw if raw.is_absolute() else ROOT / raw
        pinned_ok &= path.is_file() and sha256_file(path) == record.get("sha256")
    checks["all_pinned_hashes"] = pinned_ok and bool(plan.get("pinned_files"))

    expected_representatives: list[dict[str, object]] = []
    expected_instances: list[dict[str, object]] = []
    for class_id, line, relative, digest, conflict_edge_count in EXPECTED_REPRESENTATIVES:
        path = ROOT / relative
        adjacency = decode_graph6_file(path)
        homogeneous, near = five_set_data(adjacency)
        if (
            len(adjacency) != 43
            or len(homogeneous) != 2
            or {edge_count for _, edge_count in homogeneous}
            != {conflict_edge_count}
            or len(set(homogeneous[0][0]) & set(homogeneous[1][0])) != 4
        ):
            raise ValueError(f"invalid representative geometry for {relative}")
        union = tuple(
            sorted(set(homogeneous[0][0]) | set(homogeneous[1][0]))
        )
        pressure, pressure_trace = pressure_sequence(near, union, 43)
        diversity, diversity_trace = row_diversity_sequence(
            adjacency, near, union
        )
        expected_representatives.append(
            {
                "class_id": class_id,
                "catalog_line": line,
                "path": relative,
                "sha256": digest,
                "expected_colour": (
                    "independent" if conflict_edge_count == 0 else "clique"
                ),
                "order": 43,
                "edge_count": sum(row.bit_count() for row in adjacency) // 2,
                "conflict_sets": [list(vertices) for vertices, _ in homogeneous],
                "conflict_union": list(union),
                "near_homogeneous_five_set_count": len(near),
                "selection_sequences": {
                    "near_pressure": {
                        "vertices": list(pressure),
                        "trace": list(pressure_trace),
                    },
                    "row_diversity": {
                        "vertices": list(diversity),
                        "trace": list(diversity_trace),
                    },
                },
            }
        )
        for policy, sequence in (
            ("near_pressure", pressure),
            ("row_diversity", diversity),
        ):
            for size in SIZES:
                expected_instances.append(
                    expected_instance(
                        class_id,
                        relative,
                        digest,
                        union,
                        policy,
                        sequence,
                        size,
                    )
                )
    checks["representatives_exact"] = (
        plan.get("representatives") == expected_representatives
    )
    checks["instances_exact"] = plan.get("instances") == expected_instances
    checks["all_boundaries_unique"] = len(
        {
            tuple(instance["incident_vertices"])
            for instance in plan.get("instances", [])
        }
    ) == 16
    checks["two_policies_each_class_size"] = all(
        sum(
            instance["class_id"] == class_id
            and instance["policy"] == policy
            and instance["boundary_size"] == size
            for instance in plan.get("instances", [])
        )
        == 1
        for class_id in ("class01", "class02")
        for policy in ("near_pressure", "row_diversity")
        for size in SIZES
    )
    return {
        "checker": "independent_incident_structural_portfolio_check_v1",
        "plan": str(plan_path),
        "plan_sha256": sha256_file(plan_path),
        "checks": checks,
        "accepted": all(checks.values()),
        "expected_instances": expected_instances,
    }


def incident_edges(order: int, vertices: Iterable[int]) -> tuple[tuple[int, int], ...]:
    selected = set(vertices)
    return tuple(
        (left, right)
        for left in range(order)
        for right in range(left + 1, order)
        if left in selected or right in selected
    )


def formula_summary(
    adjacency: Sequence[int], vertices: Sequence[int]
) -> dict[str, object]:
    edges = incident_edges(len(adjacency), vertices)
    variable = {edge: index for index, edge in enumerate(edges, 1)}
    clique_clauses: list[tuple[int, ...]] = []
    independent_clauses: list[tuple[int, ...]] = []
    for subset in itertools.combinations(range(len(adjacency)), 5):
        variables: list[int] = []
        fixed: list[int] = []
        for pair in itertools.combinations(subset, 2):
            if pair in variable:
                variables.append(variable[pair])
            else:
                fixed.append((adjacency[pair[0]] >> pair[1]) & 1)
        if all(fixed):
            clique_clauses.append(tuple(-value for value in variables))
        if not any(fixed):
            independent_clauses.append(tuple(variables))
    clauses = clique_clauses + independent_clauses
    digest = hashlib.sha256()
    digest.update(f"p cnf {len(edges)} {len(clauses)}\n".encode("ascii"))
    for left, right in edges:
        digest.update(f"e {left} {right}\n".encode("ascii"))
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return {
        "variable_count": len(edges),
        "clique_clause_count": len(clique_clauses),
        "independent_clause_count": len(independent_clauses),
        "clause_count": len(clauses),
        "formula_stream_sha256": digest.hexdigest(),
    }


def count_forbidden(adjacency: Sequence[int]) -> tuple[int, int]:
    clique = 0
    independent = 0
    for subset in itertools.combinations(range(len(adjacency)), 5):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(subset, 2)
        )
        clique += edge_count == 10
        independent += edge_count == 0
    return clique, independent


def audit_candidate(
    candidate: dict[str, object],
    instance: dict[str, object],
) -> bool:
    path = ROOT / str(candidate.get("path"))
    if not path.is_file() or sha256_file(path) != candidate.get("sha256"):
        return False
    completed = decode_graph6_file(path)
    base = decode_graph6_file(ROOT / str(instance["base_graph"]))
    incident = set(instance["incident_vertices"])
    fixed_equal = all(
        ((completed[left] >> right) & 1) == ((base[left] >> right) & 1)
        for left in range(43)
        for right in range(left + 1, 43)
        if left not in incident and right not in incident
    )
    if not fixed_equal or count_forbidden(completed) != (0, 0):
        return False
    python_run = subprocess.run(
        [
            str(ROOT / "verify" / "exhaustive_verify.py"),
            str(path),
            "--k",
            "5",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    cpp_run = subprocess.run(
        [str(ROOT / "build" / "bitset_verify"), str(path), "--k", "5"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    return python_run.returncode == 0 and cpp_run.returncode == 0


def audit_result(plan_path: Path, result_path: Path) -> dict[str, object]:
    plan_audit = audit_plan(plan_path)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    records = result.get("records", [])
    checks: dict[str, bool] = {
        "plan_accepted": bool(plan_audit["accepted"]),
        "schema": result.get("schema") == RESULT_SCHEMA,
        "plan_hash": result.get("plan_sha256") == sha256_file(plan_path),
        "records_are_plan_prefix": (
            [record.get("instance") for record in records]
            == plan["instances"][: len(records)]
        ),
        "completed_count": result.get("completed_instance_count") == len(records),
        "planned_count": result.get("planned_instance_count") == 16,
        "production_after_plan": (
            result.get("production_started_after_plan_mtime") is True
        ),
    }
    record_checks: list[dict[str, object]] = []
    sat_count = unsat_count = budget_count = 0
    all_records_valid = True
    for record in records:
        instance = record.get("instance", {})
        status = record.get("status")
        summary = formula_summary(
            decode_graph6_file(ROOT / str(instance["base_graph"])),
            instance["incident_vertices"],
        )
        valid = (
            record.get("schema") == SHARD_SCHEMA
            and record.get("plan_sha256") == result.get("plan_sha256")
            and status in ("SAT", "UNSAT", "BUDGET_EXHAUSTED")
            and all(record.get(key) == value for key, value in summary.items())
        )
        if status == "SAT":
            sat_count += 1
            valid &= (
                record.get("evidence_label") == "CERTIFIED_CONSTRUCTION"
                and isinstance(record.get("candidate"), dict)
                and record["candidate"].get("independently_verified") is True
                and audit_candidate(record["candidate"], instance)
            )
        elif status == "UNSAT":
            unsat_count += 1
            valid &= (
                record.get("evidence_label")
                == "REPRODUCIBLE_COMPUTATIONAL_OBSERVATION"
                and record.get("candidate") is None
            )
        else:
            budget_count += 1
            valid &= (
                record.get("evidence_label") == "UNRESOLVED"
                and record.get("candidate") is None
                and record.get("solver_stats", {}).get("conflicts", 0)
                >= instance["conflict_budget"]
            )
        all_records_valid &= bool(valid)
        record_checks.append(
            {
                "instance_id": instance.get("instance_id"),
                "status": status,
                "formula_summary": summary,
                "valid": bool(valid),
            }
        )
    checks.update(
        {
            "all_records_valid": all_records_valid and bool(records),
            "sat_count": result.get("sat_count") == sat_count,
            "unsat_count": result.get("unsat_observation_count") == unsat_count,
            "budget_count": result.get("budget_exhausted_count") == budget_count,
            "certified_flag": (
                result.get("certified_construction") == (sat_count > 0)
            ),
            "complete_semantics": result.get("complete")
            == (len(records) == 16 or sat_count > 0),
            "stops_at_first_sat": sat_count <= 1
            and (sat_count == 0 or records[-1]["status"] == "SAT"),
        }
    )
    return {
        "checker": "independent_incident_structural_portfolio_check_v1",
        "plan": str(plan_path),
        "plan_sha256": sha256_file(plan_path),
        "result": str(result_path),
        "result_sha256": sha256_file(result_path),
        "checks": checks,
        "record_checks": record_checks,
        "accepted": all(checks.values()),
        "claim_boundary": (
            "This checker validates exact portfolio scope and any SAT graph. "
            "It does not promote proof-free UNSAT observations to theorems."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    audit = (
        audit_plan(args.plan.resolve())
        if args.result is None
        else audit_result(args.plan.resolve(), args.result.resolve())
    )
    payload = json.dumps(audit, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(json.dumps(audit, sort_keys=True))
    return 0 if audit["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
