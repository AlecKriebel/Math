#!/usr/bin/env python3
"""Add exact weighted degree bounds to the normalized 3^14 1 cases."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import automorphism3_fourteen_cycle_certificate as base  # noqa: E402


GENERATOR_ID = "ramsey55_order3_fourteen_cycle_degree_cnf_generator_v1"
LOWER_DEGREE = 18
UPPER_DEGREE = 24
TRACKED_THRESHOLD = UPPER_DEGREE + 1


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def degree_terms(
    orbits: tuple[tuple[tuple[int, int], ...], ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Return primary variable/weight terms for one vertex per 3-cycle."""
    variable_of = {
        edge: variable
        for variable, orbit in enumerate(orbits, start=1)
        for edge in orbit
    }
    result: list[tuple[tuple[int, int], ...]] = []
    for cycle in range(base.CYCLE_COUNT):
        vertex = base.PRIME * cycle
        weights: Counter[int] = Counter()
        for other in range(43):
            if other == vertex:
                continue
            edge = tuple(sorted((vertex, other)))
            weights[variable_of[edge]] += 1
        terms = tuple(sorted(weights.items()))
        if (
            len(terms) != 41
            or sum(weight for _, weight in terms) != 42
            or Counter(weight for _, weight in terms) != Counter({1: 40, 2: 1})
        ):
            raise AssertionError("unexpected moved-vertex degree expression")
        result.append(terms)
    return tuple(result)


def _positive(reference: int | bool) -> int | bool:
    return reference


def _negative(reference: int | bool) -> int | bool:
    return not reference if type(reference) is bool else -reference


def _append_simplified_clause(
    clauses: list[tuple[int, ...]], atoms: tuple[int | bool, ...]
) -> None:
    if any(atom is True for atom in atoms):
        return
    literals: list[int] = []
    seen: set[int] = set()
    for atom in atoms:
        if atom is False:
            continue
        literal = int(atom)
        if -literal in seen:
            return
        if literal not in seen:
            seen.add(literal)
            literals.append(literal)
    clauses.append(tuple(literals))


def weighted_degree_clauses(
    orbits: tuple[tuple[tuple[int, int], ...], ...],
    first_auxiliary: int,
) -> tuple[tuple[tuple[int, ...], ...], int, dict[str, object]]:
    """Encode exact cumulative ``sum >= j`` states through threshold 25."""
    clauses: list[tuple[int, ...]] = []
    next_variable = first_auxiliary
    final_states: list[tuple[int, int]] = []
    term_sets = degree_terms(orbits)
    for terms in term_sets:
        previous: dict[int, int | bool] = {
            threshold: False
            for threshold in range(1, TRACKED_THRESHOLD + 1)
        }
        for primary, weight in terms:
            current: dict[int, int] = {}
            for threshold in range(1, TRACKED_THRESHOLD + 1):
                state = next_variable
                next_variable += 1
                current[threshold] = state
                unchanged = previous[threshold]
                augmented: int | bool = (
                    True
                    if threshold <= weight
                    else previous[threshold - weight]
                )
                # state <-> unchanged OR (primary AND augmented)
                _append_simplified_clause(
                    clauses, (_negative(unchanged), state)
                )
                _append_simplified_clause(
                    clauses,
                    (-primary, _negative(augmented), state),
                )
                _append_simplified_clause(
                    clauses,
                    (-state, _positive(unchanged), primary),
                )
                _append_simplified_clause(
                    clauses,
                    (-state, _positive(unchanged), _positive(augmented)),
                )
            previous = current
        clauses.append((int(previous[LOWER_DEGREE]),))
        clauses.append((-int(previous[TRACKED_THRESHOLD]),))
        final_states.append(
            (
                int(previous[LOWER_DEGREE]),
                int(previous[TRACKED_THRESHOLD]),
            )
        )
    metadata = {
        "constrained_moved_vertex_orbits": len(term_sets),
        "terms_per_degree_expression": 41,
        "weight_histogram_per_expression": {"1": 40, "2": 1},
        "weight_sum_per_expression": 42,
        "tracked_thresholds": [1, TRACKED_THRESHOLD],
        "degree_interval": [LOWER_DEGREE, UPPER_DEGREE],
        "auxiliary_variable_count": next_variable - first_auxiliary,
        "degree_clause_count": len(clauses),
        "final_state_variables": [list(pair) for pair in final_states],
    }
    return tuple(clauses), next_variable, metadata


def write_dimacs(
    path: Path, variable_count: int, clauses: tuple[tuple[int, ...], ...]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root-cycles", type=int, choices=(6, 7), required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()

    mode = f"{args.root_cycles}-reduced"
    orbits, reduced_base, root_units, _ = base.build_formula(mode)
    degree, next_variable, degree_metadata = weighted_degree_clauses(
        orbits, len(orbits) + 1
    )
    variable_count = next_variable - 1
    clauses = (*reduced_base, *root_units, *degree)
    write_dimacs(args.cnf, variable_count, clauses)
    source = Path(__file__).resolve()
    base_source = Path(base.__file__).resolve()
    metadata = {
        "generator": GENERATOR_ID,
        "claim_scope": (
            "One normalized root-neighborhood case within order-43 "
            "Ramsey(5,5) graphs admitting cycle type 3^14 1."
        ),
        "order": 43,
        "clique_size": 5,
        "automorphism_order": 3,
        "cycle_count": 14,
        "fixed_point_count": 1,
        "cycle_type": base.CYCLE_TYPE,
        "root_neighbor_cycle_count": args.root_cycles,
        "base_mode": mode,
        "primary_variable_count": len(orbits),
        "variable_count": variable_count,
        "full_ramsey_clause_count": base.FULL_BASE_CLAUSE_COUNT,
        "reduced_ramsey_clause_count": len(reduced_base),
        "root_unit_clause_count": len(root_units),
        **degree_metadata,
        "degree_bound_justification": (
            "Every vertex degree is 18--24 because each neighborhood is a "
            "(4,5)-Ramsey graph and each nonneighborhood a (5,4)-Ramsey "
            "graph, using R(4,5)=25."
        ),
        "clause_count": len(clauses),
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256_file(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "generator_path": str(source),
        "generator_sha256": sha256_file(source),
        "base_generator_path": str(base_source),
        "base_generator_sha256": sha256_file(base_source),
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
