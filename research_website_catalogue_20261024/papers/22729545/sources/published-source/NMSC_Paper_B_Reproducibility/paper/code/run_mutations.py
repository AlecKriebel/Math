#!/usr/bin/env python3
"""Executable source-level proof mutations; every mutant must be killed."""
from __future__ import annotations

from fractions import Fraction
import copy
import inspect
import json
from pathlib import Path
import sys
import textwrap

import networkx as nx
import sympy as sp


# These three quantities are deliberately distinct.  Four looped mutation
# sites emit additional executable records, and conceptual group 47 emits two
# records.  The release contract checks all three numbers independently.
MUTATION_RECORD_CALL_SITES = 53
MUTATION_EXECUTABLE_RECORDS = 57
MUTATION_CONCEPTUAL_GROUPS = 56

from nmsc_l2_exact import (
    _audit_colored_collision_representatives,
    _colored_canonical_code,
    _behavioral_macro_payload,
    _build_behavioral_occupancy_graph,
    _decorate_actual_raw_carrier,
    _declared_primitive_quotient_graph,
    _derive_joint_occupancy_state,
    _enumerate_declared_primitive_orbits,
    _expand_actual_hidden_carriers,
    _generate_exposure_loss_observation,
    _global_retained_event_order_tag,
    _independent_behavioral_macro_payload,
    _normalize_actual_joint_carrier,
    _raw_carrier_validity_certificate,
    _relative_label_orbit_audit,
    _recover_exposure_loss_record_from_total_laws,
    _inheritance_pair_from_sum_squares,
    _type_prony_components_from_anchor_cells,
    _sampled_leaf_nodes,
    _separate_inserted_unary_times,
    _transport_colored_graph,
    _transport_observable_value,
    anchored_route_separator_matrix,
    anchored_tagged_merger_masses,
    biunary_kernel,
    biunary_kernel_from_route_enumeration,
    build_preexposure_unary_fan,
    build_repaired_core,
    behavioral_lower_cone_guard,
    behaviorally_realizable_unary_fans,
    canonical_reattach_signature,
    enumerate_minimal_repairs,
    equal_arm_routing_survival,
    enumerate_exposure_loss_certificates,
    exposure_loss_joint_bundle_matches,
    exposure_loss_record_matches_observation,
    extend_fan_across_actual_exposure,
    fan_slide_quotient_signature,
    fixed_cut_det,
    fixed_cut_expected_det,
    is_local_strong_tree_child,
    is_local_tree_child,
    is_safe_preexposure_unary_fan,
    load_cores,
    log_hazard_numerator,
    private_side_support_start,
    rank_one_nonbridge_certificate,
    recover_two_exponential_total_law,
    repair_satisfies_domain,
    routing_weights,
    scalar_separated_fan_continuation,
    side_free_suppressed_cycle,
    staggered_balance_certificate,
    survival_semigroup_defect,
)


def source_mutant(function, old: str, new: str, overrides=None):
    """Compile one exact source replacement in an isolated namespace."""
    source = textwrap.dedent(inspect.getsource(function))
    if source.count(old) != 1:
        raise AssertionError(
            f"mutation target for {function.__name__!r} occurs {source.count(old)} times"
        )
    namespace = dict(function.__globals__)
    if overrides:
        namespace.update(overrides)
    exec(compile(source.replace(old, new), f"<mutant:{function.__name__}>", "exec"), namespace)
    return namespace[function.__name__]


checks = []


def record(name, detected, detail):
    checks.append({"mutation": name, "detected": bool(detected), "detail": detail})


base = Path(__file__).resolve().parents[1]
cores = load_cores(base / "data" / "NMSC_TOPOLOGY_IMPORT.json")
u, v, lam = sp.symbols("u v lam", positive=True)

# 1. Collapse the independent-routing mixture to a one-population Kingman law.
mutant_equal_arm = source_mutant(
    equal_arm_routing_survival,
    "return pair_survival(gamma, lam, lam, u)",
    "return kingman_pair_survival(lam, u)",
)
correct_survival = equal_arm_routing_survival(sp.Rational(1, 2), lam, u)
mutant_survival = mutant_equal_arm(sp.Rational(1, 2), lam, u)
record(
    "routing_mixture_as_kingman_semigroup",
    survival_semigroup_defect(correct_survival, u, v) != 0
    and survival_semigroup_defect(mutant_survival, u, v) == 0,
    "split-route mass creates a nonzero exact semigroup defect",
)

# 2. Reverse the log-hazard curvature sign.
mutant_log_hazard = source_mutant(
    log_hazard_numerator,
    "survival * sp.diff(survival, u, 2) - sp.diff(survival, u) ** 2",
    "sp.diff(survival, u) ** 2 - survival * sp.diff(survival, u, 2)",
)
correct_curvature = log_hazard_numerator(correct_survival, u)
mutant_curvature = mutant_log_hazard(correct_survival, u)
record(
    "reverse_log_hazard_curvature",
    sp.simplify(correct_curvature + mutant_curvature) == 0
    and correct_curvature != mutant_curvature,
    "the exact routing curvature has a fixed positive sign",
)

# 3. Infer a physical bridge solely from rank-one endpoint matrices.
mutant_rank_certificate = source_mutant(
    rank_one_nonbridge_certificate,
    '"retic_arm_is_graph_bridge": retic_arm_is_bridge',
    '"retic_arm_is_graph_bridge": one_block_rows.rank() == 1 and two_block_rows.rank() == 1',
)
correct_rank_certificate = rank_one_nonbridge_certificate()
mutant_rank_result = mutant_rank_certificate()
record(
    "rank_one_endpoint_implies_graph_bridge",
    not correct_rank_certificate["retic_arm_is_graph_bridge"]
    and mutant_rank_result["retic_arm_is_graph_bridge"],
    "the repaired-cycle fixture is rank one but its reticulation arm lies on a cycle",
)

# 4. Detach the mandatory private side leaf from its repair vertex.
build_fixture = rank_one_nonbridge_certificate.__globals__["build_stc_rank_one_nonbridge_fixture"]
mutant_fixture = source_mutant(
    build_fixture,
    '("p", "h"), ("p", "z"), ("h", "A")',
    '("p", "h"), ("S", "z"), ("h", "A")',
)
mutant_graph = mutant_fixture()
record(
    "detach_cycle_repair_port",
    is_local_tree_child(correct_rank_certificate["graph"])
    and not is_local_tree_child(mutant_graph),
    "moving z off p leaves p with only a reticulation child",
)

# 5. Weaken the strong-tail threshold from two ordinary incidences to one.
mutant_strong = source_mutant(
    is_local_strong_tree_child,
    "if ordinary < 2:",
    "if ordinary < 1:",
)
side_free_graph = build_repaired_core(side_free_suppressed_cycle(), ())
record(
    "weaken_strong_tail_threshold",
    not is_local_strong_tree_child(side_free_graph)
    and mutant_strong(side_free_graph),
    "the unrepaired parallel cycle has only the incoming ordinary boundary at its tail",
)

# 6. Let a reticulation child satisfy ordinary rooted tree-childness.
mutant_tree_child = source_mutant(
    is_local_tree_child,
    "{'tree', 'leaf'}",
    "{'tree', 'leaf', 'retic'}",
)
record(
    "reticulation_child_counts_as_tree_child",
    not is_local_tree_child(side_free_graph) and mutant_tree_child(side_free_graph),
    "the source of the side-free cycle has only reticulation children",
)

