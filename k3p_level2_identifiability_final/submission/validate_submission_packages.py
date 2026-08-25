#!/usr/bin/env python3
"""Fail-closed static gate for the draft submission source packages."""

from __future__ import annotations

import argparse
import hashlib
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
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_project_file(relative: object, errors: list[str], label: str) -> Path | None:
    if not isinstance(relative, str) or not relative:
        errors.append(f"{label} path is missing")
        return None
    value = Path(relative)
    if value.is_absolute() or ".." in value.parts or "." in value.parts:
        errors.append(f"unsafe {label} path: {relative!r}")
        return None
    path = PROJECT / value
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(PROJECT.resolve())
    except (OSError, ValueError):
        errors.append(f"unsafe or missing {label} path: {relative!r}")
        return None
    current = PROJECT.resolve()
    for part in value.parts:
        current = current / part
        if current.is_symlink():
            errors.append(f"symlink forbidden for {label}: {relative!r}")
            return None
    if not resolved.is_file():
        errors.append(f"{label} file missing: {relative}")
        return None
    return resolved


def safe_project_source(relative: object, mode: object, errors: list[str],
                        label: str) -> Path | None:
    if not isinstance(relative, str) or not relative:
        errors.append(f"{label} path is missing")
        return None
    value = Path(relative)
    if value.is_absolute() or ".." in value.parts or "." in value.parts:
        errors.append(f"unsafe {label} path: {relative!r}")
        return None
    path = PROJECT / value
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(PROJECT.resolve())
    except (OSError, ValueError):
        errors.append(f"unsafe or missing {label} path: {relative!r}")
        return None
    current = PROJECT.resolve()
    for part in value.parts:
        current = current / part
        if current.is_symlink():
            errors.append(f"symlink forbidden for {label}: {relative!r}")
            return None
    if mode == "copy_file" and not resolved.is_file():
        errors.append(f"copy_file source is not a regular file for {label}: {relative!r}")
        return None
    if mode == "copy_tree" and not resolved.is_dir():
        errors.append(f"copy_tree source is not a directory for {label}: {relative!r}")
        return None
    return resolved


def validate_upload(upload: object, package: str, errors: list[str],
                    blockers: list[str]) -> None:
    if not isinstance(upload, dict):
        errors.append(f"non-object portal upload for {package}")
        return
    filename = upload.get("filename")
    present = upload.get("present")
    if not isinstance(filename, str) or not filename:
        errors.append(f"portal upload filename missing for {package}")
    if not isinstance(present, bool):
        errors.append(f"portal upload present flag is not Boolean for {package}: {filename}")
        return
    if not present:
        blockers.append(f"release PDF/upload not yet produced for {package}: {filename}")
        return
    path = safe_project_file(upload.get("path"), errors,
                             f"portal upload {package}/{filename}")
    expected_hash = upload.get("sha256")
    expected_bytes = upload.get("bytes")
    if SHA256_RE.fullmatch(str(expected_hash)) is None:
        errors.append(f"portal upload SHA-256 missing or malformed for {package}: {filename}")
    if not isinstance(expected_bytes, int) or expected_bytes < 0:
        errors.append(f"portal upload byte count missing or malformed for {package}: {filename}")
    if path is not None:
        if isinstance(expected_bytes, int) and path.stat().st_size != expected_bytes:
            errors.append(f"portal upload byte count mismatch for {package}: {filename}")
        if SHA256_RE.fullmatch(str(expected_hash)) is not None and sha256_file(path) != expected_hash:
            errors.append(f"portal upload SHA-256 mismatch for {package}: {filename}")
        if path.suffix.lower() == ".pdf":
            qa = safe_project_file(upload.get("visual_qa_report"), errors,
                                   f"visual-QA report {package}/{filename}")
            qa_hash = upload.get("visual_qa_sha256")
            if SHA256_RE.fullmatch(str(qa_hash)) is None:
                errors.append(f"visual-QA SHA-256 missing or malformed for {package}: {filename}")
            elif qa is not None and sha256_file(qa) != qa_hash:
                errors.append(f"visual-QA SHA-256 mismatch for {package}: {filename}")
            if qa is not None:
                qa_data = load_json(qa, errors)
                required_qa_fields = {
                    "schema", "status", "pdf_path", "pdf_sha256", "pdf_bytes",
                    "page_count", "inspected_pages", "issues",
                }
                if set(qa_data) != required_qa_fields:
                    errors.append(f"visual-QA schema mismatch for {package}: {filename}")
                add_error(errors, qa_data.get("schema") == "k3p-pdf-visual-qa-v1" and
                          qa_data.get("status") == "PASS" and
                          qa_data.get("pdf_path") == upload.get("path") and
                          qa_data.get("pdf_sha256") == expected_hash and
                          qa_data.get("pdf_bytes") == expected_bytes and
                          isinstance(qa_data.get("page_count"), int) and
                          qa_data.get("page_count", 0) > 0 and
                          qa_data.get("inspected_pages") ==
                          list(range(1, qa_data.get("page_count", 0) + 1)) and
                          qa_data.get("issues") == [],
                          f"visual-QA report is not a complete PASS for {package}: {filename}")


