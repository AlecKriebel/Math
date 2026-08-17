#!/usr/bin/env python3
"""Fail-closed regressions for the v1.1.2 public-release hardening."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import zipfile

from pypdf import PdfReader


PROJECT = Path(__file__).resolve().parents[2]
TAG = "stc-jc-sharp-boundary-v1.1.2"
RELEASE_URL = f"https://github.com/AlecKriebel/Math/releases/tag/{TAG}"

PACKAGE_EXPECTED = {
    "biorxiv_submission": frozenset({
        "Strong_Tree_Childness_Sharp_Level2_JC.pdf",
        "Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf",
        "Strong_Tree_Childness_Sharp_Level2_JC_source.zip",
        "BIORXIV_METADATA.md",
        "BIORXIV_UPLOAD_MAP.md",
        "FINAL_HUMAN_CHECKLIST.md",
    }),
    "journal_submission/systematic_biology": frozenset({
        "SB_Main_Manuscript.pdf",
        "SB_Supplementary_Material.pdf",
        "SB_LaTeX_Source.zip",
        "SB_Cover_Letter.tex",
        "SB_Cover_Letter.pdf",
        "SB_SUBMISSION_METADATA.md",
        "SYSTEMATIC_BIOLOGY_UPLOAD_MAP.md",
        "FINAL_HUMAN_CHECKLIST.md",
    }),
    "journal_submission/journal_of_mathematical_biology": frozenset({
        "JMB_Main_Manuscript.pdf",
        "JMB_Supplementary_Information.pdf",
        "JMB_LaTeX_Source.zip",
        "JMB_Cover_Letter.tex",
        "JMB_Cover_Letter.pdf",
        "JMB_SUBMISSION_METADATA.md",
        "JMB_UPLOAD_MAP.md",
        "FINAL_HUMAN_CHECKLIST.md",
    }),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def text(path: str) -> str:
    return (PROJECT / path).read_text(encoding="utf-8")


def validate_manuscript_and_supplement(paper: str, supplement: str) -> None:
    require(
        "Within the standard strongly tree-child level-2 class, generic exact "
        "infinite-data JC observations recover" in paper,
        "Section 10 genericity qualifier is absent",
    )
    require(
        "supported by exact primary and separately implemented replay" in paper,
        "abstract replay terminology is stale",
    )
    require(
        "independently implemented replay" not in paper,
        "ambiguous independent-review wording returned to the manuscript",
    )
    required_commands = (
        "bash s_tc_jc_landmark_closure/reproducibility/verify_quick.sh",
        "bash s_tc_jc_landmark_closure/reproducibility/verify_full.sh",
        "bash s_tc_jc_landmark_closure/reproducibility/verify_regenerate_all.sh",
    )
    for command in required_commands:
        require(command in supplement, f"supplement command missing: {command}")
    for stale in (
        "bash reproducibility/verify_quick.sh",
        "bash reproducibility/verify_full.sh",
        "bash reproducibility/verify_regenerate_all.sh",
    ):
        require(stale not in supplement, f"monorepository-breaking command returned: {stale}")


def check_manuscript_and_supplement() -> None:
    validate_manuscript_and_supplement(
        " ".join(text("source/paper/main.tex").split()),
        text("source/supplement/supplement.tex"),
    )


def validate_release_binding(final: dict, metadata: dict, public: str) -> None:
    require(RELEASE_URL in public and "RELEASE_ENVELOPE.json" in public,
            "public release assets are not precisely identified")
    require(final["release_revision"] == metadata["release_revision"] == TAG,
            "v1.1.2 release revision is not synchronized")
    expected_envelope = (
        f"https://github.com/AlecKriebel/Math/releases/download/{TAG}/"
        "RELEASE_ENVELOPE.json"
    )
    require(final["source_binding"]["outer_envelope"] == expected_envelope,
            "FINAL_OUTCOME outer-envelope URL is stale")
    require(metadata["source_binding"]["outer_envelope"] == expected_envelope,
            "RELEASE_METADATA outer-envelope URL is stale")


def check_replay_provenance() -> None:
    for stale in (
        "release/CLEAN_REPRODUCTION.json",
        "release/verify_quick.log",
        "release/verify_full.log",
        "release/verify_regenerate_all.log",
    ):
        require(not (PROJECT / stale).exists(), f"stale active replay evidence returned: {stale}")
    historical = PROJECT / "history/superseded_release_evidence/outcome_p_2026-08-13"
    for name in (
        "README.md",
        "SHA256SUMS",
        "CLEAN_REPRODUCTION.json",
        "verify_quick.log",
        "verify_full.log",
        "verify_regenerate_all.log",
    ):
        require((historical / name).is_file(), f"superseded evidence missing: {name}")
    require("18-page" in (historical / "README.md").read_text(encoding="utf-8"),
            "historical replay scope is not explicit")
    historical_expected = frozenset({
        "ARCHIVE_REPRODUCTION.md", "CLEAN_REPRODUCTION.json", "README.md",
        "stc_jc_landmark_closure_outcome_p.tar.gz.sha256", "verify_full.log",
        "verify_quick.log", "verify_regenerate_all.log",
    })
    validate_manifest_lines(
        (historical / "SHA256SUMS").read_text(encoding="utf-8").splitlines(),
        historical_expected,
        historical,
    )
    final = json.loads(text("FINAL_OUTCOME.json"))
    metadata = json.loads(text("RELEASE_METADATA.json"))
    validate_release_binding(final, metadata, text("release/PUBLIC_RELEASE_ASSETS.md"))
    local_envelope = PROJECT / "release_artifacts/RELEASE_ENVELOPE.json"
    if local_envelope.is_file():
        envelope = json.loads(local_envelope.read_text(encoding="utf-8"))
        require(
            envelope.get("core_metadata_sha256")
            == hashlib.sha256((PROJECT / "RELEASE_METADATA.json").read_bytes()).hexdigest(),
            "local release envelope is stale relative to active metadata",
        )


def validate_manifest_lines(
    lines: list[str], expected_names: frozenset[str], directory: Path | None = None
) -> None:
    require(lines, "empty checksum manifest")
    rows: dict[str, str] = {}
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", line)
        require(match is not None, f"malformed or non-flat checksum row: {line}")
        expected_hash, name = match.groups()
        require(name not in rows, f"duplicate checksum target: {name}")
        rows[name] = expected_hash
    require(frozenset(rows) == expected_names,
            f"checksum target set differs: {sorted(frozenset(rows) ^ expected_names)}")
    if directory is not None:
        for name, expected_hash in rows.items():
            target = directory / name
            require(target.is_file(), f"checksum target missing: {target}")
            require(hashlib.sha256(target.read_bytes()).hexdigest() == expected_hash,
                    f"checksum mismatch: {target}")


def verify_sum_file(directory: Path, expected_names: frozenset[str]) -> None:
    manifest = (directory / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    validate_manifest_lines(manifest, expected_names, directory)


def check_submission_packages() -> None:
    for directory, names in PACKAGE_EXPECTED.items():
        for name in names | {"SHA256SUMS"}:
            require((PROJECT / directory / name).is_file(),
                    f"submission artifact missing: {directory}/{name}")
        verify_sum_file(PROJECT / directory, names)
    main = PdfReader(PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC.pdf")
    supp = PdfReader(PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf")
    require(len(main.pages) == 31 and len(supp.pages) == 6,
            "submission PDFs have implausible page counts")
    sb = PdfReader(PROJECT / "journal_submission/systematic_biology/SB_Main_Manuscript.pdf")
    jmb = PdfReader(PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_Main_Manuscript.pdf")
    require(len(sb.pages) >= 38 and len(jmb.pages) == 31,
            "journal review PDFs have implausible page counts")
    with zipfile.ZipFile(PROJECT / "journal_submission/systematic_biology/SB_LaTeX_Source.zip") as archive:
        figure_sources = [name for name in archive.namelist() if "/figures/" in name]
        require(len(figure_sources) == 7, "SB source ZIP does not contain seven figures")
        for name in figure_sources:
            require(b"Alt text:" in archive.read(name), f"SB figure alt text missing: {name}")
        require(any(name.endswith("/BUILD.md") for name in archive.namelist()),
                "SB source ZIP lacks build instructions")
    with zipfile.ZipFile(PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_LaTeX_Source.zip") as archive:
        main_name = next(name for name in archive.namelist() if name.endswith("/paper/main.tex"))
        main_source = archive.read(main_name)
        require(b"Statements and Declarations" in main_source,
                "JMB source ZIP lacks grouped declarations")
        require(b"Online Resource~1" in main_source,
                "JMB manuscript does not cite Online Resource 1")
        supplement_name = next(
            name for name in archive.namelist()
            if name.endswith("/supplement/supplement.tex")
        )
        supplement_source = archive.read(supplement_name)
        for needle in (
            b"Online Resource 1", b"Journal of Mathematical Biology",
            b"me@aleckriebel.com", b"Independent Researcher",
        ):
            require(needle in supplement_source,
                    f"JMB supplement identification missing: {needle!r}")
        require(any(name.endswith("/BUILD.md") for name in archive.namelist()),
                "JMB source ZIP lacks build instructions")
    require("site-under-development" in text(
        "journal_submission/journal_of_mathematical_biology/JMB_UPLOAD_MAP.md"
    ), "JMB portal warning is missing")
    require("Research Article" in text(
        "journal_submission/systematic_biology/SYSTEMATIC_BIOLOGY_UPLOAD_MAP.md"
    ), "Systematic Biology article type is missing")


def must_reject(label: str, operation) -> None:
    try:
        operation()
    except AssertionError:
        return
    raise AssertionError(f"mutation was accepted: {label}")


def mutation_tests() -> None:
    paper = " ".join(text("source/paper/main.tex").split())
    supplement = text("source/supplement/supplement.tex")
    mutations = {
        "remove-generic": paper.replace("generic exact infinite-data", "exact infinite-data", 1),
        "restore-independent-wording": paper.replace(
            "separately implemented replay", "independently implemented replay", 1
        ),
        "break-monorepo-command": supplement.replace(
            "bash s_tc_jc_landmark_closure/reproducibility/verify_quick.sh",
            "bash reproducibility/verify_quick.sh",
            1,
        ),
    }
    must_reject(
        "remove-generic",
        lambda: validate_manuscript_and_supplement(
            mutations["remove-generic"], supplement
        ),
    )
    must_reject(
        "restore-independent-wording",
        lambda: validate_manuscript_and_supplement(
            mutations["restore-independent-wording"], supplement
        ),
    )
    must_reject(
        "break-monorepo-command",
        lambda: validate_manuscript_and_supplement(
            paper, mutations["break-monorepo-command"]
        ),
    )
    final = json.loads(text("FINAL_OUTCOME.json"))
    metadata = json.loads(text("RELEASE_METADATA.json"))
    bad_metadata = json.loads(json.dumps(metadata))
    bad_metadata["source_binding"]["outer_envelope"] = (
        "https://example.invalid/stale-envelope.json"
    )
    must_reject(
        "stale-envelope",
        lambda: validate_release_binding(
            final, bad_metadata, text("release/PUBLIC_RELEASE_ASSETS.md")
        ),
    )
    package = PROJECT / "biorxiv_submission"
    manifest_lines = (package / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    expected = PACKAGE_EXPECTED["biorxiv_submission"]
    must_reject(
        "delete-manifest-row",
        lambda: validate_manifest_lines(manifest_lines[:-1], expected, package),
    )
    must_reject(
        "duplicate-manifest-row",
        lambda: validate_manifest_lines(manifest_lines + [manifest_lines[0]], expected, package),
    )
    renamed = list(manifest_lines)
    renamed[0] = renamed[0].split("  ", 1)[0] + "  renamed-main.pdf"
    must_reject(
        "rename-manifest-target",
        lambda: validate_manifest_lines(renamed, expected, package),
    )
    swapped = list(manifest_lines)
    hash_a, name_a = swapped[0].split("  ", 1)
    hash_b, name_b = swapped[1].split("  ", 1)
    swapped[0] = f"{hash_a}  {name_b}"
    swapped[1] = f"{hash_b}  {name_a}"
    must_reject(
        "misassign-valid-hash",
        lambda: validate_manifest_lines(swapped, expected, package),
    )
    public_path = PROJECT / "reproducibility/verify_public_release.py"
    spec = importlib.util.spec_from_file_location("stc_jc_public_release", public_path)
    require(spec is not None and spec.loader is not None,
            "cannot load public-release verifier for bounded regressions")
    public = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(public)
    must_reject(
        "lightweight-public-tag",
        lambda: public.peel_annotated_tag(
            {"object": {"type": "commit", "sha": "a" * 40}},
            {"object": {"type": "commit", "sha": "a" * 40}},
        ),
    )
    manifest_digest = hashlib.sha256(
        (PROJECT / "biorxiv_submission/SHA256SUMS").read_bytes()
    ).hexdigest()
    result = public.public_result(
        "https://example.invalid/release", "a" * 40,
        PROJECT / "biorxiv_submission/SHA256SUMS",
    )
    require(result["release_asset_manifest_sha256"] == manifest_digest,
            "public verdict does not record the downloaded manifest digest")
    bad_result = dict(result)
    bad_result["release_asset_manifest_sha256"] = "0" * 64
    must_reject(
        "falsified-public-manifest-digest",
        lambda: public.validate_result_manifest(
            bad_result, PROJECT / "biorxiv_submission/SHA256SUMS"
        ),
    )


def main() -> None:
    check_manuscript_and_supplement()
    check_replay_provenance()
    check_submission_packages()
    mutation_tests()
    print(json.dumps({
        "status": "PACKAGE_CANDIDATE_VERIFIED",
        "revision": "v1.1.2",
        "public_release_target": RELEASE_URL,
        "public_release_status": "REQUIRES_POST_UPLOAD_EXTERNAL_GATE",
        "targeted_mutations_rejected": 10,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
