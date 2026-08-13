"""Exact support certificate for the 336 residual all-active incidences.

This module certifies a finite set identity only.  The physical-time
generator theorem for the resulting level-set family is proved in
``research_notes/proof_first_all_active_residual_levelset_336_theorem.md``.
No reaction orientations, rate vectors, population states, or stochastic
paths are enumerated here.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import permutations
import json
from typing import Iterable

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import s_tier_superlevel_interface as superlevel
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as three_active


Pair = closure.Pair
Descriptor = tier.TierDescriptor
Incidence = tuple[Pair, Descriptor]
Mask = int
DeadRayRow = tuple[Pair, Descriptor, int, str, tuple[str, ...]]

FULL_MASK = (1 << len(closure.COMPLEXES)) - 1
ZERO_NODE = closure.COMPLEXES.index((0, 0, 0))
UNARY_NODES = frozenset(
    node
    for node, vector in enumerate(closure.COMPLEXES)
    if sum(vector) == 1
)
VECTOR_TO_NODE = {
    vector: node for node, vector in enumerate(closure.COMPLEXES)
}


def _dot(weight: tuple[int, int, int], node: int) -> int:
    return sum(
        weight[coordinate] * closure.COMPLEXES[node][coordinate]
        for coordinate in range(3)
    )


def _permuted_mask(mask: Mask, permutation: tuple[int, int, int]) -> Mask:
    """Relabel a support by one species permutation."""

    result = 0
    for node in tier._nodes(mask):
        vector = closure.COMPLEXES[node]
        image = tuple(vector[permutation[index]] for index in range(3))
        result |= 1 << VECTOR_TO_NODE[image]
    return result


@lru_cache(maxsize=1)
def all_ordered_disjoint_pairs() -> frozenset[Pair]:
    """All ordered disjoint support pairs, each support of size at least two."""

    result: set[Pair] = set()
    for first in range(1, FULL_MASK + 1):
        if first.bit_count() < 2:
            continue
        available = FULL_MASK ^ first
        second = available
        while second:
            if second.bit_count() >= 2:
                result.add((first, second))
            second = (second - 1) & available
    return frozenset(result)


@lru_cache(maxsize=1)
def mixed_atlas_orbit() -> frozenset[Pair]:
    """The inherited mixed-pair tables, closed under S3 and linkage reversal."""

    seeds = set(closure.unique_pairs(closure.POSITIVE_SHIELDED_MASKS))
    seeds.update(closure.unique_pairs(closure.SIGNED_SHIELDED_MASKS))
    result: set[Pair] = set()
    for first, second in seeds:
        for permutation in permutations(range(3)):
            image = (
                _permuted_mask(first, permutation),
                _permuted_mask(second, permutation),
            )
            result.add(image)
            result.add((image[1], image[0]))
    return frozenset(result)


@lru_cache(maxsize=1)
def outside_mixed_atlas() -> frozenset[Pair]:
    return all_ordered_disjoint_pairs() - mixed_atlas_orbit()


@lru_cache(maxsize=1)
def after_positive_active_invariant_branch() -> frozenset[Pair]:
    """Diagnostic legacy prebranch with only A,B required positive."""

    return frozenset(
        pair
        for pair in outside_mixed_atlas()
        if not closure.has_positive_active_invariant(*pair)
    )


@lru_cache(maxsize=1)
def after_strictly_positive_invariant_branch() -> frozenset[Pair]:
    """Pairs not discharged by a proper all-coordinate linear invariant."""

    return frozenset(
        pair
        for pair in outside_mixed_atlas()
        if not closure.has_strictly_positive_invariant(*pair)
    )


@lru_cache(maxsize=1)
def residual_pair_universe() -> frozenset[Pair]:
    """The exact pair universe entering the corrected all-active cut."""

    return frozenset(
        pair
        for pair in after_strictly_positive_invariant_branch()
        if closure.full_deficiency(*pair) != 0
    )


@lru_cache(maxsize=1)
def all_active_descriptors() -> tuple[Descriptor, ...]:
    return tuple(
        descriptor
        for descriptor in tier.tier_descriptors()
        if descriptor.active_mask == 0b111
    )


def _incidence_sort_key(incidence: Incidence) -> tuple[object, ...]:
    pair, descriptor = incidence
    return closure.pair_payload(pair), descriptor.weight, descriptor.caps


@lru_cache(maxsize=1)
def selected_incidences() -> tuple[Incidence, ...]:
    """Corrected-cut failures which are feasible in an affine class."""

    rows = [
        (pair, descriptor)
        for pair in residual_pair_universe()
        for descriptor in all_active_descriptors()
        if not superlevel.universal_strong_orientation_condition(
            pair,
            descriptor,
        )
        and feasibility.descriptor_feasible(pair, descriptor)
    ]
    return tuple(sorted(rows, key=_incidence_sort_key))


@lru_cache(maxsize=None)
def _support_rank(mask: Mask) -> int:
    return three_active._support_rank(mask)


def levelset_geometry(
    pair: Pair,
    descriptor: Descriptor,
) -> tuple[int, Mask, Mask, int] | None:
    """Recognize the analytic level-set family.

    The return value is ``(top_side, T, R, s)``.  Here ``T`` has internal
    rank two and lies on level ``2s`` of the positive descriptor weight,
    while ``R`` is zero together with two or three unary complexes on level
    ``s``.
    """

    weight = descriptor.weight
    if not all(weight):
        return None
    matches: list[tuple[int, Mask, Mask, int]] = []
    for side in (0, 1):
        top = pair[side]
        lower = pair[1 - side]
        lower_nodes = tier._nodes(lower)
        if ZERO_NODE not in lower_nodes:
            continue
        unary_nodes = lower_nodes - {ZERO_NODE}
        if len(unary_nodes) not in (2, 3) or not unary_nodes <= UNARY_NODES:
            continue
        unary_levels = {_dot(weight, node) for node in unary_nodes}
        if len(unary_levels) != 1:
            continue
        scale = next(iter(unary_levels))
        if scale <= 0 or _support_rank(top) != 2:
            continue
        if not all(
            _dot(weight, node) == 2 * scale
            for node in tier._nodes(top)
        ):
            continue
        matches.append((side, top, lower, scale))
    if len(matches) > 1:
        raise AssertionError("disjoint supports cannot both contain zero")
    return matches[0] if matches else None


@lru_cache(maxsize=1)
def geometric_incidences() -> tuple[Incidence, ...]:
    """Every incidence in the residual universe with the level-set geometry."""

    rows = [
        (pair, descriptor)
        for pair in residual_pair_universe()
        for descriptor in all_active_descriptors()
        if levelset_geometry(pair, descriptor) is not None
    ]
    return tuple(sorted(rows, key=_incidence_sort_key))


def incidence_fingerprint(
    incidences: Iterable[Incidence],
    *,
    sort_keys: bool = True,
) -> str:
    """Fingerprint rows in the repository's established JSON encoding."""

    ordered = sorted(incidences, key=_incidence_sort_key)
    payload = [
        {
            "pair": closure.pair_payload(pair),
            "weight": descriptor.weight,
            "caps": descriptor.caps,
        }
        for pair, descriptor in ordered
    ]
    encoded = json.dumps(
        payload,
        sort_keys=sort_keys,
        separators=(",", ":"),
    ).encode()
    return sha256(encoded).hexdigest()


