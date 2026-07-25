#!/usr/bin/env python3
"""Close the primitive-nonvanishing audit over all 84 shell-two images.

The exact profile classification uses

    C6 rotations x A-star x B-star

of order 24.  With the normalized zero column fixed, only the rotations and
B-star are physical labelled phase symmetries: B-star is induced by

    row r -> 3-r (mod 9),   column c -> -c (mod 37).

A-star does not preserve the normalized A zero word.  Therefore the 84
formal profile images split into ten orbits under the physical subgroup of
order 12.  They are represented by the five published representatives and
their five A-star images.

This verifier checks that exact orbit partition, the physical profile
transport, the primitive-factor permutation, and the 90 exact MITM records
needed to prove individual-channel nonvanishing on all six factors for all
84 images.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
if str(SEARCH_ROOT) not in sys.path:
    sys.path.insert(0, str(SEARCH_ROOT))

from verify_lp333_order3_char37_transfer import PROFILES  # noqa: E402
from verify_lp333_order3_labeled_jet import (  # noqa: E402
    ZERO_A_PLUS,
    ZERO_B_PLUS,
)
from verify_lp333_order3_profile9 import actual_profile_counts  # noqa: E402


P = 167
N = 37
ROTATION_MULTIPLIER = 4

Identifiers = tuple[int, ...]
ProfilePair = tuple[Identifiers, Identifiers]


def compact_hash(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()


PROFILE_TO_ID = {
    tuple(profile): index for index, profile in enumerate(PROFILES)
}
CONJUGATE_ID = tuple(
    PROFILE_TO_ID[(profile[0], profile[2], profile[1])]
    for profile in PROFILES
)


def transform_identifiers(
    identifiers: Sequence[int],
    rotation: int,
    star: bool,
) -> Identifiers:
    """Replay the exact-classification action."""

    offset = (2 * rotation + (6 if star else 0)) % 12
    return tuple(
        CONJUGATE_ID[int(identifiers[(index + offset) % 12])]
        if star
        else int(identifiers[(index + offset) % 12])
        for index in range(12)
    )


def formal_image(
    profile: ProfilePair,
    rotation: int,
    star_a: bool,
    star_b: bool,
) -> ProfilePair:
    return (
        transform_identifiers(profile[0], rotation, star_a),
        transform_identifiers(profile[1], rotation, star_b),
    )


def physical_orbit(profile: ProfilePair) -> frozenset[ProfilePair]:
    return frozenset(
        formal_image(profile, rotation, False, star_b)
        for rotation in range(6)
        for star_b in (False, True)
    )


def affine_row_image(word: Sequence[int], sign: int, shift: int) -> tuple[int, ...]:
    """Pull a row word back by r -> sign*r+shift."""

    return tuple(
        int(word[(sign * row + shift) % 9])
        for row in range(9)
    )


def physical_counts(
    channel: int,
    identifiers: Sequence[int],
) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        actual_profile_counts(
            channel,
            class_index,
            PROFILES[int(profile_id)],
        )
        for class_index, profile_id in enumerate(identifiers)
    )


def audit_physical_transport(seeds: Sequence[ProfilePair]) -> None:
    """Check rotations and B-star on the actual complement-convention data."""

    for seed in seeds:
        counts_a = physical_counts(0, seed[0])
        counts_b = physical_counts(1, seed[1])
        for rotation in range(6):
            offset = 2 * rotation
            rotated = formal_image(seed, rotation, False, False)
            if physical_counts(0, rotated[0]) != tuple(
                counts_a[(index + offset) % 12] for index in range(12)
            ):
                raise AssertionError("A rotation lost the physical profile counts")
            if physical_counts(1, rotated[1]) != tuple(
                counts_b[(index + offset) % 12] for index in range(12)
            ):
                raise AssertionError("B rotation lost the physical profile counts")

            reflected = formal_image(seed, rotation, False, True)
            expected_b = tuple(
                (
                    counts_b[(index + offset + 6) % 12][0],
                    counts_b[(index + offset + 6) % 12][2],
                    counts_b[(index + offset + 6) % 12][1],
                )
                for index in range(12)
            )
            if physical_counts(1, reflected[1]) != expected_b:
                raise AssertionError("B-star lost the physical profile counts")


def primitive_q_orbits() -> tuple[tuple[int, ...], ...]:
    q = pow(P, 6, N)
    if q != 11 or pow(q, 2, N) != 10:
        raise AssertionError("the pinned q/H arithmetic changed")
    unseen = set(range(1, N))
    result = []
    while unseen:
        start = min(unseen)
        orbit = tuple(start * pow(q, exponent, N) % N for exponent in range(6))
        if len(set(orbit)) != 6 or not set(orbit) <= unseen:
            raise AssertionError("primitive q-orbits overlap")
        unseen.difference_update(orbit)
        result.append(orbit)
    if len(result) != 6 or unseen:
        raise AssertionError("primitive q-orbits do not partition C_37^*")
    return tuple(result)


def factor_permutations(
    q_orbits: Sequence[Sequence[int]],
) -> tuple[dict[str, object], ...]:
    factor_of = {
        exponent: factor_index
        for factor_index, orbit in enumerate(q_orbits)
        for exponent in orbit
    }
    # With the repository's pullback convention, a rotation has
    # W'_k=W_(4^s k), hence evaluation exponent multiplier 4^(-s).
    # B-star has W'_k=omega*W_(-4^s k)^(p^3), hence multiplier
    # -p^(-3)4^(-s) before the coefficient p^3 Frobenius.
    inverse_p_cubed = pow(pow(P, 3, N), -1, N)
    if any(
        (3 - row) % 9 != (3 + row * pow(P, 3, 9)) % 9
        for row in range(9)
    ):
        raise AssertionError("the B-star ninth-root Frobenius identity changed")
    actions = tuple(
        (
            action,
            rotation,
            (
                pow(ROTATION_MULTIPLIER, -rotation, N)
                if action == "rotation"
                else (
                    -inverse_p_cubed
                    * pow(ROTATION_MULTIPLIER, -rotation, N)
                )
                % N
            ),
        )
        for action in ("rotation", "b_star")
        for rotation in range(6)
    )
    permutations = []
    for action, rotation, multiplier in actions:
        column_pullback = (
            pow(ROTATION_MULTIPLIER, rotation, N)
            if action == "rotation"
            else (-pow(ROTATION_MULTIPLIER, rotation, N)) % N
        )
        coefficient_frobenius = 1 if action == "rotation" else pow(P, 3, N)
        if (
            multiplier
            * coefficient_frobenius
            * column_pullback
        ) % N != 1:
            raise AssertionError("the physical evaluation multiplier changed")
        permutation = tuple(
            factor_of[int(orbit[0]) * multiplier % N]
            for orbit in q_orbits
        )
        if sorted(permutation) != list(range(6)):
            raise AssertionError("a physical action failed to permute factors")
        for source, target in enumerate(permutation):
            mapped = {
                exponent * multiplier % N for exponent in q_orbits[source]
            }
            if mapped != set(q_orbits[target]):
                raise AssertionError("a q-orbit factor map was not exact")
        permutations.append(
            {
                "action": action,
                "rotation": rotation,
                "evaluation_exponent_multiplier": multiplier,
                "factor_permutation": permutation,
            }
        )
    return tuple(permutations)


def audit_record_semantics(record: dict[str, object]) -> None:
    semantic = {
        key: value
        for key, value in record.items()
        if key != "semantic_sha256"
    }
    if compact_hash(semantic) != record["semantic_sha256"]:
        raise AssertionError("an individual audit semantic hash changed")
    if (
        int(record["primitive_zero_assignments"]) != 0
        or record["direct_crt_formula_checked"] is not True
        or record["direct_prefix_mitm_checked"] is not True
    ):
        raise AssertionError("an exact primitive audit is not a proved zero count")


def load_audits(path: Path) -> tuple[dict[str, object], ...]:
    payload = json.loads(path.read_text())
    audits = tuple(payload["audits"])
    if int(payload["summary"]["channel_factor_audits"]) != len(audits):
        raise AssertionError("an audit certificate has the wrong record count")
    if sum(int(record["primitive_zero_assignments"]) for record in audits):
        raise AssertionError("an audit certificate contains a primitive zero")
    if compact_hash(audits) != payload["summary"]["semantic_sha256"]:
        raise AssertionError("an audit certificate semantic hash changed")
    for record in audits:
        audit_record_semantics(record)
    return audits


def index_audits(
    audits: Iterable[dict[str, object]],
) -> dict[tuple[str, str, int], dict[str, object]]:
    result: dict[tuple[str, str, int], dict[str, object]] = {}
    for record in audits:
        key = (
            str(record["label"]),
            str(record["channel"]),
            int(record["primitive_factor"]),
        )
        if key in result:
            raise AssertionError("duplicate channel/factor audit")
        result[key] = record
    return result


def verify_record_profile(
    record: dict[str, object],
    channel: int,
    identifiers: Sequence[int],
) -> None:
    if tuple(int(value) for value in record["profile_ids"]) != tuple(identifiers):
        raise AssertionError("an audit record has the wrong profile IDs")
    expected_counts = physical_counts(channel, identifiers)
    stored_counts = tuple(
        tuple(int(value) for value in profile)
        for profile in record["physical_profile_counts"]
    )
    if stored_counts != expected_counts:
        raise AssertionError("an audit record has the wrong physical profiles")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    classification_path = (
        SEARCH_ROOT
        / "shell_two_exact"
        / "shell_two_exact_orbits_certificate.json"
    )
    classification = json.loads(classification_path.read_text())
    representatives = tuple(
        (
            str(record["label"]),
            (
                tuple(int(value) for value in record["profile_ids_a"]),
                tuple(int(value) for value in record["profile_ids_b"]),
            ),
        )
        for record in classification["orbits"]
    )
    if len(representatives) != 5:
        raise AssertionError("the shell-two classification no longer has five orbits")

    formal_images = frozenset(
        formal_image(profile, rotation, star_a, star_b)
        for _, profile in representatives
        for rotation in range(6)
        for star_a in (False, True)
        for star_b in (False, True)
    )
    if (
        len(formal_images) != int(classification["raw_orbit_members"])
        or len(formal_images) != 84
    ):
        raise AssertionError("the formal shell-two action no longer has 84 images")

    canonical_seeds = tuple(profile for _, profile in representatives)
    astar_seeds = tuple(
        formal_image(profile, 0, True, False)
        for profile in canonical_seeds
    )
    lift_orbits = tuple(
        physical_orbit(seed)
        for seed in (*canonical_seeds, *astar_seeds)
    )
    distinct_lift_orbits = frozenset(lift_orbits)
    if len(distinct_lift_orbits) != 10:
        raise AssertionError("the 84 images did not split into ten lift orbits")
    for first_index, first in enumerate(lift_orbits):
        for second in lift_orbits[first_index + 1 :]:
            if first & second:
                raise AssertionError("two physical lift orbits overlap")
    if frozenset().union(*lift_orbits) != formal_images:
        raise AssertionError("the ten physical lift orbits do not cover all 84 images")
    lift_orbit_sizes = tuple(len(orbit) for orbit in lift_orbits)
    if sum(lift_orbit_sizes) != 84:
        raise AssertionError("the physical orbit sizes do not sum to 84")

    affine_stabilizers = []
    for word in (ZERO_A_PLUS, ZERO_B_PLUS):
        stabilizers = tuple(
            (sign, shift)
            for sign in (1, -1)
            for shift in range(9)
            if affine_row_image(word, sign, shift) == tuple(word)
        )
        affine_stabilizers.append(stabilizers)
    if affine_stabilizers[0] != ((1, 0),):
        raise AssertionError("the normalized A zero word gained a row symmetry")
    if affine_stabilizers[1] != ((1, 0), (-1, 3)):
        raise AssertionError("the normalized B zero-word stabilizer changed")

    audit_physical_transport((*canonical_seeds, *astar_seeds))
    q_orbits = primitive_q_orbits()
    factor_maps = factor_permutations(q_orbits)
    primitive_field_size = P**12
    # Once both channels are units in all six primitive factors, put
    # R=W_B/W_A.  In each star-paired factor equation,
    #
    #   1 + R_r R_(r+3)^(p^3) = 0,
    #
    # so R_(r+3)=(-R_r^(-1))^(p^9).  The first three nonzero
    # coordinates are free, and p^9 is inverse to p^3 on F_(p^12).
    if (3 + 9) % 12:
        raise AssertionError("the ratio-torus Frobenius exponents changed")
    unit_ratio_torus_points = (primitive_field_size - 1) ** 3
    primitive_unit_cone_points = (primitive_field_size - 1) ** 9

    canonical_audits = (
        *load_audits(HERE / "h2_factors_0_2_certificate.json"),
        *load_audits(HERE / "h2_factors_3_5_certificate.json"),
    )
    astar_audits = load_audits(
        HERE / "h2_astar_a_all_factors_certificate.json"
    )
    indexed = index_audits((*canonical_audits, *astar_audits))
    if len(indexed) != 90:
        raise AssertionError("the action closure requires exactly 90 base audits")

    for label, profile in representatives:
        for channel, identifiers in enumerate(profile):
            for factor in range(6):
                record = indexed[(label, "AB"[channel], factor)]
                verify_record_profile(record, channel, identifiers)
        astar = formal_image(profile, 0, True, False)
        for factor in range(6):
            record = indexed[(f"{label}-Astar", "A", factor)]
            verify_record_profile(record, 0, astar[0])
            # The A-star seed has unchanged B data, so its six B audits are
            # exactly the already checked canonical B records.
            verify_record_profile(indexed[(label, "B", factor)], 1, astar[1])

    semantic = {
        "schema": "lp333-shell-two-primitive-nonvanishing-action-closure-v1",
        "formal_profile_images": len(formal_images),
        "formal_group_order": 24,
        "physical_lift_group_order": 12,
        "physical_lift_orbits": len(distinct_lift_orbits),
        "physical_lift_orbit_sizes": lift_orbit_sizes,
        "base_channel_factor_audits": len(indexed),
        "primitive_zero_assignments": 0,
        "all_six_primitive_factors_nonzero_per_channel": True,
        "a_zero_word_affine_stabilizer": affine_stabilizers[0],
        "b_zero_word_affine_stabilizer": affine_stabilizers[1],
        "primitive_q_orbits": q_orbits,
        "physical_factor_permutations": factor_maps,
        "primitive_factor_field_size": primitive_field_size,
        "ratio_partner_frobenius_exponent": P**9,
        "primitive_unit_ratio_torus_points": unit_ratio_torus_points,
        "primitive_unit_cone_points": primitive_unit_cone_points,
    }
    result = {
        **semantic,
        "semantic_sha256": compact_hash(semantic),
    }
    if args.output is not None:
        args.output.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n"
        )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
