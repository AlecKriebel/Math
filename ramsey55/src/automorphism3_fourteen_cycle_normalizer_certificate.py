#!/usr/bin/env python3
"""Generate strongly symmetry-broken exact CNFs for cycle type 3^14 1."""

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


GENERATOR_ID = "ramsey55_order3_fourteen_cycle_normalizer_cnf_generator_v1"
def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def between_reference_variables(
    edge_variable: dict[tuple[int, int], int], cycle: int
) -> tuple[int, int, int]:
    if not 1 <= cycle < base.CYCLE_COUNT:
        raise ValueError("the reference cycle is zero")
    return tuple(
        edge_variable[(0, 3 * cycle + offset)]
        for offset in range(3)
    )


def cycle_profile_variables(
    edge_variable: dict[tuple[int, int], int],
    cycle: int,
    prefix_cycles: range,
) -> tuple[int, ...]:
    result = [edge_variable[(3 * cycle, 3 * cycle + 1)]]
    for previous in prefix_cycles:
        result.extend(
            edge_variable[
                tuple(
                    sorted(
                        (3 * previous, 3 * cycle + offset)
                    )
                )
            ]
            for offset in range(3)
        )
    return tuple(result)


def lexicographic_ge_clauses(
    left: tuple[int, ...],
    right: tuple[int, ...],
    first_auxiliary: int,
) -> tuple[tuple[tuple[int, ...], ...], int]:
    """Encode ``left >= right`` with exact prefix-equality states."""
    if len(left) != len(right) or not left:
        raise ValueError("lexicographic vectors must have equal positive width")
    clauses: list[tuple[int, ...]] = []
    next_variable = first_auxiliary
    prefix_equal: int | bool = True
    for index, (left_bit, right_bit) in enumerate(zip(left, right)):
        if prefix_equal is True:
            clauses.append((left_bit, -right_bit))
        else:
            clauses.append((-prefix_equal, left_bit, -right_bit))
        if index + 1 == len(left):
            break
        next_equal = next_variable
        next_variable += 1
        if prefix_equal is True:
            clauses.extend(
                (
                    (-next_equal, -left_bit, right_bit),
                    (-next_equal, left_bit, -right_bit),
                    (next_equal, left_bit, right_bit),
                    (next_equal, -left_bit, -right_bit),
                )
            )
        else:
            clauses.extend(
                (
                    (-next_equal, prefix_equal),
                    (-next_equal, -left_bit, right_bit),
                    (-next_equal, left_bit, -right_bit),
                    (-prefix_equal, -left_bit, -right_bit, next_equal),
                    (-prefix_equal, left_bit, right_bit, next_equal),
                )
            )
        prefix_equal = next_equal
    return tuple(clauses), next_variable


def normalizer_clauses(
    edge_variable: dict[tuple[int, int], int],
    root_cycles: int,
    first_auxiliary: int,
) -> tuple[tuple[tuple[int, ...], ...], int, dict[str, int]]:
    """Select a representative under cycle shifts and residual block swaps."""
    if root_cycles not in (6, 7):
        raise ValueError("normalized root case must be 6 or 7")
    clauses: list[tuple[int, ...]] = []
    for cycle in range(1, base.CYCLE_COUNT):
        first, second, third = between_reference_variables(
            edge_variable, cycle
        )
        # Every binary triple has a cyclic rotation x0 >= x1 >= x2.
        clauses.extend(((first, -second), (second, -third)))

    groups = (
        tuple(range(1, root_cycles)),
        tuple(range(root_cycles, base.CYCLE_COUNT)),
    )
    comparator_count = 0
    compared_bits = 0
    next_variable = first_auxiliary
    for group in groups:
        for left_cycle, right_cycle in zip(group, group[1:]):
            comparator_count += 1
            left = cycle_profile_variables(
                edge_variable, left_cycle, range(left_cycle)
            )
            right = cycle_profile_variables(
                edge_variable, right_cycle, range(left_cycle)
            )
            compared_bits += len(left)
            comparator, next_variable = lexicographic_ge_clauses(
                left, right, next_variable
            )
            clauses.extend(comparator)
    expected_bits = 230 if root_cycles == 6 else 227
    expected_clauses = 1_340 if root_cycles == 6 else 1_322
    expected_auxiliary = 219 if root_cycles == 6 else 216
    if (
        comparator_count != 11
        or compared_bits != expected_bits
        or len(clauses) != expected_clauses
        or next_variable - first_auxiliary != expected_auxiliary
    ):
        raise AssertionError("unexpected normalizer clause count")
    return (
        tuple(clauses),
        next_variable,
        {
            "independent_phase_shift_clauses": 26,
            "residual_block_comparators": comparator_count,
            "lexicographically_compared_bits": compared_bits,
            "residual_block_order_clauses": len(clauses) - 26,
            "normalizer_auxiliary_variable_count": (
                next_variable - first_auxiliary
            ),
        },
    )


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
    normalizer, final_next_variable, normalizer_metadata = (
        normalizer_clauses(
            edge_variable, args.root_cycles, next_variable
        )
    )
    clauses = (*reduced_base, *root_units, *normalizer, *degree_clauses)
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
        "normalizer_clause_count": len(normalizer),
        "normalizer": {
            "reference_cycle": 0,
            "reference_cycle_is_root_adjacent": True,
            **normalizer_metadata,
            "neighbor_nonreference_cycles": list(
                range(1, args.root_cycles)
            ),
            "nonneighbor_cycles": list(
                range(args.root_cycles, base.CYCLE_COUNT)
            ),
            "key": (
                "At each greedy block position: internal-edge bit followed "
                "by all three-bit edge patterns to previously fixed cycles."
            ),
            "coverage": (
                "Independent phase shifts centralizing the 3-cycle action "
                "rotate every reference-edge triple to a monotone maximum. "
                "Permutations within each root-incidence block then greedily "
                "choose a lexicographically maximal full profile at every "
                "position; exact prefix-equality states encode the ordering."
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
