#!/usr/bin/env python3
"""Exact CP-SAT constructor for the common-type two-MUB carrier packing.

For one of the 48 complementary length-five quartets, place all four copies
of each of its eight polarized carrier types in one geometric slot.  The
four row signs of a slot are one of the eight projective sign columns.  An
exact modulo-four quotient leaves only eight projective-column bijections
after row-sign symmetry.

For a fixed quartet and projective representative, this model retains the
complete remaining problem:

* an arbitrary permutation of the eight carrier types;
* eight arbitrary carrier orientations; and
* all fourteen hole signs.

Pairwise component tables impose every aperiodic lag exactly.  Any solution
is replayed through the independent base-sequence and order-668 verifier.
"""

from __future__ import annotations

import argparse
from itertools import permutations
import json
from pathlib import Path
from typing import Iterable, Sequence

from ortools.sat.python import cp_model

from check_five_comb_mub_reductions import (
    HOLE_POSITIONS,
    LENGTHS,
    QUARTETS,
    SHIFTS,
    TARGET,
    VECTORS,
    WORDS,
    row_sign_representative,
    slot_syndrome,
)
LAGS = 83
TYPE_COUNT = 8
SLOT_COUNT = 8


def projective_representatives() -> tuple[tuple[int, ...], ...]:
    """Return the eight bijective modulo-four survivors modulo row signs."""

    syndromes = tuple(
        tuple(slot_syndrome(shift, vector, vector) for vector in VECTORS)
        for shift in SHIFTS
    )
    survivors = []
    for labeling in permutations(range(8)):
        syndrome = TARGET
        for slot, label in enumerate(labeling):
            syndrome ^= syndromes[slot][label]
        if syndrome == 0:
            survivors.append(labeling)
    representatives = tuple(
        sorted({row_sign_representative(labeling) for labeling in survivors})
    )
    if len(survivors) != 64 or len(representatives) != 8:
        raise AssertionError("projective-bijection quotient changed")
    return representatives


PROJECTIVE_REPRESENTATIVES = projective_representatives()


def xor_var(
    model: cp_model.CpModel,
    left: cp_model.IntVar,
    right: cp_model.IntVar,
    name: str,
) -> cp_model.IntVar:
    result = model.new_bool_var(name)
    model.add_allowed_assignments(
        [left, right, result],
        ((0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)),
    )
    return result


