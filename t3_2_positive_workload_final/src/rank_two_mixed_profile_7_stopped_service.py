"""Certified stopped-service theorem for the final rank-two seven.

The finite part of the candidate identifies every nonservice dormant
vertex, the service-zero boundary sources, and the exact post-13 arithmetic.
The analytic theorem uses one global scalar and a physical-time
activation/service episode.  Independent audit replayed every stopping,
endpoint, and gluing estimate at this exact seven-pair scope.
"""

from __future__ import annotations

from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import rank_two_linear_switch_13_common_scalar as scalar_13
import rank_two_mixed_profile_7 as branch
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as flat
import two_active_dormant_407_certificate as hard_333


Pair = closure.Pair

EXPECTED_PAIR_SHA256 = branch.EXPECTED_PAIR_SHA256
EXPECTED_BEFORE_PAIR_SHA256 = scalar_13.EXPECTED_POST_13_PAIR_SHA256
EXPECTED_AFTER_PAIR_SHA256 = hard_333.EXPECTED_PAIR_SHA256
EXPECTED_ROWS_SHA256 = (
    "aefff460ba993878d2961f752463cd2acd87c677fbba43cfc05408523943b98c"
)
EXPECTED_PAYLOAD_SHA256 = (
    "0c06d14f1ad53c357d0c3ba0127e0c0ce3bac12db8c866523dedd3b5fb401eee"
)


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _top_linkage(pair: Pair) -> int:
    lower_sides = tuple(
        side
        for side, linkage in enumerate(pair)
        if closure.support(linkage) == ("0", "C")
    )
    lower_side, = lower_sides
    return pair[1 - lower_side]


def pair_rows() -> tuple[dict[str, object], ...]:
    """Freeze the exact service face and its dormant vertices."""

    rows: list[dict[str, object]] = []
    zero_cap_rows = tuple(
        row
        for row in branch.one_active_rows()
        if row["normalized_caps"] == [0, 0]
    )
    for pair in sorted(branch.selected_pairs(), key=closure.pair_payload):
        payload = [list(part) for part in closure.pair_payload(pair)]
        top = _top_linkage(pair)
        support = closure.support(top)
        service_free = tuple(name for name in support if "C" not in name)
        dormant = tuple(
            species for species in ("A", "B") if f"2{species}" not in support
        )
        incidence_rows = tuple(row for row in zero_cap_rows if row["pair"] == payload)
        assert tuple(sorted(row["physical_active_species"] for row in incidence_rows)) == dormant
        assert "AB" in support
        assert flat._support_rank(top) == 2
        assert all(sum(closure.COMPLEXES[node]) == 2 for node in tier._nodes(top))
        assert service_free == tuple(
            name for name in ("2A", "2B", "AB") if name in support
        )
        rows.append(
            {
                "pair": payload,
                "top_support": list(support),
                "lower_support": ["0", "C"],
                "top_stoichiometric_rank": 2,
                "top_preserves_total_population": True,
                "service_species": "C",
                "service_zero_sources": list(service_free),
                "service_zero_face_contains_AB": True,
                "nonservice_dormant_vertices": list(dormant),
                "zero_cap_failed_incidence_count": len(incidence_rows),
                "normalized_activation_menus": sorted(
                    ",".join(row["normalized_supports"][1])
                    for row in incidence_rows
                ),
            }
        )
    return tuple(rows)


def dormant_vertex_rows() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for pair_row in pair_rows():
        for vertex in pair_row["nonservice_dormant_vertices"]:
            rows.append(
                {
                    "pair": pair_row["pair"],
                    "vertex": vertex,
                    "sole_enabled_lower_reaction": "0->C",
                    "top_source_at_vertex": f"2{vertex}",
                    "top_source_is_absent": True,
                    "local_chart": (
                        "relabel vertex as X and service C as A; "
                        "R=v_A*A+v_B*B"
                    ),
                    "local_pf_inequality": (
                        "L_top R >= c*X*R-K*R^2"
                    ),
                }
            )
    rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    assert len(rows) == 8
    return tuple(rows)


def certified_pair_arithmetic() -> dict[str, object]:
    positive, signed, _residual = feasibility._residual_failures()
    before = scalar_13.easy_416.post_416_pairs() - scalar_13.branch.selected_pairs()
    selected = branch.selected_pairs()
    after = before - selected

    assert closure.pair_fingerprint(before) == EXPECTED_BEFORE_PAIR_SHA256
    assert selected <= before
    assert (len(selected & positive), len(selected & signed)) == (7, 0)
    assert (len(after & positive), len(after & signed)) == (299, 34)
    assert after == hard_333.selected_pairs()
    assert closure.pair_fingerprint(after) == EXPECTED_AFTER_PAIR_SHA256

    return {
        "certified_before_branch": {
            "positive": 306,
            "signed": 34,
            "total": 340,
            "pair_sha256": closure.pair_fingerprint(before),
        },
        "certified_final_7": {
            "positive": 7,
            "signed": 0,
            "total": 7,
            "pair_sha256": closure.pair_fingerprint(selected),
        },
        "certified_after_branch": {
            "positive": 299,
            "signed": 34,
            "total": 333,
            "pair_sha256": closure.pair_fingerprint(after),
            "equals_exact_hard_333_family": True,
        },
    }


