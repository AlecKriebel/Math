"""Exact finite certificate for the 18,496 outside-mixed remainder.

The certified universe is the 18,832 ordered support pairs left after the
strictly-positive-invariant branch, with the already certified 336 level-set
pairs removed.  This module enumerates support pairs and exact tier
descriptors only.  It does not enumerate orientations, rate vectors,
population states, stochastic histories, or communicating classes, and it
makes no recurrence claim.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
from typing import Iterable

import all_active_residual_levelset_336_certificate as levelset
import global_atlas_interface_closure as closure
import global_tier_interface as tier
import s_tier_superlevel_interface as superlevel
import stoichiometric_gate_feasibility as feasibility


Pair = closure.Pair
Descriptor = tier.TierDescriptor
Incidence = tuple[Pair, Descriptor]
Mask = int

EXPECTED_DEPENDENCY_SHA256 = {
    "all_active_residual_levelset_336_certificate.py": (
        "4149b682d1222bd3327548b0eb95921f7aae20663816b345b48285239c12f93d"
    ),
    "global_atlas_interface_closure.py": (
        "293a63711f6da152edd72615d27fad5bbb859aa33a4b7eb150673b27ae3cb5bd"
    ),
    "global_tier_interface.py": (
        "b8feae08c2eecf21b6e4e387eeaa6f5b15f32d862fca5324d4523c38872494ab"
    ),
    "s_tier_superlevel_interface.py": (
        "1a4e27fcf40af76cac6281f8830b7644bf086b3c05d97a963ce9f5bac736ad57"
    ),
    "stoichiometric_gate_feasibility.py": (
        "4602e7d31af02c26cc9785ed056c876e3e571e428ad974e861e4940b9edba9a1"
    ),
}

# Filled from the canonical JSON encodings below.  They are literal
# regression pins, not assumptions in the mathematical classification.
EXPECTED_REMAINDER_PAIR_SHA256 = (
    "eb7db151e42eb9562b1a1d519ea7dad212df52c6df368ffa08edbf79410db4ad"
)
EXPECTED_NO_FAILURE_PAIR_SHA256 = (
    "b425db9040d0836462f4240a4a3acf51d067d356eb4f2bfe4ce2cf648e42db26"
)
EXPECTED_FAILED_PAIR_SHA256 = (
    "036f9cb8f00f99f78be9cb6c2303208a8ca8b25be8c1bd350b8fac6b35582eed"
)
EXPECTED_SIGNATURE_SHA256 = (
    "d3adaf3aa0c6f3957162d1b1538dc6bf1797caa6bb4bc5c5812b53263851000b"
)
EXPECTED_SIGNATURE_CROSS_ENCODING_SHA256 = (
    "0d106ccdbd0701664aa451dead00230863abbcb88e19eb34f44fd1e12fe5fe22"
)


def _digest(payload: object, *, sort_keys: bool = True) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=sort_keys,
        separators=(",", ":"),
    ).encode()
    return sha256(encoded).hexdigest()


def dependency_sha256() -> dict[str, str]:
    source_directory = Path(__file__).resolve().parent
    return {
        filename: sha256((source_directory / filename).read_bytes()).hexdigest()
        for filename in EXPECTED_DEPENDENCY_SHA256
    }


def _nodes(mask: Mask) -> tuple[int, ...]:
    return tuple(
        node
        for node in range(len(closure.COMPLEXES))
        if mask >> node & 1
    )


def _active_coordinates(descriptor: Descriptor) -> tuple[int, ...]:
    return tuple(
        coordinate
        for coordinate in range(3)
        if descriptor.active_mask >> coordinate & 1
    )


def _level(descriptor: Descriptor, node: int) -> int:
    return sum(
        descriptor.weight[coordinate] * closure.COMPLEXES[node][coordinate]
        for coordinate in range(3)
    )


@lru_cache(maxsize=1)
def levelset_pairs() -> frozenset[Pair]:
    selected = levelset.selected_incidences()
    pairs = frozenset(pair for pair, _descriptor in selected)
    if len(pairs) != len(selected):
        raise AssertionError("the 336 certificate must select distinct pairs")
    return pairs


@lru_cache(maxsize=1)
def remainder_pairs() -> frozenset[Pair]:
    """The exact 18,832 residual universe minus the frozen 336 pairs."""

    return levelset.residual_pair_universe() - levelset_pairs()


def one_active_kind(mask: Mask, descriptor: Descriptor) -> str:
    """Return the exact Q/F0/F1/B/D one-active support category."""

    active = _active_coordinates(descriptor)
    if len(active) != 1:
        raise ValueError("one_active_kind requires exactly one active coordinate")
    (active_coordinate,) = active
    inactive = tuple(
        coordinate
        for coordinate in range(3)
        if coordinate != active_coordinate
    )
    vectors = tuple(closure.COMPLEXES[node] for node in _nodes(mask))
    degrees = tuple(vector[active_coordinate] for vector in vectors)

    if max(degrees) == 2:
        return "Q"
    if all(degree == 0 for degree in degrees):
        return "F0"
    if all(degree == 1 for degree in degrees):
        return "F1"
    if any(
        upper[active_coordinate] == 1
        and lower[active_coordinate] == 0
        and all(upper[index] <= lower[index] for index in inactive)
        for upper in vectors
        for lower in vectors
    ):
        return "B"
    return "D"


def two_active_kind(mask: Mask, descriptor: Descriptor) -> str:
    """Return the ordered Q/U/C/S classifier from the frozen bridge."""

    active = _active_coordinates(descriptor)
    if len(active) != 2:
        raise ValueError("two_active_kind requires exactly two active coordinates")
    (bounded,) = tuple(
        coordinate for coordinate in range(3) if coordinate not in active
    )
    nodes = frozenset(_nodes(mask))
    maximum = max(_level(descriptor, node) for node in nodes)
    top = frozenset(
        node for node in nodes if _level(descriptor, node) == maximum
    )

    # The order is part of the classifier definition.
    if top == nodes:
        return "S"
    if any(
        sum(closure.COMPLEXES[node][coordinate] for coordinate in active) == 2
        for node in top
    ):
        return "Q"
    top_active_support = tuple(
        coordinate
        for coordinate in active
        if any(closure.COMPLEXES[node][coordinate] > 0 for node in top)
    )
    if all(
        sum(
            closure.COMPLEXES[node][coordinate]
            for coordinate in top_active_support
        )
        == 1
        for node in nodes
    ):
        return "S"
    if any(sum(closure.COMPLEXES[node]) == 1 for node in top):
        return "U"
    if (
        any(closure.COMPLEXES[node][bounded] > 0 for node in top)
        and any(closure.COMPLEXES[node][bounded] > 0 for node in nodes - top)
    ):
        return "C"
    return "S"


def failure_profile(pair: Pair, descriptor: Descriptor) -> str:
    active_count = descriptor.active_mask.bit_count()
    if active_count == 1:
        kinds = tuple(sorted(one_active_kind(mask, descriptor) for mask in pair))
        return "/".join(kinds)
    if active_count == 2:
        kinds = tuple(two_active_kind(mask, descriptor) for mask in pair)
        if all(kind in {"Q", "U", "C"} for kind in kinds):
            return "AA"
        return "/".join(sorted(kinds))
    return f"active_count={active_count}"


def linkage_kinds(pair: Pair, descriptor: Descriptor) -> tuple[str, str]:
    active_count = descriptor.active_mask.bit_count()
    if active_count == 1:
        return tuple(one_active_kind(mask, descriptor) for mask in pair)
    if active_count == 2:
        return tuple(two_active_kind(mask, descriptor) for mask in pair)
    raise ValueError("the remainder has only one- and two-active failures")


def _incidence_sort_key(row: Incidence) -> tuple[object, ...]:
    pair, descriptor = row
    return (
        closure.pair_payload(pair),
        descriptor.weight,
        descriptor.caps,
        descriptor.active_mask,
        descriptor.partition,
    )


@lru_cache(maxsize=1)
def feasible_corrected_cut_failures() -> tuple[Incidence, ...]:
    rows = (
        (pair, descriptor)
        for pair in remainder_pairs()
        for descriptor in tier.tier_descriptors()
        if feasibility.descriptor_feasible(pair, descriptor)
        and not superlevel.universal_strong_orientation_condition(
            pair,
            descriptor,
        )
    )
    return tuple(sorted(rows, key=_incidence_sort_key))


@lru_cache(maxsize=1)
def failed_pairs() -> frozenset[Pair]:
    return frozenset(pair for pair, _descriptor in feasible_corrected_cut_failures())


@lru_cache(maxsize=1)
def no_failure_pairs() -> frozenset[Pair]:
    return remainder_pairs() - failed_pairs()


def signature_payload(
    rows: Iterable[Incidence] | None = None,
) -> list[dict[str, object]]:
    selected = feasible_corrected_cut_failures() if rows is None else rows
    payload: list[dict[str, object]] = []
    for pair, descriptor in sorted(selected, key=_incidence_sort_key):
        payload.append(
            {
                "pair": closure.pair_payload(pair),
                "partition": descriptor.partition,
                "active_mask": descriptor.active_mask,
                "caps": descriptor.caps,
                "weight": descriptor.weight,
                "profile": failure_profile(pair, descriptor),
                "ordered_linkage_kinds": linkage_kinds(pair, descriptor),
            }
        )
    return payload


def signature_fingerprint(*, sort_keys: bool = True) -> str:
    return _digest(signature_payload(), sort_keys=sort_keys)


def _profile_set_key(profiles: Iterable[str]) -> str:
    return "+".join(sorted(set(profiles)))


@lru_cache(maxsize=1)
def certificate() -> dict[str, object]:
    dependencies = dependency_sha256()
    residual = levelset.residual_pair_universe()
    removed = levelset_pairs()
    remainder = remainder_pairs()
    failures = feasible_corrected_cut_failures()
    failed = failed_pairs()
    no_failure = no_failure_pairs()

    profiles = Counter(failure_profile(pair, descriptor) for pair, descriptor in failures)
    active_counts = Counter(
        descriptor.active_mask.bit_count() for _pair, descriptor in failures
    )
    active_masks = Counter(descriptor.active_mask for _pair, descriptor in failures)
    two_active_kinds = Counter(
        tuple(sorted(linkage_kinds(pair, descriptor)))
        for pair, descriptor in failures
        if descriptor.active_mask.bit_count() == 2
    )
    by_pair: dict[Pair, list[str]] = defaultdict(list)
    for pair, descriptor in failures:
        by_pair[pair].append(failure_profile(pair, descriptor))
    pair_profile_sets = Counter(_profile_set_key(items) for items in by_pair.values())
    failure_count_per_pair = Counter(len(items) for items in by_pair.values())
    ranks_failed = Counter(len(closure.full_rows(*pair)) for pair in failed)
    ranks_no_failure = Counter(
        len(closure.full_rows(*pair)) for pair in no_failure
    )
    deficiencies_failed = Counter(
        closure.full_deficiency(*pair) for pair in failed
    )
    deficiencies_no_failure = Counter(
        closure.full_deficiency(*pair) for pair in no_failure
    )

    assert dependencies == EXPECTED_DEPENDENCY_SHA256
    assert len(residual) == 18_832
    assert len(removed) == 336
    assert removed <= residual
    assert len(remainder) == 18_496
    assert remainder | removed == residual
    assert not remainder & removed
    assert len(tier.tier_descriptors()) == 259
    assert len(failures) == 21_906
    assert len(failed) == 6_654
    assert len(no_failure) == 11_842
    assert failed | no_failure == remainder
    assert not failed & no_failure
    assert active_counts == {1: 18_822, 2: 3_084}
    assert active_masks == {
        0b001: 6_274,
        0b010: 6_274,
        0b100: 6_274,
        0b011: 1_028,
        0b101: 1_028,
        0b110: 1_028,
    }
    assert profiles == {"B/F0": 15_204, "B/B": 3_618, "AA": 3_084}
    assert two_active_kinds == {
        ("Q", "U"): 1_200,
        ("U", "U"): 996,
        ("C", "U"): 660,
        ("C", "Q"): 156,
        ("C", "C"): 72,
    }
    assert pair_profile_sets == {
        "B/B": 2_874,
        "B/F0": 1_818,
        "AA+B/F0": 1_428,
        "B/B+B/F0": 366,
        "AA+B/B+B/F0": 156,
        "AA": 12,
    }
    assert failure_count_per_pair == {
        1: 2_682,
        2: 204,
        3: 384,
        4: 708,
        5: 2_058,
        6: 444,
        7: 66,
        13: 96,
        14: 12,
    }
    assert ranks_failed == {1: 6, 2: 228, 3: 6_420}
    assert ranks_no_failure == {1: 48, 2: 198, 3: 11_596}
    assert deficiencies_failed == {1: 942, 2: 2_604, 3: 2_340, 4: 768}
    assert deficiencies_no_failure == {
        1: 930,
        2: 3_068,
        3: 4_146,
        4: 2_866,
        5: 832,
    }
    assert closure.pair_fingerprint(remainder) == EXPECTED_REMAINDER_PAIR_SHA256
    assert closure.pair_fingerprint(no_failure) == EXPECTED_NO_FAILURE_PAIR_SHA256
    assert closure.pair_fingerprint(failed) == EXPECTED_FAILED_PAIR_SHA256
    assert signature_fingerprint() == EXPECTED_SIGNATURE_SHA256
    assert (
        signature_fingerprint(sort_keys=False)
        == EXPECTED_SIGNATURE_CROSS_ENCODING_SHA256
    )

    return {
        "claim_scope": (
            "finite support/descriptor identity only; no orientation, rate, "
            "population, history, communicating-class, or recurrence claim"
        ),
        "dependency_sha256": dependencies,
        "strict_invariant_residual_pairs": len(residual),
        "removed_levelset_pairs": len(removed),
        "remaining_pairs": len(remainder),
        "remaining_pair_sha256": closure.pair_fingerprint(remainder),
        "tier_descriptors": len(tier.tier_descriptors()),
        "feasible_corrected_cut_failure_rows": len(failures),
        "pairs_with_failure": len(failed),
        "pairs_with_no_failure": len(no_failure),
        "failed_pair_sha256": closure.pair_fingerprint(failed),
        "no_failure_pair_sha256": closure.pair_fingerprint(no_failure),
        "failure_signature_sha256": signature_fingerprint(),
        "failure_signature_cross_encoding_sha256": signature_fingerprint(
            sort_keys=False
        ),
        "failure_profile_histogram": dict(sorted(profiles.items())),
        "failure_active_count_histogram": dict(sorted(active_counts.items())),
        "failure_active_mask_histogram": {
            str(mask): count for mask, count in sorted(active_masks.items())
        },
        "two_active_ordered_kind_histogram": {
            "/".join(kinds): count
            for kinds, count in sorted(two_active_kinds.items())
        },
        "failed_pair_profile_set_histogram": dict(
            sorted(pair_profile_sets.items())
        ),
        "failure_count_per_pair_histogram": dict(
            sorted(failure_count_per_pair.items())
        ),
        "failed_pair_stoichiometric_rank_histogram": dict(
            sorted(ranks_failed.items())
        ),
        "no_failure_pair_stoichiometric_rank_histogram": dict(
            sorted(ranks_no_failure.items())
        ),
        "failed_pair_full_deficiency_histogram": dict(
            sorted(deficiencies_failed.items())
        ),
        "no_failure_pair_full_deficiency_histogram": dict(
            sorted(deficiencies_no_failure.items())
        ),
        "orientation_rate_population_or_history_enumeration": False,
        "recurrence_claim": False,
    }


def main() -> None:
    print(json.dumps(certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
