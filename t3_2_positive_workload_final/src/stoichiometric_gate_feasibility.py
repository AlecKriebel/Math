"""Exact affine-stoichiometric feasibility for tier gate descriptors.

This module answers a geometric question only. Given a support pair and a
tier descriptor, can one sequence with that descriptor lie in one affine
stoichiometric class? A feasible descriptor is not a recurrence or
transience certificate.

All linear algebra and inequality elimination use fractions.Fraction.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from math import gcd, lcm
import json
from typing import Iterable

import global_atlas_interface_closure as closure
import global_tier_interface as tier


Q = Fraction
Vector = tuple[Q, Q, Q]
IntegerVector = tuple[int, int, int]
Pair = closure.Pair


@dataclass(frozen=True)
class LevelCertificate:
    """Primal direction or dual invariant at one positive weight level."""

    level: int
    equal_coordinates: tuple[int, ...]
    higher_coordinates: tuple[int, ...]
    feasible: bool
    direction: Vector | None
    invariant: Vector | None


@dataclass(frozen=True)
class WeightCertificate:
    """The complete flag test for one stoichiometric space and log weight."""

    feasible: bool
    levels: tuple[LevelCertificate, ...]


def _rref(
    matrix: Iterable[Iterable[int | Q]],
    column_count: int,
) -> tuple[tuple[tuple[Q, ...], ...], tuple[int, ...]]:
    rows = [[Q(value) for value in row] for row in matrix]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (
                index
                for index in range(pivot_row, len(rows))
                if rows[index][column]
            ),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot for value in rows[pivot_row]]
        for index, row in enumerate(rows):
            if index == pivot_row or not row[column]:
                continue
            multiplier = row[column]
            rows[index] = [
                row[position] - multiplier * rows[pivot_row][position]
                for position in range(column_count)
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    nonzero = tuple(
        tuple(row) for row in rows if any(value != 0 for value in row)
    )
    return nonzero, tuple(pivot_columns)


def _nullspace(
    matrix: Iterable[Iterable[int | Q]],
    column_count: int,
) -> tuple[tuple[Q, ...], ...]:
    rows, pivots = _rref(matrix, column_count)
    free_columns = tuple(
        column for column in range(column_count) if column not in pivots
    )
    basis: list[tuple[Q, ...]] = []
    for free in free_columns:
        vector = [Q(0) for _ in range(column_count)]
        vector[free] = Q(1)
        for row_index, pivot in enumerate(pivots):
            vector[pivot] = -rows[row_index][free]
        basis.append(tuple(vector))
    return tuple(basis)


def _solve_inequalities(
    inequalities: Iterable[tuple[Iterable[int | Q], int | Q]],
    variable_count: int,
) -> tuple[Q, ...] | None:
    """Solve coefficient dot x >= rhs by exact Fourier--Motzkin."""

    system = tuple(
        (tuple(Q(value) for value in coefficients), Q(rhs))
        for coefficients, rhs in inequalities
    )

    def solve(
        current: tuple[tuple[tuple[Q, ...], Q], ...],
        dimensions: int,
    ) -> tuple[Q, ...] | None:
        if dimensions == 0:
            return () if all(rhs <= 0 for _, rhs in current) else None

        column = dimensions - 1
        positive = tuple(item for item in current if item[0][column] > 0)
        negative = tuple(item for item in current if item[0][column] < 0)
        zero = tuple(item for item in current if item[0][column] == 0)
        projected: list[tuple[tuple[Q, ...], Q]] = [
            (coefficients[:column], rhs) for coefficients, rhs in zero
        ]
        if positive and negative:
            for pos_coefficients, pos_rhs in positive:
                for neg_coefficients, neg_rhs in negative:
                    pos_value = pos_coefficients[column]
                    neg_value = neg_coefficients[column]
                    projected.append(
                        (
                            tuple(
                                (-neg_value) * pos_coefficients[index]
                                + pos_value * neg_coefficients[index]
                                for index in range(column)
                            ),
                            (-neg_value) * pos_rhs + pos_value * neg_rhs,
                        )
                    )

        prefix = solve(tuple(projected), dimensions - 1)
        if prefix is None:
            return None

        lower: list[Q] = []
        upper: list[Q] = []
        for coefficients, rhs in current:
            remainder = sum(
                coefficients[index] * prefix[index] for index in range(column)
            )
            coefficient = coefficients[column]
            if coefficient > 0:
                lower.append((rhs - remainder) / coefficient)
            elif coefficient < 0:
                upper.append((rhs - remainder) / coefficient)
            elif remainder < rhs:
                return None
        lower_bound = max(lower) if lower else None
        upper_bound = min(upper) if upper else None
        if (
            lower_bound is not None
            and upper_bound is not None
            and lower_bound > upper_bound
        ):
            return None
        if lower_bound is not None and upper_bound is not None:
            value = (lower_bound + upper_bound) / 2
        elif lower_bound is not None:
            value = lower_bound
        elif upper_bound is not None:
            value = upper_bound
        else:
            value = Q(0)
        return prefix + (value,)

    return solve(system, variable_count)


def _linear_combination(
    coefficients: tuple[Q, ...],
    basis: tuple[tuple[Q, ...], ...],
    dimension: int = 3,
) -> tuple[Q, ...]:
    return tuple(
        sum(
            coefficients[index] * basis[index][coordinate]
            for index in range(len(basis))
        )
        for coordinate in range(dimension)
    )


def _primitive_integer(vector: tuple[Q, ...]) -> tuple[int, ...]:
    denominator = 1
    for value in vector:
        denominator = lcm(denominator, value.denominator)
    integers = [int(value * denominator) for value in vector]
    common = 0
    for value in integers:
        common = gcd(common, abs(value))
    if common:
        integers = [value // common for value in integers]
    return tuple(integers)


@lru_cache(maxsize=None)
def stoichiometric_basis(pair: Pair) -> tuple[Vector, ...]:
    """A reduced rational row basis of the full stoichiometric subspace."""

    generators: list[IntegerVector] = []
    for mask in pair:
        nodes = tuple(sorted(tier._nodes(mask)))
        anchor = closure.COMPLEXES[nodes[0]]
        generators.extend(
            tuple(
                closure.COMPLEXES[node][coordinate] - anchor[coordinate]
                for coordinate in range(3)
            )
            for node in nodes[1:]
        )
    return tuple(tuple(value for value in row) for row in _rref(generators, 3)[0])


@lru_cache(maxsize=None)
def invariant_basis(pair: Pair) -> tuple[Vector, ...]:
    """A rational basis of the common affine invariants."""

    return tuple(
        tuple(value for value in vector)
        for vector in _nullspace(stoichiometric_basis(pair), 3)
    )


def _subspace_level_certificate(
    stoichiometric_space: tuple[Vector, ...],
    weight: IntegerVector,
    level: int,
) -> LevelCertificate:
    invariants = _nullspace(stoichiometric_space, 3)
    equal = tuple(index for index, value in enumerate(weight) if value == level)
    higher = tuple(index for index, value in enumerate(weight) if value > level)
    lower = tuple(index for index, value in enumerate(weight) if value < level)

    zero_lower = tuple(
        tuple(Q(1) if coordinate == index else Q(0) for coordinate in range(3))
        for index in lower
    )
    permitted = _nullspace(invariants + zero_lower, 3)
    primal_inequalities = tuple(
        (tuple(vector[index] for vector in permitted), Q(1))
        for index in equal
    )
    primal = _solve_inequalities(primal_inequalities, len(permitted))
    if primal is not None:
        direction = _linear_combination(primal, permitted)
        return LevelCertificate(
            level,
            equal,
            higher,
            True,
            tuple(Q(value) for value in _primitive_integer(direction)),
            None,
        )

    # Gordan's alternative: find y >= 0, sum(y)=1, with P^T y=0.
    dual_inequalities: list[tuple[tuple[Q, ...], Q]] = []
    for index in range(len(equal)):
        dual_inequalities.append(
            (
                tuple(
                    Q(1) if position == index else Q(0)
                    for position in range(len(equal))
                ),
                Q(0),
            )
        )
    ones = tuple(Q(1) for _ in equal)
    dual_inequalities.extend(((ones, Q(1)), (tuple(-x for x in ones), Q(-1))))
    for basis_index in range(len(permitted)):
        row = tuple(permitted[basis_index][index] for index in equal)
        dual_inequalities.extend(((row, Q(0)), (tuple(-x for x in row), Q(0))))
    dual = _solve_inequalities(dual_inequalities, len(equal))
    if dual is None:
        raise AssertionError("Gordan alternative failed")

    target = {
        coordinate: (
            dual[equal.index(coordinate)] if coordinate in equal else Q(0)
        )
        for coordinate in equal + higher
    }
    invariant_equations: list[tuple[tuple[Q, ...], Q]] = []
    for coordinate in equal + higher:
        row = tuple(vector[coordinate] for vector in invariants)
        invariant_equations.extend(
            ((row, target[coordinate]), (tuple(-x for x in row), -target[coordinate]))
        )
    invariant_coefficients = _solve_inequalities(
        invariant_equations,
        len(invariants),
    )
    if invariant_coefficients is None:
        raise AssertionError("dual functional did not extend to an invariant")
    invariant = _linear_combination(invariant_coefficients, invariants)
    return LevelCertificate(
        level,
        equal,
        higher,
        False,
        None,
        tuple(Q(value) for value in _primitive_integer(invariant)),
    )


@lru_cache(maxsize=None)
def subspace_weight_certificate(
    stoichiometric_space: tuple[Vector, ...],
    weight: IntegerVector,
) -> WeightCertificate:
    """Apply the exact level-by-level flag criterion to a rational subspace."""

    levels = tuple(
        _subspace_level_certificate(stoichiometric_space, weight, level)
        for level in sorted({value for value in weight if value > 0}, reverse=True)
    )
    return WeightCertificate(
        all(certificate.feasible for certificate in levels),
        levels,
    )


@lru_cache(maxsize=None)
def pair_weight_certificate(pair: Pair, weight: IntegerVector) -> WeightCertificate:
    return subspace_weight_certificate(stoichiometric_basis(pair), weight)


def descriptor_feasible(pair: Pair, descriptor: tier.TierDescriptor) -> bool:
    """Whether the descriptor is realizable in some affine class of the pair."""

    return pair_weight_certificate(pair, descriptor.weight).feasible


def fixed_class_base(
    pair: Pair,
    descriptor: tier.TierDescriptor,
    class_point: tuple[int | Q, int | Q, int | Q],
) -> Vector | None:
    """Find a real base point with the descriptor caps in class_point + S."""

    basis = stoichiometric_basis(pair)
    inequalities: list[tuple[tuple[Q, ...], Q]] = []
    for coordinate, weight in enumerate(descriptor.weight):
        if weight:
            continue
        row = tuple(vector[coordinate] for vector in basis)
        target = Q(descriptor.caps[coordinate]) - Q(class_point[coordinate])
        if descriptor.caps[coordinate] < 2:
            inequalities.extend(((row, target), (tuple(-x for x in row), -target)))
        else:
            inequalities.append((row, target))
    coefficients = _solve_inequalities(inequalities, len(basis))
    if coefficients is None:
        return None
    displacement = _linear_combination(coefficients, basis)
    return tuple(
        Q(class_point[index]) + displacement[index] for index in range(3)
    )


def fixed_class_descriptor_feasible(
    pair: Pair,
    descriptor: tier.TierDescriptor,
    class_point: tuple[int | Q, int | Q, int | Q],
) -> bool:
    """The flag criterion plus the cap/base condition in one fixed class."""

    return descriptor_feasible(pair, descriptor) and fixed_class_base(
        pair, descriptor, class_point
    ) is not None


def _residual_failures() -> tuple[frozenset[Pair], frozenset[Pair], frozenset[Pair]]:
    positive = tier.tier_split(closure.POSITIVE_SHIELDED_MASKS)[1]
    signed = tier.tier_split(closure.SIGNED_SHIELDED_MASKS)[1]
    return positive, signed, positive | signed


@lru_cache(maxsize=None)
def feasible_failing_descriptors(pair: Pair) -> tuple[tier.TierDescriptor, ...]:
    return tuple(
        descriptor
        for descriptor in tier.tier_descriptors()
        if not tier.universal_orientation_tier_condition(pair, descriptor)
        and descriptor_feasible(pair, descriptor)
    )


def _incidence_fingerprint(
    incidences: Iterable[tuple[Pair, tier.TierDescriptor]],
) -> str:
    ordered = sorted(
        incidences,
        key=lambda item: (
            closure.pair_payload(item[0]),
            item[1].weight,
            item[1].caps,
        ),
    )
    payload = [
        {
            "pair": closure.pair_payload(pair),
            "weight": list(descriptor.weight),
            "caps": list(descriptor.caps),
        }
        for pair, descriptor in ordered
    ]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def canonical_gate_feasibility() -> list[dict[str, object]]:
    """Feasibility counts for the 12 displayed canonical gate rows.

    Rows overlap. These counts must not be summed to count support pairs.
    """

    _, _, failures = _residual_failures()
    rows: list[dict[str, object]] = []
    for index, key in enumerate(tier.canonical_gate_keys(), 1):
        descriptor = tier._descriptor_with_key(key)
        listed = tier._gate_pairs(key, failures)
        feasible = frozenset(
            pair for pair in listed if descriptor_feasible(pair, descriptor)
        )
        infeasible = listed - feasible
        rows.append(
            {
                "gate": f"G{index}",
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "listed_pair_orbits": len(listed),
                "stoichiometrically_feasible": len(feasible),
                "stoichiometrically_infeasible": len(infeasible),
                "feasible_sha256": closure.pair_fingerprint(feasible),
                "infeasible_sha256": closure.pair_fingerprint(infeasible),
            }
        )
    return rows


def certificate() -> dict[str, object]:
    """Complete filter on every failing descriptor of all 2,511 pairs."""

    positive, signed, failures = _residual_failures()
    all_failing: list[tuple[Pair, tier.TierDescriptor]] = []
    feasible_incidences: list[tuple[Pair, tier.TierDescriptor]] = []
    by_active = Counter()
    feasible_by_active = Counter()
    feasible_count_histogram = Counter()
    pairs_with_feasible: set[Pair] = set()

    for pair in sorted(failures):
        pair_feasible = 0
        for descriptor in tier.tier_descriptors():
            if tier.universal_orientation_tier_condition(pair, descriptor):
                continue
            all_failing.append((pair, descriptor))
            active = sum(value > 0 for value in descriptor.weight)
            by_active[active] += 1
            if descriptor_feasible(pair, descriptor):
                feasible_incidences.append((pair, descriptor))
                feasible_by_active[active] += 1
                pair_feasible += 1
                pairs_with_feasible.add(pair)
        feasible_count_histogram[pair_feasible] += 1

    with_feasible = frozenset(pairs_with_feasible)
    without_feasible = failures - with_feasible
    positive_with = positive & with_feasible
    positive_without = positive - with_feasible
    signed_with = signed & with_feasible
    signed_without = signed - with_feasible

    zero_cap_positive = tier.zero_cap_axis_pairs(
        closure.POSITIVE_SHIELDED_MASKS
    )
    zero_cap_signed = tier.zero_cap_axis_pairs(closure.SIGNED_SHIELDED_MASKS)
    assert not (positive_without & zero_cap_positive)
    assert not (signed_without & zero_cap_signed)
    positive_after_ordered_branches = (
        positive - positive_without - zero_cap_positive
    )
    signed_after_ordered_branches = signed - signed_without - zero_cap_signed

    payload: dict[str, object] = {
        "claim_scope": (
            "exact affine-stoichiometric descriptor feasibility; "
            "feasibility is not recurrence or transience"
        ),
        "input_residual_pairs": len(failures),
        "input_positive_pairs": len(positive),
        "input_signed_pairs": len(signed),
        "failing_pair_descriptor_incidences": len(all_failing),
        "stoichiometrically_feasible_incidences": len(feasible_incidences),
        "stoichiometrically_infeasible_incidences": (
            len(all_failing) - len(feasible_incidences)
        ),
        "incidences_by_active_coordinate_count": {
            str(active): {
                "failing": by_active[active],
                "feasible": feasible_by_active[active],
                "infeasible": by_active[active] - feasible_by_active[active],
            }
            for active in (1, 2, 3)
        },
        "pairs_with_a_feasible_failing_descriptor": len(with_feasible),
        "pairs_without_a_feasible_failing_descriptor": len(without_feasible),
        "classwise_tier_foster_branch": {
            "input": len(failures),
            "certified": len(without_feasible),
            "remaining": len(with_feasible),
            "positive": {
                "input": len(positive),
                "certified": len(positive_without),
                "remaining": len(positive_with),
            },
            "signed": {
                "input": len(signed),
                "certified": len(signed_without),
                "remaining": len(signed_with),
            },
        },
        "positive": {
            "with_feasible_obstruction": len(positive_with),
            "without_feasible_obstruction": len(positive_without),
            "with_feasible_sha256": closure.pair_fingerprint(positive_with),
            "without_feasible_sha256": closure.pair_fingerprint(positive_without),
        },
        "signed": {
            "with_feasible_obstruction": len(signed_with),
            "without_feasible_obstruction": len(signed_without),
            "with_feasible_sha256": closure.pair_fingerprint(signed_with),
            "without_feasible_sha256": closure.pair_fingerprint(signed_without),
        },
        "with_feasible_sha256": closure.pair_fingerprint(with_feasible),
        "without_feasible_sha256": closure.pair_fingerprint(without_feasible),
        "feasible_incidence_sha256": _incidence_fingerprint(feasible_incidences),
        "feasible_descriptor_count_histogram": {
            str(count): feasible_count_histogram[count]
            for count in sorted(feasible_count_histogram)
        },
        "canonical_gate_rows": canonical_gate_feasibility(),
        "ordered_affine_then_zero_cap_support_table": {
            "claim_scope": (
                "exact disjoint support counts; the second branch requires "
                "the separate zero-cap physical-time theorem"
            ),
            "affine_infeasible": len(without_feasible),
            "zero_cap_axis_after_affine": (
                len(zero_cap_positive) + len(zero_cap_signed)
            ),
            "overlap": (
                len(positive_without & zero_cap_positive)
                + len(signed_without & zero_cap_signed)
            ),
            "remaining": (
                len(positive_after_ordered_branches)
                + len(signed_after_ordered_branches)
            ),
            "positive": {
                "input": len(positive),
                "affine_infeasible": len(positive_without),
                "zero_cap_axis_after_affine": len(zero_cap_positive),
                "overlap": len(positive_without & zero_cap_positive),
                "remaining": len(positive_after_ordered_branches),
                "closed_union_sha256": closure.pair_fingerprint(
                    positive_without | zero_cap_positive
                ),
                "remaining_sha256": closure.pair_fingerprint(
                    positive_after_ordered_branches
                ),
            },
            "signed": {
                "input": len(signed),
                "affine_infeasible": len(signed_without),
                "zero_cap_axis_after_affine": len(zero_cap_signed),
                "overlap": len(signed_without & zero_cap_signed),
                "remaining": len(signed_after_ordered_branches),
                "closed_union_sha256": closure.pair_fingerprint(
                    signed_without | zero_cap_signed
                ),
                "remaining_sha256": closure.pair_fingerprint(
                    signed_after_ordered_branches
                ),
            },
        },
    }
    digest = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = sha256(digest).hexdigest()
    return payload


def self_test() -> None:
    result = certificate()
    assert result["input_residual_pairs"] == 2511
    assert result["failing_pair_descriptor_incidences"] == 12886
    assert result["stoichiometrically_feasible_incidences"] == 9913
    assert result["pairs_with_a_feasible_failing_descriptor"] == 2360
    assert result["pairs_without_a_feasible_failing_descriptor"] == 151
    assert result["classwise_tier_foster_branch"] == {
        "input": 2511,
        "certified": 151,
        "remaining": 2360,
        "positive": {"input": 2312, "certified": 143, "remaining": 2169},
        "signed": {"input": 199, "certified": 8, "remaining": 191},
    }
    assert result["ordered_affine_then_zero_cap_support_table"]["overlap"] == 0
    assert result["ordered_affine_then_zero_cap_support_table"]["remaining"] == 1613


if __name__ == "__main__":
    self_test()
    print(json.dumps(certificate(), indent=2, sort_keys=True))