def _weight_key(weight: tuple[int, int, int]) -> str:
    return ",".join(map(str, weight))


def _support_key(mask: Mask) -> str:
    return ",".join(closure.support(mask))


def _unit(coordinate: int) -> tuple[int, int, int]:
    return tuple(
        int(index == coordinate)
        for index in range(3)
    )  # type: ignore[return-value]


def _double(coordinate: int) -> tuple[int, int, int]:
    return tuple(
        2 * int(index == coordinate)
        for index in range(3)
    )  # type: ignore[return-value]


def _cross(first: int, second: int) -> tuple[int, int, int]:
    return tuple(
        int(index == first) + int(index == second)
        for index in range(3)
    )  # type: ignore[return-value]


@lru_cache(maxsize=1)
def homogeneous_dead_ray_rows() -> tuple[DeadRayRow, ...]:
    """Symbolically classify every dead pure ray in the 312 rows."""

    names = ("X", "Y", "Z")
    rows: list[DeadRayRow] = []
    for pair, descriptor in selected_incidences():
        if descriptor.weight != (1, 1, 1):
            continue
        geometry = levelset_geometry(pair, descriptor)
        assert geometry is not None
        _, top_mask, lower_mask, _ = geometry
        top = {
            closure.COMPLEXES[node]
            for node in tier._nodes(top_mask)
        }
        lower = {
            closure.COMPLEXES[node]
            for node in tier._nodes(lower_mask)
        }
        for dead in range(3):
            if _double(dead) in top:
                continue
            others = [index for index in range(3) if index != dead]
            carriers = [
                index
                for index in others
                if _cross(dead, index) in top
            ]
            assert carriers
            if len(carriers) == 2:
                kernel = "two_carrier"
                carrier = min(carriers)
                opposite = max(carriers)
            else:
                carrier = carriers[0]
                opposite = next(
                    index for index in others if index != carrier
                )
                if _double(opposite) in top:
                    kernel = "dyadic"
                else:
                    kernel = "common_catalyst"
                    assert top == {
                        _cross(dead, carrier),
                        _cross(carrier, opposite),
                        _double(carrier),
                    }
            relabel = (dead, carrier, opposite)
            lower_pattern = tuple(
                names[position]
                for position, coordinate in enumerate(relabel)
                if _unit(coordinate) in lower
            )
            rows.append(
                (pair, descriptor, dead, kernel, lower_pattern)
            )
    return tuple(
        sorted(
            rows,
            key=lambda row: (
                _incidence_sort_key((row[0], row[1])),
                row[2],
                row[3],
                row[4],
            ),
        )
    )


