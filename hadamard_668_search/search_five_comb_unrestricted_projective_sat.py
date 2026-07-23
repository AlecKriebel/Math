#!/usr/bin/env python3
"""Pure-Boolean exact model for unrestricted projective five-comb packing.

This is a second, independent encoding of the family modeled by
``search_five_comb_unrestricted_projective_cp_sat.py``.  It uses the same
rank-nine projective quotient and twelve normalized label parameters, but
then expands the 334 sequence coefficients to Boolean signs.

The complementary quartet and its two polarizations make the sum of all
within-carrier autocorrelations identically zero.  Those 1,440 products can
therefore be omitted.  The remaining 12,338 coefficient-pair XORs are
grouped into 83 exact cardinality equations.  This removes every nonlinear
integer product from the component-table model and provides an independent
mechanical cross-check of any feasibility result.
"""

from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path
from typing import Sequence

from ortools.sat.python import cp_model

from check_five_comb_mub_reductions import (
    HOLE_POSITIONS,
    LENGTHS,
    PROJECTIVE_RREF,
    QUARTETS,
    VECTORS,
)
from search_five_comb_common_type_cp_sat import ROW_SUM_PROFILES, xor_var
from search_five_comb_unrestricted_projective_cp_sat import (
    SLOT_COUNT,
    TYPE_COUNT,
    add_bool_lex_less_or_equal,
    add_physical_high_lag_boundary_table,
    scalar_carrier,
)


LAGS = 83
EXPECTED_RETAINED_PRODUCTS = 12_338


def add_parity_equation(
    model: cp_model.CpModel,
    variables: Sequence[cp_model.IntVar],
    right_hand_side: int,
) -> None:
    rows = tuple(
        values
        for values in product((0, 1), repeat=len(variables))
        if sum(values) % 2 == right_hand_side
    )
    model.add_allowed_assignments(variables, rows)


