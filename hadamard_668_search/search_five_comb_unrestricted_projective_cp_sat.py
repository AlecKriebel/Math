#!/usr/bin/env python3
"""Exact constructor for the unrestricted projective common-type packing.

For one complementary length-five quartet, the eight polarized carrier
types are assigned bijectively to the eight geometric slots.  Unlike
``search_five_comb_common_type_cp_sat.py``, the projective row-sign label
of a slot need not be distinct.  The exact modulo-four quotient is a
rank-nine linear system on the 24 label bits.  Row-sign normalization
leaves only twelve free bits and exactly 4,096 projective labelings.

The model retains all of those labelings simultaneously, together with:

* an arbitrary permutation of the eight polarized carrier types;
* eight arbitrary carrier orientations; and
* all fourteen hole signs.

Every aperiodic correlation and the row-square identity are imposed
exactly.  Any feasible point is replayed through the independent
base-sequence and order-668 Hadamard verifiers before it is written.
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
    SHIFTS,
    VECTORS,
    WORDS,
)
from search_five_comb_common_type_cp_sat import (
    ROW_SUM_PROFILES,
    add_wide_contribution_table,
    xor_var,
)
from verify_five_comb_high_lag_boundary import e2_boundary_rows


LAGS = 83
TYPE_COUNT = 8
SLOT_COUNT = 8


def scalar_carrier(
    quartet: Sequence[int],
    slot: int,
    carrier_type: int,
) -> dict[int, int]:
    """Return a carrier before its projective row signs are applied."""

    word = WORDS[quartet[carrier_type // 2]]
    polarization = -1 if carrier_type % 2 == 0 else 1
    shift = SHIFTS[slot]
    coefficients: dict[int, int] = {}
    for tooth, word_sign in enumerate(word):
        coefficients[shift + 4 * tooth] = word_sign
        coefficients[shift + 42 + 4 * tooth] = polarization * word_sign
    return coefficients


def scalar_cross_vector(
    left: dict[int, int],
    right: dict[int, int],
) -> tuple[int, ...]:
    """Return the scalar cross-correlation contribution at every lag."""

    result = [0] * (LAGS + 1)
    for left_position, left_sign in left.items():
        for right_position, right_sign in right.items():
            lag = abs(right_position - left_position)
            if lag:
                result[lag] += left_sign * right_sign
    return tuple(result)


def scalar_hole_vector(
    carrier: dict[int, int],
    hole_position: int,
) -> tuple[int, ...]:
    """Return one row's carrier/hole cross contribution before signs."""

    result = [0] * (LAGS + 1)
    for carrier_position, carrier_sign in carrier.items():
        lag = abs(hole_position - carrier_position)
        if lag:
            result[lag] += carrier_sign
    return tuple(result)


def projective_inner_product(left: int, right: int) -> int:
    return sum(
        VECTORS[left][row] * VECTORS[right][row] for row in range(4)
    )


PROJECTIVE_INNER_PRODUCT_ROWS = tuple(
    (
        left,
        right,
        projective_inner_product(left, right),
    )
    for left in range(8)
    for right in range(8)
)
PROJECTIVE_INNER_PRODUCTS = tuple(
    sorted({row[2] for row in PROJECTIVE_INNER_PRODUCT_ROWS})
)


def normalized_projective_labels(
    parameters: Sequence[int],
) -> tuple[int, ...]:
    """Evaluate the sparse twelve-bit parametrization of all 4,096 maps.

    The parameters are ``alpha,beta,u5,u6,u7,y1,...,y7``.  The ``y`` bits
    are the completely free middle coordinate of labels 1 through 7.
    """

    if len(parameters) != 12 or any(bit not in (0, 1) for bit in parameters):
        raise ValueError("the projective parametrization needs twelve bits")
    alpha, beta, u5, u6, u7, *middle_tail = parameters
    low = (0, 0, beta, alpha, 0, 0, alpha, beta)
    middle = (0, *middle_tail)
    high = (
        0,
        beta ^ u7,
        alpha ^ beta ^ u6,
        alpha ^ u5,
        0,
        u5,
        u6,
        u7,
    )
    labels = tuple(
        low[slot] + 2 * middle[slot] + 4 * high[slot]
        for slot in range(SLOT_COUNT)
    )
    flat_bits = tuple(
        (labels[slot] >> bit) & 1
        for slot in range(SLOT_COUNT)
        for bit in range(3)
    )
    if any(
        sum(flat_bits[index] for index in indices) % 2 != right_hand_side
        for indices, right_hand_side in PROJECTIVE_RREF
    ):
        raise AssertionError("the sparse projective parametrization is wrong")
    return labels