# 7. Check only the strong-tail predicate when accepting a repair.
mutant_domain = source_mutant(
    repair_satisfies_domain,
    "return is_local_tree_child(graph) and is_local_strong_tree_child(graph)",
    "return is_local_strong_tree_child(graph)",
)
theta0 = cores["theta0"]
record(
    "drop_rooted_tree_child_domain_test",
    not repair_satisfies_domain(theta0, (2,)) and mutant_domain(theta0, (2,)),
    "theta0 repair {2} passes the tail test but fails rooted tree-childness",
)

# 8. Enumerate repairs through that weakened domain predicate.
def strong_only_repair_domain(core, repair):
    return is_local_strong_tree_child(build_repaired_core(core, repair))


mutant_enumerator = source_mutant(
    enumerate_minimal_repairs,
    "repair_satisfies_domain(core, repair)",
    "strong_only_repair_domain(core, repair)",
    overrides={"strong_only_repair_domain": strong_only_repair_domain},
)
record(
    "catalog_enumerated_from_strong_tail_only",
    mutant_enumerator(theta0) != enumerate_minimal_repairs(theta0),
    "primitive enumeration changes when either graph-domain predicate is omitted",
)

# 9. Corrupt the second posterior survivor exponent 11 -> 10.
mutant_balance_weight = source_mutant(
    staggered_balance_certificate,
    "Fraction(1, 2**11)",
    "Fraction(1, 2**10)",
)
correct_balance = staggered_balance_certificate()
bad_balance = mutant_balance_weight()
record(
    "corrupt_posterior_balance_exponent",
    correct_balance["weight_1"] == correct_balance["weight_2"]
    and bad_balance["weight_1"] != bad_balance["weight_2"],
    "the exact equality 1/4608 is lost",
)

# 10. Reintroduce a simultaneous demographic event.
mutant_events = source_mutant(
    staggered_balance_certificate,
    '"events": (3, 4, 6, 7)',
    '"events": (3, 3, 6, 7)',
)
record(
    "make_staggered_events_simultaneous",
    len(set(correct_balance["events"])) == 4
    and len(set(mutant_events()["events"])) != 4,
    "temporal separation is checked from the event manifest",
)

# 11. Misclassify a partial suffix exchange as a global parent exchange.
mutant_exchange = source_mutant(
    staggered_balance_certificate,
    "schedules_prime in (schedules_n, schedules_n[::-1])",
    "schedules_prime not in (schedules_n, schedules_n[::-1])",
)
record(
    "partial_suffix_switch_as_global_exchange",
    not correct_balance["identity_or_global_exchange"]
    and mutant_exchange()["identity_or_global_exchange"],
    "the initial parent words remain pinned while only late continuations cross",
)

# 12. Erase the physical-arm tag by assigning suffix A to both models.
mutant_anchor_tag = source_mutant(
    anchored_tagged_merger_masses,
    "tagged_prime = balanced_weight * suffix_b * anchor_join",
    "tagged_prime = balanced_weight * suffix_a * anchor_join",
)
correct_anchor = anchored_tagged_merger_masses()
bad_anchor = mutant_anchor_tag()
record(
    "erase_physical_anchor_tag",
    correct_anchor["tagged_difference"] != 0
    and bad_anchor["tagged_difference"] == 0,
    "the labelled second merger distinguishes 15/128 from 14/128",
)

# 13. Use the wrong cumulative hazard for suffix A.
mutant_anchor_hazard = source_mutant(
    anchored_tagged_merger_masses,
    "Fraction(1, 2**7)",
    "Fraction(1, 2**6)",
)
bad_hazard = mutant_anchor_hazard()
record(
    "off_by_one_suffix_hazard",
    correct_anchor["suffix_a_interval_mass"] != correct_anchor["suffix_b_interval_mass"]
    and bad_hazard["suffix_a_interval_mass"] == bad_hazard["suffix_b_interval_mass"],
    "the rate-four arm accumulates hazard seven, not six, by 7 log 2",
)

# 14. Delete the two-merger column that isolates the PP route state.
mutant_separator = source_mutant(
    anchored_route_separator_matrix,
    "[two_mergers_pp, one_pp, one_pp, one_pp]",
    "[0, one_pp, one_pp, one_pp]",
)
correct_separator = anchored_route_separator_matrix()
bad_separator = mutant_separator()
record(
    "delete_pp_exclusive_suffix",
    correct_separator.det() != 0 and bad_separator.det() == 0,
    "the triangular all-route separator loses rank without the two-merger suffix",
)

# 15. Complement the join probability in independent bi-unary enumeration.
mutant_biunary = source_mutant(
    biunary_kernel_from_route_enumeration,
    '"join": gamma',
    '"join": 1 - gamma',
)
closed_biunary = biunary_kernel(sp.Rational(2, 5), 3, 4)
record(
    "complement_biunary_join_weight",
    biunary_kernel_from_route_enumeration(sp.Rational(2, 5), 3, 4) == closed_biunary
    and mutant_biunary(sp.Rational(2, 5), 3, 4) != closed_biunary,
    "route enumeration independently fixes the joining coefficient",
)

# 16. Reverse every Bernoulli assignment exponent without relabelling bits.
mutant_routing = source_mutant(
    routing_weights,
    "k = sum(bits)",
    "k = m - sum(bits)",
)
record(
    "reverse_routing_exponents_without_parent_exchange",
    mutant_routing(3, Fraction(2, 5)) != routing_weights(3, Fraction(2, 5)),
    "labelled assignment weights change away from gamma=1/2",
)

# 17. Change the co-occupied prefix exponent in the actual fixed-cut minor.
fixed_cut_coefficients = fixed_cut_det.__globals__["fixed_cut_coefficients"]
fixed_cut_row = fixed_cut_det.__globals__["fixed_cut_row"]
mutant_coefficients = source_mutant(
    fixed_cut_coefficients,
    "-lam * D - 2 * lam * u",
    "-lam * D - 3 * lam * u",
)
mutant_row = source_mutant(
    fixed_cut_row,
    "fixed_cut_coefficients(gamma, lam, D, u)",
    "mutant_fixed_cut_coefficients(gamma, lam, D, u)",
    overrides={"mutant_fixed_cut_coefficients": mutant_coefficients},
)
mutant_fixed_det = source_mutant(
    fixed_cut_det,
    "fixed_cut_row(gamma, lam, D, delta, u1)",
    "mutant_fixed_cut_row(gamma, lam, D, delta, u1)",
    overrides={"mutant_fixed_cut_row": mutant_row},
)
args = (
    sp.Rational(2, 5), 3, 2, sp.Rational(1, 7),
    sp.Rational(1, 10), sp.Rational(1, 5),
)
record(
    "wrong_cooccupied_prefix_exponent",
    sp.simplify(fixed_cut_det(*args) - fixed_cut_expected_det(*args)) == 0
    and sp.simplify(mutant_fixed_det(*args) - fixed_cut_expected_det(*args)) != 0,
    "the exact determinant identity fixes the co-occupied exponent two",
)

