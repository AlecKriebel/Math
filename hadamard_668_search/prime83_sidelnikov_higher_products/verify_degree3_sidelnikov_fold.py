#!/usr/bin/env python3
"""Exact degree-at-most-three Sidelnikov product audit at the prime-83 fold.

This is a deliberately scoped finite construction.  Put

    B_i = chi(2^i + 1),   Z_i = chi(2^i - 1),  i in Z/83,

where chi is the quadratic character of F_167.  Binary blocks are products
of at most three cyclic phases of B.  The one-zero block is a product of at
most three phases of B and copies of one common phase of Z; its unique zero
is translated to coordinate zero.

The script quotients binary products by common translation, applies the
universal inverse-pair orientation condition, and then performs the complete
41-coordinate integer PAF join.  It does not allow independent decimations
of the four blocks and it does not search arbitrary BS(84,83) sequences.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations
import json


FIELD_PRIME = 167
ORDER = 83
HALF = 41
TARGET_ENERGY = 334
ALL_BITS = (1 << ORDER) - 1


def character(value: int) -> int:
    value %= FIELD_PRIME
    if value == 0:
        return 0
    return 1 if pow(value, (FIELD_PRIME - 1) // 2, FIELD_PRIME) == 1 else -1


def negative_mask(values: tuple[int, ...]) -> int:
    return sum((value < 0) << index for index, value in enumerate(values))


def rotate_mask(mask: int, amount: int) -> int:
    """Cyclically shift the represented sequence by ``amount``."""

    amount %= ORDER
    if amount == 0:
        return mask
    return ((mask << amount) & ALL_BITS) | (mask >> (ORDER - amount))


POWERS = tuple(pow(2, index, FIELD_PRIME) for index in range(ORDER))
BINARY_BASE_VALUES = tuple(character(value + 1) for value in POWERS)
ZERO_BASE_VALUES = tuple(character(value - 1) for value in POWERS)
BINARY_BASE_MASK = negative_mask(BINARY_BASE_VALUES)
ZERO_BASE_MASK = negative_mask(ZERO_BASE_VALUES)
BINARY_PHASE_MASKS = tuple(
    rotate_mask(BINARY_BASE_MASK, phase) for phase in range(ORDER)
)


def canonical_translate(indices: tuple[int, ...]) -> tuple[int, ...]:
    """Canonicalize a nonempty subset of Z/83 under translation."""

    if not indices:
        return ()
    return min(
        tuple(sorted((index - anchor) % ORDER for index in indices))
        for anchor in indices
    )


def product_mask(indices: tuple[int, ...]) -> int:
    result = 0
    for index in indices:
        result ^= BINARY_PHASE_MASKS[index]
    return result


def binary_paf(mask: int) -> tuple[int, ...]:
    """Half periodic autocorrelation of a binary length-83 word."""

    return tuple(
        ORDER - 2 * (mask ^ rotate_mask(mask, lag)).bit_count()
        for lag in range(1, HALF + 1)
    )


def one_zero_paf(mask: int) -> tuple[int, ...]:
    """Half PAF when coordinate zero is 0 and all others are binary.

    The mask has coordinate zero cleared.  Filling that coordinate by +1
    gives a binary word F.  Removing its two incident products at lag k
    subtracts F_k+F_-k from PAF_F(k).
    """

    filled_paf = binary_paf(mask)
    result = []
    for lag, value in enumerate(filled_paf, start=1):
        positive = -1 if (mask >> lag) & 1 else 1
        negative = -1 if (mask >> (ORDER - lag)) & 1 else 1
        result.append(value - positive - negative)
    return tuple(result)


def orientation_signature(mask: int) -> int:
    """Encode equality/opposition on the 41 inverse pairs."""

    result = 0
    for lag in range(1, HALF + 1):
        unequal = ((mask >> lag) ^ (mask >> (ORDER - lag))) & 1
        if not unequal:
            result |= 1 << (lag - 1)
    return result


@dataclass(frozen=True)
class BinaryTemplate:
    factors: tuple[int, ...]
    mask: int
    paf: tuple[int, ...]
    row_sum: int


@dataclass(frozen=True)
class ZeroTemplate:
    kind: str
    factors: tuple[int, ...]
    mask: int
    paf: tuple[int, ...]
    row_sum: int


def binary_templates() -> tuple[BinaryTemplate, ...]:
    canonical_subsets: set[tuple[int, ...]] = {()}
    for size in (1, 2, 3):
        canonical_subsets.update(
            canonical_translate(indices)
            for indices in combinations(range(ORDER), size)
        )

    size_distribution = Counter(map(len, canonical_subsets))
    expected_distribution = Counter({0: 1, 1: 1, 2: 41, 3: 1107})
    if size_distribution != expected_distribution:
        raise AssertionError("binary translation-orbit count changed")

    result = []
    seen_masks: set[int] = set()
    for factors in sorted(canonical_subsets, key=lambda item: (len(item), item)):
        mask = product_mask(factors)
        if mask in seen_masks:
            raise AssertionError("two canonical binary products coincide")
        seen_masks.add(mask)
        result.append(
            BinaryTemplate(
                factors=factors,
                mask=mask,
                paf=binary_paf(mask),
                row_sum=ORDER - 2 * mask.bit_count(),
            )
        )
    if len(result) != 1150:
        raise AssertionError("binary template count changed")
    return tuple(result)


def zero_templates() -> tuple[ZeroTemplate, ...]:
    """Return every anchored one-zero product of total degree at most three.

    Repeated B factors cancel because B^2=1.  All Z factors must have the
    same phase or the product has multiple zeros.  The distinct possibilities
    are

        Z B_E,   |E| <= 2,
        Z^2 B_E, |E| <= 1.
    """

    result = []
    seen_masks: set[int] = set()
    for z_parity, maximum_size, kind in ((1, 2, "Z"), (0, 1, "Z2")):
        for size in range(maximum_size + 1):
            for factors in combinations(range(ORDER), size):
                mask = ZERO_BASE_MASK if z_parity else 0
                mask ^= product_mask(factors)
                mask &= ~1  # the anchored value is zero, never a sign
                if mask in seen_masks:
                    raise AssertionError("two anchored one-zero products coincide")
                seen_masks.add(mask)
                result.append(
                    ZeroTemplate(
                        kind=kind,
                        factors=factors,
                        mask=mask,
                        paf=one_zero_paf(mask),
                        row_sum=82 - 2 * mask.bit_count(),
                    )
                )
    if len(result) != 3571:
        raise AssertionError("one-zero template count changed")
    return tuple(result)


def pair_catalog(
    binary: tuple[BinaryTemplate, ...],
) -> tuple[
    dict[tuple[int, tuple[int, ...]], int],
    dict[tuple[int, tuple[int, ...]], tuple[int, int]],
    set[int],
    int,
]:
    """Build the complete unordered C/D norm-and-PAF signature catalog."""

    multiplicities: Counter[tuple[int, tuple[int, ...]]] = Counter()
    witnesses: dict[tuple[int, tuple[int, ...]], tuple[int, int]] = {}
    norms: set[int] = set()
    admissible_states = 0
    for left_index, left in enumerate(binary):
        for right_index in range(left_index, len(binary)):
            right = binary[right_index]
            norm = left.row_sum**2 + right.row_sum**2
            if norm > TARGET_ENERGY:
                continue
            signature = tuple(
                left_value + right_value
                for left_value, right_value in zip(left.paf, right.paf)
            )
            key = (norm, signature)
            multiplicities[key] += 1
            witnesses.setdefault(key, (left_index, right_index))
            norms.add(norm)
            admissible_states += 1
    return dict(multiplicities), witnesses, norms, admissible_states


def audit() -> dict[str, object]:
    if (
        sum(BINARY_BASE_VALUES),
        sum(ZERO_BASE_VALUES),
        ZERO_BASE_VALUES.count(0),
    ) != (-1, 0, 1):
        raise AssertionError("base Sidelnikov fingerprints changed")
    if ZERO_BASE_VALUES[0] != 0:
        raise AssertionError("the one-zero phase is not anchored")

    binary = binary_templates()
    zero = zero_templates()

    v_by_orientation: defaultdict[
        int, list[tuple[int, int, int]]
    ] = defaultdict(list)
    for template_index, item in enumerate(binary):
        for phase in range(ORDER):
            shifted_mask = rotate_mask(item.mask, phase)
            v_by_orientation[orientation_signature(shifted_mask)].append(
                (template_index, phase, shifted_mask)
            )

    u_orientation_counts = Counter(
        orientation_signature(item.mask) for item in zero
    )
    v_orientation_counts = Counter(
        {
            signature: len(states)
            for signature, states in v_by_orientation.items()
        }
    )
    intersection = set(u_orientation_counts).intersection(v_orientation_counts)
    intersecting_u_indices = [
        index
        for index, item in enumerate(zero)
        if orientation_signature(item.mask) in intersection
    ]
    if any(zero[index].kind != "Z2" for index in intersecting_u_indices):
        raise AssertionError("an odd-Z template passed the orientation gate")

    (
        pair_multiplicities,
        pair_witnesses,
        pair_norms,
        admissible_pair_states,
    ) = pair_catalog(binary)

    raw_uv_states = len(zero) * len(binary) * ORDER * 2
    orientation_compatible = 0
    row_compatible = 0
    parity_compatible = 0
    uv_signature_hits = 0
    prime_fold_objects = 0
    remainder_distribution: Counter[int] = Counter()
    uv_abs_profile_distribution: Counter[tuple[int, int]] = Counter()

    for u in zero:
        states = v_by_orientation.get(orientation_signature(u.mask), ())
        orientation_compatible += 2 * len(states)
        for template_index, _phase, shifted_mask in states:
            v_base = binary[template_index]
            for sign in (-1, 1):
                origin = sign * (-1 if shifted_mask & 1 else 1)
                delta = 2 - origin
                v_sum = sign * v_base.row_sum + delta
                remaining_norm = (
                    TARGET_ENERGY - u.row_sum**2 - v_sum**2
                )
                if remaining_norm not in pair_norms:
                    continue

                row_compatible += 1
                remainder_distribution[remaining_norm] += 1
                uv_abs_profile_distribution[(abs(u.row_sum), abs(v_sum))] += 1

                v_paf = []
                for lag in range(1, HALF + 1):
                    positive = sign * (
                        -1 if (shifted_mask >> lag) & 1 else 1
                    )
                    negative = sign * (
                        -1
                        if (shifted_mask >> (ORDER - lag)) & 1
                        else 1
                    )
                    v_paf.append(
                        v_base.paf[lag - 1] + delta * (positive + negative)
                    )
                needed = tuple(
                    -u_value - v_value
                    for u_value, v_value in zip(u.paf, v_paf)
                )
                if all(value % 4 == 2 for value in needed):
                    parity_compatible += 1
                key = (remaining_norm, needed)
                if key not in pair_witnesses:
                    continue
                uv_signature_hits += 1
                prime_fold_objects += pair_multiplicities[key]

    result: dict[str, object] = {
        "family": "un-decimated degree-at-most-three Sidelnikov products",
        "field_prime": FIELD_PRIME,
        "fold_order": ORDER,
        "binary_translation_orbits": len(binary),
        "binary_orbits_by_factor_count": {
            "0": 1,
            "1": 1,
            "2": 41,
            "3": 1107,
        },
        "one_zero_anchored_templates": len(zero),
        "one_zero_odd_Z_templates": 3487,
        "one_zero_even_Z_templates": 84,
        "u_orientation_signatures": len(u_orientation_counts),
        "v_orientation_signatures": len(v_orientation_counts),
        "orientation_signature_intersection": len(intersection),
        "orientation_intersecting_u_templates": len(intersecting_u_indices),
        "orientation_intersecting_u_odd_Z_templates": 0,
        "orientation_intersecting_v_phase_states": sum(
            v_orientation_counts[signature] for signature in intersection
        ),
        "raw_labeled_uv_states": raw_uv_states,
        "orientation_compatible_labeled_uv_states": orientation_compatible,
        "all_unordered_cd_template_pairs": len(binary) * (len(binary) + 1) // 2,
        "norm_admissible_cd_template_pairs": admissible_pair_states,
        "distinct_norm_paf_cd_keys": len(pair_multiplicities),
        "distinct_cd_norms": len(pair_norms),
        "row_compatible_uv_states": row_compatible,
        "mod4_compatible_uv_states": parity_compatible,
        "remainder_norm_distribution": {
            str(key): value
            for key, value in sorted(remainder_distribution.items())
        },
        "uv_abs_profile_distribution": {
            f"{key[0]},{key[1]}": value
            for key, value in sorted(uv_abs_profile_distribution.items())
        },
        "uv_states_with_exact_cd_signature": uv_signature_hits,
        "prime_fold_objects": prime_fold_objects,
        "mod84_lifts_tested": 0,
        "hadamard_candidates": 0,
    }

    expected = {
        "binary_translation_orbits": 1150,
        "one_zero_anchored_templates": 3571,
        "u_orientation_signatures": 904,
        "v_orientation_signatures": 11522,
        "orientation_signature_intersection": 42,
        "orientation_intersecting_u_templates": 84,
        "orientation_intersecting_v_phase_states": 3610,
        "raw_labeled_uv_states": 681_703_900,
        "orientation_compatible_labeled_uv_states": 14_440,
        "all_unordered_cd_template_pairs": 661_825,
        "norm_admissible_cd_template_pairs": 572_893,
        "distinct_norm_paf_cd_keys": 163_876,
        "distinct_cd_norms": 30,
        "row_compatible_uv_states": 6170,
        "mod4_compatible_uv_states": 6170,
        "uv_states_with_exact_cd_signature": 0,
        "prime_fold_objects": 0,
    }
    for key, value in expected.items():
        if result[key] != value:
            raise AssertionError(
                f"{key} changed: expected {value!r}, observed {result[key]!r}"
            )
    expected_remainders = {
        "10": 364,
        "74": 657,
        "234": 1372,
        "298": 1724,
        "314": 2053,
    }
    if result["remainder_norm_distribution"] != expected_remainders:
        raise AssertionError("remainder norm distribution changed")
    expected_profiles = {
        "0,6": 1724,
        "0,10": 1372,
        "0,18": 364,
        "2,4": 2053,
        "2,16": 657,
    }
    if result["uv_abs_profile_distribution"] != expected_profiles:
        raise AssertionError("U/V row profile distribution changed")
    return result


def main() -> None:
    result = audit()
    semantic = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"semantic_sha256={sha256(semantic.encode()).hexdigest()}")
    print("PASS exact degree-three Sidelnikov prime-fold exclusion")


if __name__ == "__main__":
    main()