def add_parity_equation(
    model: cp_model.CpModel,
    variables: Sequence[cp_model.IntVar],
    right_hand_side: int,
) -> None:
    """Add one small XOR equation as an explicit truth table."""

    rows = tuple(
        values
        for values in product((0, 1), repeat=len(variables))
        if sum(values) % 2 == right_hand_side
    )
    model.add_allowed_assignments(variables, rows)


def add_bool_lex_less_or_equal(
    model: cp_model.CpModel,
    left: Sequence[cp_model.IntVar],
    right: Sequence[cp_model.IntVar],
    name: str,
) -> None:
    """Add a lexicographic order on two equally sized Boolean vectors."""

    if len(left) != len(right):
        raise ValueError("lexicographic vectors must have equal length")
    prefix_equal = model.new_bool_var(f"{name}_prefix_0")
    model.add(prefix_equal == 1)
    for index, (left_bit, right_bit) in enumerate(
        zip(left, right, strict=True)
    ):
        next_prefix_equal = model.new_bool_var(
            f"{name}_prefix_{index + 1}"
        )
        model.add_allowed_assignments(
            [
                prefix_equal,
                left_bit,
                right_bit,
                next_prefix_equal,
            ],
            (
                (0, 0, 0, 0),
                (0, 0, 1, 0),
                (0, 1, 0, 0),
                (0, 1, 1, 0),
                (1, 0, 0, 1),
                (1, 0, 1, 0),
                (1, 1, 1, 1),
            ),
        )
        prefix_equal = next_prefix_equal


def projective_parameter_variables(
    label_bits: Sequence[Sequence[cp_model.IntVar]],
) -> tuple[cp_model.IntVar, ...]:
    """Return ``alpha,beta,u5,u6,u7,y1,...,y7`` from the sparse RREF."""

    if len(label_bits) != SLOT_COUNT or any(
        len(bits) != 3 for bits in label_bits
    ):
        raise ValueError("expected eight three-bit projective labels")
    return (
        label_bits[3][0],
        label_bits[2][0],
        label_bits[5][2],
        label_bits[6][2],
        label_bits[7][2],
        *(label_bits[slot][1] for slot in range(1, SLOT_COUNT)),
    )


