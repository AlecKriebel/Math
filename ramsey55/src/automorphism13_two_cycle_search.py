#!/usr/bin/env python3
"""Low-storage search for the order-13 cycle type 13^2 1^17.

This program covers only the two-moved-cycle class. It does not cover the
distinct order-13 cycle type 13^1 1^30. Negative solver outcomes are
observations unless accompanied by an external proof certificate.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import itertools
import json
import random
import resource
import sys
import time
from collections import Counter
from pathlib import Path

from automorphism_orbit_cnf import (
    canonical_permutation,
    edge_orbit_table,
    ramsey_signatures,
)
from graph_io import encode_graph6


SEARCH_ID = "ramsey55_order13_two_cycle_group_split_search_v1"
ORDER = 43
PRIME = 13
CYCLE_COUNT = 2
FIXED_VERTICES = tuple(range(26, 43))
EXPECTED_VARIABLES = 195
EXPECTED_SIGNATURES = 76_132
EXPECTED_CLAUSES = 152_264
EXPECTED_DIMACS_SHA256 = (
    "089d798347c2e991ce4c3c45aa879600e3edceabae7e97bae7079b6f9a7255e3"
)


def formula() -> tuple[
    tuple[int, ...],
    dict[tuple[int, int], int],
    tuple[tuple[tuple[int, int], ...], ...],
    tuple[tuple[int, ...], ...],
]:
    image = canonical_permutation(PRIME, CYCLE_COUNT)
    edge_variable, orbits = edge_orbit_table(image)
    signatures = ramsey_signatures(edge_variable)
    return image, edge_variable, orbits, signatures


def dimacs_sha256(
    variable_count: int, signatures: tuple[tuple[int, ...], ...]
) -> str:
    state = hashlib.sha256()
    state.update(f"p cnf {variable_count} {2 * len(signatures)}\n".encode("ascii"))
    for signature in signatures:
        state.update((" ".join(map(str, signature)) + " 0\n").encode("ascii"))
        state.update(
            (
                " ".join(str(-variable) for variable in signature) + " 0\n"
            ).encode("ascii")
        )
    return state.hexdigest()


def clauses(
    signatures: tuple[tuple[int, ...], ...]
) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []
    for signature in signatures:
        result.append(signature)
        result.append(tuple(-variable for variable in signature))
    return result


def normalized_group_sizes() -> tuple[int, ...]:
    """Cycle exchange maps a group of size a to one of size 17-a."""
    return tuple(range(9))


def group_assumptions(
    first_cycle_group_size: int,
    edge_variable: dict[tuple[int, int], int],
) -> tuple[int, ...]:
    if first_cycle_group_size not in normalized_group_sizes():
        raise ValueError("normalized group size must lie in 0..8")
    literals: list[int] = []
    for fixed_index, fixed_vertex in enumerate(FIXED_VERTICES):
        sees_first = fixed_index < first_cycle_group_size
        first_variable = edge_variable[(0, fixed_vertex)]
        second_variable = edge_variable[(13, fixed_vertex)]
        literals.extend(
            (
                first_variable if sees_first else -first_variable,
                -second_variable if sees_first else second_variable,
            )
        )
    if len(literals) != 34 or len(set(map(abs, literals))) != 34:
        raise AssertionError("group split must assign 34 distinct variables")
    return tuple(literals)


def decode_model(
    model: list[int],
    edge_variable: dict[tuple[int, int], int],
) -> list[int]:
    truth = {abs(literal): literal > 0 for literal in model}
    if any(variable not in truth for variable in range(1, EXPECTED_VARIABLES + 1)):
        raise AssertionError("SAT model is incomplete")
    adjacency = [0] * ORDER
    for (left, right), variable in edge_variable.items():
        if truth[variable]:
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return adjacency


def forbidden_counts(adjacency: list[int]) -> tuple[int, int]:
    cliques = 0
    independent = 0
    for vertices in itertools.combinations(range(ORDER), 5):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        cliques += edge_count == 10
        independent += edge_count == 0
    return cliques, independent


def automorphism_valid(
    adjacency: list[int], image: tuple[int, ...]
) -> bool:
    for left, right in itertools.combinations(range(ORDER), 2):
        transformed = tuple(sorted((image[left], image[right])))
        if ((adjacency[left] >> right) & 1) != (
            (adjacency[transformed[0]] >> transformed[1]) & 1
        ):
            return False
    return True


def fixed_degrees(adjacency: list[int]) -> list[int]:
    return [
        sum((adjacency[vertex] >> other) & 1 for other in FIXED_VERTICES)
        for vertex in FIXED_VERTICES
    ]


def run_search(
    conflict_budget: int,
    seed: int,
    solver_name: str,
) -> dict[str, object]:
    try:
        import pysat
        from pysat import solvers as pysat_solvers
    except ImportError as error:
        raise RuntimeError(
            "python-sat is required for search; set the pinned PYTHONPATH"
        ) from error

    started = time.monotonic()
    image, edge_variable, orbits, signatures = formula()
    orbit_histogram = Counter(map(len, orbits))
    signature_histogram = Counter(map(len, signatures))
    formula_hash = dimacs_sha256(len(orbits), signatures)
    if (
        len(orbits) != EXPECTED_VARIABLES
        or len(signatures) != EXPECTED_SIGNATURES
        or 2 * len(signatures) != EXPECTED_CLAUSES
        or orbit_histogram != Counter({13: 59, 1: 136})
        or formula_hash != EXPECTED_DIMACS_SHA256
    ):
        raise AssertionError("order-13 formula fingerprint mismatch")
    global_clauses = clauses(signatures)
    del signatures

    schedule = list(normalized_group_sizes())
    rng = random.Random(seed)
    rng.shuffle(schedule)
    records: list[dict[str, object]] = []
    construction: dict[str, object] | None = None
    solver_class = getattr(pysat_solvers, solver_name)
    with solver_class(bootstrap_with=global_clauses, use_timer=True) as solver:
        del global_clauses
        gc.collect()
        for split_index, group_size in enumerate(schedule):
            assumptions = list(group_assumptions(group_size, edge_variable))
            phases = [
                variable if rng.getrandbits(1) else -variable
                for variable in range(1, EXPECTED_VARIABLES + 1)
            ]
            rng.shuffle(phases)
            solver.set_phases(phases)
            before = solver.accum_stats()
            split_started = time.monotonic()
            solver.conf_budget(conflict_budget)
            outcome = solver.solve_limited(assumptions=assumptions)
            after = solver.accum_stats()
            record = {
                "split_index": split_index,
                "first_cycle_group_size": group_size,
                "second_cycle_group_size": 17 - group_size,
                "status": (
                    "SAT"
                    if outcome is True
                    else "OBSERVED_UNSAT_UNCHECKED"
                    if outcome is False
                    else "BUDGET_EXHAUSTED"
                ),
                "negative_certified": False,
                "wall_seconds": time.monotonic() - split_started,
                "conflicts": after.get("conflicts", 0)
                - before.get("conflicts", 0),
                "decisions": after.get("decisions", 0)
                - before.get("decisions", 0),
                "propagations": after.get("propagations", 0)
                - before.get("propagations", 0),
            }
            records.append(record)
            print(
                json.dumps(
                    {
                        "event": "split_complete",
                        **record,
                        "completed": len(records),
                        "scheduled": len(schedule),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            if outcome is True:
                model = solver.get_model()
                if model is None:
                    raise AssertionError("SAT outcome has no model")
                truth = {abs(literal): literal > 0 for literal in model}
                if any(
                    truth[abs(literal)] != (literal > 0)
                    for literal in assumptions
                ):
                    raise AssertionError("SAT model violates group assumptions")
                adjacency = decode_model(model, edge_variable)
                forbidden = forbidden_counts(adjacency)
                induced_fixed_degrees = fixed_degrees(adjacency)
                if (
                    forbidden != (0, 0)
                    or not automorphism_valid(adjacency, image)
                    or not all(5 <= degree <= 11 for degree in induced_fixed_degrees)
                ):
                    raise AssertionError("SAT model failed independent graph replay")
                graph6 = encode_graph6(adjacency)
                construction = {
                    "split_index": split_index,
                    "first_cycle_group_size": group_size,
                    "graph6": graph6,
                    "graph6_line_sha256": hashlib.sha256(
                        (graph6 + "\n").encode("ascii")
                    ).hexdigest(),
                    "true_variables": sorted(
                        variable
                        for variable in range(1, EXPECTED_VARIABLES + 1)
                        if truth[variable]
                    ),
                    "forbidden_counts": {
                        "clique_5": forbidden[0],
                        "independent_5": forbidden[1],
                    },
                    "fixed_subgraph_degree_range": [
                        min(induced_fixed_degrees),
                        max(induced_fixed_degrees),
                    ],
                    "automorphism_replay": True,
                }
                break

    status_counts = Counter(str(record["status"]) for record in records)
    return {
        "search": SEARCH_ID,
        "evidence_label": (
            "CERTIFIED_CONSTRUCTION"
            if construction is not None
            else "REPRODUCIBLE_COMPUTATIONAL_OBSERVATION"
        ),
        "claim_boundary": (
            "This covers only cycle type 13^2 1^17, not 13^1 1^30. A SAT "
            "model is independently replayed over all five-sets. Negative "
            "outcomes have no proof certificates and do not certify "
            "nonexistence."
        ),
        "cycle_type": "13^2 1^17",
        "excluded_cycle_types": ["13^1 1^30"],
        "formula": {
            "variable_count": len(orbits),
            "edge_orbit_size_histogram": dict(sorted(orbit_histogram.items())),
            "unique_signature_count": EXPECTED_SIGNATURES,
            "signature_size_histogram": dict(
                sorted(signature_histogram.items())
            ),
            "clause_count": EXPECTED_CLAUSES,
            "dimacs_sha256_without_materialization": formula_hash,
        },
        "normalization": {
            "global_degree_bound": [18, 24],
            "moved_cycle_neighbors_per_fixed_vertex": 1,
            "fixed_subgraph_degree_bound": [5, 11],
            "cycle_exchange_normalized_group_sizes": list(
                normalized_group_sizes()
            ),
            "complete_group_split_count": 9,
        },
        "solver": {
            "name": solver_name,
            "pysat_version": pysat.__version__,
            "conflict_budget_per_split": conflict_budget,
            "seed": seed,
        },
        "scheduled_split_count": len(schedule),
        "visited_split_count": len(records),
        "status_counts": dict(sorted(status_counts.items())),
        "construction": construction,
        "records": records,
        "runtime_seconds": time.monotonic() - started,
        "maximum_resident_set_bytes": resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--conflict-budget", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=20_261_313)
    parser.add_argument(
        "--solver",
        choices=("Cadical195", "Glucose4", "MapleChrono"),
        default="Cadical195",
    )
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()
    if args.conflict_budget <= 0:
        parser.error("--conflict-budget must be positive")
    result = run_search(args.conflict_budget, args.seed, args.solver)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.result is not None:
        args.result.parent.mkdir(parents=True, exist_ok=True)
        args.result.write_text(payload, encoding="utf-8")
    print(json.dumps({"event": "final", **result}, sort_keys=True), flush=True)
    return 10 if result["construction"] is not None else 0


if __name__ == "__main__":
    raise SystemExit(main())
