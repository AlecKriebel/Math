#!/usr/bin/env python3
"""Audit the exact order-three profile gate required by a full LP(333).

For two sign sequences of length 333 and sum one, the Legendre-pair
correlation target is equivalent to a combined plus-support intersection
of 167 at every nonzero lag.  In the ``C_9 x C_37`` coordinates used by
the order-three quotient, the adjusted origin intersection is also 167.
Consequently every nine-entry row-lag vector has zero Fourier coefficient
at a primitive cube root.

That coefficient is exactly the profile correlation ``D_t`` reconstructed
by :mod:`verify_lp333_order3_profile9`.  Thus ``D_t = 0`` on all thirteen
column parts is a necessary condition for a full LP(333).  Membership in
``3(1-omega) Z[omega]`` is only the weaker condition that the
primitive-nine target triples are integral.

This module applies the exact zero-moment gate to the original row-695
profile and to all 22 ideal-compatible profile witnesses.  It excludes
those fixed profile assignments, not their aggregate row-sum shards.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from typing import Sequence

from verify_lp333_order3_integral9 import invariant_correlation_table
from verify_lp333_order3_labeled_jet import (
    LABELLED_SURVIVOR_AGGREGATE,
    LABELLED_SURVIVOR_MASKS_A,
    LABELLED_SURVIVOR_MASKS_B,
)
from verify_lp333_order3_profile9 import (
    PINNED_PROFILE_IDS,
    audit_profile_table,
    moment_from_exact_correlations,
)
from verify_lp333_order3_profile9_shards import PROFILE9_SHARD_WITNESSES


Eisenstein = tuple[int, int]
Target = tuple[int, int, int, int]

EXPECTED_ZERO_GATE_CERTIFICATE_SHA256 = (
    "d0e496d2a2b01ed5432e4ff89c2a306a778a52cac08cebd22aa60292588a9060"
)
EXPECTED_PINNED_ZERO_GATE_SHA256 = (
    "e22de237bf4a6e3b61d7bd31aff2bad9d7126fd8739b5ab503f75ca52c758621"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def full_lp_plus_intersection_from_paf(
    paf_sum: int,
    plus_count_a: int = 167,
    plus_count_b: int = 167,
    length: int = 333,
) -> int:
    """Invert the exact sign-PAF/plus-intersection identity.

    For a nonzero lag,

    ``PAF(A)+PAF(B) = 4 I - 4(k_A+k_B) + 2 n``.
    """

    numerator = (
        int(paf_sum)
        + 4 * (int(plus_count_a) + int(plus_count_b))
        - 2 * int(length)
    )
    if numerator % 4:
        raise ValueError("the requested PAF has no integral intersection")
    return numerator // 4


def aggregate_shard_target(aggregate: Sequence[int]) -> Target:
    """Return the four-coordinate shard target of one 18-coordinate row."""

    if len(aggregate) != 18:
        raise ValueError("an aggregate row must have 18 coordinates")
    values = tuple(
        (int(aggregate[2 * row]), int(aggregate[2 * row + 1]))
        for row in range(9)
    )
    residue_sums = tuple(
        tuple(
            sum(values[row][coordinate] for row in range(residue, 9, 3))
            for coordinate in range(2)
        )
        for residue in range(3)
    )
    a_binary = tuple(real - imag for real, imag in residue_sums)
    b_binary = tuple(real + imag for real, imag in residue_sums)
    numerators = (
        a_binary[0] - a_binary[2],
        a_binary[1] - a_binary[2],
        b_binary[0] - b_binary[2],
        b_binary[1] - b_binary[2],
    )
    if any(value % 2 for value in numerators):
        raise ValueError("the aggregate has a nonintegral shard target")
    return tuple(value // 2 for value in numerators)  # type: ignore[return-value]


def profile_zero_gate(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> dict[str, object]:
    """Apply the exact necessary zero-moment condition to one profile tuple."""

    audit = audit_profile_table(identifiers_a, identifiers_b)
    table = tuple(audit["table"])
    violations = tuple(
        (part_index, value)
        for part_index, value in enumerate(table)
        if value != (0, 0)
    )
    nonzero_class_violations = tuple(
        (part_index - 1, value)
        for part_index, value in violations
        if part_index
    )
    return {
        "table": table,
        "table_sha256": audit["table_sha256"],
        "ideal_compatible": not audit["failing_nonzero_classes"],
        "zero_origin_moment": table[0] == (0, 0),
        "violating_parts": violations,
        "violating_nonzero_classes": nonzero_class_violations,
        "nonzero_class_violation_count": len(nonzero_class_violations),
        "passes_full_lp_zero_moment_gate": not violations,
        "fixed_profile_excluded": bool(violations),
    }


def verify_full_lp_target_implication() -> dict[str, object]:
    """Replay the elementary arithmetic behind the necessary condition."""

    target = full_lp_plus_intersection_from_paf(-2)
    if target != 167:
        raise AssertionError("the LP(333) plus-intersection target changed")
    adjusted_origin = 334 - 167
    if adjusted_origin != target:
        raise AssertionError("the adjusted origin target changed")
    constant_row = (target,) * 9
    moment = moment_from_exact_correlations(constant_row)
    if moment != (0, 0):
        raise AssertionError("a constant LP target has nonzero order-three moment")
    return {
        "length": 333,
        "sign_sums": (1, 1),
        "plus_counts": (167, 167),
        "nonzero_paf_target": -2,
        "plus_intersection_target": target,
        "adjusted_origin_target": adjusted_origin,
        "target_order3_moment": moment,
    }


def verify_row695_profile_gate() -> dict[str, object]:
    """Exclude the row-695 profile and the stored witness in its shard."""

    target = aggregate_shard_target(LABELLED_SURVIVOR_AGGREGATE)
    if target != (1, -1, 2, -2):
        raise AssertionError("row 695 moved to a different aggregate shard")
    matching = tuple(
        index
        for index, witness in enumerate(PROFILE9_SHARD_WITNESSES)
        if witness[0] == target
    )
    if matching != (8,):
        raise AssertionError("row 695 no longer selects shard witness 8")

    pinned = profile_zero_gate(*PINNED_PROFILE_IDS)
    if not pinned["ideal_compatible"]:
        raise AssertionError("the original row-695 profile lost ideal compatibility")
    if pinned["nonzero_class_violation_count"] != 12:
        raise AssertionError("the original row-695 zero-gate audit changed")

    _, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[8]
    alternative = profile_zero_gate(identifiers_a, identifiers_b)
    if not alternative["ideal_compatible"]:
        raise AssertionError("shard witness 8 lost ideal compatibility")
    if alternative["nonzero_class_violation_count"] != 12:
        raise AssertionError("the row-695 shard witness audit changed")

    pinned_certificate = (
        target,
        PINNED_PROFILE_IDS,
        pinned["table"],
        pinned["violating_nonzero_classes"],
    )
    pinned_hash = compact_hash(pinned_certificate)
    if (
        EXPECTED_PINNED_ZERO_GATE_SHA256
        and pinned_hash != EXPECTED_PINNED_ZERO_GATE_SHA256
    ):
        raise AssertionError("the pinned row-695 zero-gate certificate changed")

    # Independently reconstruct the exact labelled correlation table and
    # verify that its order-three moments are precisely the profile table.
    exact_table = invariant_correlation_table(
        LABELLED_SURVIVOR_MASKS_A,
        LABELLED_SURVIVOR_MASKS_B,
    )
    exact_moments = tuple(
        moment_from_exact_correlations(row) for row in exact_table
    )
    if exact_moments != pinned["table"]:
        raise AssertionError("labelled and profile zero-moment audits disagree")
    exact_bad_entries = sum(
        value != 167 for row in exact_table for value in row
    )
    if not exact_bad_entries:
        raise AssertionError("the known modular fixture became a full LP(333)")

    return {
        "catalog_row": 695,
        "aggregate_target": target,
        "ideal_witness_index": matching[0],
        "original_profile_nonzero_classes": (
            pinned["nonzero_class_violation_count"]
        ),
        "alternative_profile_nonzero_classes": (
            alternative["nonzero_class_violation_count"]
        ),
        "original_profile_certificate_sha256": pinned_hash,
        "labelled_full_correlation_bad_entries": exact_bad_entries,
        "original_and_same_shard_witness_excluded": True,
    }


def verify_ideal_witness_zero_gates() -> dict[str, object]:
    """Audit all 22 ideal-compatible fixed profile assignments."""

    certificate = []
    histogram: Counter[int] = Counter()
    total_nonzero_classes = 0
    for index, (target, identifiers_a, identifiers_b) in enumerate(
        PROFILE9_SHARD_WITNESSES
    ):
        gate = profile_zero_gate(identifiers_a, identifiers_b)
        if not gate["ideal_compatible"]:
            raise AssertionError("an ideal witness no longer passes its ideal test")
        if not gate["zero_origin_moment"]:
            raise AssertionError("an ideal witness has a nonzero origin moment")
        if not gate["fixed_profile_excluded"]:
            raise AssertionError("an ideal witness unexpectedly passes D_t=0")
        count = int(gate["nonzero_class_violation_count"])
        histogram[count] += 1
        total_nonzero_classes += count
        certificate.append(
            (
                index,
                target,
                identifiers_a,
                identifiers_b,
                gate["table"],
                gate["violating_nonzero_classes"],
            )
        )

    certificate_tuple = tuple(certificate)
    certificate_hash = compact_hash(certificate_tuple)
    if (
        EXPECTED_ZERO_GATE_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_ZERO_GATE_CERTIFICATE_SHA256
    ):
        raise AssertionError("the 22-witness zero-gate certificate changed")
    if tuple(sorted(histogram.items())) != ((10, 1), (12, 21)):
        raise AssertionError("the zero-moment failure histogram changed")
    if total_nonzero_classes != 262:
        raise AssertionError("the zero-moment failure count changed")
    return {
        "aggregate_shards_represented": len(PROFILE9_SHARD_WITNESSES),
        "fixed_profile_assignments_audited": len(certificate_tuple),
        "ideal_compatible_assignments": len(certificate_tuple),
        "fixed_profile_exclusions": len(certificate_tuple),
        "aggregate_shard_exclusions": 0,
        "nonzero_class_failure_histogram": tuple(sorted(histogram.items())),
        "total_nonzero_class_failures": total_nonzero_classes,
        "certificate_sha256": certificate_hash,
    }


def verify() -> dict[str, object]:
    implication = verify_full_lp_target_implication()
    row695 = verify_row695_profile_gate()
    corpus = verify_ideal_witness_zero_gates()
    return {
        "full_lp_implication": implication,
        "row695": row695,
        "ideal_witness_corpus": corpus,
        "status": (
            "all 22 fixed ideal-compatible profile assignments, including "
            "the stored witness in row 695's shard, fail the exact full-LP "
            "zero-moment gate; "
            "no aggregate shard is excluded"
        ),
    }


def main() -> None:
    result = verify()
    corpus = result["ideal_witness_corpus"]
    row695 = result["row695"]
    print(
        "fixed_profile_assignments_audited="
        f"{corpus['fixed_profile_assignments_audited']}"
    )
    print(f"fixed_profile_exclusions={corpus['fixed_profile_exclusions']}")
    print(f"aggregate_shard_exclusions={corpus['aggregate_shard_exclusions']}")
    print(
        "nonzero_class_failure_histogram="
        f"{corpus['nonzero_class_failure_histogram']}"
    )
    print(f"zero_gate_certificate_sha256={corpus['certificate_sha256']}")
    print(
        "row695_original_profile_certificate_sha256="
        f"{row695['original_profile_certificate_sha256']}"
    )
    print("PASS: exact full-LP order-three zero-moment gate replayed")
    print("STATUS: 22 fixed profile tuples excluded; zero whole shards excluded")


if __name__ == "__main__":
    main()
