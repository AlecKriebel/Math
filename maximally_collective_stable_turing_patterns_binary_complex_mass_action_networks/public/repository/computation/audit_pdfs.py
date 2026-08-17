#!/usr/bin/env python3
"""Check release PDFs for page-count, extraction, and semantic regressions."""

from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass(frozen=True)
class Document:
    relative_path: str
    pages: int
    semantic_text: bool = False


FULL_DOCUMENTS = (
    Document("manuscript/main.pdf", 16, True),
    Document("manuscript/supplement.pdf", 12, True),
    Document("external_audit/theorem_summary.pdf", 2, True),
    Document("external_audit/proof_skeleton.pdf", 5, True),
    Document("figures/network_family.pdf", 1),
    Document("figures/stable_tradeoff.pdf", 1),
    Document("figures/stable_profiles.pdf", 1),
    Document("figures/amplitude_scaling.pdf", 1),
)

PUBLIC_DOCUMENTS = tuple(
    document
    for document in FULL_DOCUMENTS
    if not document.relative_path.startswith("external_audit/")
)

FORBIDDEN_PHRASES = (
    "Theorem 3.1",
    "Theorems 4.1 and 5.1",
    "The shaded principal species set",
    "The marked point is",
    "python verify_symbolic_certificates.py",
)

SUPPLEMENT_SECTION_PREFIXES = (
    "Reaction matrices",
    "All-spectrum",
    "The principal-minor",
    "Order-",
    "Improved unit-equilibrium",
    "Conservation-compatible",
    "Equilibrium-scaled",
    "Exact coefficient",
    "Near-threshold",
    "Semilinear",
    "Numerical protocol",
)


def normalize(text: str) -> str:
    ligatures = {
        "ﬀ": "ff",
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
    }
    for glyph, expansion in ligatures.items():
        text = text.replace(glyph, expansion)
    return " ".join(text.split())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def embedded_fonts(reader: PdfReader) -> tuple[int, list[str]]:
    """Return the number of distinct page fonts and any unembedded names."""

    fonts: dict[tuple[str, str], bool] = {}
    font_file_keys = ("/FontFile", "/FontFile2", "/FontFile3")
    for page in reader.pages:
        resources = page.get("/Resources")
        if resources is None:
            continue
        font_dictionary = resources.get_object().get("/Font")
        if font_dictionary is None:
            continue
        for font_reference in font_dictionary.get_object().values():
            font = font_reference.get_object()
            identity = (str(font.get("/BaseFont", "unnamed")), str(font.get("/Subtype")))
            if identity in fonts:
                continue
            is_embedded = font.get("/Subtype") == "/Type3"
            descriptor = font.get("/FontDescriptor")
            if descriptor is not None:
                descriptor = descriptor.get_object()
                is_embedded = is_embedded or any(
                    descriptor.get(key) is not None for key in font_file_keys
                )
            descendants = font.get("/DescendantFonts")
            if descendants is not None:
                is_embedded = True
                for descendant_reference in descendants:
                    descendant = descendant_reference.get_object()
                    descendant_descriptor = descendant.get("/FontDescriptor")
                    if descendant_descriptor is None or not any(
                        descendant_descriptor.get_object().get(key) is not None
                        for key in font_file_keys
                    ):
                        is_embedded = False
            fonts[identity] = is_embedded
    missing = sorted(name for (name, _subtype), present in fonts.items() if not present)
    return len(fonts), missing


def audit(root: Path, output_dir: Path, documents: tuple[Document, ...]) -> None:
    failures: list[str] = []
    output_dir.mkdir(parents=True, exist_ok=True)
    report_names = [
        document.relative_path.replace("/", "_").replace(".", "_") + ".txt"
        for document in documents
    ]
    for report_name in (*report_names, "SUMMARY.txt"):
        (output_dir / report_name).unlink(missing_ok=True)

    extracted: dict[str, str] = {}
    for document in documents:
        path = root / document.relative_path
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing or empty PDF: {document.relative_path}")
            continue
        try:
            reader = PdfReader(path)
            if reader.is_encrypted:
                failures.append(f"encrypted PDF: {document.relative_path}")
                continue
            pages = len(reader.pages)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            font_count, missing_fonts = embedded_fonts(reader)
        except Exception as error:  # pypdf errors have several version-specific types.
            failures.append(f"unreadable PDF {document.relative_path}: {error}")
            continue

        if pages != document.pages:
            failures.append(
                f"page-count regression for {document.relative_path}: "
                f"expected {document.pages}, found {pages}"
            )
        if document.semantic_text and not text.strip():
            failures.append(f"no extractable text in {document.relative_path}")
        if missing_fonts:
            failures.append(
                f"unembedded fonts in {document.relative_path}: {', '.join(missing_fonts)}"
            )
        extracted[document.relative_path] = normalize(text)

        report_name = document.relative_path.replace("/", "_").replace(".", "_") + ".txt"
        report = (
            f"PDF: {document.relative_path}\n"
            f"SHA-256: {sha256(path)}\n"
            f"Pages: {pages}\n"
            "Encrypted: False\n"
            f"Extracted characters: {len(text)}\n"
            f"Distinct page fonts: {font_count}\n"
            "All page fonts embedded: True\n"
        )
        (output_dir / report_name).write_text(report, encoding="utf-8")

    semantic_corpus = " ".join(
        extracted.get(document.relative_path, "")
        for document in documents
        if document.semantic_text
    )
    for phrase in FORBIDDEN_PHRASES:
        if phrase in semantic_corpus:
            failures.append(f"forbidden rendered phrase: {phrase!r}")

    supplement = extracted.get("manuscript/supplement.pdf", "")
    if supplement:
        for section, title_prefix in enumerate(SUPPLEMENT_SECTION_PREFIXES, start=1):
            pattern = rf"(?:^|\s)S{section}\.?\s*{re.escape(title_prefix)}"
            if not re.search(pattern, supplement):
                failures.append(f"supplement lacks rendered S{section} section numbering")

    summary = output_dir / "SUMMARY.txt"
    if failures:
        summary.write_text("PDF_SEMANTIC_AUDIT_FAIL\n" + "\n".join(failures) + "\n")
        raise SystemExit("\n".join(failures))
    summary.write_text("PDF_SEMANTIC_AUDIT_PASS\n", encoding="utf-8")
    print("PDF_SEMANTIC_AUDIT_PASS")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=project_root)
    parser.add_argument("--profile", choices=("full", "public"), default="full")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    output_dir = args.output_dir
    if output_dir is None:
        output_dir = (
            root / "release" / "pdf_preflight"
            if args.profile == "full"
            else root / "verification_outputs" / "pdf_preflight"
        )
    documents = FULL_DOCUMENTS if args.profile == "full" else PUBLIC_DOCUMENTS
    audit(root, output_dir.resolve(), documents)


if __name__ == "__main__":
    main()