def add_physical_high_lag_boundary_table(
    model: cp_model.CpModel,
    label_bits: Sequence[Sequence[cp_model.IntVar]],
    types: Sequence[cp_model.IntVar],
    orientations: Sequence[cp_model.IntVar],
    holes: Sequence[cp_model.IntVar],
    quartet: Sequence[int],
) -> None:
    """Channel the exact physical-hole equations at lags 78 through 81.

    Lags 82 and 83 make the four signs at position 82 equal, up to a
    scalar, to projective direction ``V_2`` and make the two signs at
    position 83 opposite.  Those two outer scalars gauge out of the next
    four equations.  The resulting finite table has 10,934 rows on the
    twelve projective parameters and seven adjusted carrier signs.
    """

    if len(types) != SLOT_COUNT or len(orientations) != SLOT_COUNT:
        raise ValueError("expected eight types and orientations")
    if len(holes) != len(HOLE_POSITIONS):
        raise ValueError("expected the complete fourteen-hole fiber")
    if len(quartet) != 4:
        raise ValueError("expected one complementary word quartet")

    parameters = projective_parameter_variables(label_bits)
    gauge_bits = tuple(
        model.new_bool_var(f"high_lag_gauge_{index}")
        for index in range(7)
    )

    # eta is the sign at row 0, position 82; f is the sign at row 0,
    # position 83.  Boolean values encode negativity, so products of signs
    # become XORs.
    eta_bit = holes[2]
    tail_bit = holes[3]
    add_parity_equation(
        model,
        (orientations[1], eta_bit, tail_bit, gauge_bits[0]),
        0,
    )
    model.add(gauge_bits[1] == orientations[2])
    add_parity_equation(
        model,
        (orientations[3], eta_bit, tail_bit, gauge_bits[2]),
        0,
    )

    for offset, slot in enumerate(range(4, SLOT_COUNT)):
        outer_bit = eta_bit if slot % 2 == 0 else tail_bit
        rows = []
        for carrier_type in range(TYPE_COUNT):
            word = WORDS[quartet[carrier_type // 2]]
            polarization = -1 if carrier_type % 2 == 0 else 1
            rho_bit = int(polarization * word[4] < 0)
            for orientation in (0, 1):
                for outer in (0, 1):
                    rows.append(
                        (
                            carrier_type,
                            orientation,
                            outer,
                            orientation ^ rho_bit ^ outer,
                        )
                    )
        model.add_allowed_assignments(
            (
                types[slot],
                orientations[slot],
                outer_bit,
                gauge_bits[3 + offset],
            ),
            rows,
        )

    model.add_allowed_assignments(
        (*parameters, *gauge_bits),
        e2_boundary_rows(),
    )


def projective_row_orbit_is_canonical(labels: Sequence[int]) -> bool:
    """Test the A/B and C/D row-swap lex leader on a normalized labeling."""

    if len(labels) != SLOT_COUNT or labels[0] != 0:
        raise ValueError("expected eight normalized projective labels")
    middle = tuple((label >> 1) & 1 for label in labels[1:])
    low = tuple(label & 1 for label in labels[1:])
    high = tuple((label >> 2) & 1 for label in labels[1:])
    masks = (
        low,
        high,
        tuple(a ^ b for a, b in zip(low, high, strict=True)),
    )
    return all(
        middle
        <= tuple(
            value ^ mask_bit
            for value, mask_bit in zip(middle, mask, strict=True)
        )
        for mask in masks
    )


def build_model(
    quartet_index: int,
    projective_core: int | None = None,
) -> tuple[
    cp_model.CpModel,
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
]:
    if not 0 <= quartet_index < len(QUARTETS):
        raise ValueError("quartet index must lie in 0..47")
    if projective_core is not None and not 0 <= projective_core < 32:
        raise ValueError("projective core must lie in 0..31")
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

    # Multiplying every row by one projective character translates all
    # labels by the same element of F_2^3 and preserves every equation.
    for bit in range(3):
        model.add(label_bits[0][bit] == 0)
    flat_label_bits = tuple(bit for slot in label_bits for bit in slot)
    for indices, right_hand_side in PROJECTIVE_RREF:
        add_parity_equation(
            model,
            tuple(flat_label_bits[index] for index in indices),
            right_hand_side,
        )
    if projective_core is not None:
        core_variables = (
            label_bits[3][0],  # alpha
            label_bits[2][0],  # beta
            label_bits[5][2],  # u5
            label_bits[6][2],  # u6
            label_bits[7][2],  # u7
        )
        for bit, variable in enumerate(core_variables):
            model.add(variable == ((projective_core >> bit) & 1))

    # Swapping the two long rows and/or the two short rows preserves the
    # construction.  In the sparse RREF coordinates these swaps leave the
    # low/high label bits fixed and translate the seven free middle bits by
    # low, high, or low XOR high.  A lex leader reduces the 4,096 normalized
    # labelings to exactly 1,440 row-pair orbits.
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
    # Lag 81 alone excludes the all-zero corner of these four parameters.
    model.add_bool_or(
        (
            label_bits[2][0],  # beta
            label_bits[7][2],  # u7
            label_bits[1][1],  # y1
            label_bits[7][1],  # y7
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
    holes = tuple(
        model.new_bool_var(f"hole_{index}")
        for index in range(len(HOLE_POSITIONS))
    )
    # Negating all four completed sequences is a second free symmetry.
    model.add(orientations[0] == 0)
    # Simultaneous alternating modulation X_j -> (-1)^j X_j toggles every
    # odd-shift carrier, in particular slot 1, while preserving the family.
    model.add(orientations[1] == 0)

    # The complete physical modulo-four fiber becomes label-independent
    # after the rank-nine projective equations and row-sign normalization.
    # These six relations characterize all 2^8=256 hole completions.
    model.add(holes[0] == holes[4])
    model.add(holes[1] == holes[5])
    model.add(holes[2] == holes[6])
    model.add(holes[3] + holes[7] == 1)
    model.add(holes[8] == holes[11])
    model.add(holes[10] == holes[13])
    # Lag 82 reduces to one further two-bit cardinality.
    model.add(holes[2] + holes[10] == 1)
    # The following mod-eight consequences are redundant after the exact
    # fiber equalities, but retain useful direct propagation.
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

    # Channel only the boundary coefficients needed at lags 64,...,83.
    # These 800 Boolean products give the solver a strong direct view of
    # the high-lag equations while the compact component factorization
    # handles the dense lower lags.
    needed_positions = tuple(
        frozenset(
            position
            for lag in range(64, LAGS + 1)
            for left in range(LENGTHS[row] - lag)
            for position in (left, left + lag)
        )
        for row in range(4)
    )
    boundary_bits: dict[tuple[int, int], cp_model.IntVar] = {}
    for slot in range(SLOT_COUNT):
        positions = tuple(
            position
            for position in sorted(carriers[slot][0])
            if any(position in needed for needed in needed_positions)
        )
        if not positions:
            continue
        output_variables = []
        output_locations = []
        for row in range(4):
            for position in positions:
                if position not in needed_positions[row]:
                    continue
                variable = model.new_bool_var(
                    f"boundary_{row}_{position}"
                )
                boundary_bits[(row, position)] = variable
                output_variables.append(variable)
                output_locations.append((row, position))
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
                        for row, position in output_locations
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
    for hole, (row, position) in zip(holes, HOLE_POSITIONS, strict=True):
        if position in needed_positions[row]:
            boundary_bits[(row, position)] = hole
    if any(
        (row, position) not in boundary_bits
        for row, needed in enumerate(needed_positions)
        for position in needed
    ):
        raise AssertionError("a required boundary coefficient is missing")
    direct_high_lag_products = 0
    for lag in range(64, LAGS + 1):
        products = []
        for row in range(4):
            for position in range(LENGTHS[row] - lag):
                products.append(
                    xor_var(
                        model,
                        boundary_bits[(row, position)],
                        boundary_bits[(row, position + lag)],
                        f"boundary_product_{row}_{position}_{position + lag}",
                    )
                )
        if len(products) % 2:
            raise AssertionError("a high lag retained an odd pair count")
        model.add(sum(products) == len(products) // 2)
        direct_high_lag_products += len(products)
    if direct_high_lag_products != 800:
        raise AssertionError("the direct high-lag product count changed")

    lag_terms: list[list[cp_model.LinearExpr]] = [
        [] for _ in range(LAGS + 1)
    ]

    # The carrier/carrier term factors exactly into a projective inner
    # product and a scalar word/polarization cross-correlation.  This
    # replaces a 8,192-row joint table at every slot pair by one 64-row
    # inner-product table and one 128-row scalar table.
    for left in range(SLOT_COUNT):
        for right in range(left + 1, SLOT_COUNT):
            orientation_xor = xor_var(
                model,
                orientations[left],
                orientations[right],
                f"carrier_xor_{left}_{right}",
            )
            inner_product = model.new_int_var(
                min(PROJECTIVE_INNER_PRODUCTS),
                max(PROJECTIVE_INNER_PRODUCTS),
                f"inner_product_{left}_{right}",
            )
            model.add_allowed_assignments(
                [labels[left], labels[right], inner_product],
                PROJECTIVE_INNER_PRODUCT_ROWS,
            )

            vectors = {
                (left_type, right_type): scalar_cross_vector(
                    carriers[left][left_type],
                    carriers[right][right_type],
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
                    for orientation_parity in (0, 1):
                        multiplier = -1 if orientation_parity else 1
                        table_rows.append(
                            (
                                left_type,
                                right_type,
                                orientation_parity,
                                *(
                                    multiplier * vector[lag]
                                    for lag in active_lags
                                ),
                            )
                        )
            scalar_contributions = add_wide_contribution_table(
                model,
                (types[left], types[right], orientation_xor),
                table_rows,
                active_lags,
                f"scalar_pair_{left}_{right}",
            )
            for lag, scalar_contribution in scalar_contributions.items():
                possible = tuple(
                    inner * row[3 + active_lags.index(lag)]
                    for inner in PROJECTIVE_INNER_PRODUCTS
                    for row in table_rows
                )
                contribution = model.new_int_var(
                    min(possible),
                    max(possible),
                    f"carrier_pair_{left}_{right}_lag_{lag}",
                )
                model.add_multiplication_equality(
                    contribution,
                    [inner_product, scalar_contribution],
                )
                lag_terms[lag].append(contribution)

    # A carrier/hole term depends on only one projective row sign.  Its
    # complete 8*8*2 table remains compact and avoids another multiplication.
    for slot in range(SLOT_COUNT):
        for hole_index, (hole_row, hole_position) in enumerate(HOLE_POSITIONS):
            sign_xor = xor_var(
                model,
                orientations[slot],
                holes[hole_index],
                f"carrier_hole_xor_{slot}_{hole_index}",
            )
            vectors = tuple(
                scalar_hole_vector(carriers[slot][carrier_type], hole_position)
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
            for label in range(8):
                projective_sign = VECTORS[label][hole_row]
                for carrier_type, vector in enumerate(vectors):
                    for orientation_parity in (0, 1):
                        multiplier = (
                            -projective_sign
                            if orientation_parity
                            else projective_sign
                        )
                        table_rows.append(
                            (
                                label,
                                carrier_type,
                                orientation_parity,
                                *(
                                    multiplier * vector[lag]
                                    for lag in active_lags
                                ),
                            )
                        )
            contributions = add_wide_contribution_table(
                model,
                (labels[slot], types[slot], sign_xor),
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
                model,
                holes[left],
                holes[right],
                f"hole_xor_{left}_{right}",
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
            for label in range(8):
                projective_sign = VECTORS[label][row]
                for carrier_type in range(TYPE_COUNT):
                    base_sum = sum(carriers[slot][carrier_type].values())
                    for orientation in (0, 1):
                        multiplier = -projective_sign if orientation else projective_sign
                        values.append(
                            (
                                label,
                                carrier_type,
                                orientation,
                                multiplier * base_sum,
                            )
                        )
            contribution_values = tuple(value[3] for value in values)
            contribution = model.new_int_var(
                min(contribution_values),
                max(contribution_values),
                f"rowsum_{row}_{slot}",
            )
            model.add_allowed_assignments(
                [
                    labels[slot],
                    types[slot],
                    orientations[slot],
                    contribution,
                ],
                values,
            )
            terms.append(contribution)
        for hole_index, (hole_row, _position) in enumerate(HOLE_POSITIONS):
            if hole_row == row:
                terms.append(1 - 2 * holes[hole_index])
        model.add(row_sums[row] == sum(terms))
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
        orientation = -1 if orientations[slot] else 1
        for row in range(4):
            multiplier = orientation * VECTORS[labels[slot]][row]
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
    parser.add_argument(
        "--projective-core",
        type=int,
        choices=range(32),
        help="fix alpha,beta,u5,u6,u7 to one five-bit structural shard",
    )
    parser.add_argument("--time-limit", type=float, default=1800.0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-memory-mb", type=int, default=8192)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    model, label_vars, type_vars, orientation_vars, hole_vars = build_model(
        args.quartet, args.projective_core
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    status = solver.solve(model)
    status_name = solver.status_name(status)
    print(f"status={status_name}")
    print(f"quartet={args.quartet}")
    print(
        "projective_core="
        + ("all" if args.projective_core is None else str(args.projective_core))
    )
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
        args.quartet,
        labels,
        types,
        orientations,
        holes,
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
        "quartet_index": args.quartet,
        "projective_core": args.projective_core,
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
        f"output/five_comb_unrestricted_q{args.quartet}.json"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"candidate={destination}")
    print("verified_hadamard_order=668")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