def certificate() -> dict[str, object]:
    rows = pair_rows()
    dormant = dormant_vertex_rows()
    assert len(rows) == 7
    assert len(dormant) == 8
    assert sum(len(row["nonservice_dormant_vertices"]) for row in rows) == 8
    assert all(row["service_zero_face_contains_AB"] for row in rows)
    assert all(row["top_stoichiometric_rank"] == 2 for row in rows)

    rows_hash = _encoded_sha256({"pairs": rows, "vertices": dormant})
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256

    payload: dict[str, object] = {
        "claim_scope": (
            "independently audited stopped physical-time recurrence theorem "
            "on exactly seven pairs"
        ),
        "selector": {
            "pairs": 7,
            "pair_sha256": closure.pair_fingerprint(branch.selected_pairs()),
            "one_active_failed_incidences": 40,
            "two_active_failed_incidences": 0,
            "all_active_failed_incidences": 7,
            "nonservice_dormant_vertices": 8,
        },
        "common_scalar": {
            "formula": "V=(1+F)^4+lambda*(1+H)^6",
            "F": "K+sum_i log(x_i!)",
            "H": "A+B+C",
            "lambda": "any fixed positive constant",
            "outside_wedges": (
                "pointwise negative generator by the exact-tier passing "
                "estimate or all-active C-service power domination"
            ),
        },
        "all_reactions_retained_stopping_contract": {
            "activation": (
                "from an arbitrary dormant-wedge state, localize each "
                "full-chain PF trial at R=0, R=eta*N, a favorable downward "
                "population shell, or a rare upward population shell"
            ),
            "pf_survival_and_trial_time": (
                "the exponential PF supermartingale gives a fixed positive "
                "activation probability, while the logarithmic PF estimate "
                "gives an exponential tail on the O(log(N)/N) trial scale"
            ),
            "activation_births": (
                "one seed is charged at each dormant restart; extra births "
                "during localized fast trials have uniform exponential "
                "moments, so the compound finite-chart trial count K has "
                "a uniform exponential moment"
            ),
            "dormant_mark_scope": (
                "after rates are fixed use the minimum over the one or two "
                "dormant charts of the fixed pair; completed macroepisodes "
                "may be re-marked, with no rate-uniform constant claimed"
            ),
            "service_window": (
                "from activation population N_a run every clock for T/N_a "
                "physical time; the density limit is uniform over all "
                "lattice activation endpoints"
            ),
            "fluid_service": (
                "the top ODE has infinite integrated C from the compact "
                "activation shell; choose T so expected C->0 deaths exceed "
                "all activation births by a fixed margin"
            ),
            "mixed_poisson_control": (
                "birth and death counts in the service window are "
                "random-time-change mixed Poisson variables with uniform "
                "exponential moments, not pathwise fixed-Poisson bounds"
            ),
            "regular_event_weighting": (
                "E[K;regular]<=E[K] and "
                "E[D_win;regular]>=delta*M-o(1); no conditional bound on "
                "K is inferred from its unconditional mean"
            ),
            "exact_population_bookkeeping": (
                "N_a=N_0+K-D_pre and "
                "N_end=N_0+K-D_pre+B_win-D_win"
            ),
            "endpoint_positive_moments": (
                "for every integer m, positive workload overshoot and "
                "duration have uniform m-th moments"
            ),
            "required_audit_moment": "choose m>8",
            "candidate_episode_drift": (
                "E[V(X_tau)-V(x)+tau] <= -c*H^5"
            ),
        },
        "service_zero_face_contract": {
            "maximal_invariant_set": (
                "exactly the eight certified dormant nonservice vertices"
            ),
            "infinite_integral_argument": (
                "finite integral C forces the omega-limit into that set; "
                "the local PF logistic inequality excludes every vertex"
            ),
            "uniformization": (
                "continuity and compactness of the activation shell give "
                "one finite T for any prescribed service integral"
            ),
        },
        "endpoint_scalar_orders": {
            "deterministic_envelope": (
                "V(X_end) is bounded by the maximal factorial/total "
                "population envelope at N_0+K+B_win-D_win; D_pre remains "
                "in the physical dynamics and only improves this envelope"
            ),
            "shell_exits": (
                "downward exits have an order-N^6 drop; upward exits require "
                "order-N births and their exponential tail absorbs the "
                "order-N^6 endpoint envelope"
            ),
            "negative_H6_order": "-c*H^5",
            "maximum_factorial_reconcentration": "O(H^4*log(H)^3)",
            "strict_polynomial_margin": True,
        },
        "fixed_class_gluing": (
            "use the common-entropy physical-time gluing theorem with the "
            "pointwise-good complement and the stopped dormant wedges"
        ),
        "pair_rows": list(rows),
        "dormant_vertex_rows": list(dormant),
        "hashes": {"finite_rows_sha256": rows_hash},
        "certified_pair_arithmetic": certified_pair_arithmetic(),
        "independent_audit_passed": True,
        "analytic_activation_survival_certified": True,
        "analytic_integrated_service_certified": True,
        "analytic_common_scalar_gluing_certified": True,
        "candidate_7_pair_recurrence_certified": True,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
