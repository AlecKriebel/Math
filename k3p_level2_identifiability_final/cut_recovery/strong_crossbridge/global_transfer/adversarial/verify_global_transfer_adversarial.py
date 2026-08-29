#!/usr/bin/env python3
"""Independent fail-closed audit of the strong-class lost-bridge transfer.

This verifier does not import the producer or its verifier.  It reconstructs
the 204 labelled one-active directions from the frozen graph records, checks
the target-tree dichotomy on every labelled tree through seven vertices as an
adversarial finite search, and rederives the K3P two-terminal side-blob
closure from the character table and exact rational arithmetic.

The finite tree search is falsification evidence.  The directed cut inclusion
is checked from a self-contained K3P evidence object that binds the displayed-
tree lemma, exact wrong-flattening minor, balanced-word reduction, and reduced-
palette replay.  The legacy global-logic report and JC manuscript are not
active inputs.
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
    "model_domain": PROJECT / "model_domain/primary_exact_evidence.json",
    "marginal": PROJECT / "marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json",
    "cut_inclusion_evidence": PROJECT / "cut_recovery/strong_crossbridge/global_transfer/K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json",
    "k3p_manuscript": PROJECT / "manuscript/sections/04_physical_topology.tex",
    "displayed_tree_minor_verifier": PROJECT / "cut_recovery/strong_crossbridge/palette_independent/verify_displayed_tree_minor.py",
    "balanced_word_producer": PROJECT / "cut_recovery/strong_crossbridge/palette_independent/enumerate_balanced_word_reduction.py",
    "balanced_word_certificate": PROJECT / "cut_recovery/strong_crossbridge/palette_independent/BALANCED_WORD_REDUCTION_CERTIFICATE.json",
    "reduced_palette_cleanroom": PROJECT / "cut_recovery/strong_crossbridge/palette_independent/verify_reduced_palette_cleanroom.py",
    "reduced_palette_certificate": PROJECT / "cut_recovery/strong_crossbridge/palette_independent/REDUCED_PALETTE_CLEANROOM_CERTIFICATE.json",
    "independent_combinatorics_replay": PROJECT / "cut_recovery/strong_crossbridge/palette_independent/verify_cut_combinatorics.py",
}

# These are deliberately hard-coded rather than copied from the audit JSON.
# Any change to a load-bearing producer or frozen input invalidates this audit.
EXPECTED_SHA256 = {
    "global_certificate": "c713afe83db59ad395961273ae7ace691ee3a2f323f65b4600245545e24321f1",
    "global_universe": "c9f00df0c52bbdec1eb8601f7f9ba1652eb500ae5cf5c299fad3bb086411690f",
    "global_builder": "34d2a80cfe5aed91ca9098c3e3fb00a7ddece8dbedd762f9da051ff60ce361e3",
    "global_verifier": "56dc79c1005cca4b502af0b6c2d260cdf730ea34cdf8b08daf2f35b0347cca47",
    "global_verification": "cd55e4303475206e4cdf916638d0a02138ea9d7ae72386be527db7f70580b57d",
    "local_certificate": "643c29780219a538a5a127341ea91363aa5899d6f0f6fa1dac034889a7fdf06b",
    "local_universe": "674647dc91513ba85a2a72ed5f98d017c61f54ebb9e157975c14f5a94e4ddb9b",
    "local_verification": "210a29ae89b0cd579503a35d05bc06f6ea765f487d0e062020d2e3c7ec225046",
    "local_mutations": "caadd2a3cb9bea9bee272dfff40dacf9a10430577b379c54a1d009979da834bb",
    "frozen_topology": "edbd4afe566ed0ed5d1c518ffe5b21f8f224d547b9c351cb4e1a8c1c613ac086",
    "model_domain": "ac21e4f795537f251377411841d670c1bad4ce06a69ed24f596252c11cb7afb6",
    "marginal": "9a90ba2e075fd20a4867e8a169aa933546b8fbca6feab23a2be7d25a24935d94",
    "cut_inclusion_evidence": "6f3e37bdde95b60f0f598e09040841063e74c416cfdf518f288a5ddcc4b68d29",
    "k3p_manuscript": "de19b751e20ef091f759f86fb4764e9c3c7ee938b1cf3fbdbd1d6a5ba1881b27",
    "displayed_tree_minor_verifier": "56bf98a93b32248174f76161ad00ba5c7c81173edc0493b2bd79b90eeff90c27",
    "balanced_word_producer": "3f7747eac4aa66034d554d80c8b34017d3e3ce472dd49a01fe753bd93f82cb6a",
    "balanced_word_certificate": "23da98a065ca9e0feccfaf06831b8e788b63fb11003d19f07853d738a1031c01",
    "reduced_palette_cleanroom": "406a7f63b4a04bd8f2ab78615bbb214fb107a8da42ad8e48f0eaa840ca8fc83f",
    "reduced_palette_certificate": "79b6763bd10ed5876942cb43b4fb92a79ea6eb3252acf865f56a7c7eb565b758",
    "independent_combinatorics_replay": "30e58475817d4f7a4f91521a4dead5f13d570535d8646a10e658e950f01d34cf",
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


def evidence_payload_digest(value: dict) -> str:
    body = dict(value)
    body.pop("payload_sha256", None)
    return canonical_digest(body)


def verify_cut_inclusion_evidence(audit: dict, evidence: dict | None = None) -> dict:
    """Independently validate the active K3P premise for D1.

    This deliberately does not import either the evidence producer or the
    direct global-transfer verifier.  In particular, a coherently rehashed
    substitution of the legacy report or JC manuscript remains invalid.
    """
    if evidence is None:
        evidence = json.loads(PATHS["cut_inclusion_evidence"].read_text())
    require(set(evidence) == {
        "analytic_implication", "balanced_word_reduction", "claim",
        "displayed_tree_minor", "load_bearing_inputs", "payload_sha256",
        "provenance_policy", "reduced_palette_replay", "remaining_gaps",
        "schema", "status",
    }, "K3P directed-cut evidence key set")
    require(evidence["schema"] == "k3p-directed-cut-inclusion-evidence-v1",
            "K3P directed-cut evidence schema")
    require(evidence["status"] == "PASS" and evidence["remaining_gaps"] == [],
            "K3P directed-cut evidence status")
    require(evidence["payload_sha256"] == evidence_payload_digest(evidence),
            "K3P directed-cut evidence payload digest")
    require(evidence["claim"] == {
        "containment_identity":
            "Phi_N=Phi_Nprime_comp_sigma_on_a_nonempty_source_open_set_U",
        "conclusion": "Cut(Nprime)_subseteq_Cut(N)",
        "source_regular_only": True,
        "target_open_image_not_assumed": True,
        "target_regular_not_assumed": True,
    }, "K3P directed-cut evidence claim")

    source_map = {
        "displayed_tree_lemma": "k3p_manuscript",
        "displayed_tree_minor_verifier": "displayed_tree_minor_verifier",
        "balanced_word_producer": "balanced_word_producer",
        "balanced_word_certificate": "balanced_word_certificate",
        "reduced_palette_cleanroom": "reduced_palette_cleanroom",
        "reduced_palette_certificate": "reduced_palette_certificate",
        "independent_combinatorics_replay": "independent_combinatorics_replay",
    }
    bindings = evidence["load_bearing_inputs"]
    require(set(bindings) == set(source_map), "K3P evidence input set")
    for evidence_name, path_name in source_map.items():
        path = PATHS[path_name]
        expected = {"path": relative(path), "sha256": sha256(path)}
        require(bindings[evidence_name] == expected,
                ("K3P evidence active source binding", evidence_name))
        lowered = expected["path"].lower()
        require("global_logic" not in lowered and
                "referenced_chat_manuscripts" not in lowered,
                ("legacy premise path in active K3P evidence", evidence_name))

    manuscript = " ".join(PATHS["k3p_manuscript"].read_text().split())
    for snippet in (
        r"\begin{lemma}[Displayed-tree witness for a noncut]",
        r"\begin{proposition}[Generic noncut recovery]",
        r"p_0p_1p_2p_3(1-u^2)>0",
        r"\begin{corollary}[The easy directed cut inclusion]",
        r"\operatorname{Cut}(N')\subseteq\operatorname{Cut}(N)",
        r"\begin{lemma}[Balanced noncut compression]",
        "808{,}642",
        "379{,}742",
        "zero all-switching survivors",
    ):
        require(" ".join(snippet.split()) in manuscript,
                ("active K3P manuscript premise", snippet))

    minor_source = PATHS["displayed_tree_minor_verifier"].read_text()
    for snippet in (
        "True quartet split 01|23, flattened across the wrong split 02|13",
        "p0 * p1 * p2 * p3 * (1 - u**2)",
        "nonzero_entries = (p0 * p1, p0 * p1, p0 * p1)",
        "zero_minor.subs(u, 1)",
    ):
        require(snippet in minor_source, ("active exact-minor source", snippet))

    primitive_families = [
        "cycle", "theta_TR_nested", "theta_TR_separated",
        "theta_TT_nested", "theta_TT_separated",
    ]
    family_roles = {(family, role) for family in primitive_families
                    for role in ("root", "nonroot")}
    balanced = json.loads(PATHS["balanced_word_certificate"].read_text())
    require(set(balanced) == {
        "enumeration_commitment_sha256", "failure_count", "failures",
        "families", "mutation_results", "proof_partition", "schema",
        "scope", "status", "totals",
    }, "balanced-word certificate key set")
    require(balanced["schema"] == "stc-jc-cut-palette-reduction-v1" and
            balanced["status"] == "EXACTLY COMPUTED",
            "balanced-word certificate schema/status")
    require(balanced["failure_count"] == 0 and balanced["failures"] == [],
            "balanced-word failures")
    require(balanced["scope"] == {
        "active_port_counts": [4, 5, 6, 7, 8],
        "primitive_families": primitive_families,
        "roles": ["root", "nonroot"],
        "short_palette": [[], [0], [1], [0, 1], [1, 0]],
    }, "balanced-word scope")
    totals = {
        "balanced_total": 808_642,
        "direct_palette": 544_350,
        "singleton_doubled_palette": 34_304,
        "three_run_path_obstruction": 229_988,
    }
    require(balanced["totals"] == totals, "balanced-word totals")
    require({(row["family"], row["role"]) for row in balanced["families"]}
            == family_roles and len(balanced["families"]) == 10,
            "balanced-word family/role coverage")
    require({key: sum(row["counts"][key] for row in balanced["families"])
             for key in totals} == totals, "balanced-word family sums")
    require(len(balanced["mutation_results"]) == 3 and
            all(row["rejected"] is True for row in balanced["mutation_results"]),
            "balanced-word mutations")

    palette = json.loads(PATHS["reduced_palette_certificate"].read_text())
    require(set(palette) == {
        "failures", "families", "palette", "record_commitment_sha256",
        "schema", "status", "survivor_count",
        "total_valid_palette_presentations",
    }, "reduced-palette certificate key set")
    require(palette["schema"] == "stc-jc-reduced-palette-cleanroom-v1" and
            palette["status"] == "EXACTLY COMPUTED",
            "reduced-palette certificate schema/status")
    require(palette["palette"] == [[], [0], [1], [0, 1], [1, 0]],
            "reduced palette")
    require({(row["core"], row["role"]) for row in palette["families"]}
            == family_roles and len(palette["families"]) == 10,
            "reduced-palette family/role coverage")
    valid_presentations = sum(
        row["valid_balanced_compressed"] + row["valid_singleton_doubled"]
        for row in palette["families"]
    )
    require(valid_presentations ==
            palette["total_valid_palette_presentations"] == 379_742,
            "reduced-palette presentation count")
    require(palette["survivor_count"] == 0 and palette["failures"] == [] and
            sum(row["survivor_count"] for row in palette["families"]) == 0,
            "reduced-palette zero survivors")

    require(evidence["balanced_word_reduction"] == {
        "enumeration_commitment_sha256":
            balanced["enumeration_commitment_sha256"],
        "failure_count": 0,
        "families": 10,
        "mutation_count": 3,
        "totals": totals,
    }, "bound balanced-word summary")
    require(evidence["reduced_palette_replay"] == {
        "families": 10,
        "record_commitment_sha256": palette["record_commitment_sha256"],
        "survivors": 0,
        "valid_presentations": 379_742,
    }, "bound reduced-palette summary")

    # Derive both determinant terms from the displayed block.  Exponents are
    # ordered (p0,p1,p2,p3,u); the three one-character anchors add (3,3,0,0,0).
    minor = evidence["displayed_tree_minor"]
    require(isinstance(minor, dict), "displayed-tree minor evidence present")
    require(set(minor) == {
        "augmentation_entries", "boundary_to_strict_physical_by_continuity",
        "displayed_quartet_split", "five_minor_factorization",
        "five_minor_terms", "strict_domain", "strict_nonzero",
        "variable_order", "wrong_flattening", "zero_character_block",
        "zero_minor_factorization", "zero_minor_terms",
    }, "displayed-tree minor key set")
    require(minor["displayed_quartet_split"] == "01|23" and
            minor["wrong_flattening"] == "02|13" and
            minor["variable_order"] == ["p0", "p1", "p2", "p3", "u"],
            "displayed-tree split convention")
    require(minor["zero_character_block"] == [
        ["1", "p1*p3*u"],
        ["p0*p2*u", "p0*p1*p2*p3"],
    ], "displayed-tree zero-character block")
    zero_terms = [
        {"coefficient": 1, "exponents": [1, 1, 1, 1, 0]},
        {"coefficient": -1, "exponents": [1, 1, 1, 1, 2]},
    ]
    require(minor["zero_minor_terms"] == zero_terms and
            minor["zero_minor_factorization"] ==
                "p0*p1*p2*p3*(1-u^2)",
            "displayed-tree zero-minor derivation")
    five_terms = [
        {"coefficient": row["coefficient"],
         "exponents": [exponent + addition for exponent, addition in
                       zip(row["exponents"], [3, 3, 0, 0, 0])]}
        for row in zero_terms
    ]
    require(minor["augmentation_entries"] == ["p0*p1"] * 3 and
            minor["five_minor_terms"] == five_terms and
            minor["five_minor_factorization"] ==
                "p0^4*p1^4*p2*p3*(1-u^2)",
            "displayed-tree five-minor derivation")
    require(minor["strict_domain"] == "0<p0,p1,p2,p3,u<1" and
            minor["strict_nonzero"] is True and
            minor["boundary_to_strict_physical_by_continuity"] is True,
            "displayed-tree strict physical implication")

    expected_implication = {
        "containment_identity": (),
        "source_noncut": (),
        "displayed_switching": ("source_noncut",),
        "wrong_quartet": ("displayed_switching",),
        "source_noncut_nonzero": ("wrong_quartet",),
        "target_cut_vanishing": (),
        "composition_pullback":
            ("containment_identity", "target_cut_vanishing"),
        "open_set_contradiction":
            ("source_noncut_nonzero", "composition_pullback"),
        "directed_conclusion": ("open_set_contradiction",),
    }
    implication = evidence["analytic_implication"]
    require([row["id"] for row in implication] == list(expected_implication),
            "directed-cut implication order")
    seen = set()
    for row in implication:
        require(set(row) == {"id", "depends_on", "claim"},
                ("directed-cut implication row", row.get("id")))
        require(tuple(row["depends_on"]) == expected_implication[row["id"]],
                ("directed-cut implication dependencies", row["id"]))
        require(set(row["depends_on"]) <= seen,
                ("directed-cut implication topological order", row["id"]))
        require(isinstance(row["claim"], str) and row["claim"],
                ("directed-cut implication claim", row["id"]))
        seen.add(row["id"])
    require(implication[-1]["claim"] == "Cut(Nprime)_subseteq_Cut(N)",
            "directed-cut implication conclusion")
    require(evidence["provenance_policy"] == {
        "jc_algebra_used": False,
        "jc_manuscript_is_load_bearing": False,
        "legacy_global_logic_report_is_load_bearing": False,
        "model_independent_graph_certificate_names_retained": True,
    }, "directed-cut provenance policy")

    facts = {
        "schema": evidence["schema"],
        "conclusion": evidence["claim"]["conclusion"],
        "balanced_words": totals["balanced_total"],
        "palette_presentations": valid_presentations,
        "palette_survivors": palette["survivor_count"],
        "exact_minor_terms": len(five_terms),
        "implication_steps": len(implication),
        "legacy_global_logic_used": False,
        "jc_cut_theorem_used": False,
    }
    require(audit["directed_cut_inclusion_evidence"] == facts,
            "stored K3P directed-cut evidence facts")
    return facts


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


EXPECTED_GLOBAL_DEPENDENCIES = {
    "H0": (),
    "K0": (),
    "D1": ("H0", "K0"),
    "L0": ("H0",),
    "L1": ("L0",),
    "T1": ("L0", "L1"),
    "T2": ("D1", "L0", "T1"),
    "T3": ("T1", "T2"),
    "T4": ("T3",),
    "M1": ("H0", "T4"),
    "S1": ("H0", "T4"),
    "P1": ("M1", "L0"),
    "P2": ("T4", "S1"),
    "X": ("M1", "P1", "P2"),
    "C": ("D1", "X"),
}


def verify_global_proof_structure(global_certificate: dict) -> int:
    require(global_certificate["schema"] ==
            "k3p-lost-bridge-global-transfer-certificate-v2",
            "global producer schema")
    proof = global_certificate["proof_steps"]
    require([row["id"] for row in proof] == list(EXPECTED_GLOBAL_DEPENDENCIES),
            "global proof DAG ids")
    by_id = {row["id"]: row for row in proof}
    require(len(by_id) == len(proof), "global proof DAG duplicate ids")
    seen = set()
    for step_id, dependencies in EXPECTED_GLOBAL_DEPENDENCIES.items():
        require(tuple(by_id[step_id]["depends_on"]) == dependencies,
                ("global proof dependency", step_id))
        require(set(dependencies) <= seen,
                ("global proof topological order", step_id))
        seen.add(step_id)
    require("K3P displayed-tree" in by_id["K0"]["claim"],
            "K0 active K3P premise")
    require("Cut(Nprime) subset Cut(N)" in by_id["D1"]["claim"],
            "D1 inclusion orientation")
    require("exact wrong-quartet minor" in by_id["D1"]["reason"],
            "D1 exact K3P minor")
    require(by_id["D1"]["depends_on"] == ["H0", "K0"],
            "D1 consumes K0")
    require("two-boundary side blob" in by_id["T3"]["claim"],
            "T3 side blobs")
    require("convex mixture" in by_id["S1"]["reason"],
            "S1 convex mixture")
    require(by_id["P2"]["depends_on"] == ["T4", "S1"],
            "P2 physical dependency")
    return len(proof)


def verify_logic(audit: dict, cut_facts: dict) -> dict:
    global_certificate = json.loads(PATHS["global_certificate"].read_text())
    global_verification = json.loads(PATHS["global_verification"].read_text())
    marginal = json.loads(PATHS["marginal"].read_text())

    require(global_certificate["status"] == "PASS" and global_certificate["blocked_reason"] is None,
            "global producer status")
    proof_count = verify_global_proof_structure(global_certificate)
    require(global_verification["status"] == "PASS", "global verification status")
    require(global_verification["schema"] ==
            "k3p-lost-bridge-global-transfer-verification-v2",
            "global verification schema")
    require(global_verification["artifact_sha256"] == sha256(PATHS["global_certificate"]),
            "global verification artifact binding")
    require(global_verification["universe_sha256"] == sha256(PATHS["global_universe"]),
            "global verification universe binding")
    require(global_verification["cut_evidence_sha256"] ==
            sha256(PATHS["cut_inclusion_evidence"]),
            "global verification K3P evidence binding")
    require(global_verification["mutation_count"] == 39,
            "producer mutation count")
    require(global_verification["two_terminal_mixture_components_checked"] == 7,
            "producer side-mixture component checks")
    require(global_verification["proof_step_count"] == proof_count == 15,
            "producer proof step count")
    require(global_verification["cut_inclusion_evidence"] == {
        "balanced_words": cut_facts["balanced_words"],
        "implication_steps": cut_facts["implication_steps"],
        "jc_cut_theorem_used": False,
        "legacy_global_logic_used": False,
        "minor_terms": cut_facts["exact_minor_terms"],
        "palette_presentations": cut_facts["palette_presentations"],
        "palette_survivors": cut_facts["palette_survivors"],
    }, "producer K3P evidence summary")

    require(global_certificate["strict_physical_marginal"]["two_terminal_blob_mixture_identities"] == {
        "probability_coordinate": "p_eff(h)=sum_s w_s*p_s(h)>0",
        "spectrum_lower_margin": "x_eff=sum_s w_s*x_s>0",
        "spectrum_scope": "x in {c,g,t}",
        "spectrum_upper_margin": "1-x_eff=sum_s w_s*(1-x_s)>0",
        "switching_weights": "w_s>0 and sum_s w_s=1",
    }, "producer mixture identities")

    require(marginal["source_relative_open_image"]["direct_marginal_of_original_containment"] is True,
            "direct marginal")
    require(marginal["source_relative_open_image"]["target_marginal_openness_used"] is False,
            "target marginal openness")

    noncircularity = audit["noncircularity"]
    require(noncircularity == {
        "common_bridge_tree_assumed": False,
        "bridge_tree_equality_assumed": False,
        "fourteen_orbit_result_used": False,
        "target_open_parameter_section_used": False,
        "target_regular_point_used": False,
        "source_target_factor_correspondence_used": False,
        "directed_cut_inclusion_proved_here": "Cut(Nprime)_subseteq_Cut(N)",
        "legacy_global_logic_report_used": False,
        "jc_model_cut_theorem_used": False,
    }, "audit noncircularity contract")
    require(global_certificate["noncircularity"]["common_bridge_tree_assumed"] is False,
            "producer common bridge tree")
    require(global_certificate["noncircularity"]["fourteen_orbit_classification_imported"] is False,
            "producer fourteen-orbit use")
    require(global_certificate["noncircularity"]["legacy_global_logic_report_used"] is False,
            "producer legacy global-logic use")
    require(global_certificate["noncircularity"]["jc_model_cut_theorem_used"] is False,
            "producer JC cut theorem use")
    require(global_certificate["k3p_directed_cut_inclusion_evidence_pass"] is True,
            "producer active K3P evidence pass")
    require(global_certificate["rank_transfer"]["target_openness_needed"] is False,
            "producer target openness")

    require(audit["certificate_dependency_repair"] == {
        "active_jc_manuscript_dependency": False,
        "active_legacy_global_logic_dependency": False,
        "disposition": "CLOSED_BY_SELF_CONTAINED_K3P_EVIDENCE",
        "initial_gap": "D1_consumed_the_legacy_blocked_global_logic_report_and_JC_manuscript_while_the_K3P_word_minor_evidence_was_parallel_only",
        "replacement": "K0_binds_the_K3P_displayed_tree_lemma_exact_minor_balanced_word_certificate_and_zero_survivor_palette_and_D1_depends_on_K0",
        "semantic_mutations_required": [
            "coherently_resealed_legacy_provenance_substitution",
            "coherently_resealed_exact_minor_removal",
            "global_K0_dependency_deletion",
        ],
    }, "certificate dependency repair")

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
        "producer_proof_steps": proof_count,
        "adversarial_logical_steps": len(steps),
        "producer_mutations_bound": global_verification["mutation_count"],
        "active_k3p_implication_steps": cut_facts["implication_steps"],
        "active_legacy_premises": 0,
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
    require(audit["schema"] == "k3p-global-transfer-adversarial-audit-v2", "audit schema")
    bindings = verify_bindings(audit)
    cut_evidence = verify_cut_inclusion_evidence(audit)
    finite = verify_direction_universe(audit)
    trees = verify_tree_dichotomy(audit)
    side = verify_k3p_side_blob_closure(audit)
    logic = verify_logic(audit, cut_evidence)
    manifest_rows = verify_manifest() if check_manifest else 0
    return {
        "schema": "k3p-global-transfer-adversarial-verification-v2",
        "status": "PASS",
        "audit_sha256": sha256(audit_path),
        "verifier_sha256": sha256(Path(__file__).resolve()),
        "bound_inputs": bindings,
        "directed_cut_inclusion_evidence": cut_evidence,
        "finite_handoff": finite,
        "tree_dichotomy": trees,
        "side_blob_closure": side,
        "logic": logic,
        "manifest_rows_checked": manifest_rows,
        "producer_imported": False,
        "universal_pointwise_cut_claim_used": False,
        "common_bridge_tree_used": False,
        "fourteen_orbit_used": False,
        "legacy_global_logic_used": False,
        "jc_cut_theorem_used": False,
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
