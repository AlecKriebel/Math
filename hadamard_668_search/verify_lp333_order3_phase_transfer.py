#!/usr/bin/env python3
"""Verify the trivial-character transfer for the LP(333) phase frame.

For a fixed residue-profile tuple, each active three-row fiber contributes
one signed cube root of unity.  Because every nonzero order-three column
class has size three, augmentation of the six phase sequences reduces all
placement trits to six small Eisenstein sums.

The diagonal and directed phase-frame equations then join the two channels
through one integer energy and one Eisenstein cross term.  This module
constructs that transfer exactly, replays it on all 22 stored profile-shard
witnesses, and checks the two labelled fixtures.
"""

from __future__ import annotations

from collections import defaultdict
import csv
from hashlib import sha256
import json
from pathlib import Path
from typing import DefaultDict, Mapping, Sequence

from verify_lp333_order3_difference_family import (
    CANONICAL_ZERO_EXPONENTS,
    CATALOG_DATA_ROWS,
    CATALOG_HEADER,
    CATALOG_RELATIVE_PATH,
    CATALOG_SHA256,
    CATALOG_WITNESS_INDEX,
    ROOTS as GAUSSIAN_ROOTS,
)
from verify_lp333_order3_labeled_jet import (
    LABELLED_SURVIVOR_MASKS_A,
    LABELLED_SURVIVOR_MASKS_B,
)
from verify_lp333_order3_phase_factor import (
    Eisenstein,
    OMEGA2,
    ZERO,
    e_add,
    e_conjugate,
    e_multiply,
    e_scale,
    fiber_phase,
    phase_columns,
    phase_from_trit,
)
from verify_lp333_order3_profile9 import (
    PINNED_PROFILE_IDS,
    PROFILES,
    ZERO_A_PLUS,
    ZERO_B_PLUS,
    actual_profile_counts,
)
from verify_lp333_order3_profile9_shards import (
    PROFILE9_SHARD_WITNESSES,
    audit_shard_witness,
)
from verify_lp333_order3_profile_zero_gate import profile_zero_gate
from verify_lp333_order3_trit_lift import (
    TRIT_SURVIVOR_MASKS_A,
    TRIT_SURVIVOR_MASKS_B,
)


ProfileIdentifiers = tuple[int, ...]
PhaseSumDistribution = dict[Eisenstein, int]
TransferKey = tuple[int, Eisenstein]
PhaseSumTriple = tuple[Eisenstein, Eisenstein, Eisenstein]
PhaseSumSextuple = tuple[PhaseSumTriple, PhaseSumTriple]

PHASE_VARIABLES = 54
FRAME_ENERGY = 167
TOTAL_PHASE_ASSIGNMENTS = 3**PHASE_VARIABLES

EXPECTED_COMPATIBLE_SIGNATURE_COUNTS = (
    69,
    69,
    46,
    46,
    71,
    71,
    69,
    69,
    65,
    65,
    75,
    75,
    64,
    64,
    62,
    62,
    47,
    47,
    22,
    87,
    87,
    37,
)
EXPECTED_COMPATIBLE_CATALOG_ROWS = (
    77,
    77,
    93,
    93,
    79,
    79,
    77,
    77,
    73,
    73,
    82,
    82,
    72,
    72,
    72,
    72,
    98,
    98,
    45,
    96,
    96,
    73,
)
EXPECTED_ACCEPTED_ASSIGNMENT_COUNTS = (
    299476370398383830889,
    285391291146212486376,
    338269656430021779738,
    334202436963302929560,
    297809708683170689964,
    325887533715811099305,
    286095435102253502460,
    297137928876535479168,
    299284820085636500400,
    282896931033697012200,
    361897672694646844620,
    315109917041025241080,
    270488436031587303072,
    277384846079729614824,
    270824491877087676780,
    272179280210017800942,
    348610104286486308288,
    350009864417078476128,
    180980378357204960640,
    363733977044403716436,
    361319476281225792516,
    266128504156683310464,
)

