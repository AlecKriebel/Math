#!/usr/bin/env python3
"""Independent fail-closed audit of the strong-class lost-bridge transfer.

This verifier does not import the producer or its verifier.  It reconstructs
the 204 labelled one-active directions from the frozen graph records, checks
the target-tree dichotomy on every labelled tree through seven vertices as an
adversarial finite search, and rederives the K3P two-terminal side-blob
closure from the character table and exact rational arithmetic.

The finite tree search is falsification evidence.  The general tree lemma and
the one-active word-compression proof are recorded in the accompanying audit
and byte-bound to the authoritative JC manuscript and topology certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]

AUDIT = HERE / "ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.json"
VERIFY_REPORT = HERE / "VERIFICATION_REPORT.json"
MANIFEST = HERE / "MANIFEST.sha256"

PATHS = {
    "global_certificate": PROJECT / "cut_recovery/strong_crossbridge/global_transfer/GLOBAL_TRANSFER_CERTIFICATE.json",
    "global_universe": PROJECT / "cut_recovery/strong_crossbridge/global_transfer/GLOBAL_TRANSFER_DIRECTION_UNIVERSE.json",
    "global_builder": PROJECT / "cut_recovery/strong_crossbridge/global_transfer/build_global_transfer.py",
    "global_verifier": PROJECT / "cut_recovery/strong_crossbridge/global_transfer/verify_global_transfer.py",
    "global_verification": PROJECT / "cut_recovery/strong_crossbridge/global_transfer/VERIFICATION_REPORT.json",
    "local_certificate": PROJECT / "cut_recovery/strong_crossbridge/final_certificate/STRONG_CROSSBRIDGE_FINAL_CERTIFICATE.json",
    "local_universe": PROJECT / "cut_recovery/strong_crossbridge/final_certificate/UNIVERSE_CERTIFICATE.json",
    "local_verification": PROJECT / "cut_recovery/strong_crossbridge/final_certificate/VERIFICATION_REPORT.json",
    "local_mutations": PROJECT / "cut_recovery/strong_crossbridge/final_certificate/ADVERSARIAL_MUTATION_REPORT.json",
    "frozen_topology": PROJECT / "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json",
    "jc_manuscript": PROJECT / "input_frozen/referenced_chat_manuscripts/jc_level2_source.tex",
    "model_domain": PROJECT / "model_domain/primary_exact_evidence.json",
    "marginal": PROJECT / "marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json",
    "directed_logic": PROJECT / "cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json",
}

# These are deliberately hard-coded rather than copied from the audit JSON.
# Any change to a load-bearing producer or frozen input invalidates this audit.
EXPECTED_SHA256 = {
    "global_certificate": "b9918e80a9a6eac8acffbce65d0869c294a13932a2b37bca991b26b12b8c0596",
    "global_universe": "c9f00df0c52bbdec1eb8601f7f9ba1652eb500ae5cf5c299fad3bb086411690f",
    "global_builder": "d99ae6579fbacf18c713f0dac3045e49ccc93a42a8bed2f6861a3ad34f8a273b",
    "global_verifier": "3f0333c34c141f98232f76356961eae43ccff6d250cf2a90f68a29f607d15f50",
    "global_verification": "d602e0ebd285f338a04de57e0b89bcf2a32b93aa6f470a0a5a3aa0256aa2685b",
    "local_certificate": "643c29780219a538a5a127341ea91363aa5899d6f0f6fa1dac034889a7fdf06b",
    "local_universe": "674647dc91513ba85a2a72ed5f98d017c61f54ebb9e157975c14f5a94e4ddb9b",
    "local_verification": "c07d0c87cb5a93a556268d7bee4fb6f9d0fa475a30e2da5930e7c5369d5a0ab0",
    "local_mutations": "6f8cffb02cd2fe976840c9edf62644d4ce4f7197813510f9ba7ef0c514ce27fe",
    "frozen_topology": "edbd4afe566ed0ed5d1c518ffe5b21f8f224d547b9c351cb4e1a8c1c613ac086",
    "jc_manuscript": "36cf89a4f05a8c0339237f2cb83fe255893e013a6b78ff76e412d453b66f0dbd",
    "model_domain": "ac21e4f795537f251377411841d670c1bad4ce06a69ed24f596252c11cb7afb6",
    "marginal": "f85f918a770af7482abfe914bc93a304ce23c2489062643036b7a742ab09ef7f",
    "directed_logic": "f323625e9a629c62594df6a9ae90ca31582e0cb4fe878ddad66ddbf02be42d93",
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: object) -> None:
    if not condition:
        raise VerificationError(str(label))


def sha256(path: Path) -> str:
    answer = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def canonical_digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(PROJECT))


def verify_bindings(audit: dict) -> int:
    require(set(audit["input_sha256"]) == set(PATHS), "audit binding key set")
    for name, path in PATHS.items():
        require(path.is_file(), ("missing input", name, path))
        actual = sha256(path)
        require(actual == EXPECTED_SHA256[name], ("hard-coded input hash", name, actual))
        row = audit["input_sha256"][name]
        require(row == {"path": relative(path), "sha256": actual}, ("audit binding", name))
    return len(PATHS)


def permute_mask(mask: int, old_order: tuple[int, ...]) -> int:
    old_to_new = {old: new for new, old in enumerate(old_order)}
    answer = 0
    for old, new in old_to_new.items():
        if mask & (1 << old):
            answer |= 1 << new
    return answer


def displayed_by_all(signatures: tuple[tuple[int, ...], ...], r: int,
                     first: tuple[int, int]) -> bool:
    side = sum(1 << label for label in first)
    other = 15 ^ side
    return all(
        any(row[switch] in (side, other) for row in signatures)
        for switch in range(1 << r)
    )


def verify_direction_universe(audit: dict) -> dict:
    topology = json.loads(PATHS["frozen_topology"].read_text())
    global_universe = json.loads(PATHS["global_universe"].read_text())
    local_universe = json.loads(PATHS["local_universe"].read_text())
    local_final = json.loads(PATHS["local_certificate"].read_text())

    require(topology["status"] == "EXACTLY COMPUTED", "frozen topology status")
    require([row["name"] for row in topology["primitive_cores"]] == [
        "cycle", "theta_TR_nested", "theta_TR_separated",
        "theta_TT_nested", "theta_TT_separated",
    ], "primitive core list")
    compression = topology["switching_compression"]
    require(compression["status"] == "EXACTLY COMPUTED", "compression status")
    require(compression["survivor_count"] == 0 and compression["failures"] == [],
            "compression survivors")
    require(len(compression["families"]) == 10, "root/nonroot compression families")

    rows = []
    keys = set()
    raw = displayed = flag_checks = 0
    for expected_id, record in enumerate(topology["one_active_wrong_split"]["records"]):
        require(int(record["id"]) == expected_id, "record id order")
        r = int(record["reticulation_count"])
        signatures = tuple(tuple(int(mask) for mask in row) for row in record["signatures"])
        require(all(len(row) == 1 << r for row in signatures), "switch width")
        require(len(record["splits"]) == 3, "three quartet splits")
        for split in record["splits"]:
            raw += 1
            first = tuple(int(x) for x in split["split"])
            independently_displayed = displayed_by_all(signatures, r, first)
            flag_checks += 1
            require(independently_displayed is split["displayed_by_all"],
                    ("displayed flag", expected_id, first))
            if independently_displayed:
                displayed += 1
                continue
            complement = tuple(sorted(set(range(4)) - set(first)))
            old_order = first + complement
            unordered = tuple(sorted((tuple(sorted(first)), tuple(sorted(complement)))))
            key = (expected_id, unordered)
            require(key not in keys, "duplicate record/split direction")
            keys.add(key)
            normalized = tuple(
                tuple(permute_mask(mask, old_order) for mask in row)
                for row in signatures
            )
            rows.append({
                "target_index": len(rows),
                "record_id": expected_id,
                "reticulation_count": r,
                "old_split": list(first),
                "old_order": list(old_order),
                "normalized_split": [[0, 1], [2, 3]],
                "normalized_signatures_sha256": canonical_digest(normalized),
                "direction_key": [expected_id, [list(unordered[0]), list(unordered[1])]],
            })

    require((len(topology["one_active_wrong_split"]["records"]), raw, displayed,
             len(rows), len(keys)) == (72, 216, 12, 204, 204), "one-active census")
    require(global_universe["status"] == "PASS", "global universe status")
    require(global_universe["directions"] == rows, "global universe exact reconstruction")
    require(global_universe["directions_sha256"] == canonical_digest(rows),
            "global universe row digest")

    final_rows = local_universe["directions"]
    require(len(final_rows) == len(rows), "local/global universe length")
    for rebuilt, sealed in zip(rows, final_rows):
        for field in ("target_index", "record_id", "old_split", "old_order",
                      "normalized_split", "normalized_signatures_sha256"):
            require(sealed[field] == rebuilt[field], ("local universe crosswalk", field,
                                                      rebuilt["target_index"]))
        old_to_new = [rebuilt["old_order"].index(old) for old in range(4)]
        require(sealed["old_to_normalized_port_map"] == old_to_new,
                ("old-to-normalized map", rebuilt["target_index"]))

    coverage = local_final["coverage"]
    require(local_final["status"] == "PASS" and local_final["blocked_dependencies"] == [],
            "local pointwise status")
    require(coverage["target_directions"] == 204, "local target count")
    require(coverage["pairwise_disjoint"] is True and coverage["union_is_all_204"] is True,
            "local partition")
    targets = []
    for dependency in local_final["dependencies"]:
        require(dependency["status"] == "PASS", ("dependency status", dependency["name"]))
        targets.extend(dependency["required_targets"])
    require(len(targets) == len(set(targets)) == 204, "certificate target uniqueness")
    require(set(targets) == set(range(204)), "certificate target union")

    facts = {
        "primitive_cores": 5,
        "compression_families": 10,
        "compression_survivors": 0,
        "one_active_records": 72,
        "raw_split_entries": raw,
        "displayed_flag_checks": flag_checks,
        "displayed_by_all_removed": displayed,
        "wrong_split_directions": len(rows),
        "unique_direction_keys": len(keys),
        "pointwise_targets": len(targets),
    }
    require(audit["finite_handoff"]["replayed_counts"] == facts, "stored finite counts")
    require(audit["finite_handoff"]["tree_central_factor"] == {
        "ordinary_trivalent_component_can_be_central": False,
        "reason": "the_no_crossing_case_has_at_least_four_incident_monochromatic_branches_so_the_central_reduced_tree_vertex_has_degree_at_least_four",
        "record_zero_tree_directions": "harmless_exhaustive_superset_not_needed_for_the_central_blob_handoff",
    }, "central factor type")
    require(audit["finite_handoff"]["actual_label_selection"] == {
        "four_active_labels": "two_distinct_A_taxa_and_two_distinct_B_taxa_from_four_distinct_monochromatic_branches",
        "ordinary_tree_quartet_criterion": "a_switching_not_displaying_the_full_coloring_has_an_actual_2_by_2_quartet_not_displaying_it",
        "port_proxy_rule": "each_selected_target_bridge_branch_is_replaced_by_one_actual_taxon_and_its_strict_effective_K3P_arm",
    }, "actual-label handoff")
    require(audit["finite_handoff"]["completion_contract"] == {
        "minimum_strong_repair": "retained",
        "omitted_physical_taxa": "Fourier_character_zero",
        "path_sink_child_ports": "retained_separately",
        "physical_deletion_used": False,
        "role_of_zero_character_ports": "completion_topology_is_kept_while_its_transition_factor_is_one",
    }, "completion-port contract")
    return facts


def tree_from_prufer(sequence: tuple[int, ...], n: int) -> tuple[tuple[int, int], ...]:
    degree = [1] * n
    for vertex in sequence:
        degree[vertex] += 1
    edges = []
    for vertex in sequence:
        leaf = next(index for index, value in enumerate(degree) if value == 1)
        edges.append((leaf, vertex))
        degree[leaf] -= 1
        degree[vertex] -= 1
    remaining = [index for index, value in enumerate(degree) if value == 1]
    require(len(remaining) == 2, "Pruefer terminal pair")
    edges.append(tuple(remaining))
    return tuple(edges)


def adjacency(edges: tuple[tuple[int, int], ...], n: int) -> tuple[tuple[int, ...], ...]:
    answer = [[] for _ in range(n)]
    for left, right in edges:
        answer[left].append(right)
        answer[right].append(left)
    return tuple(tuple(sorted(row)) for row in answer)


def component_leaves(adj: tuple[tuple[int, ...], ...], start: int, blocked: int,
                     leaves: set[int]) -> set[int]:
    stack = [start]
    seen = {blocked}
    answer = set()
    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        if vertex in leaves:
            answer.add(vertex)
        stack.extend(adj[vertex])
    return answer


def path_vertices(adj: tuple[tuple[int, ...], ...], start: int, finish: int) -> set[int]:
    parent = {start: None}
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex == finish:
            break
        for nxt in adj[vertex]:
            if nxt not in parent:
                parent[nxt] = vertex
                stack.append(nxt)
    require(finish in parent, "tree path")
    answer = set()
    cursor = finish
    while cursor is not None:
        answer.add(cursor)
        cursor = parent[cursor]
    return answer


def hull(adj: tuple[tuple[int, ...], ...], colored: set[int]) -> set[int]:
    root = next(iter(colored))
    answer = {root}
    for leaf in colored - {root}:
        answer.update(path_vertices(adj, root, leaf))
    return answer


def audit_colored_tree(adj: tuple[tuple[int, ...], ...], leaves: set[int],
                       first: set[int]) -> str:
    second = leaves - first
    crossing = []
    cut = []
    for left in range(len(adj)):
        for right in adj[left]:
            if left >= right:
                continue
            side = component_leaves(adj, left, right, leaves)
            other = leaves - side
            if side in (first, second):
                cut.append((left, right))
            if (side & first and side & second and other & first and other & second):
                crossing.append((left, right))
    require(not cut, "audit called on a cut coloring")
    if crossing:
        return "crossing_bridge"

    intersection = hull(adj, first) & hull(adj, second)
    require(len(intersection) == 1, ("hull intersection not singleton", intersection))
    central = next(iter(intersection))
    branch_colors = []
    for neighbor in adj[central]:
        branch = component_leaves(adj, neighbor, central, leaves)
        colors = (bool(branch & first), bool(branch & second))
        require(colors in ((True, False), (False, True)),
                ("nonmonochromatic central branch", central, neighbor, branch))
        branch_colors.append(colors)
    require(branch_colors.count((True, False)) >= 2, "fewer than two A branches")
    require(branch_colors.count((False, True)) >= 2, "fewer than two B branches")
    require(len(adj[central]) >= 4, "central degree below four")
    return "central_component"


def verify_tree_dichotomy(audit: dict, maximum_vertices: int = 7) -> dict:
    tree_count = coloring_count = crossing_count = central_count = 0
    for n in range(2, maximum_vertices + 1):
        sequences = itertools.product(range(n), repeat=max(0, n - 2))
        for sequence in sequences:
            edges = tree_from_prufer(tuple(sequence), n)
            adj = adjacency(edges, n)
            leaves = {vertex for vertex, row in enumerate(adj) if len(row) == 1}
            if len(leaves) < 4:
                continue
            tree_count += 1
            ordered_leaves = sorted(leaves)
            # Fix the first leaf in A to remove global color-complement symmetry.
            anchor = ordered_leaves[0]
            for bits in itertools.product((0, 1), repeat=len(ordered_leaves) - 1):
                first = {anchor}
                first.update(leaf for leaf, bit in zip(ordered_leaves[1:], bits) if bit)
                second = leaves - first
                if len(first) < 2 or len(second) < 2:
                    continue
                is_cut = False
                for left in range(n):
                    for right in adj[left]:
                        if left < right:
                            side = component_leaves(adj, left, right, leaves)
                            if side in (first, second):
                                is_cut = True
                                break
                    if is_cut:
                        break
                if is_cut:
                    continue
                coloring_count += 1
                case = audit_colored_tree(adj, leaves, first)
                if case == "crossing_bridge":
                    crossing_count += 1
                else:
                    central_count += 1
    facts = {
        "maximum_vertices": maximum_vertices,
        "labelled_trees_with_at_least_four_leaves": tree_count,
        "noncut_two_colorings_modulo_color_swap": coloring_count,
        "crossing_bridge_cases": crossing_count,
        "central_component_cases": central_count,
        "counterexamples": 0,
    }
    require(audit["tree_dichotomy"]["finite_falsification"] == facts,
            "stored tree falsification counts")
    require(audit["tree_dichotomy"]["general_proof"] == {
        "branch_monochromaticity": "a_mixed_branch_would_put_its_incident_edge_in_both_color_hulls",
        "central_case": "if_no_edge_lies_in_both_hulls_their_nonempty_intersection_is_one_vertex",
        "crossing_case": "an_edge_in_both_color_hulls_has_both_colors_on_both_sides",
        "hull_intersection_nonempty": "disjoint_color_hulls_would_be_separated_by_a_target_bridge_realizing_the_lost_split",
        "two_branches_per_color": "one_branch_for_a_color_would_make_its_incident_edge_realize_the_split",
    }, "general tree proof contract")
    return facts


H = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)


def inverse_fourier(spectra: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum(Fraction(H[row][col]) * spectra[col] for col in range(4)) / 4
                 for row in range(4))


def convolution(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum(left[state] * right[state ^ output] for state in range(4))
                 for output in range(4))


def spectra_of(probabilities: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum(Fraction(H[row][col]) * probabilities[col] for col in range(4))
                 for row in range(4))


def strict_d3(triple: tuple[Fraction, Fraction, Fraction]) -> bool:
    c, g, t = triple
    return (
        all(0 < value < 1 for value in triple)
        and 1 + c - g - t > 0
        and 1 - c + g - t > 0
        and 1 - c - g + t > 0
    )


def polynomial_switching_sum(reticulations: int) -> dict[tuple[int, ...], int]:
    zero = (0,) * reticulations
    total: dict[tuple[int, ...], int] = {}
    for bits in itertools.product((0, 1), repeat=reticulations):
        weight = {zero: 1}
        for axis, bit in enumerate(bits):
            updated: dict[tuple[int, ...], int] = {}
            for exponent, coefficient in weight.items():
                if bit:
                    raised = list(exponent)
                    raised[axis] += 1
                    key = tuple(raised)
                    updated[key] = updated.get(key, 0) + coefficient
                else:
                    updated[exponent] = updated.get(exponent, 0) + coefficient
                    raised = list(exponent)
                    raised[axis] += 1
                    key = tuple(raised)
                    updated[key] = updated.get(key, 0) - coefficient
            weight = {key: value for key, value in updated.items() if value}
        for exponent, coefficient in weight.items():
            total[exponent] = total.get(exponent, 0) + coefficient
    return {key: value for key, value in total.items() if value}


def verify_k3p_side_blob_closure(audit: dict) -> dict:
    # Exact finite character-table identities.
    orthogonality = 0
    for left in range(4):
        for right in range(4):
            value = sum(H[row][left] * H[row][right] for row in range(4))
            require(value == (4 if left == right else 0), "Hadamard orthogonality")
            orthogonality += 1
    homomorphism = 0
    for character in range(4):
        for left in range(4):
            for right in range(4):
                require(H[character][left ^ right] == H[character][left] * H[character][right],
                        "character homomorphism")
                homomorphism += 1

    triples = (
        (Fraction(1, 2), Fraction(2, 5), Fraction(1, 3)),
        (Fraction(3, 5), Fraction(1, 2), Fraction(2, 5)),
        (Fraction(2, 3), Fraction(3, 5), Fraction(1, 2)),
    )
    require(all(strict_d3(row) for row in triples), "rational edge anchors")
    spectra = tuple((Fraction(1),) + row for row in triples)
    probabilities = tuple(inverse_fourier(row) for row in spectra)
    require(all(all(value > 0 for value in row) and sum(row) == 1 for row in probabilities),
            "positive inverse Fourier anchors")

    # Exact convolution theorem replay on independent rational anchors.
    convolved = convolution(probabilities[0], probabilities[1])
    product_spectra = tuple(spectra[0][index] * spectra[1][index] for index in range(4))
    require(convolved == inverse_fourier(product_spectra), "convolution/product identity")
    require(spectra_of(convolved) == product_spectra, "convolution Fourier inversion")
    require(strict_d3(product_spectra[1:]), "serial strict D3 closure")

    # A two-boundary side blob is a convex mixture of displayed-path kernels.
    path_spectra = (
        spectra[0],
        tuple(spectra[1][index] * spectra[2][index] for index in range(4)),
        tuple(spectra[0][index] * spectra[2][index] for index in range(4)),
    )
    weights = (Fraction(1, 5), Fraction(3, 10), Fraction(1, 2))
    require(sum(weights) == 1 and all(weight > 0 for weight in weights), "mixture weights")
    effective_spectra = tuple(
        sum(weights[path] * path_spectra[path][sector] for path in range(3))
        for sector in range(4)
    )
    mixed_probabilities = tuple(
        sum(weights[path] * inverse_fourier(path_spectra[path])[state]
            for path in range(3))
        for state in range(4)
    )
    require(inverse_fourier(effective_spectra) == mixed_probabilities,
            "inverse Fourier commutes with mixture")
    require(all(value > 0 for value in mixed_probabilities), "mixture probability strictness")
    require(strict_d3(effective_spectra[1:]), "mixture strict D3 closure")

    switching_checks = 0
    switching_terms = 0
    for r in range(3):
        total = polynomial_switching_sum(r)
        require(total == {(0,) * r: 1}, ("switching sum", r))
        switching_checks += 1
        switching_terms += 1 << r

    model_domain = json.loads(PATHS["model_domain"].read_text())
    require(model_domain["inverse_fourier_coefficients_over_4"] == [list(row) for row in H],
            "model-domain Hadamard table")
    require(model_domain["principal_domain_proof"] ==
            "pC,pG,pT>0 are exactly the three displayed composition inequalities; p0>0 follows from c,g,t>0",
            "principal-domain characterization")
    require(model_domain["root_movement_detailed_balance"] is True,
            "K3P detailed balance")

    facts = {
        "hadamard_orthogonality_checks": orthogonality,
        "character_homomorphism_checks": homomorphism,
        "exact_serial_anchor_checks": 1,
        "exact_mixture_anchor_checks": 1,
        "switching_weight_polynomial_checks": switching_checks,
        "switching_components": switching_terms,
        "reticulation_range": [0, 2],
    }
    require(audit["side_blob_closure"]["exact_replay"] == facts,
            "stored side-blob replay facts")
    require(audit["side_blob_closure"]["factorization_contract"] == {
        "bridge_separates_side_latent_variables": True,
        "central_and_side_reticulation_choices_are_disjoint": True,
        "conditional_on_the_central_boundary_state_each_arm_is_a_K3P_kernel": True,
        "different_arms_factor_conditionally": True,
        "off_path_leaf_marginals_equal_one": True,
        "switching_weights_are_state_independent": True,
    }, "side-blob factorization contract")
    require(audit["side_blob_closure"]["strictness_proof"] == {
        "convex_mixture": "inverse_Fourier_probability_vectors_mix_linearly_and_remain_strictly_positive",
        "nontrivial_spectra": "positive_weighted_averages_of_displayed_path_products_remain_in_(0,1)",
        "serial_path": "inverse_Fourier_probability_vectors_convolve_and_remain_strictly_positive",
        "strict_path_reason": "every_selected_arm_contains_a_strict_terminal_leaf_edge",
    }, "side-blob strictness proof")
    require(audit["inheritance_accounting"] == {
        "central_reticulation": "retained_as_lambda_or_complemented_to_1_minus_lambda_or_cancels_when_switchings_become_identical",
        "disjoint_side_components": "their_positive_switching_weights_are_summed_inside_the_effective_arm_kernel",
        "maximum_reticulations_per_blob": 2,
        "retained_values_strict": True,
        "side_and_central_choices_factor": True,
    }, "inheritance accounting")
    return facts


EXPECTED_LOGICAL_STEPS = (
    "directed_target_cut_inclusion",
    "nontrivial_lost_source_split",
    "colored_reduced_tree_dichotomy",
    "crossing_target_bridge_excluded",
    "central_vertex_is_nontrivial_blob",
    "four_monochromatic_branch_labels_selected",
    "primitive_support_and_word_compression",
    "completion_ports_kept_at_zero_character",
    "one_active_204_handoff",
    "side_blob_k3p_compression",
    "inheritance_parameter_accounting",
    "direct_four_taxon_marginal_identity",
    "source_bridge_rank_at_most_four",
    "target_pointwise_rank_at_least_five",
    "rank_contradiction",
    "cut_set_equality",
)


def verify_logic(audit: dict) -> dict:
    global_certificate = json.loads(PATHS["global_certificate"].read_text())
    global_verification = json.loads(PATHS["global_verification"].read_text())
    directed = json.loads(PATHS["directed_logic"].read_text())
    marginal = json.loads(PATHS["marginal"].read_text())
    manuscript = PATHS["jc_manuscript"].read_text()

    require(global_certificate["status"] == "PASS" and global_certificate["blocked_reason"] is None,
            "global producer status")
    require(global_verification["status"] == "PASS", "global verification status")
    require(global_verification["artifact_sha256"] == sha256(PATHS["global_certificate"]),
            "global verification artifact binding")
    require(global_verification["universe_sha256"] == sha256(PATHS["global_universe"]),
            "global verification universe binding")
    require(global_verification["mutation_count"] == 30, "producer mutation count")
    require(global_verification["two_terminal_mixture_components_checked"] == 7,
            "producer side-mixture component checks")

    proof_ids = [row["id"] for row in global_certificate["proof_steps"]]
    require(proof_ids == ["H0", "D1", "L0", "L1", "T1", "T2", "T3", "T4",
                          "M1", "S1", "P1", "P2", "X", "C"], "global proof DAG ids")
    by_id = {row["id"]: row for row in global_certificate["proof_steps"]}
    require("two-boundary side blob" in by_id["T3"]["claim"], "T3 side blobs")
    require("convex mixture" in by_id["S1"]["reason"], "S1 convex mixture")
    require(by_id["P2"]["depends_on"] == ["T4", "S1"], "P2 physical dependency")
    require(global_certificate["strict_physical_marginal"]["two_terminal_blob_mixture_identities"] == {
        "probability_coordinate": "p_eff(h)=sum_s w_s*p_s(h)>0",
        "spectrum_lower_margin": "x_eff=sum_s w_s*x_s>0",
        "spectrum_scope": "x in {c,g,t}",
        "spectrum_upper_margin": "1-x_eff=sum_s w_s*(1-x_s)>0",
        "switching_weights": "w_s>0 and sum_s w_s=1",
    }, "producer mixture identities")

    require(directed["generic_cut_consequences"]["proved_inclusion"] ==
            "Cut(N_prime)_subseteq_Cut(N)", "directed inclusion orientation")
    require(directed["generic_cut_consequences"]["reverse_inclusion_proved"] is False,
            "historical reverse inclusion must remain unproved there")
    require(marginal["source_relative_open_image"]["direct_marginal_of_original_containment"] is True,
            "direct marginal")
    require(marginal["source_relative_open_image"]["target_marginal_openness_used"] is False,
            "target marginal openness")

    # Bind the authoritative topology proof statements used in the handoff.
    snippets = (
        r"\begin{lemma}[Crossing-quartet reduction]",
        "its central configuration is either one active component or one",
        r"\begin{lemma}[Noncut-preserving word compression]",
        "at least two actual labels of each color",
        "every path-sink child",
        "balanced four-through-eight-port binary word distributions",
        "zero survivors",
        "ordinary tree quartet criterion then gives two actual labels of each colour",
        "The four-port compiler enumerates exactly these $72$ active-labelled tensors",
        "gives one strict minor for each of the other $204$ directions",
    )
    normalized_manuscript = " ".join(manuscript.split())
    for snippet in snippets:
        require(" ".join(snippet.split()) in normalized_manuscript,
                ("missing authoritative topology text", snippet))

    noncircularity = audit["noncircularity"]
    require(noncircularity == {
        "common_bridge_tree_assumed": False,
        "bridge_tree_equality_assumed": False,
        "fourteen_orbit_result_used": False,
        "target_open_parameter_section_used": False,
        "target_regular_point_used": False,
        "source_target_factor_correspondence_used": False,
        "only_prior_cut_direction": "Cut(Nprime)_subseteq_Cut(N)",
    }, "audit noncircularity contract")
    require(global_certificate["noncircularity"]["common_bridge_tree_assumed"] is False,
            "producer common bridge tree")
    require(global_certificate["noncircularity"]["fourteen_orbit_classification_imported"] is False,
            "producer fourteen-orbit use")
    require(global_certificate["rank_transfer"]["target_openness_needed"] is False,
            "producer target openness")

    require(audit["finding_during_audit"] == {
        "disposition": "CLOSED_BY_PATCH_AND_INDEPENDENT_REPLAY",
        "initial_gap": "the_first_producer_version_justified_only_serial_edge_products_and_did_not_cover_two_boundary_side_blobs",
        "patched_dependency": "proof_step_S1_and_strict_physical_marginal.two_terminal_blob_mixture_statement",
        "severity": "LOAD_BEARING",
    }, "audit finding disposition")

    steps = audit["logical_steps"]
    require(tuple(row["id"] for row in steps) == EXPECTED_LOGICAL_STEPS,
            "audit logical step ids")
    require(all(row["status"] == "PROVED" for row in steps), "unproved logical step")
    require(all(isinstance(row.get("reason"), str) and row["reason"] for row in steps),
            "missing logical reason")
    require(audit["claim_boundary"] == {
        "strong_class_cut_transfer": "PROVED",
        "universal_pointwise_K3P_cut_recovery": "WITHDRAWN_NOT_USED",
        "conclusion": "Cut(N)=Cut(Nprime)_under_source_relative_containment_in_the_strong_class",
    }, "claim boundary")
    require(audit["remaining_gaps"] == [], "remaining gaps")
    require(audit["status"] == "PASS", "audit status")
    return {
        "producer_proof_steps": len(proof_ids),
        "adversarial_logical_steps": len(steps),
        "producer_mutations_bound": global_verification["mutation_count"],
        "authoritative_topology_snippets": len(snippets),
    }


def verify_manifest() -> int:
    require(MANIFEST.is_file(), "missing manifest")
    rows = []
    for line in MANIFEST.read_text().splitlines():
        if not line.strip():
            continue
        digest, filename = line.split("  ", 1)
        path = HERE / filename
        require(path.is_file(), ("manifest missing file", filename))
        require(sha256(path) == digest, ("manifest digest", filename))
        rows.append(filename)
    require(len(rows) == len(set(rows)), "duplicate manifest rows")
    required = {
        "ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.json",
        "ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.md",
        "verify_global_transfer_adversarial.py",
        "test_global_transfer_adversarial_mutations.py",
        "VERIFICATION_REPORT.json",
        "MUTATION_RESULTS.json",
        "WORK_LOG.md",
    }
    require(set(rows) == required, "manifest file set")
    return len(rows)


def verify(audit_path: Path, check_manifest: bool = False) -> dict:
    audit = json.loads(audit_path.read_text())
    require(audit["schema"] == "k3p-global-transfer-adversarial-audit-v1", "audit schema")
    bindings = verify_bindings(audit)
    finite = verify_direction_universe(audit)
    trees = verify_tree_dichotomy(audit)
    side = verify_k3p_side_blob_closure(audit)
    logic = verify_logic(audit)
    manifest_rows = verify_manifest() if check_manifest else 0
    return {
        "schema": "k3p-global-transfer-adversarial-verification-v1",
        "status": "PASS",
        "audit_sha256": sha256(audit_path),
        "verifier_sha256": sha256(Path(__file__).resolve()),
        "bound_inputs": bindings,
        "finite_handoff": finite,
        "tree_dichotomy": trees,
        "side_blob_closure": side,
        "logic": logic,
        "manifest_rows_checked": manifest_rows,
        "producer_imported": False,
        "universal_pointwise_cut_claim_used": False,
        "common_bridge_tree_used": False,
        "fourteen_orbit_used": False,
        "remaining_gaps": [],
    }


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", type=Path, default=AUDIT)
    parser.add_argument("--check-manifest", action="store_true")
    parser.add_argument("--no-write-report", action="store_true")
    parser.add_argument("--facts-only", action="store_true")
    args = parser.parse_args()
    result = verify(args.audit, check_manifest=args.check_manifest)
    if not args.no_write_report and not args.facts_only:
        atomic_json(VERIFY_REPORT, result)
    if args.facts_only:
        print(json.dumps({
            "finite_handoff": result["finite_handoff"],
            "tree_dichotomy": result["tree_dichotomy"],
            "side_blob_closure": result["side_blob_closure"],
        }, indent=2, sort_keys=True))
    else:
        print(json.dumps({
            "status": result["status"],
            "directions": result["finite_handoff"]["wrong_split_directions"],
            "tree_counterexamples": result["tree_dichotomy"]["counterexamples"],
            "remaining_gaps": len(result["remaining_gaps"]),
        }, sort_keys=True))


if __name__ == "__main__":
    main()
