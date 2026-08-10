"""Exact tier-arrangement certificate for residual shielded/available pairs.

The ten bimolecular monomials define a rational line arrangement on the
nonnegative projective log simplex.  This module enumerates every face of
that arrangement, adds the exact capped availability data for bounded
coordinates, and checks the Anderson--Kim top-S descending-source condition
for arbitrary strongly connected orientations.

The finite enumeration certifies support geometry.  The mathematical facts
that make the enumeration complete, and the implication to physical-time
Foster recurrence, are proved in
``research_notes/global_atlas_interface_closure.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd, lcm
from typing import Iterable

import global_atlas_interface_closure as closure


Vector = tuple[int, int, int]
Partition = tuple[tuple[int, ...], ...]
Pair = closure.Pair

COMPLEXES = closure.COMPLEXES
NAMES = closure.NAMES


@dataclass(frozen=True)
class TierDescriptor:
    """One D-tier preorder and one exact eventual availability pattern."""

    partition: Partition
    active_mask: int
    caps: Vector
    weight: Vector


def _primitive_normal(vector: Vector) -> Vector:
    common = 0
    for entry in vector:
        common = gcd(common, abs(entry))
    reduced = tuple(entry // common for entry in vector)
    for entry in reduced:
        if entry:
            return tuple(-value for value in reduced) if entry < 0 else reduced
    raise ValueError("zero vector has no primitive normal")


def comparison_normals() -> tuple[Vector, ...]:
    """The 21 projectively distinct pairwise-comparison hyperplanes."""

    normals = {
        _primitive_normal(
            tuple(COMPLEXES[first][i] - COMPLEXES[second][i] for i in range(3))
        )
        for first, second in combinations(range(len(COMPLEXES)), 2)
    }
    return tuple(sorted(normals))


def _cross(first: tuple[Fraction, ...], second: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return (
        first[1] * second[2] - first[2] * second[1],
        first[2] * second[0] - first[0] * second[2],
        first[0] * second[1] - first[1] * second[0],
    )


def _simplex_intersection(
    first: tuple[Fraction, ...],
    second: tuple[Fraction, ...],
) -> tuple[Fraction, Fraction, Fraction] | None:
    """Intersect two homogeneous planes with w_A+w_B+w_C=1."""

    direction = _cross(first, second)
    total = sum(direction)
    if not total:
        return None
    return tuple(entry / total for entry in direction)


@lru_cache(maxsize=1)
def simplex_vertices() -> frozenset[tuple[Fraction, Fraction, Fraction]]:
    """All vertices of the comparison arrangement on the closed simplex."""

    normals = [tuple(map(Fraction, item)) for item in comparison_normals()]
    normals.extend(
        (
            (Fraction(1), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(1)),
        )
    )
    vertices = {
        point
        for first, second in combinations(normals, 2)
        if (point := _simplex_intersection(first, second)) is not None
        and min(point) >= 0
    }
    return frozenset(vertices)


@lru_cache(maxsize=1)
def arrangement_candidates() -> frozenset[tuple[Fraction, Fraction, Fraction]]:
    """Represent every 0-, 1-, and 2-dimensional arrangement face.

    Vertices represent zero-dimensional faces; pair midpoints represent all
    open edge cells; centroids of triples include an interior point of every
    two-dimensional polygonal cell.  Extra points are harmless and are
    removed after passing to tier types.
    """

    vertices = simplex_vertices()
    candidates = set(vertices)
    for size in (2, 3):
        for selected in combinations(vertices, size):
            candidates.add(
                tuple(sum(point[i] for point in selected) / size for i in range(3))
            )
    return frozenset(candidates)


def _primitive_weight(weight: tuple[Fraction, Fraction, Fraction]) -> Vector:
    denominator = 1
    for entry in weight:
        denominator = lcm(denominator, entry.denominator)
    integers = [int(entry * denominator) for entry in weight]
    common = 0
    for entry in integers:
        common = gcd(common, abs(entry))
    return tuple(entry // common for entry in integers)


def _partition(weight: tuple[Fraction, Fraction, Fraction]) -> Partition:
    values = tuple(
        sum(Fraction(complex_vector[i]) * weight[i] for i in range(3))
        for complex_vector in COMPLEXES
    )
    return tuple(
        tuple(index for index, value in enumerate(values) if value == level)
        for level in sorted(set(values), reverse=True)
    )


@lru_cache(maxsize=1)
def tier_types() -> dict[tuple[Partition, int], Vector]:
    """All 193 nontrivial D-tier/active-coordinate types.

    For each type retain a simple primitive integral representative of its
    arrangement face.
    """

    result: dict[tuple[Partition, int], Vector] = {}
    for candidate in arrangement_candidates():
        if not any(candidate):
            continue
        active_mask = sum(1 << i for i, entry in enumerate(candidate) if entry > 0)
        key = _partition(candidate), active_mask
        weight = _primitive_weight(candidate)
        old = result.get(key)
        if old is None or (max(weight), sum(weight), weight) < (
            max(old),
            sum(old),
            old,
        ):
            result[key] = weight
    return result


@lru_cache(maxsize=1)
def tier_descriptors() -> tuple[TierDescriptor, ...]:
    """All 259 tier types after exact bounded-coordinate availability."""

    descriptors: list[TierDescriptor] = []
    for (partition, active_mask), weight in tier_types().items():
        inactive = tuple(i for i in range(3) if not (active_mask >> i & 1))
        for bounded_caps in product((0, 1, 2), repeat=len(inactive)):
            caps = [2, 2, 2]
            for coordinate, cap in zip(inactive, bounded_caps):
                caps[coordinate] = cap
            descriptors.append(
                TierDescriptor(partition, active_mask, tuple(caps), weight)
            )
    descriptors.sort(key=descriptor_sort_key)
    return tuple(descriptors)


def descriptor_sort_key(descriptor: TierDescriptor) -> tuple[object, ...]:
    weight = descriptor.weight
    return (
        sum(entry > 0 for entry in weight),
        max(weight),
        sum(weight),
        sum(descriptor.caps),
        weight,
        descriptor.caps,
        descriptor.partition,
    )


def _nodes(mask: int) -> frozenset[int]:
    return frozenset(index for index in range(len(NAMES)) if mask >> index & 1)


def _enabled(index: int, caps: Vector) -> bool:
    return all(caps[i] >= COMPLEXES[index][i] for i in range(3))


def tier_sets(pair: Pair, descriptor: TierDescriptor) -> tuple[frozenset[int], frozenset[int]]:
    """Return the network-restricted top D-tier and top finite S-tier."""

    linkage_nodes = tuple(_nodes(mask) for mask in pair)
    network_nodes = linkage_nodes[0] | linkage_nodes[1]
    top_d = next(
        frozenset(block) & network_nodes
        for block in descriptor.partition
        if frozenset(block) & network_nodes
    )
    top_s = next(
        (
            frozenset(index for index in block if index in network_nodes and _enabled(index, descriptor.caps))
            for block in descriptor.partition
            if any(index in network_nodes and _enabled(index, descriptor.caps) for index in block)
        ),
        frozenset(),
    )
    return top_d, top_s


def universal_orientation_tier_condition(pair: Pair, descriptor: TierDescriptor) -> bool:
    """Whether every strong orientation has a top-S descending source.

    For a linkage L, strong connectivity forces an edge out of a nonempty
    proper top-D subset.  It forces the source of that edge to be top-S for
    every orientation exactly when every node in that subset is top-S.
    """

    top_d, top_s = tier_sets(pair, descriptor)
    for mask in pair:
        nodes = _nodes(mask)
        top_in_linkage = nodes & top_d
        if top_in_linkage and top_in_linkage != nodes and top_in_linkage <= top_s:
            return True
    return False


def obstruction_cycles(
    pair: Pair,
    descriptor: TierDescriptor,
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    """Construct strong orientations witnessing failure of the tier test.

    Each linkage is oriented as one directed Hamiltonian cycle.  When its
    global-top subset is nonempty and proper, its sole exiting edge is placed
    at a top-D vertex outside the top S-tier.
    """

    if universal_orientation_tier_condition(pair, descriptor):
        raise ValueError("descriptor forces a top-S descending source")
    top_d, top_s = tier_sets(pair, descriptor)
    result: list[tuple[tuple[int, int], ...]] = []
    for mask in pair:
        nodes = _nodes(mask)
        top_in_linkage = nodes & top_d
        if top_in_linkage and top_in_linkage != nodes:
            bad = min(top_in_linkage - top_s)
            order = (
                tuple(sorted(top_in_linkage - {bad}))
                + (bad,)
                + tuple(sorted(nodes - top_in_linkage))
            )
        else:
            order = tuple(sorted(nodes))
        result.append(
            tuple(
                (order[index], order[(index + 1) % len(order)])
                for index in range(len(order))
            )
        )
    return result[0], result[1]


def has_top_s_descending_source(
    pair: Pair,
    descriptor: TierDescriptor,
    orientations: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
) -> bool:
    """Directly check the Anderson--Kim source condition on given edges."""

    top_d, top_s = tier_sets(pair, descriptor)
    return any(
        source in top_s and source in top_d and target not in top_d
        for edges in orientations
        for source, target in edges
    )


@lru_cache(maxsize=None)
def obstruction(pair: Pair) -> TierDescriptor | None:
    return next(
        (
            descriptor
            for descriptor in tier_descriptors()
            if not universal_orientation_tier_condition(pair, descriptor)
        ),
        None,
    )


def tier_split(shielded_masks: frozenset[int]) -> tuple[frozenset[Pair], frozenset[Pair]]:
    passed: set[Pair] = set()
    failed: set[Pair] = set()
    for pair in closure.residual_pairs(shielded_masks):
        (passed if obstruction(pair) is None else failed).add(pair)
    return frozenset(passed), frozenset(failed)


def descriptor_payload(descriptor: TierDescriptor) -> dict[str, object]:
    return {
        "weight": list(descriptor.weight),
        "caps": list(descriptor.caps),
        "tiers": [
            [NAMES[index] for index in block]
            for block in descriptor.partition
        ],
    }


def greedy_obstruction_cover(pairs: frozenset[Pair]) -> tuple[tuple[TierDescriptor, int], ...]:
    """A deterministic small descriptor cover of all non-universal pairs."""

    descriptors = tier_descriptors()
    coverage = tuple(
        frozenset(
            pair
            for pair in pairs
            if not universal_orientation_tier_condition(pair, descriptor)
        )
        for descriptor in descriptors
    )
    uncovered = set(pairs)
    result: list[tuple[TierDescriptor, int]] = []
    while uncovered:
        best = max(
            range(len(descriptors)),
            key=lambda index: (
                len(uncovered & coverage[index]),
                tuple(
                    -int(value)
                    for value in descriptor_sort_key(descriptors[index])[:4]
                ),
                -index,
            ),
        )
        newly_covered = uncovered & coverage[best]
        if not newly_covered:
            raise AssertionError("descriptor family failed to cover an obstruction")
        result.append((descriptors[best], len(newly_covered)))
        uncovered.difference_update(newly_covered)
    return tuple(result)


def _descriptor_swap_key(descriptor: TierDescriptor) -> tuple[Vector, Vector]:
    weight = descriptor.weight
    caps = descriptor.caps
    original = weight, caps
    swapped = (weight[1], weight[0], weight[2]), (caps[1], caps[0], caps[2])
    return min(original, swapped)


def split_certificate(label: str, shielded_masks: frozenset[int]) -> dict[str, object]:
    passed, failed = tier_split(shielded_masks)
    cover = greedy_obstruction_cover(failed)
    by_shielded_support = [
        {
            "shielded": list(closure.support(shielded)),
            "input": sum(pair[0] == shielded for pair in passed | failed),
            "universally_tier_certified": sum(
                pair[0] == shielded for pair in passed
            ),
            "remaining": sum(pair[0] == shielded for pair in failed),
        }
        for shielded in sorted(
            shielded_masks,
            key=lambda value: (len(closure.support(value)), closure.support(value)),
        )
        if any(pair[0] == shielded for pair in passed | failed)
    ]
    return {
        "label": label,
        "input_residual_pairs": len(passed) + len(failed),
        "universally_tier_certified": len(passed),
        "not_universally_tier_certified": len(failed),
        "certified_modulo_A_B_exchange": len(
            {closure.pair_orbit_key(pair) for pair in passed}
        ),
        "remaining_modulo_A_B_exchange": len(
            {closure.pair_orbit_key(pair) for pair in failed}
        ),
        "certified_sha256": closure.pair_fingerprint(passed),
        "remaining_sha256": closure.pair_fingerprint(failed),
        "greedy_obstruction_descriptors": len(cover),
        "greedy_obstruction_descriptors_modulo_A_B_exchange": len(
            {_descriptor_swap_key(descriptor) for descriptor, _ in cover}
        ),
        "by_shielded_support": by_shielded_support,
        "greedy_cover": [
            {
                "new_pairs": count,
                **descriptor_payload(descriptor),
            }
            for descriptor, count in cover
        ],
    }


def signed_service_superset_certificate() -> dict[str, object]:
    """Describe unresolved signed pairs adjacent to the exact pure-C seam.

    The exact signed-service theorem is not monotone under adding complexes.
    This records, without making such an inference, the strict supersets of
    ``{C,2C}`` that remain after the global tier test.
    """

    _, failed = tier_split(closure.SIGNED_SHIELDED_MASKS)
    pure_c = closure.mask(("C", "2C"))
    adjacent = frozenset(pair for pair in failed if pair[1] & pure_c == pure_c)
    minimal: list[Pair] = []
    for shielded in closure.SIGNED_SHIELDED_MASKS:
        available = {pair[1] for pair in adjacent if pair[0] == shielded}
        minimal.extend(
            (shielded, candidate)
            for candidate in available
            if not any(
                smaller != candidate and smaller & candidate == smaller
                for smaller in available
            )
        )
    minimal.sort(
        key=lambda pair: (
            len(closure.support(pair[0])),
            closure.support(pair[0]),
            len(closure.support(pair[1])),
            closure.support(pair[1]),
        )
    )
    return {
        "remaining_signed_pairs_containing_C_2C": len(adjacent),
        "of_which_contain_0_C_2C": sum(
            {"0", "C", "2C"}.issubset(closure.support(pair[1]))
            for pair in adjacent
        ),
        "remaining_signed_pairs_without_C_2C": len(failed - adjacent),
        "inclusion_minimal_pair_count": len(minimal),
        "inclusion_minimal_pairs": [
            {
                "shielded": list(closure.support(pair[0])),
                "available": list(closure.support(pair[1])),
            }
            for pair in minimal
        ],
        "adjacent_sha256": closure.pair_fingerprint(adjacent),
    }


def _swap_pair(pair: Pair) -> Pair:
    return closure.swap_ab_mask(pair[0]), closure.swap_ab_mask(pair[1])


def _descriptor_key(descriptor: TierDescriptor) -> tuple[Vector, Vector]:
    return descriptor.weight, descriptor.caps


@lru_cache(maxsize=1)
def canonical_gate_keys() -> tuple[tuple[Vector, Vector], ...]:
    """The 12 obstruction descriptors after the external A/B quotient."""

    positive_failed = tier_split(closure.POSITIVE_SHIELDED_MASKS)[1]
    signed_failed = tier_split(closure.SIGNED_SHIELDED_MASKS)[1]
    covers = (
        greedy_obstruction_cover(positive_failed)
        + greedy_obstruction_cover(signed_failed)
    )
    return tuple(
        sorted({_descriptor_swap_key(descriptor) for descriptor, _ in covers})
    )


def _descriptor_with_key(key: tuple[Vector, Vector]) -> TierDescriptor:
    return next(
        descriptor
        for descriptor in tier_descriptors()
        if _descriptor_key(descriptor) == key
    )


def _gate_pairs(
    key: tuple[Vector, Vector],
    failures: frozenset[Pair],
) -> frozenset[Pair]:
    """Map all failures for a descriptor orbit to its canonical orientation."""

    descriptor = _descriptor_with_key(key)
    swapped_key = (
        (key[0][1], key[0][0], key[0][2]),
        (key[1][1], key[1][0], key[1][2]),
    )
    swapped_descriptor = _descriptor_with_key(swapped_key)
    symmetric = swapped_key == key
    pairs: set[Pair] = set()
    for pair in failures:
        if not universal_orientation_tier_condition(pair, descriptor):
            pairs.add(min(pair, _swap_pair(pair)) if symmetric else pair)
        if not symmetric and not universal_orientation_tier_condition(
            pair, swapped_descriptor
        ):
            pairs.add(_swap_pair(pair))
    return frozenset(pairs)


def _gate_mode(pair: Pair, descriptor: TierDescriptor) -> str:
    top_d, _ = tier_sets(pair, descriptor)
    has_proper_top_subset = any(
        (top_in_linkage := _nodes(mask) & top_d)
        and top_in_linkage != _nodes(mask)
        for mask in pair
    )
    return "disabled_source_promotion" if has_proper_top_subset else "flat_top_linkage"


def _minimum_pair_payload(pairs: set[Pair]) -> dict[str, object] | None:
    if not pairs:
        return None
    minimum_size = min(
        pair[0].bit_count() + pair[1].bit_count() for pair in pairs
    )
    pair = min(
        (
            candidate
            for candidate in pairs
            if candidate[0].bit_count() + candidate[1].bit_count() == minimum_size
        ),
        key=lambda candidate: closure.pair_payload(candidate),
    )
    return {
        "total_complexes": minimum_size,
        "shielded": list(closure.support(pair[0])),
        "available": list(closure.support(pair[1])),
    }


def _active_coordinates(descriptor: TierDescriptor) -> tuple[int, ...]:
    return tuple(
        coordinate
        for coordinate, value in enumerate(descriptor.weight)
        if value
    )


def _flat_axis_is_exact_invariant(
    pair: Pair,
    descriptor: TierDescriptor,
) -> bool:
    """Verify the support-level invariant behind a flat one-axis gate.

    On a one-active descriptor the network top D-tier consists of the
    complexes with one copy of the active species (a dimer would instead
    force a descending top-S source).  If neither linkage has a nonempty
    proper intersection with that tier, every linkage lies wholly inside or
    wholly outside it.  The active stoichiometric coordinate is therefore
    constant on each linkage and hence is an exact reaction invariant.
    """

    active = _active_coordinates(descriptor)
    if len(active) != 1 or _gate_mode(pair, descriptor) != "flat_top_linkage":
        return False
    coordinate = active[0]
    for linkage in pair:
        values = {COMPLEXES[node][coordinate] for node in _nodes(linkage)}
        if len(values) != 1:
            return False
    return True


def one_active_interface_certificate() -> dict[str, object]:
    """Exact scope of the one-active structural reduction.

    This certificate deliberately records three different claims.

    * A flat one-axis obstruction is removed rigorously when that axis is an
      exact invariant and all other descriptors pass.
    * A promotion obstruction has the universal top support
      ``I, I+A, I+C`` after removing the active molecule ``I``; no active
      dimer can occur in such a failure.
    * Clearing an actual top target is only a local episode.  The finite
      support check does not promote the remaining one-axis pairs to a
      recurrence theorem because a lower-layer reaction can destroy the
      carried cofactor without changing the active coordinate.
    """

    descriptors = tier_descriptors()
    one_active = tuple(
        descriptor
        for descriptor in descriptors
        if len(_active_coordinates(descriptor)) == 1
    )
    multi_active = tuple(
        descriptor
        for descriptor in descriptors
        if len(_active_coordinates(descriptor)) >= 2
    )
    assert len(one_active) == 27

    result: dict[str, object] = {
        "claim_scope": (
            "67 classwise invariant closures plus exact one-active gate "
            "counts; target clearance alone is not recurrence"
        ),
        "one_active_descriptors": len(one_active),
        "families": {},
    }
    for label, masks in (
        ("positive", closure.POSITIVE_SHIELDED_MASKS),
        ("signed", closure.SIGNED_SHIELDED_MASKS),
    ):
        failed = tier_split(masks)[1]
        obstruction_map = {
            pair: tuple(
                descriptor
                for descriptor in descriptors
                if not universal_orientation_tier_condition(pair, descriptor)
            )
            for pair in failed
        }
        any_one = frozenset(
            pair
            for pair, obstructions in obstruction_map.items()
            if any(descriptor in one_active for descriptor in obstructions)
        )
        only_one = frozenset(
            pair
            for pair, obstructions in obstruction_map.items()
            if obstructions
            and all(descriptor in one_active for descriptor in obstructions)
        )
        invariant_closed = frozenset(
            pair
            for pair, obstructions in obstruction_map.items()
            if obstructions
            and all(
                descriptor in one_active
                and _flat_axis_is_exact_invariant(pair, descriptor)
                for descriptor in obstructions
            )
        )

        axes: list[dict[str, object]] = []
        for coordinate, species in enumerate(("A", "B", "C")):
            axis_descriptors = tuple(
                descriptor
                for descriptor in one_active
                if descriptor.weight[coordinate]
            )
            axis_pairs = frozenset(
                pair
                for pair in failed
                if any(
                    not universal_orientation_tier_condition(pair, descriptor)
                    for descriptor in axis_descriptors
                )
            )
            representative = axis_descriptors[0]
            by_mode = {
                mode: frozenset(
                    pair
                    for pair in axis_pairs
                    if _gate_mode(pair, representative) == mode
                )
                for mode in ("disabled_source_promotion", "flat_top_linkage")
            }

            active_dimer = next(
                node
                for node, vector in enumerate(COMPLEXES)
                if vector[coordinate] == 2
            )
            top_menu = frozenset(
                node
                for node, vector in enumerate(COMPLEXES)
                if vector[coordinate] == 1
            )
            for pair in axis_pairs:
                network = _nodes(pair[0]) | _nodes(pair[1])
                assert active_dimer not in network
                top_d, _ = tier_sets(pair, representative)
                if network & top_menu:
                    assert top_d <= top_menu
                else:
                    assert _gate_mode(pair, representative) == "flat_top_linkage"
            for pair in by_mode["flat_top_linkage"]:
                assert _flat_axis_is_exact_invariant(pair, representative)

            axes.append(
                {
                    "active_species": species,
                    "descriptors": len(axis_descriptors),
                    "pairs_with_an_axis_obstruction": len(axis_pairs),
                    "disabled_source_promotion": len(
                        by_mode["disabled_source_promotion"]
                    ),
                    "flat_top_linkage": len(by_mode["flat_top_linkage"]),
                    "factored_top_complexes": [
                        NAMES[node] for node in sorted(top_menu)
                    ],
                }
            )

        remaining = failed - invariant_closed
        result["families"][label] = {
            "tier_failures_before_one_active_invariant": len(failed),
            "pairs_with_any_one_active_obstruction": len(any_one),
            "pairs_with_only_one_active_obstructions": len(only_one),
            "classwise_invariant_closures": len(invariant_closed),
            "remaining_after_classwise_invariant": len(remaining),
            "remaining_with_only_one_active_obstructions": len(
                only_one - invariant_closed
            ),
            "still_has_a_multi_active_obstruction": sum(
                any(descriptor in multi_active for descriptor in obstructions)
                for pair, obstructions in obstruction_map.items()
                if pair in remaining
            ),
            "invariant_closed_sha256": closure.pair_fingerprint(invariant_closed),
            "remaining_sha256": closure.pair_fingerprint(remaining),
            "axes": axes,
        }

    return result


ZERO_CAP_AXIS_KEYS = frozenset(
    {
        ((1, 0, 0), (2, 0, 0)),
        ((0, 1, 0), (0, 2, 0)),
        ((0, 0, 1), (0, 0, 2)),
    }
)


def zero_cap_axis_pairs(shielded_masks: frozenset[int]) -> frozenset[Pair]:
    """Pairs whose complete obstruction set consists of zero-cap axes.

    This is an exact support selector.  Its stochastic implication belongs
    to the separate physical-time zero-cap theorem; the selector itself does
    not assert recurrence.
    """

    failed = tier_split(shielded_masks)[1]
    return frozenset(
        pair
        for pair in failed
        if (
            obstruction_keys := {
                _descriptor_key(descriptor)
                for descriptor in tier_descriptors()
                if not universal_orientation_tier_condition(pair, descriptor)
            }
        )
        and obstruction_keys <= ZERO_CAP_AXIS_KEYS
    )


def zero_cap_axis_certificate() -> dict[str, object]:
    positive = zero_cap_axis_pairs(closure.POSITIVE_SHIELDED_MASKS)
    signed = zero_cap_axis_pairs(closure.SIGNED_SHIELDED_MASKS)
    invariant = one_active_interface_certificate()["families"]
    positive_invariant_sha = invariant["positive"]["invariant_closed_sha256"]
    signed_invariant_sha = invariant["signed"]["invariant_closed_sha256"]

    # Reconstruct the invariant-only sets from their defining predicate so
    # that disjointness is checked as a set statement, not by hashes.
    descriptors = tier_descriptors()
    invariant_sets: dict[str, frozenset[Pair]] = {}
    for label, masks in (
        ("positive", closure.POSITIVE_SHIELDED_MASKS),
        ("signed", closure.SIGNED_SHIELDED_MASKS),
    ):
        failed = tier_split(masks)[1]
        invariant_sets[label] = frozenset(
            pair
            for pair in failed
            if (
                obstructions := tuple(
                    descriptor
                    for descriptor in descriptors
                    if not universal_orientation_tier_condition(pair, descriptor)
                )
            )
            and all(
                len(_active_coordinates(descriptor)) == 1
                and _flat_axis_is_exact_invariant(pair, descriptor)
                for descriptor in obstructions
            )
        )
    assert closure.pair_fingerprint(invariant_sets["positive"]) == positive_invariant_sha
    assert closure.pair_fingerprint(invariant_sets["signed"]) == signed_invariant_sha
    assert not (positive & invariant_sets["positive"])
    assert not (signed & invariant_sets["signed"])

    return {
        "claim_scope": (
            "exact zero-cap-axis support selector; physical-time recurrence "
            "is supplied only by the accompanying analytic theorem"
        ),
        "allowed_obstruction_keys": [
            {"weight": list(weight), "caps": list(caps)}
            for weight, caps in sorted(ZERO_CAP_AXIS_KEYS)
        ],
        "positive": {
            "selected": len(positive),
            "sha256": closure.pair_fingerprint(positive),
            "disjoint_from_flat_axis_invariant_set": not bool(
                positive & invariant_sets["positive"]
            ),
        },
        "signed": {
            "selected": len(signed),
            "sha256": closure.pair_fingerprint(signed),
            "disjoint_from_flat_axis_invariant_set": not bool(
                signed & invariant_sets["signed"]
            ),
        },
    }


def analytic_gate_certificate() -> dict[str, object]:
    """Canonical finite library of the remaining tier-obstruction geometry."""

    positive_failed = tier_split(closure.POSITIVE_SHIELDED_MASKS)[1]
    signed_failed = tier_split(closure.SIGNED_SHIELDED_MASKS)[1]
    failures = positive_failed | signed_failed
    keys = canonical_gate_keys()
    assert len(keys) == 12

    covered: set[Pair] = set()
    gates: list[dict[str, object]] = []
    for index, key in enumerate(keys, 1):
        descriptor = _descriptor_with_key(key)
        pairs = _gate_pairs(key, failures)
        covered.update(
            pair
            for pair in failures
            if not universal_orientation_tier_condition(pair, descriptor)
        )
        swapped_key = (
            (key[0][1], key[0][0], key[0][2]),
            (key[1][1], key[1][0], key[1][2]),
        )
        if swapped_key != key:
            swapped_descriptor = _descriptor_with_key(swapped_key)
            covered.update(
                pair
                for pair in failures
                if not universal_orientation_tier_condition(pair, swapped_descriptor)
            )

        by_mode = {
            mode: {
                pair for pair in pairs if _gate_mode(pair, descriptor) == mode
            }
            for mode in ("disabled_source_promotion", "flat_top_linkage")
        }
        enabled_menu = [
            [NAMES[complex_index] for complex_index in block if _enabled(complex_index, descriptor.caps)]
            for block in descriptor.partition
        ]
        enabled_menu = [block for block in enabled_menu if block]
        gates.append(
            {
                "gate": f"G{index}",
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "active_coordinates": [
                    name
                    for name, value in zip(("A", "B", "C"), descriptor.weight)
                    if value
                ],
                "bounded_coordinates": {
                    name: descriptor.caps[coordinate]
                    for coordinate, name in enumerate(("A", "B", "C"))
                    if not descriptor.weight[coordinate]
                },
                "enabled_source_tier_menu": enabled_menu,
                "disabled_complexes": [
                    NAMES[complex_index]
                    for complex_index in range(len(NAMES))
                    if not _enabled(complex_index, descriptor.caps)
                ],
                "covered_pair_orbits": len(pairs),
                "mechanisms": {
                    mode: len(mode_pairs) for mode, mode_pairs in by_mode.items()
                },
                "canonical_minimum_pairs": {
                    mode: _minimum_pair_payload(mode_pairs)
                    for mode, mode_pairs in by_mode.items()
                    if mode_pairs
                },
            }
        )

    handled_exact_pairs = frozenset(
        {
            closure.EXACT_RESIDUAL_PAIR,
            (
                closure.mask(("C", "2C")),
                closure.mask(("0", "A", "2A", "BC")),
            ),
            (
                closure.mask(("0", "C", "2C")),
                closure.mask(("A", "2A", "BC")),
            ),
        }
    )
    handled_keys = {
        _descriptor_swap_key(obstruction(pair))
        for pair in handled_exact_pairs
        if obstruction(pair) is not None
    }
    assert handled_keys == {((0, 1, 0), (0, 2, 0))}
    assert covered == failures
    return {
        "claim_scope": "canonical analytic gate table; not recurrence for the remaining pairs",
        "remaining_positive_pairs": len(positive_failed),
        "remaining_signed_pairs": len(signed_failed),
        "remaining_total_pairs": len(failures),
        "canonical_descriptor_gates": len(gates),
        "exact_physical_time_pairs_removed_before_table": len(handled_exact_pairs),
        "removed_pairs_all_in_gate": {
            "weight": [0, 1, 0],
            "caps": [0, 2, 0],
        },
        "gates": gates,
    }


def certificate() -> dict[str, object]:
    positive = split_certificate(
        "positive-active-invariant residual",
        closure.POSITIVE_SHIELDED_MASKS,
    )
    signed = split_certificate(
        "signed residual",
        closure.SIGNED_SHIELDED_MASKS,
    )
    signed["exact_service_superset_audit"] = signed_service_superset_certificate()
    second_certified, second_failed = (
        frozenset(
            pair
            for pair in part
            if pair[0] == closure.SECOND_SHIELDED_MASK
        )
        for part in tier_split(closure.POSITIVE_SHIELDED_MASKS)
    )
    assert len(second_certified) == 12
    assert len(second_failed) == 37
    assert second_certified == closure.second_family_tier_certified_pairs()

    payload = {
        "claim_scope": "exact tier-interface support certificate; not T3-2",
        "comparison_hyperplanes": len(comparison_normals()),
        "simplex_vertices": len(simplex_vertices()),
        "arrangement_candidates": len(arrangement_candidates()),
        "tier_types": len(tier_types()),
        "tier_availability_descriptors": len(tier_descriptors()),
        "positive": positive,
        "signed": signed,
        "second_family": {
            "tier_certified": len(second_certified),
            "remaining": len(second_failed),
        },
        "analytic_gate_table": analytic_gate_certificate(),
        "one_active_interface": one_active_interface_certificate(),
        "zero_cap_axis_selector": zero_cap_axis_certificate(),
    }
    digest_payload = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = sha256(digest_payload).hexdigest()
    return payload


def self_test() -> None:
    result = certificate()
    assert result["comparison_hyperplanes"] == 21
    assert result["simplex_vertices"] == 37
    assert result["arrangement_candidates"] == 5128
    assert result["tier_types"] == 193
    assert result["tier_availability_descriptors"] == 259
    assert result["positive"]["input_residual_pairs"] == 3531
    assert result["positive"]["universally_tier_certified"] == 1219
    assert result["positive"]["not_universally_tier_certified"] == 2312
    assert result["positive"]["greedy_obstruction_descriptors"] == 17
    assert result["signed"]["input_residual_pairs"] == 358
    assert result["signed"]["universally_tier_certified"] == 159
    assert result["signed"]["not_universally_tier_certified"] == 199
    assert result["signed"]["greedy_obstruction_descriptors"] == 4
    assert result["one_active_interface"]["families"]["positive"][
        "classwise_invariant_closures"
    ] == 67
    assert result["one_active_interface"]["families"]["signed"][
        "classwise_invariant_closures"
    ] == 0
    assert result["zero_cap_axis_selector"]["positive"]["selected"] == 596
    assert result["zero_cap_axis_selector"]["signed"]["selected"] == 151


if __name__ == "__main__":
    self_test()
    print(json.dumps(certificate(), indent=2, sort_keys=True))
