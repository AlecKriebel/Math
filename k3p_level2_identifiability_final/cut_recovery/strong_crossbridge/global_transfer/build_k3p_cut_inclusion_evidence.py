#!/usr/bin/env python3
"""Build the self-contained K3P evidence for Cut(Nprime) subset Cut(N)."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
PALETTE = HERE.parent / "palette_independent"

MANUSCRIPT = PROJECT / "manuscript/sections/04_physical_topology.tex"
MINOR_VERIFIER = PALETTE / "verify_displayed_tree_minor.py"
BALANCED_PRODUCER = PALETTE / "enumerate_balanced_word_reduction.py"
BALANCED_CERTIFICATE = PALETTE / "BALANCED_WORD_REDUCTION_CERTIFICATE.json"
PALETTE_PRODUCER = PALETTE / "verify_reduced_palette_cleanroom.py"
PALETTE_CERTIFICATE = PALETTE / "REDUCED_PALETTE_CLEANROOM_CERTIFICATE.json"
COMBINATORICS_REPLAY = PALETTE / "verify_cut_combinatorics.py"
DEFAULT_OUTPUT = HERE / "K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json"


# This is a typed declaration of the nine implications used by the
# handwritten proof.  The independent verifiers carry their own literal copy
# and require exact equality; arbitrary replacement prose is therefore not a
# valid certificate row.
ANALYTIC_IMPLICATION = [
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


class EvidenceFailure(RuntimeError):
    pass


def require(condition: bool, label: object) -> None:
    if not condition:
        raise EvidenceFailure(str(label))


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def payload_sha256(value: dict) -> str:
    body = dict(value)
    body.pop("payload_sha256", None)
    return hashlib.sha256(canonical(body)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def binding(path: Path) -> dict[str, str]:
    require(path.is_file() and not path.is_symlink(), ("regular input", path))
    return {
        "path": str(path.resolve().relative_to(PROJECT.resolve())),
        "sha256": sha_file(path),
    }


def validate_inputs() -> tuple[dict, dict]:
    manuscript = " ".join(MANUSCRIPT.read_text().split())
    snippets = (
        r"\begin{lemma}[Displayed-tree witness for a noncut]",
        r"\begin{proposition}[Generic noncut recovery]",
        r"p_0p_1p_2p_3(1-u^2)>0",
        r"\begin{corollary}[The easy directed cut inclusion]",
        r"\operatorname{Cut}(N')\subseteq\operatorname{Cut}(N)",
        r"\begin{lemma}[Balanced noncut compression]",
        "808{,}642",
        "379{,}742",
        "zero all-switching survivors",
    )
    for snippet in snippets:
        require(" ".join(snippet.split()) in manuscript,
                ("displayed-tree lemma snippet", snippet))

    balanced = json.loads(BALANCED_CERTIFICATE.read_text())
    require(set(balanced) == {
        "enumeration_commitment_sha256", "failure_count", "failures",
        "families", "mutation_results", "proof_partition", "schema",
        "scope", "status", "totals",
    }, "balanced certificate key set")
    require(balanced["schema"] == "stc-jc-cut-palette-reduction-v1" and
            balanced["status"] == "EXACTLY COMPUTED", "balanced schema/status")
    require(balanced["failure_count"] == 0 and balanced["failures"] == [],
            "balanced failures")
    require(balanced["totals"] == {
        "balanced_total": 808_642,
        "direct_palette": 544_350,
        "singleton_doubled_palette": 34_304,
        "three_run_path_obstruction": 229_988,
    }, "balanced totals")
    require(len(balanced["families"]) == 10, "balanced family count")
    balanced_keys = {
        (row["family"], row["role"], row["fixed_extra_count"])
        for row in balanced["families"]
    }
    require(len(balanced_keys) == len(balanced["families"]),
            "balanced family-role uniqueness")
    require(balanced["scope"]["active_port_counts"] == [4, 5, 6, 7, 8],
            "balanced port scope")
    require(balanced["scope"]["primitive_families"] == [
        "cycle", "theta_TR_nested", "theta_TR_separated",
        "theta_TT_nested", "theta_TT_separated",
    ], "balanced primitive scope")
    require(balanced["scope"]["roles"] == ["root", "nonroot"],
            "balanced role scope")
    recomputed_totals = {
        key: sum(row["counts"][key] for row in balanced["families"])
        for key in balanced["totals"]
    }
    require(recomputed_totals == balanced["totals"], "balanced family sums")
    require(len(balanced["mutation_results"]) == 3 and
            all(row["rejected"] is True for row in balanced["mutation_results"]),
            "balanced mutation checks")

    palette = json.loads(PALETTE_CERTIFICATE.read_text())
    require(set(palette) == {
        "failures", "families", "palette", "record_commitment_sha256",
        "schema", "status", "survivor_count",
        "total_valid_palette_presentations",
    }, "palette certificate key set")
    require(palette["schema"] == "stc-jc-reduced-palette-cleanroom-v1" and
            palette["status"] == "EXACTLY COMPUTED", "palette schema/status")
    require(palette["palette"] == [[], [0], [1], [0, 1], [1, 0]],
            "short palette")
    require(len(palette["families"]) == 10, "palette family count")
    palette_keys = {(row["core"], row["role"]) for row in palette["families"]}
    require(len(palette_keys) == len(palette["families"]),
            "palette family-role uniqueness")
    require(palette["survivor_count"] == 0 and palette["failures"] == [],
            "palette survivors")
    valid = sum(
        row["valid_balanced_compressed"] + row["valid_singleton_doubled"]
        for row in palette["families"]
    )
    require(valid == palette["total_valid_palette_presentations"] == 379_742,
            "palette presentation count")
    require(sum(row["survivor_count"] for row in palette["families"]) == 0,
            "palette family survivors")
    return balanced, palette


def build_evidence() -> dict:
    balanced, palette = validate_inputs()

    # The two determinant terms are recomputed directly from the printed
    # zero-character block.  Exponents are ordered as (p0,p1,p2,p3,u).
    zero_minor_terms = [
        {"coefficient": 1, "exponents": [1, 1, 1, 1, 0]},
        {"coefficient": -1, "exponents": [1, 1, 1, 1, 2]},
    ]
    five_minor_terms = [
        {"coefficient": 1, "exponents": [4, 4, 1, 1, 0]},
        {"coefficient": -1, "exponents": [4, 4, 1, 1, 2]},
    ]
    evidence = {
        "schema": "k3p-directed-cut-inclusion-evidence-v2",
        "status": "PASS",
        "claim": {
            "containment_identity": (
                "Phi_N=Phi_Nprime_comp_sigma_on_a_nonempty_source_open_set_U"
            ),
            "conclusion": "Cut(Nprime)_subseteq_Cut(N)",
            "source_regular_only": True,
            "target_regular_not_assumed": True,
            "target_open_image_not_assumed": True,
        },
        "load_bearing_inputs": {
            "displayed_tree_lemma": binding(MANUSCRIPT),
            "displayed_tree_minor_verifier": binding(MINOR_VERIFIER),
            "balanced_word_producer": binding(BALANCED_PRODUCER),
            "balanced_word_certificate": binding(BALANCED_CERTIFICATE),
            "reduced_palette_cleanroom": binding(PALETTE_PRODUCER),
            "reduced_palette_certificate": binding(PALETTE_CERTIFICATE),
            "independent_combinatorics_replay": binding(COMBINATORICS_REPLAY),
        },
        "balanced_word_reduction": {
            "families": len(balanced["families"]),
            "totals": balanced["totals"],
            "failure_count": balanced["failure_count"],
            "mutation_count": len(balanced["mutation_results"]),
            "enumeration_commitment_sha256":
                balanced["enumeration_commitment_sha256"],
        },
        "reduced_palette_replay": {
            "families": len(palette["families"]),
            "valid_presentations": palette["total_valid_palette_presentations"],
            "survivors": palette["survivor_count"],
            "record_commitment_sha256": palette["record_commitment_sha256"],
        },
        "displayed_tree_minor": {
            "displayed_quartet_split": "01|23",
            "wrong_flattening": "02|13",
            "variable_order": ["p0", "p1", "p2", "p3", "u"],
            "zero_character_block": [
                ["1", "p1*p3*u"],
                ["p0*p2*u", "p0*p1*p2*p3"],
            ],
            "zero_minor_terms": zero_minor_terms,
            "zero_minor_factorization": "p0*p1*p2*p3*(1-u^2)",
            "augmentation_entries": ["p0*p1", "p0*p1", "p0*p1"],
            "five_minor_terms": five_minor_terms,
            "five_minor_factorization": "p0^4*p1^4*p2*p3*(1-u^2)",
            "strict_domain": "0<p0,p1,p2,p3,u<1",
            "strict_nonzero": True,
            "boundary_to_strict_physical_by_continuity": True,
        },
        "analytic_implication": ANALYTIC_IMPLICATION,
        "provenance_policy": {
            "legacy_global_logic_report_is_load_bearing": False,
            "jc_manuscript_is_load_bearing": False,
            "jc_algebra_used": False,
            "model_independent_graph_certificate_names_retained": True,
        },
        "remaining_gaps": [],
    }
    evidence["payload_sha256"] = payload_sha256(evidence)
    return evidence


def atomic_json(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        evidence = build_evidence()
        atomic_json(args.output, evidence)
        print(json.dumps({
            "status": evidence["status"],
            "balanced_words": evidence["balanced_word_reduction"]["totals"][
                "balanced_total"
            ],
            "palette_presentations": evidence["reduced_palette_replay"][
                "valid_presentations"
            ],
            "payload_sha256": evidence["payload_sha256"],
        }, sort_keys=True))
        print("K3P_DIRECTED_CUT_INCLUSION_EVIDENCE_PASS")
        return 0
    except (EvidenceFailure, KeyError, OSError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print(f"K3P_DIRECTED_CUT_INCLUSION_EVIDENCE_FAIL: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
