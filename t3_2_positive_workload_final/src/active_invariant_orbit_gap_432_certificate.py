"""Finite certificate for the 432-pair active-invariant orbit gap.

This module certifies support-orbit, tier, affine-feasibility, and literal
one-active category identities only.  It does not enumerate reaction
orientations, rate vectors, population states, or stochastic histories, and
it makes no recurrence claim.  The analytic common-potential theorem is a
separate dependency.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import permutations
import json
from math import gcd, lcm
from pathlib import Path
from typing import Iterable

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import s_tier_superlevel_interface as superlevel
import stoichiometric_gate_feasibility as feasibility


Pair = closure.Pair
Descriptor = tier.TierDescriptor
Incidence = tuple[Pair, Descriptor]
Mask = int

VECTOR_TO_NODE = {
    vector: node for node, vector in enumerate(closure.COMPLEXES)
}

EXPECTED_DEPENDENCY_SHA256 = {
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

EXPECTED_GAP_PAIR_SHA256 = (
    "5516d6071b2b9d07b0e4e02613b9caee217ba3ebb0082e21f2bc664e6247ea36"
)
EXPECTED_FAILURE_ROW_SHA256 = (
    "cad3bdf8e900cbb6f978e11d30e28bba7a7a57de055d9b9787f7dd53fbc91615"
)
EXPECTED_ANNOTATED_FAILURE_ROW_SHA256 = (
    "57dcf4af1250ee72a0658bdf5ec930e01ab657b77d739ba211dc12ef6e4ddae8"
)
EXPECTED_FAILED_PAIR_SHA256 = (
    "a50db5ec6e22275e3818a2a95991d4ea5df136a53974259ec539667ca13dd6bc"
)
EXPECTED_NO_FAILURE_PAIR_SHA256 = (
    "5ea33717ca9a6667d3cf12e77510e689f92c8314d07225d783880df420cc613c"
)
EXPECTED_INVARIANT_MANIFEST_SHA256 = (
    "9dec8108276e9d439c18aacda1ec35d9bac08e097f8833e3446c50b40d8148ca"
)
EXPECTED_ALIGNED_FAILURE_ROW_SHA256 = (
    "a9368dd934b7ac6135c3df4866e2322700d3a607dd58f8327aeb709065880ab2"
)
EXPECTED_NON_DZ_FAILED_PAIR_SHA256 = (
    "051a641f3987ec93b129ad044d96292a97e536e9ef3d2724234dc4af9bfdef69"
)

TYPE_I_REPRESENTATIVE = (
    closure.mask(("A", "AB")),
    closure.mask(("2A", "2C", "AC")),
)
TYPE_II_REPRESENTATIVE = (
    closure.mask(("A", "AB")),
    closure.mask(("C", "2A", "BC")),
)
EXPECTED_TYPE_I_ORBIT_SHA256 = (
    "50804d58a48bb1a2683014442a436761ec0ba0df34af3ef3ac0d1939fe850886"
)
EXPECTED_TYPE_II_ORBIT_SHA256 = (
    "cc76d3c7bcc7942f956f1efc8cf0f718ad1e6e08d911f8f8127ebc3cf8c5002f"
)


def _digest(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
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


def _permuted_mask(
    mask: Mask,
    permutation: tuple[int, int, int],
) -> Mask:
    """Relabel a support by one species permutation."""

    image = 0
    for node in _nodes(mask):
        vector = closure.COMPLEXES[node]
        permuted = tuple(
            vector[permutation[coordinate]] for coordinate in range(3)
        )
        image |= 1 << VECTOR_TO_NODE[permuted]
    return image


def pair_orbit(pairs: Iterable[Pair]) -> frozenset[Pair]:
    """Close ordered support pairs under S3 and linkage reversal."""

    result: set[Pair] = set()
    for first, second in pairs:
        for permutation in permutations(range(3)):
            image = (
                _permuted_mask(first, permutation),
                _permuted_mask(second, permutation),
            )
            result.add(image)
            result.add((image[1], image[0]))
    return frozenset(result)


@lru_cache(maxsize=1)
def positive_seed_pairs() -> frozenset[Pair]:
    return closure.unique_pairs(closure.POSITIVE_SHIELDED_MASKS)


@lru_cache(maxsize=1)
def signed_seed_pairs() -> frozenset[Pair]:
    return closure.unique_pairs(closure.SIGNED_SHIELDED_MASKS)


@lru_cache(maxsize=1)
def inherited_seed_pairs() -> frozenset[Pair]:
    return positive_seed_pairs() | signed_seed_pairs()


@lru_cache(maxsize=1)
def active_invariant_seed_pairs() -> frozenset[Pair]:
    return frozenset(
        pair
        for pair in inherited_seed_pairs()
        if closure.branch(pair) == "common_active_invariant"
    )


@lru_cache(maxsize=1)
def active_invariant_orbit() -> frozenset[Pair]:
    return pair_orbit(active_invariant_seed_pairs())


@lru_cache(maxsize=1)
def other_seed_orbit() -> frozenset[Pair]:
    seeds = inherited_seed_pairs()
    return pair_orbit(seeds - active_invariant_seed_pairs())


@lru_cache(maxsize=1)
def exclusive_orbit_gap_pairs() -> frozenset[Pair]:
    """The active-invariant orbit points absent from every other seed orbit."""

    return active_invariant_orbit() - other_seed_orbit()


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
    """All feasible descriptor rows which fail the corrected tier cut."""

    rows = (
        (pair, descriptor)
        for pair in exclusive_orbit_gap_pairs()
        for descriptor in tier.tier_descriptors()
        if feasibility.descriptor_feasible(pair, descriptor)
        and not superlevel.universal_strong_orientation_condition(
            pair,
            descriptor,
        )
    )
    return tuple(sorted(rows, key=_incidence_sort_key))


def one_active_category(mask: Mask, descriptor: Descriptor) -> str:
    """Return the literal Q/F0/F1/B/D support category.

    For the unique active coordinate X: Q contains 2X-degree; F0 and F1 are
    constant X-degree zero and one; B has a top degree-one complex q and a
    lower degree-zero complex c with q no larger than c in both inactive
    coordinates; D is the remaining dormant shape.
    """

    active = tuple(
        coordinate
        for coordinate in range(3)
        if descriptor.active_mask >> coordinate & 1
    )
    if len(active) != 1:
        raise ValueError("the Q/F0/F1/B/D category requires one active coordinate")
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


def category_pair(pair: Pair, descriptor: Descriptor) -> tuple[str, str]:
    first, second = (
        one_active_category(mask, descriptor) for mask in pair
    )
    return tuple(sorted((first, second)))  # type: ignore[return-value]


def pair_manifest(pairs: Iterable[Pair]) -> list[dict[str, object]]:
    return [
        {
            "first": first,
            "second": second,
        }
        for first, second in sorted(
            (
                closure.pair_payload(pair)
                for pair in pairs
            ),
            key=lambda pair: (pair[0], pair[1]),
        )
    ]


def failure_row_payload(
    rows: Iterable[Incidence] | None = None,
    *,
    annotate_categories: bool,
) -> list[dict[str, object]]:
    selected = feasible_corrected_cut_failures() if rows is None else rows
    payload: list[dict[str, object]] = []
    for pair, descriptor in sorted(selected, key=_incidence_sort_key):
        row: dict[str, object] = {
            "pair": closure.pair_payload(pair),
            "weight": descriptor.weight,
            "caps": descriptor.caps,
            "active_mask": descriptor.active_mask,
        }
        if annotate_categories:
            row["categories"] = category_pair(pair, descriptor)
        payload.append(row)
    return payload


def failure_row_fingerprint(*, annotate_categories: bool) -> str:
    return _digest(
        failure_row_payload(annotate_categories=annotate_categories)
    )


def _primitive_integer(
    vector: tuple[Fraction, Fraction, Fraction],
) -> tuple[int, int, int]:
    denominator = 1
    for value in vector:
        denominator = lcm(denominator, value.denominator)
    integers = [int(value * denominator) for value in vector]
    common = 0
    for value in integers:
        common = gcd(common, abs(value))
    if not common:
        raise ValueError("zero vector has no primitive normalization")
    integers = [value // common for value in integers]
    first_nonzero = next(value for value in integers if value)
    if first_nonzero < 0:
        integers = [-value for value in integers]
    return integers[0], integers[1], integers[2]


@lru_cache(maxsize=None)
def primitive_invariant(pair: Pair) -> tuple[int, int, int]:
    """The canonical primitive generator of the rank-two invariant line."""

    rows = closure.full_rows(*pair)
    if len(rows) != 2:
        raise ValueError("the orbit-gap invariant is defined at rank two")
    first, second = rows
    normal = (
        first[1] * second[2] - first[2] * second[1],
        first[2] * second[0] - first[0] * second[2],
        first[0] * second[1] - first[1] * second[0],
    )
    return _primitive_integer(normal)


def invariant_zero_coordinate(pair: Pair) -> int:
    invariant = primitive_invariant(pair)
    zeros = tuple(index for index, value in enumerate(invariant) if not value)
    if len(zeros) != 1:
        raise ValueError("the orbit-gap invariant must have exactly one zero")
    return zeros[0]


def invariant_manifest(pairs: Iterable[Pair]) -> list[dict[str, object]]:
    return [
        {
            "pair": closure.pair_payload(pair),
            "stoichiometric_rank": len(closure.full_rows(*pair)),
            "primitive_invariant": primitive_invariant(pair),
            "zero_coordinate": invariant_zero_coordinate(pair),
        }
        for pair in sorted(pairs, key=closure.pair_payload)
    ]


def aligned_failure_manifest(
    rows: Iterable[Incidence] | None = None,
) -> list[dict[str, object]]:
    selected = feasible_corrected_cut_failures() if rows is None else rows
    return [
        {
            "pair": closure.pair_payload(pair),
            "weight": descriptor.weight,
            "caps": descriptor.caps,
            "active_mask": descriptor.active_mask,
            "primitive_invariant": primitive_invariant(pair),
            "zero_coordinate": invariant_zero_coordinate(pair),
        }
        for pair, descriptor in sorted(selected, key=_incidence_sort_key)
    ]


@lru_cache(maxsize=1)
def certificate() -> dict[str, object]:
    dependencies = dependency_sha256()
    positive = positive_seed_pairs()
    signed = signed_seed_pairs()
    seeds = inherited_seed_pairs()
    active_seeds = active_invariant_seed_pairs()
    active_orbit = active_invariant_orbit()
    other_orbit = other_seed_orbit()
    gap = exclusive_orbit_gap_pairs()
    failures = feasible_corrected_cut_failures()
    failed_pairs = frozenset(pair for pair, _descriptor in failures)
    no_failure_pairs = gap - failed_pairs

    categories = Counter(
        category_pair(pair, descriptor) for pair, descriptor in failures
    )
    active_masks = Counter(
        descriptor.active_mask for _pair, descriptor in failures
    )
    weights = Counter(descriptor.weight for _pair, descriptor in failures)
    caps = Counter(descriptor.caps for _pair, descriptor in failures)
    failure_count_by_pair = Counter(pair for pair, _descriptor in failures)
    deficiencies = Counter(
        closure.full_deficiency(*pair) for pair in gap
    )
    deficiency_failure_cross = Counter(
        (
            closure.full_deficiency(*pair) == 0,
            pair in failed_pairs,
        )
        for pair in gap
    )
    ranks = Counter(len(closure.full_rows(*pair)) for pair in gap)
    invariant_vectors = Counter(primitive_invariant(pair) for pair in gap)
    invariant_zeros = Counter(invariant_zero_coordinate(pair) for pair in gap)
    aligned_failures = Counter(
        (
            invariant_zero_coordinate(pair),
            next(
                coordinate
                for coordinate in range(3)
                if descriptor.active_mask >> coordinate & 1
            ),
        )
        for pair, descriptor in failures
    )
    non_dz_failed_pairs = frozenset(
        pair
        for pair in failed_pairs
        if closure.full_deficiency(*pair) != 0
    )
    type_i_orbit = pair_orbit((TYPE_I_REPRESENTATIVE,))
    type_ii_orbit = pair_orbit((TYPE_II_REPRESENTATIVE,))

    assert dependencies == EXPECTED_DEPENDENCY_SHA256
    assert len(positive) == 4_761
    assert len(signed) == 408
    assert not positive & signed
    assert len(seeds) == 5_169
    assert len(active_seeds) == 110
    assert len(active_orbit) == 714
    assert len(other_orbit) == 27_462
    assert len(active_orbit & other_orbit) == 282
    assert len(active_orbit | other_orbit) == 27_894
    assert len(gap) == 432
    assert closure.pair_fingerprint(gap) == EXPECTED_GAP_PAIR_SHA256
    assert len(tier.tier_descriptors()) == 259
    assert len(failures) == 192
    assert len(failed_pairs) == 72
    assert len(no_failure_pairs) == 360
    assert categories == {("B", "F0"): 180, ("B", "B"): 12}
    assert active_masks == {0b001: 64, 0b010: 64, 0b100: 64}
    assert weights == {(1, 0, 0): 64, (0, 1, 0): 64, (0, 0, 1): 64}
    assert Counter(failure_count_by_pair.values()) == {3: 60, 1: 12}
    assert deficiencies == {0: 174, 1: 192, 2: 60, 3: 6}
    assert deficiency_failure_cross == {
        (True, False): 126,
        (True, True): 48,
        (False, False): 234,
        (False, True): 24,
    }
    assert ranks == {2: 432}
    assert invariant_zeros == {0: 144, 1: 144, 2: 144}
    assert all(
        sum(value == 0 for value in invariant) == 1
        and sum(value > 0 for value in invariant) == 2
        for invariant in invariant_vectors
    )
    assert all(
        sum(invariant[index] * row[index] for index in range(3)) == 0
        for pair in gap
        for invariant in (primitive_invariant(pair),)
        for row in closure.full_rows(*pair)
    )
    assert aligned_failures == {(0, 0): 64, (1, 1): 64, (2, 2): 64}
    assert _digest(invariant_manifest(gap)) == EXPECTED_INVARIANT_MANIFEST_SHA256
    assert (
        _digest(aligned_failure_manifest())
        == EXPECTED_ALIGNED_FAILURE_ROW_SHA256
    )
    assert len(non_dz_failed_pairs) == 24
    assert (
        closure.pair_fingerprint(non_dz_failed_pairs)
        == EXPECTED_NON_DZ_FAILED_PAIR_SHA256
    )
    assert len(type_i_orbit) == len(type_ii_orbit) == 12
    assert not type_i_orbit & type_ii_orbit
    assert type_i_orbit | type_ii_orbit == non_dz_failed_pairs
    assert closure.pair_fingerprint(type_i_orbit) == EXPECTED_TYPE_I_ORBIT_SHA256
    assert closure.pair_fingerprint(type_ii_orbit) == EXPECTED_TYPE_II_ORBIT_SHA256
    assert not any(
        closure.has_strictly_positive_invariant(*pair) for pair in gap
    )
    assert (
        failure_row_fingerprint(annotate_categories=False)
        == EXPECTED_FAILURE_ROW_SHA256
    )
    assert (
        failure_row_fingerprint(annotate_categories=True)
        == EXPECTED_ANNOTATED_FAILURE_ROW_SHA256
    )
    assert closure.pair_fingerprint(failed_pairs) == EXPECTED_FAILED_PAIR_SHA256
    assert (
        closure.pair_fingerprint(no_failure_pairs)
        == EXPECTED_NO_FAILURE_PAIR_SHA256
    )

    return {
        "scope": (
            "finite support-orbit, corrected-tier, exact affine-feasibility, "
            "and one-active category identities only"
        ),
        "recurrence_claim": False,
        "orientation_rate_population_or_history_enumeration": False,
        "dependency_sha256": dependencies,
        "positive_seed_pairs": len(positive),
        "signed_seed_pairs": len(signed),
        "inherited_seed_pairs": len(seeds),
        "active_invariant_seed_pairs": len(active_seeds),
        "active_invariant_orbit_pairs": len(active_orbit),
        "other_seed_orbit_pairs": len(other_orbit),
        "orbit_overlap_pairs": len(active_orbit & other_orbit),
        "full_inherited_seed_orbit_pairs": len(active_orbit | other_orbit),
        "exclusive_orbit_gap_pairs": len(gap),
        "exclusive_orbit_gap_pair_sha256": closure.pair_fingerprint(gap),
        "gap_pair_manifest": pair_manifest(gap),
        "tier_descriptors": len(tier.tier_descriptors()),
        "pairs_with_no_feasible_corrected_cut_failure": len(no_failure_pairs),
        "pairs_with_feasible_corrected_cut_failure": len(failed_pairs),
        "no_failure_pair_sha256": closure.pair_fingerprint(no_failure_pairs),
        "failed_pair_sha256": closure.pair_fingerprint(failed_pairs),
        "no_failure_pair_manifest": pair_manifest(no_failure_pairs),
        "failed_pair_manifest": pair_manifest(failed_pairs),
        "feasible_corrected_cut_failure_rows": len(failures),
        "failure_category_histogram": {
            "/".join(key): value for key, value in sorted(categories.items())
        },
        "active_mask_histogram": {
            str(key): value for key, value in sorted(active_masks.items())
        },
        "weight_histogram": {
            ",".join(map(str, key)): value
            for key, value in sorted(weights.items())
        },
        "cap_histogram": {
            ",".join(map(str, key)): value
            for key, value in sorted(caps.items())
        },
        "failure_count_per_pair_histogram": {
            str(key): value
            for key, value in sorted(
                Counter(failure_count_by_pair.values()).items()
            )
        },
        "full_deficiency_histogram": {
            str(key): value for key, value in sorted(deficiencies.items())
        },
        "stoichiometric_rank_histogram": {
            str(key): value for key, value in sorted(ranks.items())
        },
        "primitive_invariant_histogram": {
            ",".join(map(str, key)): value
            for key, value in sorted(invariant_vectors.items())
        },
        "invariant_zero_coordinate_histogram": {
            str(key): value for key, value in sorted(invariant_zeros.items())
        },
        "failure_zero_active_alignment_histogram": {
            f"zero={zero},active={active}": value
            for (zero, active), value in sorted(aligned_failures.items())
        },
        "all_failure_active_coordinates_equal_invariant_zero": True,
        "invariant_manifest_sha256": _digest(invariant_manifest(gap)),
        "invariant_manifest": invariant_manifest(gap),
        "aligned_failure_row_sha256": _digest(aligned_failure_manifest()),
        "aligned_failure_rows": aligned_failure_manifest(),
        "non_deficiency_zero_failed_pairs": len(non_dz_failed_pairs),
        "non_deficiency_zero_failed_pair_sha256": closure.pair_fingerprint(
            non_dz_failed_pairs
        ),
        "non_deficiency_zero_failed_orbit_split": {
            "type_I": {
                "representative": closure.pair_payload(TYPE_I_REPRESENTATIVE),
                "pairs": len(type_i_orbit),
                "sha256": closure.pair_fingerprint(type_i_orbit),
            },
            "type_II": {
                "representative": closure.pair_payload(TYPE_II_REPRESENTATIVE),
                "pairs": len(type_ii_orbit),
                "sha256": closure.pair_fingerprint(type_ii_orbit),
            },
        },
        "deficiency_zero_failure_cross": {
            f"deficiency_zero={is_zero},failure={has_failure}": value
            for (is_zero, has_failure), value in sorted(
                deficiency_failure_cross.items()
            )
        },
        "strictly_positive_invariant_pairs": 0,
        "failure_row_sha256": failure_row_fingerprint(
            annotate_categories=False
        ),
        "annotated_failure_row_sha256": failure_row_fingerprint(
            annotate_categories=True
        ),
        "failure_rows": failure_row_payload(annotate_categories=True),
    }


def main() -> None:
    print(json.dumps(certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