def dead_ray_fingerprint(rows: Iterable[DeadRayRow]) -> str:
    payload = [
        {
            "pair": closure.pair_payload(pair),
            "weight": descriptor.weight,
            "caps": descriptor.caps,
            "dead_coordinate": dead,
            "kernel": kernel,
            "lower_pattern": lower_pattern,
        }
        for pair, descriptor, dead, kernel, lower_pattern in rows
    ]
    return sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@lru_cache(maxsize=1)
def certificate() -> dict[str, object]:
    """Return and internally verify the exact 336-row support identity."""

    all_pairs = all_ordered_disjoint_pairs()
    seeds = set(closure.unique_pairs(closure.POSITIVE_SHIELDED_MASKS))
    seeds.update(closure.unique_pairs(closure.SIGNED_SHIELDED_MASKS))
    orbit = mixed_atlas_orbit()
    outside = outside_mixed_atlas()
    after_strict = after_strictly_positive_invariant_branch()
    after_active_only = after_positive_active_invariant_branch()
    active_only_gap = after_strict - after_active_only
    residual = residual_pair_universe()
    selected = selected_incidences()
    geometric = geometric_incidences()

    assert len(all_pairs) == 46_872
    assert len(seeds) == 5_169
    assert len(orbit) == 27_894
    assert len(outside) == 18_978
    assert len(outside - after_strict) == 146
    assert len(after_strict) == 18_832
    assert len(active_only_gap) == 68
    assert len(after_active_only) == 18_764
    assert after_strict == residual
    assert len(all_active_descriptors()) == 169
    assert selected == geometric
    assert len(selected) == 336
    assert len({pair for pair, _ in selected}) == 336
    assert not any(pair in active_only_gap for pair, _ in selected)

    weights: Counter[tuple[int, int, int]] = Counter()
    top_sizes: Counter[int] = Counter()
    top_deficiencies: Counter[int] = Counter()
    lower_supports: Counter[Mask] = Counter()
    full_deficiencies: Counter[int] = Counter()
    top_sides: Counter[int] = Counter()
    top_quadratic_only: Counter[bool] = Counter()
    dead_rays = homogeneous_dead_ray_rows()
    dead_ray_kernels = Counter(row[3] for row in dead_rays)
    dead_ray_lower_patterns = Counter(
        (row[3], row[4]) for row in dead_rays
    )
    dead_ray_bulk_in_lower = Counter(
        (row[3], "X" in row[4], len(row[4]))
        for row in dead_rays
    )

    for pair, descriptor in selected:
        geometry = levelset_geometry(pair, descriptor)
        assert geometry is not None
        side, top, lower, scale = geometry
        assert scale > 0
        assert descriptor.caps == (2, 2, 2)
        assert _support_rank(top) == 2
        weights[descriptor.weight] += 1
        top_sizes[top.bit_count()] += 1
        top_deficiencies[three_active._support_deficiency(top)] += 1
        lower_supports[lower] += 1
        full_deficiencies[closure.full_deficiency(*pair)] += 1
        top_sides[side] += 1
        top_quadratic_only[
            all(
                sum(closure.COMPLEXES[node]) == 2
                for node in tier._nodes(top)
            )
        ] += 1

    assert weights == Counter(
        {
            (1, 1, 1): 312,
            (1, 1, 2): 8,
            (1, 2, 1): 8,
            (2, 1, 1): 8,
        }
    )
    assert top_sizes == Counter({3: 154, 4: 126, 5: 48, 6: 8})
    assert top_deficiencies == Counter({0: 154, 1: 126, 2: 48, 3: 8})
    assert lower_supports == Counter(
        {
            closure.mask(("0", "A", "B")): 86,
            closure.mask(("0", "A", "C")): 86,
            closure.mask(("0", "B", "C")): 86,
            closure.mask(("0", "A", "B", "C")): 78,
        }
    )
    assert full_deficiencies == Counter({1: 120, 2: 130, 3: 66, 4: 18, 5: 2})
    assert top_sides == Counter({0: 168, 1: 168})
    assert top_quadratic_only == Counter({True: 312, False: 24})
    assert len(dead_rays) == 360
    assert dead_ray_kernels == Counter(
        {"two_carrier": 168, "dyadic": 144, "common_catalyst": 48}
    )
    assert dead_ray_lower_patterns[
        ("common_catalyst", ("X", "Y"))
    ] == 12
    assert dead_ray_lower_patterns[
        ("common_catalyst", ("Y", "Z"))
    ] == 12
    assert dead_ray_lower_patterns[
        ("common_catalyst", ("X", "Z"))
    ] == 12
    assert dead_ray_lower_patterns[
        ("common_catalyst", ("X", "Y", "Z"))
    ] == 12
    assert sum(
        count
        for (_, has_bulk, _), count in dead_ray_bulk_in_lower.items()
        if has_bulk
    ) == 270

    canonical_hash = incidence_fingerprint(selected, sort_keys=True)
    independent_hash = incidence_fingerprint(selected, sort_keys=False)
    assert canonical_hash == (
        "d0c31db81db2400e0ead6e4a1a86b237fbf3b8bbb597340856a2756e9f6c884d"
    )
    assert independent_hash == (
        "2bd4025f29d20ea4af467d46704c598652c9332ac4e32df18669cb7eb75c75a0"
    )

    return {
        "claim_scope": (
            "finite support/descriptor set identity only; the arbitrary-"
            "orientation physical-time theorem is analytic"
        ),
        "all_ordered_disjoint_support_pairs": len(all_pairs),
        "mixed_atlas_seed_pairs": len(seeds),
        "mixed_atlas_orbit_pairs": len(orbit),
        "outside_mixed_atlas_pairs": len(outside),
        "removed_by_strictly_positive_invariant": len(outside - after_strict),
        "after_strictly_positive_invariant_pairs": len(after_strict),
        "active_only_invariant_gap_pairs_retained": len(active_only_gap),
        "active_only_gap_selected_incidences": sum(
            pair in active_only_gap for pair, _ in selected
        ),
        "removed_by_deficiency_zero_after_invariant": len(after_strict - residual),
        "residual_pair_universe": len(residual),
        "all_active_descriptors": len(all_active_descriptors()),
        "corrected_feasible_failing_incidences": len(selected),
        "distinct_pairs": len({pair for pair, _ in selected}),
        "geometric_incidences": len(geometric),
        "selected_equals_geometric": selected == geometric,
        "weight_histogram": {
            _weight_key(weight): count
            for weight, count in sorted(weights.items())
        },
        "top_size_histogram": dict(sorted(top_sizes.items())),
        "top_rank_histogram": {2: len(selected)},
        "top_deficiency_histogram": dict(sorted(top_deficiencies.items())),
        "lower_support_histogram": {
            _support_key(mask): count
            for mask, count in sorted(
                lower_supports.items(),
                key=lambda item: closure.support(item[0]),
            )
        },
        "full_deficiency_histogram": dict(sorted(full_deficiencies.items())),
        "top_side_histogram": dict(sorted(top_sides.items())),
        "top_quadratic_only": top_quadratic_only[True],
        "top_with_unary": top_quadratic_only[False],
        "homogeneous_dead_ray_count": len(dead_rays),
        "homogeneous_dead_ray_kernel_histogram": dict(
            sorted(dead_ray_kernels.items())
        ),
        "homogeneous_dead_ray_bulk_in_lower": sum(
            count
            for (_, has_bulk, _), count in dead_ray_bulk_in_lower.items()
            if has_bulk
        ),
        "homogeneous_common_catalyst_lower_patterns": {
            ",".join(pattern): count
            for (kernel, pattern), count in sorted(
                dead_ray_lower_patterns.items()
            )
            if kernel == "common_catalyst"
        },
        "homogeneous_dead_ray_sha256": dead_ray_fingerprint(dead_rays),
        "incidence_sha256": canonical_hash,
        "independent_cross_encoding_sha256": independent_hash,
    }


def self_test() -> None:
    certificate()


if __name__ == "__main__":
    self_test()
    print(json.dumps(certificate(), indent=2, sort_keys=True))
