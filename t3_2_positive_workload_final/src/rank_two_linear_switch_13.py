"""Claim-neutral selector for the thirteen all-active-only rank-two pairs.

These pairs are the part of the exact twenty-pair linear-workload switch
family whose affine-feasible failed descriptors are all three-active.  The
module freezes the finite support facts and an exact obstruction to using
the rank-two workload by itself on the passing boundary.  It does not close
the factorial/linear potential switch and makes no recurrence claim.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import prospective_26_candidate_theorem as candidate_26
import prospective_no_promotion_26 as selector
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as all_active


Pair = closure.Pair
Descriptor = tier.TierDescriptor

EXPECTED_PAIR_SHA256 = (
    "f089ad4dbf064da8512d4854e824c36216e3eb74655ec435d06eecc69fb4f27e"
)
EXPECTED_MIXED_SEVEN_SHA256 = (
    "93717536ce82eceefe6909c62568afab31e06695dada8b69defb93335d576957"
)
EXPECTED_ALL_ACTIVE_ROWS_SHA256 = (
    "674cfbd62561207b275036b4830521df499d9062c735a4296d4d93654360a8ec"
)
EXPECTED_AFTER_756_SHA256 = (
    "40e2df862df6730b03d5abce5decaf448cf6e851159d374c5706bdf4c0141397"
)
EXPECTED_PAYLOAD_SHA256 = (
    "6cdfc7ce551859d7fe72c374ff93a94a533305eff45e3553cbaffc24ebb714bf"
)


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def linear_switch_twenty() -> frozenset[Pair]:
    """The exact no-two-active complement of the audited 26-pair branch."""

    _no_two, linear = selector._no_two_active_split()
    return linear


def selected_pairs() -> frozenset[Pair]:
    """The thirteen pairs having no feasible one- or two-active failure."""

    result = frozenset(
        pair
        for pair in linear_switch_twenty()
        if selector.active_profile(pair) == frozenset((3,))
    )
    assert len(result) == 13
    assert closure.pair_fingerprint(result) == EXPECTED_PAIR_SHA256
    return result


def mixed_profile_seven() -> frozenset[Pair]:
    result = linear_switch_twenty() - selected_pairs()
    assert len(result) == 7
    assert all(
        selector.active_profile(pair) == frozenset((1, 3))
        for pair in result
    )
    assert closure.pair_fingerprint(result) == EXPECTED_MIXED_SEVEN_SHA256
    return result


def _all_active_descriptor(pair: Pair) -> Descriptor:
    descriptors = selector.failures(pair)
    assert len(descriptors) == 1
    descriptor, = descriptors
    assert len(tier._active_coordinates(descriptor)) == 3
    return descriptor


def canonical_boundary_descriptor(pair: Pair) -> Descriptor:
    """A feasible passing B-axis descriptor with C identically zero.

    The common descriptor has weight ``(0,1,0)`` and caps ``(0,2,0)``.
    It is affine feasible because every selected pair has full
    stoichiometric rank.  Its top D- and S-tier is the enabled pure-B
    source (``B`` or ``2B``), so the ordinary universal tier condition
    passes.  Nevertheless the exact linear workload has positive drift
    there because the lower linkage is ``0 <-> C`` and ``C=0``.
    """

    matches = tuple(
        descriptor
        for descriptor in tier.tier_descriptors()
        if descriptor.weight == (0, 1, 0)
        and descriptor.caps == (0, 2, 0)
    )
    descriptor, = matches
    assert feasibility.descriptor_feasible(pair, descriptor)
    assert tier.universal_orientation_tier_condition(pair, descriptor)
    return descriptor


def all_active_rows() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for pair in sorted(selected_pairs(), key=closure.pair_payload):
        descriptor = _all_active_descriptor(pair)
        side, top = all_active.whole_top_linkage(pair, descriptor)
        lower = pair[1 - side]
        workload = descriptor.weight
        top_levels = {
            sum(
                workload[index] * closure.COMPLEXES[node][index]
                for index in range(3)
            )
            for node in tier._nodes(top)
        }
        boundary = canonical_boundary_descriptor(pair)
        top_d, top_s = tier.tier_sets(pair, boundary)
        assert closure.support(lower) == ("0", "C")
        assert len(closure.full_rows(*pair)) == 3
        assert all(value > 0 for value in workload)
        assert len(top_levels) == 1
        assert top_d == top_s
        rows.append(
            {
                "pair": [list(part) for part in closure.pair_payload(pair)],
                "all_active_weight": list(workload),
                "top_support": list(closure.support(top)),
                "top_size": top.bit_count(),
                "top_workload_level": next(iter(top_levels)),
                "lower_support": ["0", "C"],
                "full_stoichiometric_rank": 3,
                "failed_active_profile": [3],
                "canonical_passing_boundary": {
                    "weight": list(boundary.weight),
                    "caps": list(boundary.caps),
                    "top_d": [closure.NAMES[node] for node in sorted(top_d)],
                    "top_s": [closure.NAMES[node] for node in sorted(top_s)],
                    "universal_tier_condition_passes": True,
                    "C_population": 0,
                    "exact_H_generator_sign": "positive",
                    "exact_H_generator": (
                        "w_C*kappa_0C > 0 when C=0"
                    ),
                },
            }
        )
    return tuple(rows)


def pair_arithmetic() -> dict[str, object]:
    positive, signed, residual = feasibility._residual_failures()
    parent_795 = selector.prospective_after_pairs()
    after_26 = parent_795 - selector.selected_pairs()
    post_26_certified = residual - after_26
    selected = selected_pairs()
    after_13 = after_26 - selected

    assert closure.pair_fingerprint(after_26) == candidate_26.EXPECTED_AFTER_769_SHA256
    assert selected <= after_26
    assert not (selected & post_26_certified)
    assert (len(selected & positive), len(selected & signed)) == (13, 0)
    assert (len(after_13 & positive), len(after_13 & signed)) == (720, 36)
    after_hash = closure.pair_fingerprint(after_13)
    if EXPECTED_AFTER_756_SHA256 != "TO_BE_FILLED":
        assert after_hash == EXPECTED_AFTER_756_SHA256

    return {
        "post_26_remainder": {
            "positive": 733,
            "signed": 36,
            "total": 769,
            "pair_sha256": closure.pair_fingerprint(after_26),
        },
        "selected_13": {
            "positive": 13,
            "signed": 0,
            "total": 13,
            "pair_sha256": closure.pair_fingerprint(selected),
            "post_26_certified_overlap": len(selected & post_26_certified),
        },
        "claim_neutral_remainder_after_13": {
            "positive": 720,
            "signed": 36,
            "total": 756,
            "pair_sha256": after_hash,
        },
    }


def certificate() -> dict[str, object]:
    rows = all_active_rows()
    rows_hash = _encoded_sha256(rows)
    if EXPECTED_ALL_ACTIVE_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ALL_ACTIVE_ROWS_SHA256

    workload_histogram = Counter(
        ",".join(map(str, row["all_active_weight"])) for row in rows
    )
    size_histogram = Counter(row["top_size"] for row in rows)
    assert workload_histogram == {"1,1,1": 11, "1,2,1": 1, "2,1,1": 1}
    assert size_histogram == {4: 8, 5: 4, 6: 1}
    assert all(row["failed_active_profile"] == [3] for row in rows)
    assert all(
        row["canonical_passing_boundary"][
            "universal_tier_condition_passes"
        ]
        and row["canonical_passing_boundary"]["exact_H_generator_sign"]
        == "positive"
        for row in rows
    )

    payload: dict[str, object] = {
        "claim_scope": (
            "exact thirteen-pair selector, rank-two workload premises, "
            "and passing-boundary H_w obstruction only"
        ),
        "linear_switch_twenty": {
            "pairs": len(linear_switch_twenty()),
            "pair_sha256": closure.pair_fingerprint(
                linear_switch_twenty()
            ),
        },
        "all_active_only_13": {
            "pairs": len(selected_pairs()),
            "pair_sha256": closure.pair_fingerprint(selected_pairs()),
            "failed_incidences": len(rows),
            "failed_active_profile": [3],
            "top_size_histogram": {
                str(key): value for key, value in sorted(size_histogram.items())
            },
            "workload_histogram": dict(sorted(workload_histogram.items())),
            "all_lower_supports_are_0_C": True,
            "all_top_reactions_preserve_H_w": True,
            "exact_all_active_generator": (
                "L H_w=w_C*(kappa_0C-kappa_C0*C)"
            ),
        },
        "mixed_profile_7": {
            "pairs": len(mixed_profile_seven()),
            "pair_sha256": closure.pair_fingerprint(mixed_profile_seven()),
            "status": "separate PF activation bridge open",
        },
        "passing_boundary_obstruction": {
            "common_descriptor_weight": [0, 1, 0],
            "common_descriptor_caps": [0, 2, 0],
            "all_13_affine_feasible": True,
            "all_13_universal_tier_condition_passes": True,
            "C_population": 0,
            "exact_H_generator": "w_C*kappa_0C > 0",
            "conclusion": (
                "H_w alone is not a global Foster function; a common "
                "scalar or stopped boundary-to-service episode is required"
            ),
        },
        "pair_arithmetic": pair_arithmetic(),
        "hashes": {"all_active_rows_sha256": rows_hash},
        "common_potential_switch_closed": False,
        "candidate_13_pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