# 18. Erase the parent-incidence relation from the reattachment signature.
mutant_reattach = source_mutant(
    canonical_reattach_signature,
    "return (rec[0], tuple(sorted(rec[1])), rec[2], rec[3])",
    "return (rec[0], tuple(sorted(rec[1])), rec[3])",
)
correct_a = canonical_reattach_signature("theta2", "X1")
correct_b = canonical_reattach_signature("theta3", "X1")
record(
    "erase_parent_incidence_relation",
    correct_a != correct_b
    and mutant_reattach("theta2", "X1") == mutant_reattach("theta3", "X1"),
    "theta2 has incomparable U,V whereas theta3 has nested U,V",
)

# 19. Start the private-side merger support at the hidden routing time h.
fan_left = build_preexposure_unary_fan(
    Fraction(1),
    Fraction(1, 3),
    Fraction(3),
    Fraction(5),
    {"X-x": Fraction(5), "T-X": Fraction(7), "S-X": Fraction(11)},
)
fan_right = build_preexposure_unary_fan(
    Fraction(2),
    Fraction(1, 3),
    Fraction(3),
    Fraction(5),
    {"X-x": Fraction(23), "T-X": Fraction(29), "S-X": Fraction(31)},
)
mutant_support_start = source_mutant(
    private_side_support_start,
    "return min(time for _, time, _, _ in fan.first_exposure_ports)",
    "return fan.reticulation_time",
)
record(
    "private_side_support_starts_at_hidden_h",
    private_side_support_start(fan_left) == Fraction(3)
    and mutant_support_start(fan_left) == Fraction(1),
    "the x,z merger density starts when z enters T at a=3, not at hidden h=1",
)

# 20. Retain h in the new stopped-fan quotient signature.
mutant_fan_signature = source_mutant(
    fan_slide_quotient_signature,
    'return ("Q8", fan.lower_boundary, frontier, response)',
    'return ("Q8", fan.lower_boundary, fan.reticulation_time, frontier, response)',
)
fan_left_continuation = scalar_separated_fan_continuation(fan_left)
fan_right_continuation = scalar_separated_fan_continuation(fan_right)
record(
    "retain_hidden_h_in_fan_slide_quotient",
    fan_slide_quotient_signature(fan_left, fan_left_continuation)
    == fan_slide_quotient_signature(fan_right, fan_right_continuation)
    and mutant_fan_signature(fan_left, fan_left_continuation)
    != mutant_fan_signature(fan_right, fan_right_continuation),
    "Q8 preserves typed first-exposure transport but removes h and unary rate words",
)

# 21. Allow contraction through the actual two-block S--T exposure.
extended_fan = extend_fan_across_actual_exposure(fan_left)
mutant_safe_fan = source_mutant(
    is_safe_preexposure_unary_fan,
    "if fan.maximum_internal_occupancy > 1 or fan.internal_sample_entries:",
    "if fan.maximum_internal_occupancy > 2 and fan.internal_sample_entries:",
)
record(
    "contract_fan_across_actual_two_block_exposure",
    not is_safe_preexposure_unary_fan(extended_fan)
    and mutant_safe_fan(extended_fan),
    "z enters at T and creates occupancy two on S--T, so the stopped fan ends at T",
)

# 22. Replace sampled occupancy derivation by a freely assigned hidden mask.
mutant_lower_guard = source_mutant(
    behavioral_lower_cone_guard,
    "return not lower_reticulations and singleton, reasons",
    "return True, reasons",
)
mutant_behavioral_fans = source_mutant(
    behaviorally_realizable_unary_fans,
    "admissible, reasons = behavioral_lower_cone_guard(",
    "admissible, reasons = mutant_lower_cone_guard(",
    overrides={"mutant_lower_cone_guard": mutant_lower_guard},
)
theta0_graph = build_repaired_core(cores["theta0"], (2, 3))
correct_theta0_fans, _ = behaviorally_realizable_unary_fans(theta0_graph)
mutant_theta0_fans, _ = mutant_behavioral_fans(theta0_graph)
record(
    "replace_behavioral_exposure_by_assigned_mask",
    {fan["reticulation"] for fan in correct_theta0_fans} == {"X"}
    and "V" in {fan["reticulation"] for fan in mutant_theta0_fans},
    "the higher V cone crosses lower X and sampled side entries, so it is not a realizable hidden mask",
)

# Common exact fixed-S hidden-cycle fixture for the implementation mutations.
cycle = cores["cycle"]
cycle_repair = cycle.repairs[0]
cycle_occupancy = _build_behavioral_occupancy_graph(cycle, cycle_repair, ())
cycle_state = _derive_joint_occupancy_state(cycle_occupancy)
cycle_labels = dict(zip(
    _sampled_leaf_nodes(cycle_occupancy),
    tuple(f"sample-{index}" for index in range(6)),
))
cycle_fan = cycle_state["hidden_fans"][0]

# 23. Bake primitive vertex names into the independently declared quotient.
mutant_declared_precolored = source_mutant(
    _declared_primitive_quotient_graph,
    'data["observable_color"] = color',
    'data["observable_color"] = (color, ("primitive-node-name", str(node)))',
)
node_rename = {
    node: f"anonymous-renaming:{index}"
    for index, node in enumerate(sorted(cycle_occupancy, key=str))
}
renamed_cycle = nx.relabel_nodes(cycle_occupancy, node_rename, copy=True)
renamed_state = _derive_joint_occupancy_state(renamed_cycle)
renamed_labels = {
    node_rename[node]: label for node, label in cycle_labels.items()
}
correct_declared_left = _declared_primitive_quotient_graph(
    cycle_occupancy, cycle_state, cycle_labels,
)
correct_declared_right = _declared_primitive_quotient_graph(
    renamed_cycle, renamed_state, renamed_labels,
)
mutant_declared_left = mutant_declared_precolored(
    cycle_occupancy, cycle_state, cycle_labels,
)
mutant_declared_right = mutant_declared_precolored(
    renamed_cycle, renamed_state, renamed_labels,
)
record(
    "bake_primitive_names_into_declared_orbit",
    _colored_canonical_code(correct_declared_left)
    == _colored_canonical_code(correct_declared_right)
    and _colored_canonical_code(mutant_declared_left)
    != _colored_canonical_code(mutant_declared_right),
    "anonymous quotient records are invariant under raw primitive-node renaming",
)

# 24. Leave the positive unary carrier word in place when inserting the macro.
mutant_normalizer_retains_word = source_mutant(
    _normalize_actual_joint_carrier,
    "normalized.remove_nodes_from(set().union(*interiors.values()) if interiors else set())",
    "normalized.remove_nodes_from(set())",
)
cycle_immediate = _expand_actual_hidden_carriers(
    cycle_occupancy, {cycle_fan["reticulation"]: "immediate"},
)
cycle_delayed = _expand_actual_hidden_carriers(
    cycle_occupancy, {cycle_fan["reticulation"]: "delayed"},
)
immediate_state = _derive_joint_occupancy_state(cycle_immediate)
delayed_state = _derive_joint_occupancy_state(cycle_delayed)
correct_immediate = _normalize_actual_joint_carrier(
    cycle_immediate, immediate_state["hidden_fans"], cycle_labels,
)
correct_delayed = _normalize_actual_joint_carrier(
    cycle_delayed, delayed_state["hidden_fans"], cycle_labels,
)
try:
    mutant_normalizer_retains_word(
        cycle_immediate, immediate_state["hidden_fans"], cycle_labels,
    )
    mutant_normalizer_retains_word(
        cycle_delayed, delayed_state["hidden_fans"], cycle_labels,
    )
