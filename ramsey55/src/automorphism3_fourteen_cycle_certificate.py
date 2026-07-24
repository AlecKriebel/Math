#!/usr/bin/env python3
"""Generate an exact symmetry-reduced CNF for cycle type 3^14 1.

The prescribed permutation consists of fourteen 3-cycles followed by the
unique fixed vertex 42.  In a (5,5;43)-graph every degree is between 18 and
24.  Consequently the fixed vertex meets 6, 7, or 8 moved cycles.  Taking
the graph complement exchanges 6 and 8, and permuting the fourteen cycle
blocks lets us sort the incidence bits.  The default ``cover`` formula
therefore retains exactly the two normalized prefix lengths 6 and 7.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import automorphism_orbit_cnf as orbit_cnf  # noqa: E402


GENERATOR_ID = "ramsey55_order3_fourteen_cycle_symmetry_cnf_generator_v1"
PRIME = 3
CYCLE_COUNT = 14
FIXED_VERTEX = 42
CYCLE_TYPE = "3^14 1"
MODES = ("cover", "6", "7", "6-reduced", "7-reduced")
FULL_SIGNATURE_COUNT = 320_593
FULL_BASE_CLAUSE_COUNT = 641_186
FULL_SIGNATURE_SIZE_HISTOGRAM = {
    5: 91,
    6: 182,
    7: 91,
    8: 3_276,
    9: 19_656,
    10: 297_297,
}


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def root_cycle_variables(
    edge_variable: dict[tuple[int, int], int],
) -> tuple[int, ...]:
    """Return the fixed-vertex incidence variable for each moved cycle."""
    return tuple(
        edge_variable[(PRIME * cycle, FIXED_VERTEX)]
        for cycle in range(CYCLE_COUNT)
    )


def symmetry_clauses(
    edge_variable: dict[tuple[int, int], int], mode: str
) -> tuple[tuple[int, ...], ...]:
    """Return exact prefix-normalization clauses for the requested cover."""
    if mode not in MODES:
        raise ValueError(f"unsupported mode: {mode}")
    variables = root_cycle_variables(edge_variable)
    if mode != "cover":
        adjacent = int(mode.split("-", 1)[0])
        return tuple(
            (variable,) if index < adjacent else (-variable,)
            for index, variable in enumerate(variables)
        )

    # x_i OR not x_(i+1) sorts the incidence bits into a true prefix.
    clauses = [
        (left, -right)
        for left, right in zip(variables, variables[1:])
    ]
    # The sorted prefix has length at least six and at most seven.
    clauses.extend(((variables[5],), (-variables[7],)))
    if len(clauses) != 15:
        raise AssertionError("unexpected symmetry clause count")
    return tuple(clauses)


def simplify_under_root_units(
    clauses: tuple[tuple[int, ...], ...],
    edge_variable: dict[tuple[int, int], int],
    adjacent: int,
) -> tuple[tuple[int, ...], ...]:
    """Simplify and deduplicate clauses under one fixed root neighborhood.

    The returned clauses, together with the fourteen root units, are
    equisatisfiable with the original clauses plus those same units.
    """
    variables = root_cycle_variables(edge_variable)
    assignment = {
        variable: index < adjacent
        for index, variable in enumerate(variables)
    }
    result: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()
    for clause in clauses:
        if any(
            assignment.get(abs(literal)) == (literal > 0)
            for literal in clause
            if abs(literal) in assignment
        ):
            continue
        residual = tuple(
            literal for literal in clause if abs(literal) not in assignment
        )
        if residual not in seen:
            seen.add(residual)
            result.append(residual)
    return tuple(result)


def build_formula(
    mode: str,
) -> tuple[
    tuple[tuple[tuple[int, int], ...], ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
    dict[tuple[int, int], int],
]:
    permutation = orbit_cnf.canonical_permutation(PRIME, CYCLE_COUNT)
    edge_variable, orbits = orbit_cnf.edge_orbit_table(permutation)
    signatures = orbit_cnf.ramsey_signatures(edge_variable)
    base: list[tuple[int, ...]] = []
    for signature in signatures:
        base.append(signature)
        base.append(tuple(-variable for variable in signature))
    full_base = tuple(base)
    if mode.endswith("-reduced"):
        base_clauses = simplify_under_root_units(
            full_base, edge_variable, int(mode.split("-", 1)[0])
        )
    else:
        base_clauses = full_base
    extra = symmetry_clauses(edge_variable, mode)
    return orbits, base_clauses, extra, edge_variable


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
    parser.add_argument("--mode", choices=MODES, default="cover")
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()

    orbits, base, extra, edge_variable = build_formula(args.mode)
    clauses = (*base, *extra)
    write_dimacs(args.cnf, len(orbits), clauses)
    source = Path(__file__).resolve()
    generic_source = Path(orbit_cnf.__file__).resolve()
    metadata = {
        "generator": GENERATOR_ID,
        "claim_scope": (
            "Order-43 Ramsey(5,5) graphs admitting an automorphism with "
            "cycle type 3^14 1 only."
        ),
        "order": 43,
        "clique_size": 5,
        "automorphism_order": PRIME,
        "cycle_count": CYCLE_COUNT,
        "fixed_point_count": 1,
        "fixed_vertex": FIXED_VERTEX,
        "cycle_type": CYCLE_TYPE,
        "mode": args.mode,
        "variable_count": len(orbits),
        "edge_orbit_size_histogram": {
            str(size): count
            for size, count in sorted(Counter(map(len, orbits)).items())
        },
        "unique_orbit_signature_count": FULL_SIGNATURE_COUNT,
        "signature_size_histogram": {
            str(size): count
            for size, count in FULL_SIGNATURE_SIZE_HISTOGRAM.items()
        },
        "base_clause_count": len(base),
        "full_base_clause_count": (
            FULL_BASE_CLAUSE_COUNT
            if args.mode.endswith("-reduced")
            else len(base)
        ),
        "root_simplification": {
            "applied": args.mode.endswith("-reduced"),
            "equivalence": (
                "Delete clauses satisfied by the fourteen root units, remove "
                "their falsified literals from the remaining clauses, and "
                "deduplicate. Together with the retained units this is "
                "equisatisfiable with the full orbit formula and units."
            ),
        },
        "symmetry_breaking_clause_count": len(extra),
        "clause_count": len(clauses),
        "root_cycle_variables": list(root_cycle_variables(edge_variable)),
        "degree_reduction": {
            "global_degree_interval": [18, 24],
            "justification": (
                "A neighborhood is a (4,5)-Ramsey graph and a "
                "nonneighborhood is a (5,4)-Ramsey graph; R(4,5)=25."
            ),
            "fixed_vertex_degree_expression": "3*m",
            "allowed_m_before_complement": [6, 7, 8],
            "complement_action_on_m": "m -> 14-m",
            "normalized_m": [6, 7],
        },
        "symmetry_cover": {
            "cycle_block_relabeling": (
                "The S_14 action permuting whole 3-cycle blocks centralizes "
                "the canonical automorphism and sorts root incidences."
            ),
            "cover_mode_prefix_lengths": [6, 7],
            "cover_mode_clause_order": (
                "13 adjacent prefix-order clauses, then units x_6 and not x_8."
            ),
        },
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256_file(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "generator_path": str(source),
        "generator_sha256": sha256_file(source),
        "generic_orbit_source_path": str(generic_source),
        "generic_orbit_source_sha256": sha256_file(generic_source),
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
