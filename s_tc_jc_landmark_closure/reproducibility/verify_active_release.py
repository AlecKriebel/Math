#!/usr/bin/env python3
"""Fail-closed semantic checks for the active sharp-boundary release."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys


PROJECT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(relative: str):
    return json.loads((PROJECT / relative).read_text(encoding="utf-8"))


def main() -> None:
    status = (PROJECT / "STATUS.md").read_text(encoding="utf-8")
    theorem = (PROJECT / "docs/SHARP_BOUNDARY_THEOREM.md").read_text(encoding="utf-8")
    paper = (PROJECT / "source/paper/main.tex").read_text(encoding="utf-8")
    dependency = (PROJECT / "CLAIM_DEPENDENCY_GRAPH.md").read_text(encoding="utf-8")

    final_path = PROJECT / "FINAL_OUTCOME.json"
    require(final_path.is_file(), "FINAL_OUTCOME.json missing")
    final = load_json("FINAL_OUTCOME.json")
    require(final["outcome"] == "P", "active release is not Outcome P")
    require(final["status"] == "PROVED", "Outcome P is not marked PROVED")
    require("PROVED" in status and "OUTCOME P" in status.upper(), "STATUS is not final")
    require("| P |" in dependency and "VERIFIED" in dependency, "dependency graph is not closed")

    required_paper = [
        r"\begin{theorem}[Strong-class classification]",
        r"N\preceqjc N'",
        r"There is no proper one-sided",
        r"\begin{theorem}[Sharpness]",
        r"\TCw\setminus\TCs",
        r"complete stochastic images is not asserted",
        r"does not recover physical bridge multipliers",
        r"18\text{ direct isomorphisms}",
        r"42\text{ selected-incoming rooting duplicates}",
        r"132\text{ marginalized-incoming restoration roots}",
        r"reviews/final\_outcome\_p\_referee/",
    ]
    for needle in required_paper:
        require(needle in paper, f"paper scope/certificate phrase missing: {needle}")
    prohibited = [
        "reciprocal-only bridge chart is correct",
        "physical bridge multipliers are identifiable",
        "Theta is an S_TC move",
        "complete open stochastic images are equal",
    ]
    compact = " ".join(paper.split())
    for phrase in prohibited:
        require(phrase not in compact, f"withdrawn claim leaked into paper: {phrase}")

    require("source and target incoming boundaries may be chosen independently" in theorem,
            "independent incoming-role quantifier missing")
    require("Every prefix is a direct" in theorem,
            "restoration direction lock missing")
    require("full incidence action" in theorem,
            "correct bridge action missing")

    n3 = load_json("reviews/bounded_directed_relation_cleanroom/certificates/n3_full_replay.json")
    require(n3["status"] == "VERIFIED", "n3 relation gate not verified")
    n3_manifest = load_json("reviews/bounded_directed_relation_cleanroom/certificates/n3_manifest.json")
    for relative, record in n3_manifest["external_inputs"].items():
        path = (PROJECT / relative).resolve()
        require(path.is_file(), f"n3 locked input missing: {relative}")
        require(path.stat().st_size == record["bytes"], f"n3 locked input size changed: {relative}")
        require(sha256(path) == record["sha256"], f"n3 locked input hash changed: {relative}")
    certificate_dir = PROJECT / "reviews/bounded_directed_relation_cleanroom/certificates"
    for relative, record in n3_manifest["generated_certificates"].items():
        path = certificate_dir / relative
        require(path.is_file() and sha256(path) == record["sha256"],
                f"n3 independent certificate changed: {relative}")
    theta = load_json("reviews/theta2_signature_gate/signature_certificate.json")
    quotient = load_json("reviews/theta2_signature_gate/canonical_quotient_certificate.json")
    require(theta["status"] == quotient["status"] == "VERIFIED", "theta2 gate not verified")
    require(quotient["intrinsic_partition"] == {
        "direct_no_omitted_roles": 18,
        "nonretaining_marginalized_incoming": 132,
        "nonretaining_selected_incoming": 42,
    }, "theta2 partition changed")
    require(quotient["marginalized_presentation_multiset_equals_frozen"],
            "theta2 root multiset mismatch")

    triangle = load_json("primary/certificates/jc_triangle_redirection_active.json")
    require(triangle["status"] == "VERIFIED", "triangle germ not verified")
    require(triangle["stochastic_conclusion"]["complete_open_stochastic_image_equality"] == "NOT CLAIMED",
            "triangle scope widened")

    referee = PROJECT / "reviews/final_outcome_p_referee/REPORT.md"
    require(referee.is_file(), "whole-proof referee report missing")
    report = referee.read_text(encoding="utf-8")
    require(re.search(r"final (decision|verdict).*VERIFIED", report, re.I | re.S),
            "whole-proof referee did not issue a VERIFIED verdict")

    pdf = PROJECT / "submission/Strong_Tree_Childness_Sharp_Level2_JC_Boundary.pdf"
    require(pdf.is_file() and pdf.stat().st_size > 75_000, "submission PDF missing or too small")

    print(json.dumps({
        "status": "VERIFIED",
        "outcome": "P",
        "paper_sha256": sha256(PROJECT / "source/paper/main.tex"),
        "pdf_sha256": sha256(pdf),
        "theta2_partition": [18, 42, 132],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FALSE: {exc}", file=sys.stderr)
        raise
