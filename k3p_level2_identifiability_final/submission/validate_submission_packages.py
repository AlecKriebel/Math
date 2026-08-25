#!/usr/bin/env python3
"""Fail-closed static gate for the draft submission source packages."""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SUBMISSION = PROJECT / "submission"
TOKEN_RE = re.compile(r"@@([A-Z][A-Z0-9_]*)@@")
DOCUMENTATION_TOKENS = {"TOKEN", "UPPER_CASE_TOKEN"}
TEXT_SUFFIXES = {".tex", ".md", ".json", ".txt"}


def add_error(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def latex_word_count(text: str) -> int:
    text = re.sub(r"%.*", " ", text)
    text = re.sub(r"\\(?:begin|end)\{[^{}]+\}", " ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", text)
    text = text.replace("{", " ").replace("}", " ")
    text = re.sub(r"\\\(|\\\)|\\\[|\\\]|\$", " ", text)
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text))


def extract_environment(text: str, name: str) -> str | None:
    match = re.search(
        rf"\\begin\{{{re.escape(name)}\}}(.*?)\\end\{{{re.escape(name)}\}}",
        text,
        re.DOTALL,
    )
    return match.group(1).strip() if match else None


def package_status(errors: list[str], blockers: list[str]) -> tuple[str, int]:
    if errors:
        return "INVALID", 1
    if blockers:
        return "NOT_READY", 2
    return "READY", 0


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # fail closed on syntax or I/O errors
        errors.append(f"invalid JSON {path.relative_to(PROJECT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"JSON root is not an object: {path.relative_to(PROJECT)}")
        return {}
    return value


def validate_manifest(path: Path, errors: list[str], blockers: list[str]) -> dict:
    data = load_json(path, errors)
    add_error(errors, data.get("schema_version") == 1,
              f"unsupported manifest schema: {path.relative_to(PROJECT)}")
    source_map = data.get("source_map")
    add_error(errors, isinstance(source_map, list) and bool(source_map),
              f"manifest has no source_map: {path.relative_to(PROJECT)}")
    destinations: set[str] = set()
    if isinstance(source_map, list):
        for entry in source_map:
            if not isinstance(entry, dict):
                errors.append(f"non-object source_map entry in {path.relative_to(PROJECT)}")
                continue
            source = entry.get("source", "")
            destination = entry.get("destination", "")
            add_error(errors, bool(source) and (PROJECT / source).exists(),
                      f"missing manifest source {source!r} in {path.relative_to(PROJECT)}")
            dest_path = Path(destination)
            add_error(errors, bool(destination) and not dest_path.is_absolute()
                      and ".." not in dest_path.parts,
                      f"unsafe manifest destination {destination!r} in {path.relative_to(PROJECT)}")
            add_error(errors, destination not in destinations,
                      f"duplicate manifest destination {destination!r} in {path.relative_to(PROJECT)}")
            destinations.add(destination)
            add_error(errors, entry.get("mode", "copy_file") in {"copy_file", "copy_tree"},
                      f"unknown source-map mode in {path.relative_to(PROJECT)}: {entry.get('mode')}")
    for upload in data.get("initial_portal_uploads", []):
        if isinstance(upload, dict) and upload.get("present") is False:
            blockers.append(
                f"release PDF/upload not yet produced for {data.get('package')}: "
                f"{upload.get('filename')}"
            )
    return data


def validate() -> tuple[dict, int]:
    errors: list[str] = []
    blockers: list[str] = []

    required = [
        SUBMISSION / "AUTHOR_METADATA.json",
        SUBMISSION / "systematic_biology/main_systematic_biology.tex",
        SUBMISSION / "systematic_biology/supplement_systematic_biology.tex",
        SUBMISSION / "systematic_biology/cover_letter.md",
        SUBMISSION / "journal_of_mathematical_biology/main_jmb.tex",
        SUBMISSION / "journal_of_mathematical_biology/supplement_jmb.tex",
        SUBMISSION / "journal_of_mathematical_biology/cover_letter.md",
        SUBMISSION / "arxiv/main_arxiv.tex",
        SUBMISSION / "arxiv/00README.json",
        SUBMISSION / "shared/full_abstract.tex",
        SUBMISSION / "shared/canonical_article_body.tex",
    ]
    for path in required:
        add_error(errors, path.is_file(), f"required file missing: {path.relative_to(PROJECT)}")

    manifests = {}
    for key, path in {
        "systematic_biology": SUBMISSION / "systematic_biology/MANIFEST.json",
        "journal_of_mathematical_biology": SUBMISSION / "journal_of_mathematical_biology/MANIFEST.json",
        "arxiv": SUBMISSION / "arxiv/MANIFEST.json",
    }.items():
        manifests[key] = validate_manifest(path, errors, blockers)

    # Every unresolved release token is a blocker, wherever it occurs in an
    # actual package or shared author metadata. Generic grammar examples are
    # documentation rather than release fields.
    token_locations: dict[str, set[str]] = defaultdict(set)
    scan_roots = [
        SUBMISSION / "AUTHOR_METADATA.json",
        SUBMISSION / "systematic_biology",
        SUBMISSION / "journal_of_mathematical_biology",
        SUBMISSION / "arxiv",
    ]
    scan_files: set[Path] = set()
    for root in scan_roots:
        if root.is_file():
            scan_files.add(root)
        elif root.is_dir():
            scan_files.update(p for p in root.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES)
    for path in sorted(scan_files):
        text = path.read_text(encoding="utf-8")
        for token in TOKEN_RE.findall(text):
            if token not in DOCUMENTATION_TOKENS:
                token_locations[token].add(str(path.relative_to(PROJECT)))
    for token, locations in sorted(token_locations.items()):
        blockers.append(f"unresolved @@{token}@@ in {', '.join(sorted(locations))}")

    author = load_json(SUBMISSION / "AUTHOR_METADATA.json", errors)
    authors = author.get("authors", [])
    add_error(errors, isinstance(authors, list) and len(authors) == 1,
              "author metadata must contain exactly one named author")
    if isinstance(authors, list) and authors:
        record = authors[0]
        add_error(errors, record.get("display_name") == "Alec Kriebel",
                  "author name differs from the canonical author")
        add_error(errors, record.get("orcid") == "https://orcid.org/0009-0001-9320-500X",
                  "ORCID differs from the supplied author metadata")
        add_error(errors, record.get("email") == "me@aleckriebel.com",
                  "corresponding email differs from the established publication metadata")
        add_error(errors, record.get("corresponding_author") is True,
                  "sole author is not marked as corresponding author")

    # Canonical-reuse locks.
    canonical_main = (PROJECT / "manuscript/main.tex").read_text(encoding="utf-8")
    canonical_abstract = extract_environment(canonical_main, "abstract")
    shared_abstract = (SUBMISSION / "shared/full_abstract.tex").read_text(encoding="utf-8").strip()
    add_error(errors, canonical_abstract == shared_abstract,
              "shared/full_abstract.tex has drifted from manuscript/main.tex")
    canonical_sections = re.findall(r"\\input\{sections/([^{}]+)\}", canonical_main)
    body_text = (SUBMISSION / "shared/canonical_article_body.tex").read_text(encoding="utf-8")
    wrapper_sections = re.findall(
        r"\\input\{\\KThreePCanonicalRoot/sections/([^{}]+)\}", body_text
    )
    add_error(errors, canonical_sections == wrapper_sections,
              "canonical_article_body.tex section order differs from manuscript/main.tex")
    add_error(errors, len(canonical_sections) == 17,
              f"expected 17 canonical sections, found {len(canonical_sections)}")

    # Systematic Biology policy checks.
    sb = (SUBMISSION / "systematic_biology/main_systematic_biology.tex").read_text(encoding="utf-8")
    sb_meta = load_json(SUBMISSION / "systematic_biology/metadata.json", errors)
    sb_cover = (SUBMISSION / "systematic_biology/cover_letter.md").read_text(encoding="utf-8")
    add_error(errors, "\\documentclass[12pt,twoside]{article}" in sb,
              "Systematic Biology wrapper is not 12pt")
    add_error(errors, "\\usepackage{lineno}" in sb and "\\linenumbers" in sb,
              "Systematic Biology wrapper lacks continuous line numbering")
    add_error(errors, "\\onehalfspacing" in sb or "\\doublespacing" in sb,
              "Systematic Biology wrapper lacks 1.5/double spacing")
    add_error(errors, "\\usepackage[margin=1in]{geometry}" in sb,
              "Systematic Biology wrapper lacks one-inch margins")
    add_error(errors, "\\raggedright" in sb,
              "Systematic Biology wrapper lacks ragged-right text")
    add_error(errors, "\\fancyfoot[C]{\\thepage}" in sb,
              "Systematic Biology wrapper lacks explicit consecutive page numbering")
    running = sb_meta.get("running_title", "")
    add_error(errors, isinstance(running, str) and 0 < len(running) <= 50,
              f"Systematic Biology running title length is {len(running) if isinstance(running, str) else 'invalid'}")
    sb_keywords = sb_meta.get("keywords", [])
    add_error(errors, isinstance(sb_keywords, list) and 4 <= len(sb_keywords) <= 8,
              "Systematic Biology requires four to eight keywords")
    ack_pos = sb.find("\\section*{Acknowledgments}")
    data_pos = sb.find("\\section*{Data Availability}")
    add_error(errors, 0 <= ack_pos < data_pos,
              "Systematic Biology Data Availability must follow Acknowledgments")
    add_error(errors, "Generative AI" in sb and "Generative AI" in sb_cover,
              "Systematic Biology AI use is not disclosed in both manuscript and cover letter")
    add_error(errors, "not be uploaded directly to ScholarOne" in sb,
              "Systematic Biology wrapper does not keep the Zenodo archive out of ScholarOne")
    add_error(errors, "Research Article" in sb and "Research Article" in sb_cover,
              "Systematic Biology article type is not consistently Research Article")
    add_error(errors, sb_meta.get("corresponding_email") == "me@aleckriebel.com"
              and "me@aleckriebel.com" in sb and "me@aleckriebel.com" in sb_cover,
              "Systematic Biology corresponding email is inconsistent")
    add_error(errors, latex_word_count(sb_cover) <= 600,
              "Systematic Biology cover-letter draft is too long for a one-page target")

    # Journal of Mathematical Biology policy checks.
    jmb = (SUBMISSION / "journal_of_mathematical_biology/main_jmb.tex").read_text(encoding="utf-8")
    jmb_meta = load_json(SUBMISSION / "journal_of_mathematical_biology/metadata.json", errors)
    jmb_cover = (SUBMISSION / "journal_of_mathematical_biology/cover_letter.md").read_text(encoding="utf-8")
    jmb_abstract = extract_environment(jmb, "abstract")
    jmb_words = latex_word_count(jmb_abstract or "")
    add_error(errors, 150 <= jmb_words <= 250,
              f"JMB abstract word count is {jmb_words}; required range is 150--250")
    jmb_keywords = jmb_meta.get("keywords", [])
    add_error(errors, isinstance(jmb_keywords, list) and 4 <= len(jmb_keywords) <= 6,
              "JMB requires four to six keywords")
    add_error(errors, isinstance(jmb_meta.get("msc_2020"), list) and bool(jmb_meta.get("msc_2020")),
              "JMB metadata lacks MSC codes")
    for heading in [
        "Statements and Declarations", "Funding", "Competing Interests",
        "Author Contributions", "Data Availability", "Code Availability",
        "Use of Large Language Models and Generative AI",
    ]:
        add_error(errors, heading in jmb, f"JMB wrapper lacks {heading!r}")
    add_error(errors, "Biological interpretation and accessibility" in jmb,
              "JMB wrapper lacks a biological-accessibility discussion")
    add_error(errors, "Online Resource 1" in jmb and ("ESM\\_1.pdf" in jmb or "ESM_1.pdf" in jmb),
              "JMB wrapper does not cite Online Resource 1 as ESM_1.pdf")
    add_error(errors, "Generative AI" in jmb_cover,
              "JMB cover letter lacks the AI disclosure")
    add_error(errors, jmb_meta.get("corresponding_email") == "me@aleckriebel.com"
              and "me@aleckriebel.com" in jmb and "me@aleckriebel.com" in jmb_cover,
              "JMB corresponding email is inconsistent")
    add_error(errors, latex_word_count(jmb_cover) <= 600,
              "JMB cover-letter draft is too long for a one-page target")

    # arXiv policy checks.
    arxiv = (SUBMISSION / "arxiv/main_arxiv.tex").read_text(encoding="utf-8")
    arxiv_readme = load_json(SUBMISSION / "arxiv/00README.json", errors)
    add_error(errors, arxiv_readme.get("spec_version") == 1,
              "arXiv 00README.json spec_version is not 1")
    add_error(errors, arxiv_readme.get("process", {}).get("compiler") == "pdflatex",
              "arXiv 00README.json does not select pdflatex")
    sources = arxiv_readme.get("sources", [])
    add_error(errors, sources == [{"filename": "main.tex", "usage": "toplevel"}],
              "arXiv 00README.json must name exactly main.tex as toplevel")
    add_error(errors, arxiv_readme.get("texlive_version") in {2023, 2025},
              "arXiv 00README.json requests an unsupported TeX Live version")
    add_error(errors, "\\today" not in arxiv,
              "arXiv wrapper uses the discouraged changing \\today date")
    add_error(errors, all(marker not in arxiv for marker in
                          ["\\onehalfspacing", "\\doublespacing", "\\linenumbers"]),
              "arXiv wrapper is inadvertently in referee mode")
    arxiv_manifest = manifests.get("arxiv", {})
    destinations = [entry.get("destination", "") for entry in arxiv_manifest.get("source_map", [])
                    if isinstance(entry, dict)]
    add_error(errors, all(not name.lower().endswith(".pdf") for name in destinations),
              "arXiv TeX source manifest includes a generated PDF")
    add_error(errors, "manuscript/references.bib" in destinations,
              "arXiv source manifest omits the BibTeX database")

    # No generated publication artifacts should exist yet in this source-only
    # workstream. Their absence is already a release blocker from the journal
    # manifests; their accidental presence here is a structural error.
    generated_suffixes = {".aux", ".blg", ".fdb_latexmk", ".fls", ".log", ".out", ".synctex.gz", ".toc"}
    for path in SUBMISSION.rglob("*"):
        if not path.is_file():
            continue
        lower = path.name.lower()
        if lower.endswith(".pdf") or any(lower.endswith(suffix) for suffix in generated_suffixes):
            errors.append(f"generated build product present in source staging: {path.relative_to(PROJECT)}")

    status, exit_code = package_status(errors, blockers)
    report = {
        "schema_version": 1,
        "status": status,
        "checked_project": PROJECT.name,
        "structural_error_count": len(errors),
        "structural_errors": sorted(set(errors)),
        "release_blocker_count": len(set(blockers)),
        "release_blockers": sorted(set(blockers)),
        "measurements": {
            "canonical_abstract_words": latex_word_count(canonical_abstract or ""),
            "jmb_abstract_words": jmb_words,
            "systematic_biology_running_title_characters": len(running) if isinstance(running, str) else None,
            "systematic_biology_keyword_count": len(sb_keywords) if isinstance(sb_keywords, list) else None,
            "jmb_keyword_count": len(jmb_keywords) if isinstance(jmb_keywords, list) else None,
            "systematic_biology_cover_letter_words": latex_word_count(sb_cover),
            "jmb_cover_letter_words": latex_word_count(jmb_cover),
        },
        "policy": "Every unresolved release token and every absent required release PDF produces NOT_READY; structural defects produce INVALID.",
    }
    return report, exit_code


def main() -> int:
    report, exit_code = validate()
    print(json.dumps(report, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
