#!/usr/bin/env python3
"""Independent certificate for all exact h=2 order-three profile orbits."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SEARCH_ROOT))

from verify_shell_two_partition_theory import (  # noqa: E402
    PAIRS,
    PROFILES,
    TARGETS,
    actual_factor,
    add,
    all_correlations,
    profile_value,
    signed_skeleton,
    transform_identifiers,
    transform_skeleton,
)
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    audit_profile_witness,
    compact_hash as hensel_hash,
)
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    audit_profile_transfer,
    catalog_phase_sum_intersection,
)
from verify_lp333_order3_profile_zero_gate import (  # noqa: E402
    profile_zero_gate,
)


Candidate = tuple[
    str,
    tuple[int, ...],
    tuple[int, int, int, int],
    tuple[int, ...],
    tuple[int, ...],
]

CANDIDATES: tuple[Candidate, ...] = (
    (
        "h2-222222-0",
        (2, 2, 2, 2, 2, 2),
        (2, -2, -2, 2),
        (2, 5, 8, 1, 7, 9, 5, 8, 5, 5, 5, 7),
        (2, 5, 3, 6, 5, 5, 5, 4, 7, 5, 4, 7),
    ),
    (
        "h2-422220-0",
        (4, 2, 2, 2, 2, 0),
        (2, -2, -2, 2),
        (2, 5, 7, 8, 6, 5, 2, 5, 7, 8, 6, 5),
        (5, 8, 5, 0, 1, 5, 5, 8, 5, 0, 1, 5),
    ),
    (
        "h2-422220-1",
        (4, 2, 2, 2, 2, 0),
        (2, -2, -4, -2),
        (2, 8, 8, 5, 5, 5, 2, 8, 8, 5, 5, 5),
        (2, 5, 5, 4, 1, 3, 2, 5, 5, 4, 1, 3),
    ),
    (
        "h2-422220-2",
        (4, 2, 2, 2, 2, 0),
        (4, 2, -2, 2),
        (4, 9, 8, 5, 5, 5, 4, 9, 8, 5, 5, 5),
        (2, 7, 5, 1, 5, 6, 2, 7, 5, 1, 5, 6),
    ),
    (
        "h2-422220-3",
        (4, 2, 2, 2, 2, 0),
        (-3, 0, -3, -3),
        (8, 5, 4, 5, 9, 1, 6, 8, 5, 5, 2, 6),
        (2, 3, 5, 5, 1, 5, 1, 4, 7, 5, 5, 5),
    ),
)

# Fields are ordered as in ``Stats`` in the C++ verifier, followed by the
# number of modulo-27 near witnesses.
PARTITION_CENSUS = {
    "444000": (4320, 256, 704, 16896, 534, 10510722, 7572062, 4806,
               4554, 1, 230, 1, 4554, 0, 1),
    "442200": (466560, 20520, 50220, 1354320, 151440, 993597840,
               925439472, 1362960, 341206, 6, 10075, 5, 341206, 0, 6),
    "433200": (829440, 35520, 86520, 2344320, 263880, 1731316680,
               1597214354, 2374920, 591921, 2, 16148, 0, 591921, 0, 2),
    "422220": (3732480, 156880, 383520, 10354080, 3447950,
               7540666650, 7370986470, 31031550, 2590579, 17,
               71300, 7, 2590579, 4, 17),
    "333300": (61440, 2880, 7320, 190080, 21300, 139749300,
               117434712, 191700, 49152, 0, 1322, 0, 49152, 0, 0),
    "332220": (6635520, 277120, 677360, 18289920, 6097340,
               13334882580, 13021837904, 54876060, 4568708, 23,
               123446, 5, 4568708, 0, 23),
    "222222": (2985984, 124612, 304627, 8224392, 8224392,
               5995581768, 5934038318, 74019528, 2054918, 12,
               55848, 3, 2054918, 1, 12),
}
CENSUS_FIELDS = (
    "raw_skeletons",
    "canonical_skeletons",
    "skeleton_targets",
    "support_trials",
    "extendible_supports",
    "medium_records",
    "distinct_medium_records",
    "high_records",
    "mod9_survivors",
    "mod27_survivors",
    "cubic37_survivors",
    "mod27_cubic37_survivors",
    "exact_replays",
    "exact_survivors",
    "near_witnesses",
)

EXPECTED_SEMANTIC_SHA256 = (
    "36099444b32f88869557a6f510f06cfa3b6eaa7a876b26cf62a0796ca4232565"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def values_from_ids(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    result = [[(-1, 0)] + [(0, 0)] * 12,
              [(2, 0)] + [(0, 0)] * 12]
    for channel, identifiers in enumerate(
        (identifiers_a, identifiers_b)
    ):
        for class_index, identifier in enumerate(identifiers):
            value = profile_value(identifier)
            factor = actual_factor(channel, class_index)
            result[channel][class_index + 1] = (
                factor * value[0],
                factor * value[1],
            )
    return tuple(result[0]), tuple(result[1])


def full_orbit(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> frozenset[tuple[tuple[int, ...], tuple[int, ...]]]:
    result = []
    for group in range(24):
        rotation = group // 4
        star_a = bool((group // 2) % 2)
        star_b = bool(group % 2)
        result.append((
            transform_identifiers(identifiers_a, rotation, star_a),
            transform_identifiers(identifiers_b, rotation, star_b),
        ))
    return frozenset(result)


def one_orbit_certificate(
    index: int,
    candidate: Candidate,
) -> dict[str, object]:
    label, expected_partition, target, identifiers_a, identifiers_b = candidate
    if target not in TARGETS:
        raise AssertionError("candidate has an unknown aggregate target")
    values = values_from_ids(identifiers_a, identifiers_b)
    physical = all_correlations(values)
    if physical[0] != (167, 0) or any(
        value != (0, 0) for value in physical[1:]
    ):
        raise AssertionError(f"{label} failed detached physical replay")

    aggregate = []
    for channel in range(2):
        total = (0, 0)
        for value in values[channel][1:]:
            total = add(total, value)
        aggregate.extend(total)
    if tuple(aggregate) != target:
        raise AssertionError(f"{label} aggregate changed")

    skeleton = (
        signed_skeleton(identifiers_a),
        signed_skeleton(identifiers_b),
    )
    local_states = tuple(
        (
            skeleton[0][pair],
            skeleton[0][pair + 6],
            skeleton[1][pair],
            skeleton[1][pair + 6],
        )
        for pair in range(PAIRS)
    )
    partition = tuple(sorted(
        (sum(value != 0 for value in state) for state in local_states),
        reverse=True,
    ))
    if partition != expected_partition:
        raise AssertionError(f"{label} partition changed")
    for state in local_states:
        if (state[1] - state[0] - state[3] + state[2]) % 3:
            raise AssertionError(f"{label} failed a local signature")

    skeleton_images = frozenset(
        transform_skeleton(skeleton, group) for group in range(24)
    )
    if min(skeleton_images) != skeleton:
        raise AssertionError(f"{label} skeleton is not canonical")
    orbit = full_orbit(identifiers_a, identifiers_b)
    skeleton_stabilizer = 24 // len(skeleton_images)
    stabilizer = 24 // len(orbit)
    if skeleton_stabilizer != stabilizer:
        raise AssertionError(
            f"{label} orbit meets its canonical skeleton more than once"
        )

    zero_gate = profile_zero_gate(identifiers_a, identifiers_b)
    if not zero_gate["passes_full_lp_zero_moment_gate"]:
        raise AssertionError(f"{label} failed independent profile zero gate")
    if zero_gate["table"] != ((0, 0),) * 13:
        raise AssertionError(f"{label} zero table changed")

    hensel = audit_profile_witness(
        target, identifiers_a, identifiers_b, index
    )
    if (
        hensel["placement_trits"] != 54
        or hensel["coefficient_rank"] != 18
        or hensel["augmented_rank"] != 18
        or hensel["nullity"] != 36
        or not hensel["consistent"]
    ):
        raise AssertionError(f"{label} first Hensel layer changed")

    transfer = audit_profile_transfer(identifiers_a, identifiers_b)
    catalog = catalog_phase_sum_intersection(
        identifiers_a, identifiers_b
    )
    if transfer["active_variables"] != 54:
        raise AssertionError(f"{label} lost a phase variable")
    if transfer["phase_sum_corpus"] != catalog["phase_sum_corpus"]:
        raise AssertionError(f"{label} catalog/transfer join disagrees")
    if transfer["accepted_assignments"] != catalog["accepted_assignments"]:
        raise AssertionError(f"{label} phase multiplicity changed")

    return {
        "label": label,
        "partition": partition,
        "target": target,
        "profile_ids_a": identifiers_a,
        "profile_ids_b": identifiers_b,
        "local_signed_states": local_states,
        "canonical_signed_skeleton": skeleton,
        "physical_origin_correlation": physical[0],
        "nonzero_physical_correlation_lags": (),
        "profile_zero_table_sha256": zero_gate["table_sha256"],
        "orbit_size": len(orbit),
        "stabilizer_size": stabilizer,
        "first_hensel": {
            "variables": hensel["placement_trits"],
            "displayed_equations": hensel["displayed_equations"],
            "identically_zero_rows": hensel["identically_zero_rows"],
            "coefficient_rank": hensel["coefficient_rank"],
            "augmented_rank": hensel["augmented_rank"],
            "nullity": hensel["nullity"],
            "canonical_solution_sha256": hensel_hash(
                hensel["canonical_solution"]
            ),
        },
        "phase_lift": {
            "placement_trits": transfer["active_variables"],
            "raw_assignments": transfer["total_assignments"],
            "channel_a_phase_counts": transfer[
                "channel_a_phase_counts"
            ],
            "channel_b_phase_counts": transfer[
                "channel_b_phase_counts"
            ],
            "channel_a_transfer_states": transfer["channel_a_states"],
            "channel_b_transfer_states": transfer["channel_b_states"],
            "compatible_transfer_signatures": transfer[
                "compatible_signature_count"
            ],
            "compatible_row_margin_catalog_rows": catalog[
                "compatible_catalog_rows"
            ],
            "root_character_accepted_assignments": transfer[
                "accepted_assignments"
            ],
            "compatible_signature_sha256": transfer[
                "compatible_sha256"
            ],
            "phase_sum_corpus_sha256": transfer[
                "phase_sum_corpus_sha256"
            ],
        },
    }


def build_certificate() -> dict[str, object]:
    orbit_certificates = tuple(
        one_orbit_certificate(index, candidate)
        for index, candidate in enumerate(CANDIDATES)
    )
    orbits = tuple(
        full_orbit(candidate[3], candidate[4]) for candidate in CANDIDATES
    )
    for left in range(len(orbits)):
        for right in range(left):
            if orbits[left] & orbits[right]:
                raise AssertionError("two declared exact orbits intersect")
    raw_orbit_members = sum(len(orbit) for orbit in orbits)
    if raw_orbit_members != 84:
        raise AssertionError("raw exact-orbit total changed")

    census = {
        partition: dict(zip(CENSUS_FIELDS, values))
        for partition, values in sorted(PARTITION_CENSUS.items())
    }
    exact_by_partition = {
        partition: values[CENSUS_FIELDS.index("exact_survivors")]
        for partition, values in sorted(PARTITION_CENSUS.items())
    }
    if exact_by_partition != {
        "222222": 1,
        "332220": 0,
        "333300": 0,
        "422220": 4,
        "433200": 0,
        "442200": 0,
        "444000": 0,
    }:
        raise AssertionError("partition exact counts changed")

    totals = {
        field: sum(values[index] for values in PARTITION_CENSUS.values())
        for index, field in enumerate(CENSUS_FIELDS)
    }
    if (
        totals["raw_skeletons"] != 14_715_744
        or totals["canonical_skeletons"] != 617_788
        or totals["mod9_survivors"] != 10_201_038
        or totals["exact_replays"] != 10_201_038
        or totals["exact_survivors"] != 5
    ):
        raise AssertionError("aggregate census changed")

    return {
        "schema": "lp333-order3-shell-two-exact-orbits-v1",
        "scope": (
            "Exact order-three profile solutions only; not labelled "
            "LP(333) objects and not Hadamard matrices."
        ),
        "sector_n9_n3_n0": (2, 12, 10),
        "symmetry_group_order": 24,
        "exact_orbits": len(orbit_certificates),
        "raw_orbit_members": raw_orbit_members,
        "partition_census": census,
        "census_totals": totals,
        "orbits": orbit_certificates,
    }


def main() -> None:
    certificate = build_certificate()
    semantic_sha256 = compact_hash(certificate)
    if EXPECTED_SEMANTIC_SHA256 and (
        semantic_sha256 != EXPECTED_SEMANTIC_SHA256
    ):
        raise AssertionError(
            f"semantic certificate changed: {semantic_sha256}"
        )
    print(f"partitions={len(PARTITION_CENSUS)}")
    print(f"exact_orbits={certificate['exact_orbits']}")
    print(f"raw_orbit_members={certificate['raw_orbit_members']}")
    print(
        "orbit_sizes="
        + ",".join(str(orbit["orbit_size"]) for orbit in certificate["orbits"])
    )
    print(
        "hensel_rank_nullity="
        + ",".join(
            f"{orbit['first_hensel']['coefficient_rank']}/"
            f"{orbit['first_hensel']['nullity']}"
            for orbit in certificate["orbits"]
        )
    )
    print(
        "compatible_row_margin_counts="
        + ",".join(
            str(orbit["phase_lift"]["compatible_row_margin_catalog_rows"])
            for orbit in certificate["orbits"]
        )
    )
    print(f"semantic_sha256={semantic_sha256}")
    print("STATUS: profile-level classification only; no LP(333) or H(668)")


if __name__ == "__main__":
    main()