def carrier_rows(
    quartet: Sequence[int],
    projective_labels: Sequence[int],
    slot: int,
    carrier_type: int,
) -> tuple[dict[int, int], ...]:
    """Return one unoriented four-row carrier component."""

    word = WORDS[quartet[carrier_type // 2]]
    polarization = -1 if carrier_type % 2 == 0 else 1
    vector = VECTORS[projective_labels[slot]]
    shift = SHIFTS[slot]
    rows: list[dict[int, int]] = [dict() for _ in range(4)]
    for tooth, word_sign in enumerate(word):
        for row in range(4):
            rows[row][shift + 4 * tooth] = vector[row] * word_sign
            rows[row][shift + 42 + 4 * tooth] = (
                vector[row] * polarization * word_sign
            )
    return tuple(rows)


def cross_vector(
    left: Sequence[dict[int, int]],
    right: Sequence[dict[int, int]],
) -> tuple[int, ...]:
    result = [0] * (LAGS + 1)
    for left_row, right_row in zip(left, right, strict=True):
        for left_position, left_sign in left_row.items():
            for right_position, right_sign in right_row.items():
                lag = abs(right_position - left_position)
                if lag:
                    result[lag] += left_sign * right_sign
    return tuple(result)


def carrier_hole_vector(
    carrier: Sequence[dict[int, int]], hole: tuple[int, int]
) -> tuple[int, ...]:
    row, position = hole
    result = [0] * (LAGS + 1)
    for carrier_position, sign in carrier[row].items():
        lag = abs(position - carrier_position)
        if lag:
            result[lag] += sign
    return tuple(result)


def add_wide_contribution_table(
    model: cp_model.CpModel,
    selectors: Sequence[cp_model.IntVar],
    rows: Sequence[tuple[int, ...]],
    lags: Sequence[int],
    name: str,
) -> dict[int, cp_model.IntVar]:
    variables: dict[int, cp_model.IntVar] = {}
    selector_count = len(selectors)
    for offset, lag in enumerate(lags):
        values = [row[selector_count + offset] for row in rows]
        variables[lag] = model.new_int_var(
            min(values), max(values), f"{name}_lag_{lag}"
        )
    model.add_allowed_assignments(
        [*selectors, *(variables[lag] for lag in lags)],
        rows,
    )
    return variables


def row_sum_profiles() -> tuple[tuple[int, int, int, int], ...]:
    result = []
    for first in range(-84, 85, 2):
        for second in range(-84, 85, 2):
            for third in range(-83, 84, 2):
                remainder = 334 - first * first - second * second - third * third
                if remainder < 0:
                    continue
                fourth = int(remainder**0.5)
                if fourth * fourth != remainder or fourth % 2 == 0:
                    continue
                for signed_fourth in {fourth, -fourth}:
                    if -83 <= signed_fourth <= 83:
                        result.append((first, second, third, signed_fourth))
    return tuple(result)


ROW_SUM_PROFILES = row_sum_profiles()


def build_model(
    quartet_index: int,
    projective_index: int,
) -> tuple[
    cp_model.CpModel,
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
]:
    if not 0 <= quartet_index < len(QUARTETS):
        raise ValueError("quartet index must lie in 0..47")
    if not 0 <= projective_index < len(PROJECTIVE_REPRESENTATIVES):
        raise ValueError("projective index must lie in 0..7")
    quartet = QUARTETS[quartet_index]
    projective = PROJECTIVE_REPRESENTATIVES[projective_index]
    carriers = tuple(
        tuple(
            carrier_rows(quartet, projective, slot, carrier_type)
            for carrier_type in range(TYPE_COUNT)
        )
        for slot in range(SLOT_COUNT)
    )

    model = cp_model.CpModel()
    types = tuple(
        model.new_int_var(0, TYPE_COUNT - 1, f"type_{slot}")
        for slot in range(SLOT_COUNT)
    )
    model.add_all_different(types)
    orientations = tuple(
        model.new_bool_var(f"orientation_{slot}") for slot in range(SLOT_COUNT)
    )
    holes = tuple(
        model.new_bool_var(f"hole_{index}") for index in range(len(HOLE_POSITIONS))
    )
    # Negating all four sequences flips every component and preserves every
    # correlation, so one carrier orientation may be fixed.
    model.add(orientations[0] == 0)

    lag_terms: list[list[cp_model.LinearExpr]] = [
        [] for _ in range(LAGS + 1)
    ]

    # There is no within-carrier table.  A carrier's self-correlation is
    # independent of its orientation, shift, and projective row signs.
    # AllDifferent uses every word with both polarizations exactly once:
    # summing the two polarizations cancels the lobe-cross terms, and summing
    # the four remaining word terms vanishes by quartet complementarity.
    # test_five_comb_common_type_cp_sat.py checks this identity for all 48
    # quartets and checks the complete decomposition against direct replay.
    for left in range(SLOT_COUNT):
        for right in range(left + 1, SLOT_COUNT):
            orientation_xor = xor_var(
                model,
                orientations[left],
                orientations[right],
                f"carrier_xor_{left}_{right}",
            )
            vectors = {
                (left_type, right_type): cross_vector(
                    carriers[left][left_type], carriers[right][right_type]
                )
                for left_type in range(TYPE_COUNT)
                for right_type in range(TYPE_COUNT)
            }
            active_lags = tuple(
                lag
                for lag in range(1, LAGS + 1)
                if any(vector[lag] for vector in vectors.values())
            )
            table_rows = []
            for left_type in range(TYPE_COUNT):
                for right_type in range(TYPE_COUNT):
                    vector = vectors[(left_type, right_type)]
                    for xor in (0, 1):
                        multiplier = -1 if xor else 1
                        table_rows.append(
                            (
                                left_type,
                                right_type,
                                xor,
                                *(multiplier * vector[lag] for lag in active_lags),
                            )
                        )
            contributions = add_wide_contribution_table(
                model,
                (types[left], types[right], orientation_xor),
                table_rows,
                active_lags,
                f"carrier_pair_{left}_{right}",
            )
            for lag, contribution in contributions.items():
                lag_terms[lag].append(contribution)

    for slot in range(SLOT_COUNT):
        for hole_index, hole_position in enumerate(HOLE_POSITIONS):
            sign_xor = xor_var(
                model,
                orientations[slot],
                holes[hole_index],
                f"carrier_hole_xor_{slot}_{hole_index}",
            )
            vectors = tuple(
                carrier_hole_vector(carriers[slot][carrier_type], hole_position)
                for carrier_type in range(TYPE_COUNT)
            )
            active_lags = tuple(
                lag
                for lag in range(1, LAGS + 1)
                if any(vector[lag] for vector in vectors)
            )
            if not active_lags:
                continue
            table_rows = []
            for carrier_type, vector in enumerate(vectors):
                for xor in (0, 1):
                    multiplier = -1 if xor else 1
                    table_rows.append(
                        (
                            carrier_type,
                            xor,
                            *(multiplier * vector[lag] for lag in active_lags),
                        )
                    )
            contributions = add_wide_contribution_table(
                model,
                (types[slot], sign_xor),
                table_rows,
                active_lags,
                f"carrier_hole_{slot}_{hole_index}",
            )
            for lag, contribution in contributions.items():
                lag_terms[lag].append(contribution)

    for left, (left_row, left_position) in enumerate(HOLE_POSITIONS):
        for right in range(left + 1, len(HOLE_POSITIONS)):
            right_row, right_position = HOLE_POSITIONS[right]
            if left_row != right_row:
                continue
            lag = abs(right_position - left_position)
            sign_xor = xor_var(
                model, holes[left], holes[right], f"hole_xor_{left}_{right}"
            )
            lag_terms[lag].append(1 - 2 * sign_xor)

    for lag in range(1, LAGS + 1):
        model.add(sum(lag_terms[lag]) == 0)

    row_sums = tuple(
        model.new_int_var(-LENGTHS[row], LENGTHS[row], f"row_sum_{row}")
        for row in range(4)
    )
    for row in range(4):
        terms: list[cp_model.LinearExpr] = []
        for slot in range(SLOT_COUNT):
            values = []
            for carrier_type in range(TYPE_COUNT):
                base_sum = sum(carriers[slot][carrier_type][row].values())
                for orientation in (0, 1):
                    values.append(
                        (
                            carrier_type,
                            orientation,
                            (-1 if orientation else 1) * base_sum,
                        )
                    )
            contribution = model.new_int_var(-30, 30, f"rowsum_{row}_{slot}")
            model.add_allowed_assignments(
                [types[slot], orientations[slot], contribution], values
            )
            terms.append(contribution)
        for hole_index, (hole_row, _position) in enumerate(HOLE_POSITIONS):
            if hole_row == row:
                terms.append(1 - 2 * holes[hole_index])
        model.add(row_sums[row] == sum(terms))
    model.add_allowed_assignments(row_sums, ROW_SUM_PROFILES)

    return model, types, orientations, holes


def reconstruct(
    quartet_index: int,
    projective_index: int,
    types: Sequence[int],
    orientations: Sequence[int],
    holes: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    quartet = QUARTETS[quartet_index]
    projective = PROJECTIVE_REPRESENTATIVES[projective_index]
    sequences = [[0] * length for length in LENGTHS]
    for slot, carrier_type in enumerate(types):
        rows = carrier_rows(quartet, projective, slot, carrier_type)
        multiplier = -1 if orientations[slot] else 1
        for row, coefficients in enumerate(rows):
            for position, value in coefficients.items():
                if sequences[row][position]:
                    raise AssertionError("carrier supports overlap")
                sequences[row][position] = multiplier * value
    for hole_bit, (row, position) in zip(holes, HOLE_POSITIONS, strict=True):
        if sequences[row][position]:
            raise AssertionError("a hole overlaps a carrier")
        sequences[row][position] = -1 if hole_bit else 1
    result = tuple(tuple(sequence) for sequence in sequences)
    if any(value not in (-1, 1) for sequence in result for value in sequence):
        raise AssertionError("the packing left an unfilled coefficient")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quartet", type=int, required=True)
    parser.add_argument("--projective", type=int, required=True)
    parser.add_argument("--time-limit", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--max-memory-mb", type=int, default=4096)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    model, type_vars, orientation_vars, hole_vars = build_model(
        args.quartet, args.projective
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    status = solver.solve(model)
    status_name = solver.status_name(status)
    print(f"status={status_name}")
    print(f"quartet={args.quartet}")
    print(f"projective={args.projective}")
    print(f"wall_time={solver.wall_time:.6f}")
    print(f"conflicts={solver.num_conflicts}")
    print(f"branches={solver.num_branches}")
    print(f"booleans={solver.num_booleans}")
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return 2 if status == cp_model.UNKNOWN else 1

    types = tuple(solver.value(variable) for variable in type_vars)
    orientations = tuple(solver.value(variable) for variable in orientation_vars)
    holes = tuple(solver.value(variable) for variable in hole_vars)
    sequences = reconstruct(
        args.quartet, args.projective, types, orientations, holes
    )
    # These verification modules are deliberately imported only after a
    # solution exists.  In particular, variable_q_base constructs its margin
    # catalog at import time; an UNSAT shard does not need that unrelated
    # catalog.
    from construction import goethals_seidel, verify_hadamard
    from seed import special_quadruple
    from variable_q_base import base_correlations, base_to_special

    correlations = base_correlations(*sequences)
    if correlations != (334,) + (0,) * 83:
        raise AssertionError("CP-SAT emitted a non-base-sequence packing")
    s, q = base_to_special(*sequences)
    verify_hadamard(goethals_seidel(special_quadruple(s, q)))
    payload = {
        "format": "h668-five-comb-common-type-v1",
        "quartet_index": args.quartet,
        "projective_index": args.projective,
        "types": list(types),
        "orientations": list(orientations),
        "holes": list(holes),
        "a": list(sequences[0]),
        "b": list(sequences[1]),
        "c": list(sequences[2]),
        "d": list(sequences[3]),
        "s": list(s),
        "q": list(q),
    }
    destination = args.output or Path(
        f"output/five_comb_common_q{args.quartet}_p{args.projective}.json"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"candidate={destination}")
    print("verified_hadamard_order=668")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
