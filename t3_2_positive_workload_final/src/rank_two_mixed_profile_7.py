"""Claim-neutral certificate for the seven PF-activation rank-two pairs.

The seven pairs are the mixed-profile complement of
``rank_two_linear_switch_13`` inside the exact twenty-pair linear-workload
switch family.  This module freezes the carrier/lower-quadratic geometry
used by the stopped Perron--Frobenius activation-wedge lemma.  The analytic
lemma is awaiting independent audit, the interior-to-C-service seam is
open, and every recurrence flag remains false.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import one_active_relative_debt_cegar as graph
import one_active_remaining_structure as structure
import rank_two_linear_switch_13 as branch_13
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as all_active


Pair = closure.Pair

EXPECTED_PAIR_SHA256 = branch_13.EXPECTED_MIXED_SEVEN_SHA256
EXPECTED_ONE_ACTIVE_ROWS_SHA256 = (
    "8c5502bb4bc4b29fbb5c89512fbf4e796001735316b41b60f82d3c0add4dff72"
)
EXPECTED_NORMALIZED_PROFILES_SHA256 = (
    "4faa356b76299f937e7683fdf581fc229e30c40dd5ef51437e0ae9495b024ec6"
)
EXPECTED_PAYLOAD_SHA256 = (
    "0a3a9e20b07cc4a3d36429d98dd12db6ce56e0f903ed6a926911e2cf57d9f0de"
)

CARRIER_NAMES = frozenset(("AC", "BC"))
LOWER_QUADRATIC_NAMES = frozenset(("2A", "2B", "AB"))


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def selected_pairs() -> frozenset[Pair]:
    result = branch_13.mixed_profile_seven()
    assert len(result) == 7
    assert closure.pair_fingerprint(result) == EXPECTED_PAIR_SHA256
    return result


def one_active_rows() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for pair in sorted(selected_pairs(), key=closure.pair_payload):
        for descriptor in branch_13.selector.failures(pair):
            active = tier._active_coordinates(descriptor)
            if len(active) != 1:
                continue
            normalized = structure._normalized(pair, descriptor)
            supports = tuple(normalized["supports"])
            caps = tuple(normalized["caps"])
            phases = tuple(
                structure._linkage_phase(support) for support in supports
            )
            assert supports[0] == ("0", "A")
            top = supports[1]
            carriers = tuple(
                name for name in top if name in CARRIER_NAMES
            )
            lower_quadratics = tuple(
                name for name in top if name in LOWER_QUADRATIC_NAMES
            )
            assert set(carriers) == CARRIER_NAMES
            assert 2 <= len(lower_quadratics) <= 3
            assert set(top) == set(carriers) | set(lower_quadratics)
            category = graph._family_i_category(supports, phases)
            assert category == "family_i_origin_down_0"
            rows.append(
                {
                    "pair": [
                        list(part) for part in closure.pair_payload(pair)
                    ],
                    "physical_weight": list(descriptor.weight),
                    "physical_caps": list(descriptor.caps),
                    "physical_active_species": "ABC"[active[0]],
                    "normalized_supports": [list(item) for item in supports],
                    "normalized_caps": list(caps),
                    "normalized_active_species": "C",
                    "lower_birth_death_support": ["0", "A"],
                    "carrier_nodes": list(carriers),
                    "lower_quadratic_nodes": list(lower_quadratics),
                    "graph_category": category,
                }
            )
    rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    return tuple(rows)


def normalized_profiles() -> tuple[dict[str, object], ...]:
    counts: Counter[tuple[object, ...]] = Counter()
    for row in one_active_rows():
        key = (
            tuple(tuple(item) for item in row["normalized_supports"]),
            tuple(row["normalized_caps"]),
        )
        counts[key] += 1
    return tuple(
        {
            "normalized_supports": [list(item) for item in key[0]],
            "normalized_caps": list(key[1]),
            "physical_incidences": count,
        }
        for key, count in sorted(counts.items(), key=lambda item: repr(item[0]))
    )


def all_active_rows() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for pair in sorted(selected_pairs(), key=closure.pair_payload):
        descriptors = tuple(
            descriptor
            for descriptor in branch_13.selector.failures(pair)
            if len(tier._active_coordinates(descriptor)) == 3
        )
        descriptor, = descriptors
        side, top = all_active.whole_top_linkage(pair, descriptor)
        lower = pair[1 - side]
        assert descriptor.weight == (1, 1, 1)
        assert closure.support(lower) == ("0", "C")
        assert {
            sum(closure.COMPLEXES[node]) for node in tier._nodes(top)
        } == {2}
        rows.append(
            {
                "pair": [list(part) for part in closure.pair_payload(pair)],
                "top_support": list(closure.support(top)),
                "lower_support": ["0", "C"],
                "exact_workload": [1, 1, 1],
                "exact_generator": (
                    "L H=kappa_0C-kappa_C0*C"
                ),
            }
        )
    return tuple(rows)


def pair_arithmetic() -> dict[str, object]:
    positive, signed, _residual = feasibility._residual_failures()
    after_13 = (
        branch_13.selector.prospective_after_pairs()
        - branch_13.selector.selected_pairs()
        - branch_13.selected_pairs()
    )
    selected = selected_pairs()
    after_7 = after_13 - selected
    assert selected <= after_13
    assert (len(selected & positive), len(selected & signed)) == (7, 0)
    assert (len(after_7 & positive), len(after_7 & signed)) == (713, 36)
    return {
        "claim_neutral_parent_after_13": {
            "positive": 720,
            "signed": 36,
            "total": 756,
            "pair_sha256": closure.pair_fingerprint(after_13),
        },
        "selected_7": {
            "positive": 7,
            "signed": 0,
            "total": 7,
            "pair_sha256": closure.pair_fingerprint(selected),
        },
        "claim_neutral_remainder_after_7": {
            "positive": 713,
            "signed": 36,
            "total": 749,
            "pair_sha256": closure.pair_fingerprint(after_7),
        },
    }


def certificate() -> dict[str, object]:
    rows = one_active_rows()
    profiles = normalized_profiles()
    all_rows = all_active_rows()
    assert len(rows) == 40
    assert len(profiles) == 20
    assert len(all_rows) == 7

    menu_histogram = Counter(
        ",".join(row["normalized_supports"][1]) for row in rows
    )
    cap_histogram = Counter(
        ",".join(map(str, row["normalized_caps"])) for row in rows
    )
    active_histogram = Counter(
        row["physical_active_species"] for row in rows
    )
    assert menu_histogram == {
        "2A,2B,AB,AC,BC": 10,
        "2A,2B,AC,BC": 10,
        "2A,AB,AC,BC": 10,
        "2B,AB,AC,BC": 10,
    }
    assert cap_histogram == {
        "0,0": 8,
        "0,1": 8,
        "0,2": 8,
        "1,0": 8,
        "2,0": 8,
    }
    assert active_histogram == {"A": 20, "B": 20}
    assert all(
        row["graph_category"] == "family_i_origin_down_0"
        for row in rows
    )

    hashes = {
        "one_active_rows_sha256": _encoded_sha256(rows),
        "normalized_profiles_sha256": _encoded_sha256(profiles),
    }
    if EXPECTED_ONE_ACTIVE_ROWS_SHA256 != "TO_BE_FILLED":
        assert hashes["one_active_rows_sha256"] == EXPECTED_ONE_ACTIVE_ROWS_SHA256
    if EXPECTED_NORMALIZED_PROFILES_SHA256 != "TO_BE_FILLED":
        assert (
            hashes["normalized_profiles_sha256"]
            == EXPECTED_NORMALIZED_PROFILES_SHA256
        )

    payload: dict[str, object] = {
        "claim_scope": (
            "exact seven-pair selector and finite premises for the "
            "candidate stopped PF activation-wedge lemma only"
        ),
        "selector": {
            "pairs": len(selected_pairs()),
            "pair_sha256": closure.pair_fingerprint(selected_pairs()),
            "one_active_incidences": len(rows),
            "two_active_incidences": 0,
            "all_active_incidences": len(all_rows),
            "failed_active_profile": [1, 3],
        },
        "normalized_one_active_geometry": {
            "profiles": len(profiles),
            "menu_histogram": dict(sorted(menu_histogram.items())),
            "cap_histogram": dict(sorted(cap_histogram.items())),
            "physical_active_species_histogram": dict(
                sorted(active_histogram.items())
            ),
            "all_lower_linkages_are_0_A": True,
            "all_top_linkages_have_exact_carriers_AC_BC": True,
            "all_top_linkages_have_two_or_three_lower_quadratics": True,
            "all_graph_rows_are_family_i_origin_down_0": True,
        },
        "orientation_independent_pf_premise": {
            "carrier_set": ["AC", "BC"],
            "lower_quadratic_universe": ["2A", "2B", "AB"],
            "statement": (
                "in every strong orientation each closed carrier-only "
                "class has an outgoing split edge to a lower quadratic"
            ),
            "killed_carrier_generator_is_transient": True,
            "candidate_weight_construction": (
                "h=(-Q)^(-1)1; v=1-epsilon*h"
            ),
            "candidate_generator_bound": (
                "L_top R >= c*X*R-K*R^2"
            ),
        },
        "candidate_stopped_wedge_contract": {
            "proper_function": (
                "V_p=(1+H)^p*exp(-a*R/(1+H))"
            ),
            "stopped_region": (
                "R<=eta*(1+H), h0/M<=1+H<=M*h0"
            ),
            "candidate_drift": (
                "L V_p<=-c*(1+H)^(p-1)"
            ),
            "candidate_duration_bound": "E tau^m <= C_m*h0^m",
            "candidate_endpoint_bound": (
                "1+H_tau is between h0/M-O(1) and M*h0+O(1)"
            ),
            "upward_shell_exit_probability": (
                "P(1+H_tau>=M*h0)<=exp(a*v_max)*M^(-p)"
            ),
            "independent_audit_verdict": "PENDING",
        },
        "remaining_open_seam": (
            "from R>=eta*(1+H), obtain rate-uniform access to sustained "
            "physical C-service and compose it with exact H descent"
        ),
        "pair_arithmetic": pair_arithmetic(),
        "hashes": hashes,
        "analytic_stopped_wedge_independently_certified": False,
        "interior_service_access_certified": False,
        "candidate_7_pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
