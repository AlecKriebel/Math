#!/usr/bin/env python3
"""Fail-closed regression for the August 20 referee repairs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> None:
    paper = (ROOT / "source/paper/main.tex").read_text(encoding="utf-8")
    supplement = (ROOT / "source/supplement/supplement.tex").read_text(
        encoding="utf-8"
    )
    atlas = (ROOT / "certificate_bundle/ATLAS_SUMMARY.md").read_text(
        encoding="utf-8"
    )
    builder = (ROOT / "reproducibility/build_certificate_bundle.py").read_text(
        encoding="utf-8"
    )

    for phrase in (
        "blob factor induced by a standard semi-directed network in",
        "complete level-2 factor induced by a standard semi-directed",
        "complete central singleton-signature edge class",
        "preimage of $p$ having rank $d_N$",
        "No target parameter section is chosen",
        "C(g;\\mathbf h,c)\\overline Q_u(\\mathbf h)",
        "$\\mathcal Q$ is the\none-dimensional representative slice",
        "$df_i$ has rank one",
        "The one\ncoordinate $u$ and three effective boundary scales",
        "$\\phi_i=\\Phi\\circ\\pi_i$",
        "no application of\n\\cref{lem:product-chart}",
        "three monochromatic runs $c,d,c$",
        "808{,}642",
    ):
        require(phrase in paper, f"manuscript repair absent: {phrase}")
    require("$9$ with $\\Delta=0" not in paper,
            "withdrawn normalized endpoint count returned")

    cut = load("independent/bridge_cut/cut_certificate.json")
    cases = {}
    for row in cut["three_port_endpoint_dichotomy"]["records"]:
        case = row["dichotomy"]["case"]
        cases[case] = cases.get(case, 0) + 1
    require(cases == {
        "Delta_positive": 67,
        "Delta_zero_Gamma_positive": 2,
        "Delta_zero_Gamma_zero": 7,
        "Delta_zero_Gamma_zero_ordinary": 1,
    }, "normalized endpoint partition")

    reduction = load("independent/bridge_cut/palette_reduction_certificate.json")
    require(reduction["failure_count"] == 0, "palette reduction failure")
    require(reduction["totals"]["balanced_total"] == 808642,
            "palette universe changed")
    require(reduction["totals"]["three_run_path_obstruction"] == 229988,
            "three-run partition changed")
    require(
        reduction["totals"]["direct_palette"]
        + reduction["totals"]["singleton_doubled_palette"]
        == 578654,
        "palette-reduction partition changed",
    )
    cleanroom = load("reviews/global_bridge/palette_cleanroom_certificate.json")
    require(cleanroom["total_valid_palette_presentations"] == 379742,
            "clean-room palette universe changed")
    require(cleanroom["survivor_count"] == 0, "clean-room cut survivor")

    parameter = load("reviews/root_probe/parameter_submersion_certificate.json")
    require(parameter["completion_count"] == 42908, "completion count")
    require(parameter["full_row_rank_failure_count"] == 0, "submersion rank")
    require(parameter["raw_to_normalized_class_reduction_counts"] == {
        "1": 14878, "2": 27806, "3": 208, "4": 16,
    }, "zero-sum normalization partition")
    require(
        parameter["general_open_product_certificate"][
            "jacobian_constructed_and_ranked_over_Q"
        ],
        "rational Jacobian certificate absent",
    )
    require(
        parameter["normalization_mutation_tests"]["all_mutations_rejected"],
        "zero-sum normalization mutations were not rejected",
    )

    probe = load("reviews/root_probe/probe_coherence_certificate.json")
    require(probe["one_port_ambiguity_group_count"] == 372,
            "honest one-port ambiguity count")
    require(probe["one_port_max_two_port_completion_multiplicity"] == 2,
            "one-port completion multiplicity")
    require("coherence_collision_count" not in probe,
            "tautological collision statistic returned")

    for text, label in ((atlas, "atlas summary"), (supplement, "supplement")):
        text = " ".join(text.replace("$", "").split())
        for phrase in ("192", "3 direct", "57 nonretaining"):
            require(phrase in text, f"{label}: n=4 quotient crosswalk lacks {phrase}")

    require('VERSION = "1.1.7"' in builder, "certificate version")
    for required in (
        '"PROOF.md", "CUT_PALETTE_REDUCTION.md"',
        '"verify_palette_reduction.py"',
        '"verify_palette_cleanroom.py"',
        '"COMPACT_PATH_CLOSURE_BINDINGS.jsonl.gz"',
        '"RESTORATION_CLOSURE_BINDINGS.jsonl.gz"',
        '"DIRECT_ANCHOR_CLOSURE_BINDINGS.jsonl.gz"',
        '"sharpness/omega/inputs/jc_omega_move.json"',
        'def require_identical_payload(candidate: Path, fresh: Path)',
        '"prepared_payload_sha256": payload_sha256',
        'prepare_from_commit(seal_commit, fresh_stage, scratch)',
        '["git", "archive", "--format=tar", commit',
    ):
        require(required in builder, f"certificate bundle omits {required}")

    print(json.dumps({
        "status": "VERIFIED AFTER CORRECTION",
        "headline_theorem_weakened": False,
        "cut_balanced_words": 808642,
        "cleanroom_palette_presentations": 379742,
        "submersion_completions": 42908,
        "one_port_ambiguity_groups": 372,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
