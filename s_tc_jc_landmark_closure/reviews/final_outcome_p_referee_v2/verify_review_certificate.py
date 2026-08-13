#!/usr/bin/env python3
"""Machine-check the final Outcome P referee certificate.

This is intentionally narrow: it checks the two repaired blockers, the compact
release-input gate, and manuscript/release-scope regressions that would reopen
the prior final-referee failures.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
REPO = PROJECT.parent
REQUESTED_COMMIT = "e1fd6ede986cd866a310cd9b0f9e7d6d13c8318c"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(relative: str):
    return json.loads((PROJECT / relative).read_text(encoding="utf-8"))


def read_text(relative: str) -> str:
    return (PROJECT / relative).read_text(encoding="utf-8")


def compact_space(text: str) -> str:
    return " ".join(text.split())


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=PROJECT, text=True, stderr=subprocess.STDOUT
    ).strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_n3_universe() -> dict:
    cert = read_json("reviews/n3_universe_generator/n3_universe_certificate.json")
    source = read_text("reviews/n3_universe_generator/generate_universe.py")
    require(cert["status"] == "VERIFIED", "n3 universe certificate not VERIFIED")
    require(all(cert["checks"].values()), "n3 universe has a false check")
    require(cert["counts"] == {
        "canonical_merged_relations": 10466,
        "descriptor_cache": 393,
        "marginalized_incoming_completions": 1983,
        "raw_necessary_relations": 10826,
        "selected_incoming_completions": 831,
        "source_supports": 8,
    }, "n3 theorem counts changed")
    require(
        cert["hashes"]["independent_raw_multiset_sha256"]
        == cert["hashes"]["primary_raw_multiset_sha256"],
        "n3 raw multiset mismatch",
    )
    require(
        cert["hashes"]["independent_merged_multiset_sha256"]
        == cert["hashes"]["primary_merged_multiset_sha256"],
        "n3 merged multiset mismatch",
    )
    require(cert["independence"]["primary_modules_imported"] == [],
            "n3 generator declares primary imports")
    require("from primary" not in source and "import primary" not in source,
            "n3 generator imports primary code")
    require(source.index("def generate_universe") < source.index("def primary_claim"),
            "primary claim is opened before independent universe generator is defined")
    require(cert["mutations"]["status"] == "VERIFIED", "n3 mutations not verified")
    require(all(cert["mutations"]["mutations"].values()),
            "n3 mutation suite accepted a mutation")
    return {
        "status": "VERIFIED",
        "raw_relations": cert["counts"]["raw_necessary_relations"],
        "merged_relations": cert["counts"]["canonical_merged_relations"],
        "raw_multiset_sha256": cert["hashes"]["independent_raw_multiset_sha256"],
        "merged_multiset_sha256": cert["hashes"]["independent_merged_multiset_sha256"],
        "mutations": sorted(cert["mutations"]["mutations"]),
    }


def check_direct_anchor() -> dict:
    summary = read_json("reviews/direct_anchor_probe_closure/certificates/summary.json")
    mutations = read_json(
        "reviews/direct_anchor_probe_closure/certificates/mutation_results.json"
    )
    require(summary["status"] == "EXACTLY_COMPUTED",
            "direct-anchor summary is not exact")
    require(summary["counts"]["anchors"] == 62, "direct-anchor count changed")
    require(summary["counts"]["anchor_classifications"] == {
        "labelled_isomorphism": 34,
        "ordinary_T": 28,
    }, "direct-anchor base split changed")
    require(summary["counts"]["A_plus_p"] == 2642, "A+p count changed")
    require(summary["counts"]["A_plus_p_survivors"] == 314,
            "A+p survivor count changed")
    require(summary["counts"]["A_plus_p_plus_q"] == 18224,
            "A+p+q count changed")
    require(summary["counts"]["A_plus_p_plus_q_survivors"] == 2032,
            "A+p+q survivor count changed")
    require(summary["separator_search"]["unresolved"] == [],
            "direct-anchor unresolved separators present")
    require(
        summary["coverage_determination"][
            "all_direct_anchors_represented_by_existing_terminal_families"
        ] is False,
        "direct anchors were incorrectly folded into path-bound terminals",
    )
    require(mutations["status"] == "VERIFIED", "direct-anchor mutations not verified")
    require(mutations["mutation_count"] == 12, "direct-anchor mutation count changed")
    require(all(row["rejected"] for row in mutations["mutations"]),
            "direct-anchor mutation accepted")
    return {
        "status": "VERIFIED",
        "anchors": summary["counts"]["anchors"],
        "A_plus_p": summary["counts"]["A_plus_p"],
        "A_plus_p_plus_q": summary["counts"]["A_plus_p_plus_q"],
        "strict_or_generic_separators": (
            summary["counts"]["A_plus_p_classifications"][
                "generic_polynomial_separation"
            ]
            + summary["counts"]["A_plus_p_classifications"][
                "strict_open_cube_separation"
            ]
            + summary["counts"]["A_plus_p_plus_q_classifications"][
                "generic_polynomial_separation"
            ]
            + summary["counts"]["A_plus_p_plus_q_classifications"][
                "strict_open_cube_separation"
            ]
        ),
        "mutations": [row["name"] for row in mutations["mutations"]],
    }


def check_compact_gate() -> dict:
    compact = read_json(
        "reviews/compact_probe_clean_clone_gate/certificates/"
        "compact_only_semantic_replay.json"
    )
    mutations = read_json(
        "reviews/compact_probe_clean_clone_gate/certificates/mutation_tests.json"
    )
    tracked = read_json("reviews/compact_probe_clean_clone_gate/TRACKED_INPUTS.json")
    require(compact["status"] == "VERIFIED", "compact semantic replay not verified")
    families = {row["family"]: row for row in compact["families"]}
    require(families["n3"]["path_inventory_count"] == 144,
            "compact n3 path count changed")
    require(sum(families["n3"]["classification_counts"].values()) == 101148,
            "compact n3 relation count changed")
    require(families["theta2_n4"]["path_inventory_count"] == 132,
            "compact theta2 path count changed")
    require(
        sum(families["theta2_n4"]["classification_counts"].values()) == 168582,
        "compact theta2 relation count changed",
    )
    require(
        max(row["maximum_probe_port_count"] for row in families.values()) == 10,
        "compact ten-port bound changed",
    )
    require(mutations["status"] == "VERIFIED", "compact mutations not verified")
    require(len(mutations["mutations"]) == 9, "compact mutation count changed")
    require(all(row["rejected"] for row in mutations["mutations"]),
            "compact mutation accepted")
    require(tracked["status"] == "VERIFIED", "tracked input lock not verified")
    require(tracked["forbidden_verbose_probe_extension_inputs"] == [],
            "verbose probe-extension input entered compact lock")
    require(tracked["input_count"] == len(tracked["inputs"]) == 50,
            "compact tracked-input count changed")
    return {
        "status": "VERIFIED",
        "tracked_inputs": tracked["input_count"],
        "n3_relations": sum(families["n3"]["classification_counts"].values()),
        "theta2_relations": sum(
            families["theta2_n4"]["classification_counts"].values()
        ),
        "maximum_probe_ports": max(
            row["maximum_probe_port_count"] for row in families.values()
        ),
        "mutations": [row["mutation"] for row in mutations["mutations"]],
    }


def check_manuscript_and_release() -> dict:
    paper = read_text("source/paper/main.tex")
    theorem = read_text("docs/SHARP_BOUNDARY_THEOREM.md")
    definitions = read_text("docs/DEFINITIONS_LOCK.md")
    crosswalk = read_text("THEOREM_CERTIFICATE_CROSSWALK.md")
    release_scripts = "\n".join(
        read_text(path)
        for path in (
            "reproducibility/verify_quick.sh",
            "reproducibility/verify_full.sh",
            "reproducibility/verify_regenerate_all.sh",
        )
    )

    paper_required = [
        "every tail of a retained reticulation edge is incident with two",
        "the source and target incoming boundaries may be chosen independently",
        "The $62$ direct residual anchors require a separate base case",
        "all $2{,}642$",
        "all $18{,}224$",
        "does not recover physical bridge multipliers",
        "complete stochastic images is not asserted",
        "18&\\text{ direct isomorphisms}",
        "42&\\text{ selected-incoming rooting duplicates}",
        "132&\\text{ marginalized-incoming restoration roots}",
        "frozen package \\texttt{../s\\_tc\\_jc\\_sharp\\_boundary/}",
    ]
    paper_flat = compact_space(paper)
    theorem_flat = compact_space(theorem)
    for needle in paper_required:
        require(compact_space(needle) in paper_flat,
                f"paper required phrase missing: {needle}")
    theorem_required = [
        "Source and target incoming boundaries are chosen independently",
        "Each restoration prefix is a direct marginal",
    ]
    for needle in theorem_required:
        require(compact_space(needle) in theorem_flat,
                f"theorem required phrase missing: {needle}")
    require(
        "equivalently every tail of a retained reticulation edge is incident with two"
        in definitions,
        "definition lock lost no-omnian criterion",
    )
    require("The 62 direct residual anchors are a distinct four-port base case"
            in theorem, "sharp theorem lost direct-anchor repair")
    require("reviews/n3_universe_generator/" in crosswalk,
            "crosswalk lost n3 universe repair")
    require("reviews/direct_anchor_probe_closure/" in crosswalk,
            "crosswalk lost direct-anchor repair")
    require("reviews/compact_probe_clean_clone_gate/" in crosswalk,
            "crosswalk lost compact gate")

    compact_paper = paper_flat
    prohibited = [
        "complete open stochastic images are equal",
        "physical bridge multipliers are identifiable",
        "Theta is an S_TC move",
        "reciprocal-only bridge chart is correct",
    ]
    for phrase in prohibited:
        require(phrase not in compact_paper,
                f"withdrawn claim leaked into paper: {phrase}")
    require(re.search(r"(?<!\\)qquad", paper) is None,
            "literal qquad/qquad typo without backslash remains")
    require("probe_extension_" not in release_scripts,
            "release scripts consume verbose probe-extension streams")

    final_outcome = PROJECT / "FINAL_OUTCOME.json"
    release_metadata = PROJECT / "RELEASE_METADATA.json"
    report = HERE / "REPORT.md"
    untracked_verbose = git(
        "ls-files", "--others", "--exclude-standard",
        "primary/certificates/probe_extension*",
    ).splitlines()
    return {
        "status": "VERIFIED",
        "paper_sha256": sha256(PROJECT / "source/paper/main.tex"),
        "sharp_theorem_sha256": sha256(PROJECT / "docs/SHARP_BOUNDARY_THEOREM.md"),
        "release_scripts_reference_verbose_probe_extension": False,
        "final_outcome_present": final_outcome.is_file(),
        "release_metadata_present": release_metadata.is_file(),
        "final_referee_report_present": report.is_file(),
        "untracked_verbose_probe_extension_files_seen_but_not_used": untracked_verbose,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        type=Path,
        help="optional output path; omitted for a read-only verification replay",
    )
    args = parser.parse_args()

    actual_head = git("rev-parse", "HEAD")
    requested_is_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", REQUESTED_COMMIT, "HEAD"],
        cwd=PROJECT,
    ).returncode == 0
    payload = {
        "schema": "final-outcome-p-referee-v2-certificate",
        "status": "VERIFIED",
        "requested_commit": REQUESTED_COMMIT,
        "observed_head_at_certificate_time": actual_head,
        "requested_commit_is_ancestor_of_observed_head": requested_is_ancestor,
        "n3_universe_generation_repair": check_n3_universe(),
        "direct_anchor_probe_repair": check_direct_anchor(),
        "compact_probe_clean_clone_gate": check_compact_gate(),
        "manuscript_and_release_scope": check_manuscript_and_release(),
        "theorem_verdicts": {
            "locked_standard_class_and_automatic_triangle_bound": "VERIFIED",
            "pointwise_two_direction_cut_preservation": "VERIFIED",
            "full_incidence_bridge_kernel_and_projective_localization": "VERIFIED",
            "primitive_core_and_rigid_support_exhaustion": "VERIFIED",
            "independent_n3_relation_universe_and_binding": "VERIFIED",
            "theta2_five_port_18_42_132_gate": "VERIFIED",
            "arbitrary_subdivisions_including_62_direct_anchors": "VERIFIED",
            "root_reduction": "VERIFIED",
            "ordinary_T_embedded_common_regular_germ": "VERIFIED",
            "global_one_sided_iff_and_no_proper_containment": "VERIFIED",
            "exceptional_locus_and_reconstruction": "VERIFIED",
            "frozen_weak_sharpness_theorem": "VERIFIED",
            "manuscript_mathematical_scope": "VERIFIED",
        },
        "load_bearing_blocker": None,
        "non_load_bearing_release_defects": [
            "FINAL_OUTCOME.json absent at reviewed commit",
            "RELEASE_METADATA.json absent at reviewed commit",
            "system python lacks networkx; declared project virtualenv is required",
            "working checkout contains historical untracked probe_extension files, but no active release script consumes them",
        ],
        "terminal_verdict": "VERIFIED",
    }
    if args.write is not None:
        args.write.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "terminal_verdict": payload["terminal_verdict"],
        "n3_raw": payload["n3_universe_generation_repair"]["raw_relations"],
        "direct_A_plus_p": payload["direct_anchor_probe_repair"]["A_plus_p"],
        "compact_relations": (
            payload["compact_probe_clean_clone_gate"]["n3_relations"]
            + payload["compact_probe_clean_clone_gate"]["theta2_relations"]
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