except ValueError as error:
    retained_word_rejected = "positive two-block support" in str(error)
else:
    retained_word_rejected = False
record(
    "retain_unary_carrier_in_q8_normalization",
    _colored_canonical_code(correct_immediate)
    == _colored_canonical_code(correct_delayed)
    and retained_word_rejected,
    "Q8 physically removes every module-owned unary node before macro insertion",
)

# 25. Drop the common parking padding and thereby change fixed S.
mutant_unpadded_occupancy = source_mutant(
    _build_behavioral_occupancy_graph,
    "for index in range(padding_count):",
    "for index in range(0):",
)
try:
    mutant_unpadded_occupancy(cycle, cycle_repair, ())
except AssertionError as error:
    unpadded_rejected = "common fixed sampled set" in str(error)
else:
    unpadded_rejected = False
record(
    "drop_common_fixed_S_padding",
    len(_sampled_leaf_nodes(cycle_occupancy)) == 6
    and unpadded_rejected,
    "every one of the 36 local carriers uses the same six sampled labels",
)

# 26. Stop rejecting a globally tied pair of inserted event clocks.
mutant_ignore_temporal_tie = source_mutant(
    _raw_carrier_validity_certificate,
    '"strict_temporal_separation": len(set(event_times)) == len(event_times),',
    '"strict_temporal_separation": True,',
)
tied_cycle = cycle_delayed.copy()
tied_unary_nodes = tuple(
    node for node, data in tied_cycle.nodes(data=True)
    if data.get("role") == "unary"
)
if len(tied_unary_nodes) < 2:
    raise AssertionError("temporal mutation fixture needs two unary events")
tied_cycle.nodes[tied_unary_nodes[1]]["event_time"] = tied_cycle.nodes[
    tied_unary_nodes[0]
]["event_time"]
tied_state = _derive_joint_occupancy_state(tied_cycle)
correct_validity = _raw_carrier_validity_certificate(
    cycle_delayed, delayed_state["hidden_fans"],
)
tied_validity = _raw_carrier_validity_certificate(
    tied_cycle, tied_state["hidden_fans"],
)
mutant_tied_validity = mutant_ignore_temporal_tie(
    tied_cycle, tied_state["hidden_fans"],
)
record(
    "accept_globally_tied_unary_event_times",
    correct_validity["strict_temporal_separation"]
    and not tied_validity["strict_temporal_separation"]
    and mutant_tied_validity["strict_temporal_separation"],
    "strict raw carriers assign distinct exact times to every internal boundary",
)

# 27. Erase the retained event's position in the global strict order.
mutant_global_order = source_mutant(
    _global_retained_event_order_tag,
    '''return (
        "global-retained-strict-order",
        ordered.index(node),
        len(ordered),
    )''',
    '''return (
        "global-retained-strict-order",
        0,
        len(ordered),
    )''',
)
theta2 = cores["theta2"]
theta2_repair = theta2.repairs[0]
theta2_forward = _build_behavioral_occupancy_graph(
    theta2, theta2_repair, theta2.retics,
)
theta2_reverse = _build_behavioral_occupancy_graph(
    theta2, theta2_repair, theta2.retics,
    reverse_incomparable_order=True,
)
retained_probe = theta2.retics[0]
record(
    "erase_global_retained_event_order",
    _global_retained_event_order_tag(theta2_forward, retained_probe)
    != _global_retained_event_order_tag(theta2_reverse, retained_probe)
    and mutant_global_order(theta2_forward, retained_probe)
    == mutant_global_order(theta2_reverse, retained_probe),
    "the two full DAG linear extensions retain opposite incomparable-retic orders",
)

# 28. Independently complement every physical incoming-edge weight.
mutant_independent_weights = source_mutant(
    _independent_behavioral_macro_payload,
    'Fraction(matching_edges[0].get("inheritance_probability", Fraction(1, 2)))',
    '1 - Fraction(matching_edges[0].get("inheritance_probability", Fraction(1, 2)))',
)
main_cycle_response = _behavioral_macro_payload(
    cycle_occupancy, cycle_fan, cycle_labels,
)
independent_cycle_response = _independent_behavioral_macro_payload(
    cycle_occupancy, cycle_fan, cycle_labels,
)
mutant_independent_response = mutant_independent_weights(
    cycle_occupancy, cycle_fan, cycle_labels,
)
record(
    "complement_weights_in_independent_macro_builder",
    main_cycle_response == independent_cycle_response
    and main_cycle_response != mutant_independent_response,
    "the independent primitive response recomputes each typed edge-weight pairing",
)

# 29. Classify declared quotient orbits from expected graphs instead of the
# independently colored primitive carriers.
mutant_expected_orbits = source_mutant(
    _enumerate_declared_primitive_orbits,
    'graph = record["declared_quotient_graph"]',
    'graph = record["expected_graph"]',
)
one_vertex = nx.MultiDiGraph()
one_vertex.add_node("a", observable_color=("tree",))
two_vertices = nx.MultiDiGraph()
two_vertices.add_node("a", observable_color=("tree",))
two_vertices.add_node("b", observable_color=("tree",))
two_vertices.add_edge("a", "b", observable_color=("population-incidence",))
orbit_fixture = [
    {"declared_quotient_graph": one_vertex.copy(), "expected_graph": one_vertex.copy()},
    {"declared_quotient_graph": two_vertices.copy(), "expected_graph": one_vertex.copy()},
]
_, correct_orbit_count = _enumerate_declared_primitive_orbits(
    copy.deepcopy(orbit_fixture),
)
_, mutant_orbit_count = mutant_expected_orbits(copy.deepcopy(orbit_fixture))
record(
    "reuse_expected_graph_as_declared_orbit",
    correct_orbit_count == 2 and mutant_orbit_count == 1,
    "declared automorphism/Q8 orbits are computed from a separate primitive graph",
)

# 30. Audit only the identity label placement instead of the full relative S6 orbit.
mutant_identity_label_audit = source_mutant(
    _relative_label_orbit_audit,
    "for permutation in permutations(range(FIXED_LOCAL_SAMPLE_COUNT)):",
    "for permutation in (tuple(range(FIXED_LOCAL_SAMPLE_COUNT)),):",
)
expected_sample_0 = nx.MultiDiGraph()
expected_sample_0.add_node("s", observable_color=("sample", "sample-0"))
expected_sample_1 = nx.MultiDiGraph()
expected_sample_1.add_node("s", observable_color=("sample", "sample-1"))
bad_declared = nx.MultiDiGraph()
bad_declared.add_node("s", observable_color=("sample", "sample-1"))
bad_declared.add_node("extra", observable_color=("tree",))
relative_fixture = [
    {
        "expected_graph": expected_sample_0,
        "declared_quotient_graph": expected_sample_0.copy(),
    },
    {
        "expected_graph": expected_sample_1,
        "declared_quotient_graph": bad_declared,
    },
]
correct_relative = _relative_label_orbit_audit(relative_fixture)
mutant_relative = mutant_identity_label_audit(relative_fixture)
record(
    "audit_common_identity_labels_only",
    correct_relative["relative_label_placement_count"] == 2 * 720
    and bool(correct_relative["failures"])
    and mutant_relative["relative_label_placement_count"] == 2
    and not mutant_relative["failures"],
    "the certificate exhausts arbitrary relative placements, not common equivariance",
)

