#!/usr/bin/env python3
"""Fail-closed checks for the Englander-v4 and submission-package revision."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import zipfile


PROJECT = Path(__file__).resolve().parents[2]
EXPECTED_PDF_SHA256 = (
    "3c140c36aae45cd07040b0f1e03b55b40f7c61f14a04b9fbe9cd8c48112e8ba5"
)
TAG = "stc-jc-sharp-boundary-v1.1.3"
ROWS = "(A,B,C,D,E,F,G,H,K)"
MINORS = {
    "-171/2305843009213693952000000",
    "-513/9223372036854775808000000",
    "57/576460752303423488000000",
    "189/2305843009213693952000000",
}
CAPSULES = (
    PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_verifier_entrypoints.zip",
    PROJECT / "journal_submission/systematic_biology/SB_Exact_Verifier_Entry_Points.zip",
    PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_Exact_Verifier_Entry_Points.zip",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def compact(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def check_paper(text: str) -> None:
    for needle in (
        "type~(2c)",
        "contains no type-(2c)-versus-type-(2c) distinction",
        "Lemma~2.14(b) cannot be extended from type~(2a) to all type-(2) quarnets",
        "The two displayed-rooting presentations have the same arc set",
        r"\mathcal I_{\mathrm{tri}}",
        "denoted $q_{111}$",
        "exactly the incidence criterion stated for strongly tree-child",
        "lower-than-naive model dimensions",
        "Both all-$n$ sharpness families are obtained from certified four-leaf",
        "HoltgrefeEtAl2025Quartets",
    ):
        require(needle in text, f"paper revision phrase missing: {needle}")
    require("distinct type-1b ideal question" not in text,
            "obsolete Omega/type-1b comparison survived")


def check_supplement(text: str) -> None:
    require(ROWS in text, "Omega rank-nine row set missing")
    for minor in MINORS:
        require(minor in text, f"Omega rank-nine determinant missing: {minor}")
    for columns in (
        "(0,1,2,3,4,7,8,9,10)",
        "(0,1,2,3,5,7,8,9,10)",
    ):
        require(columns in text, f"Omega rank-nine columns missing: {columns}")
    require("Monorepository-root-relative evidence" in text,
            "supplement path convention is not explicit")
    require("code's state-group name" not in text,
            "malformed historical state-group sentence survived")


def check_exact_omega_record() -> None:
    record = json.loads((
        PROJECT / "omega_audit/independent/output/omega_release_audit.json"
    ).read_text(encoding="utf-8"))
    require(record["status"] == "OMEGA-PASS-ALL-(n)", "Omega status changed")
    for topology in record["topology"].values():
        stats = topology["statistics"]
        require(stats["cycle_lengths"] == [4, 4, 6] and
                stats["triangle_count"] == 0 and stats["level"] == 2,
                "Omega topology signature changed")
        require(topology["class"] == "W_TC\\S_TC" and
                topology["tree_child_rooting_count"] == 2 and
                topology["admissible_rooting_count"] == 7,
                "Omega rooting/class record changed")
        violation = topology["omnian_test"]["violations"]
        require(violation == [{
            "incident_undirected_edges": 1,
            "outgoing_reticulation_edges": 2,
            "vertex": "U",
        }], "Omega incidence witness changed")
    algebra = record["stochastic"]["independent_algebra_audit"]
    exact = algebra["exact_common_point"]["networks"]
    require({entry["rank_nine_minor"] for entry in exact.values()} == MINORS,
            "supplement minors do not match the independent Omega record")
    require(algebra["generic_rank"]["complete_generic_rank"] == 9,
            "Omega exact generic rank changed")


def check_capsule(path: Path) -> None:
    require(path.is_file(), f"submission-support verifier capsule missing: {path}")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        require("README.md" in names and "SHA256SUMS" in names,
                f"submission-support verifier capsule metadata missing: {path}")
        readme = archive.read("README.md").decode("utf-8")
        require(TAG in readme and "not the complete proof archive" in readme,
                f"submission-support verifier capsule scope/tag changed: {path}")
        require("Python dependency" in readme and "Tectonic 0.16.9" in readme,
                f"submission-support verifier capsule overstates its environment lock: {path}")
        require("submission-support capsule" in readme and
                "portal attachment" not in readme and
                "A plain\narchive extraction has no Git history" in readme,
                f"verifier capsule clone/archive routing changed: {path}")
        require("No script submits a manuscript" in readme,
                f"submission-support verifier capsule external-action boundary missing: {path}")


def mutation_tests(paper: str, supplement: str) -> None:
    mutations = (
        (check_paper, paper.replace("type~(2c)", "type~(1b)")),
        (check_paper, paper.replace("denoted $q_{111}$", "denoted $q_{123}$")),
        (check_supplement, supplement.replace(next(iter(MINORS)), "0")),
        (check_supplement, supplement.replace(ROWS, "(A,B,C,D,E,F,G,H,J)")),
    )
    for checker, mutation in mutations:
        try:
            checker(mutation)
        except AssertionError:
            continue
        raise AssertionError(f"mandatory mutation escaped: {checker.__name__}")


def main() -> None:
    paper = compact(PROJECT / "source/paper/main.tex")
    supplement = compact(PROJECT / "source/supplement/supplement.tex")
    check_paper(paper)
    check_supplement(supplement)
    check_exact_omega_record()

    build = compact(PROJECT / "source/BUILD.md")
    supplement_build = compact(PROJECT / "source/supplement/BUILD.md")
    for text in (build, supplement_build):
        require("SOURCE_DATE_EPOCH=1786924800" in text and
                "Tectonic 0.16.9" in text,
                "documented exact-byte PDF build omits its epoch/tool version")

    bibliography = compact(PROJECT / "source/paper/references.bib")
    require("HoltgrefeEtAl2025Quartets" in bibliography and
            "10.1007/s11538-025-01549-4" in bibliography,
            "quartet-distance reference missing")
    crosswalk = compact(PROJECT / "reviews/v1_1_3_englander_revision/ENGLANDER_V4_CROSSWALK.md")
    require(EXPECTED_PDF_SHA256 in crosswalk and "Zenodo DOI" in crosswalk,
            "Englander source hash/crosswalk missing")

    for path in CAPSULES:
        check_capsule(path)
    require(len({hashlib.sha256(path.read_bytes()).hexdigest() for path in CAPSULES}) == 1,
            "submission-support verifier capsules are not byte-identical")

    upload_surfaces = compact(PROJECT / "biorxiv_submission/BIORXIV_UPLOAD_MAP.md")
    require("verifier_entrypoints.zip" in upload_surfaces and
            "hundreds of megabytes" in upload_surfaces,
            "bioRxiv verifier/full-archive split is not explicit")
    sb_map = compact(PROJECT / "journal_submission/systematic_biology/SYSTEMATIC_BIOLOGY_UPLOAD_MAP.md")
    require("Do **not** upload `SB_Exact_Verifier_Entry_Points.zip`" in sb_map and
            "repository deposit" in sb_map,
            "Systematic Biology code-deposit policy is not enforced")
    jmb_map = compact(PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_UPLOAD_MAP.md")
    require("Do not designate `JMB_Exact_Verifier_Entry_Points.zip`" in jmb_map and
            "second Online Resource" in jmb_map,
            "JMB verifier capsule is incorrectly designated for portal upload")
    require("10.5281/zenodo.TODO" not in paper and
            "10.5281/zenodo.TODO" not in upload_surfaces,
            "invented project DOI placeholder leaked into active surfaces")

    public_path = PROJECT / "reproducibility/verify_public_release.py"
    spec = importlib.util.spec_from_file_location("verify_public_release_v113", public_path)
    require(spec is not None and spec.loader is not None,
            "public-release verifier could not be imported")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.mutation_test_tag_binding()
    public_text = public_path.read_text(encoding="utf-8")
    require("public_project_blobs(tag_commit)" in public_text and
            "verify_extracted_archive.py" in public_text,
            "public verifier does not bind tagged source and replay extraction")

    source_replay_path = PROJECT / "reproducibility/verify_submission_source_archives.py"
    replay_spec = importlib.util.spec_from_file_location(
        "verify_submission_source_archives_v113", source_replay_path
    )
    require(replay_spec is not None and replay_spec.loader is not None,
            "submission-source verifier could not be imported")
    replay_module = importlib.util.module_from_spec(replay_spec)
    replay_spec.loader.exec_module(replay_module)
    replay_module.mutation_test_outer_manifest()
    require(all(any("Verifier_Entry_Points.zip" in name or
                    "verifier_entrypoints.zip" in name
                    for name in expected)
                for expected in replay_module.PACKAGE_MANIFESTS.values()),
            "a current package manifest universe omits its verifier capsule")

    mutation_tests(paper, supplement)
    print("VERIFIED: Englander-v4 crosswalk, Omega witnesses, and submission-support verifier capsules")


if __name__ == "__main__":
    main()
