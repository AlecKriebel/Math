#!/usr/bin/env python3
"""Proof-free persistent screening of the exact degree-20 profile cover.

Negative outcomes from this worker are observations only.  A SAT outcome is
decoded as a full order-43 graph, replayed against the loaded CNF, counted by
an independent subset enumerator, and checked by the independent C++ bitset
verifier before it is reported as a construction.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import inspect
import json
import random
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

import pysat
from pysat import solvers as pysat_solvers

from global_degree20_profile_cover import profile_units, profiles
from graph_io import complement, encode_graph6, read_graph
from residual_completion_glucose import model_satisfies, parse_dimacs


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "verify"
WORKER_ID = "ramsey55_global_degree20_profile_screen_v1"
ORDER = 43
PRIMARY_VARIABLE_COUNT = 903
EXPECTED_BASE_SHA256 = (
    "141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1"
)
SOLVERS = (
    "Cadical195",
    "Glucose4",
    "MapleChrono",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def edge_variable(left: int, right: int) -> int:
    if left > right:
        left, right = right, left
    if not 0 <= left < right < ORDER:
        raise ValueError("invalid edge")
    return 1 + left * (2 * ORDER - left - 1) // 2 + right - left - 1


def relabel(adjacency: list[int], old_order: list[int]) -> list[int]:
    if sorted(old_order) != list(range(len(adjacency))):
        raise ValueError("old_order is not a permutation")
    result = [0] * len(adjacency)
    for new_left, old_left in enumerate(old_order):
        for new_right in range(new_left + 1, len(adjacency)):
            old_right = old_order[new_right]
            if (adjacency[old_left] >> old_right) & 1:
                result[new_left] |= 1 << new_right
                result[new_right] |= 1 << new_left
    return result


def canonical_phase_graph(
    adjacency: list[int],
) -> tuple[list[int], tuple[int, int, int]]:
    if len(adjacency) != ORDER:
        raise ValueError("phase graph must have order 43")
    degrees = [neighbors.bit_count() for neighbors in adjacency]
    if any(degree not in (20, 21, 22) for degree in degrees):
        raise ValueError("phase graph degrees are not all in {20,21,22}")
    counts = tuple(degrees.count(degree) for degree in (20, 21, 22))
    if counts[0] < counts[2]:
        adjacency = complement(adjacency)
        degrees = [neighbors.bit_count() for neighbors in adjacency]
        counts = tuple(degrees.count(degree) for degree in (20, 21, 22))
    if counts not in profiles():
        raise ValueError("phase graph does not normalize to a covered profile")
    old_order = sorted(range(ORDER), key=lambda vertex: (degrees[vertex], vertex))
    normalized = relabel(adjacency, old_order)
    normalized_degrees = tuple(
        neighbors.bit_count() for neighbors in normalized
    )
    expected = (
        (20,) * counts[0] + (21,) * counts[1] + (22,) * counts[2]
    )
    if normalized_degrees != expected:
        raise AssertionError("phase relabelling did not sort degrees")
    return normalized, counts


def primary_phases(adjacency: list[int]) -> list[int]:
    return [
        (
            edge_variable(left, right)
            if (adjacency[left] >> right) & 1
            else -edge_variable(left, right)
        )
        for left in range(ORDER)
        for right in range(left + 1, ORDER)
    ]


def decode_model(model: list[int]) -> list[int]:
    truth = {abs(literal): literal > 0 for literal in model}
    if any(variable not in truth for variable in range(1, PRIMARY_VARIABLE_COUNT + 1)):
        raise ValueError("model omits primary variables")
    adjacency = [0] * ORDER
    for left in range(ORDER):
        for right in range(left + 1, ORDER):
            if truth[edge_variable(left, right)]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
    return adjacency


def forbidden_counts(adjacency: list[int]) -> tuple[int, int]:
    sys.path.insert(0, str(VERIFY))
    from exhaustive_verify import count_forbidden

    return count_forbidden(adjacency, 5)


def schedule_hash(schedule: list[tuple[int, int, int]]) -> str:
    return hashlib.sha256(
        "".join(f"{a} {b} {c}\n" for a, b, c in schedule).encode("ascii")
    ).hexdigest()


def write_result(path: Path, result: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_cnf", type=Path)
    parser.add_argument("--solver", choices=SOLVERS, required=True)
    parser.add_argument("--conflict-budget", type=int, required=True)
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument("--phase-graph", type=Path)
    parser.add_argument("--maximum-profiles", type=int)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    if args.conflict_budget <= 0:
        parser.error("--conflict-budget must be positive")
    if args.maximum_profiles is not None and args.maximum_profiles <= 0:
        parser.error("--maximum-profiles must be positive")

    base_sha256 = sha256_file(args.base_cnf)
    if base_sha256 != EXPECTED_BASE_SHA256:
        raise SystemExit("base CNF SHA-256 mismatch")

    canonical_phase: list[int] | None = None
    phase_profile: tuple[int, int, int] | None = None
    phase_sha256: str | None = None
    if args.phase_graph is not None:
        canonical_phase, phase_profile = canonical_phase_graph(
            read_graph(args.phase_graph)
        )
        phase_sha256 = sha256_file(args.phase_graph)

    schedule = list(profiles())
    if phase_profile is not None:
        schedule.sort(
            key=lambda profile: (
                sum(
                    abs(left - right)
                    for left, right in zip(profile, phase_profile)
                ),
                profile,
            )
        )
    if args.maximum_profiles is not None:
        schedule = schedule[: args.maximum_profiles]

    setup_started = time.monotonic()
    variable_count, clauses = parse_dimacs(args.base_cnf)
    if variable_count != 65_403 or len(clauses) != 2_052_132:
        raise AssertionError("unexpected base formula counts")
    solver_class = getattr(pysat_solvers, args.solver)
    rng = random.Random(args.seed)
    records: list[dict[str, object]] = []
    statuses: Counter[str] = Counter()
    total_conflicts = 0
    construction: dict[str, object] | None = None
    started = time.monotonic()

    result: dict[str, object] = {
        "worker": WORKER_ID,
        "evidence_label": "PROOF-FREE CONSTRUCTION SEARCH",
        "claim_boundary": (
            "SAT is decoded and independently verified. Negative outcomes "
            "have no proof and do not exclude a profile or the degree-20 "
            "global branch."
        ),
        "base_cnf": str(args.base_cnf.resolve()),
        "base_cnf_sha256": base_sha256,
        "base_variable_count": variable_count,
        "base_clause_count": len(clauses),
        "solver": args.solver,
        "solver_class_source": inspect.getfile(solver_class),
        "pysat_version": pysat.__version__,
        "conflict_budget_per_profile": args.conflict_budget,
        "seed": args.seed,
        "full_profile_count": len(profiles()),
        "scheduled_profile_count": len(schedule),
        "schedule_sha256": schedule_hash(schedule),
        "phase_graph": (
            str(args.phase_graph.resolve())
            if args.phase_graph is not None
            else None
        ),
        "phase_graph_sha256": phase_sha256,
        "phase_profile": list(phase_profile) if phase_profile else None,
        "setup_seconds": time.monotonic() - setup_started,
        "records": records,
        "status_counts": {},
        "completed_profile_count": 0,
        "total_conflicts": 0,
        "construction": None,
        "scheduled_complete": False,
        "full_cover_screened": False,
    }
    write_result(args.result, result)

    with solver_class(bootstrap_with=clauses, use_timer=True) as solver:
        del clauses
        gc.collect()
        for index, profile in enumerate(schedule):
            assumptions = list(profile_units(profile))
            if canonical_phase is not None and profile == phase_profile:
                phases = assumptions + primary_phases(canonical_phase)
                phase_source = "normalized_input_graph"
            else:
                phases = assumptions + [
                    variable if rng.getrandbits(1) else -variable
                    for variable in range(1, PRIMARY_VARIABLE_COUNT + 1)
                ]
                phase_source = "seeded_random_primary"
            rng.shuffle(phases)
            solver.set_phases(phases)
            before = solver.accum_stats()
            profile_started = time.monotonic()
            solver.conf_budget(args.conflict_budget)
            outcome = solver.solve_limited(assumptions=assumptions)
            after = solver.accum_stats()
            conflicts = after.get("conflicts", 0) - before.get("conflicts", 0)
            total_conflicts += conflicts
            status = (
                "SAT"
                if outcome is True
                else "OBSERVED_UNSAT_UNCHECKED"
                if outcome is False
                else "BUDGET_EXHAUSTED"
            )
            statuses[status] += 1
            record = {
                "schedule_index": index,
                "multiplicities": list(profile),
                "edge_count": (
                    20 * profile[0] + 21 * profile[1] + 22 * profile[2]
                )
                // 2,
                "assumption_count": len(assumptions),
                "phase_source": phase_source,
                "status": status,
                "negative_certified": False,
                "conflicts": conflicts,
                "decisions": (
                    after.get("decisions", 0) - before.get("decisions", 0)
                ),
                "propagations": (
                    after.get("propagations", 0)
                    - before.get("propagations", 0)
                ),
                "wall_seconds": time.monotonic() - profile_started,
            }
            records.append(record)

            if outcome is True:
                model = solver.get_model()
                if model is None:
                    raise AssertionError("SAT outcome has no model")
                # Reparse only on the exceptional SAT path so negative
                # screening does not retain a second 2M-clause copy.
                _variables, replay_clauses = parse_dimacs(args.base_cnf)
                if not model_satisfies(model, replay_clauses):
                    raise AssertionError("SAT model fails exact CNF replay")
                adjacency = decode_model(model)
                counts = forbidden_counts(adjacency)
                if counts != (0, 0):
                    raise AssertionError("SAT graph has forbidden five-set")
                graph6 = encode_graph6(adjacency) + "\n"
                destination = args.candidate
                if destination is None:
                    destination = args.result.with_suffix(".sat.g6")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(graph6, encoding="ascii")
                cpp = subprocess.run(
                    [str(ROOT / "build" / "bitset_verify"), str(destination)],
                    capture_output=True,
                    text=True,
                    timeout=120,
                    check=False,
                )
                if cpp.returncode != 0:
                    raise AssertionError(
                        "independent C++ verifier rejected SAT graph: "
                        + cpp.stdout
                        + cpp.stderr
                    )
                construction = {
                    "profile": list(profile),
                    "graph6": graph6.strip(),
                    "graph6_sha256": hashlib.sha256(
                        graph6.encode("ascii")
                    ).hexdigest(),
                    "path": str(destination.resolve()),
                    "python_forbidden_counts": list(counts),
                    "cpp_verifier_stdout": cpp.stdout.strip(),
                }

            result.update(
                {
                    "records": records,
                    "status_counts": dict(sorted(statuses.items())),
                    "completed_profile_count": len(records),
                    "total_conflicts": total_conflicts,
                    "construction": construction,
                    "elapsed_seconds": time.monotonic() - started,
                    "scheduled_complete": construction is not None
                    or len(records) == len(schedule),
                    "full_cover_screened": (
                        construction is None
                        and len(schedule) == len(profiles())
                        and len(records) == len(schedule)
                    ),
                }
            )
            write_result(args.result, result)
            print(
                json.dumps(
                    {
                        "event": "profile_complete",
                        **record,
                        "completed": len(records),
                        "scheduled": len(schedule),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            if construction is not None:
                break

        solver_cpu_seconds = solver.time_accum()
    result["solver_cpu_seconds"] = solver_cpu_seconds
    result["source_sha256"] = sha256_file(Path(__file__))
    result["elapsed_seconds"] = time.monotonic() - started
    result["scheduled_complete"] = (
        construction is not None or len(records) == len(schedule)
    )
    result["full_cover_screened"] = (
        construction is None
        and len(schedule) == len(profiles())
        and len(records) == len(schedule)
    )
    write_result(args.result, result)
    print(json.dumps(result, sort_keys=True))
    return 10 if construction is not None else 0


if __name__ == "__main__":
    raise SystemExit(main())