# 31. Check only one nonrepresentative in each relative-label collision group.
mutant_one_collision_representative = source_mutant(
    _relative_label_orbit_audit,
    "for record_index, permutation in entries[1:]:",
    "for record_index, permutation in entries[1:2]:",
)
all_representatives_fixture = [
    {
        "expected_graph": expected_sample_0.copy(),
        "declared_quotient_graph": expected_sample_0.copy(),
    },
    {
        "expected_graph": expected_sample_0.copy(),
        "declared_quotient_graph": expected_sample_0.copy(),
    },
    {
        "expected_graph": expected_sample_0.copy(),
        "declared_quotient_graph": bad_declared.copy(),
    },
]
correct_all_representatives = _relative_label_orbit_audit(
    all_representatives_fixture,
)
mutant_one_representative = mutant_one_collision_representative(
    all_representatives_fixture,
)
record(
    "check_only_one_collision_nonrepresentative",
    bool(correct_all_representatives["failures"])
    and not mutant_one_representative["failures"],
    "every nonrepresentative receives an explicit primitive-isomorphism check",
)

# 32. Complement weights while holding the typed outlet records fixed.
mutant_fixed_outlet_complement = source_mutant(
    _behavioral_macro_payload,
    'weight = Fraction(parent_edges[0].get("inheritance_probability", Fraction(1, 2)))',
    'weight = 1 - Fraction(parent_edges[0].get("inheritance_probability", Fraction(1, 2)))',
)
mutant_complement_response = mutant_fixed_outlet_complement(
    cycle_occupancy, cycle_fan, cycle_labels,
)
record(
    "complement_gamma_at_fixed_typed_outlets",
    main_cycle_response != mutant_complement_response,
    "Q8 preserves (typed outlet, exact weight) pairs; it does not sort weights alone",
)

# 33. Drop exact inheritance weights from raw incoming-edge colors.
mutant_raw_drops_weights = source_mutant(
    _decorate_actual_raw_carrier,
    'if "inheritance_probability" in data',
    "if False",
)
swapped_cycle = cycle_delayed.copy()
swapped_edges = tuple(sorted(
    swapped_cycle.in_edges(cycle_fan["reticulation"], keys=True, data=True),
    key=lambda edge: tuple(map(str, edge[:3])),
))
swapped_weights = tuple(
    Fraction(edge[3]["inheritance_probability"]) for edge in swapped_edges
)
swapped_edges[0][3]["inheritance_probability"] = swapped_weights[1]
swapped_edges[1][3]["inheritance_probability"] = swapped_weights[0]
correct_raw_original = _decorate_actual_raw_carrier(
    cycle_delayed, delayed_state["hidden_fans"], cycle_labels,
)
swapped_state = _derive_joint_occupancy_state(swapped_cycle)
correct_raw_swapped = _decorate_actual_raw_carrier(
    swapped_cycle, swapped_state["hidden_fans"], cycle_labels,
)
mutant_raw_original = mutant_raw_drops_weights(
    cycle_delayed, delayed_state["hidden_fans"], cycle_labels,
)
mutant_raw_swapped = mutant_raw_drops_weights(
    swapped_cycle, swapped_state["hidden_fans"], cycle_labels,
)
record(
    "drop_typed_inheritance_weight_from_raw_edge_color",
    _colored_canonical_code(correct_raw_original)
    != _colored_canonical_code(correct_raw_swapped)
    and _colored_canonical_code(mutant_raw_original)
    == _colored_canonical_code(mutant_raw_swapped),
    "raw parameter records retain the exact probability on each physical parent edge",
)

# 34. Stop validating that each binary reticulation's edge weights sum to one.
mutant_ignore_weight_sum = source_mutant(
    _raw_carrier_validity_certificate,
    "len(pair) == 2 and sum(pair, Fraction(0)) == 1",
    "len(pair) == 2 and True",
)
bad_sum_cycle = cycle_delayed.copy()
bad_sum_edges = tuple(sorted(
    bad_sum_cycle.in_edges(cycle_fan["reticulation"], keys=True, data=True),
    key=lambda edge: tuple(map(str, edge[:3])),
))
bad_sum_edges[0][3]["inheritance_probability"] = Fraction(1, 4)
bad_sum_state = _derive_joint_occupancy_state(bad_sum_cycle)
correct_bad_sum = _raw_carrier_validity_certificate(
    bad_sum_cycle, bad_sum_state["hidden_fans"],
)
mutant_bad_sum = mutant_ignore_weight_sum(
    bad_sum_cycle, bad_sum_state["hidden_fans"],
)
record(
    "ignore_binary_inheritance_weight_sum",
    not correct_bad_sum["inheritance_edge_probabilities_sum_to_one"]
    and mutant_bad_sum["inheritance_edge_probabilities_sum_to_one"],
    "each reticulation has two positive edge weights summing exactly to one",
)

# 35. Let edge weights disagree with the scalar parent-presentation marker.
mutant_ignore_presentation_marker = source_mutant(
    _raw_carrier_validity_certificate,
    "and sorted(pair) == sorted((gamma, 1 - gamma))",
    "and True",
)
bad_marker_cycle = cycle_delayed.copy()
bad_marker_edges = tuple(sorted(
    bad_marker_cycle.in_edges(cycle_fan["reticulation"], keys=True, data=True),
    key=lambda edge: tuple(map(str, edge[:3])),
))
bad_marker_edges[0][3]["inheritance_probability"] = Fraction(1, 4)
bad_marker_edges[1][3]["inheritance_probability"] = Fraction(3, 4)
bad_marker_state = _derive_joint_occupancy_state(bad_marker_cycle)
correct_bad_marker = _raw_carrier_validity_certificate(
    bad_marker_cycle, bad_marker_state["hidden_fans"],
)
mutant_bad_marker = mutant_ignore_presentation_marker(
    bad_marker_cycle, bad_marker_state["hidden_fans"],
)
record(
    "ignore_edge_pair_presentation_marker_agreement",
    not correct_bad_marker["inheritance_edges_agree_with_presentation_marker"]
    and mutant_bad_marker["inheritance_edges_agree_with_presentation_marker"],
    "the scalar marker records the same unordered physical pair modulo Q5 exchange",
)

# 36. Check only the first nonrepresentative of a normalized collision group.
mutant_short_collision_audit = source_mutant(
    _audit_colored_collision_representatives,
    "for index in indices[1:]:",
    "for index in indices[1:2]:",
)
collision_rows = (
    {"normalized_graph": one_vertex.copy()},
    {"normalized_graph": one_vertex.copy()},
    {"normalized_graph": two_vertices.copy()},
)
collision_groups = {"deliberate-code-collision": (0, 1, 2)}
record(
    "check_only_first_normalized_collision_representative",
    _audit_colored_collision_representatives(
        collision_rows, collision_groups,
    ) == ((0, 2),)
    and mutant_short_collision_audit(collision_rows, collision_groups) == (),
    "all members, not one witness, are checked against the collision representative",
)

