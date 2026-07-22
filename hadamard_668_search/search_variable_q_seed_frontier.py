#!/usr/bin/env python3
"""Filter the first margin-plus-quad seed frontier with spectral identities.

The dependency-free seed-radius verifier enumerates every raw labelled margin
target near Eliahou's published seed and computes its exact minimum distance
subject to the mandatory endpoint-quad products.  This script builds one
small CP-SAT model for each surviving target, fixes its ordinary and
alternating margins, retains the raw Hamming ball, and adds the primitive
3rd-, 4th-, and 6th-root norm identities.  Optional primitive-7/14 or full
correlation layers can be enabled without changing the decomposition.

All models run sequentially with one worker and an explicit memory cap.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import lru_cache
import gc
import hashlib
import json
from pathlib import Path
import sys

from ortools.sat.python import cp_model

from construction import goethals_seidel, verify_hadamard
from search_variable_q_cp_sat import equality_literal
from seed import special_quadruple, summed_aperiodic_correlations
from variable_q_base import LONG, SHORT, base_correlations, base_to_special
from variable_q_seed_distance import SEED, build_model as build_relaxation, verify_witness
from verify_variable_q_seed_quad_radius import (
    MarginTarget,
    check_radius,
    coordinate_class_sums,
)
from verify_variable_q_seed_radius import distance_to_margins


ENERGY = 334
ROOT_COEFFICIENT_PAIRS = {
    3: ((1, 0, -1), (0, 1, -1), -1),
    4: ((1, 0, -1, 0), (0, 1, 0, -1), 0),
    6: ((1, 0, -1, -1, 0, 1), (0, 1, 1, 0, -1, -1), 1),
}
SHARD_287_MINIMUM_TARGET: MarginTarget = (
    (-18, 18),
    (0, 0),
    (3, 1),
    (-1, -3),
)


@lru_cache(maxsize=None)
def _quadratic_norm_rows(
    bound: int, cross_sign: int
) -> tuple[tuple[int, int, int], ...]:
    """Return ``(a,b,norm)`` rows with norm at most the global energy."""

    if bound < 0 or cross_sign not in (-1, 0, 1):
        raise ValueError("invalid quadratic norm table parameters")
    rows = []
    for first in range(-bound, bound + 1):
        for second in range(-bound, bound + 1):
            norm = (
                first * first
                + cross_sign * first * second
                + second * second
            )
            if norm <= ENERGY:
                rows.append((first, second, norm))
    return tuple(rows)


@lru_cache(maxsize=None)
def _restricted_quadratic_norm_rows(
    bound: int,
    cross_sign: int,
    first_low: int,
    first_high: int,
    second_low: int,
    second_high: int,
) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        row
        for row in _quadratic_norm_rows(bound, cross_sign)
        if first_low <= row[0] <= first_high
        and second_low <= row[1] <= second_high
    )


def add_small_root_table_invariants(
    model: cp_model.CpModel,
    sequences: tuple[list[cp_model.IntVar], ...],
    maximum_flips: tuple[int, int, int, int],
) -> None:
    """Add the primitive 3rd/4th/6th-root norms using exact tables.

    This is equivalent to ``add_small_root_spectral_invariants`` but avoids
    general multiplication constraints.  Since all four nonnegative norm
    contributions sum to 334, rows above 334 can be removed a priori.
    """

    totals: dict[int, list[cp_model.IntVar]] = {3: [], 4: [], 6: []}
    for label, bits, seed, flip_limit in zip(
        "abcd", sequences, SEED, maximum_flips, strict=True
    ):
        bound = len(bits)
        flips = tuple(
            bit.negated() if seed_value == 1 else bit
            for bit, seed_value in zip(bits, seed, strict=True)
        )
        for modulus, (first_pattern, second_pattern, cross_sign) in (
            ROOT_COEFFICIENT_PAIRS.items()
        ):
            first_coefficients = tuple(
                first_pattern[index % modulus] for index in range(bound)
            )
            second_coefficients = tuple(
                second_pattern[index % modulus] for index in range(bound)
            )
            first_base = sum(
                coefficient * value
                for coefficient, value in zip(
                    first_coefficients, seed, strict=True
                )
            )
            second_base = sum(
                coefficient * value
                for coefficient, value in zip(
                    second_coefficients, seed, strict=True
                )
            )
            maximum_change = 2 * flip_limit
            first_low = max(-bound, first_base - maximum_change)
            first_high = min(bound, first_base + maximum_change)
            second_low = max(-bound, second_base - maximum_change)
            second_high = min(bound, second_base + maximum_change)
            first = model.new_int_var(
                first_low, first_high, f"{label}_table_z{modulus}_first"
            )
            second = model.new_int_var(
                second_low, second_high, f"{label}_table_z{modulus}_second"
            )
            norm = model.new_int_var(
                0, ENERGY, f"{label}_table_z{modulus}_norm"
            )
            model.add(
                first
                == first_base
                + sum(
                    -2 * seed_value * coefficient * flip
                    for seed_value, coefficient, flip in zip(
                        seed, first_coefficients, flips, strict=True
                    )
                    if coefficient
                )
            )
            model.add(
                second
                == second_base
                + sum(
                    -2 * seed_value * coefficient * flip
                    for seed_value, coefficient, flip in zip(
                        seed, second_coefficients, flips, strict=True
                    )
                    if coefficient
                )
            )
            rows = _restricted_quadratic_norm_rows(
                bound,
                cross_sign,
                first_low,
                first_high,
                second_low,
                second_high,
            )
            if rows:
                model.add_allowed_assignments((first, second, norm), rows)
            else:
                model.add(0 == 1)
            totals[modulus].append(norm)

    for modulus in (3, 4, 6):
        model.add(sum(totals[modulus]) == ENERGY)


@dataclass(frozen=True)
class QuadOrbit:
    physical_groups: tuple[tuple[tuple[int, int], ...], ...]
    masks: tuple[int, ...]
    counts: tuple[cp_model.IntVar, ...]


@dataclass(frozen=True)
class QuadOrbitEncoding:
    orbits: tuple[QuadOrbit, ...]

    def decode(self, solver: cp_model.CpSolver) -> tuple[tuple[int, ...], ...]:
        sequences = [list(sequence) for sequence in SEED]
        for orbit in self.orbits:
            cursor = 0
            for mask, count in zip(orbit.masks, orbit.counts, strict=True):
                repetitions = solver.value(count)
                for _ in range(repetitions):
                    if cursor >= len(orbit.physical_groups):
                        raise AssertionError("quad-orbit count overflow")
                    group = orbit.physical_groups[cursor]
                    cursor += 1
                    for cell, (sequence_index, coordinate) in enumerate(group):
                        if mask >> cell & 1:
                            sequences[sequence_index][coordinate] *= -1
            if cursor != len(orbit.physical_groups):
                raise AssertionError("quad-orbit counts do not fill the orbit")
        return tuple(tuple(sequence) for sequence in sequences)


def _build_quad_orbits(model: cp_model.CpModel) -> QuadOrbitEncoding:
    raw_orbits: list[tuple[tuple[tuple[int, int], ...], ...]] = []
    for first_index, second_index in ((0, 1), (2, 3)):
        length = len(SEED[first_index])
        groups: dict[tuple, list[tuple[tuple[int, int], ...]]] = {}
        for left in range(length // 2):
            right = length - 1 - left
            physical = (
                (first_index, left),
                (first_index, right),
                (second_index, left),
                (second_index, right),
            )
            key = (
                first_index,
                tuple(coordinate % 12 for _index, coordinate in physical),
                tuple(SEED[index][coordinate] for index, coordinate in physical),
            )
            groups.setdefault(key, []).append(physical)
        raw_orbits.extend(tuple(group) for group in groups.values())

    # The two unpaired centre signs of the odd short sequences are free.
    short_centre = SHORT // 2
    raw_orbits.append((((2, short_centre), (3, short_centre)),))

    orbits = []
    for orbit_index, physical_groups in enumerate(raw_orbits):
        cell_count = len(physical_groups[0])
        require_even = cell_count == 4
        masks = tuple(
            mask
            for mask in range(1 << cell_count)
            if not require_even or mask.bit_count() % 2 == 0
        )
        multiplicity = len(physical_groups)
        counts = tuple(
            model.new_int_var(
                0,
                multiplicity,
                f"quad_orbit_{orbit_index}_mask_{mask}",
            )
            for mask in masks
        )
        model.add(sum(counts) == multiplicity)
        orbits.append(QuadOrbit(physical_groups, masks, counts))
    return QuadOrbitEncoding(tuple(orbits))


def _orbit_statistic(
    encoding: QuadOrbitEncoding,
    sequence_index: int,
    coefficients: tuple[int, ...],
):
    seed = SEED[sequence_index]
    expression = sum(
        coefficients[coordinate % len(coefficients)] * value
        for coordinate, value in enumerate(seed)
    )
    terms = []
    for orbit in encoding.orbits:
        representative = orbit.physical_groups[0]
        for mask, count in zip(orbit.masks, orbit.counts, strict=True):
            change = sum(
                -2
                * SEED[index][coordinate]
                * coefficients[coordinate % len(coefficients)]
                for cell, (index, coordinate) in enumerate(representative)
                if index == sequence_index and mask >> cell & 1
            )
            if change:
                terms.append(change * count)
    return expression + sum(terms)


def _orbit_distance(
    encoding: QuadOrbitEncoding,
    sequence_indices: frozenset[int] | None = None,
):
    terms = []
    for orbit in encoding.orbits:
        representative = orbit.physical_groups[0]
        for mask, count in zip(orbit.masks, orbit.counts, strict=True):
            cost = sum(
                1
                for cell, (index, _coordinate) in enumerate(representative)
                if mask >> cell & 1
                and (sequence_indices is None or index in sequence_indices)
            )
            if cost:
                terms.append(cost * count)
    return sum(terms)


def build_quad_orbit_root_model(
    target: MarginTarget,
    radius: int,
    *,
    minimum_distance: int = 0,
    pair_distance_lower_bounds: tuple[int, int] | None = None,
) -> tuple[cp_model.CpModel, QuadOrbitEncoding]:
    """Build the exact modulo-12 orbit quotient of the root relaxation."""

    if radius < 0 or not 0 <= minimum_distance <= radius:
        raise ValueError("distance interval must satisfy 0 <= minimum <= radius")
    model = cp_model.CpModel()
    encoding = _build_quad_orbits(model)

    for sequence_index, (ordinary, alternating) in enumerate(target):
        model.add(
            _orbit_statistic(encoding, sequence_index, (1,)) == ordinary
        )
        model.add(
            _orbit_statistic(encoding, sequence_index, (1, -1))
            == alternating
        )

    distance = _orbit_distance(encoding)
    model.add(distance <= radius)
    model.add(distance >= minimum_distance)
    if pair_distance_lower_bounds is not None:
        long_lower, short_lower = pair_distance_lower_bounds
        if min(long_lower, short_lower) < 0 or long_lower + short_lower > radius:
            raise ValueError("invalid pair-distance lower bounds")
        model.add(_orbit_distance(encoding, frozenset((0, 1))) >= long_lower)
        model.add(_orbit_distance(encoding, frozenset((2, 3))) >= short_lower)

    totals: dict[int, list[cp_model.IntVar]] = {3: [], 4: [], 6: []}
    for modulus, (first_pattern, second_pattern, cross_sign) in (
        ROOT_COEFFICIENT_PAIRS.items()
    ):
        for sequence_index, sequence in enumerate(SEED):
            bound = len(sequence)
            first = model.new_int_var(
                -bound,
                bound,
                f"orbit_{sequence_index}_z{modulus}_first",
            )
            second = model.new_int_var(
                -bound,
                bound,
                f"orbit_{sequence_index}_z{modulus}_second",
            )
            norm = model.new_int_var(
                0,
                ENERGY,
                f"orbit_{sequence_index}_z{modulus}_norm",
            )
            model.add(
                first
                == _orbit_statistic(encoding, sequence_index, first_pattern)
            )
            model.add(
                second
                == _orbit_statistic(encoding, sequence_index, second_pattern)
            )
            model.add_allowed_assignments(
                (first, second, norm),
                _quadratic_norm_rows(bound, cross_sign),
            )
            totals[modulus].append(norm)
        model.add(sum(totals[modulus]) == ENERGY)
    return model, encoding


def add_flip_direction_budget(
    model: cp_model.CpModel,
    sequences: tuple[list[cp_model.IntVar], ...],
    target: MarginTarget,
    radius: int,
    *,
    exact_distance: bool = False,
) -> None:
    """Expose the exact classwise flip counts implied by fixed margins.

    In one coordinate class, let ``delta`` be half the desired change in its
    sign sum.  If ``delta > 0``, at least ``delta`` seed-minus signs must flip
    and every seed-plus flip requires one additional compensating seed-minus
    flip.  The other signs are symmetric.  Thus the total number of
    opposite-direction flips over all eight classes is exactly half the
    excess over the unconstrained margin distance.  Stating these redundant
    cardinalities explicitly gives CP-SAT much stronger propagation.
    """

    minimum = distance_to_margins(target)
    if minimum > radius:
        raise ValueError("fixed target lies outside the requested seed ball")
    extra_pairs = (radius - minimum) // 2
    wrong_direction_counts = []
    for sequence_index, (bits, margins, seed) in enumerate(
        zip(sequences, target, SEED, strict=True)
    ):
        ordinary, alternating = margins
        desired = (
            (ordinary + alternating) // 2,
            (ordinary - alternating) // 2,
        )
        current = coordinate_class_sums(seed)
        for parity in (0, 1):
            class_change = desired[parity] - current[parity]
            if class_change % 2:
                raise ValueError("fixed target has unreachable class parity")
            delta = class_change // 2
            plus_seed_flips = [
                bits[index].negated()
                for index in range(parity, len(bits), 2)
                if seed[index] == 1
            ]
            minus_seed_flips = [
                bits[index]
                for index in range(parity, len(bits), 2)
                if seed[index] == -1
            ]
            wrong = model.new_int_var(
                0,
                extra_pairs,
                f"wrong_direction_{sequence_index}_{parity}",
            )
            if delta >= 0:
                model.add(sum(plus_seed_flips) == wrong)
                model.add(sum(minus_seed_flips) == delta + wrong)
            else:
                model.add(sum(minus_seed_flips) == wrong)
                model.add(sum(plus_seed_flips) == -delta + wrong)
            wrong_direction_counts.append(wrong)
    if exact_distance:
        model.add(sum(wrong_direction_counts) == extra_pairs)
    else:
        model.add(sum(wrong_direction_counts) <= extra_pairs)


def add_radius_sixteen_shard_287_structure(
    model: cp_model.CpModel,
    sequences: tuple[list[cp_model.IntVar], ...],
    target: MarginTarget,
    radius: int,
) -> bool:
    """Expose the rigid flip structure of the sole hard radius-16 target.

    The target changes only A's odd-coordinate class and requires eight
    positive-to-negative flips there.  Those coordinates occupy distinct
    long endpoint quads.  Preserving quad products needs at least one partner
    flip in each selected quad.  At radius 16 equality is forced: exactly
    eight such A coordinates flip, exactly one of the other three cells in
    each selected quad flips, and every other sign is unchanged.
    """

    if radius != 16 or target != SHARD_287_MINIMUM_TARGET:
        return False
    flips = tuple(
        tuple(
            bit.negated() if seed_value == 1 else bit
            for bit, seed_value in zip(bits, seed, strict=True)
        )
        for bits, seed in zip(sequences, SEED, strict=True)
    )
    selected = []
    for left in range(LONG // 2):
        right = LONG - 1 - left
        odd = left if left % 2 else right
        even = right if left % 2 else left
        a_odd_flip = flips[0][odd]
        partners = (flips[0][even], flips[1][left], flips[1][right])
        if SEED[0][odd] == 1:
            model.add(sum(partners) == a_odd_flip)
            selected.append(a_odd_flip)
        else:
            model.add(a_odd_flip == 0)
            model.add(sum(partners) == 0)
    model.add(sum(selected) == 8)
    for group in flips[2:]:
        for flip in group:
            model.add(flip == 0)
    return True


def add_exchangeable_quad_symmetry_breaking(
    model: cp_model.CpModel,
    sequences: tuple[list[cp_model.IntVar], ...],
) -> int:
    """Order endpoint-quad flip masks inside exact root-layer orbits.

    With only margins, distance, endpoint products, and the primitive
    3rd/4th/6th-root identities active, coordinates are distinguished modulo
    12.  Two endpoint quads in the same long or short pair are therefore
    exchangeable when their oriented seed signs and endpoint residues agree.
    Sorting their four-bit flip masks chooses one representative per orbit.

    This reduction is not valid once length-7/14 compression or individual
    correlation lags are active, so callers must omit it at those layers.
    """

    constraints = 0
    for first_index, second_index in ((0, 1), (2, 3)):
        first = sequences[first_index]
        second = sequences[second_index]
        length = len(first)
        groups: dict[tuple, list[tuple[cp_model.IntVar, ...]]] = {}
        for left in range(length // 2):
            right = length - 1 - left
            coordinates = (
                (first_index, left),
                (first_index, right),
                (second_index, left),
                (second_index, right),
            )
            key = (
                first_index,
                left % 12,
                right % 12,
                tuple(SEED[index][coordinate] for index, coordinate in coordinates),
            )
            flips = tuple(
                sequences[index][coordinate].negated()
                if SEED[index][coordinate] == 1
                else sequences[index][coordinate]
                for index, coordinate in coordinates
            )
            groups.setdefault(key, []).append(flips)

        for orbit in groups.values():
            for earlier, later in zip(orbit, orbit[1:]):
                model.add(
                    sum((1 << index) * flip for index, flip in enumerate(earlier))
                    <= sum(
                        (1 << index) * flip
                        for index, flip in enumerate(later)
                    )
                )
                constraints += 1
    return constraints


def build_target_model(
    target: MarginTarget,
    radius: int,
    *,
    minimum_distance: int = 0,
    pair_distance_lower_bounds: tuple[int, int] | None = None,
    compression_7: bool = False,
    compression_7_alternating: bool = False,
    full_correlations: bool = False,
    small_root_encoding: str = "table",
) -> tuple[cp_model.CpModel, tuple[list[cp_model.IntVar], ...]]:
    """Build one fixed-margin seed-ball model at the selected proof layer."""

    if radius < 0 or not 0 <= minimum_distance <= radius:
        raise ValueError("distance interval must satisfy 0 <= minimum <= radius")
    if small_root_encoding not in ("table", "multiplication"):
        raise ValueError("small_root_encoding must be table or multiplication")
    minimum_by_sequence = []
    for seed, (ordinary, alternating) in zip(SEED, target, strict=True):
        desired = (
            (ordinary + alternating) // 2,
            (ordinary - alternating) // 2,
        )
        current = coordinate_class_sums(seed)
        minimum_by_sequence.append(
            sum(
                abs(wanted - present) // 2
                for wanted, present in zip(desired, current, strict=True)
            )
        )
    total_minimum = sum(minimum_by_sequence)
    if total_minimum > radius:
        raise ValueError("fixed target lies outside the requested seed ball")
    extra_pairs = (radius - total_minimum) // 2
    maximum_flips = tuple(
        minimum + 2 * extra_pairs for minimum in minimum_by_sequence
    )

    model, sequences = build_relaxation(
        small_roots=small_root_encoding == "multiplication",
        compression_7=compression_7,
        compression_7_alternating=compression_7_alternating,
    )
    if small_root_encoding == "table":
        add_small_root_table_invariants(model, sequences, maximum_flips)
    model.clear_objective()
    for bits, (ordinary, alternating) in zip(sequences, target, strict=True):
        model.add(2 * sum(bits) - len(bits) == ordinary)
        model.add(
            sum(
                (1 if index % 2 == 0 else -1) * (2 * bit - 1)
                for index, bit in enumerate(bits)
            )
            == alternating
        )

    differences_by_sequence = tuple(
        tuple(
            bit.negated() if seed_value == 1 else bit
            for bit, seed_value in zip(bits, seed, strict=True)
        )
        for bits, seed in zip(sequences, SEED, strict=True)
    )
    differences = tuple(
        difference
        for group in differences_by_sequence
        for difference in group
    )
    model.add(sum(differences) <= radius)
    model.add(sum(differences) >= minimum_distance)
    if pair_distance_lower_bounds is not None:
        long_lower, short_lower = pair_distance_lower_bounds
        if min(long_lower, short_lower) < 0 or long_lower + short_lower > radius:
            raise ValueError("invalid pair-distance lower bounds")
        model.add(
            sum(differences_by_sequence[0] + differences_by_sequence[1])
            >= long_lower
        )
        model.add(
            sum(differences_by_sequence[2] + differences_by_sequence[3])
            >= short_lower
        )
    add_flip_direction_budget(
        model,
        sequences,
        target,
        radius,
        exact_distance=minimum_distance == radius,
    )
    add_radius_sixteen_shard_287_structure(model, sequences, target, radius)

    if not compression_7 and not compression_7_alternating and not full_correlations:
        add_exchangeable_quad_symmetry_breaking(model, sequences)

    if full_correlations:
        for lag in range(1, LONG):
            terms = []
            for label, bits in zip("abcd", sequences, strict=True):
                terms.extend(
                    equality_literal(
                        model,
                        bits[index],
                        bits[index + lag],
                        f"{label}{label}_frontier_{lag}_{index}",
                    )
                    for index in range(len(bits) - lag)
                )
            model.add(sum(terms) == len(terms) // 2)
    return model, sequences


def _signs(
    solver: cp_model.CpSolver, variables: list[cp_model.IntVar]
) -> tuple[int, ...]:
    return tuple(1 if solver.value(variable) else -1 for variable in variables)


def _verify_exact(sequences: tuple[tuple[int, ...], ...]) -> None:
    if base_correlations(*sequences) != (334,) + (0,) * 83:
        raise AssertionError("frontier candidate failed exact base correlations")
    s, q = base_to_special(*sequences)
    if any(summed_aperiodic_correlations(special_quadruple(s, q))[1:]):
        raise AssertionError("frontier candidate failed exact special correlations")
    verify_hadamard(goethals_seidel(special_quadruple(s, q)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--radius", type=int, default=14)
    parser.add_argument("--minimum-distance", type=int, default=0)
    parser.add_argument("--compression-7", action="store_true")
    parser.add_argument("--compression-7-alternating", action="store_true")
    parser.add_argument("--full-correlations", action="store_true")
    parser.add_argument(
        "--small-root-encoding",
        choices=("table", "multiplication"),
        default="table",
    )
    parser.add_argument(
        "--quad-encoding",
        choices=("bits", "orbit-counts"),
        default="bits",
        help=(
            "encode every sign or use the exact modulo-12 endpoint-quad "
            "quotient (root-only layers)"
        ),
    )
    parser.add_argument("--time-limit-per-target", type=float, default=30.0)
    parser.add_argument("--max-memory-mb", type=int, default=256)
    parser.add_argument("--random-seed", type=int, default=668)
    parser.add_argument(
        "--targets-from",
        type=Path,
        help=(
            "solve selected targets recorded by an earlier compatible "
            "frontier JSON artifact"
        ),
    )
    parser.add_argument(
        "--targets-from-mode",
        choices=("witnesses", "timeouts", "unresolved"),
        default="witnesses",
        help=(
            "with --targets-from, select only FEASIBLE/OPTIMAL witnesses "
            "only UNKNOWN timeouts, or every result not already proved "
            "INFEASIBLE"
        ),
    )
    parser.add_argument(
        "--resume-from",
        type=Path,
        help="reuse INFEASIBLE records from a compatible earlier JSON run",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/variable_q_seed_frontier_root_filter.json"),
    )
    return parser.parse_args()


def _result_key(result: dict) -> tuple[int, MarginTarget]:
    target = tuple(tuple(int(entry) for entry in pair) for pair in result["target"])
    if len(target) != 4 or any(len(pair) != 2 for pair in target):
        raise ValueError("frontier artifact target has the wrong shape")
    return int(result["shard"]), target  # type: ignore[return-value]


def select_prior_survivors(
    frontier: tuple,
    artifact_path: Path,
    *,
    radius: int,
    minimum_distance: int,
    selection_mode: str = "witnesses",
) -> tuple[tuple, str]:
    """Select prior live targets while checking their provenance exactly."""

    raw = artifact_path.read_bytes()
    previous = json.loads(raw)
    selected_statuses = {
        "witnesses": frozenset(("FEASIBLE", "OPTIMAL")),
        "timeouts": frozenset(("UNKNOWN",)),
        "unresolved": frozenset(("FEASIBLE", "OPTIMAL", "UNKNOWN")),
    }
    if selection_mode not in selected_statuses:
        raise ValueError("invalid survivor selection mode")
    if (
        previous.get("kind") != "variable-q-seed-frontier-filter"
        or previous.get("radius") != radius
        or previous.get("minimum_distance", 0) != minimum_distance
    ):
        raise ValueError("incompatible survivor-source certificate")

    expected = {(record.shard, record.target): record for record in frontier}
    selected_keys = []
    seen = set()
    for result in previous.get("results", ()):
        key = _result_key(result)
        if key not in expected:
            raise ValueError("survivor-source certificate contains an unknown target")
        if key in seen:
            raise ValueError("survivor-source certificate contains a duplicate target")
        seen.add(key)
        if result.get("status") in selected_statuses[selection_mode]:
            selected_keys.append(key)
    if not selected_keys:
        raise ValueError("survivor-source certificate has no selected targets")
    selected = tuple(expected[key] for key in selected_keys)
    return selected, hashlib.sha256(raw).hexdigest()


def main() -> int:
    args = parse_args()
    if (
        args.radius < 0
        or not 0 <= args.minimum_distance <= args.radius
        or args.time_limit_per_target <= 0
        or args.max_memory_mb <= 0
    ):
        print(
            "error=distance interval must be valid and limits positive",
            file=sys.stderr,
        )
        return 2
    if args.quad_encoding == "orbit-counts" and (
        args.small_root_encoding != "table"
        or args.compression_7
        or args.compression_7_alternating
        or args.full_correlations
    ):
        print(
            "error=orbit-counts supports only the table-encoded root layer",
            file=sys.stderr,
        )
        return 2

    radius_check = check_radius(args.radius)
    frontier_records = []
    parity_skipped = 0
    for record in radius_check.targets:
        if record.quad_distance is None or record.quad_distance > args.radius:
            continue
        first_possible = max(args.minimum_distance, record.quad_distance)
        if (first_possible - record.margin_distance) % 2:
            first_possible += 1
        if first_possible > args.radius:
            parity_skipped += 1
            continue
        frontier_records.append(record)
    complete_frontier = tuple(frontier_records)
    frontier = complete_frontier
    targets_from_sha256 = None
    if args.targets_from:
        try:
            frontier, targets_from_sha256 = select_prior_survivors(
                complete_frontier,
                args.targets_from,
                radius=args.radius,
                minimum_distance=args.minimum_distance,
                selection_mode=args.targets_from_mode,
            )
        except (OSError, ValueError, json.JSONDecodeError, KeyError, TypeError) as error:
            print(f"error={error}", file=sys.stderr)
            return 2
    print(f"distance_interval=[{args.minimum_distance},{args.radius}]")
    print(f"complete_margin_plus_quad_frontier={len(complete_frontier)}")
    print(f"selected_frontier={len(frontier)}")
    if args.targets_from:
        print(f"targets_from={args.targets_from}")
        print(f"targets_from_mode={args.targets_from_mode}")
        print(f"targets_from_sha256={targets_from_sha256}")
    print(f"parity_skipped={parity_skipped}")
    print(f"workers=1 max_memory_mb={args.max_memory_mb}")

    reused_results = {}
    if args.resume_from:
        previous = json.loads(args.resume_from.read_text(encoding="utf-8"))
        previous_layers = previous.get("layers", {})
        expected_layers = {
            "small_roots": True,
            "small_root_encoding": args.small_root_encoding,
            "quad_encoding": args.quad_encoding,
            "compression_7": args.compression_7,
            "compression_7_alternating": args.compression_7_alternating,
            "full_correlations": args.full_correlations,
            "exchangeable_quad_symmetry": not (
                args.compression_7
                or args.compression_7_alternating
                or args.full_correlations
            ),
            "radius_16_shard_287_structure": args.radius == 16,
        }
        if (
            previous.get("kind") != "variable-q-seed-frontier-filter"
            or previous.get("radius") != args.radius
            or previous.get("minimum_distance", 0) != args.minimum_distance
            or previous.get("frontier_size") != len(frontier)
            or previous_layers != expected_layers
        ):
            print("error=incompatible resume certificate", file=sys.stderr)
            return 2
        for result in previous.get("results", ()):
            if result.get("status") == "INFEASIBLE":
                key = _result_key(result)
                reused_results[key] = result
        print(f"reused_infeasible={len(reused_results)}")

    results = []
    for attempt, record in enumerate(frontier, start=1):
        record_key = (record.shard, record.target)
        if record_key in reused_results:
            result = dict(reused_results[record_key])
            result["reused"] = True
            results.append(result)
            continue
        pair_bounds = (
            int(record.long_distance),
            int(record.short_distance),
        )
        orbit_encoding = None
        variables = None
        if args.quad_encoding == "orbit-counts":
            model, orbit_encoding = build_quad_orbit_root_model(
                record.target,
                args.radius,
                minimum_distance=args.minimum_distance,
                pair_distance_lower_bounds=pair_bounds,
            )
        else:
            model, variables = build_target_model(
                record.target,
                args.radius,
                minimum_distance=args.minimum_distance,
                pair_distance_lower_bounds=pair_bounds,
                compression_7=args.compression_7,
                compression_7_alternating=args.compression_7_alternating,
                full_correlations=args.full_correlations,
                small_root_encoding=args.small_root_encoding,
            )
        validation = model.validate()
        if validation:
            print(f"error=invalid model: {validation}", file=sys.stderr)
            return 2
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = args.time_limit_per_target
        solver.parameters.num_search_workers = 1
        solver.parameters.max_memory_in_mb = args.max_memory_mb
        solver.parameters.random_seed = args.random_seed
        status = solver.solve(model)
        status_name = solver.status_name(status)
        result = {
            "shard": record.shard,
            "margin_distance": record.margin_distance,
            "quad_distance": record.quad_distance,
            "target": [list(pair) for pair in record.target],
            "status": status_name,
            "wall_time": solver.wall_time,
            "conflicts": solver.num_conflicts,
            "branches": solver.num_branches,
        }
        if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            if orbit_encoding is not None:
                sequences = orbit_encoding.decode(solver)
            else:
                if variables is None:
                    raise AssertionError("missing bit-level frontier variables")
                sequences = tuple(_signs(solver, group) for group in variables)
            witness = verify_witness(
                sequences,
                small_roots=True,
                compression_7=args.compression_7,
                compression_7_alternating=args.compression_7_alternating,
            )
            if tuple(
                (witness.ordinary[index], witness.alternating[index])
                for index in range(4)
            ) != record.target:
                raise AssertionError("decoded witness has the wrong fixed margins")
            if witness.distance > args.radius:
                raise AssertionError("decoded witness lies outside the seed ball")
            if args.full_correlations:
                _verify_exact(sequences)
            result["distance"] = witness.distance
            result["sequences"] = {
                label: list(sequence)
                for label, sequence in zip("abcd", sequences, strict=True)
            }
        results.append(result)
        print(
            f"attempt={attempt}/{len(frontier)} shard={record.shard} "
            f"status={status_name} wall_time={solver.wall_time:.3f} "
            f"branches={solver.num_branches}"
        )
        del solver, model, variables, orbit_encoding
        gc.collect()

    payload = {
        "kind": "variable-q-seed-frontier-filter",
        "radius": args.radius,
        "minimum_distance": args.minimum_distance,
        "parity_skipped": parity_skipped,
        "frontier_size": len(frontier),
        "complete_frontier_size": len(complete_frontier),
        "targets_from": str(args.targets_from) if args.targets_from else None,
        "targets_from_mode": args.targets_from_mode if args.targets_from else None,
        "targets_from_sha256": targets_from_sha256,
        "layers": {
            "small_roots": True,
            "small_root_encoding": args.small_root_encoding,
            "quad_encoding": args.quad_encoding,
            "compression_7": args.compression_7,
            "compression_7_alternating": args.compression_7_alternating,
            "full_correlations": args.full_correlations,
            "exchangeable_quad_symmetry": not (
                args.compression_7
                or args.compression_7_alternating
                or args.full_correlations
            ),
            "radius_16_shard_287_structure": args.radius == 16,
        },
        "workers": 1,
        "max_memory_mb": args.max_memory_mb,
        "time_limit_per_target": args.time_limit_per_target,
        "resume_from": str(args.resume_from) if args.resume_from else None,
        "reused_infeasible": len(reused_results),
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote={args.output}")

    counts = {
        name: sum(result["status"] == name for result in results)
        for name in ("INFEASIBLE", "FEASIBLE", "OPTIMAL", "UNKNOWN")
    }
    print(f"status_counts={counts}")
    if results and counts["INFEASIBLE"] == len(results):
        if len(frontier) == len(complete_frontier):
            print(
                "PASS: the selected spectral layer excludes the complete "
                f"margin-plus-quad frontier at radius {args.radius}"
            )
        else:
            print(
                "PASS: the selected spectral layer excludes all "
                f"{len(frontier)} targets carried from the source artifact"
            )
        return 0
    if counts["UNKNOWN"]:
        print("INCOMPLETE: at least one frontier model timed out")
        return 1
    print("SURVIVORS: at least one necessary-condition model is feasible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