def build_model(
    quartet_index: int,
) -> tuple[
    cp_model.CpModel,
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
]:
    if not 0 <= quartet_index < len(QUARTETS):
        raise ValueError("quartet index must lie in 0..47")
    quartet = QUARTETS[quartet_index]
    carriers = tuple(
        tuple(
            scalar_carrier(quartet, slot, carrier_type)
            for carrier_type in range(TYPE_COUNT)
        )
        for slot in range(SLOT_COUNT)
    )

    model = cp_model.CpModel()
    label_bits = tuple(
        tuple(
            model.new_bool_var(f"label_{slot}_bit_{bit}")
            for bit in range(3)
        )
        for slot in range(SLOT_COUNT)
    )
    labels = tuple(
        model.new_int_var(0, 7, f"label_{slot}")
        for slot in range(SLOT_COUNT)
    )
    for slot in range(SLOT_COUNT):
        model.add(
            labels[slot]
            == label_bits[slot][0]
            + 2 * label_bits[slot][1]
            + 4 * label_bits[slot][2]
        )
    for bit in range(3):
        model.add(label_bits[0][bit] == 0)
    flat_label_bits = tuple(bit for slot in label_bits for bit in slot)
    for indices, right_hand_side in PROJECTIVE_RREF:
        add_parity_equation(
            model,
            tuple(flat_label_bits[index] for index in indices),
            right_hand_side,
        )
    middle = tuple(label_bits[slot][1] for slot in range(1, SLOT_COUNT))
    low = tuple(label_bits[slot][0] for slot in range(1, SLOT_COUNT))
    high = tuple(label_bits[slot][2] for slot in range(1, SLOT_COUNT))
    low_xor_high = tuple(
        xor_var(model, low[index], high[index], f"row_mask_{index}")
        for index in range(SLOT_COUNT - 1)
    )
    for name, mask in (
        ("swap_long", low),
        ("swap_both", high),
        ("swap_short", low_xor_high),
    ):
        transformed = tuple(
            xor_var(
                model,
                middle[index],
                mask[index],
                f"{name}_middle_{index}",
            )
            for index in range(SLOT_COUNT - 1)
        )
        add_bool_lex_less_or_equal(model, middle, transformed, name)
    model.add_bool_or(
        (
            label_bits[2][0],
            label_bits[7][2],
            label_bits[1][1],
            label_bits[7][1],
        )
    )

    types = tuple(
        model.new_int_var(0, TYPE_COUNT - 1, f"type_{slot}")
        for slot in range(SLOT_COUNT)
    )
    model.add_all_different(types)
    orientations = tuple(
        model.new_bool_var(f"orientation_{slot}")
        for slot in range(SLOT_COUNT)
    )
    model.add(orientations[0] == 0)
    model.add(orientations[1] == 0)

    coefficient_bits: list[list[cp_model.IntVar | None]] = [
        [None] * length for length in LENGTHS
    ]
    coefficient_slots = [[-1] * length for length in LENGTHS]

    # One compact table expands each slot state to its forty coefficient
    # bits: ten occupied positions in each of four rows.
    for slot in range(SLOT_COUNT):
        positions = tuple(sorted(carriers[slot][0]))
        output_variables = []
        for row in range(4):
            for position in positions:
                if coefficient_bits[row][position] is not None:
                    raise AssertionError("carrier supports overlap")
                variable = model.new_bool_var(
                    f"coefficient_{row}_{position}"
                )
                coefficient_bits[row][position] = variable
                coefficient_slots[row][position] = slot
                output_variables.append(variable)

        table_rows = []
        for label in range(8):
            for carrier_type in range(TYPE_COUNT):
                carrier = carriers[slot][carrier_type]
                for orientation in (0, 1):
                    orientation_sign = -1 if orientation else 1
                    bits = tuple(
                        int(
                            orientation_sign
                            * VECTORS[label][row]
                            * carrier[position]
                            < 0
                        )
                        for row in range(4)
                        for position in positions
                    )
                    table_rows.append(
                        (label, carrier_type, orientation, *bits)
                    )
        model.add_allowed_assignments(
            [
                labels[slot],
                types[slot],
                orientations[slot],
                *output_variables,
            ],
            table_rows,
        )

    holes = tuple(
        model.new_bool_var(f"hole_{index}")
        for index in range(len(HOLE_POSITIONS))
    )
    for hole, (row, position) in zip(holes, HOLE_POSITIONS, strict=True):
        if coefficient_bits[row][position] is not None:
            raise AssertionError("a hole overlaps a carrier")
        coefficient_bits[row][position] = hole

    model.add(holes[0] == holes[4])
    model.add(holes[1] == holes[5])
    model.add(holes[2] == holes[6])
    model.add(holes[3] + holes[7] == 1)
    model.add(holes[8] == holes[11])
    model.add(holes[10] == holes[13])
    model.add(holes[2] + holes[10] == 1)
    model.add_bool_xor(holes[:8])
    add_parity_equation(
        model,
        (holes[8], holes[10], holes[11], holes[13]),
        0,
    )
    add_physical_high_lag_boundary_table(
        model,
        label_bits,
        types,
        orientations,
        holes,
        quartet,
    )

    if any(
        variable is None
        for row in coefficient_bits
        for variable in row
    ):
        raise AssertionError("the packing left an unfilled coefficient")
    coefficients = tuple(
        tuple(variable for variable in row if variable is not None)
        for row in coefficient_bits
    )

    retained_products = 0
    for lag in range(1, LAGS + 1):
        products = []
        for row, row_coefficients in enumerate(coefficients):
            for position in range(len(row_coefficients) - lag):
                left_slot = coefficient_slots[row][position]
                right_slot = coefficient_slots[row][position + lag]
                if left_slot >= 0 and left_slot == right_slot:
                    continue
                products.append(
                    xor_var(
                        model,
                        row_coefficients[position],
                        row_coefficients[position + lag],
                        f"product_{row}_{position}_{position + lag}",
                    )
                )
        if len(products) % 2:
            raise AssertionError(
                f"lag {lag} retained an odd number of products"
            )
        model.add(sum(products) == len(products) // 2)
        retained_products += len(products)
    if retained_products != EXPECTED_RETAINED_PRODUCTS:
        raise AssertionError("the retained-product count changed")

    row_sums = tuple(
        model.new_int_var(-LENGTHS[row], LENGTHS[row], f"row_sum_{row}")
        for row in range(4)
    )
    for row, row_coefficients in enumerate(coefficients):
        model.add(
            row_sums[row]
            == LENGTHS[row] - 2 * sum(row_coefficients)
        )
    model.add_allowed_assignments(row_sums, ROW_SUM_PROFILES)

    return model, labels, types, orientations, holes


def reconstruct(
    quartet_index: int,
    labels: Sequence[int],
    types: Sequence[int],
    orientations: Sequence[int],
    holes: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    quartet = QUARTETS[quartet_index]
    sequences = [[0] * length for length in LENGTHS]
    for slot, carrier_type in enumerate(types):
        carrier = scalar_carrier(quartet, slot, carrier_type)
        orientation_sign = -1 if orientations[slot] else 1
        for row in range(4):
            multiplier = orientation_sign * VECTORS[labels[slot]][row]
            for position, value in carrier.items():
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
    parser.add_argument("--time-limit", type=float, default=1800.0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-memory-mb", type=int, default=8192)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    model, label_vars, type_vars, orientation_vars, hole_vars = build_model(
        args.quartet
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    status = solver.solve(model)
    status_name = solver.status_name(status)
    print(f"status={status_name}")
    print(f"quartet={args.quartet}")
    print(f"wall_time={solver.wall_time:.6f}")
    print(f"conflicts={solver.num_conflicts}")
    print(f"branches={solver.num_branches}")
    print(f"booleans={solver.num_booleans}")
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return 2 if status == cp_model.UNKNOWN else 1

    labels = tuple(solver.value(variable) for variable in label_vars)
    types = tuple(solver.value(variable) for variable in type_vars)
    orientations = tuple(solver.value(variable) for variable in orientation_vars)
    holes = tuple(solver.value(variable) for variable in hole_vars)
    sequences = reconstruct(
        args.quartet, labels, types, orientations, holes
    )

    from construction import goethals_seidel, verify_hadamard
    from seed import special_quadruple
    from variable_q_base import base_correlations, base_to_special

    correlations = base_correlations(*sequences)
    if correlations != (334,) + (0,) * 83:
        raise AssertionError("CP-SAT emitted a non-base-sequence packing")
    s, q = base_to_special(*sequences)
    verify_hadamard(goethals_seidel(special_quadruple(s, q)))
    payload = {
        "format": "h668-five-comb-unrestricted-projective-v1",
        "encoding": "pure-boolean",
        "quartet_index": args.quartet,
        "labels": list(labels),
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
        f"output/five_comb_unrestricted_sat_q{args.quartet}.json"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"candidate={destination}")
    print("verified_hadamard_order=668")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