# 37. Substitute labels elementwise but do not re-sort typed route/weight pairs.
mutant_elementwise_transport = source_mutant(
    _transport_observable_value,
    "return _canonicalize_transported_observable_value(transported)",
    "return transported",
)
transport_occupancy = _build_behavioral_occupancy_graph(theta0, (2, 3), ())
transport_labels = dict(zip(
    _sampled_leaf_nodes(transport_occupancy),
    tuple(f"sample-{index}" for index in range(6)),
))
transport_state = _derive_joint_occupancy_state(transport_occupancy)
transport_actual = _expand_actual_hidden_carriers(
    transport_occupancy,
    {
        reticulation: "immediate"
        for reticulation in transport_state["hidden_reticulations"]
    },
)
transport_actual_state = _derive_joint_occupancy_state(transport_actual)
transport_baseline = _normalize_actual_joint_carrier(
    transport_actual,
    transport_actual_state["hidden_fans"],
    transport_labels,
)
label_swap = {f"sample-{index}": f"sample-{index}" for index in range(6)}
label_swap["sample-1"] = "sample-2"
label_swap["sample-2"] = "sample-1"
swapped_labels = {
    node: label_swap[label] for node, label in transport_labels.items()
}
transport_rebuilt = _normalize_actual_joint_carrier(
    transport_actual,
    transport_actual_state["hidden_fans"],
    swapped_labels,
)
correct_transport = _transport_colored_graph(transport_baseline, label_swap)
elementwise_transport = transport_baseline.copy()
for _, data in elementwise_transport.nodes(data=True):
    data["observable_color"] = mutant_elementwise_transport(
        data["observable_color"], label_swap,
    )
for _, _, _, data in elementwise_transport.edges(keys=True, data=True):
    data["observable_color"] = mutant_elementwise_transport(
        data["observable_color"], label_swap,
    )
record(
    "transport_labels_without_recanonicalizing_typed_pairs",
    _colored_canonical_code(correct_transport)
    == _colored_canonical_code(transport_rebuilt)
    and _colored_canonical_code(elementwise_transport)
    != _colored_canonical_code(transport_rebuilt),
    "label transport re-sorts typed route records while carrying exact weights",
)

# Exact exposure-loss fixture used by mutations 38 onward.  Its inverse sees
# only total scalar laws; the raw parameter manifest is retained solely as an
# independent expected record.
exposure_certificate = enumerate_exposure_loss_certificates(cores)
exposure_row = exposure_certificate["rows"][0]
exposure_observation = exposure_row["observation"]
exposure_record = exposure_row["recovered_v_record"]
exposure_u = exposure_observation["u"]
first_above_total = exposure_observation["above_chambers"][0]["total_survival"]
child_hazard = sum(
    duration * rate
    for duration, rate in exposure_record["exposed_rate_words"]["child"]
)
exposure_scale = exposure_observation["p_x"] * sp.exp(-child_hazard)

# 38. Omit the known surviving-prefix normalization from total-law moments.
mutant_prony_without_scale = source_mutant(
    recover_two_exponential_total_law,
    " / scale)",
    ")",
)
correct_prony = recover_two_exponential_total_law(
    first_above_total, exposure_scale, exposure_u,
)
mutant_prony = mutant_prony_without_scale(
    first_above_total, exposure_scale, exposure_u,
)
record(
    "prony_moments_without_surviving_prefix_scale",
    sp.simplify(correct_prony["reconstructed_total"] - first_above_total) == 0
    and sp.simplify(mutant_prony["reconstructed_total"] - first_above_total) != 0,
    "m0..m3 are normalized by the independently recovered positive p-tilde",
)

# 39. Invert the common rate in the determinant-zero branch.
mutant_equal_rate_inverse = source_mutant(
    recover_two_exponential_total_law,
    "rate = sp.simplify(m1 / m0)",
    "rate = sp.simplify(m0 / m1)",
)
equal_total = exposure_observation["equal_rate_observations"][0]["total_survival"]
correct_equal = recover_two_exponential_total_law(
    equal_total, exposure_scale, exposure_u,
)
mutant_equal = mutant_equal_rate_inverse(
    equal_total, exposure_scale, exposure_u,
)
record(
    "invert_equal_rate_prony_ratio",
    correct_equal["branch"] == "equal-rate"
    and sp.simplify(correct_equal["reconstructed_total"] - equal_total) == 0
    and sp.simplify(mutant_equal["reconstructed_total"] - equal_total) != 0,
    "the rank-one branch recovers lambda=m1/m0, including q=1/2 cases",
)

# 40. Shift the observable zero-atom breakpoint h_V after inversion.
mutant_shift_breakpoint = source_mutant(
    _recover_exposure_loss_record_from_total_laws,
    "h_v = min(h_candidates)",
    "h_v = min(h_candidates) + 1",
)
shifted_record = mutant_shift_breakpoint(exposure_observation)
record(
    "shift_recovered_exposure_breakpoint",
    exposure_loss_record_matches_observation(
        exposure_record, exposure_observation,
    )
    and not exposure_loss_record_matches_observation(
        shifted_record, exposure_observation,
    ),
    "h_V is the first ordered chamber with a positive zero-atom jump",
)

# 41. Replace Prony-recovered Bernoulli weights by a fixed inheritance pair.
mutant_fixed_inheritance = source_mutant(
    _recover_exposure_loss_record_from_total_laws,
    "inheritance_pair = square_roots",
    "inheritance_pair = (sp.Rational(1, 4), sp.Rational(3, 4))",
)
try:
    fixed_inheritance_record = mutant_fixed_inheritance(exposure_observation)
except ValueError:
    fixed_inheritance_killed = True
else:
    fixed_inheritance_killed = not exposure_loss_record_matches_observation(
        fixed_inheritance_record, exposure_observation,
    )
record(
    "replace_prony_inheritance_by_fixed_pair",
    fixed_inheritance_killed,
    "q is recovered from total-law atom weights and the triangle direction cell",
)

# 42--44. Corrupt one recovered demographic word at a time.
for word_key in ("child", "parent_1", "parent_2"):
    changed_word_record = copy.deepcopy(exposure_record)
    changed_word = list(changed_word_record["exposed_rate_words"][word_key])
    changed_word[0] = (changed_word[0][0], changed_word[0][1] + 1)
    changed_word_record["exposed_rate_words"][word_key] = tuple(changed_word)
    record(
        f"change_recovered_{word_key}_rate_word",
        not exposure_loss_record_matches_observation(
            changed_word_record, exposure_observation,
        )
        and not exposure_loss_joint_bundle_matches(
            cores[exposure_row["core"]],
            exposure_row["manifest"],
            exposure_observation,
            changed_word_record,
            exposure_row["stored_x_macro"],
        ),
        "each child/parent rate word is checked against total laws and consumed by lift",
    )

