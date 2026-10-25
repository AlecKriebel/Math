#!/usr/bin/env python3
"""Independent audit of the lost-bridge global-transfer proof.

This verifier does not import the builder or any fourteen-orbit code.  It
recomputes the topology-only 204-direction universe from frozen switching
signatures, checks the exact dependency DAG, audits split compatibility and
strict K3P convolution, and binds the independently verified pointwise local
certificate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
DEFAULT_ARTIFACT = HERE / "GLOBAL_TRANSFER_CERTIFICATE.json"
DEFAULT_UNIVERSE = HERE / "GLOBAL_TRANSFER_DIRECTION_UNIVERSE.json"
REPORT = HERE / "VERIFICATION_REPORT.json"
FROZEN_TOPOLOGY = PROJECT / "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json"
MARGINAL = PROJECT / "marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json"
CUT_EVIDENCE = HERE / "K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json"
MANUSCRIPT = PROJECT / "manuscript/sections/04_physical_topology.tex"
PALETTE = HERE.parent / "palette_independent"
MINOR_VERIFIER = PALETTE / "verify_displayed_tree_minor.py"
BALANCED_PRODUCER = PALETTE / "enumerate_balanced_word_reduction.py"
BALANCED_CERTIFICATE = PALETTE / "BALANCED_WORD_REDUCTION_CERTIFICATE.json"
PALETTE_PRODUCER = PALETTE / "verify_reduced_palette_cleanroom.py"
PALETTE_CERTIFICATE = PALETTE / "REDUCED_PALETTE_CLEANROOM_CERTIFICATE.json"
COMBINATORICS_REPLAY = PALETTE / "verify_cut_combinatorics.py"
LOCAL_FINAL = HERE.parent / "final_certificate/STRONG_CROSSBRIDGE_FINAL_CERTIFICATE.json"
LOCAL_UNIVERSE = HERE.parent / "final_certificate/UNIVERSE_CERTIFICATE.json"
LOCAL_VERIFICATION = HERE.parent / "final_certificate/VERIFICATION_REPORT.json"
LOCAL_MUTATIONS = HERE.parent / "final_certificate/ADVERSARIAL_MUTATION_REPORT.json"


# Deliberately duplicated rather than imported from the producer.  Exact
# equality with this typed object is part of the certificate contract.
EXPECTED_ANALYTIC_IMPLICATION = [
    {
        "id": "containment_identity",
        "depends_on": [],
        "claim": {
            "type": "analytic_identity_on_source_open_set",
            "identity": "Phi_N=Phi_Nprime_comp_sigma",
            "domain": "nonempty_source_open_set_U",
        },
    },
    {
        "id": "source_noncut",
        "depends_on": [],
        "claim": {
            "type": "source_split_assumption",
            "candidate_split_is_source_bridge": False,
        },
    },
    {
        "id": "displayed_switching",
        "depends_on": ["source_noncut"],
        "claim": {
            "type": "displayed_tree_witness",
            "mechanism": "hull_or_balanced_compression",
            "witness": "displayed_tree_not_displaying_candidate_split",
        },
    },
    {
        "id": "wrong_quartet",
        "depends_on": ["displayed_switching"],
        "claim": {
            "type": "labelled_wrong_quartet_extraction",
            "actual_label_count": 4,
            "candidate_split_displayed": False,
        },
    },
    {
        "id": "source_noncut_nonzero",
        "depends_on": ["wrong_quartet"],
        "claim": {
            "type": "nonzero_source_polynomial_witness",
            "polynomial": "wrong_split_5x5_flattening_minor",
            "nonzero_reason": "displayed_tree_specialization",
        },
    },
    {
        "id": "target_cut_vanishing",
        "depends_on": [],
        "claim": {
            "type": "target_cut_polynomial_identity",
            "polynomial_family": "all_5x5_flattening_minors",
            "value": "identically_zero",
        },
    },
    {
        "id": "composition_pullback",
        "depends_on": ["containment_identity", "target_cut_vanishing"],
        "claim": {
            "type": "composition_pullback_identity",
            "polynomial": "same_wrong_split_5x5_flattening_minor",
            "domain": "source_open_set_U",
            "value": "zero",
        },
    },
    {
        "id": "open_set_contradiction",
        "depends_on": ["source_noncut_nonzero", "composition_pullback"],
        "claim": {
            "type": "real_polynomial_open_set_principle",
            "premise": "nonzero_real_polynomial_vanishes_on_nonempty_open_set",
            "conclusion": "contradiction",
        },
    },
    {
        "id": "directed_conclusion",
        "depends_on": ["open_set_contradiction"],
        "claim": {
            "type": "directed_cut_inclusion",
            "conclusion": "Cut(Nprime)_subseteq_Cut(N)",
        },
    },
]


class VerificationError(RuntimeError):
    pass


def require(condition, label):
    if not condition:
        raise VerificationError(str(label))


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    answer = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            answer.update(block)
    return answer.hexdigest()


def expected_binding(path: Path):
    return {
        "path": str(path.resolve().relative_to(PROJECT)),
        "sha256": sha_file(path),
    }


def payload_digest(value: dict) -> str:
    body = dict(value)
    body.pop("payload_sha256", None)
    return digest(body)


def verify_cut_inclusion_evidence(evidence: dict) -> dict:
    require(set(evidence) == {
        "analytic_implication", "balanced_word_reduction", "claim",
        "displayed_tree_minor", "load_bearing_inputs", "payload_sha256",
        "provenance_policy", "reduced_palette_replay", "remaining_gaps",
        "schema", "status",
    }, "K3P cut evidence key set")
    require(evidence["schema"] == "k3p-directed-cut-inclusion-evidence-v2",
            "K3P cut evidence schema")
    require(evidence["status"] == "PASS" and evidence["remaining_gaps"] == [],
            "K3P cut evidence status")
    require(evidence["payload_sha256"] == payload_digest(evidence),
            "K3P cut evidence payload")
    require(evidence["claim"] == {
        "containment_identity":
            "Phi_N=Phi_Nprime_comp_sigma_on_a_nonempty_source_open_set_U",
        "conclusion": "Cut(Nprime)_subseteq_Cut(N)",
        "source_regular_only": True,
        "target_open_image_not_assumed": True,
        "target_regular_not_assumed": True,
    }, "K3P cut evidence claim")

    expected_inputs = {
        "displayed_tree_lemma": MANUSCRIPT,
        "displayed_tree_minor_verifier": MINOR_VERIFIER,
        "balanced_word_producer": BALANCED_PRODUCER,
        "balanced_word_certificate": BALANCED_CERTIFICATE,
        "reduced_palette_cleanroom": PALETTE_PRODUCER,
        "reduced_palette_certificate": PALETTE_CERTIFICATE,
        "independent_combinatorics_replay": COMBINATORICS_REPLAY,
    }
    require(set(evidence["load_bearing_inputs"]) == set(expected_inputs),
            "K3P cut evidence input set")
    for name, path in expected_inputs.items():
        require(evidence["load_bearing_inputs"][name] == expected_binding(path),
                ("K3P cut evidence input", name))

    manuscript = " ".join(MANUSCRIPT.read_text().split())
    for snippet in (
        r"\begin{lemma}[Displayed-tree witness for a noncut]",
        r"\begin{proposition}[Generic noncut recovery]",
        r"p_0p_1p_2p_3(1-u^2)>0",
        r"\begin{corollary}[The easy directed cut inclusion]",
        r"\operatorname{Cut}(N')\subseteq\operatorname{Cut}(N)",
        r"\begin{lemma}[Balanced noncut compression]",
    ):
        require(" ".join(snippet.split()) in manuscript,
                ("K3P cut manuscript premise", snippet))

    balanced = json.loads(BALANCED_CERTIFICATE.read_text())
    require(balanced["schema"] == "stc-jc-cut-palette-reduction-v1" and
            balanced["status"] == "EXACTLY COMPUTED" and
            balanced["failure_count"] == 0 and balanced["failures"] == [],
            "balanced certificate semantics")
    require(balanced["scope"] == {
        "active_port_counts": [4, 5, 6, 7, 8],
        "primitive_families": [
            "cycle", "theta_TR_nested", "theta_TR_separated",
            "theta_TT_nested", "theta_TT_separated",
        ],
        "roles": ["root", "nonroot"],
        "short_palette": [[], [0], [1], [0, 1], [1, 0]],
    }, "balanced scope")
    require(balanced["totals"] == {
        "balanced_total": 808_642,
        "direct_palette": 544_350,
        "singleton_doubled_palette": 34_304,
        "three_run_path_obstruction": 229_988,
    }, "balanced totals")
    require(len(balanced["families"]) == 10 and len({
        (row["family"], row["role"], row["fixed_extra_count"])
        for row in balanced["families"]
    }) == 10, "balanced family uniqueness")
    require({
        key: sum(row["counts"][key] for row in balanced["families"])
        for key in balanced["totals"]
    } == balanced["totals"], "balanced family sums")
    require(len(balanced["mutation_results"]) == 3 and
            all(row["rejected"] is True for row in balanced["mutation_results"]),
            "balanced mutation semantics")

    palette = json.loads(PALETTE_CERTIFICATE.read_text())
    require(palette["schema"] == "stc-jc-reduced-palette-cleanroom-v1" and
            palette["status"] == "EXACTLY COMPUTED" and
            palette["palette"] == [[], [0], [1], [0, 1], [1, 0]],
            "palette semantics")
    require(len(palette["families"]) == 10 and len({
        (row["core"], row["role"]) for row in palette["families"]
    }) == 10, "palette family uniqueness")
    valid = sum(
        row["valid_balanced_compressed"] + row["valid_singleton_doubled"]
        for row in palette["families"]
    )
    require(valid == palette["total_valid_palette_presentations"] == 379_742,
            "palette valid presentation count")
    require(palette["survivor_count"] == 0 and palette["failures"] == [] and
            sum(row["survivor_count"] for row in palette["families"]) == 0,
            "palette survivors")

    reduction = evidence["balanced_word_reduction"]
    require(reduction == {
        "enumeration_commitment_sha256":
            balanced["enumeration_commitment_sha256"],
        "failure_count": 0,
        "families": 10,
        "mutation_count": 3,
        "totals": balanced["totals"],
    }, "bound balanced summary")
    require(evidence["reduced_palette_replay"] == {
        "families": 10,
        "record_commitment_sha256": palette["record_commitment_sha256"],
        "survivors": 0,
        "valid_presentations": 379_742,
    }, "bound palette summary")

    minor = evidence["displayed_tree_minor"]
    require(minor["zero_character_block"] == [
        ["1", "p1*p3*u"], ["p0*p2*u", "p0*p1*p2*p3"],
    ], "zero-character block")
    zero_terms = [
        {"coefficient": 1, "exponents": [1, 1, 1, 1, 0]},
        {"coefficient": -1, "exponents": [1, 1, 1, 1, 2]},
    ]
    require(minor["zero_minor_terms"] == zero_terms and
            minor["zero_minor_factorization"] == "p0*p1*p2*p3*(1-u^2)",
            "zero-minor derivation")
    augmentation = [3, 3, 0, 0, 0]
    five_terms = [
        {"coefficient": row["coefficient"],
         "exponents": [left + right for left, right in
                       zip(row["exponents"], augmentation)]}
        for row in zero_terms
    ]
    require(minor["augmentation_entries"] == ["p0*p1"] * 3 and
            minor["five_minor_terms"] == five_terms and
            minor["five_minor_factorization"] ==
                "p0^4*p1^4*p2*p3*(1-u^2)", "five-minor derivation")
    require(minor["strict_domain"] == "0<p0,p1,p2,p3,u<1" and
            minor["strict_nonzero"] is True and
            minor["boundary_to_strict_physical_by_continuity"] is True,
            "strict minor implication")

    steps = evidence["analytic_implication"]
    require(steps == EXPECTED_ANALYTIC_IMPLICATION,
            "K3P cut exact typed analytic implication")
    seen = set()
    for row in steps:
        require(set(row) == {"id", "depends_on", "claim"},
                ("K3P cut implication row", row.get("id")))
        require(set(row["depends_on"]) <= seen,
                ("K3P cut implication topological order", row["id"]))
        require(isinstance(row["claim"], dict) and
                isinstance(row["claim"].get("type"), str),
                ("K3P cut typed implication claim", row["id"]))
        seen.add(row["id"])
    require(steps[-1]["claim"] == {
        "type": "directed_cut_inclusion",
        "conclusion": "Cut(Nprime)_subseteq_Cut(N)",
    },
            "K3P cut implication conclusion")
    require(evidence["provenance_policy"] == {
        "jc_algebra_used": False,
        "jc_manuscript_is_load_bearing": False,
        "legacy_global_logic_report_is_load_bearing": False,
        "model_independent_graph_certificate_names_retained": True,
    }, "K3P cut evidence provenance")
    return {
        "balanced_words": balanced["totals"]["balanced_total"],
        "palette_presentations": palette["total_valid_palette_presentations"],
        "palette_survivors": palette["survivor_count"],
        "minor_terms": len(five_terms),
        "implication_steps": len(steps),
        "legacy_global_logic_used": False,
        "jc_cut_theorem_used": False,
    }


def permute_mask(mask: int, old_order: tuple[int, ...]) -> int:
    answer = 0
    for new, old in enumerate(old_order):
        if mask & (1 << old):
            answer |= 1 << new
    return answer


def displayed_by_all(signatures, reticulation_count, first):
    side = sum(1 << label for label in first)
    complement = 15 ^ side
    return all(
        any(signature[switch] in (side, complement) for signature in signatures)
        for switch in range(1 << reticulation_count)
    )


def rebuild_directions(topology):
    rows = []
    raw = 0
    displayed = 0
    keys = set()
    section = topology["one_active_wrong_split"]
    for expected_record_id, record in enumerate(section["records"]):
        require(record["id"] == expected_record_id, "record order")
        reticulations = int(record["reticulation_count"])
        signatures = tuple(tuple(int(mask) for mask in row) for row in record["signatures"])
        require(all(len(row) == 1 << reticulations for row in signatures), "signature width")
        for split in record["splits"]:
            raw += 1
            first = tuple(int(label) for label in split["split"])
            computed = displayed_by_all(signatures, reticulations, first)
            require(computed == split["displayed_by_all"], "displayed flag replay")
            if computed:
                displayed += 1
                continue
            complement = tuple(sorted(set(range(4)) - set(first)))
            old_order = first + complement
            key = (record["id"], tuple(sorted((tuple(sorted(first)), complement))))
            require(key not in keys, "direction uniqueness")
            keys.add(key)
            normalized = tuple(
                tuple(permute_mask(mask, old_order) for mask in signature)
                for signature in signatures
            )
            rows.append(
                {
                    "target_index": len(rows),
                    "record_id": record["id"],
                    "reticulation_count": reticulations,
                    "old_split": list(first),
                    "old_order": list(old_order),
                    "normalized_split": [[0, 1], [2, 3]],
                    "normalized_signatures_sha256": digest(normalized),
                    "direction_key": [
                        record["id"],
                        [list(key[1][0]), list(key[1][1])],
                    ],
                }
            )
    require(len(section["records"]) == 72, "one-active records")
    require(raw == 216 and displayed == 12 and len(rows) == 204, "direction census")
    require(len(keys) == 204, "direction key census")
    return rows, raw, displayed


def verify_topology_universe(universe, topology):
    require(universe["schema"] == "k3p-global-transfer-direction-universe-v1", "universe schema")
    require(universe["status"] == "PASS", "universe status")
    require(universe["input"] == expected_binding(FROZEN_TOPOLOGY), "universe input")
    require(universe["algebraic_JC_minor_fields_used"] is False, "JC algebra field use")
    rows, raw, displayed = rebuild_directions(topology)
    counts = universe["counts"]
    require(counts["primitive_core_templates"] == 5, "core count")
    require(counts["one_active_records"] == 72, "record count")
    require(counts["raw_labelled_split_entries"] == raw == 216, "raw split count")
    require(counts["displayed_by_all_removed"] == displayed == 12, "displayed split count")
    require(counts["wrong_split_directions"] == 204, "wrong split count")
    require(counts["unique_direction_keys"] == 204, "unique directions")
    require(universe["independent_displayed_flag_recomputation_failures"] == [], "display replay failures")
    require(universe["directions"] == rows, "direction rows")
    require(universe["directions_sha256"] == digest(rows), "direction digest")
    return rows


def split_compatible(first, second, labels):
    first = set(first)
    second = set(second)
    first_complement = set(labels) - first
    second_complement = set(labels) - second
    intersections = (
        first & second,
        first & second_complement,
        first_complement & second,
        first_complement & second_complement,
    )
    return any(not part for part in intersections), tuple(len(part) for part in intersections)


def verify_crossing_split_logic(payload):
    two_active = payload["two_active_exclusion"]
    require(two_active["four_nonempty_intersections"] == ["A∩C", "A∩D", "B∩C", "B∩D"], "four intersections")
    compatible, sizes = split_compatible({0, 1}, {0, 2}, range(4))
    require(sizes == (1, 1, 1, 1), "crossing witness intersections")
    require(compatible is False, "crossing splits called compatible")
    require("R in Cut(Nprime) implies R in Cut(N)" == two_active["directional_step"], "directional use")
    return sizes


def verify_k3p_convolution(payload, marginal):
    table = marginal["character_group"]["xor_table"]
    require(table == [[left ^ right for right in range(4)] for left in range(4)], "XOR table")

    # Exact character-homomorphism replay.  It proves that convolution of the
    # inverse-Fourier probability vectors has coordinatewise-product spectra.
    bit_pair = ((0, 0), (1, 0), (0, 1), (1, 1))
    hadamard = []
    for character in bit_pair:
        row = []
        for state in bit_pair:
            parity = character[0] * state[0] + character[1] * state[1]
            row.append(-1 if parity % 2 else 1)
        hadamard.append(row)
    homomorphism_checks = 0
    for character in range(4):
        for left in range(4):
            for right in range(4):
                require(
                    hadamard[character][left ^ right]
                    == hadamard[character][left] * hadamard[character][right],
                    "character homomorphism",
                )
                homomorphism_checks += 1

    # Each of the four convolution coordinates is a sum of four products of
    # strictly positive entries and is therefore strictly positive.
    convolution_pairs = {
        output: tuple((left, left ^ output) for left in range(4))
        for output in range(4)
    }
    require(all(len(set(pairs)) == 4 for pairs in convolution_pairs.values()), "convolution pairs")

    # Independently expand the switching weights for every level-2 side blob.
    # Their sum is the constant polynomial one, and each unexpanded factor is
    # lambda_i or 1-lambda_i, hence strictly positive on the physical domain.
    switching_components = 0
    switching_sum_checks = 0
    for reticulation_count in range(3):
        zero = (0,) * reticulation_count
        total = {}
        for bits in itertools.product((0, 1), repeat=reticulation_count):
            switching_components += 1
            weight = {zero: 1}
            for axis, bit in enumerate(bits):
                updated = {}
                for exponent, coefficient in weight.items():
                    if bit:
                        raised = list(exponent); raised[axis] += 1
                        updated[tuple(raised)] = updated.get(tuple(raised), 0) + coefficient
                    else:
                        updated[exponent] = updated.get(exponent, 0) + coefficient
                        raised = list(exponent); raised[axis] += 1
                        updated[tuple(raised)] = updated.get(tuple(raised), 0) - coefficient
                weight = {exponent: coefficient for exponent, coefficient in updated.items() if coefficient}
            for exponent, coefficient in weight.items():
                total[exponent] = total.get(exponent, 0) + coefficient
        total = {exponent: coefficient for exponent, coefficient in total.items() if coefficient}
        require(total == {zero: 1}, ("switching weights do not sum to one", reticulation_count))
        switching_sum_checks += 1

    strict = payload["strict_physical_marginal"]
    require("convolution" in strict["serial_convolution_statement"], "edge convolution statement")
    require("convex mixture" in strict["two_terminal_blob_mixture_statement"], "two-terminal mixture statement")
    require("strict positivity" in strict["two_terminal_blob_mixture_statement"], "mixture strictness")
    mixture_identities = strict["two_terminal_blob_mixture_identities"]
    require(mixture_identities["switching_weights"] == "w_s>0 and sum_s w_s=1", "mixture weights identity")
    require(mixture_identities["probability_coordinate"] == "p_eff(h)=sum_s w_s*p_s(h)>0", "mixture probability identity")
    require(mixture_identities["spectrum_lower_margin"] == "x_eff=sum_s w_s*x_s>0", "mixture lower margin")
    require(mixture_identities["spectrum_upper_margin"] == "1-x_eff=sum_s w_s*(1-x_s)>0", "mixture upper margin")
    require(mixture_identities["spectrum_scope"] == "x in {c,g,t}", "mixture spectrum scope")
    require("retained as lambda" in strict["inheritance_statement"], "inheritance statement")
    require("set to zero" in strict["Fourier_marginal_statement"], "Fourier marginal statement")
    require(marginal["switching_and_inheritance"]["weights_sum_to_one"] is True, "inheritance weights")
    return (
        homomorphism_checks,
        sum(map(len, convolution_pairs.values())),
        switching_sum_checks,
        switching_components,
    )


EXPECTED_DEPENDENCIES = {
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


def verify_proof_dag(payload):
    steps = payload["proof_steps"]
    require([row["id"] for row in steps] == list(EXPECTED_DEPENDENCIES), "proof step order")
    by_id = {row["id"]: row for row in steps}
    require(len(by_id) == len(steps), "duplicate proof ids")
    seen = set()
    for step_id, expected in EXPECTED_DEPENDENCIES.items():
        row = by_id[step_id]
        require(tuple(row["depends_on"]) == expected, ("proof dependencies", step_id))
        require(set(row["depends_on"]) <= seen, ("non-topological DAG", step_id))
        seen.add(step_id)
    require(payload["proof_step_ids_sha256"] == digest(list(EXPECTED_DEPENDENCIES)), "proof ids digest")
    require("K3P displayed-tree" in by_id["K0"]["claim"], "active K3P premise")
    require("Cut(Nprime) subset Cut(N)" in by_id["D1"]["claim"], "proved inclusion direction")
    require("exact wrong-quartet minor" in by_id["D1"]["reason"], "D1 K3P minor reason")
    require("two-active" in by_id["T2"]["claim"], "two-active exclusion")
    require("204-direction" in by_id["T4"]["claim"], "finite handoff")
    require("no target-open" in by_id["M1"]["reason"], "target openness leak")
    require("strict physical D3,+" in by_id["S1"]["claim"], "strict target marginal")
    require("rank at most four" in by_id["P1"]["claim"], "source rank")
    require("rank greater than four" in by_id["P2"]["claim"], "target rank")
    return len(steps)


def verify_local_pointwise(payload, independently_rebuilt_rows):
    final = json.loads(LOCAL_FINAL.read_text())
    universe = json.loads(LOCAL_UNIVERSE.read_text())
    verification = json.loads(LOCAL_VERIFICATION.read_text())
    mutations = json.loads(LOCAL_MUTATIONS.read_text())
    bindings = payload["load_bearing_inputs"]
    require(set(bindings) == {
        "frozen_strong_topology", "selected_marginal",
        "k3p_directed_cut_inclusion_evidence", "recompiled_direction_universe",
        "pointwise_204_certificate", "pointwise_204_universe",
        "pointwise_204_independent_verification",
        "pointwise_204_adversarial_mutations",
    }, "global-transfer load-bearing input set")
    require(bindings["pointwise_204_certificate"] == expected_binding(LOCAL_FINAL), "local final binding")
    require(bindings["pointwise_204_universe"] == expected_binding(LOCAL_UNIVERSE), "local universe binding")
    require(bindings["pointwise_204_independent_verification"] == expected_binding(LOCAL_VERIFICATION), "local verification binding")
    require(bindings["pointwise_204_adversarial_mutations"] == expected_binding(LOCAL_MUTATIONS), "local mutation binding")
    require(final["schema"] == "k3p-strong-crossbridge-final-certificate-v1", "local schema")
    require(final["status"] == "PASS" and final["blocked_dependencies"] == [], "local status")
    coverage = final["coverage"]
    require(coverage["target_directions"] == 204, "local coverage")
    require(coverage["pairwise_disjoint"] is True and coverage["union_is_all_204"] is True, "local partition flags")
    require(coverage["automorphism_transport_used"] is False, "local automorphism transport")
    targets = []
    for dependency in final["dependencies"]:
        require(dependency["status"] == "PASS", ("local dependency", dependency["name"]))
        targets.extend(dependency["required_targets"])
    require(len(targets) == len(set(targets)) == 204, "local target partition cardinality")
    require(set(targets) == set(range(204)), "local target partition union")
    require(universe["status"] == "PASS" and len(universe["directions"]) == 204, "local universe status")
    require(
        [row["normalized_signatures_sha256"] for row in universe["directions"]]
        == [row["normalized_signatures_sha256"] for row in independently_rebuilt_rows],
        "local/global direction crosswalk",
    )
    require(verification["schema"] == "k3p-strong-crossbridge-final-verification-v1", "local verification schema")
    require(verification["status"] == "PASS", "local verification status")
    require(verification["artifacts"]["final_certificate_sha256"] == sha_file(LOCAL_FINAL), "local verification final hash")
    require(verification["artifacts"]["universe_certificate_sha256"] == sha_file(LOCAL_UNIVERSE), "local verification universe hash")
    require(mutations["schema"] == "k3p-strong-crossbridge-final-adversarial-mutations-v1", "local mutation schema")
    require(mutations["status"] == "PASS" and mutations["all_mutations_rejected"] is True, "local mutations")
    require(mutations["rejected_count"] == mutations["mutation_count"] == 34, "local mutation count")
    require(payload["local_204_dependency_pass"] is True, "payload local pass")
    return len(targets), mutations["mutation_count"]


def verify_payload(payload, universe, cut_evidence, cut_evidence_path=CUT_EVIDENCE):
    require(payload["schema"] == "k3p-lost-bridge-global-transfer-certificate-v2", "schema")
    require(payload["status"] == "PASS", "status")
    require(payload["blocked_reason"] is None, "blocked reason")
    scope = payload["scope"]
    require(scope["network_class"] == "binary standard semi-directed strongly tree-child level-2", "network class")
    require(scope["conclusion"] == "Cut(N)=Cut(Nprime)", "conclusion")

    bindings = payload["load_bearing_inputs"]
    require(bindings["frozen_strong_topology"] == expected_binding(FROZEN_TOPOLOGY), "topology binding")
    require(bindings["selected_marginal"] == expected_binding(MARGINAL), "marginal binding")
    require(bindings["k3p_directed_cut_inclusion_evidence"] ==
            expected_binding(cut_evidence_path),
            "K3P directed-cut evidence binding")
    require(bindings["recompiled_direction_universe"] == expected_binding(DEFAULT_UNIVERSE), "direction universe binding")

    topology = json.loads(FROZEN_TOPOLOGY.read_text())
    marginal = json.loads(MARGINAL.read_text())
    require(topology["status"] == "EXACTLY COMPUTED", "topology status")
    require(len(topology["primitive_cores"]) == 5, "primitive core count")
    require(topology["primitive_orientation_derivation"]["template_match"] is True, "primitive templates")
    require(topology["switching_compression"]["status"] == "EXACTLY COMPUTED", "switching compression status")
    require(topology["switching_compression"]["survivor_count"] == 0, "switching survivors")
    require(topology["switching_compression"]["failures"] == [], "switching failures")
    rows = verify_topology_universe(universe, topology)
    require(payload["one_active_handoff"]["wrong_split_directions"] == 204, "handoff direction count")
    require(payload["one_active_handoff"]["direction_universe_sha256"] == sha_file(DEFAULT_UNIVERSE), "handoff universe hash")

    require(marginal["status"] == "PASS" and marginal["k2p_algebra_used"] is False, "marginal status")
    source_relative = marginal["source_relative_open_image"]
    require(source_relative["direct_marginal_of_original_containment"] is True, "direct marginal")
    require(source_relative["target_marginal_openness_used"] is False, "target marginal openness")
    cut_evidence_summary = verify_cut_inclusion_evidence(cut_evidence)
    require(payload["k3p_directed_cut_inclusion_evidence_pass"] is True,
            "payload K3P directed-cut evidence pass")

    noncircular = payload["noncircularity"]
    require(noncircular["common_bridge_tree_assumed"] is False, "common bridge tree assumption")
    require(noncircular["bridge_tree_equality_assumed"] is False, "bridge equality assumption")
    require(noncircular["fourteen_orbit_classification_imported"] is False, "fourteen-orbit import")
    require(noncircular["target_regular_point_assumed"] is False, "target regular point")
    require(noncircular["target_open_marginal_assumed"] is False, "target-open marginal")
    require(noncircular["legacy_global_logic_report_used"] is False,
            "legacy global-logic premise")
    require(noncircular["jc_model_cut_theorem_used"] is False,
            "JC model cut premise")
    require(noncircular["directed_cut_inclusion_proved_here"] ==
            "Cut(Nprime) subset Cut(N)", "directed inclusion proof")
    require(noncircular["reverse_direction_proved_here"] == "Cut(N) subset Cut(Nprime)", "new direction")

    require("pendant leaf bridge" in payload["trivial_split_handling"], "trivial split handling")
    intersections = verify_crossing_split_logic(payload)
    (
        homomorphism_checks,
        convolution_terms,
        switching_sum_checks,
        switching_components,
    ) = verify_k3p_convolution(payload, marginal)
    proof_steps = verify_proof_dag(payload)
    local_targets, local_mutations = verify_local_pointwise(payload, rows)

    rank = payload["rank_transfer"]
    require(rank["source_bridge_rank_bound"] == 4, "source rank bound")
    require(rank["target_local_rank_lower_bound"] == 5, "target rank lower bound")
    require(rank["target_pointwise_not_generic"] is True, "pointwise target use")
    require(rank["target_openness_needed"] is False, "target openness needed")
    require("for every theta in U" in rank["identity"], "pointwise marginal identity")
    return {
        "status": "PASS",
        "direction_count": len(rows),
        "proof_step_count": proof_steps,
        "crossing_intersection_sizes": list(intersections),
        "character_homomorphism_checks": homomorphism_checks,
        "strict_convolution_product_terms": convolution_terms,
        "switching_weight_polynomial_checks": switching_sum_checks,
        "two_terminal_mixture_components_checked": switching_components,
        "local_targets_bound": local_targets,
        "local_mutations_bound": local_mutations,
        "cut_inclusion_evidence": cut_evidence_summary,
        "common_bridge_tree_used": False,
        "fourteen_orbit_used": False,
    }


def mutation_cases(payload):
    cases = []
    def changed(name, mutate):
        value = copy.deepcopy(payload)
        mutate(value)
        cases.append((name, value))

    changed("status", lambda x: x.__setitem__("status", "BLOCKED"))
    changed("common_bridge_tree", lambda x: x["noncircularity"].__setitem__("common_bridge_tree_assumed", True))
    changed("bridge_tree_equality", lambda x: x["noncircularity"].__setitem__("bridge_tree_equality_assumed", True))
    changed("fourteen_orbit", lambda x: x["noncircularity"].__setitem__("fourteen_orbit_classification_imported", True))
    changed("target_open", lambda x: x["noncircularity"].__setitem__("target_open_marginal_assumed", True))
    changed("directed_cut_inclusion", lambda x: x["noncircularity"].__setitem__("directed_cut_inclusion_proved_here", "Cut(N) subset Cut(Nprime)"))
    changed("new_cut_direction", lambda x: x["noncircularity"].__setitem__("reverse_direction_proved_here", "Cut(Nprime) subset Cut(N)"))
    changed("legacy_global_logic", lambda x: x["noncircularity"].__setitem__("legacy_global_logic_report_used", True))
    changed("jc_model_cut", lambda x: x["noncircularity"].__setitem__("jc_model_cut_theorem_used", True))
    changed("topology_hash", lambda x: x["load_bearing_inputs"]["frozen_strong_topology"].__setitem__("sha256", "0" * 64))
    changed("marginal_hash", lambda x: x["load_bearing_inputs"]["selected_marginal"].__setitem__("sha256", "1" * 64))
    changed("cut_evidence_hash", lambda x: x["load_bearing_inputs"]["k3p_directed_cut_inclusion_evidence"].__setitem__("sha256", "4" * 64))
    changed("local_hash", lambda x: x["load_bearing_inputs"]["pointwise_204_certificate"].__setitem__("sha256", "2" * 64))
    changed("universe_count", lambda x: x["one_active_handoff"].__setitem__("wrong_split_directions", 203))
    changed("universe_hash", lambda x: x["one_active_handoff"].__setitem__("direction_universe_sha256", "3" * 64))
    changed("source_rank", lambda x: x["rank_transfer"].__setitem__("source_bridge_rank_bound", 5))
    changed("target_rank", lambda x: x["rank_transfer"].__setitem__("target_local_rank_lower_bound", 4))
    changed("pointwise_flag", lambda x: x["rank_transfer"].__setitem__("target_pointwise_not_generic", False))
    changed("target_openness_rank", lambda x: x["rank_transfer"].__setitem__("target_openness_needed", True))
    changed("two_terminal_mixture", lambda x: x["strict_physical_marginal"].__setitem__("two_terminal_blob_mixture_statement", "omitted"))
    changed("trivial_split", lambda x: x.__setitem__("trivial_split_handling", "omitted"))
    changed("four_intersections", lambda x: x["two_active_exclusion"]["four_nonempty_intersections"].pop())
    changed("directional_step", lambda x: x["two_active_exclusion"].__setitem__("directional_step", "reverse"))
    for step_id in ("D1", "T2", "T4", "M1", "S1", "P1", "P2", "X", "C"):
        changed(
            f"dependency_{step_id}",
            lambda x, step_id=step_id: next(row for row in x["proof_steps"] if row["id"] == step_id)["depends_on"].pop(),
        )
    changed("duplicate_step", lambda x: x["proof_steps"].__setitem__(1, copy.deepcopy(x["proof_steps"][0])))
    changed("local_pass", lambda x: x.__setitem__("local_204_dependency_pass", False))
    changed("cut_evidence_pass", lambda x: x.__setitem__("k3p_directed_cut_inclusion_evidence_pass", False))
    return cases


def reseal_evidence(value):
    value["payload_sha256"] = payload_digest(value)
    return value


def evidence_mutation_cases(evidence):
    cases = []

    def changed(name, mutate):
        value = copy.deepcopy(evidence)
        mutate(value)
        cases.append((name, reseal_evidence(value)))

    legacy_report = PROJECT / "cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json"
    jc_manuscript = PROJECT / "input_frozen/referenced_chat_manuscripts/jc_level2_source.tex"
    changed(
        "coherently_resealed_legacy_premise_substitution",
        lambda x: x["load_bearing_inputs"].__setitem__(
            "displayed_tree_lemma", expected_binding(legacy_report)
        ),
    )
    changed(
        "coherently_resealed_jc_provenance_substitution",
        lambda x: x["load_bearing_inputs"].__setitem__(
            "displayed_tree_lemma", expected_binding(jc_manuscript)
        ),
    )
    changed(
        "coherently_resealed_exact_minor_removal",
        lambda x: x.__setitem__("displayed_tree_minor", None),
    )
    changed(
        "coherently_resealed_implication_edge_removal",
        lambda x: next(
            row for row in x["analytic_implication"]
            if row["id"] == "source_noncut_nonzero"
        ).__setitem__("depends_on", []),
    )
    for step_id in (row["id"] for row in EXPECTED_ANALYTIC_IMPLICATION):
        changed(
            f"coherently_resealed_claim_body_{step_id}",
            lambda x, step_id=step_id: next(
                row for row in x["analytic_implication"]
                if row["id"] == step_id
            )["claim"].__setitem__("type", "semantically_false_placeholder"),
        )
    return cases


def run_mutations(payload, universe, cut_evidence, cut_evidence_path=CUT_EVIDENCE):
    results = []
    for name, changed in mutation_cases(payload):
        rejected = False
        try:
            verify_payload(changed, universe, cut_evidence, cut_evidence_path)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected = True
        require(rejected, ("mutation accepted", name))
        results.append({"name": name, "result": "REJECTED"})
    for name, changed in evidence_mutation_cases(cut_evidence):
        rejected = False
        try:
            verify_cut_inclusion_evidence(changed)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected = True
        require(rejected, ("evidence mutation accepted", name))
        results.append({"name": name, "result": "REJECTED"})
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--universe", type=Path, default=DEFAULT_UNIVERSE)
    parser.add_argument("--cut-evidence", type=Path, default=CUT_EVIDENCE)
    parser.add_argument("--mutations", action="store_true")
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument("--no-write-report", action="store_true")
    args = parser.parse_args()
    payload = json.loads(args.artifact.read_text())
    universe = json.loads(args.universe.read_text())
    cut_evidence = json.loads(args.cut_evidence.read_text())
    result = verify_payload(payload, universe, cut_evidence, args.cut_evidence)
    mutations = run_mutations(
        payload, universe, cut_evidence, args.cut_evidence
    ) if args.mutations else []
    report = {
        "schema": "k3p-lost-bridge-global-transfer-verification-v2",
        **result,
        "artifact_sha256": sha_file(args.artifact),
        "universe_sha256": sha_file(args.universe),
        "cut_evidence_sha256": sha_file(args.cut_evidence),
        "verifier_sha256": sha_file(Path(__file__).resolve()),
        "producer_imported": False,
        "python_optimized": not __debug__,
        "mutation_count": len(mutations),
        "mutations": mutations,
    }
    if not args.no_write_report:
        temporary = args.report.with_suffix(args.report.suffix + ".tmp")
        temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        temporary.replace(args.report)
    print(
        json.dumps(
            {
                key: report[key]
                for key in ("status", "direction_count", "proof_step_count", "mutation_count")
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
