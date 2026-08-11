"""Exact selector arithmetic for the certified one-active composition.

The accompanying note supplies the classwise common-potential proof.  This
module freezes its finite selector inputs, disjoint arithmetic, and
independently audited pair-level status.  Global T3-2 remains false.
"""

from __future__ import annotations

from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import one_active_phase_shape as phase_shape
import one_active_prospective_composition as prospective
import one_active_relative_debt_cegar as graph
import stoichiometric_gate_feasibility as feasibility
import universal_fourth_power_interface_regression as interface


Pair = closure.Pair

EXPECTED_CANDIDATE_SHA256 = prospective.EXPECTED_CANDIDATE_SHA256
EXPECTED_OVERLAP_SHA256 = (
    "6ec74f95e50e39ecda002b988d8233ae74c040ff9bb3518892dfd980bfad06d3"
)
EXPECTED_NEW_SHA256 = prospective.EXPECTED_NEW_SHA256
EXPECTED_AFTER_SHA256 = prospective.EXPECTED_AFTER_SHA256
EXPECTED_PAYLOAD_SHA256 = (
    "85847255a93aafd1a6fb4fde862f7e35cc3aadffa04cce01794541e0841ef8d6"
)


def pair_sets() -> dict[str, frozenset[Pair]]:
    branches = prospective.certified_branch_sets()
    current = frozenset().union(*branches.values())
    candidate = frozenset(phase_shape.candidate_pairs())
    overlap = candidate & current
    new = candidate - current
    _positive, _signed, residual = feasibility._residual_failures()
    after = residual - current - new
    return {
        "candidate_1227": candidate,
        "already_certified_overlap_15": overlap,
        "new_disjoint_1212": new,
        "remainder_after_795": after,
    }


def certificate() -> dict[str, object]:
    positive, signed, residual = feasibility._residual_failures()
    sets = pair_sets()
    candidate = sets["candidate_1227"]
    overlap = sets["already_certified_overlap_15"]
    new = sets["new_disjoint_1212"]
    after = sets["remainder_after_795"]

    prospective_payload = prospective.certificate()
    graph_payload = graph.graph_architecture_certificate()
    interface_payload = interface.certificate()
    incidences = phase_shape.candidate_incidences()
    assert len(incidences) == 3297
    assert all(
        len(tier._active_coordinates(descriptor)) == 1
        for _pair, descriptor in incidences
    )

    counts = {
        "candidate_1227": {
            "positive": len(candidate & positive),
            "signed": len(candidate & signed),
            "total": len(candidate),
        },
        "already_certified_overlap_15": {
            "positive": len(overlap & positive),
            "signed": len(overlap & signed),
            "total": len(overlap),
        },
        "new_disjoint_1212": {
            "positive": len(new & positive),
            "signed": len(new & signed),
            "total": len(new),
        },
        "remainder_after_795": {
            "positive": len(after & positive),
            "signed": len(after & signed),
            "total": len(after),
        },
    }
    assert counts == {
        "candidate_1227": {"positive": 1076, "signed": 151, "total": 1227},
        "already_certified_overlap_15": {
            "positive": 15,
            "signed": 0,
            "total": 15,
        },
        "new_disjoint_1212": {
            "positive": 1061,
            "signed": 151,
            "total": 1212,
        },
        "remainder_after_795": {
            "positive": 759,
            "signed": 36,
            "total": 795,
        },
    }
    assert len(residual) == 2511

    fingerprints = {
        name: closure.pair_fingerprint(pairs)
        for name, pairs in sets.items()
    }
    assert fingerprints == {
        "candidate_1227": EXPECTED_CANDIDATE_SHA256,
        "already_certified_overlap_15": EXPECTED_OVERLAP_SHA256,
        "new_disjoint_1212": EXPECTED_NEW_SHA256,
        "remainder_after_795": EXPECTED_AFTER_SHA256,
    }
    assert (
        prospective_payload["fingerprints"]["prospective_new_1212"]
        == EXPECTED_NEW_SHA256
    )
    assert graph_payload["candidate_pairs"] == 1227
    assert graph_payload["candidate_incidences"] == 3297
    assert graph_payload["arbitrary_strong_orientation_graph_theorem_certified"]
    assert interface_payload["analytic_templates"] == 23
    assert interface_payload["all_23_moving_cutoff_promotion_access_certified"]
    assert interface_payload[
        "graph_resistance_to_aggregate_kernel_analytic_lift_certified"
    ]

    payload: dict[str, object] = {
        "claim_scope": (
            "independently audited exact candidate-1227/net-1212 selector "
            "and common-potential pair recurrence theorem"
        ),
        "orientation_scope": (
            "every strongly connected orientation and every positive rate vector"
        ),
        "common_potential": {
            "factorial_linear_correction": 0,
            "power": 4,
            "proper_on_population_space": True,
        },
        "analytic_inputs": {
            "affine_feasible_failures_all_one_active": True,
            "arbitrary_orientation_graph_resistance_certified": True,
            "all_23_physical_kernel_interface_certified_locally": True,
            "random_up_overshoot_uses_q_strictly_above": 8,
            "all_species_reflected_finite_target_used": True,
            "classwise_family_ii_cap_constants": True,
        },
        "counts": counts,
        "candidate_one_active_incidences": len(incidences),
        "fingerprints": fingerprints,
        "independent_audit": {
            "verdict": "pass",
            "confidence": "0.91",
            "audited_note_sha256": (
                "652e41ccd7ae36183862a798fcdfd3bd5acf92ab2528bb356816d14df003b09a"
            ),
        },
        "composition_note_complete_for_audit": True,
        "candidate_1227_recurrence_certified": True,
        "new_disjoint_1212_recurrence_certified": True,
        "global_t3_2_certified": False,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