# 45--46. Remove/change each recovered V incidence.
for incidence_key in ("parent_incidences", "child_incidence"):
    removed_incidence_record = copy.deepcopy(exposure_record)
    removed_incidence_record.pop(incidence_key)
    changed_incidence_record = copy.deepcopy(exposure_record)
    changed_incidence = list(changed_incidence_record[incidence_key])
    changed_incidence[0] = ("wrong-port", *changed_incidence[0][1:])
    changed_incidence_record[incidence_key] = tuple(changed_incidence)
    record(
        f"remove_or_change_recovered_V_{incidence_key}",
        not exposure_loss_record_matches_observation(
            removed_incidence_record, exposure_observation,
        )
        and not exposure_loss_record_matches_observation(
            changed_incidence_record, exposure_observation,
        )
        and not exposure_loss_joint_bundle_matches(
            cores[exposure_row["core"]],
            exposure_row["manifest"],
            exposure_observation,
            changed_incidence_record,
            exposure_row["stored_x_macro"],
        ),
        "both V parent and child incidences are semantically required",
    )

# 47. Remove and alter h and q fields independently.
for field_name in ("h_v", "inheritance_pair"):
    removed_field_record = copy.deepcopy(exposure_record)
    removed_field_record.pop(field_name)
    changed_field_record = copy.deepcopy(exposure_record)
    if field_name == "h_v":
        changed_field_record[field_name] += 1
    else:
        changed_field_record[field_name] = (
            sp.Rational(1, 4), sp.Rational(3, 4)
        )
    record(
        f"remove_or_change_recovered_{field_name}",
        not exposure_loss_record_matches_observation(
            removed_field_record, exposure_observation,
        )
        and not exposure_loss_record_matches_observation(
            changed_field_record, exposure_observation,
        )
        and not exposure_loss_joint_bundle_matches(
            cores[exposure_row["core"]],
            exposure_row["manifest"],
            exposure_observation,
            changed_field_record,
            exposure_row["stored_x_macro"],
        ),
        "the recovered breakpoint and inheritance pair are both consumed",
    )

# 48. Change the stored typed X attachment and its physical probability.
wrong_x_attachment = copy.deepcopy(exposure_row["stored_x_macro"])
wrong_x_incoming = list(wrong_x_attachment["incoming"])
wrong_x_incoming[0] = ("wrong-X-port", *wrong_x_incoming[0][1:])
wrong_x_attachment["incoming"] = tuple(wrong_x_incoming)
wrong_x_weight = copy.deepcopy(exposure_row["stored_x_macro"])
wrong_x_weights = list(wrong_x_weight["typed_weights"])
wrong_x_weights[0] = (wrong_x_weights[0][0], sp.Rational(1, 4))
wrong_x_weight["typed_weights"] = tuple(wrong_x_weights)
record(
    "change_stored_typed_X_attachment_or_weight",
    not exposure_loss_joint_bundle_matches(
        cores[exposure_row["core"]],
        exposure_row["manifest"],
        exposure_observation,
        exposure_record,
        wrong_x_attachment,
    )
    and not exposure_loss_joint_bundle_matches(
        cores[exposure_row["core"]],
        exposure_row["manifest"],
        exposure_observation,
        exposure_record,
        wrong_x_weight,
    ),
    "joint lift consumes the stored typed X ports and exact physical weights",
)

# 49. Accept a simultaneous two-parent demographic boundary.
mutant_accept_simultaneous = source_mutant(
    _recover_exposure_loss_record_from_total_laws,
    "if any(count != 1 for count in asynchronous_changes):",
    "if any(count > 2 for count in asynchronous_changes):",
)
simultaneous_manifest = copy.deepcopy(exposure_row["manifest"])
simultaneous_schedule = [
    dict(chamber) for chamber in simultaneous_manifest["parent_schedule"]
]
first_rates = simultaneous_schedule[0]["rates"]
simultaneous_schedule[1]["rates"] = (
    simultaneous_schedule[1]["rates"][0],
    first_rates[1] + 3,
)
simultaneous_manifest["parent_schedule"] = tuple(simultaneous_schedule)
simultaneous_observation = _generate_exposure_loss_observation(
    cores[exposure_row["core"]], simultaneous_manifest,
)
try:
    _recover_exposure_loss_record_from_total_laws(simultaneous_observation)
except ValueError as error:
    correct_rejects_simultaneous = "strictly asynchronous" in str(error)
else:
    correct_rejects_simultaneous = False
try:
    mutant_simultaneous_record = mutant_accept_simultaneous(
        simultaneous_observation
    )
except ValueError:
    mutant_accepts_simultaneous = False
else:
    mutant_accepts_simultaneous = (
        2 in mutant_simultaneous_record["asynchronous_parent_boundary_changes"]
    )
record(
    "accept_simultaneous_parent_word_changes",
    correct_rejects_simultaneous and mutant_accepts_simultaneous,
    "the fixture uses one strictly separated parent-word boundary at a time",
)

# 50. Treat theta0 {2,3}'s bypass sibling as an immediate V parent arm.
mutant_bypass_as_parent_arm = source_mutant(
    _generate_exposure_loss_observation,
    'if graph.has_edge(typing_port, "X"):',
    "if False:",
)
try:
    mutant_bypass_as_parent_arm(
        cores[exposure_row["core"]], exposure_row["manifest"]
    )
except AssertionError as error:
    bypass_shortcut_killed = "typing anchor" in str(error)
else:
    bypass_shortcut_killed = False
record(
    "type_theta0_23_bypass_as_immediate_parent_arm",
    exposure_row["typing_kind"] == "U-to-X-bypass-sibling-at-U"
    and bypass_shortcut_killed,
    "z2 types the U-to-X bypass sibling at U, not a V parent chamber",
)

# 51. Reattach sorted unordered q values to physical parents after recovery.
sorted_q_source = textwrap.dedent(inspect.getsource(
    _recover_exposure_loss_record_from_total_laws
))
old_physical_assignment = '''                typed_q_by_parent[parent],
            )
            for parent in ("physical-parent-0", "physical-parent-1")
'''
new_physical_assignment = '''                inheritance_pair[index],
            )
            for index, parent in enumerate(
                ("physical-parent-0", "physical-parent-1")
            )
'''
if sorted_q_source.count(old_physical_assignment) != 1:
    raise AssertionError("typed-q physical assignment mutation target drifted")
sorted_q_namespace = dict(
    _recover_exposure_loss_record_from_total_laws.__globals__
)
exec(compile(
    sorted_q_source.replace(
        old_physical_assignment,
        new_physical_assignment,
    ),
    "<mutant:sort_unordered_q_onto_physical_parents>",
    "exec",
), sorted_q_namespace)
mutant_sorted_physical_q = sorted_q_namespace[
    "_recover_exposure_loss_record_from_total_laws"
]
swapped_q_row = exposure_certificate["swapped_physical_q_row"]
swapped_q_observation = swapped_q_row["observation"]
mutant_swapped_q_record = mutant_sorted_physical_q(swapped_q_observation)
record(
    "sort_unordered_q_onto_physical_parent_incidences",
    exposure_certificate["swapped_physical_q_assignment_exact"]
    and not exposure_loss_record_matches_observation(
        mutant_swapped_q_record,
        swapped_q_observation,
    )
    and not exposure_loss_joint_bundle_matches(
        cores[swapped_q_row["core"]],
        swapped_q_row["manifest"],
        swapped_q_observation,
        mutant_swapped_q_record,
        swapped_q_row["stored_x_macro"],
    ),
    "Prony weights remain paired with their route-exclusive physical anchors",
)

