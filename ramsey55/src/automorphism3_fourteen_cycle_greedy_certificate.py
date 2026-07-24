#!/usr/bin/env python3
"""Exact greedy normalizer quotient for the cycle type 3^14 1 cases."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import automorphism3_fourteen_cycle_certificate as base  # noqa: E402
import automorphism3_fourteen_cycle_degree_certificate as degree  # noqa: E402
from automorphism3_fourteen_cycle_normalizer_certificate import (  # noqa: E402
    lexicographic_ge_clauses,
)


GENERATOR_ID = "ramsey55_order3_fourteen_cycle_greedy_normalizer_cnf_v1"


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def oriented_profile(
    edge_variable: dict[tuple[int, int], int],
    candidate_cycle: int,
    prefix_cycles: range,
    phase_shift: int,
) -> tuple[int, ...]:
    """Profile after cyclically shifting the candidate block."""
    if phase_shift not in (0, 1, 2):
        raise ValueError("phase shift must be modulo three")
    result = [
        edge_variable[
            (3 * candidate_cycle, 3 * candidate_cycle + 1)
        ]
    ]
    for previous in prefix_cycles:
        result.extend(
            edge_variable[
                tuple(
                    sorted(
                        (
                            3 * previous,
                            3 * candidate_cycle
                            + (offset + phase_shift) % 3,
                        )
                    )
                )
            ]
            for offset in range(3)
        )
    return tuple(result)


def greedy_normalizer_clauses(
    edge_variable: dict[tuple[int, int], int],
    root_cycles: int,
    first_auxiliary: int,
) -> tuple[tuple[tuple[int, ...], ...], int, dict[str, int]]:
    """Canonicalize residual blocks and phases by greedy full profiles."""
    if root_cycles not in (6, 7):
        raise ValueError("normalized root case must be 6 or 7")
    clauses: list[tuple[int, ...]] = []
    reference_internal = edge_variable[(0, 1)]
    for neighbor_cycle in range(1, root_cycles):
        neighbor_internal = edge_variable[
            (3 * neighbor_cycle, 3 * neighbor_cycle + 1)
        ]
        clauses.append((reference_internal, -neighbor_internal))

    next_variable = first_auxiliary
    comparator_count = 0
    self_phase_comparators = 0
    competing_block_phase_comparators = 0
    compared_bits = 0
    groups = (
        tuple(range(1, root_cycles)),
        tuple(range(root_cycles, base.CYCLE_COUNT)),
    )
    for group in groups:
        for position, current in enumerate(group):
            prefix = range(current)
            left = oriented_profile(
                edge_variable, current, prefix, 0
            )
            # Choose the maximum of this block's three possible phases.
            for shift in (1, 2):
                right = oriented_profile(
                    edge_variable, current, prefix, shift
                )
                comparator, next_variable = lexicographic_ge_clauses(
                    left, right, next_variable
                )
                clauses.extend(comparator)
                comparator_count += 1
                self_phase_comparators += 1
                compared_bits += len(left)
            # Choose this oriented block over every remaining oriented block.
            for later in group[position + 1 :]:
                for shift in (0, 1, 2):
                    right = oriented_profile(
                        edge_variable, later, prefix, shift
                    )
                    comparator, next_variable = lexicographic_ge_clauses(
                        left, right, next_variable
                    )
                    clauses.extend(comparator)
                    comparator_count += 1
                    competing_block_phase_comparators += 1
                    compared_bits += len(left)
    metadata = {
        "reference_internal_max_clauses": root_cycles - 1,
        "profile_comparator_count": comparator_count,
        "self_phase_comparator_count": self_phase_comparators,
        "competing_block_phase_comparator_count": (
            competing_block_phase_comparators
        ),
        "lexicographically_compared_bits": compared_bits,
        "greedy_normalizer_clause_count": len(clauses),
        "greedy_normalizer_auxiliary_variable_count": (
            next_variable - first_auxiliary
        ),
    }
    expected = {
        6: {
            "profile_comparator_count": 140,
            "self_phase_comparator_count": 26,
            "competing_block_phase_comparator_count": 114,
            "lexicographically_compared_bits": 2882,
        },
        7: {
            "profile_comparator_count": 134,
            "self_phase_comparator_count": 26,
            "competing_block_phase_comparator_count": 108,
            "lexicographically_compared_bits": 2633,
        },
    }[root_cycles]
    if any(metadata[key] != value for key, value in expected.items()):
        raise AssertionError("unexpected greedy normalizer dimensions")
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
    orbits, reduced_base, root_units, edge_variable = base.build_formula(mode)
    degree_clauses, next_variable, degree_metadata = (
        degree.weighted_degree_clauses(orbits, len(orbits) + 1)
    )
    greedy, final_next_variable, greedy_metadata = (
        greedy_normalizer_clauses(
            edge_variable, args.root_cycles, next_variable
        )
    )
    clauses = (*reduced_base, *root_units, *greedy, *degree_clauses)
    variable_count = final_next_variable - 1
    write_dimacs(args.cnf, variable_count, clauses)
    source = Path(__file__).resolve()
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
        **greedy_metadata,
        "greedy_normalizer": {
            "group_action": "C3^14 semidirect S14, preserving root incidence",
            "reference_selection": (
                "Cycle zero is chosen from the root-neighbor block with "
                "maximal internal-edge bit. Its phase is free because a "
                "simultaneous phase shift is the prescribed automorphism."
            ),
            "inductive_selection": (
                "At every subsequent position, independently rotate every "
                "remaining block through all three phases and choose a "
                "lexicographically maximal profile against all previously "
                "fixed cycles. Exact prefix-equality variables encode every "
                "comparison."
            ),
            "neighbor_nonreference_cycles": list(
                range(1, args.root_cycles)
            ),
            "nonneighbor_cycles": list(
                range(args.root_cycles, base.CYCLE_COUNT)
            ),
        },
        **degree_metadata,
        "total_auxiliary_variable_count": variable_count - len(orbits),
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
