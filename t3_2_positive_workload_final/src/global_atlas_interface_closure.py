"""Finite support audit for the global shielded/available interface.

This certificate deliberately separates finite support statements from the
analytic recurrence arguments in ``research_notes/global_atlas_interface_closure.md``.
It does not certify T3-2.

The displayed chart has active coordinates A,B and uses the four workload
representatives in :mod:`exact_shielded_seam`.  Exchange of A and B, and the
corresponding relabellings of a chart, are external symmetries.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from itertools import combinations, product
from typing import Iterable, Sequence

import exact_shielded_seam as seam


Vector = tuple[int, int, int]
Support = tuple[str, ...]
Pair = tuple[int, int]

NAMES = seam.NAMES
COMPLEXES = seam.COMPLEXES
WORKLOADS = seam.WORKLOADS

NAME_TO_INDEX = {name: index for index, name in enumerate(NAMES)}

POSITIVE_SHIELDED_MASKS = frozenset(
    sum(1 << NAME_TO_INDEX[name] for name in support)
    for support in seam.positive_invariant_shielded_supports()
)
SIGNED_SHIELDED_MASKS = frozenset(
    sum(1 << NAME_TO_INDEX[name] for name in support)
    for support in seam.SIGNED_SUPPORTS
)

SIGNED_SERVICE_PURE_MASKS = frozenset(
    {
        sum(1 << NAME_TO_INDEX[name] for name in ("C", "2C")),
        sum(1 << NAME_TO_INDEX[name] for name in ("0", "C", "2C")),
    }
)

EXACT_AVAILABLE_MASK = sum(
    1 << NAME_TO_INDEX[name] for name in ("C", "AC", "BC")
)
EXACT_SHIELDED_MASKS = frozenset(
    sum(1 << NAME_TO_INDEX[name] for name in support)
    for support in seam.EXPECTED_EXACT_SEAM_SUPPORTS
)

SECOND_SHIELDED_SUPPORT: Support = ("A", "B", "AC", "BC")
SECOND_SHIELDED_MASK = sum(
    1 << NAME_TO_INDEX[name] for name in SECOND_SHIELDED_SUPPORT
)
SECOND_LOW: tuple[str, ...] = ("0", "C", "2C")
SECOND_QUADRATIC: tuple[str, ...] = ("2A", "2B", "AB")

EXACT_RESIDUAL_PAIR: Pair = (
    sum(1 << NAME_TO_INDEX[name] for name in ("B", "2A", "BC")),
    sum(1 << NAME_TO_INDEX[name] for name in ("0", "A", "C")),
)

AB_SWAP = {
    "0": "0",
    "A": "B",
    "B": "A",
    "C": "C",
    "2A": "2B",
    "2B": "2A",
    "2C": "2C",
    "AB": "AB",
    "AC": "BC",
    "BC": "AC",
}


def support(mask: int) -> Support:
    return tuple(NAMES[index] for index in range(len(NAMES)) if mask >> index & 1)


def mask(names: Iterable[str]) -> int:
    return sum(1 << NAME_TO_INDEX[name] for name in names)


def swap_ab_mask(value: int) -> int:
    return mask(AB_SWAP[name] for name in support(value))


def pair_orbit_key(pair: Pair) -> Pair:
    swapped = swap_ab_mask(pair[0]), swap_ab_mask(pair[1])
    return min(pair, swapped)


def nonempty_subsets(names: Sequence[str]) -> tuple[Support, ...]:
    return tuple(
        tuple(choice)
        for size in range(1, len(names) + 1)
        for choice in combinations(names, size)
    )


def full_rows(first: int, second: int) -> tuple[tuple[Fraction, ...], ...]:
    return seam._rref(seam._difference_rows(first) + seam._difference_rows(second))


def full_deficiency(first: int, second: int) -> int:
    """Deficiency of two disjoint linkage supports."""

    if first & second:
        raise ValueError("linkage supports must be disjoint")
    return first.bit_count() + second.bit_count() - 2 - len(full_rows(first, second))


def has_positive_active_invariant(first: int, second: int) -> bool:
    """Whether the common kernel contains q with q_A,q_B strictly positive."""

    rows = full_rows(first, second)
    rank = len(rows)
    if rank == 0:
        return True
    if rank == 3:
        return False
    if rank == 1:
        a_value, b_value, c_value = rows[0]
        return bool(
            c_value
            or a_value * b_value < 0
            or (not a_value and not b_value)
        )
    first_row, second_row = rows
    normal = (
        first_row[1] * second_row[2] - first_row[2] * second_row[1],
        first_row[2] * second_row[0] - first_row[0] * second_row[2],
        first_row[0] * second_row[1] - first_row[1] * second_row[0],
    )
    return bool(normal[0] and normal[1] and normal[0] * normal[1] > 0)


def has_strictly_positive_invariant(first: int, second: int) -> bool:
    """Whether the common kernel contains q with all three entries positive."""

    rows = full_rows(first, second)
    rank = len(rows)
    if rank == 0:
        return True
    if rank == 3:
        return False
    if rank == 1:
        row = rows[0]
        return bool(min(row) < 0 < max(row) or all(not entry for entry in row))
    first_row, second_row = rows
    normal = (
        first_row[1] * second_row[2] - first_row[2] * second_row[1],
        first_row[2] * second_row[0] - first_row[0] * second_row[2],
        first_row[0] * second_row[1] - first_row[1] * second_row[0],
    )
    return all(entry > 0 for entry in normal) or all(entry < 0 for entry in normal)


@lru_cache(maxsize=None)
def chart_instances(shielded_masks: frozenset[int]) -> tuple[tuple[Vector, int, int], ...]:
    """Ordered shielded/available chart instances before support de-duplication."""

    instances: list[tuple[Vector, int, int]] = []
    for workload, shielded in product(WORKLOADS, shielded_masks):
        if not seam.classify_shielded(shielded, workload):
            continue
        for available in range(1, 1 << len(NAMES)):
            if available.bit_count() < 2 or shielded & available:
                continue
            if seam.classify_shielded(available, workload):
                continue
            instances.append((workload, shielded, available))
    return tuple(instances)


@lru_cache(maxsize=None)
def unique_pairs(shielded_masks: frozenset[int]) -> frozenset[Pair]:
    return frozenset((shielded, available) for _, shielded, available in chart_instances(shielded_masks))


def is_exact_seam(pair: Pair) -> bool:
    shielded, available = pair
    return shielded in EXACT_SHIELDED_MASKS and available == EXACT_AVAILABLE_MASK


def is_signed_service_seam(pair: Pair) -> bool:
    """Exact support scope of ``signed_service_seam_full_proof.md``.

    This is an unordered physical-network predicate.  Overlapping supports
    are excluded because linkage classes have disjoint complex sets.
    """

    first, second = pair
    if first & second:
        return False
    return bool(
        (first in SIGNED_SERVICE_PURE_MASKS and second in SIGNED_SHIELDED_MASKS)
        or (second in SIGNED_SERVICE_PURE_MASKS and first in SIGNED_SHIELDED_MASKS)
    )


def is_exact_residual_pair(pair: Pair) -> bool:
    """Exact scope of ``residual_pair_full_proof.md``, up to linkage order."""

    return pair == EXACT_RESIDUAL_PAIR or pair == tuple(reversed(EXACT_RESIDUAL_PAIR))


def branch(pair: Pair) -> str:
    """Disjoint branch order used solely for the reported table.

    Strictly positive invariants are listed before the broader active-only
    invariant branch.  Deficiency zero is then applied before the exact seam;
    consequently one of the seven exact-seam pairs is recorded under
    deficiency zero.  ``exact_seam_pairs`` below reports the overlap-free
    geometric count of seven separately.
    """

    shielded, available = pair
    if has_strictly_positive_invariant(shielded, available):
        return "finite_strict_invariant"
    if has_positive_active_invariant(shielded, available):
        return "common_active_invariant"
    if full_deficiency(shielded, available) == 0:
        return "full_deficiency_zero"
    if is_signed_service_seam(pair):
        return "exact_signed_service_seam"
    if is_exact_residual_pair(pair):
        return "exact_residual_pair"
    if is_exact_seam(pair):
        return "exact_seven_support_seam"
    return "residual"


@lru_cache(maxsize=None)
def residual_pairs(shielded_masks: frozenset[int]) -> frozenset[Pair]:
    return frozenset(pair for pair in unique_pairs(shielded_masks) if branch(pair) == "residual")


def pair_payload(pair: Pair) -> tuple[Support, Support]:
    return support(pair[0]), support(pair[1])


def pair_fingerprint(pairs: Iterable[Pair]) -> str:
    payload = sorted((pair_payload(pair) for pair in pairs), key=lambda item: (item[0], item[1]))
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=False).encode()
    return sha256(encoded).hexdigest()


def residual_counts_by_shielded(shielded_masks: frozenset[int]) -> dict[str, int]:
    counts = Counter(shielded for shielded, _ in residual_pairs(shielded_masks))
    return {
        ",".join(support(shielded)): counts[shielded]
        for shielded in sorted(counts, key=lambda item: (item.bit_count(), support(item)))
    }


def second_family_supports() -> frozenset[int]:
    return frozenset(
        mask(low + quadratic)
        for low, quadratic in product(
            nonempty_subsets(SECOND_LOW),
            nonempty_subsets(SECOND_QUADRATIC),
        )
    )


def second_family_minimal_supports() -> frozenset[int]:
    return frozenset(mask((low, quadratic)) for low, quadratic in product(SECOND_LOW, SECOND_QUADRATIC))


def second_family_tier_certified_supports() -> frozenset[int]:
    """The 12 supersets proved by the tier argument in the research note."""

    return frozenset(
        available
        for available in second_family_supports()
        if {"2A", "2B"}.issubset(support(available))
        and bool({"C", "2C"}.intersection(support(available)))
    )


def second_family_tier_certified_pairs() -> frozenset[Pair]:
    return frozenset(
        (SECOND_SHIELDED_MASK, available)
        for available in second_family_tier_certified_supports()
    )


def verify_second_family() -> dict[str, object]:
    chart_workloads = tuple(
        workload
        for workload in WORKLOADS
        if seam.classify_shielded(SECOND_SHIELDED_MASK, workload)
    )
    assert chart_workloads == ((1, 1, 0),)

    compatible = frozenset(
        available
        for available in range(1, 1 << len(NAMES))
        if available.bit_count() >= 2
        and not (available & SECOND_SHIELDED_MASK)
        and not seam.classify_shielded(available, chart_workloads[0])
    )
    expected = second_family_supports()
    assert compatible == expected
    assert len(expected) == 49

    minimal = frozenset(
        available
        for available in compatible
        if not any(
            candidate != available and candidate & available == candidate
            for candidate in compatible
        )
    )
    assert minimal == second_family_minimal_supports()
    assert len(minimal) == 9

    for available in compatible:
        assert len(full_rows(SECOND_SHIELDED_MASK, available)) == 3
        assert full_deficiency(SECOND_SHIELDED_MASK, available) == available.bit_count() - 1
        assert not has_positive_active_invariant(SECOND_SHIELDED_MASK, available)

    tier_certified = second_family_tier_certified_supports()
    assert len(tier_certified) == 12
    assert tier_certified.isdisjoint(minimal)

    all_orbits = {min(item, swap_ab_mask(item)) for item in compatible}
    minimal_orbits = {min(item, swap_ab_mask(item)) for item in minimal}
    remaining_orbits = {
        min(item, swap_ab_mask(item)) for item in compatible - tier_certified
    }
    assert len(all_orbits) == 35
    assert len(minimal_orbits) == 6
    assert len(remaining_orbits) == 23

    return {
        "workload": list(chart_workloads[0]),
        "compatible_available_supports": len(compatible),
        "minimal_available_supports": len(minimal),
        "minimal_supports": [list(support(item)) for item in sorted(minimal)],
        "tier_certified_supersets": len(tier_certified),
        "tier_certified_supports": [
            list(support(item))
            for item in sorted(tier_certified, key=lambda item: (item.bit_count(), support(item)))
        ],
        "remaining_after_tier_lemma": len(compatible - tier_certified),
        "supports_modulo_A_B_exchange": len(all_orbits),
        "minimal_modulo_A_B_exchange": len(minimal_orbits),
        "remaining_modulo_A_B_exchange": len(remaining_orbits),
        "deficiency_formula": "delta(L0 union L1) = |L1|-1",
    }


def family_certificate(label: str, shielded_masks: frozenset[int]) -> dict[str, object]:
    instances = chart_instances(shielded_masks)
    pairs = unique_pairs(shielded_masks)
    branch_counts = Counter(branch(pair) for pair in pairs)
    residual = residual_pairs(shielded_masks)
    return {
        "label": label,
        "chart_instances": len(instances),
        "unique_ordered_support_pairs": len(pairs),
        "branch_counts": dict(sorted(branch_counts.items())),
        "residual_pairs": len(residual),
        "residual_pair_keys_modulo_A_B_exchange": len(
            {pair_orbit_key(pair) for pair in residual}
        ),
        "residual_sha256": pair_fingerprint(residual),
        "residual_by_shielded_support": residual_counts_by_shielded(shielded_masks),
    }


def certificate() -> dict[str, object]:
    positive = family_certificate("positive-active-invariant shielded", POSITIVE_SHIELDED_MASKS)
    signed = family_certificate("signed one-active shielded", SIGNED_SHIELDED_MASKS)
    post_tier_residual = residual_pairs(POSITIVE_SHIELDED_MASKS) - second_family_tier_certified_pairs()
    assert len(post_tier_residual) == 3519
    positive["residual_after_12_support_tier_lemma"] = len(post_tier_residual)
    positive["post_tier_residual_sha256"] = pair_fingerprint(post_tier_residual)
    exact_pairs = frozenset(
        pair
        for pair in unique_pairs(POSITIVE_SHIELDED_MASKS)
        if is_exact_seam(pair)
    )
    assert len(exact_pairs) == 7
    assert sum(branch(pair) == "exact_seven_support_seam" for pair in exact_pairs) == 6
    assert sum(branch(pair) == "full_deficiency_zero" for pair in exact_pairs) == 1

    signed_service_pairs = frozenset(
        (pure, mixed)
        for pure, mixed in product(SIGNED_SERVICE_PURE_MASKS, SIGNED_SHIELDED_MASKS)
        if is_signed_service_seam((pure, mixed))
    )
    assert len(signed_service_pairs) == 5
    assert sum(full_deficiency(*pair) == 0 for pair in signed_service_pairs) == 3
    assert sum(branch(pair) == "exact_signed_service_seam" for pair in signed_service_pairs) == 2
    signed_available_pairs = unique_pairs(SIGNED_SHIELDED_MASKS)
    assert not (signed_service_pairs & signed_available_pairs)
    assert not any(
        (mixed, pure) in signed_available_pairs
        for pure, mixed in signed_service_pairs
    )
    assert EXACT_RESIDUAL_PAIR in unique_pairs(POSITIVE_SHIELDED_MASKS)
    assert branch(EXACT_RESIDUAL_PAIR) == "exact_residual_pair"
    assert EXACT_RESIDUAL_PAIR not in unique_pairs(SIGNED_SHIELDED_MASKS)

    return {
        "claim_scope": "finite support/interface audit plus separately proved exact seams and 12-support tier lemma; not T3-2",
        "positive": positive,
        "signed": signed,
        "exact_seam_geometric_pairs": len(exact_pairs),
        "exact_seam_deficiency_zero_overlap": 1,
        "signed_service_geometric_pairs": len(signed_service_pairs),
        "signed_service_deficiency_zero_overlap": 3,
        "signed_service_new_positive_table_pairs": 2,
        "signed_service_pairs_in_signed_available_table": 0,
        "exact_residual_pair_new_positive_table_pairs": 1,
        "exact_residual_pair_pairs_in_signed_available_table": 0,
        "second_deficiency_one_family": verify_second_family(),
    }


def self_test() -> None:
    result = certificate()
    positive = result["positive"]
    signed = result["signed"]
    assert positive["chart_instances"] == 11070
    assert positive["unique_ordered_support_pairs"] == 4761
    assert positive["branch_counts"] == {
        "common_active_invariant": 110,
        "exact_seven_support_seam": 6,
        "exact_signed_service_seam": 2,
        "exact_residual_pair": 1,
        "finite_strict_invariant": 187,
        "full_deficiency_zero": 924,
        "residual": 3531,
    }
    assert signed["chart_instances"] == 645
    assert signed["unique_ordered_support_pairs"] == 408
    assert signed["branch_counts"] == {
        "full_deficiency_zero": 50,
        "residual": 358,
    }


if __name__ == "__main__":
    self_test()
    print(json.dumps(certificate(), indent=2, sort_keys=True))
