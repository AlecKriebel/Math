#!/usr/bin/env python3
"""Primitive-eighth-root arithmetic for the ``BS(84,83)`` lane.

The base-sequence norm identity evaluated at ``z = exp(pi*i/4)`` splits over
``Q(sqrt(2))``.  For a sign sequence ``X``, let ``c_r`` be its sum on indices
congruent to ``r`` modulo eight and put

    x = c_0-c_4,  y = c_2-c_6,  alpha = c_1-c_5,  beta = c_3-c_7.

Then

    |X(z)|^2
      = x^2+y^2+alpha^2+beta^2
        + sqrt(2) * (alpha*(x+y) + beta*(y-x)).

This module checks the resulting exact invariant, the distance-33 root shell,
and the sharp distance-34 lower bound after the exact ordinary/alternating
margin norms are imposed.  It uses only the Python standard library.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from seed import ELIAHOU_Q, ELIAHOU_S, validate_sign_sequence
from variable_q_base import LONG, SHORT, special_to_base


ENERGY = 2 * (LONG + SHORT)
ROOT8_GROUPS = (
    ((0, 1), (4, -1)),
    ((2, 1), (6, -1)),
    ((1, 1), (5, -1)),
    ((3, 1), (7, -1)),
)

# This target lies on both exact primitive-eighth-root equations and is at
# distance 33 from the seed.  It proves that the distance lower bound supplied
# by the rational sphere equation alone is sharp even after the irrational
# coefficient is imposed.
TIGHT_ROOT8_TARGET = (
    (7, -7, 7, -1),
    (5, -5, 5, 1),
    (-7, 5, 1, 0),
    (-5, 3, 1, 0),
)

# A raw distance-34 witness satisfying the complete primitive-eight
# equations, both exact margin norms, and every mandatory endpoint-quad
# product.  It is deliberately nonexact at the full correlation layer.
MARGIN_QUAD_WITNESS_FLIPS = (
    (21, 22, 29, 30, 32, 33, 37, 40, 44, 45, 48, 49, 57),
    (21, 26, 29, 32, 34, 37, 39, 40, 45, 48, 50, 53, 61),
    (36, 42, 50, 58),
    (24, 32, 40, 46),
)


@dataclass(frozen=True)
class Root8Report:
    rational: int
    irrational: int

    @property
    def exact(self) -> bool:
        return self.rational == ENERGY and self.irrational == 0


def residue_sign_sums(sequence: Sequence[int], modulus: int = 8) -> tuple[int, ...]:
    validate_sign_sequence(sequence)
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    return tuple(
        sum(sequence[index] for index in range(residue, len(sequence), modulus))
        for residue in range(modulus)
    )


def root8_coordinates(sequence: Sequence[int]) -> tuple[int, int, int, int]:
    """Return ``(x,y,alpha,beta)`` in the primitive-eight decomposition."""

    compressed = residue_sign_sums(sequence)
    return (
        compressed[0] - compressed[4],
        compressed[2] - compressed[6],
        compressed[1] - compressed[5],
        compressed[3] - compressed[7],
    )


def root8_energy_pair(
    coordinates: Sequence[int],
) -> tuple[int, int]:
    """Return the rational and ``sqrt(2)`` coefficients of the squared norm."""

    if len(coordinates) != 4:
        raise ValueError("four primitive-eight coordinates are required")
    x, y, alpha, beta = coordinates
    rational = x * x + y * y + alpha * alpha + beta * beta
    irrational = alpha * (x + y) + beta * (y - x)
    return rational, irrational


def root8_report(sequences: Sequence[Sequence[int]]) -> Root8Report:
    if len(sequences) != 4:
        raise ValueError("four base sequences are required")
    pairs = tuple(root8_energy_pair(root8_coordinates(sequence)) for sequence in sequences)
    return Root8Report(
        rational=sum(pair[0] for pair in pairs),
        irrational=sum(pair[1] for pair in pairs),
    )


def coordinate_group_sizes(length: int) -> tuple[int, int, int, int]:
    """Return the number of signs contributing to each root-eight coordinate."""

    if length <= 0:
        raise ValueError("length must be positive")
    return tuple(
        sum(len(range(residue, length, 8)) for residue, _ in group)
        for group in ROOT8_GROUPS
    )


def coordinate_distance(source: int, target: int, group_size: int) -> int:
    """Minimum sign flips changing one signed group sum to ``target``."""

    if abs(source) > group_size or source % 2 != group_size % 2:
        raise ValueError("source is not a signed sum for this group")
    if abs(target) > group_size or target % 2 != group_size % 2:
        raise ValueError("target is not a signed sum for this group")
    return abs(target - source) // 2


def minimum_seed_distance_to_rational_sphere(
    seed: Sequence[Sequence[int]] | None = None,
) -> tuple[int, tuple[int, ...]]:
    """Minimize raw Hamming distance subject only to rational energy 334.

    The dynamic program is an exhaustive enumeration of the sixteen bounded
    signed sums, retaining the cheapest prefix at each accumulated square
    energy.  Since the irrational root-eight equation is omitted, its optimum
    is a valid lower bound for every exact base sequence.
    """

    if seed is None:
        seed = special_to_base(ELIAHOU_S, ELIAHOU_Q)
    if tuple(map(len, seed)) != (LONG, LONG, SHORT, SHORT):
        raise ValueError("seed must have base lengths (84,84,83,83)")

    sources: list[int] = []
    bounds: list[int] = []
    for sequence in seed:
        sources.extend(root8_coordinates(sequence))
        bounds.extend(coordinate_group_sizes(len(sequence)))

    states: dict[int, tuple[int, tuple[int, ...]]] = {0: (0, ())}
    for source, bound in zip(sources, bounds, strict=True):
        next_states: dict[int, tuple[int, tuple[int, ...]]] = {}
        for used_energy, (used_distance, prefix) in states.items():
            for target in range(-bound, bound + 1, 2):
                energy = used_energy + target * target
                if energy > ENERGY:
                    continue
                distance = used_distance + coordinate_distance(
                    source, target, bound
                )
                incumbent = next_states.get(energy)
                if incumbent is None or distance < incumbent[0]:
                    next_states[energy] = (distance, prefix + (target,))
        states = next_states
    if ENERGY not in states:
        raise AssertionError("primitive-eight rational sphere is unexpectedly empty")
    return states[ENERGY]


def _root8_target_suffixes(
    sources: Sequence[int],
    bounds: Sequence[int],
    distance: int,
) -> tuple[frozenset[tuple[int, int]], ...]:
    """Return exact suffix ``(energy,cost)`` sets for target enumeration."""

    if len(sources) != len(bounds):
        raise ValueError("source and bound vectors must have equal length")
    suffixes: list[frozenset[tuple[int, int]]] = [
        frozenset() for _ in range(len(sources) + 1)
    ]
    suffixes[-1] = frozenset({(0, 0)})
    for index in range(len(sources) - 1, -1, -1):
        states: set[tuple[int, int]] = set()
        source = sources[index]
        bound = bounds[index]
        for target in range(-bound, bound + 1, 2):
            target_energy = target * target
            target_cost = coordinate_distance(source, target, bound)
            for suffix_energy, suffix_cost in suffixes[index + 1]:
                energy = target_energy + suffix_energy
                cost = target_cost + suffix_cost
                if energy <= ENERGY and cost <= distance:
                    states.add((energy, cost))
        suffixes[index] = frozenset(states)
    return tuple(suffixes)


def root8_targets_at_distance(
    seed: Sequence[Sequence[int]],
    distance: int,
) -> tuple[tuple[int, ...], ...]:
    """Enumerate every rational-sphere coordinate vector at exact distance."""

    if distance < 0:
        raise ValueError("distance must be nonnegative")
    sources: list[int] = []
    bounds: list[int] = []
    for sequence in seed:
        sources.extend(root8_coordinates(sequence))
        bounds.extend(coordinate_group_sizes(len(sequence)))
    suffixes = _root8_target_suffixes(sources, bounds, distance)
    result: list[tuple[int, ...]] = []

    def visit(
        index: int,
        energy: int,
        cost: int,
        prefix: tuple[int, ...],
    ) -> None:
        if (ENERGY - energy, distance - cost) not in suffixes[index]:
            return
        if index == len(sources):
            result.append(prefix)
            return
        source = sources[index]
        bound = bounds[index]
        for target in range(-bound, bound + 1, 2):
            visit(
                index + 1,
                energy + target * target,
                cost + coordinate_distance(source, target, bound),
                prefix + (target,),
            )

    visit(0, 0, 0, ())
    return tuple(result)


def _pair_sums_at_minimum(
    sequence: Sequence[int],
    group: Sequence[tuple[int, int]],
    target_difference: int,
) -> tuple[int, ...]:
    """Possible pair totals at minimum cost for one root-eight coordinate."""

    if len(group) != 2 or tuple(coefficient for _, coefficient in group) != (1, -1):
        raise ValueError("expected one positive and one negative residue class")
    first_residue, _ = group[0]
    second_residue, _ = group[1]
    first_size = len(sequence[first_residue::8])
    second_size = len(sequence[second_residue::8])
    first_source = sum(sequence[first_residue::8])
    second_source = sum(sequence[second_residue::8])
    source_difference = first_source - second_source
    minimum_cost = coordinate_distance(
        source_difference, target_difference, first_size + second_size
    )
    totals = set()
    for first in range(-first_size, first_size + 1, 2):
        for second in range(-second_size, second_size + 1, 2):
            if first - second != target_difference:
                continue
            cost = (
                abs(first - first_source) + abs(second - second_source)
            ) // 2
            if cost == minimum_cost:
                totals.add(first + second)
    return tuple(sorted(totals))


def minimum_cost_margin_pairs(
    sequence: Sequence[int],
    target_coordinates: Sequence[int],
) -> tuple[tuple[int, int], ...]:
    """Return all ``(ordinary,alternating)`` sums at minimum coordinate cost."""

    if len(target_coordinates) != 4:
        raise ValueError("four target coordinates are required")
    totals = tuple(
        _pair_sums_at_minimum(sequence, group, target)
        for group, target in zip(
            ROOT8_GROUPS, target_coordinates, strict=True
        )
    )
    even_totals = {
        first + second for first in totals[0] for second in totals[1]
    }
    odd_totals = {
        first + second for first in totals[2] for second in totals[3]
    }
    return tuple(
        sorted(
            {
                (even + odd, even - odd)
                for even in even_totals
                for odd in odd_totals
            }
        )
    )


def exact_margin_norms_possible(
    seed: Sequence[Sequence[int]],
    flat_target: Sequence[int],
) -> bool:
    """Whether a root target can also have both exact margin square norms."""

    if len(seed) != 4 or len(flat_target) != 16:
        raise ValueError("expected four sequences and sixteen coordinates")
    options = tuple(
        minimum_cost_margin_pairs(sequence, flat_target[4 * index : 4 * index + 4])
        for index, sequence in enumerate(seed)
    )
    left = {
        (
            first[0] * first[0] + second[0] * second[0],
            first[1] * first[1] + second[1] * second[1],
        )
        for first in options[0]
        for second in options[1]
    }
    return any(
        (
            ENERGY - third[0] * third[0] - fourth[0] * fourth[0],
            ENERGY - third[1] * third[1] - fourth[1] * fourth[1],
        )
        in left
        for third in options[2]
        for fourth in options[3]
    )


def root8_irrational_total(flat_target: Sequence[int]) -> int:
    if len(flat_target) != 16:
        raise ValueError("sixteen root-eight coordinates are required")
    return sum(
        root8_energy_pair(flat_target[4 * index : 4 * index + 4])[1]
        for index in range(4)
    )


def minimum_seed_distance_with_margins(
    seed: Sequence[Sequence[int]] | None = None,
) -> tuple[int, int, int]:
    """Prove the sharp distance 34 after root-eight and margin identities.

    Returns ``(distance, rational_shell_targets, full_root_targets)``.  The
    rational sphere has minimum 33, so excluding every distance-33 target
    satisfying the irrational equation and both margin norms proves a lower
    bound of 34.  The explicit witness below proves sharpness.
    """

    canonical_seed = special_to_base(ELIAHOU_S, ELIAHOU_Q)
    if seed is None:
        seed = canonical_seed
    elif tuple(tuple(sequence) for sequence in seed) != canonical_seed:
        raise ValueError(
            "the sharp distance-34 certificate is specific to Eliahou's seed"
        )
    rational_distance, _ = minimum_seed_distance_to_rational_sphere(seed)
    if rational_distance != 33:
        raise AssertionError(
            f"unexpected rational-sphere distance {rational_distance}"
        )
    targets = root8_targets_at_distance(seed, rational_distance)
    full_root_targets = tuple(
        target for target in targets if root8_irrational_total(target) == 0
    )
    if any(exact_margin_norms_possible(seed, target) for target in full_root_targets):
        raise AssertionError(
            "a distance-33 primitive-eight target unexpectedly meets both margins"
        )
    witness = margin_quad_witness(seed)
    if distance_between(seed, witness) != 34:
        raise AssertionError("margin witness does not establish sharpness at 34")
    return 34, len(targets), len(full_root_targets)


def distance_between(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]
) -> int:
    if len(left) != len(right):
        raise ValueError("sequence families have different sizes")
    return sum(
        first != second
        for left_sequence, right_sequence in zip(left, right, strict=True)
        for first, second in zip(left_sequence, right_sequence, strict=True)
    )


def retarget_coordinates(
    sequence: Sequence[int], target: Sequence[int]
) -> tuple[int, ...]:
    """Reach a feasible root-eight coordinate vector with minimum flips."""

    validate_sign_sequence(sequence)
    if len(target) != 4:
        raise ValueError("four target coordinates are required")
    result = list(sequence)
    source = root8_coordinates(sequence)
    bounds = coordinate_group_sizes(len(sequence))
    for coordinate, (current, desired, bound, group) in enumerate(
        zip(source, target, bounds, ROOT8_GROUPS, strict=True)
    ):
        flips_needed = coordinate_distance(current, desired, bound)
        direction = 1 if desired > current else -1
        if not flips_needed:
            continue
        eligible = []
        for residue, coefficient in group:
            for index in range(residue, len(sequence), 8):
                transformed_sign = coefficient * result[index]
                if transformed_sign == -direction:
                    eligible.append(index)
        if len(eligible) < flips_needed:
            raise AssertionError(
                f"coordinate {coordinate} lacks the required flip direction"
            )
        for index in eligible[:flips_needed]:
            result[index] *= -1
    actual = root8_coordinates(result)
    if actual != tuple(target):
        raise AssertionError(f"retargeting failed: expected {tuple(target)}, got {actual}")
    return tuple(result)


def tight_root8_witness(
    seed: Sequence[Sequence[int]] | None = None,
) -> tuple[tuple[int, ...], ...]:
    """Construct a distance-33 witness for the root-eight relaxation."""

    if seed is None:
        seed = special_to_base(ELIAHOU_S, ELIAHOU_Q)
    return tuple(
        retarget_coordinates(sequence, target)
        for sequence, target in zip(seed, TIGHT_ROOT8_TARGET, strict=True)
    )


def margin_quad_witness(
    seed: Sequence[Sequence[int]] | None = None,
) -> tuple[tuple[int, ...], ...]:
    """Return the distance-34 witness for roots, margins, and quad products."""

    if seed is None:
        seed = special_to_base(ELIAHOU_S, ELIAHOU_Q)
    if len(seed) != 4:
        raise ValueError("four seed sequences are required")
    result = []
    for sequence, flips in zip(seed, MARGIN_QUAD_WITNESS_FLIPS, strict=True):
        changed = list(sequence)
        if len(set(flips)) != len(flips):
            raise AssertionError("duplicate witness flip")
        for index in flips:
            if not 0 <= index < len(changed):
                raise AssertionError("witness flip is out of range")
            changed[index] *= -1
        result.append(tuple(changed))
    return tuple(result)


def verify() -> None:
    seed = special_to_base(ELIAHOU_S, ELIAHOU_Q)
    expected_coordinates = (
        (11, -11, 19, -1),
        (11, -11, 19, 1),
        (-9, 11, 1, 0),
        (-11, 9, 1, 0),
    )
    actual_coordinates = tuple(root8_coordinates(sequence) for sequence in seed)
    if actual_coordinates != expected_coordinates:
        raise AssertionError(
            f"unexpected seed coordinates {actual_coordinates}"
        )
    seed_report = root8_report(seed)
    if seed_report != Root8Report(rational=1614, irrational=0):
        raise AssertionError(f"unexpected seed report {seed_report}")

    # Holding s fixed holds A and C fixed.  Their partial squared norm is
    # 807+24*sqrt(2), already greater than the full target 334; the remaining
    # B,D norms are nonnegative.
    fixed_s_pairs = tuple(
        root8_energy_pair(actual_coordinates[index]) for index in (0, 2)
    )
    fixed_s_report = Root8Report(
        rational=sum(pair[0] for pair in fixed_s_pairs),
        irrational=sum(pair[1] for pair in fixed_s_pairs),
    )
    if fixed_s_report != Root8Report(rational=807, irrational=24):
        raise AssertionError(f"unexpected fixed-s report {fixed_s_report}")

    minimum_distance, _ = minimum_seed_distance_to_rational_sphere(seed)
    if minimum_distance != 33:
        raise AssertionError(
            f"unexpected primitive-eight distance bound {minimum_distance}"
        )
    witness = tight_root8_witness(seed)
    if distance_between(seed, witness) != 33:
        raise AssertionError("tight root-eight witness has the wrong distance")
    witness_coordinates = tuple(root8_coordinates(sequence) for sequence in witness)
    if witness_coordinates != TIGHT_ROOT8_TARGET:
        raise AssertionError("tight root-eight witness has the wrong coordinates")
    if root8_report(witness) != Root8Report(rational=ENERGY, irrational=0):
        raise AssertionError("tight root-eight witness misses the exact root equations")

    distance, rational_targets, full_root_targets = (
        minimum_seed_distance_with_margins(seed)
    )
    if (distance, rational_targets, full_root_targets) != (34, 1350, 66):
        raise AssertionError(
            "unexpected root-eight/margin enumeration "
            f"{(distance, rational_targets, full_root_targets)}"
        )
    margin_witness = margin_quad_witness(seed)
    if root8_report(margin_witness) != Root8Report(
        rational=ENERGY, irrational=0
    ):
        raise AssertionError("margin witness misses the root-eight equations")
    ordinary = tuple(sum(sequence) for sequence in margin_witness)
    alternating = tuple(
        sum(value if index % 2 == 0 else -value for index, value in enumerate(sequence))
        for sequence in margin_witness
    )
    if sum(value * value for value in ordinary) != ENERGY:
        raise AssertionError("margin witness misses the ordinary norm")
    if sum(value * value for value in alternating) != ENERGY:
        raise AssertionError("margin witness misses the alternating norm")
    from variable_q_base import base_correlations, base_quad_products

    if base_quad_products(*margin_witness) != base_quad_products(*seed):
        raise AssertionError("margin witness breaks an endpoint-quad product")
    if not any(base_correlations(*margin_witness)[1:]):
        raise AssertionError("relaxation witness must not be reported as exact")


if __name__ == "__main__":
    verify()
    print("seed_root8=1614")
    print("fixed_s_partial_root8=807+24*sqrt(2)>334")
    print("minimum_raw_base_distance_to_root8_sphere=33")
    print("distance33_rational_shell_targets=1350")
    print("distance33_full_root8_targets=66")
    print("minimum_raw_base_distance_with_exact_margins=34")
    print("PASS primitive-eighth-root obstruction and sharp margin distance bound")
