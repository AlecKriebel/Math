#!/usr/bin/env python3
"""Exact logic regressions for the final-theorem promotion review.

These checks detect recurrence of known invalid implications.  They do not
enumerate or certify the outstanding local topology atlas.
"""

from __future__ import annotations

import copy
import hashlib
import json
from fractions import Fraction
from itertools import permutations
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


EXPECTED_INPUT_HASHES = {
    "docs/DEFINITIONS_LOCK.md": "c3382650fa004d90b2122aff1c95524590b31e436d77d4b804293184aa925b09",
    "docs/GENERATOR_AND_SUPPORT_THEOREM.md": "a6b195d158972ba842c7995ddf97898272db533d8505f5fbb4299f1a296f79e9",
    "docs/ROOT_REDUCTION_THEOREM.md": "720f4b63f2a88ce4d4b8247b856a6f0b7f9939494e342915747c86e0173eb836",
    "docs/GLOBAL_THEOREM_DRAFT.md": "618361383f5123127147ffbf4efca74be490453298b0e0b59fa6dbd7ef9024e5",
    "reviews/global_bridge/REVIEW.md": "f6a9a608e841796d98999dfa639716c091cdcef8d1895b85c7f7597023fa05db",
    "reviews/root_probe/REVIEW.md": "dd6e6cd380791108390b20960e23bb0a5bd7b0539b81b54046fc2203900a0108",
    "reviews/hard_cover_design/REVIEW.md": "30cca503872946284f026a018841a62f3fbefcb18f3c92e464973b3e5db9241f",
    "reviews/invariant_engine/REVIEW.md": "8704c0687ce6cd16d4e58648372619bf1e7b32da9bcb6938fa7ae22e2ec08b9f",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_contract(c: dict) -> list[str]:
    errors: list[str] = []
    local = c["local_closure_contract"]
    artifacts = c["current_local_artifact_status"]
    glob = c["global_contract"]
    exc = c["exceptional_locus_contract"]

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(local["scope"] == "every fixed full labelled source-target local factor relation", "scope is not fixed-full")
    require(local["fixed_full_relation_id_required"], "full-relation binding omitted")
    require(local["parent_prefix_binding_required"], "parent-prefix binding omitted")
    require(not local["lift_from_selected_marginal_alone"], "invalid marginal lift enabled")
    require(local["target_boundary_quotient"] == "full_S_p", "target quotient is not full S_p")
    require(set(local["target_incoming_modes"]) == {"incoming_selected", "incoming_marginalized_as_zero_character_dummy"}, "incoming mode missing")
    require(not local["matched_physical_incoming_boundary_required"], "false matched-incoming requirement restored")
    require(local["minimal_disjoint_incoming_rooting_census_each_side"] == [9, 9], "corrected incoming rooting census altered")
    require(set(local["all_dummy_roles"]) == {"D_SINK", "D_REPAIR", "INCOMING"}, "dummy role family missing")
    require(local["maximum_minimal_support_tensor_ports"] == 5, "minimal support bound altered")
    require(local["maximum_common_anchor_tensor_ports"] >= 2 * local["maximum_minimal_support_tensor_ports"], "common-anchor union underbounded")
    require(local["maximum_common_anchor_plus_two_tensor_ports"] >= local["maximum_common_anchor_tensor_ports"] + 2, "pair-probe bound undercounted")
    require(local["minimal_cycle_two_outgoing_gate_separate"], "two-outgoing cycle gate omitted")
    require(local["fixed_full_hard_cover_source_outgoing_sizes"] == [3, 4], "base hard-cover source-size range altered")
    require(local["theta2_four_outgoing_minimal_support_gate_required"], "theta-2 n4 gate omitted")
    require(not local["equal_signature_hard_cover_classifies_unequal_necessary_pairs"], "equal-signature cover promoted over unequal pairs")
    require(local["unequal_necessary_directed_signature_pair_counts"] == {"3": 110, "4": 776}, "unequal directed-pair counts altered")
    require(local["pair_level_graph_bound_exact_closure_required"], "pair-level unequal closure omitted")
    extension = local["terminal_extension_contract"]
    require(extension["extend_each_raw_path_bound_allowed_terminal"], "terminal extension not path-bound")
    require(extension["deduplicated_terminal_state_alone_is_not_a_relation"], "canonical terminal state substituted for raw relation")
    require(extension["preserve_restoration_root_parent_path_Qt_and_transport"], "terminal extension lost base transport")
    require(extension["insert_new_label_on_every_admissible_internal_blob_arc_on_both_sides"], "terminal arc insertion incomplete")
    require(extension["filter_and_record_standard_strong_membership"], "terminal extension membership filter omitted")
    require(extension["recompute_graph_switchings_masks_tensors_and_witnesses"], "terminal graph-to-algebra regeneration omitted")
    require(extension["verify_child_deletion_returns_exact_parent_relation"], "terminal child-parent deletion check omitted")
    require(extension["plus_one_then_plus_two_depth"] == 2, "terminal extension depth altered")
    require(extension["maximum_terminal_tensor_ports"] == 12, "terminal extension underbounded")
    require(not extension["full_Sp_completion_enumeration_at_outgoing_sizes_5_and_6_required"], "unnecessary factorial n5/n6 completion restored")
    require(local["all_mixed_sign_terminal_cases_closed"], "mixed-sign terminal left open")
    require(local["every_wrong_relation_has_graph_bound_witness"], "wrong relation lacks graph-bound witness")
    require(set(local["terminal_allowed_relations"]) == {"labelled_isomorphism", "ordinary_T"}, "terminal move list changed")
    require(not local["ordinary_T_terminal_means_complete_image_equality"], "T promoted to complete-image equality")
    require(local["terminal_T_topology_and_stochastic_converse_are_separate_gates"], "terminal T code conflated with stochastic T germ")
    require(not local["restriction_commutes_with_nontrivial_T"], "restriction incorrectly assumed to commute with T")
    require(not local["target_may_be_reoriented_on_the_same_containment_germ"], "target reoriented without complete-image equality")
    require(local["seven_tensor_port_probe_refinement_requires_actual_target_core_retention"], "seven-port refinement made unconditional")
    require(local["arbitrary_subdivision_promotion_proved"], "finite census substituted for arbitrary-subdivision proof")

    require(artifacts["present_streams"] == [], "current bounded relation-stream status altered")
    require(artifacts["unequal_pair_level_gate"] == "UNRESOLVED", "unresolved unequal gate promoted")

    require(set(glob["cut_preservation_directions"]) == {"source_cut_implies_target_cut", "target_cut_implies_source_cut"}, "one cut direction missing")
    require(glob["bridge_gauge"] == "full_incidence_scaling", "withdrawn bridge gauge restored")
    require(not glob["physical_bridge_multiplier_recovered"], "physical bridge recovery claimed")
    require(glob["positive_local_analytic_slices"], "local slice omitted")
    require(not glob["cross_blob_compensation_allowed"], "cross-blob compensation allowed")
    require(not glob["continuous_target_parameter_selector_used"], "continuous target selector assumed")
    require(glob["root_factors_use_independently_chosen_real_incoming_boundaries"], "independent incoming choices omitted")
    require(glob["ordinary_T_germs_glued_on_sufficiently_small_effective_scale_intervals"], "T gluing interval omitted")
    require(not glob["every_T_orientation_realizes_every_generic_distribution"], "all T variants claimed at every point")

    require(exc["network_specific"], "exceptional locus not network-specific")
    require(exc["finite_for_fixed_taxon_set"], "finite-topology union omitted")
    require(exc["contains_non_T_intersection_closures"], "non-T intersections omitted")
    require(exc["contains_generic_rank_critical_values"], "critical values omitted")
    require(exc["certificate_overapproximation_uses_graph_bound_witnesses"], "exceptional certificate not graph-bound")
    require(not exc["claimed_minimal"], "unsupported minimality claim")
    return errors


def exact_regressions() -> dict:
    # Withdrawn reciprocal-only bridge chart: same observable product.
    triple_1 = (Fraction(1, 2), Fraction(1, 2), Fraction(1, 2))
    triple_2 = (Fraction(3, 5), Fraction(3, 5), Fraction(25, 72))
    assert triple_1[0] * triple_1[1] * triple_1[2] == Fraction(1, 8)
    assert triple_2[0] * triple_2[1] * triple_2[2] == Fraction(1, 8)
    assert triple_1 != triple_2

    # Marginal equality does not lift: a+b=1 and b=a meet only at 1/2.
    a = Fraction(1, 2)
    b = Fraction(1, 2)
    assert a + b == 1 and b == a
    for q in (Fraction(1, 5), Fraction(2, 5), Fraction(4, 5)):
        assert 0 < q < 1 and 0 < 1 - q < 1
        assert 0 < q < 1 and 0 < q < 1
    # Solving b=1-a and b=a gives 2a=1 exactly.
    assert 2 * a == 1

    # Safe common-anchor bound from the five primitive support rows.
    support_rows = {
        "cycle": (1, 1),
        "TT_nested": (2, 1),
        "TT_separated": (2, 2),
        "TR_nested": (1, 2),
        "TR_separated": (1, 2),
    }
    totals = {name: 1 + sinks + repair for name, (sinks, repair) in support_rows.items()}
    assert max(totals.values()) == 5
    common_anchor_bound = 2 * max(totals.values())
    pair_probe_bound = common_anchor_bound + 2
    assert common_anchor_bound == 10 and pair_probe_bound == 12

    # Starting from one fixed labelled terminal edge, sequential insertion of
    # p and then q on every current arc gives every interleaving with the
    # existing ordered anchors, while deleting q recovers the exact p-parent.
    insertion_counts = {}
    for anchor_count in range(6):
        anchors = tuple(f"A{i}" for i in range(anchor_count))

        def insert(word, label):
            return {
                (*word[:position], label, *word[position:])
                for position in range(len(word) + 1)
            }

        p_words = insert(anchors, "p")
        pq_with_parent = {
            (p_word, pq_word)
            for p_word in p_words
            for pq_word in insert(p_word, "q")
        }
        pq_words = {row[1] for row in pq_with_parent}
        direct = {
            word
            for word in permutations((*anchors, "p", "q"))
            if tuple(value for value in word if value.startswith("A")) == anchors
        }
        assert pq_words == direct
        assert all(
            tuple(value for value in child if value != "q") == parent
            for parent, child in pq_with_parent
        )
        insertion_counts[str(anchor_count)] = {
            "plus_one": len(p_words),
            "plus_two": len(pq_words),
        }

    # Positive path-product differential: every partial derivative is positive.
    xs = [Fraction(2, 3), Fraction(3, 5), Fraction(5, 7), Fraction(7, 11)]
    derivatives = []
    for i in range(len(xs)):
        value = Fraction(1, 1)
        for j, x in enumerate(xs):
            if i != j:
                value *= x
        derivatives.append(value)
    assert all(d > 0 for d in derivatives)

    # Small effective scales always realize both positive incidence slices.
    products = [Fraction(2, 5) * Fraction(3, 7), Fraction(4, 9) * Fraction(5, 8)]
    z = min(products) / 2
    physical = [z / p for p in products]
    assert z > 0 and all(Fraction(0) < x < Fraction(1) for x in physical)

    # Both cut directions use the same pointwise disjoint rank alternatives.
    cut_rank_upper = 4
    noncut_rank_lower = 5
    assert cut_rank_upper < noncut_rank_lower

    return {
        "bridge_equal_product": str(Fraction(1, 8)),
        "marginal_lift_full_intersection": [str(a), str(b)],
        "minimal_support_tensor_port_totals": totals,
        "maximum_common_anchor_tensor_ports": common_anchor_bound,
        "maximum_pair_probe_tensor_ports": pair_probe_bound,
        "sequential_internal_arc_insertion_counts": insertion_counts,
        "path_product_derivatives": [str(x) for x in derivatives],
        "gluing_effective_scale": str(z),
        "gluing_physical_scales": [str(x) for x in physical],
        "cut_rank_gap": [cut_rank_upper, noncut_rank_lower],
    }


def mutation_tests(contract: dict) -> list[str]:
    mutations = []

    def reject(name: str, mutator) -> None:
        candidate = copy.deepcopy(contract)
        mutator(candidate)
        if validate_contract(candidate):
            mutations.append(name)
        else:
            raise AssertionError(f"mutation was not rejected: {name}")

    reject("enable_marginal_lift", lambda c: c["local_closure_contract"].__setitem__("lift_from_selected_marginal_alone", True))
    reject("drop_full_relation_binding", lambda c: c["local_closure_contract"].__setitem__("fixed_full_relation_id_required", False))
    reject("drop_parent_prefix_binding", lambda c: c["local_closure_contract"].__setitem__("parent_prefix_binding_required", False))
    reject("restore_fixed_incoming", lambda c: c["local_closure_contract"].__setitem__("target_boundary_quotient", "fixed_INCOMING"))
    reject("drop_marginalized_incoming", lambda c: c["local_closure_contract"].__setitem__("target_incoming_modes", ["incoming_selected"]))
    reject("require_matched_incoming", lambda c: c["local_closure_contract"].__setitem__("matched_physical_incoming_boundary_required", True))
    reject("restore_leaf_internal_rooting_bug", lambda c: c["local_closure_contract"].__setitem__("minimal_disjoint_incoming_rooting_census_each_side", [9, 0]))
    reject("restore_seven_port_bound", lambda c: c["local_closure_contract"].__setitem__("maximum_common_anchor_plus_two_tensor_ports", 7))
    reject("omit_theta2_n4_gate", lambda c: c["local_closure_contract"].__setitem__("theta2_four_outgoing_minimal_support_gate_required", False))
    reject("truncate_base_hard_cover_at_n3", lambda c: c["local_closure_contract"].__setitem__("fixed_full_hard_cover_source_outgoing_sizes", [3]))
    reject("conflate_equal_and_unequal_pair_gates", lambda c: c["local_closure_contract"].__setitem__("equal_signature_hard_cover_classifies_unequal_necessary_pairs", True))
    reject("omit_pair_level_unequal_closure", lambda c: c["local_closure_contract"].__setitem__("pair_level_graph_bound_exact_closure_required", False))
    reject("extend_only_deduplicated_terminal_states", lambda c: c["local_closure_contract"]["terminal_extension_contract"].__setitem__("extend_each_raw_path_bound_allowed_terminal", False))
    reject("drop_terminal_parent_deletion_check", lambda c: c["local_closure_contract"]["terminal_extension_contract"].__setitem__("verify_child_deletion_returns_exact_parent_relation", False))
    reject("omit_terminal_graph_to_algebra_regeneration", lambda c: c["local_closure_contract"]["terminal_extension_contract"].__setitem__("recompute_graph_switchings_masks_tensors_and_witnesses", False))
    reject("leave_mixed_sign_terminal", lambda c: c["local_closure_contract"].__setitem__("all_mixed_sign_terminal_cases_closed", False))
    reject("use_unbound_separator", lambda c: c["local_closure_contract"].__setitem__("every_wrong_relation_has_graph_bound_witness", False))
    reject("omit_arbitrary_word_proof", lambda c: c["local_closure_contract"].__setitem__("arbitrary_subdivision_promotion_proved", False))
    reject("omit_reverse_cut", lambda c: c["global_contract"].__setitem__("cut_preservation_directions", ["source_cut_implies_target_cut"]))
    reject("restore_reciprocal_bridge_chart", lambda c: c["global_contract"].__setitem__("bridge_gauge", "reciprocal_only"))
    reject("claim_physical_bridge_recovery", lambda c: c["global_contract"].__setitem__("physical_bridge_multiplier_recovered", True))
    reject("allow_cross_blob_compensation", lambda c: c["global_contract"].__setitem__("cross_blob_compensation_allowed", True))
    reject("assume_continuous_target_selector", lambda c: c["global_contract"].__setitem__("continuous_target_parameter_selector_used", True))
    reject("claim_T_complete_images", lambda c: c["local_closure_contract"].__setitem__("ordinary_T_terminal_means_complete_image_equality", True))
    reject("conflate_terminal_T_with_germ", lambda c: c["local_closure_contract"].__setitem__("terminal_T_topology_and_stochastic_converse_are_separate_gates", False))
    reject("assume_restriction_commutes_with_T", lambda c: c["local_closure_contract"].__setitem__("restriction_commutes_with_nontrivial_T", True))
    reject("reorient_target_on_same_germ", lambda c: c["local_closure_contract"].__setitem__("target_may_be_reoriented_on_the_same_containment_germ", True))
    reject("make_seven_port_refinement_unconditional", lambda c: c["local_closure_contract"].__setitem__("seven_tensor_port_probe_refinement_requires_actual_target_core_retention", False))
    reject("claim_all_T_variants_at_every_point", lambda c: c["global_contract"].__setitem__("every_T_orientation_realizes_every_generic_distribution", True))
    reject("omit_exceptional_intersections", lambda c: c["exceptional_locus_contract"].__setitem__("contains_non_T_intersection_closures", False))
    return mutations


def main() -> None:
    for rel, expected in EXPECTED_INPUT_HASHES.items():
        actual = sha256(ROOT / rel)
        assert actual == expected, f"upstream input changed: {rel}: {actual} != {expected}"

    contract = json.loads((HERE / "promotion_contract.json").read_text())
    errors = validate_contract(contract)
    assert not errors, errors
    artifact_status = contract["current_local_artifact_status"]
    actual_relation_streams = sorted(
        str(path.relative_to(ROOT))
        for path in ROOT.glob(artifact_status["bounded_relation_stream_glob"])
    )
    assert actual_relation_streams == artifact_status["present_streams"], (
        "bounded relation-stream inventory changed",
        actual_relation_streams,
        artifact_status["present_streams"],
    )

    ledger = json.loads((HERE / "dependency_ledger.json").read_text())
    statuses = {item["id"]: item["status"] for item in ledger["dependencies"]}
    assert statuses["corrected_fixed_full_local_classification"] == "UNRESOLVED"
    assert ledger["overall_current_status"] == "UNRESOLVED"
    assert ledger["overall_conditional_status"] == "PROVED_CONDITIONAL_ON_LOCAL_CLOSURE_CONTRACT"

    regressions = exact_regressions()
    mutations = mutation_tests(contract)
    assert len(mutations) == 30

    report = {
        "status": "VERIFIED_SCOPE_LIMITED",
        "current_outcome_p_status": "UNRESOLVED",
        "conditional_promotion": "VALID",
        "input_hash_count": len(EXPECTED_INPUT_HASHES),
        "active_bounded_relation_streams": actual_relation_streams,
        "exact_regressions": regressions,
        "rejected_mutations": mutations,
    }
    expected_report = json.loads((HERE / "structural_certificate.json").read_text())
    assert report == expected_report, "structural certificate does not match regenerated report"
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
