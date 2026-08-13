"""Claim-neutral obstruction certificate for the hard-333 switch sixteen.

The exact sixteen-pair complement in :mod:`hard333_pair_composition`
contains twelve ``H_b`` curvature seams and four homogeneous rank-two
``H_w`` seams.  This module freezes their failed descriptors and two exact
rate/orientation examples showing that the direct scalar

    W_ell + eta * (1 + H)**q

cannot simply be placed on top of the repaired hard ``W_ell`` episode.
It is an obstruction to that composition, not to recurrence.  Every
analytic, pair-recurrence, and global flag remains false.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import hard333_pair_composition as composition
import prospective_no_promotion_26 as atlas
import three_active_flat_phase as flat
import three_active_gluing_gate as all_active
import two_active_dormant_407_certificate as hard


Pair = closure.Pair

EXPECTED_SWITCH_PAIR_SHA256 = composition.EXPECTED_SWITCH_16_SHA256
EXPECTED_ROWS_SHA256 = (
    "44e7fbb28583a880d5a3f0f11510c117484c48a20930ef61e4c26a6616a11931"
)
EXPECTED_PAYLOAD_SHA256 = (
    "412604c04682ff0483af12df4222ff9d3043422cb454fcde733b445835b63a0c"
)


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _pair_payload(pair: Pair) -> list[list[str]]:
    return [list(part) for part in closure.pair_payload(pair)]


@lru_cache(maxsize=1)
def _selectors() -> tuple[frozenset[Pair], frozenset[Pair], frozenset[Pair]]:
    hb_pairs = composition.hb_switch_pairs()
    hw_pairs = composition.hw_switch_pairs()
    assert not (hb_pairs & hw_pairs)
    selected = hb_pairs | hw_pairs
    assert len(selected) == 16
    assert closure.pair_fingerprint(selected) == EXPECTED_SWITCH_PAIR_SHA256
    return selected, hb_pairs, hw_pairs


def _failure_histogram(pair: Pair) -> dict[str, int]:
    counts = Counter(
        len(tier._active_coordinates(descriptor))
        for descriptor in atlas.failures(pair)
    )
    return {str(key): value for key, value in sorted(counts.items())}


def _hard_row_lookup() -> dict[str, dict[str, object]]:
    return {
        json.dumps(row["pair"], separators=(",", ":")): row
        for row in hard.normalized_rows()
    }


def _all_active_lookup(
    selected: frozenset[Pair],
) -> dict[Pair, list[tuple[tier.TierDescriptor, int]]]:
    excess = {
        (pair, descriptor): value
        for pair, descriptor, value in all_active.curvature_obstructions()
    }
    result: dict[Pair, list[tuple[tier.TierDescriptor, int]]] = {}
    for pair, descriptor in flat.feasible_all_active_incidences():
        if pair not in selected:
            continue
        result.setdefault(pair, []).append(
            (descriptor, excess.get((pair, descriptor), 0))
        )
    return result


def switch_rows() -> tuple[dict[str, object], ...]:
    """Freeze all failed profiles and the hard/all-active potential seam."""

    selected, hb_pairs, hw_pairs = _selectors()
    hard_rows = _hard_row_lookup()
    all_rows = _all_active_lookup(selected)
    rows: list[dict[str, object]] = []
    for pair in sorted(selected, key=closure.pair_payload):
        payload = _pair_payload(pair)
        hard_row = hard_rows[json.dumps(payload, separators=(",", ":"))]
        incidences: list[dict[str, object]] = []
        workload_menu: set[tuple[int, int, int]] = set()
        for descriptor, excess in all_rows[pair]:
            side, top = flat.whole_top_linkage(pair, descriptor)
            rank = flat._support_rank(top)
            incidence: dict[str, object] = {
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "top_support": list(closure.support(top)),
                "top_rank": rank,
                "curvature_excess": excess,
            }
            if excess:
                workload = all_active.curvature_obstruction_workload(
                    pair, descriptor
                )
                workload_menu.add(workload)
                incidence["curvature_workload"] = list(workload)
            incidences.append(incidence)
        incidences.sort(key=lambda row: json.dumps(row, sort_keys=True))

        if pair in hb_pairs:
            branch = "H_b_curvature_12"
            assert hard._resistance_class(hard_row) in (1, 2)
            assert tuple(hard_row["proper_support"]) == ("2U", "VI")
            assert workload_menu in ({(2, 1, 3)}, {(2, 3, 1)})
            switch_workload = (
                "2A+bB+(4-b)C"
                if workload_menu == {(2, 1, 3)}
                else "2A+(4-b)B+bC"
            )
            all_active_power_requirement = "q>21/5"
            hard_episode_power_requirement = "q<=4"
        else:
            branch = "H_w_rank_two_4"
            assert pair in hw_pairs
            assert hard._resistance_class(hard_row) == 0
            assert flat._support_rank(pair[hard_row["proper_side"]]) == 2
            assert {
                tuple(item["weight"]) for item in incidences
            } == {(1, 1, 1)}
            switch_workload = "A+B+C"
            all_active_power_requirement = "q>5"
            hard_episode_power_requirement = "q<=14/3"

        rows.append(
            {
                "pair": payload,
                "branch": branch,
                "failure_incidence_histogram": _failure_histogram(pair),
                "hard_dormant_row": {
                    "weight": hard_row["weight"],
                    "caps": hard_row["caps"],
                    "normalized_ratio": hard_row["normalized_ratio"],
                    "proper_support": hard_row["proper_support"],
                    "other_support": hard_row["other_support"],
                    "resistance": hard._resistance_class(hard_row),
                },
                "all_active_incidences": incidences,
                "switch_workload": switch_workload,
                "branch_witness_all_active_power_requirement": (
                    all_active_power_requirement
                ),
                "branch_witness_unchanged_hard_episode_power_requirement": (
                    hard_episode_power_requirement
                ),
                "direct_branch_scalar_interval_is_empty": True,
            }
        )
    assert len(rows) == 16
    return tuple(rows)


def hb_exact_obstruction() -> dict[str, object]:
    """One exact curvature/service exponent conflict on an H_b pair."""

    pair = next(
        pair
        for pair in _selectors()[1]
        if closure.pair_payload(pair)
        == (("2A", "BC"), ("0", "A", "2B", "AB"))
    )
    workload = (2, 1, 3)
    top_values = {
        sum(
            workload[index] * closure.COMPLEXES[node][index]
            for index in range(3)
        )
        for node in tier._nodes(pair[0])
    }
    assert top_values == {4}

    all_active_threshold = Fraction(21, 5)
    hard_endpoint_threshold = Fraction(4, 1)
    assert hard_endpoint_threshold < all_active_threshold
    return {
        "pair": _pair_payload(pair),
        "orientations_and_rates": {
            "top": "2A<->BC, both rates 1",
            "lower": "0->A->AB->2B->0, all rates 1",
        },
        "workload": "H_B=2A+B+3C",
        "top_is_exactly_H_B_neutral": True,
        "all_active_curvature_center": {
            "state": "(A,B,C)=(N^3,N,N^5)",
            "W_top_positive_order": "N^20*(log N)^3",
            "leading_negative_HBq_order": "N^(5q-1)",
            "necessary_power": "q>21/5",
        },
        "hard_service_scale": {
            "state": "(A,B,C)=(s,0,s^3)",
            "asymptotically_dominant_service_word": "A->AB; BC->2A",
            "endpoint": "(s+2,0,s^3-1)",
            "exact_HB_increment": 1,
            "W_decrease_order": "-s^9*(log s)^4",
            "positive_HBq_cost_order": "s^(3q-3)",
            "necessary_power": "q<=4",
        },
        "empty_power_interval": True,
    }


def hw_exact_obstruction() -> dict[str, object]:
    """One exact flat-interior/rare-birth conflict on an H_w pair."""

    pair = next(
        pair
        for pair in _selectors()[2]
        if closure.pair_payload(pair)
        == (("0", "C"), ("2A", "2C", "AC", "BC"))
    )
    total = (1, 1, 1)
    top = pair[1]
    top_values = {
        sum(
            total[index] * closure.COMPLEXES[node][index]
            for index in range(3)
        )
        for node in tier._nodes(top)
    }
    assert top_values == {2}

    all_active_threshold = Fraction(5, 1)
    hard_endpoint_threshold = Fraction(14, 3)
    assert hard_endpoint_threshold < all_active_threshold
    return {
        "pair": _pair_payload(pair),
        "orientations_and_rates": {
            "top_cycle": "2A->AC->2C->BC->2A",
            "top_rates_in_cycle_order": [10, 1, 1, 1],
            "lower": "0<->C, both rates 1",
        },
        "workload": "H=A+B+C",
        "top_is_exactly_H_neutral": True,
        "all_active_flat_sequence": {
            "state": "(A,B,C)=(N,N,2N)",
            "leading_F_drift_coefficient": "6*log(2)>0",
            "W_positive_order": "N^5*(log N)^3",
            "negative_Hq_service_order": "N^q",
            "necessary_power": "q>5",
        },
        "hard_service_scale": {
            "state": "(A,B,C)=(s,s^3,0)",
            "ordinary_top_service_word": "2A->AC; BC->2A",
            "ordinary_endpoint": "(s+1,s^3-1,0)",
            "rare_birth_service_word": "0->C; BC->2A",
            "rare_birth_endpoint": "(s+2,s^3-1,0)",
            "rare_birth_probability_order": "s^-2",
            "exact_total_increment_on_rare_birth_endpoint": 1,
            "W_decrease_order": "-s^9*(log s)^4",
            "positive_Hq_cost_order": "s^(3q-5)",
            "necessary_power": "q<=14/3",
        },
        "empty_power_interval": True,
    }


def certificate() -> dict[str, object]:
    rows = switch_rows()
    rows_hash = _encoded_sha256(rows)
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256

    branch_histogram = Counter(row["branch"] for row in rows)
    failure_histogram: Counter[str] = Counter()
    curvature_incidences = 0
    for row in rows:
        failure_histogram.update(row["failure_incidence_histogram"])
        curvature_incidences += sum(
            item["curvature_excess"] > 0
            for item in row["all_active_incidences"]
        )
    assert branch_histogram == {"H_b_curvature_12": 12, "H_w_rank_two_4": 4}
    assert failure_histogram == {"1": 50, "2": 56, "3": 64}
    assert curvature_incidences == 16

    hb = hb_exact_obstruction()
    hw = hw_exact_obstruction()
    payload: dict[str, object] = {
        "claim_scope": (
            "exact switch-16 descriptors and counterexamples to direct "
            "additive power scalarization of the repaired hard W episode"
        ),
        "selector": {
            "pairs": 16,
            "positive": 16,
            "signed": 0,
            "pair_sha256": closure.pair_fingerprint(
                _selectors()[0]
            ),
            "branch_histogram": dict(sorted(branch_histogram.items())),
            "failure_incidence_histogram": dict(
                sorted(failure_histogram.items())
            ),
            "curvature_obstruction_incidences": curvature_incidences,
        },
        "direct_scalar_class": "W_ell+eta*(1+H)^q, eta>0 fixed",
        "H_b_exact_obstruction": hb,
        "H_w_exact_obstruction": hw,
        "conclusion": (
            "no fixed power q directly glues the unchanged hard W episode "
            "to the all-active switch workload on these witnesses"
        ),
        "remaining_transfer_obligation": (
            "a marked regenerative block must repay every positive switch-"
            "workload seed before changing from W_ell to the all-active "
            "workload potential"
        ),
        "rows": list(rows),
        "hashes": {"rows_sha256": rows_hash},
        "independent_analytic_audit_passed": False,
        "regenerative_switch_transfer_certified": False,
        "switch_16_pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
