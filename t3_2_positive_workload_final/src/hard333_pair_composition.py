"""Claim-neutral pair-composition split inside the hard 333 family.

The repaired dormant/generalized resolvent is a local common-factorial
episode.  This module freezes the exact subset on which every other failed
dimension is compatible with that same corrected factorial potential, and
separates the remaining all-active workload switches.  It makes no analytic
or recurrence claim.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import prospective_no_promotion_26 as atlas
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as flat
import three_active_gluing_gate as all_active
import two_active_dormant_407_certificate as hard
import two_active_phase_gate as two_active


Pair = closure.Pair

EXPECTED_COMMON_317_SHA256 = (
    "bc9d5ddd17f703b664b411f955dd6ae3b059729971428f922a40654fd6fd19e0"
)
EXPECTED_HB_12_SHA256 = (
    "7fcbd17c5571534a7e1bd50d218cfc56389c73a136c2fe0a73d3478ac2cf14fb"
)
EXPECTED_HW_4_SHA256 = (
    "4b24d4d3437351daf8e1d9b0e84e3d38e5e77147141a44fd9b68f6e1bba68716"
)
EXPECTED_SWITCH_16_SHA256 = (
    "35aa9260eedf3305abf6ec72704beec44394ecaa851ce7dc045e4d3c899d9896"
)
EXPECTED_AFTER_317_SHA256 = EXPECTED_SWITCH_16_SHA256
EXPECTED_ROWS_SHA256 = (
    "4cfe4964216dbec70989d6d4413161e170c9c0e8e8a54592c39d8c58dc7030aa"
)
EXPECTED_PAYLOAD_SHA256 = (
    "6ac4ef091ef771d377fb33e050fac9444236effe85c2838e11f48173d180ef75"
)


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def hb_switch_pairs() -> frozenset[Pair]:
    result = hard.selected_pairs() & frozenset(
        pair for pair, _descriptor, _excess in all_active.curvature_obstructions()
    )
    assert len(result) == 12
    assert closure.pair_fingerprint(result) == EXPECTED_HB_12_SHA256
    return result


def hw_switch_pairs() -> frozenset[Pair]:
    result = frozenset(
        pair
        for pair, descriptor in flat.feasible_all_active_incidences()
        if pair in hard.selected_pairs()
        and flat._support_rank(flat.whole_top_linkage(pair, descriptor)[1]) == 2
    )
    assert len(result) == 4
    assert closure.pair_fingerprint(result) == EXPECTED_HW_4_SHA256
    return result


def switch_pairs() -> frozenset[Pair]:
    assert not (hb_switch_pairs() & hw_switch_pairs())
    result = hb_switch_pairs() | hw_switch_pairs()
    assert len(result) == 16
    assert closure.pair_fingerprint(result) == EXPECTED_SWITCH_16_SHA256
    return result


def common_w_pairs() -> frozenset[Pair]:
    result = hard.selected_pairs() - switch_pairs()
    assert len(result) == 317
    assert closure.pair_fingerprint(result) == EXPECTED_COMMON_317_SHA256
    return result


def _two_active_categories() -> dict[Pair, set[str]]:
    result: dict[Pair, set[str]] = defaultdict(set)
    for pair, _descriptor, category in two_active.incidences():
        if pair in hard.selected_pairs():
            result[pair].add(category)
    return result


def _closed_top_masks() -> dict[Pair, set[int]]:
    result: dict[Pair, set[int]] = defaultdict(set)
    for pair, descriptor, category in two_active.incidences():
        if pair not in hard.selected_pairs() or category != "closed_rank_one_top_phase":
            continue
        tops = two_active._whole_top_linkages(pair, descriptor)
        top, = tops
        result[pair].add(top)
    return result


def _all_active_data() -> tuple[dict[Pair, set[str]], dict[Pair, set[int]]]:
    categories: dict[Pair, set[str]] = defaultdict(set)
    tops: dict[Pair, set[int]] = defaultdict(set)
    for pair, descriptor in flat.feasible_all_active_incidences():
        if pair not in hard.selected_pairs():
            continue
        _side, top = flat.whole_top_linkage(pair, descriptor)
        tops[pair].add(top)
        rank = flat._support_rank(top)
        if rank == 1 and top.bit_count() == 2:
            category = (
                "safe_reversible_two_node"
                if all_active.direct_entropy_safe(pair, descriptor)
                else "H_b_curvature_switch"
            )
        elif rank == 1 and top.bit_count() == 3:
            category = "directed_triple"
        elif rank == 2:
            category = "H_w_rank_two_switch"
        else:
            raise AssertionError((pair, descriptor, rank, top.bit_count()))
        categories[pair].add(category)
    return categories, tops


def common_rows() -> tuple[dict[str, object], ...]:
    two_categories = _two_active_categories()
    closed_tops = _closed_top_masks()
    all_categories, all_tops = _all_active_data()
    rows: list[dict[str, object]] = []

    for pair in sorted(common_w_pairs(), key=closure.pair_payload):
        active_profile = sorted(
            {
                len(tier._active_coordinates(descriptor))
                for descriptor in atlas.failures(pair)
            }
        )
        categories = sorted(all_categories.get(pair, set()))
        assert "H_b_curvature_switch" not in categories
        assert "H_w_rank_two_switch" not in categories
        if pair in closed_tops and pair in all_tops:
            assert closed_tops[pair] == all_tops[pair]
            assert len(closed_tops[pair]) == 1

        if "directed_triple" in categories:
            correction = "directed_triple_adjusted_ell"
        elif pair in closed_tops or "safe_reversible_two_node" in categories:
            correction = "reversible_top_adjusted_ell"
        else:
            correction = "arbitrary_fixed_ell"

        rows.append(
            {
                "pair": [list(part) for part in closure.pair_payload(pair)],
                "failure_active_profile": active_profile,
                "two_active_categories": sorted(two_categories[pair]),
                "all_active_categories": categories,
                "pair_fixed_correction_family": correction,
                "closed_and_all_active_top_masks_identical": (
                    pair not in closed_tops
                    or pair not in all_tops
                    or closed_tops[pair] == all_tops[pair]
                ),
            }
        )
    return tuple(rows)


def certificate() -> dict[str, object]:
    positive, signed, _residual = feasibility._residual_failures()
    common = common_w_pairs()
    switches = switch_pairs()
    rows = common_rows()
    rows_hash = _encoded_sha256(rows)
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256

    failure_histogram: Counter[int] = Counter()
    for pair in common:
        for descriptor in atlas.failures(pair):
            failure_histogram[len(tier._active_coordinates(descriptor))] += 1

    two_histogram: Counter[str] = Counter()
    for pair, _descriptor, category in two_active.incidences():
        if pair in common:
            two_histogram[category] += 1

    all_histogram: Counter[str] = Counter()
    all_categories, _all_tops = _all_active_data()
    for pair in common:
        for category in all_categories.get(pair, set()):
            # Each common pair has only one all-active category.  Count
            # incidences separately below to preserve the exact 66+24 split.
            assert category in {
                "safe_reversible_two_node",
                "directed_triple",
            }
    for pair, descriptor in flat.feasible_all_active_incidences():
        if pair not in common:
            continue
        _side, top = flat.whole_top_linkage(pair, descriptor)
        if top.bit_count() == 2:
            assert all_active.direct_entropy_safe(pair, descriptor)
            all_histogram["safe_reversible_two_node"] += 1
        else:
            assert flat._support_rank(top) == 1 and top.bit_count() == 3
            all_histogram["directed_triple"] += 1

    correction_histogram = Counter(
        row["pair_fixed_correction_family"] for row in rows
    )
    assert failure_histogram == {1: 1054, 2: 646, 3: 90}
    assert two_histogram == {
        "promotion_dormant_top": 391,
        "promotion_enabled_top_seed": 177,
        "closed_rank_one_top_phase": 78,
    }
    assert all_histogram == {
        "safe_reversible_two_node": 66,
        "directed_triple": 24,
    }
    assert correction_histogram == {
        "arbitrary_fixed_ell": 287,
        "reversible_top_adjusted_ell": 22,
        "directed_triple_adjusted_ell": 8,
    }

    remaining_16 = switches
    assert (len(common & positive), len(common & signed)) == (283, 34)
    assert (len(switches & positive), len(switches & signed)) == (16, 0)
    assert (len(remaining_16 & positive), len(remaining_16 & signed)) == (16, 0)
    assert closure.pair_fingerprint(remaining_16) == EXPECTED_AFTER_317_SHA256

    payload: dict[str, object] = {
        "claim_scope": (
            "exact claim-neutral common-potential and switch partition "
            "inside the hard 333 family; no analytic promotion"
        ),
        "parent_hard_333": {
            "pairs": 333,
            "positive": 299,
            "signed": 34,
            "pair_sha256": closure.pair_fingerprint(hard.selected_pairs()),
        },
        "candidate_common_w_317": {
            "pairs": 317,
            "positive": 283,
            "signed": 34,
            "pair_sha256": closure.pair_fingerprint(common),
            "failure_incidence_histogram": {
                str(key): value for key, value in sorted(failure_histogram.items())
            },
            "two_active_incidence_histogram": dict(sorted(two_histogram.items())),
            "all_active_incidence_histogram": dict(sorted(all_histogram.items())),
            "correction_family_histogram": dict(sorted(correction_histogram.items())),
            "all_closed_and_all_active_top_masks_match": all(
                row["closed_and_all_active_top_masks_identical"] for row in rows
            ),
        },
        "remaining_switch_16": {
            "pairs": 16,
            "positive": 16,
            "signed": 0,
            "pair_sha256": closure.pair_fingerprint(switches),
            "H_b_pairs": 12,
            "H_b_pair_sha256": closure.pair_fingerprint(hb_switch_pairs()),
            "H_w_pairs": 4,
            "H_w_pair_sha256": closure.pair_fingerprint(hw_switch_pairs()),
        },
        "claim_neutral_after_common_317": {
            "pairs": 16,
            "positive": 16,
            "signed": 0,
            "pair_sha256": closure.pair_fingerprint(remaining_16),
            "split": "sixteen all-active workload switches",
        },
        "rows": list(rows),
        "hashes": {"rows_sha256": rows_hash},
        "local_repaired_hard_kernel_independently_audited": False,
        "common_w_317_pair_recurrence_certified": False,
        "switch_16_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
