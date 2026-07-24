#!/usr/bin/env python3
"""Exact two-coefficient sieve for the LP(333) diagonal phase frame.

For each of the 22 pinned primitive-nine-ideal profile tuples, the 54 active
fibers carry independent signed cube-root phases.  The diagonal frame

    sum_(channel,residue) U U* = 167 e

has two especially small necessary projections:

* evaluation at the trivial C_37 character, giving exact total norm 167;
* coefficient one of the characteristic-37 logarithmic norm transfer.

Both projections split as a sum of six one-sequence summaries.  This
verifier enumerates each one-sequence phase space exactly, collapses it to
``(exact norm, transfer coefficient)``, and joins only those summaries.
It does not search for, or assert, a complete diagonal-frame assignment.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from hashlib import sha256
import json
from typing import Sequence

from verify_lp333_order3_char37_transfer import (
    P,
    PROFILES,
    TRANSFER_FACTORS,
    class_log_transfer,
    e_conjugate,
    e_multiply,
    e_reduce,
    norm_transfer,
)
from verify_lp333_order3_labeled_jet import ZERO_A_PLUS, ZERO_B_PLUS
from verify_lp333_order3_phase_factor import ROOTS, fiber_phase
from verify_lp333_order3_profile9 import actual_profile_counts
from verify_lp333_order3_profile9_shards import PROFILE9_SHARD_WITNESSES


Eisenstein = tuple[int, int]
Target = tuple[int, int, int, int]
SequenceSignature = tuple[int, ...]

RAW_PHASE_ASSIGNMENTS = 3**54
EXPECTED_RESULT_SHA256 = (
    "443d0e733f5c383d5d5ed14d5ec98b458becf9d7dd9e64c08d9d07c2b625a81a"
)

# (aggregate target, exact augmentation survivors, augmentation+T1 survivors)
EXPECTED_COUNTS: tuple[tuple[Target, int, int], ...] = (
    ((-3, -3, -4, -2), 225607966687460409861942, 6097512613173259004766),
    ((-3, -3, -2, 2), 210563040946931567161416, 5690892998567259379752),
    ((-3, 0, -3, -3), 211218303518262767764980, 5708602797788004231450),
    ((-3, 0, 0, 3), 209495038833176167292760, 5662028076377136346398),
    ((-1, -2, -5, -1), 209967625213584980822244, 5674800681224540749794),
    ((-1, -2, -4, 1), 229536837530169637729176, 6203698311594366895866),
    ((0, 3, -4, -2), 215882326870233615335196, 5834657482991635755360),
    ((0, 3, -2, 2), 221609850924373397262036, 5989455430388985851952),
    ((1, -1, 2, -2), 225424699738725956905296, 6092559452403808199808),
    ((1, -1, 4, 2), 213477155092935890190720, 5769652840335575735070),
    ((1, 2, -5, -1), 233232723804553256004480, 6303587129843385773508),
    ((1, 2, -4, 1), 210989985104317617843984, 5702432029700785860930),
    ((2, -2, -4, -2), 211365795148911299469663, 5712589058074479308379),
    ((2, -2, -2, 2), 218242998255267127520208, 5898459412315133342958),
    ((2, 1, 2, -2), 212766400412581288258440, 5750443254391683509910),
    ((2, 1, 4, 2), 213781329468075796484472, 5777873769411517646352),
    ((3, 0, 0, -3), 211199547699156285853344, 5708095883774218698804),
    ((3, 0, 3, 3), 212179786988846366989656, 5734588837527763259148),
    ((4, -1, 0, 0), 214168199217504640264332, 5788329708586727721588),
    ((4, 2, -4, -2), 212251675312687802199048, 5736531765218400103596),
    ((4, 2, -2, 2), 210893956076353663128420, 5699836650715880616222),
    ((5, 1, 0, 0), 209362382441060450385168, 5658442768663401171882),
)


ZERO_PHASES: tuple[tuple[Eisenstein, ...], ...] = tuple(
    tuple(fiber_phase(word, residue) for residue in range(3))
    for word in (ZERO_A_PLUS, ZERO_B_PLUS)
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def e_add_integer(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return left[0] + right[0], left[1] + right[1]


def e_scale_integer(scale: int, value: Eisenstein) -> Eisenstein:
    return scale * value[0], scale * value[1]


def e_norm_integer(value: Eisenstein) -> int:
    return value[0] * value[0] - value[0] * value[1] + value[1] * value[1]


def e_sub_mod37(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return (left[0] - right[0]) % P, (left[1] - right[1]) % P


def sequence_signature(
    channel: int,
    residue: int,
    identifiers: Sequence[int],
) -> SequenceSignature:
    """Encode the fixed zero phase and every active signed class."""

    if channel not in (0, 1) or not 0 <= residue < 3:
        raise ValueError("the channel or residue is outside its range")
    if len(identifiers) != 12:
        raise ValueError("a phase sequence needs twelve profile IDs")
    result = [*ZERO_PHASES[channel][residue]]
    for class_index, profile_id in enumerate(identifiers):
        if not 0 <= int(profile_id) < len(PROFILES):
            raise ValueError("a profile ID lies outside the catalog")
        count = actual_profile_counts(
            channel,
            class_index,
            PROFILES[int(profile_id)],
        )[residue]
        if count in (1, 2):
            result.extend((class_index, 1 if count == 1 else -1))
    return tuple(result)


def decode_signature(
    signature: SequenceSignature,
) -> tuple[Eisenstein, tuple[tuple[int, int], ...]]:
    if len(signature) < 2 or (len(signature) - 2) % 2:
        raise ValueError("a sequence signature has the wrong length")
    zero = int(signature[0]), int(signature[1])
    active = tuple(
        (int(signature[index]), int(signature[index + 1]))
        for index in range(2, len(signature), 2)
    )
    if any(
        not 0 <= class_index < 12 or sign not in (-1, 1)
        for class_index, sign in active
    ):
        raise ValueError("an active phase descriptor is invalid")
    return zero, active


def first_norm_coefficient(
    exact_sum: Eisenstein,
    first_transfer: Eisenstein,
) -> int:
    """Return the one scalar in the anti-self-conjugate T_1 coefficient."""

    constant = e_reduce(exact_sum)
    value = e_sub_mod37(
        e_multiply(first_transfer, e_conjugate(constant)),
        e_multiply(constant, e_conjugate(first_transfer)),
    )
    if (value[1] - 2 * value[0]) % P:
        raise AssertionError("the first norm coefficient lost anti-reality")
    return value[0]


@lru_cache(maxsize=None)
def sequence_summary(
    signature: SequenceSignature,
) -> tuple[tuple[tuple[int, int], int], ...]:
    """Count one phase sequence by ``(exact norm, T_1 scalar)``."""

    zero, active = decode_signature(signature)
    result: defaultdict[tuple[int, int], int] = defaultdict(int)

    def visit(
        position: int,
        sum_real: int,
        sum_omega: int,
        transfer_real: int,
        transfer_omega: int,
    ) -> None:
        if position == len(active):
            exact_sum = sum_real, sum_omega
            norm = e_norm_integer(exact_sum)
            if norm <= 167:
                coefficient = first_norm_coefficient(
                    exact_sum,
                    (transfer_real, transfer_omega),
                )
                result[norm, coefficient] += 1
            return

        class_index, sign = active[position]
        scale = (
            TRANSFER_FACTORS[1]
            * pow(8, class_index, P)
            * sign
        ) % P
        for root in ROOTS:
            visit(
                position + 1,
                sum_real + 3 * sign * root[0],
                sum_omega + 3 * sign * root[1],
                (transfer_real + scale * root[0]) % P,
                (transfer_omega + scale * root[1]) % P,
            )

    visit(0, zero[0], zero[1], 0, 0)
    return tuple(sorted(result.items()))


def verify_transfer_formula(signatures: Sequence[SequenceSignature]) -> int:
    """Compare the short formula with the general logarithmic transfer."""

    checks = 0
    for fixture_index, signature in enumerate(sorted(set(signatures))):
        zero, active = decode_signature(signature)
        classes = [(0, 0)] * 12
        exact_sum = zero
        first = (0, 0)
        for local_index, (class_index, sign) in enumerate(active):
            root = ROOTS[(fixture_index + 2 * local_index) % 3]
            value = e_scale_integer(sign, root)
            classes[class_index] = value
            exact_sum = e_add_integer(
                exact_sum,
                e_scale_integer(3, value),
            )
            scale = (
                TRANSFER_FACTORS[1] * pow(8, class_index, P)
            ) % P
            first = (
                (first[0] + scale * value[0]) % P,
                (first[1] + scale * value[1]) % P,
            )

        transfer = class_log_transfer(zero, classes)
        if transfer[0] != e_reduce(exact_sum) or transfer[1] != first:
            raise AssertionError("the short phase transfer formula changed")
        zero_transfer = ((0, 0),) * 13
        direct_norm = norm_transfer(transfer, zero_transfer)[1]
        scalar = first_norm_coefficient(exact_sum, first)
        if direct_norm != (scalar, 2 * scalar % P):
            raise AssertionError("the first norm coefficient formula changed")
        checks += 1
    return checks


def audit_profile_tuple(
    target: Target,
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> dict[str, object]:
    signatures = tuple(
        sequence_signature(channel, residue, identifiers)
        for channel, identifiers in enumerate((identifiers_a, identifiers_b))
        for residue in range(3)
    )
    active_counts = tuple((len(signature) - 2) // 2 for signature in signatures)
    if sum(active_counts) != 54:
        raise AssertionError("a profile tuple lost its 54 active fibers")

    summaries = tuple(dict(sequence_summary(signature)) for signature in signatures)
    sequence_metadata = tuple(
        (
            active_count,
            3**active_count,
            sum(summary.values()),
            len(summary),
        )
        for active_count, summary in zip(
            active_counts, summaries
        )
    )

    augmentation: dict[int, int] = {0: 1}
    prefix: dict[tuple[int, int], int] = {(0, 0): 1}
    for summary in summaries:
        norm_marginal: defaultdict[int, int] = defaultdict(int)
        for (norm, _), count in summary.items():
            norm_marginal[norm] += count

        next_augmentation: defaultdict[int, int] = defaultdict(int)
        for left_norm, left_count in augmentation.items():
            for right_norm, right_count in norm_marginal.items():
                total_norm = left_norm + right_norm
                if total_norm <= 167:
                    next_augmentation[total_norm] += left_count * right_count
        augmentation = dict(next_augmentation)

        next_prefix: defaultdict[tuple[int, int], int] = defaultdict(int)
        for (left_norm, left_transfer), left_count in prefix.items():
            for (right_norm, right_transfer), right_count in summary.items():
                total_norm = left_norm + right_norm
                if total_norm <= 167:
                    next_prefix[
                        total_norm,
                        (left_transfer + right_transfer) % P,
                    ] += left_count * right_count
        prefix = dict(next_prefix)

    augmentation_survivors = augmentation.get(167, 0)
    prefix_survivors = prefix.get((167, 0), 0)
    return {
        "target": target,
        "active_counts": active_counts,
        "raw_assignments": RAW_PHASE_ASSIGNMENTS,
        "sequence_metadata": sequence_metadata,
        "joined_prefix_states": len(prefix),
        "augmentation_survivors": augmentation_survivors,
        "prefix_survivors": prefix_survivors,
    }


def verify_diagonal_frame_prefix() -> dict[str, object]:
    audits = tuple(
        audit_profile_tuple(target, identifiers_a, identifiers_b)
        for target, identifiers_a, identifiers_b in PROFILE9_SHARD_WITNESSES
    )
    observed_counts = tuple(
        (
            audit["target"],
            audit["augmentation_survivors"],
            audit["prefix_survivors"],
        )
        for audit in audits
    )
    if observed_counts != EXPECTED_COUNTS:
        raise AssertionError("the diagonal-prefix count corpus changed")

    signatures = tuple(
        sequence_signature(channel, residue, identifiers)
        for _, identifiers_a, identifiers_b in PROFILE9_SHARD_WITNESSES
        for channel, identifiers in enumerate((identifiers_a, identifiers_b))
        for residue in range(3)
    )
    transfer_checks = verify_transfer_formula(signatures)

    payload = tuple(
        (
            audit["target"],
            audit["active_counts"],
            audit["sequence_metadata"],
            audit["joined_prefix_states"],
            audit["augmentation_survivors"],
            audit["prefix_survivors"],
        )
        for audit in audits
    )
    result_hash = compact_hash(payload)
    if EXPECTED_RESULT_SHA256 and result_hash != EXPECTED_RESULT_SHA256:
        raise AssertionError("the diagonal-prefix result hash changed")

    return {
        "profile_tuples": len(audits),
        "raw_assignments_per_tuple": RAW_PHASE_ASSIGNMENTS,
        "transfer_formula_checks": transfer_checks,
        "largest_sequence_summary": max(
            metadata[3]
            for audit in audits
            for metadata in audit["sequence_metadata"]
        ),
        "largest_joined_prefix": max(
            audit["joined_prefix_states"] for audit in audits
        ),
        "smallest_prefix_survivors": min(
            audit["prefix_survivors"] for audit in audits
        ),
        "largest_prefix_survivors": max(
            audit["prefix_survivors"] for audit in audits
        ),
        "profile_tuples_surviving_prefix": sum(
            audit["prefix_survivors"] > 0 for audit in audits
        ),
        "result_sha256": result_hash,
        "full_diagonal_assignments_asserted": 0,
    }


def main() -> None:
    result = verify_diagonal_frame_prefix()
    print(f"profile_tuples={result['profile_tuples']}")
    print(f"raw_assignments_per_tuple={result['raw_assignments_per_tuple']}")
    print(f"transfer_formula_checks={result['transfer_formula_checks']}")
    print(f"largest_sequence_summary={result['largest_sequence_summary']}")
    print(f"largest_joined_prefix={result['largest_joined_prefix']}")
    print(
        "prefix_survivor_range="
        f"{result['smallest_prefix_survivors']}.."
        f"{result['largest_prefix_survivors']}"
    )
    print(f"result_sha256={result['result_sha256']}")
    print("PASS: diagonal-frame augmentation and T1 counts replayed")
    print("STATUS: all 22 fixed profile tuples survive this exact prefix")
    print("STATUS: no complete diagonal frame, LP(333), or H(668) asserted")


if __name__ == "__main__":
    main()
