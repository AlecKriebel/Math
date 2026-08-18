#!/usr/bin/env python3
"""Fail-closed checks for the bounded v1.1.4 proof and Figure 7 revision."""

from __future__ import annotations

import json
import math
from pathlib import Path
import re


PROJECT = Path(__file__).resolve().parents[2]
TAG = "stc-jc-sharp-boundary-v1.1.4"
BCR_SHA256 = "ad406cb6d1342abf194126467ed440d4bcafc5073af48eef43e060540f168ef4"
EXPECTED_N26_VECTORS = {
    "N26_source": [
        "1/4", "1/2", "1/2", "3/4", "2/3", "1/4", "1/2",
        "1/20", "1/2", "1/2", "1/10", "1/2", "1/2", "1/2",
    ],
    "N26_target": [
        "1/7", "1/2", "41/48", "19/24", "14/19", "14/41", "1/2",
        "12/205", "1/2", "1/2", "3/40", "1/2", "1/2", "1/2",
    ],
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def compact(text: str) -> str:
    return " ".join(text.split())


def check_paper(text: str) -> None:
    flat = compact(text)
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S)
    require(abstract is not None, "abstract not found")
    require(r"Definition~\ref{def:fixed-mixed}" not in abstract.group(1),
            "contextless internal definition reference survived in abstract")
    require("fixed one-step reticulation-preserving semi-directed convention" in
            abstract.group(1), "abstract no longer states the fixed convention")

    for needle in (
        r"\newcommand{\preceqproj}{\preceq_{\!\mathrm{proj}}}",
        r"\PM_H\preceqproj\PM_{H'}",
        r"P\in(\PM_H)_{\rm reg}\cap\PM_{H'}",
        "The target dimension is allowed to be larger.",
        r"\PM_{\,H|_{Q_s\cup D_j}}\preceqproj",
        r"\begin{theorem}[Finite decorated-relation theorem]\label{thm:atlas}",
        r"\cref{thm:atlas,lem:probes}",
        "choose a nonempty relatively open semialgebraic neighborhood",
        "Proposition~2.8.5(i), applied to the finite atlas",
        "Theorem~2.2.1, applied iteratively",
        r"\dim(\overline C\setminus C)<d",
        r"\dim(\overline A\setminus A)<\dim A",
        "semialgebraic bijections preserve dimension",
        "displayed-rooting source and target minors listed with their",
        "alternative-rooting minors give an additional",
        "type-(2a) statement of Lemma~2.14(b) does not extend to all type-(2c)",
        r"All paths in this appendix are relative to the project root",
    ):
        require(needle in flat, f"required v1.1.4 paper phrase missing: {needle}")

    for prohibited in (
        r"\PM_H\preceq\PM_{H'}",
        r"\label{lem:atlas}",
        "invariance of semialgebraic dimension under semialgebraic homeomorphism",
        "to all type-(2) quarnets",
    ):
        require(prohibited not in flat, f"superseded v1.1.4 phrase survived: {prohibited}")

    atlas = re.search(
        r"\\begin\{theorem\}\[Finite decorated-relation theorem\].*?"
        r"\\end\{theorem\}", text, re.S,
    )
    require(atlas is not None, "finite atlas theorem block missing")
    require(r"\fbox" not in atlas.group(0) and r"\begin{minipage}" not in atlas.group(0),
            "production-fragile atlas box survived")


def check_figure(text: str) -> None:
    d = re.search(r"\\node\[treev\] \(D\) at \(([-.0-9]+),([-.0-9]+)\)", text)
    leaf = re.search(r"\\node\[leaf\] \(lD\) at \(([-.0-9]+),([-.0-9]+)\) \{\$2\$\}", text)
    require(d is not None and leaf is not None, "Figure 7 D/leaf-2 coordinates missing")
    dx, dy = map(float, d.groups())
    lx, ly = map(float, leaf.groups())
    require(math.hypot(dx - lx, dy - ly) > 1.0,
            "Figure 7 leaf 2 remains too close to D")
    require(lx < dx - 1.0, "Figure 7 leaf 2 is not visibly separated to the left")
    require(r"\draw (D)--(lD);" in text, "Figure 7 pendant edge D--2 missing")


def check_bibliography(text: str) -> None:
    require("Shelby Cox and Elizabeth Gross and Samuel Martin" in text,
            "Cox first name is not corrected")
    require("Sarah Cox" not in text, "incorrect Cox first name survived")
    sullivant = re.search(r"@misc\{Sullivant2026,(.*?)\n\}", text, re.S)
    require(sullivant is not None, "Sullivant record missing")
    require("year         = {2025}" in sullivant.group(1) and
            "revised 14 July 2026" in sullivant.group(1),
            "Sullivant original-year/revision metadata changed")
    currie = re.search(r"@misc\{CurrieEtAl2026,(.*?)\n\}", text, re.S)
    require(currie is not None and "year         = {2026}" in currie.group(1),
            "unrelated Currie publication year was changed")


