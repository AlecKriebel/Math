"""Exact arithmetic for the certified universal one-active branch.

This module composes only executable support-pair selectors.  The analytic
pair theorem is certified separately in
``one_active_fourth_power_pair_composition``; global T3-2 remains false.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json

import all_active_only_recurrence as all_active_only
import critical_one_active_q_trace_certificate as critical
import global_atlas_interface_closure as closure
import one_active_phase_shape as one_active
import rank_one_no_promotion_branch as rank_one
import rank_two_return_certificate as rank_two
import stoichiometric_gate_feasibility as feasibility
import suppressed_promotion_orbit_certificate as suppressed
import two_active_promotion_obstruction as promotion


Pair = closure.Pair

EXPECTED_CURRENT_CERTIFIED_SHA256 = (
    "ae644ada7fa910e84270cc24d3871e0dd40842645a57a089363edb68ef5dbd17"
)
EXPECTED_CURRENT_REMAINDER_SHA256 = (
    "b6fd356af7be66969df256fa67b0c669f46fa42e5d75048f43573e58aba0f5f7"
)
EXPECTED_CANDIDATE_SHA256 = (
    "3ab28358663c45a089a5bdf4144c28573718b0c4f8b05472a0af208ca919fcf8"
)
EXPECTED_NEW_SHA256 = (
    "a7784a1f98da2fbadd70a62bc97fe852393cb410a24e666a6d6c246998f0f579"
)
EXPECTED_AFTER_SHA256 = (
    "6a1327e6c38bfcab30d334691415ba457e84d45d1dfe53d81df4c02aad868123"
)
EXPECTED_PAYLOAD_SHA256 = (
    "116f622500a9039def2b123a2cfe5c880cd0ebd7784a9c8714e1f56da945f9ef"
)


def certified_branch_sets() -> dict[str, frozenset[Pair]]:
    """The disjoint branches underlying the current (1820,187) remainder."""

    _positive, _signed, residual = feasibility._residual_failures()
    affine = frozenset(
        pair
        for pair in residual
        if not feasibility.feasible_failing_descriptors(pair)
    )
    return {
        "affine_stoichiometric_151": affine,
        "rank_two_14": frozenset(
            pair for pair, _descriptor in rank_two._rank_two_rows()
        ),
        "all_active_only_51": all_active_only.selected_pairs(),
        "rank_one_no_promotion_141": rank_one.candidate_pair_level_pairs(),
        "post_rank_one_one_active_92": rank_one.one_active_obstruction_pairs(),
        "two_active_promotion_36": promotion.pair_level_selector(),
        "suppressed_promotion_4": suppressed.selected_pairs(),
        "critical_one_active_15": critical.selected_pairs(),
    }


def certificate() -> dict[str, object]:
    positive, signed, residual = feasibility._residual_failures()
    branches = certified_branch_sets()
    branch_names = tuple(sorted(branches))

    pairwise_overlaps = {
        f"{left}|{right}": len(branches[left] & branches[right])
        for left, right in combinations(branch_names, 2)
    }
    assert not any(pairwise_overlaps.values())

    current_certified = frozenset().union(*branches.values())
    current_remainder = residual - current_certified
    candidate = frozenset(one_active.candidate_pairs())
    overlap_by_branch = {
        name: len(candidate & branch)
        for name, branch in sorted(branches.items())
    }
    candidate_overlap = candidate & current_certified
    prospective_new = candidate - current_certified
    prospective_after = residual - current_certified - prospective_new

    branch_payload = {
        name: {
            "pairs": len(branch),
            "positive": len(branch & positive),
            "signed": len(branch & signed),
            "sha256": closure.pair_fingerprint(branch),
        }
        for name, branch in sorted(branches.items())
    }

    assert len(residual) == 2511
    assert (len(positive), len(signed)) == (2312, 199)
    assert (len(current_certified & positive), len(current_certified & signed)) == (
        492,
        12,
    )
    assert (len(current_remainder & positive), len(current_remainder & signed)) == (
        1820,
        187,
    )
    assert len(candidate) == 1227
    assert (len(candidate & positive), len(candidate & signed)) == (1076, 151)
    assert overlap_by_branch == {
        "affine_stoichiometric_151": 0,
        "all_active_only_51": 0,
        "critical_one_active_15": 15,
        "post_rank_one_one_active_92": 0,
        "rank_one_no_promotion_141": 0,
        "rank_two_14": 0,
        "suppressed_promotion_4": 0,
        "two_active_promotion_36": 0,
    }
    assert candidate_overlap == branches["critical_one_active_15"]
    assert (len(prospective_new & positive), len(prospective_new & signed)) == (
        1061,
        151,
    )
    assert (len(prospective_after & positive), len(prospective_after & signed)) == (
        759,
        36,
    )

    fingerprints = {
        "current_certified": closure.pair_fingerprint(current_certified),
        "current_remainder": closure.pair_fingerprint(current_remainder),
        "candidate_1227": closure.pair_fingerprint(candidate),
        "candidate_current_overlap": closure.pair_fingerprint(
            candidate_overlap
        ),
        "prospective_new_1212": closure.pair_fingerprint(prospective_new),
        "prospective_after_795": closure.pair_fingerprint(prospective_after),
    }
    assert fingerprints["current_certified"] == EXPECTED_CURRENT_CERTIFIED_SHA256
    assert fingerprints["current_remainder"] == EXPECTED_CURRENT_REMAINDER_SHA256
    assert fingerprints["candidate_1227"] == EXPECTED_CANDIDATE_SHA256
    assert fingerprints["candidate_current_overlap"] == critical.EXPECTED_PAIR_SHA256
    assert fingerprints["prospective_new_1212"] == EXPECTED_NEW_SHA256
    assert fingerprints["prospective_after_795"] == EXPECTED_AFTER_SHA256

    payload: dict[str, object] = {
        "claim_scope": (
            "exact selector arithmetic for the independently audited "
            "candidate-1227/net-1212 pair recurrence theorem"
        ),
        "baseline": {"positive": 2312, "signed": 199, "total": 2511},
        "currently_certified": {
            "positive": 492,
            "signed": 12,
            "total": len(current_certified),
        },
        "current_remainder": {"positive": 1820, "signed": 187},
        "certified_branches": branch_payload,
        "certified_branch_pairwise_overlaps": pairwise_overlaps,
        "candidate_1227": {
            "positive": 1076,
            "signed": 151,
            "total": len(candidate),
        },
        "candidate_overlap_by_certified_branch": overlap_by_branch,
        "candidate_current_overlap": {
            "positive": 15,
            "signed": 0,
            "total": len(candidate_overlap),
            "branch": "critical_one_active_15",
        },
        "prospective_new_contribution": {
            "positive": 1061,
            "signed": 151,
            "total": len(prospective_new),
        },
        "prospective_after_remainder": {
            "positive": 759,
            "signed": 36,
            "total": len(prospective_after),
        },
        "fingerprints": fingerprints,
        "prospective_composition_recurrence_certified": True,
        "candidate_1227_recurrence_certified": True,
        "global_t3_2_certified": False,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