def collect_token_locations(paths: set[Path]) -> dict[str, set[str]]:
    token_locations: dict[str, set[str]] = defaultdict(set)
    for path in sorted(paths):
        text = path.read_text(encoding="utf-8")
        for token in TOKEN_RE.findall(text):
            if token not in DOCUMENTATION_TOKENS:
                token_locations[token].add(str(path.relative_to(PROJECT)))
    return token_locations


def validate_manifest(path: Path, errors: list[str], blockers: list[str]) -> dict:
    data = load_json(path, errors)
    add_error(errors, data.get("schema_version") == 1,
              f"unsupported manifest schema: {path.relative_to(PROJECT)}")
    status = data.get("status")
    add_error(errors, status in {"DRAFT_NOT_READY", "READY"},
              f"unsupported manifest status: {path.relative_to(PROJECT)}")
    if status != "READY":
        blockers.append(f"manifest remains {status!r}: {path.relative_to(PROJECT)}")
    elif data.get("release_blockers") not in ([], None):
        errors.append(f"READY manifest retains release_blockers: {path.relative_to(PROJECT)}")
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
            mode = entry.get("mode", "copy_file")
            add_error(errors, mode in {"copy_file", "copy_tree"},
                      f"unknown source-map mode in {path.relative_to(PROJECT)}: {mode}")
            if mode in {"copy_file", "copy_tree"}:
                safe_project_source(
                    source, mode, errors,
                    f"manifest source in {path.relative_to(PROJECT)}",
                )
            dest_path = Path(destination)
            add_error(errors, bool(destination) and not dest_path.is_absolute()
                      and ".." not in dest_path.parts,
                      f"unsafe manifest destination {destination!r} in {path.relative_to(PROJECT)}")
            add_error(errors, destination not in destinations,
                      f"duplicate manifest destination {destination!r} in {path.relative_to(PROJECT)}")
            destinations.add(destination)
    uploads = data.get("initial_portal_uploads")
    if data.get("package") != "arxiv_source_staging":
        add_error(errors, isinstance(uploads, list) and bool(uploads),
                  f"manifest has no initial_portal_uploads: {path.relative_to(PROJECT)}")
    if isinstance(uploads, list):
        for upload in uploads:
            validate_upload(upload, str(data.get("package")), errors, blockers)
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
    scan_roots = [
        SUBMISSION / "AUTHOR_METADATA.json",
        SUBMISSION / "systematic_biology",
        SUBMISSION / "journal_of_mathematical_biology",
        SUBMISSION / "arxiv",
    ]
    for manifest in manifests.values():
        for entry in manifest.get("source_map", []) if isinstance(manifest, dict) else []:
            if isinstance(entry, dict) and isinstance(entry.get("source"), str):
                source_errors: list[str] = []
                source = safe_project_source(
                    entry["source"], entry.get("mode", "copy_file"), source_errors,
                    "manifest token-scan source",
                )
                if source is not None:
                    scan_roots.append(source)
    scan_files: set[Path] = set()
    for root in scan_roots:
        if root.is_file():
            scan_files.add(root)
        elif root.is_dir():
            scan_files.update(p for p in root.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES)
    token_locations = collect_token_locations(scan_files)
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
        "validator_sha256": sha256_file(Path(__file__).resolve()),
        "manifest_sha256": {
            str(path.relative_to(PROJECT)): sha256_file(path)
            for path in sorted([
                SUBMISSION / "systematic_biology/MANIFEST.json",
                SUBMISSION / "journal_of_mathematical_biology/MANIFEST.json",
                SUBMISSION / "arxiv/MANIFEST.json",
            ])
        },
    }
    report["payload_sha256"] = hashlib.sha256(json.dumps(
        report, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")).hexdigest()
    return report, exit_code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    report, exit_code = validate()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        output = args.output.resolve()
        try:
            output.relative_to(PROJECT)
        except ValueError as error:
            raise SystemExit(f"submission validation output outside project: {output}") from error
        temporary = output.with_suffix(output.suffix + ".tmp")
        temporary.write_text(rendered, encoding="utf-8")
        temporary.replace(output)
    print(rendered, end="")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