def check_supplement(text: str) -> None:
    flat = compact(text)
    for needle in (
        "alternative rooting (historical census entry N26)",
        r"U\to P0\_0",
        r"S\to V",
        r"X0\to L3",
        "displayed-rooting source and target minors give the rank lower bound",
        "alternative-rooting minors are an additional exact check",
        r"N26_{\rm source}",
        r"\frac{41}{48}",
        r"N26_{\rm target}",
        r"\frac{14}{41}",
        "Monorepository-root-relative evidence",
    ):
        require(needle in flat, f"supplement v1.1.4 evidence missing: {needle}")


def check_source_audit() -> None:
    record = json.loads((
        PROJECT / "reviews/v1_1_4_bcr_and_figure_revision/BCR_SOURCE_AUDIT.json"
    ).read_text(encoding="utf-8"))
    require(record["status"] == "SOURCE VERIFIED", "BCR audit status changed")
    require(record["source"]["sha256"] == BCR_SHA256 and
            record["source"]["page_count"] == 429,
            "BCR source identity changed")
    require(record["whole_book_loaded"] is False,
            "bounded BCR inspection claim changed")
    expected = {
        "Theorem 2.2.1", "Proposition 2.8.2", "Proposition 2.8.4",
        "Proposition 2.8.5(i)", "Proposition 2.8.5(ii)",
        "Theorem 2.8.8", "Proposition 2.8.13",
    }
    require({row["result"] for row in record["inspected"]} == expected and
            all(row["verified"] for row in record["inspected"]),
            "BCR cited-result inventory changed")


def check_omega_record(record: dict) -> None:
    parameter_record = record["stochastic"]["exact_common_parameter_vectors"]
    require(parameter_record["order"] == "e_0,...,e_11,lambda_V,lambda_X0",
            "Omega parameter-vector order changed")
    require(
        {name: parameter_record["vectors"][name] for name in EXPECTED_N26_VECTORS}
        == EXPECTED_N26_VECTORS,
        "Omega N26 parameter vectors changed",
    )


def mutation_tests(paper: str, figure: str, bibliography: str, supplement: str,
                   omega_record: dict) -> None:
    mutations = (
        (check_paper, paper.replace(r"\label{thm:atlas}", r"\label{lem:atlas}")),
        (check_paper, paper.replace(r"\preceqproj", r"\preceq", 1)),
        (check_paper, paper.replace("Proposition~2.8.5(i), applied to the finite atlas",
                                   "Proposition~2.8.5, applied to the finite atlas")),
        (check_figure, figure.replace("(-.35,-1.05)", "(.25,-.85)")),
        (check_bibliography, bibliography.replace("Shelby Cox", "Sarah Cox")),
        (check_supplement, supplement.replace(r"U\to P0\_0", r"U\to V", 1)),
        (check_supplement, supplement.replace(
            "displayed-rooting source and target minors give the rank lower bound",
            "all four minors jointly give the rank lower bound",
        )),
        (check_supplement, supplement.replace(r"\frac{14}{41}", r"\frac{15}{41}")),
    )
    for checker, mutation in mutations:
        try:
            checker(mutation)
        except AssertionError:
            continue
        raise AssertionError(f"mandatory mutation escaped: {checker.__name__}")

    changed_record = json.loads(json.dumps(omega_record))
    changed_record["stochastic"]["exact_common_parameter_vectors"]["vectors"] \
        ["N26_target"][5] = "15/41"
    try:
        check_omega_record(changed_record)
    except AssertionError:
        return
    raise AssertionError("mandatory Omega parameter-vector mutation escaped")


def main() -> None:
    paper = (PROJECT / "source/paper/main.tex").read_text(encoding="utf-8")
    figure = (PROJECT / "source/paper/figures/theta_pair.tex").read_text(encoding="utf-8")
    bibliography = (PROJECT / "source/paper/references.bib").read_text(encoding="utf-8")
    supplement = (PROJECT / "source/supplement/supplement.tex").read_text(encoding="utf-8")
    omega_record = json.loads((
        PROJECT / "omega_audit/independent/output/omega_release_audit.json"
    ).read_text(encoding="utf-8"))
    check_paper(paper)
    check_figure(figure)
    check_bibliography(bibliography)
    check_supplement(supplement)
    check_source_audit()
    check_omega_record(omega_record)
    mutation_tests(paper, figure, bibliography, supplement, omega_record)

    final = json.loads((PROJECT / "FINAL_OUTCOME.json").read_text(encoding="utf-8"))
    require(final["release_revision"] == TAG,
            "active release revision is not v1.1.4")
    print(json.dumps({
        "status": "VERIFIED",
        "release": TAG,
        "bcr_source_sha256": BCR_SHA256,
        "mutations_rejected": 9,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