# Pinned from the canonical exact objects returned by ``verify()``.
EXPECTED_TRANSFER_CORPUS_SHA256 = (
    "af3bd3a306b7e23bd8c200acdd717d4c2b622bb17a08daf08a9ab5e2e2b6564d"
)
EXPECTED_CATALOG_INTERSECTION_SHA256 = (
    "24b33f2fc55c8fe3580c1d35c1d24491e95b2ef0eafaa213b12e8030ae8378e7"
)
EXPECTED_FIXTURE_SHA256 = (
    "87a5cf3f7be613a5fc77e285f9f0e55d2b6f67d07a88639aff8e66001e7f7c63"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def e_negate(value: Eisenstein) -> Eisenstein:
    return -value[0], -value[1]


def e_norm(value: Eisenstein) -> int:
    """Return the absolute Eisenstein norm."""

    return value[0] * value[0] - value[0] * value[1] + value[1] * value[1]


def channel_cross_term(
    sums: Sequence[Eisenstein],
) -> Eisenstein:
    """Return S_1 S_0^* + S_2 S_1^* + omega^2 S_0 S_2^*."""

    if len(sums) != 3:
        raise ValueError("a channel must have three fiber sums")
    first = e_multiply(sums[1], e_conjugate(sums[0]))
    second = e_multiply(sums[2], e_conjugate(sums[1]))
    third = e_multiply(
        OMEGA2,
        e_multiply(sums[0], e_conjugate(sums[2])),
    )
    return e_add(e_add(first, second), third)


def validate_identifiers(
    identifiers: Sequence[int],
) -> ProfileIdentifiers:
    normalized = tuple(int(value) for value in identifiers)
    if len(normalized) != 12:
        raise ValueError("a channel must contain twelve profile IDs")
    if any(not 0 <= value < len(PROFILES) for value in normalized):
        raise ValueError("a profile ID lies outside the ten-state catalog")
    return normalized


def fiber_phase_counts(
    channel: int,
    identifiers: Sequence[int],
    residue: int,
) -> tuple[int, int]:
    """Return the numbers of positive and negative phase variables."""

    if channel not in (0, 1):
        raise ValueError("the channel must be zero or one")
    if residue not in (0, 1, 2):
        raise ValueError("the residue must be zero, one, or two")
    normalized = validate_identifiers(identifiers)
    positive = 0
    negative = 0
    for class_index, profile_id in enumerate(normalized):
        count = actual_profile_counts(
            channel,
            class_index,
            PROFILES[profile_id],
        )[residue]
        positive += int(count == 1)
        negative += int(count == 2)
    return positive, negative


def phase_sum_distribution(
    channel: int,
    identifiers: Sequence[int],
    residue: int,
) -> PhaseSumDistribution:
    """Enumerate an augmented phase sum with exact assignment multiplicity."""

    normalized = validate_identifiers(identifiers)
    zero_words = (ZERO_A_PLUS, ZERO_B_PLUS)
    distribution: dict[Eisenstein, int] = {
        fiber_phase(zero_words[channel], residue): 1
    }
    active = 0
    for class_index, profile_id in enumerate(normalized):
        count = actual_profile_counts(
            channel,
            class_index,
            PROFILES[profile_id],
        )[residue]
        if count not in (1, 2):
            continue
        active += 1
        choices = tuple(
            e_scale(3, phase_from_trit(count, trit))
            for trit in range(3)
        )
        updated: DefaultDict[Eisenstein, int] = defaultdict(int)
        for current, multiplicity in distribution.items():
            for choice in choices:
                updated[e_add(current, choice)] += multiplicity
        distribution = dict(updated)
    if sum(distribution.values()) != 3**active:
        raise AssertionError("the phase-sum convolution lost assignments")
    return distribution


def channel_transfer(
    channel: int,
    identifiers: Sequence[int],
    energy_cap: int = FRAME_ENERGY,
) -> dict[str, object]:
    """Build the exact (energy, cross term) transfer for one channel."""

    normalized = validate_identifiers(identifiers)
    distributions = tuple(
        phase_sum_distribution(channel, normalized, residue)
        for residue in range(3)
    )
    phase_counts = tuple(
        fiber_phase_counts(channel, normalized, residue)
        for residue in range(3)
    )
    table: DefaultDict[TransferKey, int] = defaultdict(int)
    sum_states: dict[PhaseSumTriple, tuple[TransferKey, int]] = {}
    distinct_sum_triples = 0
    assignments_under_cap = 0

    for sum_0, multiplicity_0 in distributions[0].items():
        energy_0 = e_norm(sum_0)
        if energy_0 > energy_cap:
            continue
        for sum_1, multiplicity_1 in distributions[1].items():
            energy_01 = energy_0 + e_norm(sum_1)
            if energy_01 > energy_cap:
                continue
            partial_cross = e_multiply(
                sum_1,
                e_conjugate(sum_0),
            )
            for sum_2, multiplicity_2 in distributions[2].items():
                energy = energy_01 + e_norm(sum_2)
                if energy > energy_cap:
                    continue
                cross = e_add(
                    partial_cross,
                    e_multiply(sum_2, e_conjugate(sum_1)),
                )
                cross = e_add(
                    cross,
                    e_multiply(
                        OMEGA2,
                        e_multiply(sum_0, e_conjugate(sum_2)),
                    ),
                )
                multiplicity = (
                    multiplicity_0 * multiplicity_1 * multiplicity_2
                )
                table[(energy, cross)] += multiplicity
                sums: PhaseSumTriple = (sum_0, sum_1, sum_2)
                if sums in sum_states:
                    raise AssertionError("a phase-sum triple was duplicated")
                sum_states[sums] = ((energy, cross), multiplicity)
                distinct_sum_triples += 1
                assignments_under_cap += multiplicity

    active_variables = sum(
        positive + negative for positive, negative in phase_counts
    )
    return {
        "channel": channel,
        "phase_counts": phase_counts,
        "active_variables": active_variables,
        "sum_distribution_sizes": tuple(
            len(distribution) for distribution in distributions
        ),
        "distinct_sum_triples_under_cap": distinct_sum_triples,
        "assignments_under_cap": assignments_under_cap,
        "table": dict(table),
        "sum_states": sum_states,
    }


def compatible_transfer_join(
    transfer_a: Mapping[TransferKey, int],
    transfer_b: Mapping[TransferKey, int],
) -> tuple[tuple[int, Eisenstein, int, int], ...]:
    """Join channels on E_A+E_B=167 and T_A+T_B=0."""

    compatible = []
    for (energy_a, cross_a), multiplicity_a in sorted(
        transfer_a.items()
    ):
        key_b = FRAME_ENERGY - energy_a, e_negate(cross_a)
        multiplicity_b = transfer_b.get(key_b)
        if multiplicity_b:
            compatible.append(
                (energy_a, cross_a, multiplicity_a, multiplicity_b)
            )
    return tuple(compatible)


def compatible_phase_sum_join(
    transfer_a: Mapping[PhaseSumTriple, tuple[TransferKey, int]],
    transfer_b: Mapping[PhaseSumTriple, tuple[TransferKey, int]],
) -> tuple[tuple[PhaseSumSextuple, int], ...]:
    """Join the uncollapsed six augmented sums on the frame equations."""

    grouped_b: DefaultDict[
        TransferKey,
        list[tuple[PhaseSumTriple, int]],
    ] = defaultdict(list)
    for sums_b, (key_b, multiplicity_b) in transfer_b.items():
        grouped_b[key_b].append((sums_b, multiplicity_b))

    result = []
    for sums_a, ((energy_a, cross_a), multiplicity_a) in transfer_a.items():
        key_b = FRAME_ENERGY - energy_a, e_negate(cross_a)
        for sums_b, multiplicity_b in grouped_b.get(key_b, ()):
            result.append(
                ((sums_a, sums_b), multiplicity_a * multiplicity_b)
            )
    return tuple(sorted(result))


def audit_profile_transfer(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> dict[str, object]:
    """Audit the complete trivial-character transfer for one profile pair."""

    transfer_a = channel_transfer(0, identifiers_a)
    transfer_b = channel_transfer(1, identifiers_b)
    table_a = transfer_a["table"]
    table_b = transfer_b["table"]
    if not isinstance(table_a, dict) or not isinstance(table_b, dict):
        raise AssertionError("a channel transfer table has the wrong type")
    sum_states_a = transfer_a["sum_states"]
    sum_states_b = transfer_b["sum_states"]
    if not isinstance(sum_states_a, dict) or not isinstance(
        sum_states_b, dict
    ):
        raise AssertionError("a phase-sum transfer has the wrong type")
    compatible = compatible_transfer_join(table_a, table_b)
    phase_sum_corpus = compatible_phase_sum_join(
        sum_states_a,
        sum_states_b,
    )
    accepted_from_signatures = sum(
        multiplicity_a * multiplicity_b
        for _, _, multiplicity_a, multiplicity_b in compatible
    )
    accepted = sum(multiplicity for _, multiplicity in phase_sum_corpus)
    if accepted != accepted_from_signatures:
        raise AssertionError("collapsed and uncollapsed joins disagree")
    active_variables = (
        int(transfer_a["active_variables"])
        + int(transfer_b["active_variables"])
    )
    return {
        "active_variables": active_variables,
        "total_assignments": 3**active_variables,
        "channel_a_phase_counts": transfer_a["phase_counts"],
        "channel_b_phase_counts": transfer_b["phase_counts"],
        "channel_a_states": len(table_a),
        "channel_b_states": len(table_b),
        "compatible": compatible,
        "compatible_signature_count": len(compatible),
        "phase_sum_corpus": phase_sum_corpus,
        "compatible_phase_sum_count": len(phase_sum_corpus),
        "accepted_assignments": accepted,
        "compatible_sha256": compact_hash(compatible),
        "phase_sum_corpus_sha256": compact_hash(phase_sum_corpus),
    }


def row_sum_catalog() -> tuple[tuple[int, ...], ...]:
    """Load the pinned 1,756-word aggregate catalog dependency-free."""

    path = Path(__file__).resolve().parent / CATALOG_RELATIVE_PATH
    payload = path.read_bytes()
    if sha256(payload).hexdigest() != CATALOG_SHA256:
        raise AssertionError("the row-sum catalog hash changed")
    rows = list(csv.reader(payload.decode("ascii").splitlines()))
    if not rows or tuple(rows[0]) != CATALOG_HEADER:
        raise AssertionError("the row-sum catalog header changed")
    if len(rows) - 1 != CATALOG_DATA_ROWS:
        raise AssertionError("the row-sum catalog length changed")

    zero = tuple(
        GAUSSIAN_ROOTS[exponent]
        for exponent in CANONICAL_ZERO_EXPONENTS
    )
    result = []
    for raw in rows[1:]:
        values = tuple(int(value) for value in raw)
        aggregate = []
        for row in range(9):
            difference = (
                values[2 * row] - zero[row][0],
                values[2 * row + 1] - zero[row][1],
            )
            if difference[0] % 3 or difference[1] % 3:
                raise AssertionError("a catalog word is not core plus 3t")
            aggregate.extend(
                (difference[0] // 3, difference[1] // 3)
            )
        result.append(tuple(aggregate))
    if len(set(result)) != len(result):
        raise AssertionError("the row-sum catalog contains a duplicate")
    return tuple(result)


def physical_row_margins(
    aggregate: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Recover the two physical plus-count margins from one catalog row."""

    if len(aggregate) != 18:
        raise ValueError("an aggregate row must have 18 coordinates")
    result = ([], [])
    for row in range(9):
        real = int(aggregate[2 * row])
        imag = int(aggregate[2 * row + 1])
        if (real - imag) % 2 or (real + imag) % 2:
            raise ValueError("an aggregate row has incompatible parity")
        class_a = (12 + real - imag) // 2
        class_b = (12 + real + imag) // 2
        if not 0 <= class_a <= 12 or not 0 <= class_b <= 12:
            raise ValueError("a class-row margin lies outside [0,12]")
        result[0].append(ZERO_A_PLUS[row] + 3 * class_a)
        result[1].append(ZERO_B_PLUS[row] + 3 * class_b)
    return tuple(result[0]), tuple(result[1])


def profile_residue_totals(
    channel: int,
    identifiers: Sequence[int],
) -> tuple[int, int, int]:
    """Return the three fixed sums of physical row margins."""

    normalized = validate_identifiers(identifiers)
    zero = (ZERO_A_PLUS, ZERO_B_PLUS)[channel]
    return tuple(
        sum(zero[residue::3])
        + 3
        * sum(
            actual_profile_counts(
                channel,
                class_index,
                PROFILES[profile_id],
            )[residue]
            for class_index, profile_id in enumerate(normalized)
        )
        for residue in range(3)
    )  # type: ignore[return-value]


def phase_sums_from_margins(
    margins: Sequence[Sequence[int]],
) -> PhaseSumSextuple:
    """Take the three length-three Eisenstein transforms of row margins."""

    if len(margins) != 2 or any(len(channel) != 9 for channel in margins):
        raise ValueError("physical row margins must have shape 2 by 9")
    result = []
    for channel in margins:
        sums = []
        for residue in range(3):
            values = tuple(int(channel[residue + 3 * q]) for q in range(3))
            sums.append(
                (
                    values[0] - values[2],
                    values[1] - values[2],
                )
            )
        result.append(tuple(sums))
    return tuple(result)  # type: ignore[return-value]


def catalog_phase_sum_intersection(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> dict[str, object]:
    """Intersect one fixed profile tuple with the exact row-sum catalog."""

    identifiers = (
        validate_identifiers(identifiers_a),
        validate_identifiers(identifiers_b),
    )
    totals = tuple(
        profile_residue_totals(channel, identifiers[channel])
        for channel in range(2)
    )
    distributions = tuple(
        tuple(
            phase_sum_distribution(
                channel,
                identifiers[channel],
                residue,
            )
            for residue in range(3)
        )
        for channel in range(2)
    )
    records = []
    for catalog_index, aggregate in enumerate(row_sum_catalog()):
        margins = physical_row_margins(aggregate)
        if any(
            sum(margins[channel][residue::3])
            != totals[channel][residue]
            for channel in range(2)
            for residue in range(3)
        ):
            continue
        sums = phase_sums_from_margins(margins)
        multiplicity = 1
        for channel in range(2):
            for residue in range(3):
                multiplicity *= distributions[channel][residue].get(
                    sums[channel][residue],
                    0,
                )
        if multiplicity:
            records.append((catalog_index, sums, multiplicity))

    phase_sum_corpus = tuple(
        sorted((sums, multiplicity) for _, sums, multiplicity in records)
    )
    if len({sums for sums, _ in phase_sum_corpus}) != len(phase_sum_corpus):
        raise AssertionError("fixed totals did not make phase sums injective")
    return {
        "catalog_rows": len(row_sum_catalog()),
        "compatible_catalog_indices": tuple(
            index for index, _, _ in records
        ),
        "compatible_catalog_rows": len(records),
        "phase_sum_corpus": phase_sum_corpus,
        "accepted_assignments": sum(
            multiplicity for _, multiplicity in phase_sum_corpus
        ),
        "phase_sum_corpus_sha256": compact_hash(phase_sum_corpus),
    }


def phase_sums_from_masks(
    masks_a: Sequence[int],
    masks_b: Sequence[int],
) -> tuple[tuple[Eisenstein, Eisenstein, Eisenstein], ...]:
    phases = phase_columns(masks_a, masks_b)
    result = []
    for channel in phases:
        sums = []
        for residue in range(3):
            value = ZERO
            for column in channel:
                value = e_add(value, column[residue])
            sums.append(value)
        result.append(tuple(sums))
    return tuple(result)  # type: ignore[return-value]


def channel_signature(
    sums: Sequence[Eisenstein],
) -> TransferKey:
    if len(sums) != 3:
        raise ValueError("a channel must have three fiber sums")
    return sum(e_norm(value) for value in sums), channel_cross_term(sums)


def audit_fixture(
    masks_a: Sequence[int],
    masks_b: Sequence[int],
    pinned_transfer: Mapping[str, object],
) -> dict[str, object]:
    sums = phase_sums_from_masks(masks_a, masks_b)
    signatures = tuple(channel_signature(channel) for channel in sums)
    energy = signatures[0][0] + signatures[1][0]
    cross = e_add(signatures[0][1], signatures[1][1])
    if energy != FRAME_ENERGY or cross != ZERO:
        raise AssertionError("a labelled fixture failed the phase transfer")

    compatible = pinned_transfer["compatible"]
    if not isinstance(compatible, tuple):
        raise AssertionError("the pinned compatible join has the wrong type")
    signature_a = signatures[0]
    if not any(
        energy_a == signature_a[0] and cross_a == signature_a[1]
        for energy_a, cross_a, _, _ in compatible
    ):
        raise AssertionError("a labelled fixture is absent from the transfer")
    phase_sum_corpus = pinned_transfer["phase_sum_corpus"]
    if not isinstance(phase_sum_corpus, tuple):
        raise AssertionError("the pinned phase-sum corpus has the wrong type")
    if not any(candidate == sums for candidate, _ in phase_sum_corpus):
        raise AssertionError("a labelled six-sum word is absent from the transfer")
    return {
        "phase_sums": sums,
        "signatures": signatures,
        "frame_equations_hold": True,
    }


def verify() -> dict[str, object]:
    shard_summaries = []
    transfer_corpus = []
    catalog_intersection_corpus = []
    zero_gate_failures = 0
    for target, identifiers_a, identifiers_b in PROFILE9_SHARD_WITNESSES:
        # Recheck that the object being transferred is a valid stored
        # profile-ideal witness, without trusting its label.
        audit_shard_witness(target, identifiers_a, identifiers_b)
        zero_gate = profile_zero_gate(identifiers_a, identifiers_b)
        if zero_gate["passes_full_lp_zero_moment_gate"]:
            raise AssertionError(
                "a diagnostic profile tuple unexpectedly passed D_t=0"
            )
        zero_gate_failures += 1
        audit = audit_profile_transfer(identifiers_a, identifiers_b)
        catalog = catalog_phase_sum_intersection(
            identifiers_a,
            identifiers_b,
        )
        if audit["active_variables"] != PHASE_VARIABLES:
            raise AssertionError("a profile shard lost its 54 phase variables")
        if audit["total_assignments"] != TOTAL_PHASE_ASSIGNMENTS:
            raise AssertionError("a profile shard has the wrong search volume")
        if not int(audit["accepted_assignments"]):
            raise AssertionError("a profile shard has no root-character lift")
        if audit["phase_sum_corpus"] != catalog["phase_sum_corpus"]:
            raise AssertionError(
                "the phase transfer and row-sum catalog disagree"
            )
        if (
            audit["accepted_assignments"]
            != catalog["accepted_assignments"]
        ):
            raise AssertionError(
                "the phase transfer and catalog multiplicities disagree"
            )
        shard_summaries.append(
            (
                target,
                audit["compatible_signature_count"],
                catalog["compatible_catalog_rows"],
                audit["accepted_assignments"],
                audit["channel_a_states"],
                audit["channel_b_states"],
            )
        )
        transfer_corpus.append((target, audit["compatible"]))
        catalog_intersection_corpus.append(
            (
                target,
                catalog["compatible_catalog_indices"],
                catalog["phase_sum_corpus"],
            )
        )

    compatible_counts = tuple(summary[1] for summary in shard_summaries)
    compatible_catalog_rows = tuple(
        summary[2] for summary in shard_summaries
    )
    accepted_counts = tuple(summary[3] for summary in shard_summaries)
    if compatible_counts != EXPECTED_COMPATIBLE_SIGNATURE_COUNTS:
        raise AssertionError("the compatible signature counts changed")
    if compatible_catalog_rows != EXPECTED_COMPATIBLE_CATALOG_ROWS:
        raise AssertionError("the compatible catalog-row counts changed")
    if accepted_counts != EXPECTED_ACCEPTED_ASSIGNMENT_COUNTS:
        raise AssertionError("the accepted assignment counts changed")

    transfer_hash = compact_hash(tuple(transfer_corpus))
    if (
        EXPECTED_TRANSFER_CORPUS_SHA256
        and transfer_hash != EXPECTED_TRANSFER_CORPUS_SHA256
    ):
        raise AssertionError("the phase-transfer corpus changed")
    catalog_intersection_hash = compact_hash(
        tuple(catalog_intersection_corpus)
    )
    if (
        EXPECTED_CATALOG_INTERSECTION_SHA256
        and catalog_intersection_hash
        != EXPECTED_CATALOG_INTERSECTION_SHA256
    ):
        raise AssertionError("the catalog-intersection corpus changed")

    pinned_transfer = audit_profile_transfer(*PINNED_PROFILE_IDS)
    pinned_catalog = catalog_phase_sum_intersection(*PINNED_PROFILE_IDS)
    if (
        pinned_transfer["phase_sum_corpus"]
        != pinned_catalog["phase_sum_corpus"]
    ):
        raise AssertionError("the pinned transfer and catalog disagree")
    pinned_zero_gate = profile_zero_gate(*PINNED_PROFILE_IDS)
    if pinned_zero_gate["passes_full_lp_zero_moment_gate"]:
        raise AssertionError("the pinned diagnostic profile passed D_t=0")
    if (
        pinned_transfer["compatible_signature_count"],
        pinned_catalog["compatible_catalog_rows"],
        pinned_transfer["accepted_assignments"],
    ) != (65, 73, 291964627896688393920):
        raise AssertionError("the pinned transfer census changed")
    if CATALOG_WITNESS_INDEX not in pinned_catalog[
        "compatible_catalog_indices"
    ]:
        raise AssertionError("catalog row 695 left the pinned phase transfer")
    labelled = audit_fixture(
        LABELLED_SURVIVOR_MASKS_A,
        LABELLED_SURVIVOR_MASKS_B,
        pinned_transfer,
    )
    trit = audit_fixture(
        TRIT_SURVIVOR_MASKS_A,
        TRIT_SURVIVOR_MASKS_B,
        pinned_transfer,
    )
    fixtures = (labelled, trit)
    fixture_hash = compact_hash(fixtures)
    if EXPECTED_FIXTURE_SHA256 and fixture_hash != EXPECTED_FIXTURE_SHA256:
        raise AssertionError("the phase-transfer fixtures changed")

    if labelled != trit:
        raise AssertionError("the two fixtures lost their common phase sums")
    if labelled["signatures"] != (
        (69, (32, 15)),
        (98, (-32, -15)),
    ):
        raise AssertionError("the pinned fixture signatures changed")
    catalog_witness_sums = phase_sums_from_margins(
        physical_row_margins(row_sum_catalog()[CATALOG_WITNESS_INDEX])
    )
    if labelled["phase_sums"] != catalog_witness_sums:
        raise AssertionError("the labelled fixtures left catalog row 695")

    return {
        "profile_shards": len(PROFILE9_SHARD_WITNESSES),
        "phase_variables_per_shard": PHASE_VARIABLES,
        "total_assignments_per_shard": TOTAL_PHASE_ASSIGNMENTS,
        "compatible_signature_counts": compatible_counts,
        "compatible_catalog_rows": compatible_catalog_rows,
        "accepted_assignment_counts": accepted_counts,
        "minimum_compatible_signatures": min(compatible_counts),
        "maximum_compatible_signatures": max(compatible_counts),
        "minimum_compatible_catalog_rows": min(
            compatible_catalog_rows
        ),
        "maximum_compatible_catalog_rows": max(
            compatible_catalog_rows
        ),
        "minimum_accepted_assignments": min(accepted_counts),
        "maximum_accepted_assignments": max(accepted_counts),
        "transfer_corpus_sha256": transfer_hash,
        "catalog_intersection_sha256": catalog_intersection_hash,
        "pinned_compatible_signatures": pinned_transfer[
            "compatible_signature_count"
        ],
        "pinned_compatible_catalog_rows": pinned_catalog[
            "compatible_catalog_rows"
        ],
        "pinned_accepted_assignments": pinned_transfer[
            "accepted_assignments"
        ],
        "pinned_fixture_catalog_index": CATALOG_WITNESS_INDEX,
        "fixture_sha256": fixture_hash,
        "fixture_signature": labelled["signatures"],
        "diagnostic_zero_gate_failures": zero_gate_failures + 1,
        "fixed_profile_assignments_audited": 23,
        "aggregate_shard_exclusions": 0,
        "labelled_fixtures_checked": 2,
        "status": (
            "phase-coordinate transfer exactly matches the row-sum catalog; "
            "all stored profile inputs are diagnostic D_t != 0 fixtures"
        ),
    }


def main() -> None:
    result = verify()
    print(f"profile_shards={result['profile_shards']}")
    print(f"phase_variables_per_shard={result['phase_variables_per_shard']}")
    print(
        "total_assignments_per_shard="
        f"{result['total_assignments_per_shard']}"
    )
    print(
        "compatible_signature_range="
        f"{result['minimum_compatible_signatures']}.."
        f"{result['maximum_compatible_signatures']}"
    )
    print(
        "compatible_catalog_row_range="
        f"{result['minimum_compatible_catalog_rows']}.."
        f"{result['maximum_compatible_catalog_rows']}"
    )
    print(
        "accepted_assignment_range="
        f"{result['minimum_accepted_assignments']}.."
        f"{result['maximum_accepted_assignments']}"
    )
    print(
        "transfer_corpus_sha256="
        f"{result['transfer_corpus_sha256']}"
    )
    print(
        "catalog_intersection_sha256="
        f"{result['catalog_intersection_sha256']}"
    )
    print(f"fixture_sha256={result['fixture_sha256']}")
    print("PASS: exact LP(333) trivial-character phase transfer replayed")
    print("STATUS: diagnostic fixtures fail D_t=0; no LP(333) or H(668)")


if __name__ == "__main__":
    main()
