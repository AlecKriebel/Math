"""Claim-neutral killed-shell transfer target for the hard H_b twelve.

The twelve selected pairs have the same reversible top support
``2A <-> BC``.  A rate-adjusted factorial entropy is therefore the exact
negative logarithm of the finite top-shell stationary law.  This file
freezes a proposed *local* common-entropy episode: use ordinary pointwise
entropy descent outside a central top shell core, and inside that core stop
at the first lower-linkage reaction or at a wider guard boundary.

The construction deliberately does not use a global shell Poisson gauge,
does not infer mixing from a divergent number of top jumps, and does not
claim that one hard-boundary service episode repays an order-n shell mark.
Those three shortcuts are known to be invalid.  All analytic, recurrence,
and global flags remain false pending an independent proof and replay.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import hard333_pair_composition as composition
import prospective_no_promotion_26 as atlas
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as flat
import three_active_gluing_gate as all_active
import two_active_dormant_407_certificate as hard
import two_active_phase_gate as two_active


Pair = closure.Pair

EXPECTED_PAIR_SHA256 = composition.EXPECTED_HB_12_SHA256
EXPECTED_ROWS_SHA256 = (
    "6a5240865b78898be273738bb2e227ede2bcc3db46936864af995010bd53e572"
)
EXPECTED_PAYLOAD_SHA256 = (
    "e9d113351e2d67db0d93595b5adb351814834459f77b23d840c55f4eef9042f7"
)


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _pair_payload(pair: Pair) -> list[list[str]]:
    return [list(part) for part in closure.pair_payload(pair)]


@lru_cache(maxsize=1)
def selected_pairs() -> frozenset[Pair]:
    result = composition.hb_switch_pairs()
    assert len(result) == 12
    assert closure.pair_fingerprint(result) == EXPECTED_PAIR_SHA256
    return result


def _hard_rows() -> dict[str, dict[str, object]]:
    return {
        json.dumps(row["pair"], separators=(",", ":")): row
        for row in hard.normalized_rows()
    }


def geometry_rows() -> tuple[dict[str, object], ...]:
    """Freeze the exact top shells, curvature cores, and hard interfaces."""

    selected = selected_pairs()
    hard_rows = _hard_rows()
    obstructions: dict[Pair, list[tuple[object, int]]] = {}
    for pair, descriptor, excess in all_active.curvature_obstructions():
        if pair in selected:
            obstructions.setdefault(pair, []).append((descriptor, excess))

    rows: list[dict[str, object]] = []
    for pair in sorted(selected, key=closure.pair_payload):
        payload = _pair_payload(pair)
        top_sides = [
            side
            for side, linkage in enumerate(pair)
            if closure.support(linkage) == ("2A", "BC")
        ]
        top_side, = top_sides
        top = pair[top_side]
        lower = pair[1 - top_side]
        assert flat._support_rank(top) == 1
        assert top.bit_count() == 2

        hard_row = hard_rows[json.dumps(payload, separators=(",", ":"))]
        incidences: list[dict[str, object]] = []
        workloads: set[tuple[int, int, int]] = set()
        for descriptor, excess in obstructions[pair]:
            side, certified_top = flat.whole_top_linkage(pair, descriptor)
            assert side == top_side and certified_top == top
            workload = all_active.curvature_obstruction_workload(pair, descriptor)
            workloads.add(workload)
            incidences.append(
                {
                    "weight": list(descriptor.weight),
                    "caps": list(descriptor.caps),
                    "curvature_excess": excess,
                    "neutral_workload": list(workload),
                }
            )
        incidences.sort(key=lambda item: json.dumps(item, sort_keys=True))
        workload_menu = sorted(workloads)
        assert workload_menu in ([(2, 1, 3)], [(2, 3, 1)])
        assert tuple(hard_row["proper_support"]) == ("2U", "VI")

        rows.append(
            {
                "pair": payload,
                "top_support": ["2A", "BC"],
                "lower_support": list(closure.support(lower)),
                "top_rank": 1,
                "top_reversible_two_node": True,
                "top_preserves_total_population": True,
                "top_preserves_neutral_workload": True,
                "neutral_workload_menu": workload_menu,
                "curvature_incidences": incidences,
                "hard_dormant_resistance": hard._resistance_class(hard_row),
                "hard_dormant_proper_support": hard_row["proper_support"],
                "closed_and_all_active_top_mask_identical": True,
            }
        )
    assert len(rows) == 12
    return tuple(rows)


def claim_neutral_arithmetic() -> dict[str, object]:
    positive, signed, _residual = feasibility._residual_failures()
    selected = selected_pairs()
    assert (len(selected & positive), len(selected & signed)) == (12, 0)
    return {
        "candidate_H_b_12": {
            "pairs": 12,
            "positive": 12,
            "signed": 0,
            "pair_sha256": closure.pair_fingerprint(selected),
        },
        "claim_neutral_after": {
            "pairs": 12,
            "positive": 12,
            "signed": 0,
            "unchanged": True,
        },
    }


def lower_dimensional_routing() -> dict[str, object]:
    """Freeze the exhaustive non-all-active common-W menu on these pairs."""

    selected = selected_pairs()
    failure_histogram = Counter(
        len(tier._active_coordinates(descriptor))
        for pair in selected
        for descriptor in atlas.failures(pair)
    )
    two_histogram = Counter(
        category
        for pair, _descriptor, category in two_active.incidences()
        if pair in selected
    )
    selected_payloads = {closure.pair_payload(pair) for pair in selected}
    one_histogram = Counter(
        row["structural_family"]
        for row in hard.one_active_rows()
        if tuple(tuple(part) for part in row["pair"]) in selected_payloads
    )
    assert failure_histogram == {1: 38, 2: 48, 3: 60}
    assert two_histogram == {
        "closed_rank_one_top_phase": 36,
        "promotion_dormant_top": 12,
    }
    assert one_histogram == {
        "generalized_family_ii": 36,
        "direct_physical_C": 2,
    }
    return {
        "failure_incidence_histogram": {
            str(key): value for key, value in sorted(failure_histogram.items())
        },
        "two_active_48": {
            "closed_rank_one_top_phase": 36,
            "promotion_dormant_top": 12,
        },
        "one_active_38": {
            "generalized_family_ii": 36,
            "direct_physical_C": 2,
        },
        "central_guard_reached_before_dimension_loss": True,
        "single_dormant_handoff_is_exhaustive": False,
    }


def certificate() -> dict[str, object]:
    rows = geometry_rows()
    rows_hash = _encoded_sha256(rows)
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256

    resistance_histogram = Counter(
        row["hard_dormant_resistance"] for row in rows
    )
    excess_histogram = Counter(
        incidence["curvature_excess"]
        for row in rows
        for incidence in row["curvature_incidences"]
    )
    assert resistance_histogram == {1: 10, 2: 2}
    assert excess_histogram == {1: 12, 2: 4}

    payload: dict[str, object] = {
        "claim_scope": (
            "finite premises and unaudited killed-shell common-factorial "
            "transfer target for the exact hard H_b twelve"
        ),
        "selector": {
            "pairs": 12,
            "positive": 12,
            "signed": 0,
            "pair_sha256": closure.pair_fingerprint(selected_pairs()),
            "curvature_incidences": 16,
            "curvature_excess_histogram": {
                str(key): value for key, value in sorted(excess_histogram.items())
            },
            "hard_resistance_histogram": {
                str(key): value
                for key, value in sorted(resistance_histogram.items())
            },
        },
        "exact_top_shell_identity": {
            "top": "2A<->BC",
            "invariants": ["A+B+C", "2A+bB+(4-b)C"],
            "rate_adjustment": (
                "choose ell with exp(-ell dot (BC-2A))=kappa_+/kappa_-"
            ),
            "stationary_law": (
                "on every finite top shell, pi_q(x) is proportional to "
                "exp(-F_ell(x))"
            ),
            "birth_death_coordinate": (
                "lambda(a)=kappa_+*A*(A-1), "
                "mu(a)=kappa_-*B*C"
            ),
        },
        "candidate_local_episode": {
            "pointwise_complement": (
                "outside a fixed central core, exact top entropy "
                "dissipation absorbs curvature and the lower linkage"
            ),
            "central_start": (
                "start only where the shell displacement is O(one) "
                "stationary standard deviations from its kinetic mode"
            ),
            "stopping_rule": (
                "first lower-linkage reaction or first exit from a wider "
                "sqrt(log scale) guard tube"
            ),
            "top_endpoint_target": (
                "all stopped moments of F_ell(top endpoint)-F_ell(start) "
                "are O(1) by the mean-reverting birth-death shell"
            ),
            "lower_endpoint_target": (
                "conditional first-lower-reaction mean equals "
                "L_R F_ell/q_R and tends uniformly to -infinity"
            ),
            "guard_exit_target": (
                "for each target K, enlarge the guard coefficient to absorb "
                "the polynomial relaxation/kill ratio and obtain O(s^-K); "
                "its O(log scale) entropy toll is event-weighted"
            ),
            "all_reactions_retained": True,
        },
        "common_W_lift_target": {
            "potential": "W_ell=(K_ell+sum log(x_i!)+ell dot x)^4",
            "central_drift": (
                "E[W_ell(X_tau)-W_ell(x)+tau] "
                "<=-c*F_ell(x)^3*g(x), with g(x)->infinity"
            ),
            "endpoint_moment_order": "prove one uniform integer order p>8",
            "lower_dimensional_handoff": (
                "the central guard is hit while every center coordinate "
                "still diverges; separate lower-dimensional starts use the "
                "exact 48-row two-active and 38-row one-active common-W menu"
            ),
        },
        "withdrawn_shortcuts": {
            "global_mean_zero_poisson_gauge": {
                "valid": False,
                "exact_N4_corrected_drift": "16.971403723...>0",
            },
            "raw_first_R_after_divergent_top_flux": {
                "valid": False,
                "passing_witness": (
                    "at (N^6,N^10,N^11), the first-R factorial mean is "
                    "+log(N)+O(1)"
                ),
            },
            "single_hard_episode_repays_full_shell_mark": {
                "valid": False,
                "scale_mismatch": (
                    "fixed-shell factorial redistribution can cost O(n), "
                    "whereas one hard service gives only O(log n) in F"
                ),
            },
        },
        "geometry_rows": list(rows),
        "lower_dimensional_routing": lower_dimensional_routing(),
        "claim_neutral_arithmetic": claim_neutral_arithmetic(),
        "hashes": {"rows_sha256": rows_hash},
        "uniform_birth_death_moment_lemma_certified": False,
        "uniform_killed_lower_reward_certified": False,
        "guard_exit_charge_certified": False,
        "pointwise_core_complement_certified": False,
        "common_W_endpoint_certified": False,
        "H_b_12_pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
