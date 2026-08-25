#!/usr/bin/env python3
"""Build the noncircular lost-bridge-to-one-active transfer certificate."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
FROZEN_TOPOLOGY = PROJECT / "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json"
MARGINAL = PROJECT / "marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json"
DIRECTED_LOGIC = PROJECT / "cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json"
LOCAL_FINAL = HERE.parent / "final_certificate/STRONG_CROSSBRIDGE_FINAL_CERTIFICATE.json"
LOCAL_UNIVERSE = HERE.parent / "final_certificate/UNIVERSE_CERTIFICATE.json"
LOCAL_VERIFICATION = HERE.parent / "final_certificate/VERIFICATION_REPORT.json"
LOCAL_MUTATIONS = HERE.parent / "final_certificate/ADVERSARIAL_MUTATION_REPORT.json"
UNIVERSE_OUTPUT = HERE / "GLOBAL_TRANSFER_DIRECTION_UNIVERSE.json"
OUTPUT = HERE / "GLOBAL_TRANSFER_CERTIFICATE.json"


def require(condition, label):
    if not condition:
        raise AssertionError(label)


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


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(PROJECT))


def binding(path: Path):
    return {"path": relative(path), "sha256": sha_file(path)}


def permute_mask(mask: int, old_order: tuple[int, ...]) -> int:
    old_to_new = {old: new for new, old in enumerate(old_order)}
    answer = 0
    for old, new in old_to_new.items():
        if mask & (1 << old):
            answer |= 1 << new
    return answer


def split_displayed_by_all(signatures, reticulation_count, first):
    side_mask = sum(1 << label for label in first)
    complement_mask = 15 ^ side_mask
    return all(
        any(row[switch] in (side_mask, complement_mask) for row in signatures)
        for switch in range(1 << reticulation_count)
    )


def build_direction_universe(topology):
    section = topology["one_active_wrong_split"]
    rows = []
    raw_splits = 0
    displayed = 0
    recomputation_failures = []
    direction_keys = set()
    record_reticulations = collections.Counter()
    for record in section["records"]:
        record_id = int(record["id"])
        reticulation_count = int(record["reticulation_count"])
        signatures = tuple(tuple(int(mask) for mask in row) for row in record["signatures"])
        require(all(len(row) == 1 << reticulation_count for row in signatures), "switching width")
        record_reticulations[reticulation_count] += 1
        for split in record["splits"]:
            raw_splits += 1
            first = tuple(int(label) for label in split["split"])
            require(len(first) == 2 and len(set(first)) == 2, "split side")
            independently_displayed = split_displayed_by_all(
                signatures, reticulation_count, first
            )
            if independently_displayed != split["displayed_by_all"]:
                recomputation_failures.append([record_id, list(first)])
            if independently_displayed:
                displayed += 1
                continue
            complement = tuple(sorted(set(range(4)) - set(first)))
            old_order = first + complement
            require(tuple(sorted(old_order)) == (0, 1, 2, 3), "normalizing permutation")
            unordered_split = tuple(
                sorted((tuple(sorted(first)), tuple(sorted(complement))))
            )
            direction_key = (record_id, unordered_split)
            require(direction_key not in direction_keys, "duplicate direction")
            direction_keys.add(direction_key)
            normalized_signatures = tuple(
                tuple(permute_mask(mask, old_order) for mask in row)
                for row in signatures
            )
            rows.append(
                {
                    "target_index": len(rows),
                    "record_id": record_id,
                    "reticulation_count": reticulation_count,
                    "old_split": list(first),
                    "old_order": list(old_order),
                    "normalized_split": [[0, 1], [2, 3]],
                    "normalized_signatures_sha256": digest(normalized_signatures),
                    "direction_key": [
                        record_id,
                        [list(unordered_split[0]), list(unordered_split[1])],
                    ],
                }
            )
    require(not recomputation_failures, "displayed flags")
    require(len(section["records"]) == 72, "primitive record count")
    require(raw_splits == 216 and displayed == 12 and len(rows) == 204, "universe census")
    require(len(direction_keys) == 204, "direction uniqueness")
    require(section["common_displayed_splits_skipped"] == 12, "frozen displayed count")
    require(section["strict_wrong_split_certificates"] == 204, "frozen direction count")
    require(section["status"] == "EXACTLY COMPUTED" and section["failures"] == [], "one-active topology status")
    return {
        "schema": "k3p-global-transfer-direction-universe-v1",
        "status": "PASS",
        "input": binding(FROZEN_TOPOLOGY),
        "topology_only_fields_used": [
            "primitive_cores",
            "primitive_orientation_derivation",
            "switching_compression",
            "one_active_wrong_split.records[*].id",
            "one_active_wrong_split.records[*].reticulation_count",
            "one_active_wrong_split.records[*].signatures",
            "one_active_wrong_split.records[*].splits[*].split",
            "one_active_wrong_split.records[*].splits[*].displayed_by_all",
        ],
        "algebraic_JC_minor_fields_used": False,
        "counts": {
            "primitive_core_templates": len(topology["primitive_cores"]),
            "one_active_records": len(section["records"]),
            "raw_labelled_split_entries": raw_splits,
            "displayed_by_all_removed": displayed,
            "wrong_split_directions": len(rows),
            "unique_direction_keys": len(direction_keys),
            "record_reticulation_distribution": dict(sorted(record_reticulations.items())),
        },
        "independent_displayed_flag_recomputation_failures": recomputation_failures,
        "directions_sha256": digest(rows),
        "directions": rows,
    }


def atomic_json(path: Path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def proof_steps():
    return [
        {
            "id": "H0",
            "depends_on": [],
            "claim": "Phi_N=Phi_Nprime∘sigma on a nonempty source-open regular set U; N,Nprime are binary standard semi-directed strongly tree-child level-2 networks on the same labels.",
        },
        {
            "id": "D1",
            "depends_on": ["H0"],
            "claim": "Every target bridge split is a source bridge split: Cut(Nprime) subset Cut(N).",
            "reason": "A target-cut 5x5 flattening minor vanishes after composition with sigma on U. If the split were a source noncut, isotropic-JC generic recovery gives a nonzero source polynomial, which cannot vanish on U.",
        },
        {
            "id": "L0",
            "depends_on": ["H0"],
            "claim": "Assume for contradiction that S=A|B is a bridge split of N and is not a bridge split of Nprime.",
        },
        {
            "id": "L1",
            "depends_on": ["L0"],
            "claim": "Both A and B contain at least two labels.",
            "reason": "A singleton side is the pendant leaf bridge in every standard network, so it cannot be lost.",
        },
        {
            "id": "T1",
            "depends_on": ["L0", "L1"],
            "claim": "Color the target reduced bridge tree by A/B. The crossing-quartet tree dichotomy gives either a target bridge R with both colors on both sides, or a unique central component v with at least two monochromatic incident branches of each color.",
        },
        {
            "id": "T2",
            "depends_on": ["D1", "L0", "T1"],
            "claim": "The target-bridge/two-active alternative is impossible.",
            "reason": "Its split R has all four intersections with S nonempty, so R crosses S. D1 makes R a source bridge split, while bridge splits of one reduced tree are compatible; this contradicts that S is a source bridge split.",
        },
        {
            "id": "T3",
            "depends_on": ["T1", "T2"],
            "claim": "The target witness is one central active component v; every selected-leaf-free serial path or two-boundary side blob on its four arms compresses to an effective K3P edge.",
        },
        {
            "id": "T4",
            "depends_on": ["T3"],
            "claim": "Strong-tree-child primitive-core support and noncut word compression select two actual A labels and two actual B labels whose one-active restriction is a wrong-split direction in the complete 204-direction universe.",
            "reason": "Minimum repair and path-sink roles are retained as zero-character completion ports. Switching compression has zero survivors; hence some switching fails the color split and a four-leaf tree witness exists.",
        },
        {
            "id": "M1",
            "depends_on": ["H0", "T4"],
            "claim": "Marginalizing the containment identity to the four selected labels gives identical source and target quartet tensors pointwise on U.",
            "reason": "Fourier marginalization sets omitted characters to zero; it is a direct linear marginal of the original identity and needs no target-open parameter image.",
        },
        {
            "id": "S1",
            "depends_on": ["H0", "T4"],
            "claim": "The compressed target quartet is evaluated at a strict physical D3,+ point.",
            "reason": "Nonempty serial edge classes compose by strictly positive Z2xZ2 convolution; a two-boundary side blob is a positive convex mixture of its strict displayed-path K3P matrices; inheritances are retained, complemented, or summed out.",
        },
        {
            "id": "P1",
            "depends_on": ["M1", "L0"],
            "claim": "The source quartet flattening on the selected 2|2 split has rank at most four at every point of U.",
            "reason": "The source bridge S survives the two-label-per-side restriction and the four K3P character blocks factor as rank-one outer products.",
        },
        {
            "id": "P2",
            "depends_on": ["T4", "S1"],
            "claim": "The target quartet flattening on that split has rank greater than four at every strict physical target point.",
            "reason": "All 204 normalized one-active wrong-split directions have pointwise exact certificates. Effective edge products remain strict D3+; inherited probabilities are retained, complemented, or disappear.",
        },
        {
            "id": "X",
            "depends_on": ["M1", "P1", "P2"],
            "claim": "Contradiction: the same quartet tensor cannot have flattening rank both at most four and greater than four.",
        },
        {
            "id": "C",
            "depends_on": ["D1", "X"],
            "claim": "Cut(N)=Cut(Nprime) under source-relative regular full-dimensional containment in the stated strong class.",
        },
    ]


def main():
    topology = json.loads(FROZEN_TOPOLOGY.read_text())
    marginal = json.loads(MARGINAL.read_text())
    directed = json.loads(DIRECTED_LOGIC.read_text())
    universe = build_direction_universe(topology)
    atomic_json(UNIVERSE_OUTPUT, universe)

    require(topology["status"] == "EXACTLY COMPUTED", "topology status")
    require(len(topology["primitive_cores"]) == 5, "primitive cores")
    require(topology["primitive_orientation_derivation"]["template_match"] is True, "core template match")
    require(topology["switching_compression"]["status"] == "EXACTLY COMPUTED", "compression status")
    require(topology["switching_compression"]["survivor_count"] == 0, "compression survivors")
    require(topology["switching_compression"]["failures"] == [], "compression failures")
    require(marginal["status"] == "PASS", "marginal status")
    require(marginal["k2p_algebra_used"] is False, "marginal K2P use")
    source_relative = marginal["source_relative_open_image"]
    require(source_relative["direct_marginal_of_original_containment"] is True, "direct marginal")
    require(source_relative["target_marginal_openness_used"] is False, "target openness")
    require(directed["generic_cut_consequences"]["proved_inclusion"] == "Cut(N_prime)_subseteq_Cut(N)", "directional inclusion")
    require(directed["directed_relation"]["target_regular_not_assumed"] is True, "target regularity")

    local_final = json.loads(LOCAL_FINAL.read_text()) if LOCAL_FINAL.is_file() else None
    local_universe = json.loads(LOCAL_UNIVERSE.read_text()) if LOCAL_UNIVERSE.is_file() else None
    local_verification = json.loads(LOCAL_VERIFICATION.read_text()) if LOCAL_VERIFICATION.is_file() else None
    local_mutations = json.loads(LOCAL_MUTATIONS.read_text()) if LOCAL_MUTATIONS.is_file() else None
    local_pass = bool(
        local_final
        and local_universe
        and local_verification
        and local_mutations
        and local_final.get("schema") == "k3p-strong-crossbridge-final-certificate-v1"
        and local_final.get("status") == "PASS"
        and local_final.get("coverage", {}).get("target_directions") == 204
        and local_final.get("coverage", {}).get("union_is_all_204") is True
        and local_universe.get("status") == "PASS"
        and len(local_universe.get("directions", [])) == 204
        and local_verification.get("schema") == "k3p-strong-crossbridge-final-verification-v1"
        and local_verification.get("status") == "PASS"
        and local_verification.get("artifacts", {}).get("final_certificate_sha256") == sha_file(LOCAL_FINAL)
        and local_verification.get("artifacts", {}).get("universe_certificate_sha256") == sha_file(LOCAL_UNIVERSE)
        and local_mutations.get("schema") == "k3p-strong-crossbridge-final-adversarial-mutations-v1"
        and local_mutations.get("status") == "PASS"
        and local_mutations.get("all_mutations_rejected") is True
        and local_mutations.get("rejected_count") == local_mutations.get("mutation_count") == 34
        and [row["normalized_signatures_sha256"] for row in local_universe["directions"]]
        == [row["normalized_signatures_sha256"] for row in universe["directions"]]
    )

    load_bearing = {
        "frozen_strong_topology": binding(FROZEN_TOPOLOGY),
        "selected_marginal": binding(MARGINAL),
        "directed_cut_inclusion_audit": binding(DIRECTED_LOGIC),
        "recompiled_direction_universe": binding(UNIVERSE_OUTPUT),
        "pointwise_204_certificate": binding(LOCAL_FINAL) if LOCAL_FINAL.is_file() else None,
        "pointwise_204_universe": binding(LOCAL_UNIVERSE) if LOCAL_UNIVERSE.is_file() else None,
        "pointwise_204_independent_verification": binding(LOCAL_VERIFICATION) if LOCAL_VERIFICATION.is_file() else None,
        "pointwise_204_adversarial_mutations": binding(LOCAL_MUTATIONS) if LOCAL_MUTATIONS.is_file() else None,
    }
    steps = proof_steps()
    payload = {
        "schema": "k3p-lost-bridge-global-transfer-certificate-v1",
        "status": "PASS" if local_pass else "BLOCKED",
        "scope": {
            "network_class": "binary standard semi-directed strongly tree-child level-2",
            "relation": "source-relative regular full-dimensional analytic containment N preceq Nprime",
            "domain": "strict principal K3P domain D3,+ with inheritance probabilities in (0,1)",
            "conclusion": "Cut(N)=Cut(Nprime)",
        },
        "load_bearing_inputs": load_bearing,
        "noncircularity": {
            "common_bridge_tree_assumed": False,
            "bridge_tree_equality_assumed": False,
            "fourteen_orbit_classification_imported": False,
            "target_regular_point_assumed": False,
            "target_open_marginal_assumed": False,
            "only_preexisting_cut_direction_used": "Cut(Nprime) subset Cut(N)",
            "reverse_direction_proved_here": "Cut(N) subset Cut(Nprime)",
        },
        "trivial_split_handling": (
            "A singleton side is the pendant leaf bridge in every standard network; "
            "therefore a source split absent from the target is automatically nontrivial "
            "with at least two labels on each side."
        ),
        "two_active_exclusion": {
            "target_bridge_split": "R=C|D",
            "four_nonempty_intersections": ["A∩C", "A∩D", "B∩C", "B∩D"],
            "incompatibility_criterion": "two splits are compatible iff at least one of the four intersections is empty",
            "directional_step": "R in Cut(Nprime) implies R in Cut(N)",
            "contradiction": "S and R would be incompatible bridge splits of the same source reduced bridge tree",
        },
        "one_active_handoff": {
            "primitive_core_count": len(topology["primitive_cores"]),
            "primitive_cores": [row["name"] for row in topology["primitive_cores"]],
            "switching_compression_survivors": topology["switching_compression"]["survivor_count"],
            "one_active_records": universe["counts"]["one_active_records"],
            "raw_split_entries": universe["counts"]["raw_labelled_split_entries"],
            "displayed_by_all_removed": universe["counts"]["displayed_by_all_removed"],
            "wrong_split_directions": universe["counts"]["wrong_split_directions"],
            "direction_universe_sha256": sha_file(UNIVERSE_OUTPUT),
        },
        "strict_physical_marginal": {
            "serial_convolution_statement": (
                "A serial product of strict D3,+ K3P matrices is strict D3,+: in "
                "probability coordinates it is convolution of two strictly positive "
                "Z2xZ2 distributions, and its spectra are coordinatewise products in (0,1)."
            ),
            "two_terminal_blob_mixture_statement": (
                "A selected-leaf-free two-boundary side blob is a convex mixture, "
                "with positive switching weights summing to one, of strict K3P path "
                "matrices. Convex mixture preserves strict positivity of all inverse-"
                "Fourier probabilities and keeps each nontrivial spectrum in (0,1)."
            ),
            "two_terminal_blob_mixture_identities": {
                "switching_weights": "w_s>0 and sum_s w_s=1",
                "probability_coordinate": "p_eff(h)=sum_s w_s*p_s(h)>0",
                "spectrum_lower_margin": "x_eff=sum_s w_s*x_s>0",
                "spectrum_upper_margin": "1-x_eff=sum_s w_s*(1-x_s)>0",
                "spectrum_scope": "x in {c,g,t}",
            },
            "inheritance_statement": "Each inheritance is retained as lambda, complemented to 1-lambda, or summed out; retained values remain in (0,1).",
            "Fourier_marginal_statement": "Omitted leaf characters are set to zero, so the quartet flattening is the corresponding Fourier submatrix.",
        },
        "rank_transfer": {
            "source_bridge_rank_bound": 4,
            "target_local_rank_lower_bound": 5,
            "target_pointwise_not_generic": True,
            "target_openness_needed": False,
            "identity": "Marginal_4(Phi_N(theta))=Marginal_4(Phi_Nprime(sigma(theta))) for every theta in U",
        },
        "proof_steps": steps,
        "proof_step_ids_sha256": digest([row["id"] for row in steps]),
        "local_204_dependency_pass": local_pass,
        "blocked_reason": None if local_pass else "The aggregate pointwise 204-direction certificate is missing, blocked, or does not match the independently rebuilt universe.",
    }
    atomic_json(OUTPUT, payload)
    print(
        json.dumps(
            {
                "status": payload["status"],
                "directions": universe["counts"]["wrong_split_directions"],
                "two_active_excluded": True,
                "local_204_dependency_pass": local_pass,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