# 52. Drop one of two same-rate anchored components instead of grouping them.
mutant_overwrite_equal_rate_group = source_mutant(
    _type_prony_components_from_anchor_cells,
    "grouped[rate] = sp.simplify(grouped.get(rate, 0) + weight)",
    "grouped[rate] = sp.simplify(weight)",
)
equal_first_rows = exposure_certificate["equal_first_chamber_rows"]
equal_group_mutant_killed = True
for row in equal_first_rows:
    mutant_globals = dict(_recover_exposure_loss_record_from_total_laws.__globals__)
    mutant_globals["_type_prony_components_from_anchor_cells"] = (
        mutant_overwrite_equal_rate_group
    )
    mutant_recover = source_mutant(
        _recover_exposure_loss_record_from_total_laws,
        '    """Recover E using total scalar laws; anchor cells only type atoms."""',
        '    """Recover E using total scalar laws; anchor cells only type atoms."""',
        overrides=mutant_globals,
    )
    try:
        mutant_recover(row["observation"])
    except ValueError:
        pass
    else:
        equal_group_mutant_killed = False
record(
    "drop_same_rate_route_exclusive_anchor_component",
    exposure_certificate["all_full_equal_first_chamber_records_exact"]
    and equal_group_mutant_killed,
    "equal-rate total atoms are split by observable physical anchor cells",
)

# 53. Deduplicate the repeated q=1/2 Bernoulli root.
mutant_drop_repeated_half_root = source_mutant(
    _inheritance_pair_from_sum_squares,
    "return pair",
    "return tuple(dict.fromkeys(pair))",
)
half_root = mutant_drop_repeated_half_root(sp.Rational(1, 2))
record(
    "drop_repeated_q_half_root",
    _inheritance_pair_from_sum_squares(sp.Rational(1, 2))
    == (sp.Rational(1, 2), sp.Rational(1, 2))
    and half_root == (sp.Rational(1, 2),),
    "the determinant-zero branch retains both positive parent-route weights",
)

# 54. Swap X's corridor/bypass probabilities while holding scalar p_X fixed.
wrong_physical_x = copy.deepcopy(swapped_q_row["stored_x_macro"])
x_weight_rows = list(wrong_physical_x["typed_weights"])
x_weight_rows[0], x_weight_rows[1] = (
    (x_weight_rows[0][0], x_weight_rows[1][1]),
    (x_weight_rows[1][0], x_weight_rows[0][1]),
)
wrong_physical_x["typed_weights"] = tuple(x_weight_rows)
record(
    "swap_fixed_scalar_p_x_between_corridor_and_bypass",
    swapped_q_observation["p_x"] == swapped_q_row["manifest"]["p_x"]
    and not exposure_loss_joint_bundle_matches(
        cores[swapped_q_row["core"]],
        swapped_q_row["manifest"],
        swapped_q_observation,
        swapped_q_row["recovered_v_record"],
        wrong_physical_x,
    ),
    "p_X is typed to the actual V-child corridor, not repr-sorted X parents",
)

# 55. Ignore stored repair-label typing and X focal/parent port metadata.
wrong_typing_labels = copy.deepcopy(exposure_record)
wrong_typing_labels["repair_side_typing"]["labels"] = (
    "wrong-focal", "wrong-child", "wrong-anchor",
)
wrong_x_focal = copy.deepcopy(exposure_row["stored_x_macro"])
wrong_x_focal["focal"] = "wrong-X-focal"
wrong_x_parents = copy.deepcopy(exposure_row["stored_x_macro"])
wrong_x_parents["parents"] = ("wrong-parent",)
record(
    "ignore_repair_labels_or_X_focal_parent_ports",
    not exposure_loss_record_matches_observation(
        wrong_typing_labels,
        exposure_observation,
    )
    and not exposure_loss_joint_bundle_matches(
        cores[exposure_row["core"]],
        exposure_row["manifest"],
        exposure_observation,
        exposure_record,
        wrong_x_focal,
    )
    and not exposure_loss_joint_bundle_matches(
        cores[exposure_row["core"]],
        exposure_row["manifest"],
        exposure_observation,
        exposure_record,
        wrong_x_parents,
    ),
    "all stored typing labels and X macro boundary ports are consumed",
)

# 56. Retain a latent boundary between adjacent equal-rate child epochs.
mutant_retain_equal_child_boundary = source_mutant(
    _recover_exposure_loss_record_from_total_laws,
    "child_word = _compress_physical_rate_word(child_durations, child_rates)",
    "child_word = tuple(zip(child_durations, child_rates))",
)
equal_child_row = exposure_certificate["equal_child_epoch_rows"][0]
mutant_equal_child_record = mutant_retain_equal_child_boundary(
    equal_child_row["observation"]
)
record(
    "retain_equal_rate_child_epoch_boundary",
    exposure_certificate["all_equal_child_epochs_q3_compressed"]
    and len(equal_child_row["recovered_v_record"]["exposed_rate_words"]["child"])
    == 1
    and len(mutant_equal_child_record["exposed_rate_words"]["child"]) == 2
    and not exposure_loss_record_matches_observation(
        mutant_equal_child_record,
        equal_child_row["observation"],
    )
    and not exposure_loss_joint_bundle_matches(
        cores[equal_child_row["core"]],
        equal_child_row["manifest"],
        equal_child_row["observation"],
        mutant_equal_child_record,
        equal_child_row["stored_x_macro"],
    ),
    "Q3 merges adjacent equal-rate epochs on the unchanged child lineage",
)

if len(checks) != MUTATION_EXECUTABLE_RECORDS:
    raise RuntimeError(
        f"runtime mutation record count {len(checks)} != "
        f"{MUTATION_EXECUTABLE_RECORDS}"
    )
for record_number, item in enumerate(checks, start=1):
    if record_number <= 46:
        conceptual_group = record_number
    elif record_number <= 48:
        conceptual_group = 47
    else:
        conceptual_group = record_number - 1
    item["conceptual_group"] = conceptual_group
observed_groups = {item["conceptual_group"] for item in checks}
expected_groups = set(range(1, MUTATION_CONCEPTUAL_GROUPS + 1))
if observed_groups != expected_groups:
    raise RuntimeError(
        "conceptual mutation groups differ: "
        f"observed={sorted(observed_groups)!r} expected={sorted(expected_groups)!r}"
    )

failed = [item for item in checks if not item["detected"]]
report = {
    "status": "PASS" if not failed else "FAIL",
    "mutations_total": len(checks),
    "mutations_detected": len(checks) - len(failed),
    "conceptual_groups_total": len(observed_groups),
    "record_call_sites": MUTATION_RECORD_CALL_SITES,
    "records": checks,
}
out = base / "certificates" / "mutation_report.json"
out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
for item in checks:
    print(
        "DETECTED" if item["detected"] else "MISSED",
        item["mutation"],
        "-",
        item["detail"],
    )
if failed:
    sys.exit(1)
print(
    "ALL_EXECUTABLE_SOURCE_MUTATIONS_DETECTED "
    f"records={len(checks)} conceptual_groups={len(observed_groups)} "
    f"call_sites={MUTATION_RECORD_CALL_SITES}"
)
