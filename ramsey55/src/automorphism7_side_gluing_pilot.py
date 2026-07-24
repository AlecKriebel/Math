#!/usr/bin/env python3
"""Constructive gluing pilot inside the order-7 automorphism class."""

from __future__ import annotations

import argparse
import hashlib
import inspect
import itertools
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Any

import pysat
import pysat.solvers as pysat_solvers
import pysolvers
from pysat.solvers import Cadical195

from graph_io import encode_graph6
from residual_completion_glucose import model_satisfies, parse_dimacs


ROOT = Path(__file__).resolve().parents[1]
PILOT_ID = "ramsey55_automorphism7_side_gluing_pilot_v2"
PLAN_SCHEMA = "ramsey55.automorphism7_side_gluing_plan.v2"
ORDER = 43
PRIME = 7
SIDE_ORDER = 21
LOCAL_VARIABLES = 30
PAIR_RULE = (
    "a=i mod 64; round=floor(i/64); "
    "b=(17*i+23+11*round) mod 64 for i=0,...,255"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_lines(lines: list[str]) -> str:
    payload = ("\n".join(lines) + "\n").encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def atomic_write(path: Path, payload: bytes) -> None:
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
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def existing_ancestor(path: Path) -> Path:
    ancestor = path.resolve().parent
    while not ancestor.exists():
        parent = ancestor.parent
        if parent == ancestor:
            raise ValueError(f"no existing ancestor for {path}")
        ancestor = parent
    return ancestor


def validate_toolchain(plan: dict[str, Any]) -> dict[str, Any]:
    expected = plan.get("toolchain_sha256")
    if not isinstance(expected, dict):
        raise ValueError("plan toolchain hashes missing")
    solvers_path = Path(inspect.getfile(pysat_solvers))
    extension_path = Path(str(pysolvers.__file__))
    python_path = Path(sys.executable)
    actual = {
        "pysat_solvers_py": sha256_file(solvers_path),
        "pysolvers_extension": sha256_file(extension_path),
        "python": sha256_file(python_path),
    }
    if expected != actual:
        raise ValueError(
            f"plan toolchain hash mismatch: expected {expected}, actual {actual}"
        )
    if plan.get("pysat_version") != pysat.__version__:
        raise ValueError("plan PySAT version mismatch")
    return {
        "python_path": str(python_path.resolve()),
        "pysat_solvers_path": str(solvers_path.resolve()),
        "pysolvers_extension_path": str(extension_path.resolve()),
        "sha256": actual,
    }


def validate_storage_gate(
    plan: dict[str, Any], output: Path, candidate: Path
) -> dict[str, int]:
    gate = plan.get("storage_gate")
    if not isinstance(gate, dict):
        raise ValueError("plan storage gate missing")
    labels = (
        "maximum_new_artifact_bytes",
        "minimum_free_bytes_after_completion",
        "required_prelaunch_free_bytes",
    )
    values = {label: gate.get(label) for label in labels}
    if any(type(value) is not int or value < 1 for value in values.values()):
        raise ValueError("invalid plan storage gate")
    maximum = int(values["maximum_new_artifact_bytes"])
    reserve = int(values["minimum_free_bytes_after_completion"])
    required = int(values["required_prelaunch_free_bytes"])
    if required != reserve + maximum:
        raise ValueError("storage gate does not reserve the full artifact cap")
    ancestors = [existing_ancestor(path) for path in (output, candidate)]
    devices = {os.stat(path).st_dev for path in ancestors}
    if len(devices) != 1:
        raise ValueError("planned outputs are on different filesystems")
    available = min(shutil.disk_usage(path).free for path in ancestors)
    if available < required:
        raise ValueError(
            f"storage preflight failed: free {available} < required {required}"
        )
    return {
        "maximum_new_artifact_bytes": maximum,
        "minimum_free_bytes_after_completion": reserve,
        "required_prelaunch_free_bytes": required,
        "available_prelaunch_free_bytes": available,
    }


def parse_json_object(text: str, label: str) -> dict[str, Any]:
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError(f"{label} is not a JSON object")
    return value


def side_edge_orbits() -> tuple[
    tuple[tuple[tuple[int, int], ...], ...],
    dict[tuple[int, int], int],
]:
    permutation = tuple(
        block * PRIME + (offset + 1) % PRIME
        for block in range(3)
        for offset in range(PRIME)
    )
    unseen = set(itertools.combinations(range(SIDE_ORDER), 2))
    orbits: list[tuple[tuple[int, int], ...]] = []
    while unseen:
        edge = min(unseen)
        orbit: set[tuple[int, int]] = set()
        while edge not in orbit:
            orbit.add(edge)
            edge = tuple(sorted((permutation[edge[0]], permutation[edge[1]])))
        unseen.difference_update(orbit)
        orbits.append(tuple(sorted(orbit)))
    orbits.sort(key=lambda orbit: orbit[0])
    table = {
        edge: variable
        for variable, orbit in enumerate(orbits, start=1)
        for edge in orbit
    }
    if len(orbits) != LOCAL_VARIABLES or len(table) != math.comb(SIDE_ORDER, 2):
        raise AssertionError("unexpected side edge-orbit partition")
    return tuple(orbits), table


def side_formula(
    edge_variables: dict[tuple[int, int], int],
) -> tuple[tuple[int, ...], ...]:
    clique_signatures = {
        tuple(
            sorted(
                {
                    edge_variables[edge]
                    for edge in itertools.combinations(vertices, 2)
                }
            )
        )
        for vertices in itertools.combinations(range(SIDE_ORDER), 4)
    }
    independent_signatures = {
        tuple(
            sorted(
                {
                    edge_variables[edge]
                    for edge in itertools.combinations(vertices, 2)
                }
            )
        )
        for vertices in itertools.combinations(range(SIDE_ORDER), 5)
    }
    clauses = [
        tuple(-variable for variable in signature)
        for signature in sorted(clique_signatures)
    ]
    clauses.extend(sorted(independent_signatures))
    if len(clique_signatures) != 843 or len(independent_signatures) != 2775:
        raise AssertionError("unexpected side formula signature counts")
    return tuple(clauses)


def diverse_side_models(
    clauses: tuple[tuple[int, ...], ...],
    count: int,
    seed: int,
) -> list[tuple[bool, ...]]:
    rng = random.Random(seed)
    models: list[tuple[bool, ...]] = []
    with Cadical195(bootstrap_with=clauses) as solver:
        for _ in range(count):
            phases = [
                variable if rng.getrandbits(1) else -variable
                for variable in range(1, LOCAL_VARIABLES + 1)
            ]
            rng.shuffle(phases)
            solver.set_phases(phases)
            if not solver.solve():
                raise AssertionError("side model enumeration exhausted unexpectedly")
            raw = solver.get_model()
            truth = {abs(literal): literal > 0 for literal in raw}
            model = tuple(truth[variable] for variable in range(1, LOCAL_VARIABLES + 1))
            if not model_satisfies(
                [
                    variable if value else -variable
                    for variable, value in enumerate(model, start=1)
                ],
                clauses,
            ):
                raise AssertionError("side model failed direct clause replay")
            if model in models:
                raise AssertionError("blocking failed to produce a distinct side model")
            models.append(model)
            solver.add_clause(
                [
                    -variable if value else variable
                    for variable, value in enumerate(model, start=1)
                ]
            )
    return models


def global_edge_table(metadata: dict[str, Any]) -> dict[tuple[int, int], int]:
    raw_orbits = metadata.get("edge_orbits")
    if not isinstance(raw_orbits, list):
        raise ValueError("global metadata has no edge orbits")
    table: dict[tuple[int, int], int] = {}
    for record in raw_orbits:
        if not isinstance(record, dict) or type(record.get("variable")) is not int:
            raise ValueError("malformed global edge-orbit record")
        variable = record["variable"]
        if not 1 <= variable <= 129:
            raise ValueError("global edge-orbit variable is outside 1..129")
        edges = record.get("edges")
        if not isinstance(edges, list):
            raise ValueError("malformed global edge list")
        for raw_edge in edges:
            if (
                not isinstance(raw_edge, list)
                or len(raw_edge) != 2
                or any(type(vertex) is not int for vertex in raw_edge)
            ):
                raise ValueError("malformed global edge")
            edge = tuple(raw_edge)
            if not 0 <= edge[0] < edge[1] < ORDER or edge in table:
                raise ValueError("invalid or duplicate global edge")
            table[edge] = variable
    if len(table) != math.comb(ORDER, 2):
        raise ValueError("global edge-orbit table is incomplete")
    multiplicities = Counter(table.values())
    if set(multiplicities) != set(range(1, 130)) or set(
        multiplicities.values()
    ) != {PRIME}:
        raise ValueError("global edge-orbit variables are not 129 size-7 orbits")
    return table


def complete_model_truth(
    model: list[int], variable_count: int
) -> dict[int, bool]:
    truth: dict[int, bool] = {}
    for literal in model:
        if (
            type(literal) is not int
            or literal == 0
            or abs(literal) > variable_count
            or abs(literal) in truth
        ):
            raise ValueError("SAT model is duplicate, zero, or out of range")
        truth[abs(literal)] = literal > 0
    if set(truth) != set(range(1, variable_count + 1)):
        raise ValueError("SAT model is not a complete primary assignment")
    return truth


def decode_global_graph(
    truth: dict[int, bool], edge_variables: dict[tuple[int, int], int]
) -> list[int]:
    adjacency = [0] * ORDER
    for (left, right), variable in edge_variables.items():
        if truth[variable]:
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return adjacency


def deterministic_pairs(
    pool_count: int, pair_count: int
) -> list[tuple[int, int]]:
    pairs = []
    for pair_index in range(pair_count):
        a_index = pair_index % pool_count
        round_index = pair_index // pool_count
        b_index = (17 * pair_index + 23 + 11 * round_index) % pool_count
        pairs.append((a_index, b_index))
    if len(set(pairs)) != len(pairs):
        raise ValueError("deterministic pair schedule contains a duplicate")
    return pairs


def verify_candidate(
    candidate: Path, exhaustive: Path, bitset: Path
) -> dict[str, Any]:
    commands = {
        "python": [sys.executable, str(exhaustive), str(candidate)],
        "cpp": [str(bitset), str(candidate)],
    }
    results: dict[str, Any] = {}
    for label, command in commands.items():
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        results[label] = {
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "json": (
                parse_json_object(completed.stdout, f"{label} verifier")
                if completed.returncode == 0
                else None
            ),
        }
    python_json = results["python"]["json"]
    cpp_json = results["cpp"]["json"]
    candidate_sha256 = sha256_file(candidate)
    results["valid"] = (
        results["python"]["returncode"] == 0
        and results["cpp"]["returncode"] == 0
        and python_json.get("valid") is True
        and python_json.get("objective") == 0
        and python_json.get("n") == ORDER
        and python_json.get("k") == 5
        and python_json.get("input_sha256") == candidate_sha256
        and python_json.get("verifier")
        == "python_exhaustive_k_subset_pairs_v1"
        and cpp_json.get("valid") is True
        and cpp_json.get("n") == ORDER
        and cpp_json.get("k") == 5
        and cpp_json.get("clique_k_found") is False
        and cpp_json.get("independent_k_found") is False
        and cpp_json.get("verifier") == "cpp_recursive_bitset_clique_v1"
    )
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--exhaustive-verifier", type=Path, required=True)
    parser.add_argument("--bitset-verifier", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()

    plan = parse_json_object(args.plan.read_text(encoding="utf-8"), "plan")
    if plan.get("schema") != PLAN_SCHEMA or plan.get("status") != "PREREGISTERED":
        raise SystemExit("invalid preregistered plan schema/status")
    pinned = {
        "cnf": args.cnf,
        "metadata": args.metadata,
        "exhaustive_verifier": args.exhaustive_verifier,
        "bitset_verifier": args.bitset_verifier,
        "runner": Path(__file__).resolve(),
    }
    for label, path in pinned.items():
        record = plan.get(label)
        if (
            not isinstance(record, dict)
            or Path(record.get("path", "")).resolve() != path.resolve()
            or sha256_file(path) != record.get("sha256")
        ):
            raise SystemExit(f"plan pin mismatch for {label}")
    configuration = plan.get("configuration")
    if not isinstance(configuration, dict):
        raise SystemExit("plan configuration missing")
    pool_count = configuration.get("side_pool_count")
    pair_count = configuration.get("pair_count")
    conflict_budget = configuration.get("conflict_budget_per_pair")
    seed = configuration.get("side_pool_seed")
    if any(type(value) is not int or value < 1 for value in (pool_count, pair_count, conflict_budget, seed)):
        raise SystemExit("invalid plan configuration")
    outputs = plan.get("outputs")
    if (
        not isinstance(outputs, dict)
        or Path(outputs.get("summary", "")).resolve() != args.output.resolve()
        or Path(outputs.get("candidate", "")).resolve() != args.candidate.resolve()
    ):
        raise SystemExit("plan output mismatch")
    if args.output.exists() or args.candidate.exists():
        raise SystemExit("refusing to overwrite an output")
    try:
        toolchain = validate_toolchain(plan)
        storage = validate_storage_gate(plan, args.output, args.candidate)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    variable_count, global_clauses = parse_dimacs(args.cnf)
    metadata = parse_json_object(args.metadata.read_text(encoding="utf-8"), "metadata")
    if (
        variable_count != 129
        or metadata.get("order") != ORDER
        or metadata.get("variable_count") != variable_count
        or metadata.get("edge_orbit_count") != variable_count
        or metadata.get("automorphism_order") != 7
        or metadata.get("cycle_count") != 6
        or metadata.get("fixed_point_count") != 1
        or metadata.get("cnf_sha256") != sha256_file(args.cnf)
    ):
        raise SystemExit("unexpected global orbit formula")
    edge_variables = global_edge_table(metadata)
    side_orbits, side_table = side_edge_orbits()
    local_clauses = side_formula(side_table)
    local_clause_sha256 = sha256_lines(
        [" ".join(map(str, clause)) for clause in local_clauses]
    )
    if (
        configuration.get("side_formula_variable_count") != LOCAL_VARIABLES
        or configuration.get("side_formula_clause_count") != len(local_clauses)
        or configuration.get("side_formula_sha256") != local_clause_sha256
        or configuration.get("pair_rule") != PAIR_RULE
    ):
        raise SystemExit("plan side formula or pair rule mismatch")
    side_models = diverse_side_models(local_clauses, pool_count, seed)
    encoded_side_models = [
        "".join("1" if value else "0" for value in model)
        for model in side_models
    ]
    side_pool_sha256 = sha256_lines(encoded_side_models)
    if configuration.get("side_pool_sha256") != side_pool_sha256:
        raise SystemExit("plan side-model pool hash mismatch")
    pairs = deterministic_pairs(pool_count, pair_count)
    pair_schedule_sha256 = sha256_lines(
        [f"{left},{right}" for left, right in pairs]
    )
    if configuration.get("pair_schedule_sha256") != pair_schedule_sha256:
        raise SystemExit("plan pair schedule hash mismatch")

    map_a = [edge_variables[orbit[0]] for orbit in side_orbits]
    map_b = [
        edge_variables[(orbit[0][0] + SIDE_ORDER, orbit[0][1] + SIDE_ORDER)]
        for orbit in side_orbits
    ]
    fixed_orbits = sorted(
        {
            variable
            for (left, right), variable in edge_variables.items()
            if right == ORDER - 1
        },
        key=lambda variable: min(
            left
            for (left, right), observed in edge_variables.items()
            if right == ORDER - 1 and observed == variable
        ),
    )
    if len(fixed_orbits) != 6:
        raise AssertionError("fixed vertex does not have six cycle orbits")
    fixed_vertex_units = fixed_orbits[:3] + [-variable for variable in fixed_orbits[3:]]
    assigned_orbits = set(fixed_orbits + map_a + map_b)
    free_orbits = sorted(set(range(1, variable_count + 1)) - assigned_orbits)
    if len(assigned_orbits) != 66 or len(free_orbits) != 63:
        raise AssertionError("global orbit partition is not 66 fixed / 63 free")

    started = time.monotonic()
    records: list[dict[str, Any]] = []
    construction: dict[str, Any] | None = None
    for pair_index, (a_index, b_index) in enumerate(pairs):
        try:
            validate_storage_gate(plan, args.output, args.candidate)
        except ValueError as error:
            raise RuntimeError(
                f"storage gate closed before pair {pair_index}: {error}"
            ) from error
        units = list(fixed_vertex_units)
        units.extend(
            variable if value else -variable
            for variable, value in zip(map_a, side_models[a_index])
        )
        units.extend(
            -variable if value else variable
            for variable, value in zip(map_b, side_models[b_index])
        )
        if len(units) != 66 or len({abs(literal) for literal in units}) != 66:
            raise AssertionError("gluing assignment does not fix 66 distinct variables")
        pair_started = time.monotonic()
        with Cadical195(
            bootstrap_with=[*global_clauses, *((literal,) for literal in units)],
            use_timer=True,
        ) as solver:
            solver.conf_budget(conflict_budget)
            outcome = solver.solve_limited()
            stats = solver.accum_stats()
            solver_cpu = solver.time_accum()
            model = solver.get_model() if outcome is True else None
        record: dict[str, Any] = {
            "pair_index": pair_index,
            "a_model_index": a_index,
            "b_model_index": b_index,
            "status": (
                "SAT"
                if outcome is True
                else "OBSERVED_UNSAT_UNCHECKED"
                if outcome is False
                else "BUDGET_EXHAUSTED"
            ),
            "negative_certified": False,
            "wall_seconds": time.monotonic() - pair_started,
            "solver_cpu_seconds": solver_cpu,
            **stats,
        }
        records.append(record)
        if outcome is True:
            assert model is not None
            model_truth = complete_model_truth(model, variable_count)
            full_formula = [
                *global_clauses,
                *((literal,) for literal in units),
            ]
            if not model_satisfies(model, full_formula):
                raise AssertionError("gluing SAT model failed direct CNF replay")
            adjacency = decode_global_graph(model_truth, edge_variables)
            candidate_payload = (
                encode_graph6(adjacency) + "\n"
            ).encode("ascii")
            if len(candidate_payload) > storage["maximum_new_artifact_bytes"]:
                raise RuntimeError("candidate exceeds artifact cap")
            atomic_write(args.candidate, candidate_payload)
            verification = verify_candidate(
                args.candidate, args.exhaustive_verifier, args.bitset_verifier
            )
            construction = {
                "pair_index": pair_index,
                "candidate_path": str(args.candidate.resolve()),
                "candidate_sha256": sha256_file(args.candidate),
                "true_primary_variables": [
                    variable
                    for variable in range(1, variable_count + 1)
                    if model_truth.get(variable, False)
                ],
                "verification": verification,
            }
            if not verification["valid"]:
                raise AssertionError("SAT orbit model failed full-graph verification")
            break

    status_counts: dict[str, int] = {}
    for record in records:
        label = str(record["status"])
        status_counts[label] = status_counts.get(label, 0) + 1
    result = {
        "pilot": PILOT_ID,
        "evidence_label": (
            "CERTIFIED CONSTRUCTION"
            if construction
            else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        ),
        "status": "CONSTRUCTION_VERIFIED" if construction else "COMPLETE_NO_CONSTRUCTION",
        "claim_boundary": (
            "A dual-verified SAT model is a construction. Negative pair results "
            "without proofs are observations only and do not exclude the "
            "automorphism class or arbitrary order-43 graphs."
        ),
        "plan_path": str(args.plan.resolve()),
        "plan_sha256": sha256_file(args.plan),
        "cnf_sha256": sha256_file(args.cnf),
        "metadata_sha256": sha256_file(args.metadata),
        "pysat_version": pysat.__version__,
        "toolchain": toolchain,
        "storage_preflight": storage,
        "configuration": configuration,
        "side_formula": {
            "variable_count": LOCAL_VARIABLES,
            "clause_count": len(local_clauses),
            "sha256": local_clause_sha256,
            "model_count": len(side_models),
            "model_pool_sha256": side_pool_sha256,
            "models": encoded_side_models,
        },
        "pair_schedule": {
            "sha256": pair_schedule_sha256,
            "unique_pair_count": len(set(pairs)),
            "left_model_use_histogram": dict(
                sorted(Counter(left for left, _ in pairs).items())
            ),
            "right_model_use_histogram": dict(
                sorted(Counter(right for _, right in pairs).items())
            ),
        },
        "fixed_vertex_orbit_variables": fixed_orbits,
        "fixed_vertex_units": fixed_vertex_units,
        "fixed_orbit_count": len(assigned_orbits),
        "free_orbit_count": len(free_orbits),
        "free_orbit_variables": free_orbits,
        "record_count": len(records),
        "status_counts": status_counts,
        "records": records,
        "construction": construction,
        "runtime_seconds": time.monotonic() - started,
    }
    result_payload = (
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    candidate_bytes = args.candidate.stat().st_size if args.candidate.exists() else 0
    if (
        candidate_bytes + len(result_payload)
        > storage["maximum_new_artifact_bytes"]
    ):
        raise RuntimeError("planned outputs exceed the artifact cap")
    output_ancestor = existing_ancestor(args.output)
    if shutil.disk_usage(output_ancestor).free < (
        storage["minimum_free_bytes_after_completion"] + len(result_payload)
    ):
        raise RuntimeError("free-space reserve would be breached by summary")
    atomic_write(args.output, result_payload)
    print(json.dumps({key: value for key, value in result.items() if key != "records"}, sort_keys=True))
    return 10 if construction else 0


if __name__ == "__main__":
    raise SystemExit(main())
