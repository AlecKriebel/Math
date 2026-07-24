#!/usr/bin/env python3
"""Low-storage constructive search in the order-3 class ``3^14 1^1``.

The exact orbit formula is held in memory.  The fixed vertex has degree
18, 21, or 24, hence meets 6, 7, or 8 moved cycles.  Complementation exchanges
6 and 8, and the cycle labels can be normalized, so the two cases ``t=6`` and
``t=7`` cover the whole automorphism class.

This is a positive search, not a nonexistence proof.  A SAT model is decoded
and exhaustively replayed before it is returned.  Every negative bounded
solver outcome is explicitly labelled as uncertified.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import itertools
import json
import math
import random
import resource
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Iterable

from graph_io import encode_graph6


SEARCH_ID = "ramsey55_order3_maxcycle_search_v1"
ORDER = 43
PRIME = 3
CYCLE_COUNT = 14
FIXED_VERTEX = 42
EXPECTED_VARIABLES = 301
EXPECTED_SIGNATURES = 320_593
EXPECTED_CLAUSES = 641_186
EXPECTED_DIMACS_SHA256 = (
    "2cb249c2d09d00bd199be27711fc344873785b9e9756dc1cafad8f756084a5e5"
)
EXPECTED_SIGNATURE_HISTOGRAM = Counter(
    {5: 91, 6: 182, 7: 91, 8: 3_276, 9: 19_656, 10: 297_297}
)


def permutation(order: int = ORDER, cycle_count: int = CYCLE_COUNT) -> tuple[int, ...]:
    """Return ``(0 1 2)(3 4 5)...(39 40 41)(42)`` or a local analogue."""
    if order != PRIME * cycle_count and order != PRIME * cycle_count + 1:
        raise ValueError("order must be 3*c or 3*c+1")
    image = list(range(order))
    for cycle in range(cycle_count):
        base = PRIME * cycle
        for offset in range(PRIME):
            image[base + offset] = base + (offset + 1) % PRIME
    return tuple(image)


def edge_orbits(
    order: int = ORDER, cycle_count: int = CYCLE_COUNT
) -> tuple[
    dict[tuple[int, int], int],
    tuple[tuple[tuple[int, int], ...], ...],
]:
    """Construct the exact edge-orbit partition by direct group action."""
    image = permutation(order, cycle_count)
    unseen = set(itertools.combinations(range(order), 2))
    parts: list[tuple[tuple[int, int], ...]] = []
    while unseen:
        edge = min(unseen)
        orbit: set[tuple[int, int]] = set()
        while edge not in orbit:
            orbit.add(edge)
            edge = tuple(sorted((image[edge[0]], image[edge[1]])))
        unseen.difference_update(orbit)
        parts.append(tuple(sorted(orbit)))
    parts.sort(key=lambda part: part[0])
    table = {
        edge: variable
        for variable, part in enumerate(parts, start=1)
        for edge in part
    }
    if len(table) != math.comb(order, 2):
        raise AssertionError("edge orbits do not partition the complete graph")
    return table, tuple(parts)


def homogeneous_signatures(
    order: int, size: int, edge_variable: dict[tuple[int, int], int]
) -> tuple[tuple[int, ...], ...]:
    """Return the deduplicated orbit-variable signatures of all ``size``-sets."""
    return tuple(
        sorted(
            {
                tuple(
                    sorted(
                        {
                            edge_variable[edge]
                            for edge in itertools.combinations(vertices, 2)
                        }
                    )
                )
                for vertices in itertools.combinations(range(order), size)
            }
        )
    )


def ramsey_signatures(
    edge_variable: dict[tuple[int, int], int]
) -> tuple[tuple[int, ...], ...]:
    return homogeneous_signatures(ORDER, 5, edge_variable)


def clauses_from_signatures(
    signatures: Iterable[tuple[int, ...]],
) -> list[tuple[int, ...]]:
    clauses: list[tuple[int, ...]] = []
    for signature in signatures:
        clauses.append(signature)
        clauses.append(tuple(-variable for variable in signature))
    return clauses


def dimacs_sha256(
    variable_count: int, signatures: Iterable[tuple[int, ...]]
) -> str:
    """Hash the canonical DIMACS byte stream without materializing it."""
    signatures = tuple(signatures)
    state = hashlib.sha256()
    state.update(f"p cnf {variable_count} {2 * len(signatures)}\n".encode("ascii"))
    for signature in signatures:
        state.update((" ".join(map(str, signature)) + " 0\n").encode("ascii"))
        state.update(
            (" ".join(str(-value) for value in signature) + " 0\n").encode(
                "ascii"
            )
        )
    return state.hexdigest()


def build_exact_formula() -> tuple[
    dict[tuple[int, int], int],
    tuple[tuple[tuple[int, int], ...], ...],
    list[tuple[int, ...]],
    dict[str, object],
]:
    started = time.monotonic()
    edge_variable, orbits = edge_orbits()
    signatures = ramsey_signatures(edge_variable)
    formula_sha256 = dimacs_sha256(len(orbits), signatures)
    orbit_histogram = Counter(map(len, orbits))
    signature_histogram = Counter(map(len, signatures))
    if (
        len(orbits) != EXPECTED_VARIABLES
        or orbit_histogram != Counter({3: EXPECTED_VARIABLES})
        or len(signatures) != EXPECTED_SIGNATURES
        or signature_histogram != EXPECTED_SIGNATURE_HISTOGRAM
        or formula_sha256 != EXPECTED_DIMACS_SHA256
    ):
        raise AssertionError("order-3 exact formula fingerprint mismatch")
    clauses = clauses_from_signatures(signatures)
    metadata = {
        "variable_count": len(orbits),
        "edge_orbit_size_histogram": dict(sorted(orbit_histogram.items())),
        "unique_signature_count": len(signatures),
        "signature_size_histogram": dict(sorted(signature_histogram.items())),
        "clause_count": len(clauses),
        "dimacs_sha256_without_materialization": formula_sha256,
        "build_seconds": time.monotonic() - started,
    }
    return edge_variable, orbits, clauses, metadata


def fixed_vertex_variables(
    edge_variable: dict[tuple[int, int], int]
) -> tuple[int, ...]:
    variables = tuple(
        edge_variable[(PRIME * cycle, FIXED_VERTEX)]
        for cycle in range(CYCLE_COUNT)
    )
    if len(set(variables)) != CYCLE_COUNT:
        raise AssertionError("fixed-vertex incident orbits are not distinct")
    return variables


def fixed_vertex_units(
    t_case: int, edge_variable: dict[tuple[int, int], int]
) -> tuple[int, ...]:
    if t_case not in (6, 7):
        raise ValueError("the normalized search cases are t=6 and t=7")
    return tuple(
        variable if cycle < t_case else -variable
        for cycle, variable in enumerate(fixed_vertex_variables(edge_variable))
    )


def local_side_formula(
    cycle_count: int,
) -> tuple[
    tuple[tuple[tuple[int, int], ...], ...],
    dict[tuple[int, int], int],
    tuple[tuple[int, ...], ...],
]:
    """Build the C3-invariant ``R(4,5;3*cycle_count)`` side formula."""
    order = PRIME * cycle_count
    edge_variable, orbits = edge_orbits(order, cycle_count)
    four_signatures = homogeneous_signatures(order, 4, edge_variable)
    five_signatures = homogeneous_signatures(order, 5, edge_variable)
    clauses = [
        tuple(-variable for variable in signature)
        for signature in four_signatures
    ]
    clauses.extend(five_signatures)
    return orbits, edge_variable, tuple(clauses)


def complete_truth(model: list[int], variable_count: int) -> dict[int, bool]:
    truth: dict[int, bool] = {}
    for literal in model:
        variable = abs(literal)
        if (
            not 1 <= variable <= variable_count
            or literal == 0
            or variable in truth
        ):
            raise ValueError("model has an invalid or duplicate literal")
        truth[variable] = literal > 0
    if set(truth) != set(range(1, variable_count + 1)):
        raise ValueError("model is not complete over the primary variables")
    return truth


def assignment_satisfies(
    assignment: tuple[bool, ...], clauses: Iterable[tuple[int, ...]]
) -> bool:
    return all(
        any(
            assignment[abs(literal) - 1] == (literal > 0)
            for literal in clause
        )
        for clause in clauses
    )


def transformed_side_model(
    model: tuple[bool, ...],
    orbits: tuple[tuple[tuple[int, int], ...], ...],
    edge_variable: dict[tuple[int, int], int],
    cycle_permutation: tuple[int, ...],
    shifts: tuple[int, ...],
    multiplier: int,
) -> tuple[bool, ...]:
    """Relabel a local model by an element of the C3-subgroup normalizer."""
    cycle_count = len(cycle_permutation)
    if (
        sorted(cycle_permutation) != list(range(cycle_count))
        or len(shifts) != cycle_count
        or any(shift not in range(PRIME) for shift in shifts)
        or multiplier not in (1, -1)
    ):
        raise ValueError("invalid side-model relabeling")

    def image(vertex: int) -> int:
        cycle, phase = divmod(vertex, PRIME)
        return (
            PRIME * cycle_permutation[cycle]
            + (multiplier * phase + shifts[cycle]) % PRIME
        )

    transformed: list[bool | None] = [None] * len(orbits)
    for old_variable, orbit in enumerate(orbits, start=1):
        left, right = orbit[0]
        new_edge = tuple(sorted((image(left), image(right))))
        new_variable = edge_variable[new_edge]
        value = model[old_variable - 1]
        previous = transformed[new_variable - 1]
        if previous is not None and previous != value:
            raise AssertionError("side relabeling is not orbit-consistent")
        transformed[new_variable - 1] = value
    if any(value is None for value in transformed):
        raise AssertionError("side relabeling did not permute every variable")
    return tuple(bool(value) for value in transformed)


def diverse_side_models(
    cycle_count: int,
    requested_count: int,
    base_model_count: int,
    conflict_budget: int,
    seed: int,
) -> tuple[
    tuple[tuple[tuple[int, int], ...], ...],
    tuple[tuple[int, ...], ...],
    list[tuple[bool, ...]],
    dict[str, object],
]:
    try:
        from pysat.solvers import Cadical195
    except ImportError as error:
        raise RuntimeError("Python-SAT is required for the constructive search") from error

    orbits, edge_variable, clauses = local_side_formula(cycle_count)
    rng = random.Random(seed)
    base_models: list[tuple[bool, ...]] = []
    started = time.monotonic()
    stop_status = "BASE_TARGET_REACHED"
    with Cadical195(bootstrap_with=clauses) as solver:
        for _ in range(min(base_model_count, requested_count)):
            phases = [
                variable if rng.getrandbits(1) else -variable
                for variable in range(1, len(orbits) + 1)
            ]
            rng.shuffle(phases)
            solver.set_phases(phases)
            solver.conf_budget(conflict_budget)
            outcome = solver.solve_limited()
            if outcome is not True:
                stop_status = (
                    "OBSERVED_EXHAUSTED_UNCHECKED"
                    if outcome is False
                    else "BUDGET_EXHAUSTED"
                )
                break
            model = complete_truth(solver.get_model(), len(orbits))
            assignment = tuple(
                model[variable] for variable in range(1, len(orbits) + 1)
            )
            if not assignment_satisfies(assignment, clauses):
                raise AssertionError("side model failed direct formula replay")
            if assignment in base_models:
                raise AssertionError("side blocking clause produced a duplicate")
            base_models.append(assignment)
            solver.add_clause(
                [
                    -variable if value else variable
                    for variable, value in enumerate(assignment, start=1)
                ]
            )
    if not base_models:
        raise RuntimeError(f"no side model found for {cycle_count} cycles")

    models = list(base_models)
    observed = set(models)
    attempts = 0
    maximum_attempts = max(10_000, 100 * requested_count)
    while len(models) < requested_count and attempts < maximum_attempts:
        attempts += 1
        source = base_models[rng.randrange(len(base_models))]
        cycle_permutation = list(range(cycle_count))
        rng.shuffle(cycle_permutation)
        shifts = tuple(rng.randrange(PRIME) for _ in range(cycle_count))
        transformed = transformed_side_model(
            source,
            orbits,
            edge_variable,
            tuple(cycle_permutation),
            shifts,
            1 if rng.getrandbits(1) else -1,
        )
        if transformed in observed:
            continue
        if not assignment_satisfies(transformed, clauses):
            raise AssertionError("relabelled side model failed formula replay")
        observed.add(transformed)
        models.append(transformed)
    if len(models) != requested_count:
        raise RuntimeError("could not construct the requested distinct side pool")
    encoded = ["".join("1" if value else "0" for value in model) for model in models]
    pool_hash = hashlib.sha256(("\n".join(encoded) + "\n").encode("ascii")).hexdigest()
    pairwise_distances = [
        sum(left != right for left, right in zip(models[i], models[j]))
        for i in range(len(models))
        for j in range(i)
    ]
    metadata = {
        "cycle_count": cycle_count,
        "order": PRIME * cycle_count,
        "variable_count": len(orbits),
        "clause_count": len(clauses),
        "requested_count": requested_count,
        "base_model_count": len(base_models),
        "base_stop_status": stop_status,
        "normalizer_augmentation_attempts": attempts,
        "model_pool_sha256": pool_hash,
        "minimum_pairwise_hamming_distance": min(pairwise_distances, default=0),
        "maximum_pairwise_hamming_distance": max(pairwise_distances, default=0),
        "runtime_seconds": time.monotonic() - started,
    }
    return orbits, clauses, models, metadata


def map_local_orbits(
    local_orbits: tuple[tuple[tuple[int, int], ...], ...],
    starting_cycle: int,
    global_edge_variable: dict[tuple[int, int], int],
) -> tuple[int, ...]:
    shift = PRIME * starting_cycle
    mapped = tuple(
        global_edge_variable[
            tuple(vertex + shift for vertex in orbit[0])
        ]
        for orbit in local_orbits
    )
    if len(set(mapped)) != len(local_orbits):
        raise AssertionError("local side variables did not map injectively")
    return mapped


def gluing_units(
    t_case: int,
    a_model: tuple[bool, ...],
    b_model: tuple[bool, ...],
    local_orbits: dict[int, tuple[tuple[tuple[int, int], ...], ...]],
    edge_variable: dict[tuple[int, int], int],
) -> tuple[int, ...]:
    """Fix the two sides; side B is complemented to enforce R(5,4)."""
    a_cycles = t_case
    b_cycles = CYCLE_COUNT - t_case
    map_a = map_local_orbits(local_orbits[a_cycles], 0, edge_variable)
    map_b = map_local_orbits(local_orbits[b_cycles], t_case, edge_variable)
    units = list(fixed_vertex_units(t_case, edge_variable))
    units.extend(
        variable if value else -variable
        for variable, value in zip(map_a, a_model)
    )
    units.extend(
        -variable if value else variable
        for variable, value in zip(map_b, b_model)
    )
    if len(units) != len(set(map(abs, units))):
        raise AssertionError("side-gluing units overlap")
    expected_fixed = 157 if t_case == 6 else 154
    if len(units) != expected_fixed:
        raise AssertionError("unexpected number of side-gluing fixed variables")
    return tuple(units)


def decode_model(
    model: list[int], edge_variable: dict[tuple[int, int], int]
) -> list[int]:
    truth = complete_truth(model, EXPECTED_VARIABLES)
    adjacency = [0] * ORDER
    for (left, right), variable in edge_variable.items():
        if truth[variable]:
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return adjacency


def forbidden_counts(adjacency: list[int]) -> tuple[int, int]:
    clique_count = 0
    independent_count = 0
    for vertices in itertools.combinations(range(ORDER), 5):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        clique_count += edge_count == 10
        independent_count += edge_count == 0
    return clique_count, independent_count


def automorphism_valid(adjacency: list[int]) -> bool:
    image = permutation()
    return all(
        ((adjacency[left] >> right) & 1)
        == (
            (
                adjacency[min(image[left], image[right])]
                >> max(image[left], image[right])
            )
            & 1
        )
        for left, right in itertools.combinations(range(ORDER), 2)
    )


def model_satisfies(
    model: list[int], clauses: Iterable[tuple[int, ...]]
) -> bool:
    truth = complete_truth(model, EXPECTED_VARIABLES)
    return all(
        any(truth[abs(literal)] == (literal > 0) for literal in clause)
        for clause in clauses
    )


def dual_verify_candidate(
    adjacency: list[int],
    candidate_path: Path,
    exhaustive_verifier: Path,
    bitset_verifier: Path,
) -> dict[str, object]:
    graph6 = encode_graph6(adjacency)
    payload = (graph6 + "\n").encode("ascii")
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    if candidate_path.exists():
        raise FileExistsError(f"refusing to overwrite {candidate_path}")
    candidate_path.write_bytes(payload)
    candidate_sha256 = hashlib.sha256(payload).hexdigest()
    commands = {
        "python_exhaustive": [sys.executable, str(exhaustive_verifier), str(candidate_path)],
        "cpp_bitset": [str(bitset_verifier), str(candidate_path)],
    }
    results: dict[str, object] = {}
    for label, command in commands.items():
        completed = subprocess.run(
            command, capture_output=True, text=True, check=False, timeout=120
        )
        parsed = None
        if completed.stdout.strip():
            parsed = json.loads(completed.stdout)
        results[label] = {
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "json": parsed,
        }
    python_result = results["python_exhaustive"]["json"]  # type: ignore[index]
    cpp_result = results["cpp_bitset"]["json"]  # type: ignore[index]
    valid = (
        results["python_exhaustive"]["returncode"] == 0  # type: ignore[index]
        and results["cpp_bitset"]["returncode"] == 0  # type: ignore[index]
        and python_result.get("valid") is True
        and python_result.get("objective") == 0
        and python_result.get("n") == ORDER
        and python_result.get("input_sha256") == candidate_sha256
        and cpp_result.get("valid") is True
        and cpp_result.get("clique_k_found") is False
        and cpp_result.get("independent_k_found") is False
    )
    return {
        "valid": valid,
        "candidate_path": str(candidate_path.resolve()),
        "candidate_sha256": candidate_sha256,
        "graph6": graph6,
        "graph6_line_sha256": candidate_sha256,
        "verifiers": results,
    }


def raw_search(
    clauses: list[tuple[int, ...]],
    edge_variable: dict[tuple[int, int], int],
    solvers: tuple[str, ...],
    attempts: int,
    conflict_budget: int,
    seed: int,
) -> tuple[list[dict[str, object]], list[int] | None]:
    try:
        from pysat import solvers as pysat_solvers
    except ImportError as error:
        raise RuntimeError("Python-SAT is required for the constructive search") from error
    records: list[dict[str, object]] = []
    for solver_offset, solver_name in enumerate(solvers):
        solver_class = getattr(pysat_solvers, solver_name)
        for attempt in range(attempts):
            rng = random.Random(seed + 10_000 * solver_offset + attempt)
            with solver_class(bootstrap_with=clauses, use_timer=True) as solver:
                for t_case in (6, 7):
                    phases = [
                        variable if rng.getrandbits(1) else -variable
                        for variable in range(1, EXPECTED_VARIABLES + 1)
                    ]
                    rng.shuffle(phases)
                    solver.set_phases(phases)
                    solver.conf_budget(conflict_budget)
                    before = solver.accum_stats()
                    started = time.monotonic()
                    outcome = solver.solve_limited(
                        assumptions=fixed_vertex_units(t_case, edge_variable)
                    )
                    after = solver.accum_stats()
                    record = {
                        "solver": solver_name,
                        "attempt": attempt,
                        "t_case": t_case,
                        "status": (
                            "SAT"
                            if outcome is True
                            else "OBSERVED_UNSAT_UNCHECKED"
                            if outcome is False
                            else "BUDGET_EXHAUSTED"
                        ),
                        "negative_certified": False,
                        "conflict_budget": conflict_budget,
                        "conflicts": after.get("conflicts", 0)
                        - before.get("conflicts", 0),
                        "decisions": after.get("decisions", 0)
                        - before.get("decisions", 0),
                        "propagations": after.get("propagations", 0)
                        - before.get("propagations", 0),
                        "wall_seconds": time.monotonic() - started,
                    }
                    records.append(record)
                    print(json.dumps({"event": "raw_case_complete", **record}), flush=True)
                    if outcome is True:
                        return records, solver.get_model()
    return records, None


def pair_schedule(
    left_count: int, right_count: int, seed: int
) -> list[tuple[int, int]]:
    pairs = list(itertools.product(range(left_count), range(right_count)))
    random.Random(seed).shuffle(pairs)
    return pairs


def gluing_search(
    clauses: list[tuple[int, ...]],
    edge_variable: dict[tuple[int, int], int],
    local_orbits: dict[int, tuple[tuple[tuple[int, int], ...], ...]],
    pools: dict[int, list[tuple[bool, ...]]],
    stages: tuple[tuple[str, int, int], ...],
    seed: int,
) -> tuple[list[dict[str, object]], list[int] | None]:
    try:
        from pysat import solvers as pysat_solvers
    except ImportError as error:
        raise RuntimeError("Python-SAT is required for the constructive search") from error
    records: list[dict[str, object]] = []
    offsets = {6: 0, 7: 0}
    schedules = {
        t_case: pair_schedule(
            len(pools[t_case]), len(pools[CYCLE_COUNT - t_case]), seed + t_case
        )
        for t_case in (6, 7)
    }
    for stage_index, (solver_name, conflict_budget, pair_count) in enumerate(stages):
        solver_class = getattr(pysat_solvers, solver_name)
        for t_case in (7, 6):
            schedule = schedules[t_case]
            start = offsets[t_case]
            stop = min(start + pair_count, len(schedule))
            offsets[t_case] = stop
            rng = random.Random(seed + 1_000_000 * stage_index + t_case)
            with solver_class(bootstrap_with=clauses, use_timer=True) as solver:
                for schedule_index in range(start, stop):
                    left_index, right_index = schedule[schedule_index]
                    units = gluing_units(
                        t_case,
                        pools[t_case][left_index],
                        pools[CYCLE_COUNT - t_case][right_index],
                        local_orbits,
                        edge_variable,
                    )
                    phases = [
                        variable if rng.getrandbits(1) else -variable
                        for variable in range(1, EXPECTED_VARIABLES + 1)
                    ]
                    rng.shuffle(phases)
                    solver.set_phases(phases)
                    solver.conf_budget(conflict_budget)
                    before = solver.accum_stats()
                    started = time.monotonic()
                    outcome = solver.solve_limited(assumptions=units)
                    after = solver.accum_stats()
                    record = {
                        "stage_index": stage_index,
                        "solver": solver_name,
                        "conflict_budget": conflict_budget,
                        "t_case": t_case,
                        "schedule_index": schedule_index,
                        "left_model_index": left_index,
                        "right_model_index": right_index,
                        "fixed_variable_count": len(units),
                        "free_variable_count": EXPECTED_VARIABLES - len(units),
                        "status": (
                            "SAT"
                            if outcome is True
                            else "OBSERVED_UNSAT_UNCHECKED"
                            if outcome is False
                            else "BUDGET_EXHAUSTED"
                        ),
                        "negative_certified": False,
                        "conflicts": after.get("conflicts", 0)
                        - before.get("conflicts", 0),
                        "decisions": after.get("decisions", 0)
                        - before.get("decisions", 0),
                        "propagations": after.get("propagations", 0)
                        - before.get("propagations", 0),
                        "wall_seconds": time.monotonic() - started,
                    }
                    records.append(record)
                    if len(records) % 32 == 0 or outcome is True:
                        print(
                            json.dumps(
                                {
                                    "event": "gluing_progress",
                                    "completed": len(records),
                                    **record,
                                }
                            ),
                            flush=True,
                        )
                    if outcome is True:
                        return records, solver.get_model()
            gc.collect()
    return records, None


def parse_stage(raw: str) -> tuple[str, int, int]:
    fields = raw.split(":")
    if len(fields) != 3:
        raise ValueError("stage must have SOLVER:BUDGET:PAIRS form")
    solver, budget_raw, pairs_raw = fields
    if solver not in ("Cadical195", "Glucose4", "MapleChrono"):
        raise ValueError(f"unsupported stage solver: {solver}")
    budget, pairs = int(budget_raw), int(pairs_raw)
    if budget <= 0 or pairs <= 0:
        raise ValueError("stage budget and pair count must be positive")
    return solver, budget, pairs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("raw", "glue", "both"), default="both")
    parser.add_argument("--seed", type=int, default=20_260_727)
    parser.add_argument("--raw-budget", type=int, default=100_000)
    parser.add_argument("--raw-attempts", type=int, default=2)
    parser.add_argument(
        "--raw-solvers",
        default="Cadical195,Glucose4,MapleChrono",
    )
    parser.add_argument("--pool-6", type=int, default=64)
    parser.add_argument("--pool-7", type=int, default=96)
    parser.add_argument("--pool-8", type=int, default=64)
    parser.add_argument("--base-side-models", type=int, default=16)
    parser.add_argument("--side-budget", type=int, default=300_000)
    parser.add_argument(
        "--stage",
        action="append",
        default=[],
        help="repeatable SOLVER:BUDGET:PAIRS gluing stage",
    )
    parser.add_argument("--result", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument(
        "--exhaustive-verifier",
        type=Path,
        default=Path("verify/exhaustive_verify.py"),
    )
    parser.add_argument(
        "--bitset-verifier",
        type=Path,
        default=Path("build/bitset_verify"),
    )
    args = parser.parse_args()
    if (
        args.raw_budget <= 0
        or args.raw_attempts <= 0
        or min(args.pool_6, args.pool_7, args.pool_8) <= 0
        or args.base_side_models <= 0
        or args.side_budget <= 0
    ):
        parser.error("budgets, attempts, and pool sizes must be positive")
    raw_solvers = tuple(name for name in args.raw_solvers.split(",") if name)
    if any(
        name not in ("Cadical195", "Glucose4", "MapleChrono")
        for name in raw_solvers
    ):
        parser.error("unsupported raw solver")
    try:
        stages = tuple(map(parse_stage, args.stage)) or (
            ("Cadical195", 5_000, 256),
            ("Glucose4", 20_000, 128),
            ("MapleChrono", 50_000, 64),
        )
    except ValueError as error:
        parser.error(str(error))

    started = time.monotonic()
    edge_variable, orbits, clauses, formula = build_exact_formula()
    result: dict[str, object] = {
        "search": SEARCH_ID,
        "evidence_label": "REPRODUCIBLE_COMPUTATIONAL_OBSERVATION",
        "claim_boundary": (
            "A returned SAT model is independently replayed over all 962,598 "
            "five-sets and then checked by two standalone verifiers. Negative "
            "bounded outcomes have no proof and do not exclude this symmetry "
            "class or arbitrary order-43 graphs."
        ),
        "cycle_type": "3^14 1^1",
        "formula": formula,
        "normalization": {
            "degree_bound": [18, 24],
            "fixed_degree_multiple": 3,
            "possible_fixed_degrees": [18, 21, 24],
            "possible_neighbor_cycle_counts": [6, 7, 8],
            "complement_pair": [6, 8],
            "searched_cases": [6, 7],
            "cycle_relabeling": "S14 fixes the first t cycles as neighbors",
            "coverage": "t=6 and t=7 cover t=6,7,8 up to complement",
        },
        "configuration": {
            "mode": args.mode,
            "seed": args.seed,
            "raw_solvers": raw_solvers,
            "raw_budget": args.raw_budget,
            "raw_attempts": args.raw_attempts,
            "side_pool_counts": {6: args.pool_6, 7: args.pool_7, 8: args.pool_8},
            "base_side_models": args.base_side_models,
            "side_budget": args.side_budget,
            "stages": stages,
        },
    }
    model: list[int] | None = None
    if args.mode in ("raw", "both"):
        raw_records, model = raw_search(
            clauses,
            edge_variable,
            raw_solvers,
            args.raw_attempts,
            args.raw_budget,
            args.seed,
        )
        result["raw_records"] = raw_records
        result["raw_status_counts"] = dict(
            sorted(Counter(record["status"] for record in raw_records).items())
        )

    if model is None and args.mode in ("glue", "both"):
        local_orbits: dict[
            int, tuple[tuple[tuple[int, int], ...], ...]
        ] = {}
        pools: dict[int, list[tuple[bool, ...]]] = {}
        pool_metadata: dict[int, dict[str, object]] = {}
        for cycle_count, requested in (
            (6, args.pool_6),
            (7, args.pool_7),
            (8, args.pool_8),
        ):
            side_orbits, _, side_models, metadata = diverse_side_models(
                cycle_count,
                requested,
                args.base_side_models,
                args.side_budget,
                args.seed + cycle_count,
            )
            local_orbits[cycle_count] = side_orbits
            pools[cycle_count] = side_models
            pool_metadata[cycle_count] = metadata
            print(json.dumps({"event": "side_pool_complete", **metadata}), flush=True)
        result["side_pools"] = pool_metadata
        gluing_records, model = gluing_search(
            clauses,
            edge_variable,
            local_orbits,
            pools,
            stages,
            args.seed,
        )
        result["gluing_records"] = gluing_records
        result["gluing_status_counts"] = dict(
            sorted(Counter(record["status"] for record in gluing_records).items())
        )

    construction = None
    if model is not None:
        if not model_satisfies(model, clauses):
            raise AssertionError("SAT model failed direct exact-CNF replay")
        adjacency = decode_model(model, edge_variable)
        counts = forbidden_counts(adjacency)
        if counts != (0, 0) or not automorphism_valid(adjacency):
            raise AssertionError("SAT model failed exhaustive in-process replay")
        if args.candidate is None:
            raise RuntimeError("--candidate is required when a construction is found")
        verification = dual_verify_candidate(
            adjacency,
            args.candidate,
            args.exhaustive_verifier,
            args.bitset_verifier,
        )
        if not verification["valid"]:
            raise AssertionError("SAT model failed standalone dual verification")
        construction = {
            "verification": verification,
            "forbidden_counts": {
                "clique_5": counts[0],
                "independent_5": counts[1],
            },
            "automorphism_replay": True,
            "true_primary_variables": [
                literal for literal in model if 0 < literal <= EXPECTED_VARIABLES
            ],
        }
        result["evidence_label"] = "CERTIFIED_CONSTRUCTION"
    result["construction"] = construction
    result["runtime_seconds"] = time.monotonic() - started
    result["maximum_resident_set_bytes"] = resource.getrusage(
        resource.RUSAGE_SELF
    ).ru_maxrss
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.result is not None:
        args.result.parent.mkdir(parents=True, exist_ok=True)
        if args.result.exists():
            raise FileExistsError(f"refusing to overwrite {args.result}")
        args.result.write_text(payload, encoding="utf-8")
    print(
        json.dumps(
            {
                key: value
                for key, value in result.items()
                if key not in ("raw_records", "gluing_records")
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 10 if construction is not None else 0


if __name__ == "__main__":
    raise SystemExit(main())
